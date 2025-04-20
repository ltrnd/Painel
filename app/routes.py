from flask import Blueprint, request, jsonify, current_app
from datetime import datetime
import os
import logging

bp = Blueprint("routes", __name__)

comando = {"comando": None}
localizacao = {"latitude": None, "longitude": None, "timestamp": None}

logging.basicConfig(level=logging.INFO)

@bp.route("/enviar", methods=["POST"])
def receber_localizacao():
    data = request.get_json()
    localizacao["latitude"] = data.get("latitude")
    localizacao["longitude"] = data.get("longitude")
    localizacao["timestamp"] = data.get("timestamp")
    logging.info(f"Localização recebida: {localizacao}")
    return jsonify({"status": "ok", "mensagem": "Localização recebida com sucesso!"})

@bp.route("/localizacao", methods=["GET"])
def enviar_localizacao():
    return jsonify(localizacao)

@bp.route("/comando", methods=["GET", "POST"])
def gerenciar_comando():
    global comando
    if request.method == "POST":
        data = request.get_json()
        comando["comando"] = data.get("comando")
        logging.info(f"Comando recebido: {comando['comando']}")
        return jsonify({"status": "ok", "mensagem": "Comando atualizado"})
    return jsonify(comando)

@bp.route("/upload", methods=["POST"])
def upload_arquivo():
    if "arquivo" not in request.files:
        return jsonify({"status": "erro", "mensagem": "Nenhum arquivo enviado"}), 400

    file = request.files["arquivo"]
    if file.filename == "":
        return jsonify({"status": "erro", "mensagem": "Arquivo sem nome"}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{file.filename}"
    caminho = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(caminho)

    logging.info(f"Arquivo salvo: {caminho}")
    return jsonify({"status": "ok", "mensagem": f"Arquivo salvo como {filename}"})
