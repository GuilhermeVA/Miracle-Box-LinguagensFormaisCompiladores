from flask import Flask, jsonify, render_template, request

from miracle_compiler.compiler import codigo_miracle_box_3, resultado_compilacao


app = Flask(__name__)


@app.get("/")
def index():
    return render_template("index.html", exemplo_padrao=codigo_miracle_box_3)


@app.post("/compilar")
def compilar_codigo():
    dados = request.get_json(silent=True) or {}
    codigo = dados.get("codigo", "")

    if not isinstance(codigo, str):
        return jsonify({"erro": "campo 'codigo' deve ser texto"}), 400

    return jsonify(resultado_compilacao(codigo))


if __name__ == "__main__":
    app.run(debug=True)
