import json
import shutil
from datetime import date
from pathlib import Path


# Define las carpetas y el archivo donde se guarda la lista de candidatos.
CARPETA_path = Path(__file__).parent
ENTRADA_path = CARPETA_path.parent / "candidatos"
PROCESADOS_path = ENTRADA_path / "procesados"
LISTA_path = CARPETA_path / "candidatos.json"


# Define las habilidades e idiomas que se usan para calcular la nota.
HABILIDADES_NECESARIAS_list = ["html", "python", "java", "javascript"]
IDIOMAS_NECESARIOS_list = ["espanol", "euskera", "ingles"]


# Calcula la experiencia laboral total en anos a partir de las fechas.
def experiencia_en_anios(trabajos_list):
    meses_int = 0

    for trabajo_dict in trabajos_list:
        inicio_str = trabajo_dict.get("fecha_inicio")
        fin_str = trabajo_dict.get("fecha_fin") or "actualidad"

        if not inicio_str:
            continue

        anio_inicio_int, mes_inicio_int = map(int, inicio_str.split("-"))

        if fin_str.lower() in ("actualidad", "presente", "actual"):
            hoy_date = date.today()
            anio_fin_int, mes_fin_int = hoy_date.year, hoy_date.month
        else:
            anio_fin_int, mes_fin_int = map(int, fin_str.split("-"))

        meses_int += max(
            (anio_fin_int - anio_inicio_int) * 12
            + mes_fin_int - mes_inicio_int + 1,
            0
        )

    return round(meses_int / 12, 1)


# Crea las carpetas de entrada y de archivos procesados si no existen.
ENTRADA_path.mkdir(exist_ok=True)
PROCESADOS_path.mkdir(exist_ok=True)