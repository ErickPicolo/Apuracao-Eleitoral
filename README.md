# Dashboard de Apuração Eleitoral (CP-5)

Projeto desenvolvido para visualização em tempo real da apuração eleitoral no Brasil (2º turno).

## Tecnologias
* Backend: Python + FastAPI
* Banco de dados: MongoDB
* Mapas e Interface: Leaflet.js e Tailwind CSS

## Como rodar localmente

1. Instalar as dependências:
   pip install -r requirements.txt

2. Garantir que o MongoDB está a rodar na porta padrão (27017).

3. Iniciar o servidor FastAPI:
   uvicorn api:app --reload

4. Abrir no navegador:
   http://127.0.0.1:8000
