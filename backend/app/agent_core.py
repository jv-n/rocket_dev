import os
import re
import sqlite3
import textwrap
from dataclasses import dataclass

import pandas as pd
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from app.config import settings

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "banco.db"))
MAX_ROWS = 500
SAMPLE_ROWS_PER_TABLE = 3

FORBIDDEN_PATTERN = re.compile(
    r"\b(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|REPLACE|TRUNCATE|ATTACH|DETACH|PRAGMA|VACUUM|REINDEX)\b",
    re.IGNORECASE,
)

SYSTEM_PROMPT = textwrap.dedent("""
    You are a senior data analyst working over a SQLite e-commerce database.
    Your users are non-technical, they want clear answers, not raw data dumps.

    WORKFLOW (follow this every turn):
      1. Call `inspect_schema` ONCE to discover the real tables, columns, and sample rows.
         Never invent table or column names — always verify against the schema.
      2. Write ONE SQLite SELECT (or WITH ... SELECT) query. Use SQLite-specific functions
         (strftime, julianday, date(), substr, etc.) — NOT MySQL/Postgres-specific syntax.
      3. Call `execute_query` to run it. If it errors, read the error, fix the SQL, and retry
         (up to 3 attempts). Only after 3 failures should you apologise to the user.
      4. Produce a concise answer:
           - One sentence stating the main result as assumed by your search.
           - A brief insight if relevant (trend, outlier, caveat).
           - A small markdown table when it helps (for top-N, breakdowns, etc.).
           - At the end, include the SQL you ran inside a ```sql code block, for auditability.

    RULES:
      - Read-only queries only. Never attempt INSERT, UPDATE, DELETE, or DDL.
      - Apply LIMIT for ranking / top-N questions (default 10 if unspecified).
      - For rates/percentages, round to 2 decimals and use CAST(... AS FLOAT) to avoid
        integer division.
      - When joining, prefer explicit JOIN ... ON ... over comma joins.
      - If a question is genuinely ambiguous, ask ONE short clarifying question. Otherwise
        pick the most reasonable interpretation and state the assumption in your answer.
      - Reply in the SAME language the user used (Portuguese, English, etc.).
""").strip()

@dataclass
class DBDeps:
    db_path: str = DB_PATH


def get_database_schema(db_path: str = DB_PATH) -> str:
    """Return a description of all tables, their CREATE statements, and sample rows."""
    with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name;"
        )
        tables = [r[0] for r in cur.fetchall()]

        parts = [f"Database has {len(tables)} tables: {', '.join(tables)}", ""]
        for t in tables:
            cur.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name = ?;", (t,)
            )
            create_stmt = (cur.fetchone() or [""])[0] or ""

            sample = pd.read_sql_query(
                f'SELECT * FROM "{t}" LIMIT {SAMPLE_ROWS_PER_TABLE};', conn
            )

            parts.append(f"### Table: {t}")
            parts.append(create_stmt.strip() + ";")
            parts.append(f"-- sample rows (up to {SAMPLE_ROWS_PER_TABLE}):")
            parts.append(
                sample.to_string(index=False) if not sample.empty else "(empty table)"
            )
            parts.append("")

    return "\n".join(parts)


def run_select_query(sql: str, db_path: str = DB_PATH, max_rows: int = MAX_ROWS) -> str:
    """Execute a read-only SELECT/WITH query and return a markdown table string."""
    q = sql.strip().rstrip(";").strip()
    if not q:
        return "ERROR: empty query."
    if FORBIDDEN_PATTERN.search(q):
        return "ERROR: only read-only queries are allowed (no INSERT/UPDATE/DELETE/DROP/DDL)."
    if not re.match(r"^\s*(select|with)\b", q, re.IGNORECASE):
        return "ERROR: query must start with SELECT or WITH."
    try:
        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True) as conn:
            df = pd.read_sql_query(q, conn)
    except Exception as e:
        return f"ERROR executing query: {e}"

    truncated = len(df) > max_rows
    if truncated:
        df = df.head(max_rows)

    body = df.to_markdown(index=False) if not df.empty else "(no rows returned)"
    footer = f"\n\n[result truncated to first {max_rows} rows]" if truncated else ""
    header = f"{len(df)} row(s) returned. Columns: {list(df.columns)}\n\n"
    return header + body + footer


agent = Agent(
    model=GoogleModel("gemini-2.5-flash-lite", provider=GoogleProvider(api_key=settings.gemnini_api_key)),
    deps_type=DBDeps,
    system_prompt=SYSTEM_PROMPT,
    retries=2,
)


@agent.tool
def inspect_schema(ctx: RunContext[DBDeps]) -> str:
    """Return the full schema and sample rows for every table. Call this before writing any SQL."""
    return get_database_schema(ctx.deps.db_path)


@agent.tool
def execute_query(ctx: RunContext[DBDeps], sql: str) -> str:
    """Execute a read-only SQLite SELECT (or WITH ... SELECT) and return results as markdown."""
    return run_select_query(sql, ctx.deps.db_path)
