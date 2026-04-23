# routers/agent_router.py
import re, uuid
from dataclasses import dataclass
from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_ai import Agent, RunContext
from pydantic_ai.messages import ModelMessage

from ..agent_core import agent, DBDeps, DB_PATH   

router = APIRouter(prefix="/api/agent", tags=["agent"])

_sessions: dict[str, list[ModelMessage]] = {}

class ChatRequest(BaseModel):
    session_id: str | None = None
    question: str

class ChatResponse(BaseModel):
    session_id: str
    answer: str
    sql_calls: list[str]


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    history = _sessions.get(session_id, [])

    deps = DBDeps(db_path=DB_PATH)
    result = await agent.run(req.question, deps=deps, message_history=history)

    _sessions[session_id] = result.all_messages()

    sql_calls = [
        (part.args if isinstance(part.args, dict) else {}).get("sql", "")
        for msg in result.all_messages()
        for part in getattr(msg, "parts", [])
        if getattr(part, "part_kind", None) == "tool-call"
        and part.tool_name == "execute_query"
    ]

    return ChatResponse(
        session_id=session_id,
        answer=result.output,
        sql_calls=sql_calls,
    )


@router.delete("/chat/{session_id}")
async def clear_session(session_id: str):
    _sessions.pop(session_id, None)
    return {"ok": True}
