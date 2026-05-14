from datetime import date

import pytest

from interfaz.formulario import validar_fecha_nacimiento, validar_nombre_usuario


@pytest.mark.parametrize(
    "usuario,esperado",
    [
        ("juan_perez01", True),
        ("Ana_2026", True),
        ("abc", False),
        ("usuario_demasiado_largo_01", False),
        ("1juan", False),
        ("_juan", False),
        ("juan_", False),
        ("juan__perez", False),
        ("juan-perez", False),
        ("juan perez", False),
    ],
)
def test_validar_nombre_usuario(usuario, esperado):
    ok, _ = validar_nombre_usuario(usuario)
    assert ok is esperado


@pytest.mark.parametrize(
    "fecha,hoy,esperado",
    [
        ("13/05/2026", date(2026, 5, 13), True),
        ("12/05/2026", date(2026, 5, 13), True),
        ("14/05/2026", date(2026, 5, 13), False),
        ("01/01/2099", date(2026, 5, 13), False),
        ("29/02/2023", date(2026, 5, 13), False),
    ],
)
def test_validar_fecha_nacimiento_no_permite_futuro(fecha, hoy, esperado):
    ok, _ = validar_fecha_nacimiento(fecha, hoy=hoy)
    assert ok is esperado
