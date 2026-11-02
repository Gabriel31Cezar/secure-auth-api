# app/routers/filesearch.py
from datetime import datetime
from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.filesearch.services.indexer import FileIndexer
from app.filesearch.services.search_engine import SearchEngine
from app.security import get_current_user

router = APIRouter(
    prefix="/filesearch",
    tags=["Filesearch"]
)


@router.post("/scan", response_model=schemas.ScanResponse)
def scan_directory(
        payload: schemas.ScanRequest,
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Executa a varredura e indexação de uma pasta no sistema."""
    _ = current_user  # Silencia o aviso de parâmetro não utilizado (mantém a rota protegida)

    target_dir = Path(payload.path)
    if not target_dir.exists() or not target_dir.is_dir():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O caminho '{payload.path}' não existe ou não é uma pasta válida."
        )

    try:
        indexer = FileIndexer(db)
        changed_count = indexer.index_directory(target_dir)
        return schemas.ScanResponse(
            message="Varredura concluída com sucesso.",
            files_changed=changed_count
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro durante a varredura: {str(e)}"
        )


@router.get("/search", response_model=List[schemas.IndexedFileResponse])
def search_files(
        q: str | None = Query(None, description="Termo para buscar no nome ou caminho"),
        camera: str | None = Query(None, description="Filtrar por fabricante da câmara"),
        since: str | None = Query(None, description="Data inicial (YYYY-MM-DD)"),
        limit: int = Query(10, ge=1, le=100, description="Limite de resultados"),
        offset: int = Query(0, ge=0, description="Offset de paginação"),
        db: Session = Depends(get_db),
        current_user: models.User = Depends(get_current_user)
):
    """Realiza buscas avançadas na base de dados de imagens indexadas."""
    _ = current_user  # Silencia o aviso de parâmetro não utilizado (mantém a rota protegida)

    date_from = None
    if since:
        try:
            date_from = datetime.strptime(since, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Formato de data inválido para 'since'. Utilize YYYY-MM-DD."
            )

    engine = SearchEngine(db)
    results = engine.search(
        query_text=q,
        camera_make=camera,
        date_from=date_from,
        limit=limit,
        offset=offset
    )

    return results