# Proyecto Final — Teoría de Lenguajes Formales
### Búsqueda y Validación de Patrones en Textos y Sistemas Interactivos

**Institución:** Universidad del Quindio  
**Asignatura:** Teoría de Lenguajes Formales  
**Autores:** Natalia Ramírez Lievano · Jhaineth Valentina Naranjo Mejía · Sebastian Gallego Salazar

---

## 1. Objetivo General

Desarrollar una aplicación en Python que permita detectar y validar patrones dentro de textos mediante autómatas finitos implementados manualmente, así como verificar la entrada de datos en una interfaz interactiva con formularios, asegurando que la información cumpla con criterios sintácticos y estructurales previamente definidos, sin recurrir a la librería `re` ni a ninguna librería predefinida de procesamiento de expresiones regulares.

---

## 2. Descripción del Proyecto

La aplicación desarrollada es un sistema de escritorio construido con Python y tkinter que integra dos funcionalidades principales:

**A. Búsqueda de patrones en textos:** el usuario ingresa o carga un archivo de texto y la aplicación identifica y resalta automáticamente todas las ocurrencias de los patrones definidos. Los patrones soportados son:

| Patrón | Formato | Ejemplo |
|---|---|---|
| Correo electrónico | `usuario@dominio.extension` | `soporte@empresa.com.co` |
| Teléfono colombiano | `3XXXXXXXXX` / `+573XXXXXXXXX` | `+57 300 123 4567` |
| Fecha | `DD/MM/AAAA` o `DD-MM-AAAA` | `06/05/2026` |
| Cédula colombiana | 6 a 10 dígitos, no inicia en 0 | `1098765432` |
| URL | `http://` o `https://` + dominio | `https://www.pagina.com/ruta` |
| Placa colombiana | `ABC-123` (carro) / `ABC12D` (moto) | `XYZ-999` |

**B. Validación en formulario interactivo:** un formulario de registro valida cada campo en tiempo real mientras el usuario escribe, emitiendo retroalimentación visual inmediata. Los campos validados son: nombre de usuario, correo electrónico, teléfono, cédula, fecha de nacimiento, contraseña y confirmación de contraseña.

La solución cumple el requisito central del proyecto: **todas las validaciones se implementan mediante autómatas finitos deterministas codificados manualmente**, sin usar la librería `re` de Python ni ningún motor de expresiones regulares externo.

---

## 3. Desarrollo

### 3.1 Análisis de Requerimientos

Se identificaron seis patrones de texto con relevancia en el contexto colombiano: correos electrónicos, números telefónicos móviles, fechas calendario, números de cédula, URLs web y placas vehiculares. Para cada uno se definió:

- El conjunto de cadenas válidas (lenguaje regular reconocido).
- El formato esperado y sus variantes permitidas.
- Un conjunto de ejemplos válidos e inválidos para verificación.

Adicionalmente se identificaron las reglas de negocio del formulario: contraseña segura con fortaleza progresiva y confirmación de contraseña coincidente.

### 3.2 Diseño del Sistema

La arquitectura separa responsabilidades en tres capas:

```
main.py                  ← punto de entrada, arma la ventana principal
├── motor_regex.py       ← capa lógica: autómatas y algoritmos de búsqueda
├── patrones.py          ← catálogo de patrones + casos de prueba
└── interfaz/
    ├── busqueda.py      ← pestaña de búsqueda en textos
    ├── formulario.py    ← pestaña de formulario con validación
    └── pruebas.py       ← pestaña de casos de prueba automáticos
```

El diseño garantiza que la interfaz gráfica nunca accede directamente a los autómatas; siempre pasa por `patrones.py`, lo que desacopla la lógica de la presentación.

### 3.3 Implementación del Motor de Autómatas (`motor_regex.py`)

Cada validador implementa un **autómata finito determinista (AFD)** como función que recorre la cadena carácter a carácter, manteniendo un estado implícito mediante la posición del índice `i` y condiciones booleanas.

#### Funciones auxiliares de clasificación de caracteres

```python
def es_letra(c):      return ('a' <= c <= 'z') or ('A' <= c <= 'Z')
def es_digito(c):     return '0' <= c <= '9'
def es_mayuscula(c):  return 'A' <= c <= 'Z'
```

Estas funciones reemplazan completamente los predicados de la librería `re` y sirven como base de todos los autómatas.

#### Autómata para correo electrónico

El AFD transita por cuatro estados:

- **q0→q1:** consume uno o más caracteres válidos de usuario (`[a-zA-Z0-9._-]+`)
- **q1→q2:** consume exactamente un carácter `@`
- **q2→q3:** consume uno o más caracteres alfanuméricos de dominio
- **q3→qf:** consume uno o más bloques `.extension` donde la extensión tiene entre 2 y 6 letras

La cadena es aceptada si el índice `i` alcanza exactamente el final de la cadena en el estado final.

#### Autómata para teléfono colombiano

El validador primero normaliza la cadena eliminando espacios y guiones, luego:

1. Consume el prefijo opcional `+` seguido de `57`.
2. Verifica que el número local resultante tenga exactamente 10 dígitos y comience con `3`.

Esto acepta formatos como `3001234567`, `+573001234567`, `300-123-4567` y `+57 300 123 4567`.

#### Autómata para fecha

Verifica longitud fija de 10 caracteres, separadores consistentes (`/` o `-`) en las posiciones 2 y 5, y rangos lógicos: día en [1,31], mes en [1,12], año en [1900,2099], con una tabla de días máximos por mes.

#### Autómata para cédula colombiana

Acepta cadenas de solo dígitos con longitud entre 6 y 10 que no inicien en `0`. Verificación de límites mediante comparación de posición en texto para evitar falsos positivos dentro de secuencias más largas.

#### Autómata para URL

Verifica el protocolo (`http://` o `https://`) carácter a carácter, luego lee el dominio exigiendo la presencia de al menos un punto (requisito corregido para rechazar `https://localhost`), y finalmente acepta una ruta opcional con el conjunto de caracteres válidos en URLs.

#### Autómata para placa colombiana

Normaliza quitando guiones, luego verifica:
- Primeros 3 caracteres: letras mayúsculas.
- Siguientes 3: dígitos (formato carro `ABC-123`) o 2 dígitos + 1 mayúscula (formato moto `ABC12D`).

#### Algoritmos de búsqueda en texto

Para cada patrón existe una función `buscar_X(texto)` que recorre el texto con un índice `i` e intenta hacer coincidir subcadenas de distintas longitudes en cada posición. El resultado es la lista de todas las ocurrencias no solapadas encontradas.

La función `buscar_todos` combina todos los buscadores y resuelve el conflicto de solapamiento entre teléfonos y cédulas: extrae los 10 dígitos locales de cada teléfono encontrado y los excluye del resultado de cédulas.

### 3.4 Catálogo de Patrones (`patrones.py`)

Define la lista `PATRONES`, donde cada elemento es un diccionario que contiene el ID del patrón, su nombre legible, descripción, formato, ejemplos válidos, ejemplos inválidos y referencias a las funciones `validar` y `buscar` de `motor_regex.py`.

Provee las funciones de acceso `obtener_patron`, `validar_con_patron` y `buscar_con_patron`, que permiten a la interfaz operar sobre cualquier patrón usando solo su ID, sin conocer los detalles de implementación.

### 3.5 Interfaz Gráfica

La aplicación presenta una ventana principal con tres pestañas implementadas:

**Pestaña 1 — Búsqueda en Textos:**  
Panel izquierdo con área de texto editable y carga de archivos `.txt`. Panel derecho con resultados por categoría. Las coincidencias se resaltan en amarillo dentro del texto original. El usuario puede buscar todos los patrones a la vez o seleccionar uno específico mediante botones de radio.

**Pestaña 2 — Formulario de Registro:**  
Siete campos con validación en tiempo real al escribir. Un panel lateral muestra el resumen de estado de todos los campos simultáneamente. El indicador de fortaleza de contraseña evalúa seis criterios: longitud mínima, longitud extendida, mayúsculas, minúsculas, dígitos y caracteres especiales.

**Pestaña 3 — Casos de Prueba:**  
Ejecuta automáticamente los 52 casos de prueba (válidos e inválidos) de los seis patrones y muestra el resultado de cada uno con codificación de color. Incluye un resumen con el puntaje total y porcentaje de precisión.

### 3.6 Pruebas y Casos de Uso

Se definieron **52 casos de prueba** distribuidos entre los seis patrones: 26 casos con entradas válidas y 26 con entradas inválidas. Además del visor integrado en la aplicación, se implementó una suite formal con `pytest` en `tests/test_patrones.py` que parametriza automáticamente todos los casos.

**Resultado de ejecución:**

```
============================= test session starts ==============================
collected 52 items

tests/test_patrones.py::test_patron[correo-...] PASSED
...
============================== 52 passed in 0.03s ==============================
```

**Tabla de casos de prueba representativos:**

| Patrón | Entrada | Esperado | Resultado |
|---|---|---|---|
| Correo | `usuario@correo.com` | VÁLIDO | ✅ OK |
| Correo | `@dominio.com` | INVÁLIDO | ✅ OK |
| Correo | `usuario@dominio` | INVÁLIDO | ✅ OK |
| Teléfono | `3001234567` | VÁLIDO | ✅ OK |
| Teléfono | `+57 300 123 4567` | VÁLIDO | ✅ OK |
| Teléfono | `1234567890` | INVÁLIDO | ✅ OK |
| Fecha | `06/05/2026` | VÁLIDO | ✅ OK |
| Fecha | `32/01/2026` | INVÁLIDO | ✅ OK |
| Fecha | `06-05/2026` | INVÁLIDO | ✅ OK |
| Cédula | `1098765432` | VÁLIDO | ✅ OK |
| Cédula | `0123456789` | INVÁLIDO | ✅ OK |
| URL | `https://www.google.com` | VÁLIDO | ✅ OK |
| URL | `https://localhost` | INVÁLIDO | ✅ OK |
| URL | `www.google.com` | INVÁLIDO | ✅ OK |
| Placa | `ABC-123` | VÁLIDO | ✅ OK |
| Placa | `abc-123` | INVÁLIDO | ✅ OK |

**Casos de búsqueda en texto compuesto:**

Texto de entrada:
```
Contáctenos en soporte@empresa.com.co — Tel: +57 310 987 6543
Cédula: 10987654 — Fecha: 06/05/2026
Visita https://www.miempresa.com — Placa: ABC-123
```

Resultados obtenidos:
- **Correos:** `soporte@empresa.com.co`
- **Teléfonos:** `+57 310 987 6543`
- **Cédulas:** `10987654` *(sin conflicto con el teléfono)*
- **Fechas:** `06/05/2026`
- **URLs:** `https://www.miempresa.com`
- **Placas:** `ABC-123`

---

## 4. Conclusiones

**Sobre la implementación de autómatas:**  
La construcción manual de los AFDs demostró que es plenamente posible reconocer lenguajes regulares sin bibliotecas especializadas, traduciendo directamente los estados y transiciones del autómata en condiciones e índices sobre la cadena. Esta aproximación obliga a entender con precisión el lenguaje que se quiere reconocer antes de codificarlo, lo que refuerza los conceptos teóricos de la asignatura.

**Sobre la separación entre validar y buscar:**  
El diseño de tener funciones `validar_X` (reconocen si una cadena completa pertenece al lenguaje) separadas de `buscar_X` (localizan subcadenas que pertenecen al lenguaje dentro de un texto) permitió reutilizar la misma lógica de autómata tanto para el formulario como para el buscador, sin duplicar código.

**Sobre el conflicto entre patrones:**  
Un desafío real fue que los lenguajes de cédula y teléfono son ambiguos para ciertas cadenas: `3001234567` pertenece a ambos lenguajes. Esto evidencia que en sistemas reales el contexto es necesario para la desambiguación; la solución adoptada fue dar prioridad al patrón más específico (teléfono) sobre el más general (cédula).

**Sobre la validación en formularios:**  
La validación en tiempo real con retroalimentación inmediata mejora la experiencia del usuario al evitar el ciclo de error-corrección-reenvío.

**Sobre las pruebas:**  
La definición de casos de prueba formales como parte del desarrollo, y no como actividad posterior, permitió detectar errores en los autómatas durante la implementación. La suite de 52 casos con resultado 100% de precisión valida que los autómatas implementados reconocen correctamente el lenguaje definido para cada patrón.

---

*Documento generado automáticamente como parte del entregable del Proyecto Final de Teoría de Lenguajes Formales — Mayo 2026.*
