# tests/test_indexer.py
import time
from pathlib import Path
import pytest
from PIL import Image
from sqlalchemy.orm import Session

from app.filesearch.models import IndexedFile
from app.filesearch.services.indexer import FileIndexer, calculate_sha256


def create_test_image(path: Path):
    """Helper para criar uma imagem válida no disco."""
    img = Image.new("RGB", (10, 10), color="blue")
    img.save(path)


def test_calculate_sha256(tmp_path: Path):
    file_path = tmp_path / "hash_test.txt"
    file_path.write_text("hello world")

    # Hash SHA-256 de "hello world"
    expected_hash = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    assert calculate_sha256(file_path) == expected_hash


def test_indexer_insert_and_skip(db: Session, tmp_path: Path):
    # Cria 2 imagens
    img1 = tmp_path / "img1.jpg"
    create_test_image(img1)

    indexer = FileIndexer(db)

    # 1ª Varredura: Deve inserir 1 imagem
    changed = indexer.index_directory(tmp_path)
    assert changed == 1

    records = db.query(IndexedFile).all()
    assert len(records) == 1
    assert records[0].filename == "img1.jpg"
    assert len(records[0].sha256) == 64  # Hash calculado

    # 2ª Varredura imediata: Deve ignorar (mtime e size não mudaram)
    changed_again = indexer.index_directory(tmp_path)
    assert changed_again == 0
    assert db.query(IndexedFile).count() == 1


def test_indexer_update_existing(db: Session, tmp_path: Path):
    img1 = tmp_path / "img_update.jpg"
    create_test_image(img1)

    indexer = FileIndexer(db)
    indexer.index_directory(tmp_path)

    # Altera o arquivo (força mudança de mtime e tamanho)
    time.sleep(0.01)  # Garante que o mtime mude no SO
    img1.write_text("novo conteudo maior")

    # 3ª Varredura: Deve atualizar, não inserir novo
    changed = indexer.index_directory(tmp_path)
    assert changed == 1
    assert db.query(IndexedFile).count() == 1