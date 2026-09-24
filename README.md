# Veintiuno — CEO summary

**Micro-SaaS para hotelería. Nicho investigado: hoteles de CABA. Septiembre 2026.**

Ejercicio multi-agente: cinco especialistas en paralelo, síntesis, red team, decisión, paquete comercial y muestra funcionando.

---

## Qué encontramos

**El mercado está en modo supervivencia y con más extranjeros que nunca.** CABA tiene 440 hoteles y ~55.000 plazas; unos 150-220 son independientes. En julio de 2026 la ocupación general rondó el 65%, con los 4★ arriba del 60% y los **2-3★ estancados en 45-50%**. Al mismo tiempo, el turismo internacional a la Ciudad creció **19% interanual** (1,61 M de visitantes entre enero y julio). Gabriela Akrabian, de la Cámara de Hoteles de AHRCC: *"El sector sobrevive con endeudamiento, posterga inversiones y ajusta los costos todo lo posible."*

**Los carriles obvios ya tienen dueño.** El de "AI + WhatsApp + reservas" lo ocupa WeSpeak con 500+ hoteles argentinos. El de pricing lo cubren gratis Booking (Opportunity Center) y SiteMinder con IDeaS, y PriceLabs cobra ~USD 10. Nuestra primera elección —un copiloto de tarifas con benchmark de mercado— **murió en el red team**: el competidor gratis ya está adentro del hotel, y el "apagón estadístico" del INDEC resultó menos apagón de lo que creíamos, porque el Observatorio del Ente porteño publica ocupación de CABA y Pxsol ya anunció su módulo de Revenue Management.

**Lo que quedó en pie es aburrido, argentino y nadie lo mira.** Existe desde 2017 un régimen —**RG Conjunta 3971/2016 (AFIP/ARCA) + Res. 566/2016 del Ministerio de Turismo**— que exime del IVA al alojamiento de no residentes que pagan con tarjeta emitida en el exterior o transferencia del exterior. La Ciudad lo promociona en su sitio oficial en inglés. El hotelero no lo puede ejecutar: exige leer un pasaporte, verificar residencia, identificar de dónde salió el plástico, emitir un comprobante de otra clase y armar un legajo que sobreviva a una fiscalización, todo en el minuto y medio de un check-in. Un huésped extranjero, citando a la recepción de un hotel argentino sobre por qué no le aplicaban la exención: *"they don't have the software for it."*

---

## Qué problema resolvemos

El hotel deja sin capturar el 21% de IVA de sus huéspedes extranjeros, y cuando lo captura, muchas veces no puede probarlo.

Son tres pérdidas distintas: **plata que no se cobra o se cobra de más al huésped**, **una ventaja de precio del 17,4% que no se usa**, y **exenciones tomadas sin legajo** que quedan expuestas ante ARCA.

---

## Para quién

**ICP primario:** hotel independiente de 20-60 habitaciones en Recoleta, Palermo, Retiro, San Telmo y Microcentro, con alta proporción de huéspedes extranjeros. Decide el dueño-operador o el gerente general. **60-90 establecimientos en CABA.**

Señales verificables desde afuera: reseñas recientes en inglés y portugués, sitio con versión en inglés, precios publicados en USD.

**Anti-ICP:** hoteles con pocos extranjeros, cadenas internacionales con back-office propio, hostels de ticket bajo, alquileres temporarios no habilitados.

CABA es cabecera de playa, no mercado: **el régimen es nacional** y alcanza también a agencias de viaje habilitadas.

---

## Qué vendemos

**Veintiuno**, en cuatro módulos:

1. **Detector de fuga** — cruza el export de reservas del PMS contra la liquidación de la pasarela e identifica, estadía por estadía, las que calificaban y se facturaron con IVA. La tarjeta emitida en el exterior se detecta por **BIN**.
2. **Legajo probatorio digital** — lectura multilingüe de pasaportes y documentación migratoria con AI, expediente por estadía, listo para una fiscalización.
3. **Régimen informativo mensual** — armado y validado antes del día 15.
4. **Cotización sin IVA** — el precio exento mostrado al huésped extranjero en el canal directo.

**Se vende al lado del PMS, nunca contra el PMS.** No requiere integración: trabaja sobre exports. Y **no damos asesoramiento fiscal**: preparamos y probamos; el contador del hotel sigue siendo el responsable.

---

## Cuánto cobraríamos

| Plan | Precio (facturado en pesos) | Alcance |
|---|---|---|
| **Radiografía del 21%** | Sin cargo | Diagnóstico de 90 días. Es el lead magnet y la demo. |
| **Recepción** | equiv. USD 120/mes | Detector + legajo + régimen informativo. Hasta 60 estadías exentas/mes. |
| **Recupero** | equiv. USD 240/mes | Todo lo anterior + cotización sin IVA + panel. Hasta 200 estadías. |
| **Performance** | 6% del IVA exceptuado, piso equiv. USD 90/mes | Para el hotel que no aprueba costo fijo nuevo. |
| **Onboarding** | equiv. USD 350, bonificable | Por única vez. |

Factura A en pesos, sin permanencia, baja con 30 días. *(Tipo de cambio de referencia supuesto: ARS 1.500 = USD 1.)*

**El anclaje:** en el hotel testigo el fee de Recupero representa el **12%** del IVA en juego y devuelve **5,4×** sobre la fuga que deja de ocurrir. Facturar en pesos es en sí un argumento: una suscripción en USD con tarjeta arrastra hasta ~+59% en IVA y percepciones.

---

## Qué construimos

Una **Radiografía del 21%** completa y funcionando, en `/demo`:

- Un motor en Python que aplica las tres condiciones del régimen estadía por estadía y clasifica en `correcto` / `fuga` / `riesgo_legajo` / `no_elegible`, cada uno con su motivo.
- Un dataset sintético de 90 días (800 reservas, 528 liquidaciones con BIN) con semilla fija.
- El informe que ve el cliente, publicado como página web.

**Resultado de la corrida:** de 800 reservas, 172 elegibles; **ARS 3.819.535 de fuga en 90 días** (75 estadías, tasa de fuga 43,6%), más ARS 864.852 en riesgo por legajo incompleto. Anualizado: **ARS 15.320.113**.

El detalle que da credibilidad: de **347 huéspedes no residentes sólo 172 califican**. 96 pagaron con tarjeta emitida en Argentina y 79 por medios no habilitantes. Contar a los 347 duplicaría el número y no resistiría una fiscalización.

---

## Cómo conseguiríamos el primer cliente

**Regalo primero.** Se arma una lista de 200-300 hoteles en un día cruzando el padrón ENTUR con el dataset abierto del GCBA y enriqueciendo con Google Places y Booking. Se prioriza por señales de volumen de extranjeros. Se manda una estimación preliminar de una página —hecha con datos públicos— y se ofrece la Radiografía real a 48 horas del export.

**Cuatro canales, 30 días:** mail en frío con la estimación adjunta (90 toques), puerta a puerta en Microcentro (60 hoteles caminables, recepción abierta 24/7, nadie del software B2B lo hace), alianza con estudios contables de hotelería (el legajo protege al contador: es el aliado natural) y **FIT América Latina, 26-29 de septiembre en La Rural**.

**Embudo:** ~205 toques → 20 reuniones → 14 radiografías → **5 cierres**. La tasa crítica es radiografía→cierre: si baja de 25%, el problema es la oferta, no el canal.

**Piloto pago, no gratis.** El descuento va en el plazo, no en el precio.

---

## Qué hipótesis todavía debemos validar

| # | Hipótesis | Cómo se testea | Fatal si es falsa |
|---|---|---|---|
| 1 | **La fuga es material en hoteles reales.** Nuestro 43,6% es un supuesto del generador, no un dato de campo. | La propia Radiografía, con 5 hoteles. Sin escribir producto. | **Sí.** Si el hotel promedio ya lo hace bien, no hay negocio. |
| 2 | El hotelero entrega su export de reservas y su liquidación a un desconocido. | Pedirlo en la reunión, en el acto. Umbral: 8 de 25 en 72 h sin NDA. | Sí |
| 3 | Aprueba un gasto mensual nuevo estando en modo supervivencia. | Landing con precio + 25 llamadas. Umbral: 5 con monto comprometido. Verbal no cuenta. | Sí |
| 4 | El PMS argentino no lo resuelve ya de punta a punta. | Demo en vivo de Pxsol, MiniHotel, AlojaSys y CQR con un hotelero al lado. | Sí |
| 5 | Qué exige ARCA hoy como respaldo probatorio concreto. | Consulta con dos estudios contables de hotelería. | Define el alcance del módulo 2 |
| 6 | Que el 21% se pueda retener sin fricción con el huésped. | Preguntarlo en las 25 llamadas. | No, pero cambia el pitch |

**La honestidad que corresponde:** el Pain Miner encontró evidencia sólida de dolor y **evidencia débil de intención de pago**. Ni un solo hotelero argentino escribiendo "estoy pagando X por Y". Este mercado no se descubre por internet: se descubre con 15 llamadas.

---

## Qué construiríamos en una semana

| Día | Entregable |
|---|---|
| 1-2 | Lista de 250 hoteles priorizada + estimación preliminar de una página automatizada |
| 3 | Motor de Radiografía sobre exports reales de 2 PMS distintos (Pxsol y uno más) |
| 4 | Resolución de BIN contra proveedor real, reemplazando la tabla ilustrativa |
| 5 | Lectura de pasaporte con AI: foto → campos verificados, con tasa de acierto medida |
| 6 | 40 mails enviados + 15 visitas a Microcentro |
| 7 | 3 Radiografías reales entregadas y las respuestas de la hipótesis 1 |

Al séptimo día no tenemos un SaaS: tenemos **la respuesta a la hipótesis que puede matar el negocio**, y tres hoteles que vieron su propio número.

---

## Estructura de archivos

```
veintiuno/
├── README.md                          Este documento
├── CLAUDE.md                          Guía para Claude Code
│
├── .claude/skills/radiografia-21/     El skill: reglas + motor + generador
│   ├── SKILL.md
│   ├── scripts/motor_radiografia.py   El motor: aplica el régimen estadía por estadía
│   └── references/generar_datos_demo.py
│
├── research/                          Etapa 1 — cinco especialistas en paralelo
│   ├── market-scout.md                Mercado, regulación, procesos manuales
│   ├── pain-miner.md                  Dolores con cita textual y fuente
│   ├── competitor-analyst.md          PMS, RMS, AI hotelera, precios, huecos
│   ├── offer-architect.md             8 ofertas evaluadas y puntuadas
│   ├── customer-acquisition.md        ICP, universo, canales, primeros 5
│   └── 00-sintesis-lead-agent.md      Etapa 2 — cruce, matriz y elección
│
├── validation/                        Etapa 3 y 4
│   ├── devils-advocate.md             Red team: veredicto MATAR
│   └── decision-lead-agent.md         Qué de la crítica acepté y qué no
│
├── business/                          Etapa 5 — la oferta
│   ├── offer.md                       Oferta, alcance, onboarding, objeciones
│   ├── ideal-customer.md              ICP, anti-ICP, checklist de calificación
│   ├── pricing.md                     Planes, anclaje en valor, unit economics
│   ├── value-proposition.md           Pitch de 30 s y de 2 min, diferenciación
│   ├── first-5-customers.md           Plan de 30 días con embudo numérico
│   └── outreach.md                    13 materiales listos para copiar
│
└── demo/                              Etapa 6 — la muestra
    ├── README.md                      Cómo correrlo y qué da
    ├── radiografia-demo.html          El informe que ve el cliente
    ├── datos/
    │   ├── reservas.csv
    │   └── liquidacion.csv
    └── salida/
        ├── radiografia.json
        └── detalle_estadias.csv
```
