# Veintiuno — Pricing

Todos los números de este documento salen del **caso testigo** y de sus supuestos. Los supuestos están marcados como tales. Si cambiás un supuesto, cambia el resultado.

## El caso testigo (supuestos explícitos)

| Variable | Valor | Origen |
|---|---|---|
| Hotel | 42 habitaciones, 3★ superior, Recoleta | caso construido |
| Ocupación | 58% → 42 × 0,58 × 30 = **731 noches-hab/mes** | supuesto |
| Huéspedes extranjeros | 45% → 329 noches | **supuesto** |
| Pagan con tarjeta emitida en el exterior o transferencia del exterior | 55% → **181 noches elegibles/mes** | **supuesto** |
| ADR | ARS 95.000 con IVA → neto **ARS 78.512** (95.000 / 1,21) | supuesto |
| IVA en juego | 181 × 78.512 × 0,21 = **ARS 2.984.241/mes** | derivado |
| Fuga actual | 40% de lo elegible se factura mal → **ARS 1.193.696/mes** | **supuesto** |
| Tipo de cambio | **ARS 1.500 = USD 1** — supuesto ajustable, no es una cotización | supuesto |

Dos números que se usan en todo el resto: **IVA por estadía elegible = 78.512 × 0,21 = ARS 16.487** y **fuga por estadía elegible = 16.487 × 0,40 = ARS 6.595**.

---

## Los planes

| Plan | Precio de referencia | En pesos (a 1.500) | Alcance | Tope |
|---|---|---|---|---|
| **Radiografía del 21%** | Sin cargo | — | Diagnóstico de 90 días, fuga cuantificada | Una vez por hotel |
| **Recepción** | USD 120/mes | ARS 180.000 | Módulos 1-3 (detector de fuga, legajo, informativo) | 60 estadías exentas/mes |
| **Recupero** | USD 240/mes | ARS 360.000 | Módulos 1-4 + panel de recupero + soporte prioritario | 200 estadías exentas/mes |
| **Performance** | 6% del IVA correctamente exceptuado, **piso USD 90/mes** | piso ARS 135.000 | Módulos 1-3 | Sin tope |
| **Onboarding** | USD 350 única vez | ARS 525.000 | Implementación de 7 días | Bonificado en piloto |

**Facturación en pesos, factura A**, ajuste trimestral por índice pactado, sin permanencia, baja con 30 días.

---

## Por qué estos precios (anclaje en valor, no en costo)

El precio no está anclado en lo que cuesta el software; está anclado en el IVA que el hotel tiene en juego todos los meses.

**El fee como porcentaje del IVA en juego (caso testigo, ARS 2.984.241/mes):**

- Recepción: 180.000 / 2.984.241 = **6,0%**
- Recupero: 360.000 / 2.984.241 = **12,1%**
- Performance: 6% por definición

**El fee como múltiplo del valor recuperado (fuga de ARS 1.193.696/mes):**

- Recepción: 1.193.696 / 180.000 = **6,6x**
- Recupero: 1.193.696 / 360.000 = **3,3x**
- Performance: 6.595 / 989 = **6,7x fijo** (porque cobramos 6% y recuperamos 40%: 0,40 / 0,06 = 6,67 — el múltiplo no depende del volumen)

Comparación de referencia: una OTA se lleva **15-20% del valor bruto de la reserva** (Booking), 15-25% (Expedia), 10-18% (Despegar). Nosotros nos llevamos 6-12% de un impuesto que hoy el hotel está pagando entero. Es el argumento de anclaje más fuerte que tenemos y hay que usarlo así, textual.

---

## ROI del hotel testigo, por plan

Valor considerado: **solo la fuga que deja de ocurrir** (ARS 1.193.696/mes). No cuento la ventaja de precio del 17,4% ni la reducción de riesgo fiscal, que son reales pero no se pueden cuantificar sin más supuestos.

| Plan | Costo mensual | Costo año 1 (con onboarding) | Valor año 1 | Retorno neto año 1 | Múltiplo |
|---|---|---|---|---|---|
| Recepción* | 180.000 | 180.000×12 + 525.000 = 2.685.000 | 14.324.352 | **11.639.352** | 5,3x |
| Recupero | 360.000 | 360.000×12 + 525.000 = 4.845.000 | 14.324.352 | **9.479.352** | 3,0x |
| Performance | 179.054 (6% de 2.984.241) | 179.054×12 + 525.000 = 2.673.648 | 14.324.352 | **11.650.704** | 5,4x |

\* Recepción no aplica a este hotel: 181 estadías supera el tope de 60. Se muestra solo como referencia de anclaje. **El hotel testigo va a Recupero.**

Con onboarding bonificado (piloto), Recupero da 4.320.000 de costo anual contra 14.324.352 de valor: **3,3x**, y el costo de los doce meses se repaga con **3,6 meses** de fuga recuperada (4.320.000 / 1.193.696).

---

## Contra el stack que ya paga

Un hotel chico gasta **USD 400-600/mes** en software, todo en dólares, facturando en pesos. Pxsol (PMS + CM + motor) USD 180/mes; SiteMinder USD 85-119.

- Recupero (USD 240) es un **+40 a +60% sobre el stack**. Es plata. Pero es la **única línea del stack que genera ingreso**: el PMS, el channel manager y el motor son costos de operar; Veintiuno devuelve pesos facturables.
- Una suscripción en USD pagada con tarjeta arrastra hasta **~+59%** entre IVA y percepciones: los USD 180 de Pxsol cuestan ~USD 286 reales. Nuestros USD 120 **facturados en pesos con factura A** equivalen a pagar ~USD 75 afuera (120 / 1,59). **Facturar en pesos es, en sí mismo, parte del precio.**

---

## Moneda, ajuste y topes

- **Precio de referencia en USD, cobro en pesos**, al tipo de cambio del día de emisión. El hotel nunca toca una tarjeta internacional por nosotros.
- **Ajuste trimestral** por índice pactado en el contrato (se pacta al firmar; no se ajusta de manera discrecional ni fuera de esa ventana).
- **Excedente de tope:** cada estadía exenta por encima del tope se factura al equivalente de **USD 1,50** (Recepción) o **USD 1,00** (Recupero). Está deliberadamente **por debajo** del costo por estadía del plan (Recepción incluye 60 por USD 120 = USD 2,00 por estadía) para que a nadie le convenga esconder volumen o dejar estadías sin procesar.
- **Dos meses seguidos por encima del tope** → migración automática al plan siguiente, con aviso previo. Arriba de 200 estadías/mes es plan a medida.
- **Pago anual anticipado: 10% de descuento** y **precio congelado los 12 meses, sin ajuste trimestral**. El descuento es 10% y no 20% justamente porque el riesgo de índice lo asumimos nosotros.

**Traducción de los topes a tamaño de hotel** (con los supuestos del caso: 45% × 55% = **24,75% de las noches son elegibles**, ocupación 58%):

- 60 estadías/mes ⇒ 60 / 0,2475 / 0,58 / 30 ≈ **14 habitaciones**
- 200 estadías/mes ⇒ 200 / 0,2475 / 0,58 / 30 ≈ **46 habitaciones**

O sea: **Recepción es para hoteles de hasta ~14 habitaciones; el ICP de 15 a 46 habitaciones cae entero en Recupero.** Conviene saberlo antes de una reunión.

---

## Cuándo NO le conviene a un hotel contratarnos

**Punto de equilibrio.** El hotel empata cuando la fuga que deja de tener iguala el fee:

> **N\* = fee mensual ÷ (ADR/1,21 × 0,21 × tasa de fuga)**

Con ADR 95.000 y fuga 40% (ARS 6.595 por estadía):

- Recepción (180.000): **27 estadías elegibles/mes**
- Recupero (360.000): **55 estadías elegibles/mes**
- Performance en el piso (135.000): **21 estadías elegibles/mes**

Con ADR 60.000, la cuenta se endurece: la fuga por estadía cae a ARS 4.165 y Recepción necesita **43 estadías elegibles/mes**.

**No le vendas a un hotel si:**

1. Tiene **menos de ~40 estadías elegibles por mes** (empatar no es vender: por debajo de 3x no aguanta el mes 6 y se da de baja). Con ADR bajo, subí el corte.
2. Su mezcla de extranjeros es **menor al 15%** y no está creciendo: aunque tenga volumen, el número no llega.
3. Cobra casi todo con **tarjeta local, efectivo o Mercado Pago** — sin tarjeta emitida en el exterior ni transferencia del exterior, no hay exención por más extranjeros que tenga. Este es el filtro que más prospectos mata y hay que preguntarlo temprano.
4. **No está inscripto o no puede emitir clase T**, y su contador no quiere gestionarlo. No somos su gestoría.
5. Está en un **PMS que no exporta** reservas en ningún formato razonable y no hay voluntad de pedirlo. Sin dato de entrada no hay producto.

En estos casos, la Radiografía se entrega igual, se dice "no te conviene" y se cierra. Un cliente que se da de baja en el mes 4 cuesta más que el que nunca firmó.

---

## Unit economics del lado nuestro (estimaciones, no medidas)

Por hotel y por mes, en USD:

| Concepto | Recepción (~60 estadías) | Recupero (~180 estadías) |
|---|---|---|
| Procesamiento de documentos con AI (~2,5 docs por estadía, USD 0,015-0,03 por doc) | 2,5 - 4,5 | 7 - 14 |
| Infraestructura (almacenamiento de legajos, backups, cómputo) | 3 - 5 | 4 - 6 |
| Soporte (0,5-1 h/mes a USD 15/h cargada) | 8 - 12 | 8 - 15 |
| **COGS total** | **14 - 22** | **19 - 35** |
| **Margen bruto** | **~82-88%** | **~85-92%** |

Margen bruto objetivo de referencia: **~85%**. El onboarding de USD 350 cubre entre 4 y 6 horas de implementación (USD 100-150 de costo): aporta, pero no es un centro de ganancia y por eso se bonifica sin drama en el piloto.

---

## Nota de arbitraje entre planes (para revisar)

Con los supuestos de arriba, **Performance cuesta menos que Recepción para cualquier hotel de menos de 182 estadías elegibles/mes**: el cruce está en 180.000 / (16.487 × 0,06) = **182 estadías**. Como el tope de Recepción es 60, dentro del alcance de Recepción el hotel siempre paga menos con Performance (en el tope: 6% de 60 × 16.487 = ARS 59.355, o sea aplica el piso de ARS 135.000 = USD 90, contra USD 120). Recomendación operativa: **Performance no se publica en la web ni se ofrece de entrada**; se usa solo cuando el hotel rechaza el costo fijo, y con compromiso mínimo de 6 meses. Si se publica, hay que subir el piso a USD 120 o bajar el precio de Recepción.
