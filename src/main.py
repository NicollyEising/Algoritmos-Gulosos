import firebase_admin  
from firebase_admin import credentials, firestore
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict
import unicodedata
import logging

# Configuração do logging
logging.basicConfig(level=logging.DEBUG)  # Define o nível de log como DEBUG
logger = logging.getLogger(__name__)

# Inicialize o Firebase Admin SDK com as credenciais
cred = credentials.Certificate(r"C:\Users\faculdade\Desktop\Nova pasta\Algoritmos Gulosos\config\algoritmosgulosos-firebase-adminsdk-fbsvc-8e7d3a0335.json")
firebase_admin.initialize_app(cred)

# Referência ao Firestore
db = firestore.client()

# Configuração do FastAPI
app = FastAPI()

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, defina os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Manipulador explícito para OPTIONS
@app.options("/caminho")
async def options_caminho():
    return Response(status_code=200)

# Função para normalizar a string (remove acentos)
def normalizar_string(s: str) -> str:
    return ''.join(
        c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'
    ).lower()

# Função para pegar as cidades e distâncias do Firestore
def get_cidades_from_firestore() -> Dict:
    cidades_ref = db.collection("cities")
    cidades = {}
    for doc in cidades_ref.stream():
        # Log: Exibe os ids dos documentos encontrados
        logger.debug(f"Documento encontrado: {doc.id}")  # Verifique se o id está correto
        cidades[normalizar_string(doc.id)] = doc.to_dict()  # Converte para lowercase e normaliza
    logger.debug(f"Cidades carregadas: {cidades}")  # Mostra todas as cidades carregadas
    return cidades

# Algoritmo guloso para encontrar o caminho
def caminho_guloso(origem: str, destino: str) -> Dict:
    origem = normalizar_string(origem)  # Normaliza a cidade de origem
    destino = normalizar_string(destino)  # Normaliza a cidade de destino
    cidades = get_cidades_from_firestore()  # Pega as cidades do Firestore

    if origem not in cidades:
        return {"erro": f"Cidade de origem '{origem}' não encontrada."}
    
    caminho = [origem]  # Inicia o caminho com a cidade de origem
    distancia_total = 0
    cidade_atual = origem
    visitadas = {origem}  # Conjunto para evitar ciclos

    while cidade_atual != destino:
        if cidade_atual not in cidades:
            return {"erro": f"Cidade '{cidade_atual}' não encontrada no banco de dados."}
        
        vizinhos = cidades[cidade_atual]
        # Converte os nomes dos vizinhos para lowercase e filtra os já visitados
        vizinhos_filtrados = {normalizar_string(cidade): dist for cidade, dist in vizinhos.items() if normalizar_string(cidade) not in visitadas}
        
        if not vizinhos_filtrados:
            return {"erro": f"Não há caminho disponível a partir da cidade '{cidade_atual}' para chegar em '{destino}'."}
        
        # Seleciona o vizinho com a menor distância (decisão gulosa)
        proxima_cidade = min(vizinhos_filtrados, key=vizinhos_filtrados.get)
        distancia = vizinhos_filtrados[proxima_cidade]
        
        caminho.append(proxima_cidade)
        distancia_total += distancia
        cidade_atual = proxima_cidade
        visitadas.add(proxima_cidade)
    
    return {"caminho": caminho, "distancia_total": distancia_total}

# Modelo de requisição
class Requisicao(BaseModel):
    origem: str
    destino: str

@app.post("/caminho")
async def calcular_caminho(requisicao: Requisicao):
    origem = requisicao.origem
    destino = requisicao.destino
    resultado = caminho_guloso(origem, destino)
    return resultado
