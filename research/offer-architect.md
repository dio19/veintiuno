# ESPACIO DE OFERTAS — Micro-SaaS con AI para hoteles independientes de CABA
**Rol:** Offer Architect · **Fecha:** septiembre 2026 · **Estado:** exploración, sin ganadora elegida

---

## 0. CALIBRACIÓN ECONÓMICA (lo verificado y lo supuesto)

### Datos verificados
- Comisiones OTA: promedio actual **15–30%+**, contra ~10% hace una década ([Cloudbeds](https://www.cloudbeds.com/online-travel-agencies/commissions/)).
- Las OTAs concentran el **63,4% de las reservas de hoteles independientes**; el RevPAR de independientes cayó **5,4% en 2025**; la mano de obra pesa **47–60% del opex**; solo el **41% de los independientes usa AI** (vs 80% de las cadenas) y el **67% señala "sistemas desconectados"** como principal problema, perdiendo **1–2 jornadas de trabajo por semana** conciliando datos ([Hospitality Net, 2026](https://www.hospitalitynet.org/news/4132167/six-forces-reshaping-independent-hotels-in-2026-including-ai-discovery-margin-pressure-and-the-connectivity-imperative)).
- Conversión de web/motor propio: **2,2–3,9%** promedio; boutique/lujo **1,8–2,5%**; OTAs **12–15%** ([BookBetterDirect](https://bookbetterdirect.com/hotel-website-conversion-rate-benchmarks-2026-direct-booking-vs-otas/)).
- Reseñas: el estudio de Cornell (Anderson) muestra que **el ingreso empieza a caer cuando se responde más del 40% de las reseñas**, y responder al 85%+ rinde **peor que no responder**. Lo que sí mueve la aguja es el **volumen**: el índice de reseñas saltó de 86,1 a 224,4 y el ranking de 46,8 a 42,0 ([Cornell SHA](https://sha.cornell.edu/wp-content/uploads/sites/4/2019/03/anderson-engaged-consumers.pdf)).
- Upsell: benchmark Oaky sobre 1.100 hoteles → el mejor segmento genera **€38,39 por habitación por mes** ([Revfine](https://www.revfine.com/upselling-hotel/)).
- WhatsApp Business Platform: **precio por mensaje** desde el 1/7/2025; conversaciones de servicio **gratis** y plantillas *utility* gratis dentro de la ventana abierta ([Meta](https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing)). Tarifas indicativas Argentina: **marketing USD 0,0618 / utility USD 0,0120 / auth USD 0,0220** ([Ominiflow](https://ominiflow.com/whatsapp-api-pricing/argentina)).
- Descubrimiento: el uso de buscadores tradicionales para planificar viajes cayó de **51% a 36% en un año**, y el uso de plataformas generativas más que se duplicó (Hospitality Net, ídem).
- Revinate 2026: solo **16% de los huéspedes responde mensajes de texto** del hotel; el ingreso por email cayó **19% global**; **22% de los emails vienen enmascarados por OTAs**; la automatización resuelve **31% de los mensajes en 1,8 s vs 3 minutos** ([Revinate](https://www.revinate.com/blog/2026-hospitality-benchmark-report-key-insights/)).
- CABA, julio 2026: ocupación promedio **~65%** (2–3 estrellas 45–50%, 4 estrellas 60%+); tarifas desde **ARS 55.000 (3★) y 65.000 (4★) por persona**; salarios, energía, alimentos, lavandería e impuestos subieron **por encima de las tarifas** ([Ámbito](https://www.ambito.com/negocios/hoteles-alerta-la-ocupacion-ronda-el-65-que-estrategias-trazan-sobrevivir-n6304861)).
- Tipo de cambio 8/9/2026: blue 1.525/1.545, oficial 1.480/1.530, MEP 1.526,73 ([El Cronista](https://www.cronista.com/finanzas-mercados/dolar-blue-como-cerro-su-cotizacion-hoy-martes-8-de-septiembre/)).
- Fiscal: los hoteles emiten **Factura T** (códigos 195/196/197) por alojamiento y desayuno a turistas extranjeros no residentes, con autorización previa de ARCA; la RG 5866/2026 fija liquidación mensual desde julio 2026 ([Anfy](https://anfy.app/blog/facturacion-electronica-hoteles-arca.html)). **Ojo:** la RG 5843/2026 de validación digital del reintegro de IVA aplica a **comercios minoristas, no a hoteles** ([Microjuris](https://aldiaargentina.microjuris.com/2026/05/06/legislacion-reintegro-de-iva-a-turistas-arca-implementa-nuevo-regimen-de-validacion-digital/)). No vendas lo que no es.

### El hotel modelo (TODO SUPUESTO, defendible)
> 40 habitaciones · ocupación 65% · **780 noches/mes** · ADR **ARS 85.000 ≈ USD 55** (supuesto: mezcla 3★ alta con desayuno, extranjeros y corporativo).
> **Ingreso habitación ≈ ARS 66,3M ≈ USD 43.300/mes.**
> OTA 63,4% → 494 noches → USD 27.400 por canal OTA → **comisión ~18% = USD 4.930/mes ≈ ARS 7,5M**.
> **Regla de oro del pricing:** mover **5 puntos de share de OTA a directo** = 39 noches = USD 2.145 de ingreso reasignado y **~USD 386/mes de comisión ahorrada**. Ese es el techo natural de una herramienta de canal.
> **Presupuesto de software:** supuesto 2–4% del ingreso habitación = **USD 870–1.730/mes para TODO el stack** (PMS + channel manager + motor + pasarela). Un proveedor nuevo, sin marca, realistamente captura **USD 80–400/mes**. Cualquier oferta que exija más de USD 500/mes necesita desplazar a un incumbente, no sumarse.

---

## 1. FISCO HUÉSPED — Factura T y legajo de no residentes
Motor que lee pasaporte/documento y datos de la reserva, decide si el huésped califica como no residente, emite la **Factura T** correcta, arma el legajo probatorio (imagen de documento, sello migratorio, medio de pago del exterior) y concilia mensualmente contra el libro IVA ventas.

- **DOLOR:** el hotel aplica mal la exención por miedo o por desprolijidad. Si la aplica sin respaldo, el ajuste es el **21% de IVA** sobre esas noches; si no la aplica, queda **21% más caro** que el competidor que sí la aplica. Supuesto: 30% de las noches son extranjeros no residentes = 234 noches × USD 55 = **USD 12.870/mes expuestos**. Un ajuste sobre un año son **~USD 32.000**. Además, supuesto de 8 h/mes de administración conciliando.
- **COMPRADOR:** el **dueño**, con el contador externo como influenciador decisivo (y como canal de distribución: un estudio contable de turismo puede traerte 15 hoteles).
- **RESULTADO:** cero diferencias entre PMS y libro IVA al cierre de mes, en 60 días; legajo completo por reserva.
- **IMPLEMENTACIÓN: 3/5.** No requiere PMS: se puede empezar leyendo el export CSV/Excel de reservas + carga de documentos por web. Sí requiere webservice de ARCA (WSFE) o integrarse a un facturador existente. La complejidad real es **normativa, no técnica**.
- **DISPOSICIÓN A PAGAR: USD 120–250/mes (ARS 184.000–383.000).** Se ancla en riesgo evitado, no en horas.
- **RECURRENCIA: alta.** El riesgo fiscal no se agota: cada mes hay huéspedes nuevos y la normativa se mueve.
- **VENTAJA DE AI: media-alta y honesta.** OCR + extracción de documentos multilingües y clasificación de residencia es genuinamente AI. La emisión es CRUD. Sin AI, esto es un formulario.
- **MVP: 2–3 semanas.** Semi-manual total: el hotel sube el export, tu equipo procesa, devolvés PDF de conciliación + legajos. Nadie se entera de que hay un humano.
- **RIESGO PRINCIPAL:** que el contador del hotel diga "esto ya lo hago yo" y lo mate gratis. Y el riesgo de responsabilidad: si emitís mal, el problema es tuyo.

---

## 2. TERMÓMETRO DE TARIFAS — repricing anti-inflación en ARS y USD
Agente que reprecia el tarifario contra inflación proyectada, evolución del tipo de cambio y costos del hotel, y **alerta cuando una reserva vendida a 60–120 días ya perdió margen en dólares**. Salida: propuesta de tarifario nuevo, no cambio automático.

- **DOLOR:** el hotel vende con meses de anticipación contra costos que no puede prever (verificado, Ámbito). Supuesto: 25% de las noches se venden con más de 60 días de anticipación y pierden 8% de margen real = 195 noches × USD 55 × 8% = **USD 858/mes de margen evaporado**, ~USD 10.300/año.
- **COMPRADOR:** **dueño**. En 40 habitaciones no hay revenue manager; hay un dueño con un Excel.
- **RESULTADO:** ADR real en USD estable o creciente vs. mes anterior; margen por noche visible por primera vez. 60–90 días.
- **IMPLEMENTACIÓN: 3/5.** Necesita el tarifario y el pickup. Se puede leer del channel manager por export, sin tocar el PMS. Publicar tarifas sí exige integración; **no la hagas en el MVP** — entregá recomendación, que el hotel cargue.
- **DISPOSICIÓN A PAGAR: USD 150–350/mes (ARS 230.000–535.000).** Es lo más cercano a "esto me hace ganar plata" que hay en la lista.
- **RECURRENCIA: muy alta.** Mientras haya inflación y brecha, el problema se renueva cada mes. En Argentina eso es estructural.
- **VENTAJA DE AI: baja-media. Sé honesto: el 80% de esto es una planilla con series de precios y un modelo de costos.** La AI aporta en el pronóstico de demanda y en explicar la recomendación en lenguaje natural, que es lo que hace que el dueño la ejecute. Es un adorno *útil*, no el núcleo.
- **MVP: 2 semanas.** Semi-manual: un analista corre el modelo y manda un PDF semanal por WhatsApp. Escala hasta ~25 hoteles a mano.
- **RIESGO PRINCIPAL:** que Argentina se estabilice y el dolor se enfríe. También que el dueño no ejecute la recomendación y culpe a la herramienta.

---

## 3. RADAR DE PARIDAD Y FUGAS DE COMISIÓN *(no es un chatbot)*
Rastrea diariamente Booking, Expedia, Despegar, Airbnb y metabuscadores; detecta **undercutting de bedbanks y mayoristas**, disparidades del propio channel manager y errores de carga (habitación cerrada, restricción mal puesta, tarifa vieja). Entrega el reclamo redactado y listo para enviar a la OTA.

- **DOLOR:** el hotel descubre que un mayorista lo vende 15% más barato que su propia web, o que una categoría estuvo cerrada tres semanas. Supuesto: 3% de las noches se pierden o se venden mal por errores de carga = 23 noches × USD 55 = **USD 1.265/mes**. Verificado que el 67% de los independientes sufre sistemas desconectados.
- **COMPRADOR:** **dueño** o gerente general. En hoteles de 60+, el jefe de recepción/reservas.
- **RESULTADO:** número de disparidades detectadas y corregidas por mes; noches recuperadas. Resultado visible en la **primera semana** — es la oferta de demo más fácil de todas.
- **IMPLEMENTACIÓN: 4/5.** **Cero integración con PMS.** Scraping + comparación. Barrera: anti-bot de las OTAs y costo de proxies.
- **DISPOSICIÓN A PAGAR: USD 100–200/mes (ARS 153.000–306.000).** Techo bajo: se percibe como "informe", no como sistema.
- **RECURRENCIA: media.** Riesgo real de que el hotel arregle las 5 fugas grandes en el mes 1 y cancele en el mes 4. **Mitigación:** convertirlo en informe de competencia (tarifas de los 8 hoteles del barrio), que nunca se agota.
- **VENTAJA DE AI: baja. Esto es scraping y diffs.** La AI solo sirve para normalizar nombres de habitación y redactar el reclamo. **Decilo así internamente: es un CRUD con buen envoltorio.**
- **MVP: 1–2 semanas.** El más rápido de los ocho. Se puede correr a mano el primer mes.
- **RIESGO PRINCIPAL:** que la OTA bloquee el scraping o que el hotel considere el dato "lindo pero no accionable".

---

## 4. CONSERJE DE UPSELL PRE-ARRIVAL *(secuencia, no chatbot)*
72 h antes del check-in, secuencia por WhatsApp/email con ofertas segmentadas por perfil y por disponibilidad real: upgrade, early check-in, late checkout, traslado desde Ezeiza, desayuno, estacionamiento. Pago con link.

- **DOLOR:** ingreso ancillary cerca de cero. Benchmark verificado: mejores segmentos **€38,39/habitación/mes**. Supuesto conservador para 3★ urbano: **€12/habitación/mes** = 40 × €12 ≈ **USD 520/mes de ingreso nuevo**, con margen alto (un late checkout cuesta casi nada).
- **COMPRADOR:** **dueño**. Es el que ve el número de ingreso extra y firma en la primera reunión.
- **RESULTADO:** ingreso ancillary por habitación disponible; tasa de aceptación de ofertas. Visible en 30 días.
- **IMPLEMENTACIÓN: 2/5.** **Acá sí duele el PMS:** sin disponibilidad real ni datos de reserva, ofrecés upgrades que no existe. Además hay que cargar los cargos de vuelta. Es la barrera más subestimada de la lista.
- **DISPOSICIÓN A PAGAR: USD 90/mes base + 15% del upsell generado (ARS 138.000 + variable)**, o fijo **USD 150–400/mes**. El modelo de éxito baja la fricción de venta pero complica la cobranza en Argentina.
- **RECURRENCIA: alta.** Cada reserva es una oportunidad nueva; el valor no se agota nunca.
- **VENTAJA DE AI: media.** Segmentar y personalizar el mensaje sí mejora conversión. Pero recordá el dato: solo **16% responde mensajes del hotel**. La AI no arregla eso.
- **MVP: 2–3 semanas.** Semi-manual: el hotel te pasa el listado de llegadas cada mañana, tu equipo dispara la secuencia y avisa por WhatsApp lo vendido. Funciona hasta ~10 hoteles.
- **RIESGO PRINCIPAL:** el enmascaramiento de emails de las OTAs (22% verificado) más la ausencia de teléfono válido te deja sin canal de contacto en buena parte de las reservas.

---

## 5. FÁBRICA DE RESEÑAS *(no es un chatbot)*
No es "responder todas las reseñas con AI". Es lo contrario, y ahí está la diferenciación: **generar volumen** de reseñas nuevas con pedidos bien temporizados, y responder **selectivamente** solo negativas y neutras, con borradores en la voz del hotel en cuatro idiomas.

- **DOLOR:** puntaje estancado y pocas reseñas nuevas. Verificado: el volumen de reseñas se multiplicó ×2,6 y el ranking mejoró de 46,8 a 42,0 con estímulo activo; y **responder al 85%+ rinde peor que no responder**. Supuesto: +0,3 puntos de rating → +2% de conversión sobre 780 noches → **USD 860/mes** de ingreso incremental.
- **COMPRADOR:** **dueño**; en hoteles con gerente, el gerente general.
- **RESULTADO:** reseñas nuevas por mes y puntaje. Se ve el volumen a 30 días, el puntaje a 90.
- **IMPLEMENTACIÓN: 4/5.** Sin PMS obligatorio (lista de check-outs por export). APIs de reseñas limitadas — parte es scraping.
- **DISPOSICIÓN A PAGAR: USD 80–150/mes (ARS 122.000–230.000).** Techo bajo: el mercado ya percibe "responder reseñas con AI" como commodity gratis.
- **RECURRENCIA: alta.** Las reseñas nunca paran.
- **VENTAJA DE AI: media.** Redactar en cuatro idiomas con tono consistente sí es AI real y ahorra tiempo. Pero **hay diez herramientas que hacen esto y algunos PMS lo regalan**. Tu único diferencial defendible es la tesis contraria del estudio de Cornell — y eso es posicionamiento, no tecnología.
- **MVP: 1–2 semanas.** Totalmente humano-detrás al inicio.
- **RIESGO PRINCIPAL:** commoditización inmediata. Es la categoría más saturada.

---

## 6. RECEPCIÓN 24/7 QUE COTIZA *(sí, es un chatbot — pero con precio real)*
Responde consultas de WhatsApp, mail y formulario en menos de 2 minutos, 24/7, en español/inglés/portugués, y **devuelve disponibilidad y tarifa reales con link de pago**, no un "te contactamos a la brevedad".

- **DOLOR:** consultas que se responden a las 9 de la mañana siguiente, cuando el huésped ya reservó en Booking. Verificado: OTAs convierten 12–15% vs 2,2–3,9% del sitio propio; la automatización resuelve 31% de los mensajes en 1,8 s vs 3 minutos. Supuesto: 120 consultas/mes, 25% hoy sin respuesta útil, recuperar un tercio a 20% de conversión = 2 reservas de 3 noches = **USD 330/mes** de ingreso directo + USD 59 de comisión ahorrada. Modesto — y por eso hay que decirlo.
- **COMPRADOR:** **dueño**; jefe de recepción como usuario y potencial saboteador.
- **RESULTADO:** tiempo de primera respuesta y consultas convertidas. 30–45 días.
- **IMPLEMENTACIÓN: 2/5.** **La cotización real exige disponibilidad y tarifa en vivo = integración con PMS o channel manager. Sin eso es un FAQ y no vale nada.** Es la barrera más grande del set.
- **DISPOSICIÓN A PAGAR: USD 150–300/mes (ARS 230.000–460.000)** + costo variable de WhatsApp (marginal: USD 0,0618 por marketing, utility gratis dentro de ventana).
- **RECURRENCIA: alta** si convierte; **cero** si el hotel percibe que responde mal.
- **VENTAJA DE AI: alta en lo técnico, nula en lo comercial.** Es genuinamente AI, pero **el mercado está saturado y el hotelero ya vio cinco demos iguales**. Vender esto sin marca en el sector es la pelea más dura.
- **MVP: 3–4 semanas** (menos si arrancás con un humano contestando desde el panel y AI sugiriendo).
- **RIESGO PRINCIPAL:** que alucine una tarifa o una disponibilidad. Una vez que un huésped llega con un precio inventado, perdiste la cuenta.

---

## 7. HOTEL VISIBLE EN IA — GEO hotelero *(no es un chatbot)*
Auditoría y corrección continua de cómo aparece el hotel en ChatGPT, Gemini, Perplexity y AI Overviews: datos estructurados, consistencia de NAP, contenido citable, monitoreo mensual de menciones vs. competidores del barrio.

- **DOLOR:** verificado — la planificación de viajes vía buscadores tradicionales cayó de **51% a 36% en un año** y el uso de IA generativa más que se duplicó. Si la IA recomienda "hoteles en Palermo" y no te nombra, sos invisible en el canal que crece. Supuesto (agresivo, marcarlo): 3% del tráfico directo llega hoy vía IA y crece; recuperar 8 noches/mes = **USD 440/mes**.
- **COMPRADOR:** **dueño**, o quien maneje el marketing si existe. Se vende con miedo, y el miedo vende bien en 2026.
- **RESULTADO:** frecuencia de mención y posición en respuestas de IA para 20 consultas objetivo. 60–90 días.
- **IMPLEMENTACIÓN: 4/5.** **Cero PMS.** El trabajo es de contenido y datos estructurados.
- **DISPOSICIÓN A PAGAR:** setup USD 400–800 + retainer **USD 100–180/mes (ARS 153.000–275.000)**.
- **RECURRENCIA: media.** Riesgo claro de que se perciba como proyecto único. Se sostiene con el monitoreo comparativo mensual.
- **VENTAJA DE AI: media, pero honesta al revés:** la AI no es tu producto, es tu **medio**. Usás modelos para medir y generar contenido. Es consultoría productizada.
- **MVP: 1–2 semanas.** Es la oferta más fácil de arrancar 100% a mano.
- **RIESGO PRINCIPAL:** métrica de resultado difícil de auditar. El hotelero no puede verificar si mejoraste, y eso corta la renovación al mes 4. Además huele a "SEO 2.0", categoría con reputación dañada.

---

## 8. PARTE DIARIO UNIFICADO — cierre de turno inteligente
Consolida PMS, channel manager, POS del bar, caja, Mercado Pago y tarjetas en un **parte diario** con ingresos, ocupación, pickup, diferencias de caja y anomalías explicadas en lenguaje natural, que hoy la administración arma a mano en Excel.

- **DOLOR:** verificado — 67% de los independientes cita sistemas desconectados y pierde **1–2 jornadas semanales** conciliando. Supuesto: 24 h/mes de un administrativo a USD 6/h cargado = **USD 144/mes de costo directo**, más el costo invisible de decidir con datos de tres días atrás. Además: diferencias de caja que hoy nadie detecta, supuesto 0,4% del ingreso = **USD 173/mes**.
- **COMPRADOR:** **dueño** (es literalmente el reporte que lee cada mañana). Usuario: administración/recepción.
- **RESULTADO:** parte listo a las 8 AM sin intervención humana; diferencias de caja detectadas. 30 días.
- **IMPLEMENTACIÓN: 2/5.** Requiere tocar **varias** fuentes, no una. Mitigación: arrancar con exports diarios por email/carpeta compartida, sin API.
- **DISPOSICIÓN A PAGAR: USD 100–180/mes (ARS 153.000–275.000).** Se ancla en horas ahorradas, y ahorrar horas siempre paga menos que generar ingreso.
- **RECURRENCIA: muy alta.** Una vez que el dueño lee ese mail todas las mañanas, sacarlo duele. **Es la oferta más pegajosa del set.**
- **VENTAJA DE AI: baja en el core, alta en el borde.** Consolidar es ETL puro. La AI aporta en detectar anomalías y explicarlas ("el pickup de este martes está 40% abajo del martes típico"). **Sin ese borde, es un Power BI.**
- **MVP: 2–3 semanas.** Semi-manual perfecto: tu equipo arma el parte a mano los primeros 30 días mientras aprendés el formato real de cada hotel.
- **RIESGO PRINCIPAL:** cada hotel tiene un stack distinto; el costo marginal del cliente 2 no baja. Muere por falta de escala, no por falta de demanda.

---

## 9. TABLA COMPARATIVA (1–5)

| # | Oferta | Dolor | Frec. | Fácil encontrar clientes | Capac. de pago | Velocidad MVP | Diferenciación | Recurrencia | **Total** |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Fisco Huésped (Factura T) | **5** | 4 | 3 | **5** | 4 | **5** | **5** | **31** |
| 2 | Termómetro de Tarifas | 4 | **5** | 3 | 4 | 4 | 4 | **5** | **29** |
| 3 | Radar de Paridad | 3 | 4 | 4 | 3 | **5** | 2 | 3 | **24** |
| 4 | Conserje de Upsell | 3 | **5** | 4 | 4 | 3 | 3 | **5** | **27** |
| 5 | Fábrica de Reseñas | 3 | 4 | **5** | 2 | **5** | 1 | 4 | **24** |
| 6 | Recepción 24/7 | 4 | **5** | 4 | 4 | 2 | 1 | 4 | **24** |
| 7 | Hotel Visible en IA (GEO) | 3 | 3 | 4 | 3 | **5** | 4 | 2 | **24** |
| 8 | Parte Diario Unificado | 4 | **5** | 3 | 3 | 4 | 3 | **5** | **27** |

---

## 10. LAS 3 QUE DESCARTARÍA Y POR QUÉ

**a) Fábrica de Reseñas (#5).** Commodity absoluta. Diferenciación 1/5, capacidad de pago 2/5. Hay diez herramientas y varios PMS lo regalan. Y lo peor: el propio estudio de Cornell dice que **responder mucho destruye ingreso**, así que la promesa intuitiva que el hotelero quiere comprar es falsa. Vender la verdad ("respondé menos") es un argumento hermoso para un blog y horrible para un contrato.

**b) Recepción 24/7 (#6).** Es el chatbot de hotel. Diferenciación 1/5 y el MVP más lento (2/5) porque **sin integración a PMS/channel manager no cotiza, y si no cotiza no vale nada**. Un equipo sin marca en el sector entrando por la puerta más competida, con la barrera técnica más alta y con riesgo de alucinación que quema la cuenta al primer error. Es la trampa clásica.

**c) Radar de Paridad (#3).** Se salva por velocidad (1–2 semanas) y por ser una demo espectacular, pero el valor se agota: arreglás las cinco fugas grandes el primer mes y el cliente cancela el cuarto. Capacidad de pago 3/5 porque se percibe como informe. Además, jurídica y técnicamente dependés del scraping de las OTAs, que puede cortarse cualquier martes. **Mi lectura: no es un producto, es una feature de otro producto o un gancho de venta gratuito.**

---

## 11. SUPUESTOS QUE HAY QUE VALIDAR ANTES DE CONSTRUIR CUALQUIERA

**Económicos**
1. ADR real de ARS 85.000/habitación y ocupación 65% para hoteles independientes de 30–60 habitaciones en CABA. Verificar contra IDECBA por categoría.
2. Que el hotel de 40 habitaciones gaste hoy USD 870–1.730/mes en software. **Es el supuesto más frágil de todo el documento.** Puede ser la mitad.
3. Que la comisión efectiva sea 18%. Podría ser 15% (contrato base) o 22–25% (con programas de visibilidad).
4. Que el 63,4% de share OTA de independientes globales aplique a CABA. Con el peso de Despegar y el mercado regional, podría ser mayor.

**De comprador**
5. **Que el dueño firme.** En 40 habitaciones el dueño es también el que decide, pero también es el que está tapado. Hay que medir cuántas reuniones hacen falta para cerrar y si el ciclo cabe en 30 días.
6. Que el contador externo sea aliado y no bloqueante en la oferta #1. Se valida con cinco llamadas a estudios contables de turismo, no con hoteles.
7. Que el hotelero porteño pague en USD o acepte precio indexado. Cobrar en ARS a precio fijo te licúa en seis meses.

**Técnicos**
8. **Qué PMS usan realmente los independientes de CABA y si tienen API abierta.** Esto define la mitad del ranking. Si el 60% usa un PMS local sin API, las ofertas 4, 6 y 8 pierden dos puntos cada una.
9. Que los exports diarios (CSV/Excel/mail) sean confiables como puente en el MVP semi-manual.
10. Que WhatsApp Business API sea aprobable rápido para cuentas nuevas en Argentina y que el hotel acepte ceder o migrar su número.

**Normativos (crítico para #1)**
11. Qué exige exactamente ARCA hoy como respaldo probatorio para la Factura T, y si la RG 5866/2026 cambia el circuito para hoteles. **Verificar con un contador especialista antes de prometer nada.** No confundir el régimen minorista (RG 5843) con el hotelero.
12. Qué responsabilidad asumís vos si emitís mal. Definir el límite contractual antes de la primera venta.

**De valor**
13. Que el upsell de €12/habitación/mes sea alcanzable en un 3★ porteño con huéspedes sensibles al precio. Puede ser un tercio de eso.
14. Que exista tráfico real de descubrimiento vía IA hacia hoteles de CABA. Sin esto, la oferta #7 no tiene piso.
