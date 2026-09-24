"""Utilidades compartidas por los dos renderers."""

from ..modelo import Dossier, SIN_VERIFICAR


def pesos(n) -> str:
    """ARS con separador de miles a la argentina."""
    if n is None:
        return SIN_VERIFICAR
    return "ARS " + f"{int(n ):,}".replace(",", ".")


def rango_pesos(r) -> str:
    if not r:
        return SIN_VERIFICAR
    return f"{pesos(r[0 ])} a {pesos(r[1 ])}"


class IndiceDeFuentes:
    """Numera las fuentes para las notas al pie. Una fuente, un número, aunque
    respalde varios campos."""

    def __init__(self, d: Dossier, campos: list | None = None):
        """Si se pasa `campos`, sólo numera las fuentes de esos campos.

        Un listado con entradas que no se citan en ninguna parte del documento
        se lee como descuido, y en el material externo ademas cuenta de más
        sobre como trabajamos.
        """
        self._orden = {}
        if campos is None:
            fuentes = d.fuentes()
        else:
            fuentes, vistas = [], set()
            for campo in campos:
                h = d.hallazgo(campo)
                if h and h.verificado and h.fuente and h.fuente.url not in vistas:
                    vistas.add(h.fuente.url)
                    fuentes.append(h.fuente)
        for fuente in fuentes:
            if fuente.url not in self._orden:
                self._orden[fuente.url] = len(self._orden) + 1
        self._fuentes = fuentes

    def marca(self, hallazgo) -> str:
        """La nota al pie de un hallazgo, o la marca de que no tiene respaldo.

        Nunca devuelve vacio: un dato sin marca ni nota al pie es exactamente
        lo que este diseno existe para impedir.
        """
        if hallazgo is None or not hallazgo.verificado or not hallazgo.fuente:
            return SIN_VERIFICAR
        return f"[{self._orden.get(hallazgo.fuente.url, '?')}]"

    def listado(self, d: Dossier) -> list:
        salida = []
        for fuente in self._fuentes:
            n = self._orden[fuente.url]
            titulo = f" — {fuente.titulo}" if fuente.titulo else ""
            salida.append(f"[{n}] {fuente.url}{titulo} (consultada {fuente.consultada})")
        return salida
