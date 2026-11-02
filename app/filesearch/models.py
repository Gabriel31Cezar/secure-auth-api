# app/filesearch/models.py
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.sql import func

from app.database import Base


class IndexedFile(Base):
    """Representa uma imagem indexada no filesystem, com metadados EXIF opcionais."""

    __tablename__ = "indexed_files"

    # --- Identidade / filesystem ---
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, index=True, nullable=False)
    filename = Column(String, index=True, nullable=False)
    extension = Column(String(10), index=True, nullable=False)
    size_bytes = Column(Integer, nullable=False)
    mtime = Column(Float, nullable=False)  # epoch (pathlib st_mtime)
    sha256 = Column(String(64), nullable=True)  # preenchido na Etapa 4
    indexed_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # --- EXIF (opcional; NULL = imagem sem EXIF ou campo ausente) ---
    camera_make = Column(String, index=True, nullable=True)
    camera_model = Column(String, index=True, nullable=True)
    taken_at = Column(DateTime(timezone=True), index=True, nullable=True)
    gps_lat = Column(Float, nullable=True)
    gps_lon = Column(Float, nullable=True)
    orientation = Column(Integer, nullable=True)

    def __repr__(self) -> str:  # ajuda no debug interativo do PyCharm
        return f"<IndexedFile id={self.id} path={self.path!r}>"