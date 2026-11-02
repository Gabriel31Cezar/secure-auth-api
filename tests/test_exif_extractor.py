# tests/test_exif_extractor.py
from pathlib import Path
import pytest
from PIL import Image
# <--- MUDOU: Importando o nome novo
from app.filesearch.exif_extractor import extract_exif, convert_gps_to_decimal


@pytest.fixture
def dummy_image(tmp_path: Path) -> Path:
    img_path = tmp_path / "plain.jpg"
    img = Image.new("RGB", (10, 10), color="red")
    img.save(img_path)
    return img_path


def test_extract_exif_from_image_without_exif(dummy_image: Path):
    result = extract_exif(dummy_image)
    assert result == {}


def test_extract_exif_corrupted_file(tmp_path: Path):
    bad_file = tmp_path / "corrupted.jpg"
    bad_file.write_text("isso não é uma imagem")
    result = extract_exif(bad_file)
    assert result == {}


def test_convert_gps_to_decimal():
    gps_data = ((23, 1), (33, 1), (3, 1))

    # <--- MUDOU: Chamada sem underline
    lat = convert_gps_to_decimal(gps_data, "S")
    assert lat == pytest.approx(-23.550833, abs=1e-5)

    lat_n = convert_gps_to_decimal(gps_data, "N")
    assert lat_n == pytest.approx(23.550833, abs=1e-5)