# app/filesearch/services/search_engine.py
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.filesearch.models import IndexedFile


class SearchEngine:
    def __init__(self, db: Session):
        self.db = db

    def search(
            self,
            query_text: str | None = None,
            camera_make: str | None = None,
            camera_model: str | None = None,
            date_from: datetime | None = None,
            date_to: datetime | None = None,
            limit: int = 50,
            offset: int = 0,
    ) -> List[IndexedFile]:
        """
        Executa uma busca dinâmica no banco de dados.
        """
        q = self.db.query(IndexedFile)

        # 1. Busca Textual (LIKE) no nome do arquivo ou caminho completo
        if query_text:
            search_pattern = f"%{query_text}%"
            q = q.filter(
                or_(
                    IndexedFile.filename.ilike(search_pattern),
                    IndexedFile.path.ilike(search_pattern)
                )
            )

        # 2. Filtros EXIF (Case-Insensitive)
        if camera_make:
            q = q.filter(IndexedFile.camera_make.ilike(f"%{camera_make}%"))

        if camera_model:
            q = q.filter(IndexedFile.camera_model.ilike(f"%{camera_model}%"))

        # 3. Filtros de Data
        if date_from:
            q = q.filter(IndexedFile.taken_at >= date_from)

        if date_to:
            q = q.filter(IndexedFile.taken_at <= date_to)

        # 4. Ordenação e Paginação
        # Se a foto não tiver EXIF, ordena pela data de indexação como fallback
        q = q.order_by(IndexedFile.taken_at.desc().nullslast(), IndexedFile.indexed_at.desc())

        return q.offset(offset).limit(limit).all()