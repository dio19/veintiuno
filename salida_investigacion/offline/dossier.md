# Dossier · Hotel Prueba Veintiuno

> MATERIAL INTERNO DE VENTA - NO DISTRIBUIR
> Este documento es sobre un hotel identificable y se arma con fuentes públicas.
> No es un informe fiscal ni asesoramiento fiscal: prepara una conversación comercial.
> No compartir fuera de Veintiuno sin autorización escrita de Dionisio.

Generado: 2026-09-15T21:43:18 · Ciudad: Buenos Aires

## Veredicto

**Indeterminado** — 71 puntos sobre los 80 que se pudieron evaluar (de 100 posibles)

Falta el dato de idioma de las reseñas, que es el proxy central del ICP. Sin eso el puntaje no califica nada.

Sin dato para 1 de 8 preguntas: % de reseñas en idioma extranjero.

## Calificación — las 8 preguntas de `business/ideal-customer.md`

| # | Pregunta | Puntos | Detalle |
|---|---|---|---|
| 1 | % de reseñas en idioma extranjero | — /20 | sin dato verificado |
| 2 | Cantidad de habitaciones | 10/10 | 38 habitaciones |
| 3 | Independiente o de cadena | 15/15 | independiente |
| 4 | Decisor con nombre y contacto directo | 6/15 | sólo contacto genérico |
| 5 | Sitio en inglés y motor de reserva propio | 10/10 | inglés: sí · motor propio: sí |
| 6 | ADR publicado en fecha alta | 10/10 | ARS 115.000 |
| 7 | Ubicación en el corredor de receptivo | 10/10 | recoleta |
| 8 | Menciona exención o publica en USD | 10/10 | menciona la exención |

## Qué sabemos del hotel

### Identificación

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Direccion completa | AV. CALLAO 1234 | [1] | direccion: AV. CALLAO 1234 |
| Barrio de CABA, o localidad si está fuera | Recoleta | [2] | 38 habitaciones en el corazón de Recoleta |
| Categoria declarada: estrellas, boutique, apart | 3 Estrellas | [1] | tipo: 3 Estrellas |
| Figura en el dataset abierto de Alojamientos Turisticos del GCBA | sí | [1] | nombre: Hotel Prueba Veintiuno |
| URL del sitio propio | https://hotelpruebaveintiuno.test | [1] | web: https://hotelpruebaveintiuno.test |

### Tamaño y estructura

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Cantidad de habitaciones | 38 | [2] | 38 habitaciones en el corazón de Recoleta |
| Pertenencia a cadena | independiente | [2] | Hotel Prueba Veintiuno |

### Señales de pago del exterior

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Publica tarifas en dólares | sí | [2] | Habitacion Standard desde USD 95 por noche |
| Menciona 'tax free', 'VAT' o exención de IVA en algún canal propio | sí | [2] | may be eligible for a tax free rate |

### Canal de venta

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Tarifa publicada por noche en pesos, con IVA, en fecha alta | ARS 115.000 | [2] | Tarifas en pesos: ARS 115.000 la noche, IVA incluido |
| Tiene motor de reserva directa en su sitio | sí | [2] | Reservar ahora |
| PMS o booking engine identificado por la huella de la URL | Cloudbeds | [2] | Reservar ahora |

### Presencia online

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Tiene versión en inglés real, no traductor automático | sí | [2] | International guests |
| Usuario de Instagram | @hotelpruebaveintiuno | [2] | Instagram |
| El hotel responde las reseñas públicas | SIN VERIFICAR | SIN VERIFICAR |  |

### Decisor

| Campo | Valor | Fuente | Cita |
|---|---|---|---|
| Vía de contacto profesional publicada | reservas@hotelpruebaveintiuno.test | [2] | reservas@hotelpruebaveintiuno.test |
| El único contacto disponible es un mail genérico (info@, reservas@) | sí | [2] | reservas@hotelpruebaveintiuno.test |

## IVA en juego — estimación preliminar

*IVA en juego: el impuesto sobre las estadías que podrían encuadrar en el régimen de exención. NO es la fuga: qué porción se está facturando mal sólo lo dice la Radiografía sobre el export del hotel.*

**Sin numero.** Falta un insumo observable: proporción de huéspedes no residentes. Se resuelve mirando el sitio del hotel o su ficha en una OTA; hasta entonces no se emite número.

| Insumo | Valor | Procedencia | Fundamento |
|---|---|---|---|
| habitaciones | 38 hab | observado [2] | Cantidad de habitaciones publicada |
| ADR publicado con IVA | ARS 115.000 | observado [2] | Tarifa por noche publicada en fecha alta |
| proporción de huéspedes no residentes | SIN VERIFICAR | SIN VERIFICAR SIN VERIFICAR | Proxy: idioma de las reseñas públicas, muestra sin precisar. No es la mezcla real de nacionalidades del PMS. |
| ocupación | 50% a 65% | supuesto | Ocupación general de CABA ~65% en julio 2026; los 2-3 estrellas entre 45-50%. Ver README.md y research/customer-acquisition.md. |
| pago desde el exterior | 35% a 55% | supuesto | Proporción de huéspedes no residentes que paga con tarjeta emitida en el exterior o transferencia del exterior. SIN VERIFICAR: la corrida de la demo dio ~50%, pero es un supuesto del generador sintético, no un dato de campo. Es exactamente la hipótesis 1 del README, todavía sin validar. |

## Lo que este dossier NO puede responder

El país emisor de la tarjeta (BIN) NO se ve desde afuera. Todo lo que figura abajo como señal de pago del exterior es eso, una señal: nunca una medición. La medición sale del cruce de reservas contra liquidación, y eso es la Radiografía.

- ocupación real
- ADR real facturado
- mezcla real de nacionalidades del PMS
- porcentaje real de pago con tarjeta emitida en el exterior
- facturación
- qué comprobante emite hoy por cada estadía

Todo eso sale del cruce de reservas contra liquidación de la pasarela, es decir, de la Radiografía del 21%. Este documento prepara esa conversación; no la reemplaza ni la anticipa.

## Verificación pendiente

Dos minutos a mano cierran cada uno de estos. Se responden editando `dossier.json` y volviendo a correr con `--rehacer`, sin costo de API.

- **responde_resenas** — Confirmar 'responde_resenas' = True
  - https://hotelpruebaveintiuno.test
  - por qué importa: el agente lo encontró pero no se pudo comprobar: la cita no aparece en la fuente citada
- **pct_resenas_idioma_extranjero** — Que porcentaje de las últimas 30 reseñas está en inglés, portugués, francés o alemán?
  - https://www.booking.com/
  - por qué importa: vale 20 puntos del ICP y es el proxy central de no residentes

## Interpretación

*Esto es lectura del agente sobre cómo entrar, no un dato sobre el hotel. Se discute; no se cita.*

- **Angulo de entrada:** Ya menciona 'tax free' en la sección en inglés pero no dice factura T: o lo opera sin legajo, o lo promete y no lo cumple. Las dos son venta.
- **Objecion esperada:** 'Eso lo maneja mi contador'. Respuesta: el legajo lo protege a el, por eso el contador es aliado y no obstaculo.
- **Proximo paso:** Mail al contacto publicado pidiendo el nombre del gerente.

## Fuentes

[1] https://data.buenosaires.gob.ar/dataset/alojamientos-turisticos/resource/juqdkmgo-51-resource/download (consultada 2026-09-15)
[2] https://hotelpruebaveintiuno.test (consultada 2026-09-15)

## Consumo de la corrida

- turnos: 0/24
- búsquedas web: 0/8
- páginas leídas: 1/12
- verificaciones de cita: 0
- tokens entrada: 0
- tokens salida: 0
- duración: 0s
