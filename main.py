from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sqlite3
import os

app = FastAPI()
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/mangas")
def listar_mangas():
    try:
        conn = sqlite3.connect('mangas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, volume, editora FROM colecao")
        mangas = cursor.fetchall()
        conn.close()
        lista_final = [
            {"id": m[0], "titulo": m[1], "volume": m[2], "editora": m[3]} 
            for m in mangas
        ]
        return {"colecao": lista_final}
    except Exception as e:
        print(f"Erro ao listar: {e}")
        return {"colecao": [], "error": str(e)}

@app.post("/mangas")
def cadastrar_manga(titulo: str, volume: int, editora: str):
    if not titulo or not volume:
        raise HTTPException(status_code=400, detail="Dados incompletos")
    
    try:
        conn = sqlite3.connect('mangas.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM colecao WHERE titulo = ? AND volume = ?", (titulo, volume))
        if cursor.fetchone():
            conn.close()
            raise HTTPException(status_code=400, detail="Volume já cadastrado!")

        cursor.execute("INSERT INTO colecao (titulo, volume, editora) VALUES (?, ?, ?)", (titulo, volume, editora))
        conn.commit()
        conn.close()
        return {"message": "Sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/mangas/{manga_id}")
def excluir_manga(manga_id: int):
    try:
        conn = sqlite3.connect('mangas.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM colecao WHERE id = ?", (manga_id,))
        conn.commit()
        conn.close()
        return {"message": "Removido!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# ==========================================
# ROTA DE BUSCA (Consulta por ID ou Nome)
# ==========================================
@app.get("/mangas/buscar")
def buscar_manga(termo: str):
    try:
        conn = sqlite3.connect('mangas.db')
        cursor = conn.cursor()
        
        # Se o usuário digitou um número, busca por ID. Se foi texto, busca por Título (usando LIKE).
        if termo.isdigit():
            cursor.execute("SELECT id, titulo, volume, editora FROM colecao WHERE id = ?", (int(termo),))
        else:
            # O % permite achar "Naruto" mesmo se a pessoa digitar só "Naru"
            cursor.execute("SELECT id, titulo, volume, editora FROM colecao WHERE titulo LIKE ?", ('%' + termo + '%',))
            
        mangas = cursor.fetchall()
        conn.close()
        
        lista_final = [{"id": m[0], "titulo": m[1], "volume": m[2], "editora": m[3]} for m in mangas]
        return {"colecao": lista_final}
    except Exception as e:
        return {"colecao": [], "error": str(e)}

# ==========================================
# ROTA DE EDIÇÃO (Update)
# ==========================================
@app.put("/mangas/{manga_id}")
def editar_manga(manga_id: int, titulo: str, volume: int, editora: str):
    try:
        conn = sqlite3.connect('mangas.db')
        cursor = conn.cursor()
        
        # Atualiza os dados onde o ID for igual ao selecionado
        cursor.execute("UPDATE colecao SET titulo = ?, volume = ?, editora = ? WHERE id = ?", (titulo, volume, editora, manga_id))
        conn.commit()
        conn.close()
        return {"message": "Mangá atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))