"""
Veintiuno - investigacion_hotel · Bloque normativo congelado
============================================================
Copia literal del marco que fija .claude/skills/radiografia-21/SKILL.md. Es la
ÚNICA descripción del régimen que esta librería puede usar: ni el agente ni el
render arman una propia.

Por qué congelado: la distinción entre este régimen y la RG 5843/2026 (tax free
minorista de bienes, factura B) es parte del valor del producto. Equivocarla lo
invalida. Y un LLM que "explica el régimen con sus palabras" es exactamente
como se cuela esa confusion en un mail que ya salio.

Si hace falta afirmar un requisito que no este acá, se escribe SIN VERIFICAR.
No se completa por analogia.
"""

SIN_VERIFICAR = "SIN VERIFICAR"

MARCO = "RG Conjunta 3971/2016 (AFIP/ARCA) + Res. 566/2016 (Ministerio de Turismo)"

CONDICIONES = (
    "el huésped NO reside en la República Argentina",
    "paga con tarjeta de crédito o débito emitida en el EXTERIOR, o con "
    "transferencia desde un banco del exterior (el pago local no habilita, "
    "sin excepción)",
    "el consumo es alojamiento y desayuno incluido en el precio; cualquier otro "
    "consumo se factura aparte y queda fuera del régimen",
)

COMPROBANTE = "factura electrónica clase T, con autorización previa de ARCA"

# El parrafo tal como puede aparecer en material que ve el hotel.
PARRAFO_PUBLICO = (
    f"Desde el 1 de enero de 2017 rige la {MARCO}: el alojamiento a huéspedes no "
    "residentes está exento de IVA cuando se cumplen tres condiciones a la vez — "
    f"{CONDICIONES[0 ]}; {CONDICIONES[1 ]}; y {CONDICIONES[2 ]}. "
    f"El comprobante que corresponde es {COMPROBANTE}."
)

# Lo que nunca se dice, ni en material interno ni externo.
PROHIBIDO = (
    "prometer el resultado de una fiscalización, o decir que ARCA no va a observar",
    "dar asesoramiento fiscal o resolver un caso límite: preparamos y probamos, "
    "el contador del hotel firma",
    "confundir este régimen con la RG 5843/2026 (tax free minorista de bienes, "
    "factura B): son regímenes distintos, con requisitos y comprobantes distintos",
    "afirmar qué comprobante emite hoy el hotel: desde afuera no se puede saber",
)

# Quitar el IVA de un precio final es -17,36% (1 - 1/1,21), no -21%.
DESCUENTO_EQUIVALENTE_PCT = 17.36
