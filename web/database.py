import sqlite3
import os

# Define o caminho do banco de dados dentro do diretório web
DB_PATH = os.path.join(os.path.dirname(__file__), "miracle_box.db")

def obter_conexao():
    """Abre uma conexão com o banco de dados e retorna dicionários nas linhas."""
    conexao = sqlite3.connect(DB_PATH)
    conexao.row_factory = sqlite3.Row  # Permite acessar colunas pelo nome: musica['titulo']
    return conexao

def inicializar_banco():
    """Cria a tabela de músicas com o campo personalizado de cor se não existir."""
    query_tabela = """
    CREATE TABLE IF NOT EXISTS musicas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        codigo_mrcb TEXT,
        cor TEXT DEFAULT '#0f766e'
    );
    """
    with obter_conexao() as conn:
        conn.execute(query_tabela)
        conn.commit()

# Funções auxiliares para manipulação das músicas

def listar_musicas():
    with obter_conexao() as conn:
        return conn.execute("SELECT id, titulo, codigo_mrcb, cor FROM musicas").fetchall()

def buscar_musica_por_id(musica_id):
    with obter_conexao() as conn:
        return conn.execute("SELECT id, titulo, codigo_mrcb, cor FROM musicas WHERE id = ?", (musica_id,)).fetchone()

def criar_musica(titulo, cor, codigo_inicial=""):
    with obter_conexao() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO musicas (titulo, cor, codigo_mrcb) VALUES (?, ?, ?)",
            (titulo, cor, codigo_inicial)
        )
        conn.commit()
        return cursor.lastrowid

def atualizar_codigo_musica(musica_id, novo_codigo):
    with obter_conexao() as conn:
        conn.execute(
            "UPDATE musicas SET codigo_mrcb = ? WHERE id = ?",
            (novo_codigo, musica_id)
        )
        conn.commit()


def deletar_musica(musica_id):
    """Remove uma música do banco de dados pelo ID."""
    with obter_conexao() as conn:
        conn.execute("DELETE FROM musicas WHERE id = ?", (musica_id,))
        conn.commit()

def editar_dados_musica(musica_id, novo_titulo, nova_cor):
    """Atualiza apenas o título e a cor de uma música existente."""
    with obter_conexao() as conn:
        conn.execute(
            "UPDATE musicas SET titulo = ?, cor = ? WHERE id = ?",
            (novo_titulo, nova_cor, musica_id)
        )
        conn.commit()