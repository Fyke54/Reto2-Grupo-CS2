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


#crea las carpetas de entrada y de archivos procesados si no existen.
ENTRADA_path.mkdir(exist_ok=True)
PROCESADOS_path.mkdir(exist_ok=True)


#carga los candidatos guardados o empieza con una lista vacia.
if LISTA_path.exists():
    candidatos_list = json.loads(LISTA_path.read_text(encoding="utf-8"))
else:
    candidatos_list = []


#asigna el siguiente codigo disponible a los nuevos candidatos.
codigo_int = max(
    (candidato_dict.get("codigo", 0) for candidato_dict in candidatos_list),
    default=0
) + 1


#lee y procesa cada JSON de la carpeta de entrada.
archivos_procesados_list = []

for archivo_path in ENTRADA_path.glob("*.json"):
    try:
        datos_dict = json.loads(
            archivo_path.read_text(encoding="utf-8-sig")
        )
        cv_dict = datos_dict.get("cv", datos_dict)

        #extrae los datos personales del candidato.
        personales_dict = cv_dict.get("datos_personales", {})
        nombre_str = " ".join(filter(None, [
            datos_dict.get("nombre", personales_dict.get("nombre", "")),
            datos_dict.get("apellido1", ""),
            datos_dict.get("apellido2", "")
        ])).strip()

        correo_str = datos_dict.get(
            "correo",
            personales_dict.get("email", "")
        )
        idiomas_list = [
            idioma_dict.get("idioma", "") if isinstance(idioma_dict, dict)
            else idioma_dict
            for idioma_dict in cv_dict.get("idiomas", [])
        ]

        #calcula la experiencia laboral en años.
        experiencia_dato = cv_dict.get("experiencia_laboral", [])
        if isinstance(experiencia_dato, list):
            experiencia_num = experiencia_en_anios(experiencia_dato)
        else:
            experiencia_num = float(cv_dict.get("experiencia", 0))