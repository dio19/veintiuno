# Estrategia de adquisición: primeros 5 clientes pagos — micro-SaaS con AI para hoteles independientes de CABA

**Fecha:** septiembre 2026. **Autor del plan:** Customer Acquisition Strategist.
**Supuesto de partida:** vendedor técnico argentino, sin marca en hotelería, sin presupuesto de ads, producto todavía sin definir (mensajería/reservas, revenue, reseñas, back-office o venta directa vs OTA).

> Nota de método: todo lo marcado **SIN VERIFICAR** no lo pude confirmar contra fuente primaria. Los conteos por categoría del padrón del ENTUR salen de una lectura automática del PDF y hay que recontarlos a mano antes de usarlos en un pitch.

---

## 1. Definición de ICP

### Segmento A — Boutique 15-40 habitaciones (Palermo, Recoleta, San Telmo, Retiro)
- **Tamaño estimado en CABA:** ~40 establecimientos figuran como "Boutique" en el padrón del ENTUR (julio 2026), más una fracción de los ~50 de 3 estrellas y de los "prestadores registrados" que operan de facto como boutique. **Universo realista: 60-90.** (Conteo aproximado, SIN VERIFICAR uno por uno.)
- **Quién decide:** el dueño, casi siempre. Muchas veces es también quien contesta el Instagram. Ciclo de decisión: 1-3 semanas.
- **Presupuesto de software:** USD 50-200/mes por herramienta. Ya pagan PMS/channel manager (Pxsol, Cloudbeds) y suelen tener agencia de marketing o consultora de revenue.
- **Digitalización:** media-alta. Motor de reservas propio, Instagram activo, obsesión con la reputación en Google/TripAdvisor.
- **Accesibilidad del decisor:** **alta**. DM de Instagram, WhatsApp del hotel, o el dueño en LinkedIn. Es el segmento donde un desconocido puede llegar al que firma en 48 horas.

### Segmento B — 3-4 estrellas tradicional, 50-150 habitaciones (Microcentro, San Nicolás, Monserrat, Congreso)
- **Tamaño:** ~110 establecimientos entre 3 y 4 estrellas en el padrón; descontando cadenas internacionales, **universo direccionable: 70-90 independientes.**
- **Quién decide:** gerente general o gerente comercial; el dueño (a veces una familia o una sociedad) firma. Compra por comité informal: GG + administración + recepción. Ciclo: 4-10 semanas.
- **Presupuesto:** USD 150-600/mes, pero con proceso de compra, factura A y exigencia de "papeles".
- **Digitalización:** baja-media. PMS viejo, Excel para tarifas, mail y teléfono como canal principal. **Acá está el dolor más grande y la menor competencia.**
- **Accesibilidad:** media-baja por canal digital, **muy alta en persona**: están todos a 15 cuadras entre sí y tienen recepción abierta 24/7.

### Segmento C — Apart-hotel o mini-cadena de 2-4 propiedades
- **Tamaño:** ~20 apart-hoteles registrados 1-3 estrellas, más mini-cadenas locales. **Universo: 25-40.**
- **Quién decide:** un gerente de operaciones que mira las N propiedades. Es el comprador más sofisticado y el que más valor saca de automatización, porque cualquier ahorro se multiplica por 2-4.
- **Presupuesto:** USD 200-800/mes.
- **Digitalización:** media, pero con procesos ya escritos.
- **Accesibilidad:** baja. Son pocos y difíciles de encontrar; no hay lista pública de mini-cadenas.

### ICP elegido: **Segmento A (boutique 15-40 hab.), con Segmento B como cantera secundaria de visitas presenciales.**

**Por qué:**
1. **Ciclo de venta de una sola persona.** Con 5 clientes a mano, lo único que importa es la velocidad al "sí". El dueño-operador decide solo.
2. **Ya compran software.** No hay que educar sobre "pagar una suscripción mensual"; hay que ganarle a una alternativa.
3. **El decisor es alcanzable sin intermediarios.** Instagram + WhatsApp + puerta. No hay recepcionista que filtre al dueño que está sentado en el lobby.
4. **Cualquiera de las cinco hipótesis de producto le sirve.** Un boutique de 25 habitaciones tiene el mismo problema de mensajería, de reseñas, de tarifas y de venta directa que uno de 120, pero sin equipo para resolverlo.
5. **Referencia social densa.** Los dueños de boutique porteños se conocen entre sí; 2 clientes felices en Palermo generan las 3 presentaciones siguientes.

**Contra-argumento honesto:** el ticket es más chico. Los primeros 5 clientes no son un negocio, son evidencia; el ticket se sube en la ronda 6-20 con el Segmento B, ya con casos.

---

## 2. Dónde encontrarlos — listas verificables

**Fuente madre 1 — Dataset abierto del GCBA "Alojamientos Turísticos"** (existe y está vivo).
- Portal: https://data.buenosaires.gob.ar/dataset/alojamientos-turisticos
- Descarga CSV directa: https://data.buenosaires.gob.ar/dataset/alojamientos-turisticos/resource/juqdkmgo-51-resource/download
- **Campos:** `id, nombre, domicilio, telefono, email, web, tipo, calle, altura, direccion, Long, Lat, geometry`. Hay versión SHP.
- **Última actualización verificada: 1 de septiembre de 2026.** Trae teléfono y mail. Es literalmente una lista de prospectos con coordenadas.

**Fuente madre 2 — Padrón oficial del Ente de Turismo (ENTUR), PDF**
- https://turismo.buenosaires.gob.ar/es/article/alojamientos-tur%C3%ADsticos → "Descargá el listado completo acá"
- PDF: https://turismo.buenosaires.gob.ar/sites/turismo/files/Alojamientos-Registrados-ENTUR.pdf
- **Versión julio 2026, ~450+ establecimientos**, con nombre, domicilio, barrio, teléfono y mail, agrupados por categoría (5*, 4*, 3*, 2*, 1*, Boutique, Apart 1-3*, Hostel A/B, prestadores registrados). Es la fuente para segmentar por categoría, que el CSV no da tan limpio.

**Asociaciones (padrones parciales, gratis):**
- **AHT / AHTRA** — https://aht.com.ar/hoteles_asociados.php?fil=2 lista **~100 hoteles socios en CABA** con link a ficha individual. Sesga a 4-5 estrellas y cadenas. Contacto de la entidad: Piedras 383 1°, info@ahtra.com.ar, WhatsApp +54 9 11 5582-8619.
- **AHRCC** — https://ahrcc.org.ar — Tucumán 1610, tel. 4372-7275, info@ahrcc.org.ar. Es la **única entidad de FEHGRA en la región CABA** (https://fehgra.org.ar/entidades-region-caba). No publica padrón de socios, **pero sí publica un "Listado de Proveedores"** — puerta de entrada para figurar como proveedor del sector. Tiene instituto de capacitación (ISEHG). Presidente: **Camilo Suárez**.
- **CATbaires** (Cámara de Turismo de la Ciudad de Buenos Aires) — entidad paraguas, útil para eventos.

**Universo de mercado y señales de calidad:**
- **Google Maps / Places**: buscar por comuna. Da reseñas, rating, sitio web, teléfono y **si el hotel responde o no las reseñas** (señal de dolor directa).
- **Booking.com**: filtrar CABA por tipo "Hotel". Da habitaciones aproximadas, precio y comentarios recientes sin responder. **TripAdvisor**: ranking + reseñas viejas sin respuesta.
- **LinkedIn**: buscar por títulos exactos en español — `"Gerente General" hotel`, `"Director de Hotel"`, `"Gerente Comercial" hotel`, `"Jefe de Recepción"`, `"Revenue Manager"` + ubicación "Ciudad Autónoma de Buenos Aires". Filtro adicional: empresa = nombre del hotel sacado del padrón. La búsqueda por empresa es mucho más productiva que por título.
- **Instagram**: los boutique porteños viven ahí. Buscar por geolocalización de Palermo Soho/Hollywood y Recoleta, y por hashtags `#hotelboutiquebuenosaires`, `#palermosoho`. El DM lo lee el dueño o el community manager que le reenvía.

**Estimación de universo direccionable real: 150-220 hoteles independientes en CABA** (excluyendo cadenas internacionales, hostels puros y alojamientos de <10 hab.). De esos, **60-90 son el ICP A**.

**Cómo armar una lista de 200-300 en un día (jornada real, 8 h):**
1. (30 min) Bajar el CSV del portal abierto y el PDF del ENTUR. Parsear el PDF a tabla.
2. (60 min) Merge por nombre normalizado + dirección. Quedan ~450 filas con tipo, tel, mail, lat/long.
3. (60 min) Filtrar: sacar cadenas internacionales, hostels clase B, alojamientos fuera de las comunas 1, 2, 14 y 3.
4. (120 min) Enriquecer con Google Places API: place_id, rating, cantidad de reseñas, sitio web, **fecha de la última reseña respondida**.
5. (90 min) Enriquecer con Booking: cantidad de habitaciones, precio mediano, puntaje.
6. (60 min) Scoring: priorizar los que tienen 100+ reseñas, rating entre 3,8 y 4,5, y **cero respuestas del hotel**. Esos son los que tienen problema y volumen.
7. (60 min) Buscar el dueño/GG en LinkedIn e Instagram solo para el top 60.

---

## 3. Eventos y puntos de concentración

**Verificados:**
- **HOTELGA 2026** — 2 al 4 de septiembre de 2026, La Rural (pabellones verde y amarillo), Av. Sarmiento 2704. Más de **200 empresas expositoras**. Organizada por **FEHGRA, AHT y AHRCC**. Entrada gratuita con acreditación previa, restringida a profesionales del sector. **Ya pasó** (fue la semana anterior a esta planificación). Fecha 2027: **SIN VERIFICAR**, históricamente ronda agosto-septiembre.
- **FIT América Latina 2026 (30ª edición)** — **26 al 29 de septiembre de 2026**, La Rural. Sábado y domingo público general 14-21 h; **lunes 28 y martes 29, profesionales, 10-19 h**. Proyectan +150.000 visitantes. https://fit.org.ar — **Este es el evento accionable de este mes.**
- **Expo Eventos** — **SIN VERIFICAR** fecha 2026/2027.
- **Congreso/encuentro anual de AHT** — calendario en https://aht.com.ar/calendario.php — **fecha 2026-2027 SIN VERIFICAR**.
- **Cursos y eventos de AHRCC** — https://ahrcc.org.ar/eventos/ — agenda propia y capacitaciones del ISEHG. Mucho más barato de infiltrar que una feria.

**Medios que leen (verificados como activos):**
- Hosteltur Latam — https://www.hosteltur.com/lat
- Ladevi Argentina — https://argentina.ladevi.info
- Mensajero Turístico — https://mensajero.com.ar
- Reportur, Diario del Hotelero (https://www.diariodelhotelero.com), Boardingpax, Turismo530, Ciudadanos Viajeros.

**Podcast en español:** "Experto en Hoteles" — https://podcasts.apple.com/ar/podcast/experto-en-hoteles/id1523058739 (entrevistas a líderes de hotelería en español). Detalles de formato **SIN VERIFICAR**.

**Digital:** no hay un grupo de WhatsApp público del sector; se entra por AHRCC o por un proveedor. En LinkedIn, seguir y comentar a AHT, AHRCC, FEHGRA, Pxsol y las consultoras de revenue rinde más que cualquier grupo.

---

## 4. Estrategia de adquisición sin publicidad — 5 tácticas rankeadas

| # | Táctica | Costo | Esfuerzo | Prob. de cerrar 1er cliente | Veredicto |
|---|---------|-------|----------|------------------------------|-----------|
| 1 | **Auditoría automática gratuita** ("regalo primero") | ~USD 0 + API | Alto una vez, cero después | **Alta** | Motor central |
| 2 | **Puerta a puerta en Microcentro/Palermo** | Zapatos | Alto recurrente | **Alta** | Acelerador |
| 3 | **Alianzas con proveedores existentes** | 0 | Medio | Media-alta, lenta | Apuesta a 60 días |
| 4 | **Contenido en LinkedIn con datos propios** | 0 | Medio recurrente | Media | Compuesto |
| 5 | **Referidos con incentivo** | Descuento | Bajo | Baja al inicio, alta después | Activar en cliente 3 |

### 4.1 El regalo: "Radiografía digital de tu hotel" (la táctica madre)

Un PDF de 3 páginas, personalizado, generado automáticamente para cada hotel del padrón, que se manda **antes** de pedir nada.

**Cómo se produce a escala:**
1. Base: las 200-300 filas del merge CSV+ENTUR.
2. Un script recorre, por hotel: Google Places (rating, N de reseñas, % respondidas, tiempo medio de respuesta), Booking/TripAdvisor (puntaje, comentarios negativos recientes), el sitio web (¿tiene motor de reservas propio?, ¿tiene WhatsApp?, ¿responde?), Instagram (frecuencia de posteo), y una prueba real: **se manda una consulta de disponibilidad al WhatsApp/mail del hotel y se cronometra la respuesta.**
3. Un LLM redacta 3 secciones: (a) qué dicen tus últimas 30 reseñas negativas, agrupado en 4 temas; (b) cuántas reseñas quedaron sin responder y cuánto vale eso; (c) cuánto tardaste en contestar mi consulta versus el promedio de tu zona.
4. Render a PDF con el nombre y la foto del hotel. Costo marginal: centavos.

**Por qué funciona:** es simultáneamente prueba de competencia técnica, demo del producto y regalo. Y sobre todo, **resuelve el problema de que el producto todavía no está definido**: la auditoría te dice cuál de las cinco hipótesis duele más, hotel por hotel, antes de escribir una línea de producto.

**Regla:** el PDF se manda sin pedir reunión. La reunión se pide en el segundo toque, tres días después.

### 4.2 Puerta a puerta

Microcentro y San Nicolás tienen 70-90 hoteles independientes en un radio caminable, con recepción abierta siempre. Nadie del software B2B hace esto. Formato: entrar, no pedir hablar con el gerente, dejar la carpeta impresa con la auditoría del hotel a nombre del gerente, con el celular escrito a mano. Cadencia real: **12-15 hoteles por mañana**. En Palermo/Recoleta el equivalente es ir al bar del lobby a las 11 h.

### 4.3 Alianzas con quien ya les vende

Objetivos concretos, verificados y operando en Argentina:
- **Consultoras de revenue:** MAD About Hotels (https://madabouthotels.com.ar, fundada en 2014 por Dolo Sylvester y Magui Llavar), Revenue Hotel (https://revenuehotel.com.ar), Salaun Consulting (https://www.salaun.com.ar), RMA Revenue (https://www.rmarevenue.com), The Hotels Co (https://www.thehotelsco.com).
- **PMS/channel manager con base argentina:** Pxsol (https://www.pxsol.com) — integración o co-venta.
- **Estudios contables y agencias de marketing** que ya facturan a hoteles.
- **AHRCC:** figurar en su Listado de Proveedores y ofrecer una charla gratis en el ISEHG.

Oferta al partner: 20% recurrente o co-branding de la auditoría con su logo.

### 4.4 Contenido en LinkedIn

No opiniones: **datos**. Un post por semana con hallazgos agregados y anonimizados de las auditorías: "Analicé 180 hoteles de CABA: el 61% no respondió ninguna reseña en 90 días. Los que sí responden tienen 0,4 puntos más de rating." Ese post lo comparte medio sector y te consigue la primera charla en AHRCC.

### 4.5 Referidos

Recién desde el cliente 3. Oferta: dos meses gratis por cada hotel referido que firme, para ambas partes. Nunca pedir "referidos" en abstracto: pedir dos nombres específicos.

---

## 5. Borradores de contacto listos para usar

### Email en frío (asunto + cuerpo, 108 palabras)

**Asunto:** 43 reseñas sin responder en [Hotel X]

> Hola [Nombre],
>
> Soy Oscar, desarrollo software. Estuve mirando hoteles independientes de [barrio] y armé un análisis del [Hotel X]: tiene 4,2 en Google con 812 reseñas, pero 43 de los últimos 90 días quedaron sin responder, y las tres quejas que más se repiten son el check-in, el wifi y el ruido de la calle.
>
> Te lo adjunto en PDF, son 3 carillas. No te lo cobro ni te estoy vendiendo nada hoy: lo generé automático y quería ver si el diagnóstico te cierra.
>
> Si te sirve, decime y te mando el mismo análisis de los 5 hoteles que te compiten en la zona.
>
> Oscar — [celular]

### LinkedIn (56 palabras)

> [Nombre], vi que manejás [Hotel X]. Soy técnico, no vendedor de hotelería. Armé un análisis automático de la reputación online de 180 hoteles de CABA y el de ustedes me llamó la atención: 4,2 de rating pero casi ninguna reseña respondida. Te paso el PDF sin compromiso, ¿te lo mando por acá o por mail?

### Guion de visita / llamada (45 segundos)

> "Hola, buen día. Mirá, no vengo a venderte nada hoy, te dejo dos minutos y me voy.
> Soy Oscar, soy programador. Estuve analizando los hoteles independientes de la zona y armé un informe de tres carillas del [Hotel X]: qué dicen las reseñas de los últimos tres meses, cuántas quedaron sin contestar, y cuánto tardaron en responderme cuando les escribí por WhatsApp pidiendo disponibilidad — fueron 19 horas, el promedio de la zona es 4.
> Te lo dejo impreso, es tuyo, hagas lo que hagas con esto.
> Lo único que te pido: si algo de lo que dice ahí te resuena, mandame un WhatsApp. Está el celular en la última hoja. Gracias, che."

### WhatsApp

> Hola [Nombre], soy Oscar, el que pasó por la recepción el martes y dejó el informe del [Hotel X]. ¿Llegó a tus manos? Si querés te mando el mismo análisis pero comparado contra los 5 hoteles que te compiten en Palermo — tarda 2 minutos en generarse. Si no te interesa, no te escribo más y quedamos bien igual 🙂

---

## 6. Plan de 30 días hasta los primeros 5 clientes

**Posición sobre el modelo: piloto PAGO, no gratis.** Precio de entrada: **ARS equivalente a USD 90-150/mes, facturado en pesos**, con los primeros 30 días con garantía de devolución total. Gratis no es un cliente: es un favor que no valida nada y que además te condena a soportar sin ingresos. El descuento va en el plazo (precio congelado 12 meses para los 5 fundadores), no en el precio a cero.

| Días | Actividad | Números objetivo |
|------|-----------|------------------|
| 1-2 | Bajar CSV GCBA + PDF ENTUR, merge, limpieza, filtro por comunas 1/2/3/14 | Lista de 250-300 |
| 3-5 | Construir el generador de auditorías (Places API + scraping Booking + LLM + PDF) | Motor funcionando |
| 6-7 | Enriquecer y scorear. Buscar decisor en LinkedIn/Instagram del top 80 | 80 con nombre y apellido |
| 8 | Generar las primeras 80 auditorías. QA manual de 10 | 80 PDFs |
| 9-12 | **Ola 1 de email en frío**, 20/día, con PDF adjunto. Sin pedir reunión | 80 enviados |
| 10-12 | **Puerta a puerta Microcentro**, 3 mañanas, carpeta impresa | 40 visitas |
| 12-14 | Seguimiento WhatsApp/LinkedIn a todo el que abrió o recibió carpeta | 60 toques |
| 13 | Post 1 en LinkedIn con el dato agregado de las 80 auditorías | — |
| 15-17 | Reuniones ola 1. Escuchar cuál de las 5 hipótesis duele. **No demear producto: validar dolor** | 4-6 reuniones |
| 15-16 | Contactar 6 partners (MAD, Revenue Hotel, Salaun, RMA, Pxsol, AHRCC proveedores) | 6 mails + 2 llamadas |
| 18-21 | **Ola 2**: 100 auditorías nuevas, boutique Palermo/Recoleta, entrada por Instagram DM | 100 enviados |
| 19-21 | Puerta a puerta Palermo/Recoleta, 3 mañanas | 35 visitas |
| 20 | Post 2 en LinkedIn: caso concreto anonimizado | — |
| 22-24 | Reuniones ola 2 + **primeras 2 propuestas de piloto pago** | 6-8 reuniones, 2 propuestas |
| 25-27 | Cierre 1-2. Onboarding manual, concierge, sin producto terminado | **2 clientes** |
| 26-28 | Ola 3 sobre no-respondedores: reenvío con dato nuevo ("actualicé tu informe") | 120 toques |
| 28-30 | Reuniones ola 3, cierre 3-5. Pedir 2 referidos a cada cliente firmado | **3-5 clientes** |

**Aritmética esperable.** 180 mails en frío bien personalizados con regalo adjunto: reply rate razonable **8-15%** (muy por encima del 3,43% promedio de cold email en 2026, justamente porque el adjunto es específico y verificable) → 15-27 respuestas. Puerta a puerta: 75 visitas, **20-25% de conversación real** con el decisor → 15-18 conversaciones. Total ~35 conversaciones → **12-16 reuniones** → **4-6 propuestas** → **3-5 cierres**. Es ajustado pero alcanzable si el motor de auditorías funciona el día 8.

**Señales de que hay que pivotear:**
- Menos de 5% de respuesta al email **con** auditoría adjunta → el gancho no es creíble o el dolor elegido no duele.
- Reuniones que terminan en "muy interesante, mandame material" sin fecha → estás vendiendo curiosidad, no dolor.
- Nadie menciona espontáneamente el mismo problema en 8 reuniones → ninguna de las 5 hipótesis está madura; volvé a escuchar.
- Aceptan gratis pero no pagan USD 90 → no es un problema de precio, es que no es un problema.
- **Señal positiva de foco:** si 6 de 10 reuniones derivan solas hacia el mismo tema, ese es el producto.

---

## 7. Obstáculos reales

**Por qué no te contestan.** El hotelero porteño está saturado de proveedores. Recibe mails de channel managers, motores de reserva y agencias todas las semanas. Además, la economía lo tiene en modo supervivencia: la ocupación en CABA rondaba el **65% en julio de 2026** (2-3 estrellas: 45-50%), y desde AHRCC describían un sector que "sobrevive endeudándose, posterga inversiones y recorta costos donde puede" (Gabriela Akrabian, ámbito.com, 29/7/2026 — cargo exacto **SIN VERIFICAR**). En ese contexto, cualquier cosa que suene a "nuevo gasto mensual" muere en el asunto del mail. Por eso el regalo primero no es un truco de marketing: es la única forma de entrar sin pedir plata.

**El guardián.** En el Segmento B es la recepción y, sobre todo, **administración**. La recepción no te va a pasar con el gerente por teléfono nunca. El atajo es presencial: el gerente general de un hotel de Microcentro está físicamente en el hotel entre las 10 y las 13. En el Segmento A el guardián es el community manager que maneja el Instagram; se lo saltea preguntando directamente "¿me pasás el mail del dueño? tengo un informe para él, no le vendo nada".

**Estacionalidad de la atención — cuándo NO llamar.**
- **Enero y febrero:** verano, temporada baja en CABA para el hotelero porteño en volumen local pero alta en internacionales; y sobre todo, medio equipo de vacaciones. No arranques nada.
- **Semana Santa, fines de semana largos y las semanas de FIT/Hotelga:** cero atención.
- **Últimos 3 días y primeros 5 de cada mes:** cierre contable y liquidación de sueldos. Administración no te atiende.
- **Mejor ventana:** martes a jueves, 10:00-12:30 y 15:00-17:00. Marzo-junio y agosto-noviembre son los mejores meses.
- Dato operativo relevante: Camilo Suárez (presidente de AHRCC) señalaba que muchas reservas llegan **tres días antes** del arribo. Traducción: el hotelero vive apagando incendios de corto plazo, y cualquier propuesta que prometa valor "en 6 meses" pierde contra la que promete valor esta semana.

**Vender en dólares a quien factura en pesos.** Es el obstáculo más subestimado. Un boutique cobra en pesos (ADR de 3 estrellas ~ARS 55.000 por persona en julio 2026) y una suscripción en USD pagada con tarjeta al exterior arrastra IVA 21% + percepción de Ganancias 30% + percepción de IVA 8%, lo que puede llevar el costo efectivo a **~+59% sobre el precio de lista** (el Impuesto PAIS dejó de aplicarse en 2026). Además, no todos pueden computar esas percepciones.

**Qué hacer:** facturar en pesos desde una entidad argentina, con factura A, débito automático o transferencia, y **precio indexado trimestralmente** (no mensualmente: la revisión mensual del precio es lo que más ruido genera). Aceptar transferencia bancaria además de tarjeta. Eso solo te pone por delante de todo competidor extranjero que cobra en USD con tarjeta, y es un argumento de venta explícito, no un detalle administrativo.

**Último obstáculo, el propio.** Sin marca en hotelería, la objeción real es "¿y vos qué sabés de hoteles?". No se responde con credenciales que no tenés: se responde con la auditoría, que demuestra que estudiaste ese hotel más que el proveedor que manda un PDF genérico. Esa es toda la credibilidad que necesitás para los primeros cinco.

---

## Fuentes

- Dataset Alojamientos Turísticos, GCBA — https://data.buenosaires.gob.ar/dataset/alojamientos-turisticos (CSV: .../resource/juqdkmgo-51-resource/download; actualizado 1/9/2026)
- Datasets del Ente de Turismo — https://data.buenosaires.gob.ar/dataset?organization=ente-de-turismo
- Registro de Alojamientos Turísticos, ENTUR — https://turismo.buenosaires.gob.ar/es/article/alojamientos-tur%C3%ADsticos | PDF: https://turismo.buenosaires.gob.ar/sites/turismo/files/Alojamientos-Registrados-ENTUR.pdf (julio 2026)
- INDEC, Encuesta de Ocupación Hotelera, noviembre 2025 — https://www.indec.gob.ar/uploads/informesdeprensa/eoh_01_265BAAB03CBF.pdf
- Instituto de Estadística y Censos CABA, tarifa promedio por categoría — https://www.estadisticaciudad.gob.ar/eyc/banco-datos/tarifa-promedio-por-categoria-hotelera-ciudad-de-buenos-aires-enero-2008-mayo-2024-pesos/
- ámbito, "Hoteles en alerta: la ocupación ronda el 65%", 29/7/2026 — https://www.ambito.com/negocios/hoteles-alerta-la-ocupacion-ronda-el-65-que-estrategias-trazan-sobrevivir-n6304861
- AHT/AHTRA, hoteles asociados — https://aht.com.ar/hoteles_asociados.php?fil=2 | https://www.ahtra.com.ar/
- AHRCC — https://ahrcc.org.ar/ | eventos: https://ahrcc.org.ar/eventos/
- FEHGRA, entidades región CABA — https://fehgra.org.ar/entidades-region-caba
- FEHGRA, "Camilo Suárez, nuevo presidente de la AHRCC" — https://fehgra.org.ar/archivos/40434
- Hotelga 2026 — https://www.timeout.com/es/buenos-aires/hotelga-feria-hoteleria-gastronomia-la-rural | https://mensajero.com.ar/alojamiento-y-gastronomia/hotelga-2026--la-guia-clave-del-evento-que-acelera-el-turismo-argentino_a6a95af6a77f15703565660c6 | https://fehgra.org.ar/archivos/40991
- FIT América Latina 2026 — https://fit.org.ar/fit-2026-fue-declarada-de-interes-turistico/
- Instantly, Cold Email Benchmark Report 2026 — https://instantly.ai/cold-email-benchmark-report-2026
- Cloudbeds, comisiones de OTAs 2026 — https://www.cloudbeds.com/online-travel-agencies/commissions/
- Impuestos a compras en el exterior, Argentina 2026 — https://www.calcusite.com.ar/articulos/impuestos-compras-exterior-argentina | https://economis.com.ar/desde-2026-pagar-con-tarjeta-en-dolares-cuesta-menos-tras-el-fin-del-impuesto-pais/
- Consultoras: https://madabouthotels.com.ar/quienes-somos/ | https://revenuehotel.com.ar/ | https://www.salaun.com.ar/ | https://www.rmarevenue.com/ | https://www.thehotelsco.com/
- Pxsol (PMS argentino) — https://www.pxsol.com/es-ar/producto/pms-para-hoteles
- Medios: https://www.hosteltur.com/lat | https://argentina.ladevi.info/ | https://mensajero.com.ar | https://www.diariodelhotelero.com/argentina.html
- Podcast "Experto en Hoteles" — https://podcasts.apple.com/ar/podcast/experto-en-hoteles/id1523058739
