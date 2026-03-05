"""
NASA APOD - Backend API
Retorna a foto do dia da NASA para uma data específica (ex: aniversário)
"""
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import requests
import urllib3
from dotenv import load_dotenv

# Suprime aviso de SSL desabilitado (necessário em redes corporativas)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

# Carrega .env da pasta do backend
_env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=_env_path)
load_dotenv()  # fallback: carrega do diretório atual

app = Flask(__name__, static_folder=None)
CORS(app)

# Caminho para o frontend (pasta irmã)
FRONTEND_PATH = Path(__file__).resolve().parent.parent / "frontend"

# NASA API Key - várias tentativas de carregamento
NASA_API_KEY = (
    os.getenv("NASA_API_KEY")
    or os.environ.get("NASA_API_KEY")
    or _carregar_chave_do_env(_env_path)
)
APOD_URL = "https://api.nasa.gov/planetary/apod"


def _carregar_chave_do_env(env_path: Path) -> Optional[str]:
    """Lê NASA_API_KEY diretamente do arquivo .env."""
    if not env_path.exists():
        return None
    try:
        texto = env_path.read_text(encoding="utf-8-sig")
        for linha in texto.strip().splitlines():
            linha = linha.strip()
            if linha.startswith("#") or "=" not in linha:
                continue
            chave, valor = linha.split("=", 1)
            if chave.strip() == "NASA_API_KEY":
                return valor.strip().strip('"\'')
    except Exception:
        pass
    return None


def validar_data(data_str: str) -> Tuple[bool, str]:
    """Valida se a data está no formato correto e dentro do intervalo da API."""
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        # APOD começa em 16 de junho de 1995
        data_minima = datetime(1995, 6, 16)
        data_maxima = datetime.now()
        
        if data < data_minima:
            return False, "A NASA começou a publicar fotos em 16 de junho de 1995. Escolha uma data depois disso!"
        if data > data_maxima:
            return False, "Essa data ainda não chegou! Escolha uma data de hoje ou do passado."
        
        return True, ""
    except ValueError:
        return False, "Data inválida. Use o formato: dia/mês/ano (ex: 15/01/2000)"


@app.route("/api/apod", methods=["GET"])
def obter_apod():
    """
    Obtém a foto do dia da NASA para uma data específica.
    Parâmetro: date (YYYY-MM-DD)
    """
    data_param = request.args.get("date")
    
    if not data_param:
        return jsonify({
            "erro": True,
            "mensagem": "Por favor, informe uma data no formato ano-mês-dia (ex: 2000-01-15)"
        }), 400
    
    valido, mensagem_erro = validar_data(data_param)
    if not valido:
        return jsonify({
            "erro": True,
            "mensagem": mensagem_erro
        }), 400
    
    if not NASA_API_KEY:
        return jsonify({
            "erro": True,
            "mensagem": "Chave da API NASA não configurada. Verifique o arquivo .env"
        }), 500
    
    try:
        resposta = requests.get(
            APOD_URL,
            params={"date": data_param, "api_key": NASA_API_KEY},
            timeout=10,
            verify=False
        )
        resposta.raise_for_status()
        dados = resposta.json()
        
        return jsonify({
            "erro": False,
            "data": {
                "titulo": dados.get("title", "Sem título"),
                "descricao": dados.get("explanation", ""),
                "url_imagem": dados.get("url"),
                "url_imagem_hd": dados.get("hdurl"),
                "data": dados.get("date"),
                "tipo_midia": dados.get("media_type", "image"),
                "copyright": dados.get("copyright", "NASA")
            }
        })
    
    except requests.exceptions.Timeout:
        return jsonify({
            "erro": True,
            "mensagem": "A NASA está demorando para responder. Tente novamente em alguns segundos!"
        }), 504
    except requests.exceptions.RequestException as e:
        return jsonify({
            "erro": True,
            "mensagem": f"Não foi possível buscar a foto. Erro: {str(e)}"
        }), 502


@app.route("/api/saude", methods=["GET"])
def health_check():
    """Verifica se a API está funcionando."""
    return jsonify({"status": "ok", "mensagem": "API NASA APOD funcionando!"})


@app.route("/")
def index():
    """Serve a página principal do frontend."""
    return send_from_directory(FRONTEND_PATH, "index.html")


@app.route("/<path:path>")
def servir_frontend(path):
    """Serve arquivos estáticos do frontend (CSS, JS, etc)."""
    return send_from_directory(FRONTEND_PATH, path)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
