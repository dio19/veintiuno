# /demo — La muestra

Lo que se le enseña a un hotelero mañana a la mañana: **la Radiografía del 21%**,
el producto de entrada de Veintiuno.

No es un mockup. Es un motor que corre.

## Qué hay acá

```
demo/
├── radiografia-demo.html      El informe que ve el cliente (publicado como artifact)
├── datos/
│   ├── reservas.csv           800 reservas — imita el export del PMS
│   └── liquidacion.csv        528 liquidaciones con BIN — imita la pasarela
└── salida/
    ├── radiografia.json       KPIs + cortes por mes, canal y país
    └── detalle_estadias.csv   Las 800 estadías con estado y motivo
```

## Cómo correrlo

El motor y el generador viven en el skill `radiografia-21`; estos comandos se corren
desde la raíz del repo:

```bash
python3 .claude/skills/radiografia-21/references/generar_datos_demo.py --salida demo/datos
```

```bash
python3 .claude/skills/radiografia-21/scripts/motor_radiografia.py \
    --reservas demo/datos/reservas.csv \
    --liquidacion demo/datos/liquidacion.csv \
    --hotel "Demo Recoleta 42" \
    --salida demo/salida \
    --demo
```

El generador tiene semilla fija: siempre produce el mismo dataset.

Sin dependencias externas: sólo la librería estándar.

## Qué hace el motor

Cruza reservas contra liquidaciones y evalúa las tres condiciones del régimen
(**RG Conjunta 3971/2016 AFIP/ARCA + Res. 566/2016 MinTur**):

1. **Residencia** — el huésped no puede residir en Argentina.
2. **Medio de pago** — tarjeta emitida en el exterior (se resuelve por BIN) o
   transferencia desde un banco del exterior. El pago local no habilita.
3. **Alcance** — alojamiento y desayuno incluido. Los consumos extra quedan fuera.

Y clasifica cada estadía en cinco estados: `correcto`, `fuga`,
`riesgo_legajo` (factura T emitida sin documentación archivada), `revisar`
(no residente con BIN no reconocido: requiere verificación manual) y
`no_elegible`, cada uno con su motivo en texto.

## El resultado de esta corrida

| | |
|---|---|
| Reservas analizadas | 800 (2.196 noches; ventana real 91 días, del primer check-in al último check-out) |
| Estadías elegibles | 172 (21,5%) |
| IVA en juego | ARS 8.339.703 |
| **Fuga detectada** | **ARS 3.819.535** — 75 estadías, tasa de fuga 43,6% |
| En riesgo por legajo | ARS 864.852 — 18 estadías |
| Mensualizado / anualizado | ARS 1.259.187 / ARS 15.320.113 |

El filtro que da credibilidad: de **347 huéspedes no residentes**, sólo **172**
califican. 96 pagaron con tarjeta emitida en Argentina y 79 por medios no
habilitantes. Contar a los 347 duplicaría el número y no resistiría una
fiscalización.

## Aviso

Datos **sintéticos**. «Demo Recoleta 42» no existe. Los BIN son ficticios; en
producción se resuelven contra un proveedor con cobertura global. El motor
prepara y prueba: **no brinda asesoramiento fiscal**.
