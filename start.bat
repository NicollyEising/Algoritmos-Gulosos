@echo off

REM Instala as dependências do backend (Python)
echo Instalando dependências do backend...
pip install -r requirements.txt

REM Verifica se as dependências do frontend já estão instaladas, se não, instala
if not exist "caminho-cidades\node_modules" (
    echo Instalando dependências do frontend...
    cd caminho-cidades
    npm install
    cd ..
)

REM Inicia o backend (API com FastAPI)
echo Iniciando o backend...
cd src
start uvicorn main:app --host 0.0.0.0 --port 8000
cd ..

REM Inicia o frontend (seu aplicativo React ou similar)
echo Iniciando o frontend...
cd caminho-cidades
npm start

