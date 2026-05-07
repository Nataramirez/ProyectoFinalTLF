from motor_regex import (
    validar_correo,    buscar_correos,
    validar_telefono,  buscar_telefonos,
    validar_fecha,     buscar_fechas,
    validar_cedula,    buscar_cedulas,
    validar_url,       buscar_urls,
    validar_placa,     buscar_placas,
    buscar_todos
)


PATRONES = [
    {
        "id"          : "correo",
        "nombre"      : "Correo electrónico",
        "descripcion" : "Dirección de correo con usuario, @ y dominio",
        "formato"     : "usuario@dominio.extension",
        "ejemplos_ok" : [
            "usuario@correo.com",
            "nombre.apellido@empresa.com.co",
            "contacto_123@gmail.com",
            "soporte-tech@dominio.org",
        ],
        "ejemplos_mal": [
            "usuariocorreo.com",     # falta @
            "@dominio.com",          # falta usuario
            "usuario@.com",          # falta dominio
            "usuario@dominio",       # falta extensión
            "usuario@dominio.c",     # extensión muy corta
        ],
        "validar"     : validar_correo,
        "buscar"      : buscar_correos,
    },
    {
        "id"          : "telefono",
        "nombre"      : "Teléfono colombiano",
        "descripcion" : "Número móvil colombiano de 10 dígitos que empieza por 3",
        "formato"     : "3XXXXXXXXX  /  +573XXXXXXXXX  /  300-123-4567",
        "ejemplos_ok" : [
            "3001234567",
            "+573001234567",
            "573001234567",
            "300-123-4567",
            "300 123 4567",
        ],
        "ejemplos_mal": [
            "1234567890",    # no empieza por 3
            "30012345",      # muy corto
            "30012345678",   # muy largo
            "+1234567890",   # indicativo incorrecto
        ],
        "validar"     : validar_telefono,
        "buscar"      : buscar_telefonos,
    },
    {
        "id"          : "fecha",
        "nombre"      : "Fecha",
        "descripcion" : "Fecha en formato DD/MM/AAAA o DD-MM-AAAA",
        "formato"     : "DD/MM/AAAA  o  DD-MM-AAAA",
        "ejemplos_ok" : [
            "06/05/2026",
            "31/12/1999",
            "01-01-2000",
            "28/02/2024",
        ],
        "ejemplos_mal": [
            "6/5/2026",      # día y mes sin cero inicial
            "06-05/2026",    # separadores mezclados
            "32/01/2026",    # día inválido
            "06/13/2026",    # mes inválido
            "06/05/26",      # año con 2 dígitos
        ],
        "validar"     : validar_fecha,
        "buscar"      : buscar_fechas,
    },
    {
        "id"          : "cedula",
        "nombre"      : "Cédula colombiana",
        "descripcion" : "Número de cédula colombiana entre 6 y 10 dígitos",
        "formato"     : "NNNNNNNNNN  (6 a 10 dígitos, no empieza en 0)",
        "ejemplos_ok" : [
            "1234567890",
            "987654",
            "10203040",
            "1000234567",
        ],
        "ejemplos_mal": [
            "0123456789",    # empieza en 0
            "12345",         # muy corta (menos de 6)
            "12345678901",   # muy larga (más de 10)
            "12345A789",     # contiene letra
        ],
        "validar"     : validar_cedula,
        "buscar"      : buscar_cedulas,
    },
    {
        "id"          : "url",
        "nombre"      : "URL",
        "descripcion" : "Dirección web con protocolo http o https",
        "formato"     : "http://dominio.ext/ruta  o  https://dominio.ext/ruta",
        "ejemplos_ok" : [
            "https://www.google.com",
            "http://ejemplo.com.co",
            "https://portal.universidad.edu.co/login",
            "https://api.servicio.io/v1/datos?id=123",
        ],
        "ejemplos_mal": [
            "www.google.com",         # sin protocolo
            "ftp://servidor.com",     # protocolo no soportado
            "https://",               # sin dominio
            "http:/dominio.com",      # doble slash faltante
        ],
        "validar"     : validar_url,
        "buscar"      : buscar_urls,
    },
    {
        "id"          : "placa",
        "nombre"      : "Placa colombiana",
        "descripcion" : "Placa de vehículo o moto colombiana",
        "formato"     : "ABC-123  (carro)  o  ABC12D  (moto)",
        "ejemplos_ok" : [
            "ABC-123",
            "XYZ999",
            "ABC12D",
            "ZZZ00A",
        ],
        "ejemplos_mal": [
            "AB-123",        # solo 2 letras iniciales
            "ABC-12",        # solo 2 dígitos finales
            "abc-123",       # letras minúsculas
            "1BC-123",       # inicia con dígito
            "ABCD-123",      # 4 letras iniciales
        ],
        "validar"     : validar_placa,
        "buscar"      : buscar_placas,
    },
]


def obtener_patron(id_patron):
    """
    Busca y retorna un patrón por su ID.
    Retorna el diccionario del patrón o None si no existe.

    Ejemplo:
        patron = obtener_patron('correo')
        print(patron['nombre'])  # → 'Correo electrónico'
    """
    for patron in PATRONES:
        if patron["id"] == id_patron:
            return patron
    return None


def listar_nombres():
    """
    Retorna una lista con los nombres legibles de todos los patrones.

    Ejemplo:
        ['Correo electrónico', 'Teléfono colombiano', ...]
    """
    return [p["nombre"] for p in PATRONES]


def listar_ids():
    """
    Retorna una lista con los IDs de todos los patrones.

    Ejemplo:
        ['correo', 'telefono', 'fecha', 'cedula', 'url', 'placa']
    """
    return [p["id"] for p in PATRONES]


def validar_con_patron(id_patron, cadena):
    """
    Valida una cadena usando el patrón indicado por su ID.
    Retorna True, False, o None si el ID no existe.

    Ejemplo:
        validar_con_patron('correo', 'test@mail.com')  # → True
        validar_con_patron('correo', 'correo-malo')    # → False
    """
    patron = obtener_patron(id_patron)
    if patron is None:
        return None
    return patron["validar"](cadena)


def buscar_con_patron(id_patron, texto):
    """
    Busca coincidencias en un texto usando el patrón indicado por su ID.
    Retorna una lista de coincidencias, o None si el ID no existe.

    Ejemplo:
        buscar_con_patron('telefono', 'llama al 3001234567 o al 3109876543')
        # → ['3001234567', '3109876543']
    """
    patron = obtener_patron(id_patron)
    if patron is None:
        return None
    return patron["buscar"](texto)


def ejecutar_casos_de_prueba():
    """
    Recorre todos los patrones y prueba sus ejemplos válidos e inválidos.
    Imprime un reporte completo en consola.
    """
    total = 0
    exitosos = 0

    print("\n" + "=" * 60)
    print(" REPORTE DE CASOS DE PRUEBA ")
    print("=" * 60)

    for patron in PATRONES:
        print(f"\n📌 {patron['nombre'].upper()}")
        print(f"   Formato: {patron['formato']}")
        print()

        # Casos que deben ser válidos
        for ejemplo in patron["ejemplos_ok"]:
            total += 1
            resultado = patron["validar"](ejemplo)
            estado = "✅ OK    " if resultado else "❌ FALLO"
            if resultado:
                exitosos += 1
            print(f"   {estado} [esperado: VÁLIDO  ] → {ejemplo}")

        # Casos que deben ser inválidos
        for ejemplo in patron["ejemplos_mal"]:
            total += 1
            resultado = patron["validar"](ejemplo)
            estado = "✅ OK    " if not resultado else "❌ FALLO"
            if not resultado:
                exitosos += 1
            print(f"   {estado} [esperado: INVÁLIDO] → {ejemplo}")

    print("\n" + "=" * 60)
    print(f" RESULTADO FINAL: {exitosos}/{total} casos correctos")
    porcentaje = (exitosos / total) * 100 if total > 0 else 0
    print(f" PRECISIÓN: {porcentaje:.1f}%")
    print("=" * 60)


if __name__ == '__main__':
    # Mostrar patrones disponibles
    print("Patrones disponibles:", listar_ids())

    # Ejecutar todos los casos de prueba
    ejecutar_casos_de_prueba()