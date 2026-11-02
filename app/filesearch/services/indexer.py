# app/filesearch/services/indexer.py
import hashlib
from pathlib import Path

from sqlalchemy.orm import Session

from app.filesearch.fs_scanner import scan_directory
from app.filesearch.exif_extractor import extract_exif
from app.filesearch.models import IndexedFile


def calculate_sha256(file_path: Path, chunk_size: int = 8192) -> str:
    """Calcula o hash SHA-256 de um arquivo em blocos para economizar memória."""
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                sha256_hash.update(chunk)
        return sha256_hash.hexdigest()
    except (OSError, IOError):
        return ""


class FileIndexer:
    def __init__(self, db: Session):
        self.db = db

    def _upsert_file(self, file_path: Path, root_path: Path) -> bool:
        """
        Processa um único arquivo e insere/atualiza no banco.
        Retorna True se houve alteração real, False se pulou.
        """
        try:
            stat = file_path.stat()
            current_mtime = stat.st_mtime
            current_size = stat.st_size
        except OSError:
            # Arquivo deletado ou sem permissão entre a varredura e o processamento
            return False

        # Busca no banco se o arquivo já foi indexado
        db_file = self.db.query(IndexedFile).filter(IndexedFile.path == str(file_path)).first()

        # Se o arquivo já existe no banco e não mudou de tamanho nem data, ignoramos (economia de I/O)
        if db_file and db_file.mtime == current_mtime and db_file.size_bytes == current_size:
            return False

        # Extração de metadados (EXIF e Hash)
        exif_data = extract_exif(file_path)
        new_hash = calculate_sha256(file_path)

        if not db_file:
            # Inserção de novo registro
            db_file = IndexedFile(path=str(file_path))
            self.db.add(db_file)

        # Atualização de dados básicos
        db_file.filename = file_path.name
        db_file.extension = file_path.suffix.lower()
        db_file.size_bytes = current_size
        db_file.mtime = current_mtime
        db_file.sha256 = new_hash

        # Atualização de dados EXIF (valores podem ser None se não houver EXIF)
        db_file.camera_make = exif_data.get("camera_make")
        db_file.camera_model = exif_data.get("camera_model")
        db_file.taken_at = exif_data.get("taken_at")
        db_file.gps_lat = exif_data.get("gps_lat")
        db_file.gps_lon = exif_data.get("gps_lon")
        db_file.orientation = exif_data.get("orientation")

        return True

    def index_directory(self, root_path: str | Path, commit_every: int = 50) -> int:
        """
        Varre o diretório e indexa todas as imagens.
        Retorna a quantidade de arquivos novos ou alterados salvos no banco.
        """
        root = Path(root_path).resolve()
        processed_count = 0
        changed_count = 0

        # O scanner retorna um generator (não estoura a memória)
        for file_path in scan_directory(root):
            processed_count += 1
            has_changes = self._upsert_file(file_path, root)

            if has_changes:
                changed_count += 1
                # Faz commit em lote (a cada 50 arquivos) para não travar o banco
                if changed_count % commit_every == 0:
                    self.db.commit()

        # Commit final do que sobrou
        self.db.commit()
        print(f"[Indexer] Varredura concluída. {processed_count} imagens verificadas, {changed_count} salvas/atualizadas.")
        return changed_count