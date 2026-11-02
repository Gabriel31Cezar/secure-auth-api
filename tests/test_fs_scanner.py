# tests/test_fs_scanner.py
from pathlib import Path
import pytest
from app.filesearch.fs_scanner import scan_directory


def test_scan_directory_filters_and_ignores(tmp_path: Path):
    # 1. Cria estrutura de pastas
    (tmp_path / "subfolder").mkdir()
    # Usamos 'node_modules' pois já está no IGNORED_DIRS padrão do scanner
    (tmp_path / "node_modules").mkdir()

    # 2. Cria arquivos válidos (deve achar 2)
    valid_img_1 = tmp_path / "photo1.JPG"  # Maiúsculo de propósito
    valid_img_1.write_text("fake data")

    valid_img_2 = tmp_path / "subfolder" / "photo2.png"
    valid_img_2.write_text("fake data")

    # 3. Cria arquivos inválidos (não deve achar)
    (tmp_path / "document.pdf").write_text("fake data")
    # Colocamos a imagem "escondida" dentro da pasta que DEVE ser ignorada
    (tmp_path / "node_modules" / "hidden.jpg").write_text("fake data")
    (tmp_path / "node_modules" / "package.json").write_text("fake data")

    # 4. Executa o scanner
    results = list(scan_directory(tmp_path))

    # 5. Validações
    assert len(results) == 2, f"Esperava 2 imagens, mas achou {len(results)}: {results}"
    assert valid_img_1.resolve() in results
    assert valid_img_2.resolve() in results

    # Garante que os arquivos ignorados não estão lá
    paths_as_str = [str(p).lower() for p in results]
    assert not any("document.pdf" in p for p in paths_as_str)
    assert not any("node_modules" in p for p in paths_as_str)


def test_scan_invalid_directory_raises_error():
    with pytest.raises(ValueError, match="não é um diretório válido"):
        # Passa um arquivo falso que não existe
        list(scan_directory("/caminho/que/nao/existe/12345"))