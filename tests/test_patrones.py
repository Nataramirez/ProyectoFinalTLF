import pytest
from patrones import PATRONES


def _generar_casos():
    casos = []
    for patron in PATRONES:
        for ejemplo in patron["ejemplos_ok"]:
            casos.append((patron["id"], patron["validar"], ejemplo, True))
        for ejemplo in patron["ejemplos_mal"]:
            casos.append((patron["id"], patron["validar"], ejemplo, False))
    return casos


@pytest.mark.parametrize("patron_id,validar,cadena,esperado", _generar_casos())
def test_patron(patron_id, validar, cadena, esperado):
    resultado = validar(cadena)
    assert resultado == esperado, (
        f"Patrón '{patron_id}': '{cadena}' → "
        f"esperado {'VÁLIDO' if esperado else 'INVÁLIDO'}, "
        f"obtenido {'VÁLIDO' if resultado else 'INVÁLIDO'}"
    )


@pytest.mark.parametrize(
    "patron_id,cadena,esperado",
    [
        ("correo", ".usuario@dominio.com", False),
        ("correo", "usuario.@dominio.com", False),
        ("correo", "usuario..x@dominio.com", False),
        ("correo", "usuario@sub.dominio.com", True),
        ("fecha", "29/02/2023", False),
        ("fecha", "29/02/2024", True),
        ("url", "https://google..com", False),
        ("url", "https://google.com.", False),
        ("url", "https://-google.com", False),
        ("url", "https://google-.com", False),
        ("url", "https://google.c", False),
        ("url", "https://docs.python.org/3/library/index.html", True),
        ("placa", "ABC--123", False),
        ("placa", "ABC-12D", False),
        ("placa", "ABC-123", True),
        ("placa", "ABC12D", True),
    ],
)
def test_casos_borde_validacion(patron_id, cadena, esperado):
    patron = next(p for p in PATRONES if p["id"] == patron_id)
    assert patron["validar"](cadena) is esperado


def test_busqueda_evitar_falsos_positivos():
    from motor_regex import buscar_todos

    texto = (
        "correo usuario@dominio.com, fecha 29/02/2023 y 29/02/2024. "
        "url https://google.com. ruido abc3001234567 x573001234567 "
        "telefono +57 310 987 6543 placa ABC--123 y ABC-123"
    )

    resultados = buscar_todos(texto)

    assert resultados["fechas"] == ["29/02/2024"]
    assert resultados["telefonos"] == ["+57 310 987 6543"]
    assert resultados["cedulas"] == []
    assert resultados["urls"] == ["https://google.com"]
    assert resultados["placas"] == ["ABC-123"]
