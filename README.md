# Rodando

1. Rode a API no backend

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```
Faça a seed do banco de dados antes:

1. Adicione um diretório **```data```** a raiz do backend
2. Adicione os arquivos **.csv** ao diretório ```data```

Rode o script no terminal: 
```bash
python seed.py
```
Agora rode a API

```bash
python -m app.main
```
2. Rode o frontend
```bash
cd ..\frontend
pnpm i
pnpm run dev
```
E entre no localhost! Pronto!
