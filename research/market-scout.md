# Market Scout — Hotelería CABA para micro-SaaS con AI
**Fecha:** septiembre 2026 · **Autor:** Market Scout
**Convención:** `[DATO]` = fuente primaria/verificable · `[EST]` = estimación propia derivada de datos citados · `[SUP]` = supuesto sin verificar · `NO VERIFICADO` = no encontré fuente y no lo invento.

---

## 0. Resumen ejecutivo

CABA tiene **440 hoteles y ~55.000 plazas** `[DATO]`, con un parque mayoritariamente de tamaño medio (~62 habitaciones promedio `[EST]`) y un receptivo en fuerte recuperación (**+19% i.a.**) pero con márgenes aplastados por costo en dólares, presión impositiva y dependencia de OTAs. El hallazgo más explotable no es la falta de software de gestión —hay PMS de sobra— sino tres huecos concretos: **(a) el apagón estadístico del INDEC dejó al sector sin benchmark desde diciembre 2025**, **(b) la ventana de reserva colapsó a ~3 días, lo que rompe el revenue management manual**, y **(c) la operatoria de Factura T / exención de IVA a extranjeros es manual y afecta al 48,5% de los huéspedes de CABA**.

---

## 1. Tamaño y estructura del mercado

| Métrica | Valor | Fuente |
|---|---|---|
| Hoteles en CABA | **440** | Ente de Turismo CABA, sept. 2026 `[DATO]` |
| Hoteles 4 y 5 estrellas | **117** (26,6%) | ídem `[DATO]` |
| Resto (1-3★, boutique, apart, hostel) | **323** (73,4%) | `[EST]` por diferencia |
| Plazas disponibles diarias | **~55.000** | ídem `[DATO]` |
| Plazas promedio por hotel | ~125 → **~62 habitaciones** | `[EST]` (a 2 plazas/hab.) |
| Empleo turístico CABA | 85.000 puestos | ídem `[DATO]` |
| Impacto económico anual | **USD 970 millones** | ídem `[DATO]` |

**Lectura para el producto:** el promedio de ~62 habitaciones cae justo en el centro del segmento objetivo (20-120 hab.). El grueso numérico del parque —323 establecimientos de categoría media/baja— es exactamente donde no hay equipo de revenue management ni IT propio.

- **Independientes vs. cadena:** `NO VERIFICADO` para CABA. No encontré un censo público que discrimine cadena vs. independiente. `[SUP]` razonable: las cadenas internacionales (Wyndham, Meliá, Hilton, Accor, NH) concentran buena parte de los 117 hoteles 4-5★, mientras el segmento 1-3★/boutique/apart es predominantemente independiente y familiar.
- **Concentración por barrio:** `NO VERIFICADO` con dato oficial. Ninguna fuente pública desagrega plazas por barrio. Se menciona cualitativamente que **Palermo rinde por encima del promedio** de ocupación (FEHGRA, julio 2026) `[DATO cualitativo]`.
- **Parahotelería y alquiler temporario:** ~**20.000 unidades** listadas en plataformas tipo Airbnb en CABA (estudio UTDT, 3er trim. 2023) `[DATO, desactualizado]` = **~36% de las plazas hoteleras formales** en unidades `[EST]`. Es el competidor estructural del hotel chico.
- **Contexto nacional:** la EOH del INDEC releva ~3.000 establecimientos hoteleros y parahoteleros con más de 12 plazas o 4 habitaciones `[DATO]`. CABA aporta el **22,0% de las pernoctaciones del país** y el **51,0% de las pernoctaciones de no residentes** `[DATO, oct. 2025]`.

---

## 2. Salud económica: ocupación, tarifas y macro

### Ocupación (CABA, tasa de ocupación de habitaciones — TOH)

| Período | TOH | TOP (plazas) | Fuente |
|---|---|---|---|
| Junio 2025 | 47,7% | 37,4% | INDEC EOH `[DATO]` |
| Octubre 2025 | 62,4% | 47,4% | INDEC EOH `[DATO]` |
| Noviembre 2025 | 74,7% | 57,8% | INDEC EOH `[DATO]` |
| Julio 2026 | ~65% (general) | — | Ámbito / AHRCC `[DATO]` |

Estacionalidad marcada: **junio-julio es el piso** (invierno, ~48-50% en 2025) y **octubre-noviembre el pico** (temporada de congresos y eventos, hasta 74,7%). En julio 2026 la ocupación se partió por categoría: **2-3★ en 45-50%** vs. **4★ por encima del 60%** `[DATO]`. El hotel chico sufre desproporcionadamente.

> ⚠️ **Apagón estadístico.** El INDEC **dejó de publicar la EOH**; el último dato difundido fue **diciembre 2025**, tras el corte de financiamiento de la Secretaría de Turismo en dic-2025 `[DATO, marzo 2026]`. Esto dejó sin estadística pública a 47 ciudades turísticas. El IDECBA (Ciudad) sí mantiene su serie propia, con datos hasta **mayo 2026** `[DATO]`. **Implicancia directa de producto: el sector se quedó sin benchmark de mercado.**

### Tarifas (ADR)

- INDEC **no publica ADR** en el informe de prensa de la EOH `[DATO verificado]`. Los datasets de "tarifa media diaria en pesos/USD" de datos.yvera.gob.ar **fueron dados de baja** `[DATO]`. **ADR/RevPAR oficial de CABA: NO VERIFICADO.**
- Proxies de prensa (julio 2026): **3★ desde ~$55.000 por persona**, **4★ desde ~$65.000 por persona** `[DATO]`. Marzo 2026: **habitación doble $60.000-$75.000** en hotel boutique `[DATO]`.
- **RevPAR:** `NO VERIFICADO`. `[EST]` con TOH 65% y ADR doble ~$67.500 → RevPAR ≈ **$43.900/hab/noche**. Tomar con pinzas: mezcla base por persona y por habitación.

### Macro y competitividad

| Indicador | 2025 | 2026 (ene-jul o proyectado) | Fuente |
|---|---|---|---|
| Déficit turístico | USD 7.200 M | **USD 5.700-6.200 M** (proyectado) | IERAL `[DATO]` |
| Turistas receptivos (país) | 5,68 M (año) | **3,4 M** ene-jul, **+8%** | IERAL / OMT `[DATO]` |
| Argentinos al exterior | — | **7,1 M** ene-jul, **−14%** | IERAL `[DATO]` |
| Ratio salidas/entradas | 2,6 | **2,1** | IERAL `[DATO]` |
| Receptivo internacional CABA | — | **1,61 M** ene-jul, **+19%** | Ente de Turismo `[DATO]` |

**Mercados emisores a CABA (ene-jul 2026):** Brasil 22% (357.000), EE.UU. 14% (219.000), Uruguay 11% (171.000), España 5% (73.000); **China +62% i.a.** `[DATO]`.

**Interpretación:** el receptivo se recupera con fuerza en CABA (+19%, muy por encima del +8% nacional), pero **la apreciación del peso post-cepo destruyó competitividad de precio**: Argentina cayó al 4º mayor descenso porcentual global entre destinos reportantes a la OMT y perdió el liderazgo regional frente a Brasil, Colombia y Chile `[DATO, ago. 2026]`. La rentabilidad no acompaña al volumen: costos de energía **+1.000%** según un operador boutique `[DATO cualitativo]`, y **+300-500%** en servicios, alquileres y seguros según AHT `[DATO]`.

**Cambio de comportamiento clave:** *"La planificación prácticamente desapareció. Hoy muchas reservas ingresan apenas tres días antes"* — Camilo Suárez, AHRCC Buenos Aires `[DATO, julio 2026]`. Estadía media CABA: **2,1-2,2 noches** y cayendo `[DATO]`.

---

## 3. Marco regulatorio y fiscal (CABA)

| Norma / obligación | Contenido | Fuente |
|---|---|---|
| **Ley CABA 4631** | Registro de Alojamientos Turísticos obligatorio, dentro del Registro de Prestadores Turísticos. Autoridad: Ente de Turismo. Trámite por TAD con clave miBA. **Gratuito**. | `[DATO]` |
| **Registro de Alquileres Temporarios (RAT)** | Resolución N°8 (feb. 2025). 180 días para regularizar. Cobro de **1,5% por persona/noche** a turistas extranjeros vía plataforma, destinado a Visit BUE. | `[DATO]` |
| **Ingresos Brutos CABA 2026** | Hoteles: **3,00%** si ingresos ≤ $2.004.000.000 anuales; **4,50%** por encima. | Ley Impositiva 6927 `[DATO]` |
| **IIBB alquiler temporario turístico** | **6,00%** (cód. 681098) | ídem `[DATO]` |
| **Exención de IVA a extranjeros (alojamiento)** | 21% de IVA no se cobra sobre alojamiento **y desayuno incluido** a no residentes que paguen con **tarjeta emitida en el exterior o transferencia desde banco extranjero**. Automático en la facturación; otros servicios se facturan aparte. | Ente de Turismo CABA `[DATO]` |
| **Factura T** | Comprobante electrónico específico que reemplaza A/B para alojamiento y desayuno a turistas extranjeros (estadía ≤ 90 días). Requiere autorización de ARCA/AFIP y régimen de información. | `[DATO]` |
| **RG 5843/2026 (ARCA)** | Digitaliza la validación del reintegro de IVA a turistas. Comprobantes electrónicos, transmisión online, validación digital en puntos de salida. **Aplica a bienes (tax-free shopping), no a alojamiento** — son regímenes distintos. | `[DATO]` |

**Presión fiscal total:** AHT estima **$60 de impuestos cada $100 facturados** en tarifa `[DATO, 2025]`. Un estudio IARAF/FEHGRA ubicó la carga en **39,7% del precio final en Buenos Aires** `[DATO, pero de 2015 — desactualizado]`.

**Asimetría relevante:** el alquiler temporario paga **6% de IIBB** vs. **3-4,5%** del hotel, pero el hotel carga con habilitación, convenio UTHGRA, Factura T y registro. `[EST]` La ventaja competitiva real del temporario es la informalidad y la ausencia de costo laboral, no la alícuota.

---

## 4. Procesos manuales en un hotel de 20-120 habitaciones

Fuentes: AHRCC/FEHGRA (julio 2026), Pxsol (2026), y `[SUP]` donde se indica.

| Proceso | Estado típico | Dolor |
|---|---|---|
| Carga de tarifas multicanal | Channel manager si existe; **planillas de cálculo** en los chicos `[DATO cualitativo]` | Errores, paridad rota, overbooking |
| Revenue management | Manual o inexistente en 1-3★ `[SUP]` | Ventana de 3 días vuelve imposible el pricing manual |
| Consultas WhatsApp / mail / Instagram | Manual, en horario de recepción | Se pierden reservas por no responder a tiempo `[DATO: WeSpeak]` |
| Respuesta a reseñas | Esporádica `[SUP]` | Impacto directo en RevPAR (ver §7) |
| Factura T / IVA extranjeros | Manual, verificación de pasaporte y medio de pago | **48,5% de huéspedes CABA son no residentes** `[DATO]` |
| Conciliación comisiones OTA | Manual, planilla `[SUP]` | Comisiones mal liquidadas no se detectan |
| Reporte EOH al INDEC | Portal eoh.indec.gob.ar, carga mensual | Sistema migrado en 2025; publicación suspendida pero **el operativo de carga sigue** `[SUP — no verificado si la carga continúa siendo exigible]` |
| Housekeeping, grupos, upselling, cobranza | Manual/papel `[SUP]` | — |

---

## 5. Estructura de costos: dónde se quema la plata

**Comisiones OTA** `[DATO, Pxsol 2026 — LatAm, no exclusivo Argentina]`:

| Canal | Comisión |
|---|---|
| Booking.com | **15-20%** |
| Expedia | 15-25% |
| Despegar | 10-18% |
| Airbnb (host) | 3-5% |

**Dependencia:** hay propiedades con **más del 80% de las reservas vía OTA**, perdiendo ~15% de cada reserva `[DATO]`.

**Caso cuantificado** (hotel de 20 habitaciones, ADR USD 80, ocupación 70%) `[DATO, Pxsol]`:
- Ingreso bruto mensual: **USD 33.600**
- Si 80% entra por Booking al 17% promedio → **USD 4.570/mes = USD 54.000/año** a una sola OTA
- **Pasar de 20% a 40% de reserva directa ahorra >USD 27.000/año** sin subir ocupación ni tarifa

`[EST]` Escalado al parque de CABA: si ~300 hoteles independientes promedian USD 40.000/año en comisiones, el pool anual de comisiones OTA del segmento ronda **USD 12 millones**. Cada punto porcentual de shift OTA→directa vale ~**USD 120.000/año** para el conjunto y ~**USD 400/año por hotel** `[EST]`.

**Costo laboral (UTHGRA-FEHGRA, jul-sep 2026)** `[DATO]`:

| Categoría | Hotel 1★ | Hotel 5★ |
|---|---|---|
| Cat. 4 (recepcionista/telefonista) | $1.157.884 | $1.424.619 |
| Cat. 6 (conserje principal/gobernanta) | $1.292.026 | $1.524.806 |

Más **gratificación no remunerativa de $79.000-$104.000/mes** en tres cuotas. Acuerdo firmado 24/07/2026, pendiente de homologación. Los básicos de junio 2026 se mantuvieron sin cambio.

**Peso de la nómina:** los salarios representan **hasta 55% de las ventas** de un hotel `[DATO, Perfil — referido a Córdoba, no CABA]`. AHT reporta caída del 4% del empleo formal anual y pérdida de **10 puestos por día** en el sector `[DATO, 2025]`.

---

## 6. Adopción de tecnología

- **PMS presentes en Argentina:** Cloudbeds, Mews, Oracle Opera, Protel, Sihot (internacionales); **Axis PMS, Aloja, MiniHotel, Avirato, Octopus24, Pxsol** (locales/regionales). Channel managers: SiteMinder, RateGain `[DATO]`.
- **Nivel de digitalización:** `NO VERIFICADO` con estadística. Evidencia cualitativa consistente: disponibilidad en planillas, facturación desconectada del PMS y demoras de respuesta multicanal `[DATO cualitativo, Pxsol 2026]`.
- **Adopción de AI global:** 82% de los hoteles aumentará su uso de AI en 2026; 71% reporta impacto significativo o transformador; 85% destinará ≥5% del presupuesto IT a AI. **Estudio Canary Technologies, 400+ profesionales — cobertura Norteamérica, EMEA y APAC. NO incluye LatAm** `[DATO, con la salvedad explícita]`.
- **Caso argentino concreto: WeSpeak** `[DATO, feb. 2026]` — startup argentina de venta conversacional con AI y pagos por WhatsApp, 70 idiomas, CRM integrado. **500+ hoteles en LatAm y Europa** (Howard Johnson, Wyndham, Holiday Inn, Radisson). **125.000 reservas procesadas en 2025**, facturación **USD 700.000** en 2025, **ticket promedio USD 247/mes por hotel**.

> **Señal competitiva crítica:** el nicho "AI + WhatsApp + reservas directas" **ya tiene un incumbente argentino con tracción y clientes de cadena**. Entrar de frente ahí es pelear cuesta arriba. El ticket de USD 247/mes es, además, un ancla de precio de mercado.

---

## 7. Oportunidades de automatización cuantificadas

| # | Oportunidad | Impacto estimado | Base |
|---|---|---|---|
| 1 | **Shift OTA → directa** | USD 27.000/año en hotel de 20 hab. al pasar 20%→40% directa | `[DATO Pxsol]` |
| 2 | **Gestión de reputación / respuesta a reseñas** | **+1 punto de índice de reseñas = +0,89% ADR, +0,54% ocupación, +1,42% RevPAR** | Cornell/ReviewPro, 31.000+ observaciones, 11 mercados NA+Europa `[DATO — no LatAm]` |
| 3 | **Pricing dinámico para ventana de 3 días** | `NO VERIFICADO` en magnitud. El colapso de la ventana de reserva invalida el pricing manual `[DATO cualitativo AHRCC]` | — |
| 4 | **Benchmark de mercado post-apagón INDEC** | Sin dato público desde dic-2025; demanda insatisfecha estructural | `[DATO]` |
| 5 | **Automatización Factura T / IVA extranjeros** | Alcanza al **48,5%** de los huéspedes de CABA | `[DATO]` |
| 6 | **Respuesta multicanal 24/7** | Reservas perdidas por demora de respuesta | `[DATO cualitativo WeSpeak]` |
| 7 | **Conciliación de comisiones OTA** | `NO VERIFICADO` (no hallé tasa de error de liquidación) | — |

---

## 8. Diez hallazgos accionables

1. **El mercado direccionable en CABA es chico: ~323 hoteles no-4/5★.** A un ticket de referencia de USD 247/mes `[DATO WeSpeak]`, el techo de ARR sólo en CABA es **~USD 960.000/año** `[EST]` capturando el 100%. **CABA sirve como beachhead, no como mercado final.** Diseñar desde el día uno para replicar a Córdoba, Mendoza, Bariloche y LatAm.

2. **El apagón estadístico del INDEC es la oportunidad más limpia y menos disputada.** Desde diciembre 2025 no hay benchmark público de ocupación `[DATO]`. Un producto que agregue datos anónimos de sus propios hoteles y devuelva un índice comparativo de CABA por barrio y categoría crea **efecto de red y dato propietario** que ningún PMS internacional tiene.

3. **No competir de frente con WeSpeak en WhatsApp + reservas.** Ya tiene 500+ hoteles y cadenas `[DATO]`. Buscar el flanco: back-office fiscal, conciliación, benchmark, revenue.

4. **La ventana de reserva de 3 días es el dolor más citado por las cámaras** `[DATO AHRCC]`. Es un problema estructuralmente irresoluble a mano y por lo tanto perfecto para AI: repricing diario automático sobre ocupación, eventos y competencia.

5. **Factura T y la exención de IVA tocan a casi 1 de cada 2 huéspedes en CABA (48,5%)** `[DATO]`. Es un proceso normado, repetitivo, verificable y con riesgo fiscal: candidato ideal a automatización con validación de pasaporte y medio de pago.

6. **La brecha por categoría es la señal de segmentación.** 2-3★ en 45-50% de ocupación vs. 4★ por encima de 60% `[DATO, julio 2026]`. El cliente con más dolor y menos herramientas es el 1-3★ independiente — pero también el de menor capacidad de pago. **Tensión central del negocio: el que más lo necesita es el que menos puede pagarlo.**

7. **El pitch debe ser en pesos y con ROI en comisiones, no en "eficiencia".** Con salarios hasta 55% de ventas `[DATO]` y $60 de impuestos cada $100 `[DATO AHT]`, el único argumento que compra un hotelero endeudado es plata concreta: "esto te devuelve USD X de comisión OTA".

8. **El volumen crece pero el margen no.** Receptivo CABA +19% `[DATO]` con ocupación en ~65% y rentabilidad en caída. **El producto debe vender margen, no ocupación** — la ocupación ya está llegando sola.

9. **Brasil, EE.UU. y Uruguay son el 47% del receptivo de CABA; China crece 62%** `[DATO]`. Multi-idioma no es un lujo: es requisito de entrada, y el chino es el diferencial emergente.

10. **Huecos honestos que hay que cerrar antes de decidir:** ADR/RevPAR oficial de CABA (`NO VERIFICADO` — INDEC no lo publica y los datasets de yvera fueron dados de baja), split cadena/independiente (`NO VERIFICADO`), distribución de plazas por barrio (`NO VERIFICADO`), y si la carga mensual al portal EOH sigue siendo exigible pese a la suspensión de la publicación (`NO VERIFICADO`). **Recomiendo 8-10 entrevistas con hoteleros de Palermo/Recoleta/San Nicolás para cerrarlos antes de escribir una línea de código.**

---

## 9. Fuentes

**Organismos oficiales y estadística**
- INDEC — EOH noviembre 2025: https://www.indec.gob.ar/uploads/informesdeprensa/eoh_01_265BAAB03CBF.pdf
- INDEC — EOH octubre 2025: https://www.indec.gob.ar/uploads/informesdeprensa/eoh_12_25ED486DC3BD.pdf
- INDEC — EOH junio 2025: https://www.indec.gob.ar/uploads/informesdeprensa/eoh_08_2517BC177A31.pdf
- INDEC — portal de carga EOH: https://eoh.indec.gob.ar/
- IDECBA — Oferta hotelera CABA: https://www.estadisticaciudad.gob.ar/eyc/categoria-banco-datos/oferta-hotelera/
- IDECBA — Tasa de ocupación de plazas por categoría (ene-2008 / may-2026): https://www.estadisticaciudad.gob.ar/eyc/banco-datos/tasa-de-ocupacion-de-plazas-por-categoria-hotelera-ciudad-de-buenos-aires-enero-2008-mayo-2025-porcentaje/
- Datos Abiertos Turismo (yvera) — EOH: https://datos.yvera.gob.ar/dataset/encuesta-ocupacion-hotelera-parahotelera-eoh
- Ente de Turismo CABA — Alojamientos turísticos (Ley 4631): https://turismo.buenosaires.gob.ar/es/article/alojamientos-tur%C3%ADsticos
- Ente de Turismo CABA — Exención de IVA a extranjeros: https://turismo.buenosaires.gob.ar/en/article/vat-free-accommodation
- Ente de Turismo CABA — Tablero de ocupación hotelera: https://turismo.buenosaires.gob.ar/es/observatorio/tableros/ocupacion-hotelera
- Ley Impositiva CABA 2026 (Ley 6927), anexo de alícuotas: https://documentosboletinoficial.buenosaires.gob.ar/publico/PL-LEY-LCABA-LCBA-6927-25-ANX.pdf
- Ley CABA 4631 (texto ordenado): http://www2.cedom.gov.ar/es/legislacion/normas/leyes/ley4631.html
- ARCA/AFIP — Régimen de reintegro de IVA a turistas: https://servicioscf.afip.gob.ar/publico/abc/ABCpaso2.aspx?id_nivel1=563&id_nivel2=566&id_nivel3=674&id_nivel4=2411&id_nivel5=2421

**Prensa sectorial y económica**
- Ámbito — "Hoteles en alerta: la ocupación ronda el 65%" (jul. 2026): https://www.ambito.com/negocios/hoteles-alerta-la-ocupacion-ronda-el-65-que-estrategias-trazan-sobrevivir-n6304861
- Infobae — Balanza turística, déficit USD 6.000 M (sept. 2026): https://www.infobae.com/economia/2026/09/03/la-balanza-del-turismo-tendra-un-deficit-cercano-a-usd-6000-millones-en-2026/
- La Nación — "Por qué la Argentina perdió el liderazgo turístico de la región" (ago. 2026): https://www.lanacion.com.ar/revista-lugares/por-que-la-argentina-perdio-el-liderazgo-turistico-de-la-region-nid11082026/
- 0223 — "Apagón estadístico: el INDEC dejó de publicar la EOH" (mar. 2026): https://www.0223.com.ar/nota/2026-3-10-12-39-0-apagon-estadistico-el-indec-dejo-de-publicar-la-encuesta-de-ocupacion-hotelera
- Zona Norte Hoy — Turismo internacional CABA 1,61 M (sept. 2026): https://www.zonanortehoy.com/caba/fuerte-crecimiento-del-turismo-internacional-la-ciudad-recibio-1-61-millones-de-visitantes-internacionales-entre-enero-y-julio/
- Zona Norte Hoy / Hotelga 2026 — 440 hoteles, 55.000 plazas (sept. 2026): https://www.zonanortehoy.com/caba/hotelga-2026-el-turismo-crece-en-la-ciudad-y-hay-mas-posibilidades-de-desarrollo-economico-con-los-grandes-eventos-1216/
- Perfil / Canal E — "Crisis hotelera en CABA" (mar. 2026): https://www.perfil.com/noticias/canal-e/crisis-hotelera-en-caba-turismo-en-baja-servicios-por-las-nubes-y-ocupacion-floja.phtml
- Ladevi — AHT advierte caída de empleo y pide alivios fiscales: https://argentina.ladevi.info/actualidad/hoteles-crisis-aht-advierte-la-caida-empleo-denuncia-ocupacion-baja-y-pide-alivios-fiscales-n86710
- Infobae — Validación digital del reintegro de IVA, RG 5843/2026 (may. 2026): https://www.infobae.com/economia/2026/05/06/la-validacion-para-el-reintegro-del-iva-a-turistas-extranjeros-sera-digital-a-partir-de-ahora/
- El Cronista — Registro de alquileres temporarios CABA: https://www.cronista.com/economia-politica/caba-regulariza-la-situacion-de-los-alquileres-temporarios-como-registrar-mi-propiedad-en-airbnb/
- Hosteltur — Carga impositiva 40% del precio (IARAF/FEHGRA, 2015): https://www.hosteltur.com/lat/120800_40-precio-se-paga-hoteles-argentina-responde-al-costo-impositivo.html
- Perfil — Salarios hasta 55% de las ventas: https://www.perfil.com/noticias/cordoba/los-salarios-representan-hasta-55-de-las-ventas-de-los-hoteles.phtml
- Diario del Hotelero — WeSpeak, AI y pagos por WhatsApp (feb. 2026): https://www.diariodelhotelero.com/nota-argentinos-crean-una-ia-para-reservar-y-pagar-hoteles-por-whatsapp-ya-la-usan-grandes-cadenas-en-la-region-172999

**Tecnología y benchmarks sectoriales**
- Pxsol — Costo de depender de Booking y Airbnb: https://www.pxsol.com/blog/cu%C3%A1nto-te-cuesta-depender-de-booking-y-airbnb
- Pxsol — Software hotelero en Argentina: https://www.pxsol.com/blog/software-hotelero-en-argentina-panorama-y-opciones-disponibles
- Pxsol — Hotelería argentina 2026: https://www.pxsol.com/blog/hoteler%C3%ADa-argentina-2026
- Pxsol — Factura T: https://www.pxsol.com/blog/factura-t-en-argentina-todo-lo-que-hay-que-saber
- Shiji Insights / Cornell — Reputación online y RevPAR: https://insights.shijigroup.com/es/cornell-hospitality-research-online-reputation-directly-affects-pricing-power-occupancy-revpar/
- TecnoHotel — Informe Canary: 82% de hoteles aumentará AI en 2026: https://tecnohotelnews.com/2026/04/ia-hoteles-2026-informe-canary/
- Estudio Vilaplana — Escalas salariales UTHGRA-FEHGRA 2026: https://estudiovilaplana.com.ar/sueldos-gastronomicos/
- Cloudbeds — Guía de comisiones OTA 2026: https://www.cloudbeds.com/online-travel-agencies/commissions/

**Fuentes consultadas sin dato utilizable / descartadas**
- Infobae "200 hoteles en venta en la Ciudad" — **descartada por obsoleta**: es de enero 2021 (contexto pandemia), no refleja 2026: https://www.infobae.com/economia/2021/01/24/la-grave-crisis-de-los-hoteles-portenos-estiman-que-hay-mas-de-200-en-venta-en-la-ciudad/
- Ente de Turismo CABA "ocupación más alta de la década" — datos de 2022, no vigentes: https://turismo.buenosaires.gob.ar/es/turismo-noticias/buenos-aires-tuvo-el-promedio-de-ocupaci%C3%B3n-hotelera-m%C3%A1s-alto-de-la-d%C3%A9cada
