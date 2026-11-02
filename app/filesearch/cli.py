# app/filesearch/cli.py
import argparse
import sys
from datetime import datetime
from pathlib import Path

# Importações do nosso projeto
from app.database import SessionLocal
from app.filesearch.services.indexer import FileIndexer
from app.filesearch.services.search_engine import SearchEngine


def cmd_scan(args):
    """Executa a varredura de uma pasta."""
    target_dir = Path(args.path)
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ Erro: O caminho '{target_dir}' não existe ou não é uma pasta.")
        sys.exit(1)

    print(f"🔍 Iniciando varredura em: {target_dir.resolve()}")
    db = SessionLocal()
    try:
        indexer = FileIndexer(db)
        indexer.index_directory(target_dir)
        print("✅ Varredura concluída com sucesso!")
    except Exception as e:
        print(f"❌ Erro durante a varredura: {e}")
    finally:
        db.close()


def cmd_search(args):
    """Executa a busca no banco."""
    db = SessionLocal()
    try:
        engine = SearchEngine(db)

        date_from = None
        if args.since:
            try:
                date_from = datetime.strptime(args.since, "%Y-%m-%d")
            except ValueError:
                print("❌ Erro: Formato de data inválido. Use YYYY-MM-DD.")
                sys.exit(1)

        print(f"🔎 Buscando... (Filtros: termo='{args.query}', camera='{args.camera}', desde='{args.since}')")

        results = engine.search(
            query_text=args.query,
            camera_make=args.camera,
            date_from=date_from,
            limit=args.limit
        )

        if not results:
            print("Nenhuma imagem encontrada.")
            return

        print(f"\n✨ Encontradas {len(results)} imagens:")
        print("-" * 60)
        for img in results:
            # Pega só o final do caminho para ficar bonito no terminal
            short_path = Path(img.path).name
            camera_info = f"{img.camera_make or '?'} {img.camera_model or ''}".strip()
            date_info = img.taken_at.strftime("%Y-%m-%d") if img.taken_at else "Sem data"
            print(f"📸 {short_path}")
            print(f"   📁 Caminho: .../{img.path[-50:]}")
            print(f"   📷 Câmera: {camera_info}")
            print(f"   📅 Data:   {date_info}")
            print("-" * 60)

    except Exception as e:
        print(f"❌ Erro durante a busca: {e}")
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description="Motor de Busca de Imagens (Filesearch CLI)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Comando: scan
    parser_scan = subparsers.add_parser("scan", help="Varre e indexa uma pasta de imagens")
    parser_scan.add_argument("path", type=str, help="Caminho da pasta a ser varrida")
    parser_scan.set_defaults(func=cmd_scan)

    # Comando: search
    parser_search = subparsers.add_parser("search", help="Busca imagens no banco de dados")
    parser_search.add_argument("query", type=str, nargs="?", default=None, help="Termo para buscar no nome ou caminho")
    parser_search.add_argument("--camera", type=str, help="Filtrar por fabricante da câmera (ex: Canon)")
    parser_search.add_argument("--since", type=str, help="Filtrar por data de captura (Formato: YYYY-MM-DD)")
    parser_search.add_argument("--limit", type=int, default=10, help="Limite de resultados (padrão: 10)")
    parser_search.set_defaults(func=cmd_search)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()