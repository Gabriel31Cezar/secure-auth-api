# tests/test_search_engine.py
from datetime import datetime, timezone
import pytest
from sqlalchemy.orm import Session
# Adicione o type ignore para a importação
from app.filesearch.models import IndexedFile  # type: ignore
from app.filesearch.services.search_engine import SearchEngine

@pytest.fixture
def populate_db(db: Session):
    """Cria dados falsos no banco para testar o motor de busca."""
    photos = [
        IndexedFile(
            path="/pics/ferias_praia.jpg", filename="ferias_praia.jpg", extension=".jpg",
            size_bytes=100, mtime=1000.0,
            camera_make="Canon", camera_model="EOS 5D",
            # O type: ignore na linha abaixo resolve o aviso do 'taken_at'
            taken_at=datetime(2023, 7, 10, tzinfo=timezone.utc)  # type: ignore
        ),
        IndexedFile(
            path="/pics/ferias_montanha.jpg", filename="ferias_montanha.jpg", extension=".jpg",
            size_bytes=100, mtime=1000.0,
            camera_make="Nikon", camera_model="D850",
            taken_at=datetime(2023, 12, 20, tzinfo=timezone.utc)  # type: ignore
        ),
        IndexedFile(
            path="/pics/aniversario.jpg", filename="aniversario.jpg", extension=".jpg",
            size_bytes=100, mtime=1000.0,
            camera_make="Canon", camera_model="EOS R5",
            taken_at=datetime(2024, 2, 15, tzinfo=timezone.utc)  # type: ignore
        ),
        IndexedFile(
            path="/pics/sem_exif.png", filename="sem_exif.png", extension=".png",
            size_bytes=100, mtime=1000.0,
            # type: ignore para o PyCharm entender que campos nullable aceitam None
            camera_make=None, camera_model=None, taken_at=None  # type: ignore
        ),
    ]
    db.add_all(photos)
    db.commit()
    return db


def test_search_textual(populate_db: Session):
    engine = SearchEngine(populate_db)
    results = engine.search(query_text="ferias")

    assert len(results) == 2
    assert results[0].filename in ["ferias_montanha.jpg", "ferias_praia.jpg"]


def test_search_by_camera(populate_db: Session):
    engine = SearchEngine(populate_db)
    results = engine.search(camera_make="canon")  # testando case-insensitive

    assert len(results) == 2
    assert all(r.camera_make == "Canon" for r in results)


def test_search_by_date_range(populate_db: Session):
    engine = SearchEngine(populate_db)
    date_from = datetime(2023, 12, 1, tzinfo=timezone.utc)
    date_to = datetime(2024, 12, 31, tzinfo=timezone.utc)

    results = engine.search(date_from=date_from, date_to=date_to)

    # Deve achar apenas Montanha (Dez 2023) e Aniversario (Fev 2024)
    assert len(results) == 2
    assert results[0].filename == "aniversario.jpg"  # o mais recente vem primeiro
    assert results[1].filename == "ferias_montanha.jpg"


def test_search_combined_filters(populate_db: Session):
    engine = SearchEngine(populate_db)
    results = engine.search(query_text="ferias", camera_make="Canon")

    # Apenas a foto da praia (Canon + ferias)
    assert len(results) == 1
    assert results[0].filename == "ferias_praia.jpg"


def test_search_pagination(populate_db: Session):
    engine = SearchEngine(populate_db)

    # Pega a primeira foto (a mais recente: Aniversario)
    page1 = engine.search(limit=1, offset=0)
    assert len(page1) == 1
    assert page1[0].filename == "aniversario.jpg"

    # Pega a segunda foto (Montanha)
    page2 = engine.search(limit=1, offset=1)
    assert len(page2) == 1
    assert page2[0].filename == "ferias_montanha.jpg"