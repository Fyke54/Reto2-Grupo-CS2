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
IDIOMAS_NECESARIOS_list = ["español", "euskera", "inglés"]


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
            
            # Crea el registro del candidato con los datos extraidos.
        candidato_dict = {
            "nombre": nombre_str,
            "codigo": codigo_int,
            "correo": correo_str,
            "idiomas": idiomas_list,
            "habilidades": cv_dict.get("habilidades", []),
            "experiencia": experiencia_num
        }

        # Calcula la nota segun habilidades, idiomas y experiencia.
        habilidades_list = [
            habilidad_str.casefold()
            for habilidad_str in candidato_dict["habilidades"]
        ]
        idiomas_normalizados_list = [
            idioma_str.casefold()
            for idioma_str in idiomas_list
        ]

        puntos_int = sum(
            habilidad_necesaria_str in habilidades_list
            for habilidad_necesaria_str in HABILIDADES_NECESARIAS_list
        )
        puntos_int += sum(
            idioma_necesario_str in idiomas_normalizados_list
            for idioma_necesario_str in IDIOMAS_NECESARIOS_list
        )
        puntos_int += experiencia_num >= 3

        candidato_dict["nota"] = round(puntos_int / 8 * 10, 2)
        candidatos_list.append(candidato_dict)
        archivos_procesados_list.append(archivo_path)
        codigo_int += 1

        print(f"Procesado: {nombre_str}, nota {candidato_dict['nota']}/10")

    except (OSError, ValueError, TypeError, KeyError) as error_exc:
        print(f"Error en {archivo_path.name}: {error_exc}")


# Guarda la lista actualizada de candidatos en formato JSON.
LISTA_path.write_text(
    json.dumps(candidatos_list, ensure_ascii=False, indent=4),
    encoding="utf-8"
)


# Mueve los archivos procesados a su carpeta correspondiente.
for archivo_path in archivos_procesados_list:
    shutil.move(
        str(archivo_path),
        str(PROCESADOS_path / archivo_path.name)
    )


# Muestra la ubicacion de la lista actualizada.
print(f"Lista actualizada: {LISTA_path}")