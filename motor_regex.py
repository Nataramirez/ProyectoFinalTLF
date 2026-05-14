def es_letra(c):
    """Retorna True si el carácter es una letra (a-z, A-Z)"""
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')


def es_digito(c):
    """Retorna True si el carácter es un dígito (0-9)"""
    return '0' <= c <= '9'


def es_alfanumerico(c):
    """Retorna True si el carácter es letra o dígito"""
    return es_letra(c) or es_digito(c)


def es_mayuscula(c):
    """Retorna True si el carácter es una letra mayúscula"""
    return 'A' <= c <= 'Z'


def _label_dominio_valido(label):
    """Valida una parte de dominio sin usar expresiones regulares."""
    if label == "":
        return False
    if label[0] == '-' or label[-1] == '-':
        return False
    for c in label:
        if not (es_alfanumerico(c) or c == '-'):
            return False
    return True


def _dominio_valido(dominio):
    """Valida dominios con al menos un punto y TLD alfabetico de 2+ letras."""
    partes = dominio.split('.')
    if len(partes) < 2:
        return False
    for parte in partes[:-1]:
        if not _label_dominio_valido(parte):
            return False
    tld = partes[-1]
    if len(tld) < 2:
        return False
    for c in tld:
        if not es_letra(c):
            return False
    return True


def _es_bisiesto(anio):
    return (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0)


def _limite_token(texto, indice):
    """True si el indice esta fuera o apunta a un separador de token."""
    return indice < 0 or indice >= len(texto) or not es_alfanumerico(texto[indice])


def validar_correo(cadena):
    """
    Valida si una cadena completa es un correo electrónico válido.
    Retorna True o False.
    """
    n = len(cadena)
    if n == 0:
        return False

    i = 0
    # Estado q0 → q1: leer el usuario (al menos 1 carácter válido)
    if i >= n or not (es_alfanumerico(cadena[i]) or cadena[i] in '._-'):
        return False
    while i < n and (es_alfanumerico(cadena[i]) or cadena[i] in '._-'):
        i += 1
    usuario = cadena[:i]
    if usuario[0] == '.' or usuario[-1] == '.' or '..' in usuario:
        return False

    # Estado q1 → q2: debe haber exactamente un '@'
    if i >= n or cadena[i] != '@':
        return False
    i += 1

    return _dominio_valido(cadena[i:])


def buscar_correos(texto):
    """
    Busca todos los correos electrónicos dentro de un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    i = 0
    while i < n:
        # Solo intentar si el carácter actual puede iniciar un correo
        if es_alfanumerico(texto[i]) or texto[i] in '._-':
            for j in range(i + 1, n + 1):
                subcadena = texto[i:j]
                if validar_correo(subcadena):
                    # Intentar extender para encontrar el correo más largo
                    if j == n or not (es_alfanumerico(texto[j]) or texto[j] in '._-@'):
                        resultados.append(subcadena)
                        i = j - 1
                        break
        i += 1
    return resultados


def validar_telefono(cadena):
    """
    Valida si una cadena es un número telefónico colombiano válido.
    Retorna True o False.
    """
    # Limpiar separadores permitidos (espacios y guiones)
    limpio = ''
    for c in cadena:
        if c not in ' -':
            limpio += c

    n = len(limpio)
    i = 0

    # Manejar prefijo internacional +57 o 57
    if i < n and limpio[i] == '+':
        i += 1
    if i + 1 < n and limpio[i] == '5' and limpio[i + 1] == '7':
        i += 2

    # El número local debe tener exactamente 10 dígitos y comenzar con 3
    numero_local = limpio[i:]
    if len(numero_local) != 10:
        return False
    if numero_local[0] != '3':
        return False
    for c in numero_local:
        if not es_digito(c):
            return False
    return True


def buscar_telefonos(texto):
    """
    Busca todos los números telefónicos colombianos en un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    i = 0
    while i < n:
        for longitud in [16, 15, 14, 13, 12, 11, 10]:
            if i + longitud <= n:
                subcadena = texto[i:i + longitud]
                antes = _limite_token(texto, i - 1)
                despues = _limite_token(texto, i + longitud)
                if antes and despues and validar_telefono(subcadena):
                    resultados.append(subcadena.strip())
                    i += longitud - 1
                    break
        i += 1
    return resultados


def validar_fecha(cadena):
    """
    Valida si una cadena es una fecha válida en formato DD/MM/AAAA o DD-MM-AAAA.
    Retorna True o False.
    """
    if len(cadena) != 10:
        return False

    # Verificar posiciones de separadores (índices 2 y 5)
    sep = cadena[2]
    if sep not in ('/', '-'):
        return False
    if cadena[5] != sep:
        return False

    # Extraer partes
    dia_str = cadena[0:2]
    mes_str = cadena[3:5]
    anio_str = cadena[6:10]

    # Verificar que sean dígitos
    for c in dia_str + mes_str + anio_str:
        if not es_digito(c):
            return False

    dia = int(dia_str)
    mes = int(mes_str)
    anio = int(anio_str)

    # Validar rangos
    if not (1 <= dia <= 31):
        return False
    if not (1 <= mes <= 12):
        return False
    if not (1900 <= anio <= 2099):
        return False

    # Validar dias por mes, incluyendo bisiestos.
    dias_por_mes = [
        0, 31, 29 if _es_bisiesto(anio) else 28, 31, 30, 31, 30,
        31, 31, 30, 31, 30, 31
    ]
    if dia > dias_por_mes[mes]:
        return False

    return True


def buscar_fechas(texto):
    """
    Busca todas las fechas en formato DD/MM/AAAA o DD-MM-AAAA en un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    for i in range(n - 9):
        subcadena = texto[i:i + 10]
        if _limite_token(texto, i - 1) and _limite_token(texto, i + 10) and validar_fecha(subcadena):
            resultados.append(subcadena)
    return resultados


def validar_cedula(cadena):
    """
    Valida si una cadena es una cédula colombiana válida.
    Retorna True o False.
    """
    n = len(cadena)
    if not (6 <= n <= 10):
        return False
    if cadena[0] == '0':
        return False
    for c in cadena:
        if not es_digito(c):
            return False
    return True


def buscar_cedulas(texto):
    """
    Busca posibles cédulas colombianas en un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    i = 0
    while i < n:
        if es_digito(texto[i]) and texto[i] != '0':
            j = i
            while j < n and es_digito(texto[j]):
                j += 1
            subcadena = texto[i:j]
            # Verificar que no este dentro de otro token alfanumerico.
            antes = _limite_token(texto, i - 1)
            despues = _limite_token(texto, j)
            if antes and despues and validar_cedula(subcadena):
                resultados.append(subcadena)
            i = j
        else:
            i += 1
    return resultados


def validar_url(cadena):
    """
    Valida si una cadena es una URL válida con protocolo http o https.
    Retorna True o False.
    """
    n = len(cadena)
    i = 0

    # Verificar protocolo 'http' o 'https'
    protocolo_http = 'http://'
    protocolo_https = 'https://'

    if cadena[:len(protocolo_https)] == protocolo_https:
        i = len(protocolo_https)
    elif cadena[:len(protocolo_http)] == protocolo_http:
        i = len(protocolo_http)
    else:
        return False

    # Leer dominio hasta que empiece ruta, query o fragmento.
    if i >= n or not (es_alfanumerico(cadena[i]) or cadena[i] == '-'):
        return False
    inicio_dominio = i
    while i < n and (es_alfanumerico(cadena[i]) or cadena[i] in '.-'):
        i += 1
    if not _dominio_valido(cadena[inicio_dominio:i]):
        return False

    # Leer ruta opcional
    caracteres_ruta = set('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&\'()*+,;=%')
    while i < n and cadena[i] in caracteres_ruta:
        i += 1

    return i == n


def buscar_urls(texto):
    """
    Busca todas las URLs en un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    i = 0
    while i < n:
        if texto[i] == 'h':
            encontrado = False
            for longitud in range(n - i, 6, -1):
                subcadena = texto[i:i + longitud]
                if validar_url(subcadena):
                    # Verificar que el siguiente carácter no es parte de la URL
                    fin = i + longitud
                    if fin == n or texto[fin] in ' \t\n"\'<>),];.':
                        resultados.append(subcadena)
                        i += longitud - 1
                        encontrado = True
                        break
            if not encontrado:
                i += 1
        else:
            i += 1
    return resultados


def validar_placa(cadena):
    """
    Valida si una cadena es una placa colombiana válida.
    Retorna True o False.
    """
    n = len(cadena)
    if n not in (6, 7):
        return False
    for c in cadena[:3]:
        if not es_mayuscula(c):
            return False

    if n == 7:
        if cadena[3] != '-':
            return False
        resto = cadena[4:]
        return len(resto) == 3 and all(es_digito(c) for c in resto)

    resto = cadena[3:]

    if len(resto) != 3:
        return False

    # Formato moto: 2 dígitos + 1 letra mayúscula  (ej: ABC12D)
    if es_digito(resto[0]) and es_digito(resto[1]) and es_mayuscula(resto[2]):
        return True

    # Formato carro: 3 dígitos  (ej: ABC123)
    if es_digito(resto[0]) and es_digito(resto[1]) and es_digito(resto[2]):
        return True

    return False


def buscar_placas(texto):
    """
    Busca todas las placas colombianas en un texto.
    Retorna una lista con las coincidencias encontradas.
    """
    resultados = []
    n = len(texto)
    for i in range(n):
        # Intentar con guión (longitud 7): ABC-123
        for longitud in [7, 6]:
            if i + longitud <= n:
                subcadena = texto[i:i + longitud]
                if validar_placa(subcadena):
                    # Verificar que no esté dentro de una palabra más larga
                    antes = (i == 0 or not es_alfanumerico(texto[i - 1]))
                    despues = (i + longitud == n or not es_alfanumerico(texto[i + longitud]))
                    if antes and despues:
                        resultados.append(subcadena)
                        break
    return resultados


def buscar_todos(texto):
    """
    Recorre el texto buscando todos los patrones definidos.
    Retorna un diccionario con los resultados por categoría.
    """
    telefonos = buscar_telefonos(texto)

    # Extraer los 10 dígitos locales de cada teléfono para evitar
    # que un número como 3001234567 aparezca también como cédula.
    numeros_telefono = set()
    for t in telefonos:
        solo_digitos = ''
        for c in t:
            if es_digito(c):
                solo_digitos += c
        if len(solo_digitos) >= 10:
            numeros_telefono.add(solo_digitos[-10:])

    cedulas = [c for c in buscar_cedulas(texto) if c not in numeros_telefono]

    return {
        'correos'   : buscar_correos(texto),
        'telefonos' : telefonos,
        'fechas'    : buscar_fechas(texto),
        'cedulas'   : cedulas,
        'urls'      : buscar_urls(texto),
        'placas'    : buscar_placas(texto),
    }


if __name__ == '__main__':
    texto_prueba = """
    Contáctenos en soporte@empresa.com.co o ventas@tienda.org
    Teléfono: 3001234567 o también al +57 310 987 6543
    Cédula del cliente: 1234567890
    Fecha de registro: 06/05/2026
    Visítenos en https://www.miempresa.com/contacto
    Placa del vehículo: ABC-123 o moto XYZ12D
    """

    print("=" * 50)
    print("RESULTADOS DE BÚSQUEDA")
    print("=" * 50)
    resultados = buscar_todos(texto_prueba)
    for categoria, encontrados in resultados.items():
        print(f"\n{categoria.upper()}:")
        if encontrados:
            for item in encontrados:
                print(f"  ✔ {item}")
        else:
            print("  (ninguno encontrado)")
    print("\n" + "=" * 50)
