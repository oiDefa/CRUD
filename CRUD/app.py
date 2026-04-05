from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

ARQUIVO_JSON = "musicas.json"


def carregar_musicas():
    if not os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(ARQUIVO_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_musicas(musicas):
    with open(ARQUIVO_JSON, "w", encoding="utf-8") as f:
        json.dump(musicas, f, ensure_ascii=False, indent=4)


@app.route("/")
def inicio():
    return jsonify({
        "mensagem": "API de musicas funcionando!"
    })


# cadastrar musica
@app.route("/musicas", methods=["POST"])
def cadastrar_musica():
    musicas = carregar_musicas()
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Nenhum dado enviado"}), 400

    titulo = dados.get("titulo")
    artista = dados.get("artista")
    album = dados.get("album")
    ano = dados.get("ano")

    if not titulo or not artista:
        return jsonify({"erro": "Os campos 'titulo' e 'artista' são obrigatórios"}), 400

    if musicas:
        novo_id = max(m["id"] for m in musicas) + 1
    else:
        novo_id = 1

    nova_musica = {
        "id": novo_id,
        "titulo": titulo,
        "artista": artista,
        "album": album,
        "ano": ano
    }

    musicas.append(nova_musica)
    salvar_musicas(musicas)

    return jsonify({
        "mensagem": "Música cadastrada com sucesso",
        "musica": nova_musica
    }), 201


# listar todas
@app.route("/musicas", methods=["GET"])
def listar_musicas():
    musicas = carregar_musicas()
    return jsonify(musicas), 200


# buscar  por id
@app.route("/musicas/<int:id>", methods=["GET"])
def buscar_musica(id):
    musicas = carregar_musicas()

    for musica in musicas:
        if musica["id"] == id:
            return jsonify(musica), 200

    return jsonify({"erro": "Música não encontrada"}), 404


# atualizar música
@app.route("/musicas/<int:id>", methods=["PUT"])
def atualizar_musica(id):
    musicas = carregar_musicas()
    dados = request.get_json()

    for musica in musicas:
        if musica["id"] == id:
            musica["titulo"] = dados.get("titulo", musica["titulo"])
            musica["artista"] = dados.get("artista", musica["artista"])
            musica["album"] = dados.get("album", musica["album"])
            musica["ano"] = dados.get("ano", musica["ano"])

            salvar_musicas(musicas)

            return jsonify({
                "mensagem": "Música atualizada com sucesso",
                "musica": musica
            }), 200

    return jsonify({"erro": "Música não encontrada"}), 404


# excluir musica
@app.route("/musicas/<int:id>", methods=["DELETE"])
def excluir_musica(id):
    musicas = carregar_musicas()

    for musica in musicas:
        if musica["id"] == id:
            musicas.remove(musica)
            salvar_musicas(musicas)

            return jsonify({"mensagem": "Música excluída com sucesso"}), 200

    return jsonify({"erro": "Música não encontrada"}), 404


if __name__ == "__main__":
    app.run(debug=True)