"""Constructores de Dossier para los tests. Hotel ficticio, nunca un prospecto real."""

from investigacion_hotel.modelo import Dossier, Hallazgo, Fuente, VERIFICADO, SIN_VERIFICAR


def dossier(hotel="Hotel Prueba Veintiuno", ciudad="Buenos Aires", **campos):
    """Arma un dossier con los campos dados ya VERIFICADOS.

    Para dejar un campo sin verificar, simplemente no lo pases: un hallazgo que
    no esta, y uno que esta sin fuente, valen lo mismo para el resto del sistema.
    """
    d = Dossier(hotel, ciudad)
    for campo, valor in campos.items():
        d.hallazgos[campo] = Hallazgo(
            campo,
            valor,
            VERIFICADO,
            Fuente(f"https://ejemplo.test/{campo}"),
            cita="cita de prueba",
            confianza="alta",
        )
    return d


def sin_fuente(d, campo, valor):
    """Agrega un hallazgo SIN fuente, como quedaria uno que el agente no pudo respaldar."""
    d.hallazgos[campo] = Hallazgo(campo, valor, SIN_VERIFICAR, None, "", "baja")
    return d
