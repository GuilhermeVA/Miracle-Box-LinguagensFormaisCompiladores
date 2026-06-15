from flask import Flask, jsonify, render_template, request, redirect, url_for
from miracle_compiler.compiler import codigo_miracle_box_3, resultado_compilacao
# Importa as funções que criamos na camada de persistência
from web.database import inicializar_banco, listar_musicas, buscar_musica_por_id, criar_musica, atualizar_codigo_musica, deletar_musica, editar_dados_musica

app = Flask(__name__)

# Garante a criação do banco de dados e da tabela quando o servidor rodar
inicializar_banco()

# TELA 1: Página Inicial (Home)
@app.get("/")
def index():
    return render_template("index.html")

# TELA 2: Dashboard de Músicas (Cards)
@app.get("/musicas")
def view_musicas():
    todas_musicas = listar_musicas()
    return render_template("musicas.html", musicas=todas_musicas)

# API: Endpoint para criação de novas músicas via formulário ou fetch
@app.post("/api/musicas")
def api_criar_musica():
    # Coleta os dados enviados pelo front
    titulo = request.form.get("titulo", "Nova Música")
    cor = request.form.get("cor", "#0f766e")  # Recebe o hex do seletor do front
    
    # Inicia a nova pasta de música com o código exemplo padrão que você já possui
    criar_musica(titulo, cor, codigo_inicial=codigo_miracle_box_3)
    
    return redirect(url_for("view_musicas"))

# TELA 3: IDE / Editor de Composição de uma música específica
@app.get("/composicao/<int:musica_id>")
def view_composicao(musica_id):
    musica = buscar_musica_por_id(musica_id)
    if not musica:
        return "Música não encontrada", 404
    
    # Renderiza o editor injetando o código guardado especificamente para este ID
    return render_template("composicao.html", musica=musica)

# API: Endpoint para salvar alterações no código .mrcb sem recarregar a tela
@app.post("/api/musicas/salvar/<int:musica_id>")
def api_salvar_musica(musica_id):
    dados = request.get_json(silent=True) or {}
    codigo = dados.get("codigo")
    
    if codigo is None:
        return jsonify({"erro": "O código não pode ser nulo."}), 400
        
    atualizar_codigo_musica(musica_id, codigo)
    return jsonify({"sucesso": True, "mensagem": "Música salva com sucesso!"})


# API: Endpoint para deletar uma música
@app.post("/api/musicas/deletar/<int:musica_id>")
def api_deletar_musica(musica_id):
    deletar_musica(musica_id)
    return redirect(url_for("view_musicas"))

# API: Endpoint para editar metadados (Título e Cor) da música
@app.post("/api/musicas/editar/<int:musica_id>")
def api_editar_musica(musica_id):
    novo_titulo = request.form.get("titulo")
    nova_cor = request.form.get("cor")
    
    if novo_titulo and nova_cor:
        editar_dados_musica(musica_id, novo_titulo, nova_cor)
        
    return redirect(url_for("view_musicas"))




# COMPILADOR: Mantido exatamente original, isolado das modificações de persistência
@app.post("/compilar")
def compilar_codigo():
    dados = request.get_json(silent=True) or {}
    codigo = dados.get("codigo", "")

    if not isinstance(codigo, str):
        return jsonify({"erro": "campo 'codigo' deve ser texto"}), 400

    return jsonify(resultado_compilacao(codigo))

if __name__ == "__main__":
    app.run(debug=True)