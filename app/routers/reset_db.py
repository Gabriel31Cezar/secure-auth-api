# reset_db.py
"""
Script utilitário para limpar completamente todos os registros do banco de dados
sem a necessidade de remover o arquivo .db.
"""

from app.database import SessionLocal
from app.models import User
from app.filesearch.models import IndexedFile


def reset_database():
    print("Iniciando a limpeza do banco de dados...")
    db = SessionLocal()
    try:
        # 1. Apaga os registros das tabelas
        num_files = db.query(IndexedFile).delete()
        num_users = db.query(User).delete()

        # 2. Confirma as alterações na base de dados
        db.commit()

        print("--- BANCO DE DADOS LIMPO COM SUCESSO ---")
        print(f"• Registros de arquivos removidos: {num_files}")
        print(f"• Usuários removidos: {num_users}")

    except Exception as e:
        db.rollback()
        print(f"Erro ao tentar limpar o banco de dados: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    reset_database()