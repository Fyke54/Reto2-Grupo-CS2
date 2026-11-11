import json # Para manejar archivos JSON
import os # Para manejar rutas de archivos de manera independiente del sistema operativo
import unicodedata # Para normalizar texto y eliminar acentos


def normalizar(texto):
    texto = unicodedata.normalize("NFD", str(texto).casefold())
    return "".join(
        letra for letra in texto
        if unicodedata.category(letra) != "Mn"
    )


ruta = os.path.join(os.path.dirname(__file__), "candidatos.json")

with open(ruta, "r", encoding="utf-8") as f:
    candidatos = json.load(f)

while True:
    print("\n1. Buscar candidatos")
    print("2. Listar candidatos")
    print("3. Salir")

    opcion = input("Elige una opción: ")

    if opcion == "1":
        print("Deja vacio el filtro que no quieras usar")

        habilidad = normalizar(input("Habilidad: ").strip())
        idioma = normalizar(input("Idioma: ").strip())
        experiencia = input("Años minimos de experiencia: ").strip()
        nota = input("Nota minima del CV: ").strip()

        while experiencia and not experiencia.isdigit():
            print("Introduce un numero valido")
            experiencia = input(
                "Años mínimos de experiencia: "
            ).strip()

        while nota and not nota.isdigit():
            print("Introduce un numero valido")
            nota = input("Nota mínima del CV: ").strip()

        experiencia_minima = int(experiencia) if experiencia else 0
        nota_minima = int(nota) if nota else 0
        encontrados = 0

        for candidato in candidatos:
            habilidades = [
                normalizar(h) for h in candidato["habilidades"]
            ]
            idiomas = [
                normalizar(i) for i in candidato["idiomas"]
            ]

            cumple = True

            if habilidad and habilidad not in habilidades:
                cumple = False
            if idioma and idioma not in idiomas:
                cumple = False
            if candidato["experiencia"] < experiencia_minima:
                cumple = False
            if candidato["nota"] < nota_minima:
                cumple = False

            if not cumple:
                cumple = False

            if cumple:
                encontrados += 1
                print("\nNombre:", candidato["nombre"])
                print("Código de candidato:", candidato["codigo"])
                print("Idiomas:", candidato["idiomas"])
                print("Habilidades:", candidato["habilidades"])
                print("Experiencia:", candidato["experiencia"])
                print("Nota del CV:", candidato["nota"])

        if encontrados == 0:
            print("No hay candidatos con esos filtros")

    elif opcion == "2":
        for candidato in candidatos:
            print("\nNombre:", candidato["nombre"])
            print("Código de candidato:", candidato["codigo"])
            print("Idiomas:", candidato["idiomas"])
            print("Habilidades:", candidato["habilidades"])
            print("Experiencia:", candidato["experiencia"])
            print("Correo:", candidato["correo_electronico"])
            print("Nota del CV:", candidato["nota"])
            break

    elif opcion == "3":
        continue

    else:
        print("Opción incorrecta")
