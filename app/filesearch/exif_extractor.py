# app/filesearch/exif_extractor.py
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, cast

from PIL import Image, ExifTags


def convert_gps_to_decimal(gps_data: Any, ref: str) -> float | None:
    """Converte coordenadas GPS EXIF (graus, minutos, segundos) para float decimal."""
    if not gps_data or not ref:
        return None
    try:
        # O EXIF retorna frações no formato (numerador, denominador).
        # Usamos cast para o PyCharm entender que lidamos com números.
        def _to_float(val: Any) -> float:
            if isinstance(val, tuple) and len(val) == 2:
                # Força o PyCharm a tratar os elementos como float
                numerador = cast(float, val[0])
                denominador = cast(float, val[1])
                # O ignore abaixo para o PyCharm parar de encher o saco
                return float(numerador) / float(denominador)  # type: ignore
            return float(val)

        degrees = _to_float(gps_data[0])
        minutes = _to_float(gps_data[1])
        seconds = _to_float(gps_data[2])

        decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)

        if ref in ['S', 'W']:
            decimal = -decimal

        return round(decimal, 6)
    except (TypeError, ValueError, IndexError):
        return None


def extract_exif(file_path: str | Path) -> dict[str, Any]:
    """Extrai metadados EXIF de uma imagem."""
    exif_data: dict[str, Any] = {}

    try:
        with Image.open(file_path) as img:
            raw_exif = img.getexif()  # type: ignore
            if not raw_exif:
                return {}

            tags = {v: k for k, v in ExifTags.TAGS.items()}

            make_id = tags.get("Make")
            model_id = tags.get("Model")

            if make_id in raw_exif:
                exif_data["camera_make"] = str(raw_exif[make_id]).strip()  # type: ignore
            if model_id in raw_exif:
                exif_data["camera_model"] = str(raw_exif[model_id]).strip()  # type: ignore

            exif_ifd = raw_exif.get_ifd(ExifTags.IFD.Exif)
            date_str = exif_ifd.get(tags.get("DateTimeOriginal"))  # type: ignore

            if date_str:
                try:
                    dt = datetime.strptime(str(date_str), "%Y:%m:%d %H:%M:%S")
                    exif_data["taken_at"] = dt.replace(tzinfo=timezone.utc)
                except ValueError:
                    pass

            orientation_id = tags.get("Orientation")
            if orientation_id in raw_exif:
                exif_data["orientation"] = int(raw_exif[orientation_id])  # type: ignore

            gps_ifd = raw_exif.get_ifd(ExifTags.IFD.GPSInfo)
            if gps_ifd:
                lat_data = gps_ifd.get(tags.get("GPSLatitude"))  # type: ignore
                lat_ref = gps_ifd.get(tags.get("GPSLatitudeRef"))  # type: ignore
                lon_data = gps_ifd.get(tags.get("GPSLongitude"))  # type: ignore
                lon_ref = gps_ifd.get(tags.get("GPSLongitudeRef"))  # type: ignore

                lat = convert_gps_to_decimal(lat_data, lat_ref)
                lon = convert_gps_to_decimal(lon_data, lon_ref)

                if lat is not None and lon is not None:
                    exif_data["gps_lat"] = lat
                    exif_data["gps_lon"] = lon

    except (OSError, SyntaxError, ValueError):
        return {}

    return exif_data