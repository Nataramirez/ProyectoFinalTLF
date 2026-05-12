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
