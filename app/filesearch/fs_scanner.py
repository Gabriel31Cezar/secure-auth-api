# app/filesearch/fs_scanner.py
import os
from pathlib import Path
from typing import Generator, Iterable

# Extensões suportadas (escopo 1A)
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".heic"}

# Diretórios a ignorar para evitar lixo e lentidão (ocultos ou de sistema)
IGNORED_DIRS = {
    ".git", ".svn", "node_modules", "venv", ".venv",
    "__pycache__", ".idea", ".vscode", "System Volume Information"
}


def scan_directory(
        root_path: str | Path,
        extra_ignored_dirs: Iterable[str] | None = None
) -> Generator[Path, None, None]:
    """
    Varre um diretório recursivamente e gera caminhos absolutos de imagens.

    Args:
        root_path: Caminho raiz para iniciar a varredura.
        extra_ignored_dirs: Nomes de diretórios adicionais a serem ignorados.

    Yields:
        Path: Caminho absoluto (resolvido) para cada arquivo de imagem encontrado.
    """
    base = Path(root_path).resolve()
    if not base.is_dir():
        raise ValueError(f"O caminho fornecido não é um diretório válido: {base}")

    ignored = IGNORED_DIRS.copy()
    if extra_ignored_dirs:
        ignored.update(extra_ignored_dirs)

    # Usamos os.scandir em vez de Path.rglob por performance e controle de erro
    def _walk(current_dir: Path) -> Generator[Path, None, None]:
        try:
            with os.scandir(current_dir) as entries:
                for entry in entries:
                    # Ignora links simbólicos quebrados ou loops
                    if entry.is_symlink():
                        continue

                    if entry.is_dir(follow_symlinks=False):
                        if entry.name not in ignored:
                            yield from _walk(Path(entry.path))

                    elif entry.is_file(follow_symlinks=False):
                        ext = Path(entry.name).suffix.lower()
                        if ext in IMAGE_EXTENSIONS:
                            # .resolve() garante caminho absoluto padronizado
                            yield Path(entry.path).resolve()

        except PermissionError:
            # Ignora silenciosamente pastas sem permissão de leitura (ex: Windows System)
            pass

    yield from _walk(base)