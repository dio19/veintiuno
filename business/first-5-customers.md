# Veintiuno — Los primeros 5 clientes pagos en 30 días

Ventana: **lunes 14/09/2026 a martes 13/10/2026**. Sin publicidad, sin agencia, sin equipo. Una persona full-time.

## La aritmética del embudo

Dos productos distintos y no hay que confundirlos: la **estimación preliminar** (1 página, hecha con datos públicos, es el regalo que va adjunto al primer mail) y la **Radiografía del 21%** (el diagnóstico real de 90 días, sin cargo, que requiere el export del PMS y se entrega en 48 horas). El regalo abre la puerta; la Radiografía cierra la venta.

| Canal | Toques | → Respuesta / contacto útil | → Reunión | → Radiografía real | → Cierre |
|---|---|---|---|---|---|
| Mail en frío con estimación adjunta | 90 | 11 (**12%**) | 7 | 5 | **2** |
| Puerta a puerta Microcentro | 60 visitas | 15 (**25%**) | 6 | 4 | **2** |
| Estudios contables (referidos) | 15 estudios | 5 conversaciones → 2 acuerdos → 3 hoteles | 2 | 2 | **1** |
| FIT América Latina (28-29/09) | 40 charlas | 12 con permiso de contacto | 5 | 3 | (cierra en octubre) |
| **Total 30 días** | | | **20** | **14** | **5** |

**De dónde salen las tasas.** El 12% de respuesta al mail está dentro del rango 8-15% que da un cold email 2026 **con un regalo específico adjunto**, contra 3,43% del promedio sin regalo; es el extremo conservador del rango con regalo. El 25% del puerta a puerta es contacto útil, no venta: en Microcentro la recepción está abierta 24/7 y de cada 4 visitas una deja el material en manos del gerente o entrega su mail directo. Reunión→Radiografía es alto (70-80%) porque la Radiografía es gratis y el pedido es un export de dos clics. **Radiografía→cierre es 36% (5 de 14)** y es la tasa que hay que defender: la Radiografía muestra un número en pesos, propio del hotel, ya perdido. Si esa tasa da menos de 25%, el problema no es el embudo, es la oferta.

**Resultado esperado:** 5 clientes. Mix supuesto 3 Recepción + 2 Recupero = **USD 840/mes ≈ ARS 1.260.000/mes**, más onboarding.

## La lista de 200-300 hoteles en un día

1. **Padrón ENTUR (PDF, julio 2026)**, ~450+ establecimientos de CABA con nombre, domicilio, barrio, teléfono y mail. Extracción de tablas del PDF a CSV.
2. **Dataset abierto GCBA "Alojamientos Turísticos"** (data.buenosaires.gob.ar, act. 1/9/2026): `nombre, domicilio, telefono, email, web, tipo, Long, Lat`. Aporta web, mail y coordenadas.
3. **Merge** por nombre normalizado + domicilio. Resuelve ~85% automático; el resto a mano.
4. **Enriquecimiento con Google Places**: rating, cantidad de reseñas, idioma de las últimas 30, lat/long para el ruteo del puerta a puerta.
5. **Booking**: cantidad de habitaciones, categoría, ADR en fecha alta, país de los reseñadores.
6. **Filtro y scoring** con la checklist de 8 preguntas de `ideal-customer.md`. Salida: **Lista A** (≥65 pts, 80-90 hoteles) y **Lista B** (45-64).

Priorización: primero Lista A ordenada por `% reseñas en idioma extranjero × habitaciones`, que es el proxy directo del IVA en juego. Dentro de la A, los de **Microcentro/San Nicolás** se marcan para puerta a puerta (70-90 caminables) y el resto va a mail.

## Plan día por día

| Día | Fecha | Actividad | Número |
|---|---|---|---|
| 1 | lun 14/09 | Extracción ENTUR + GCBA, merge | 450 filas |
| 2 | mar 15/09 | Enriquecimiento Places/Booking + scoring | 250 puntuadas |
| 3 | mié 16/09 | Plantilla de estimación preliminar + 15 primeras | 15 |
| 4 | jue 17/09 | Estimaciones + envío ola 1 | 30 enviados |
| 5 | vie 18/09 | Estimaciones + envío ola 2 | 30 enviados |
| 6-7 | sáb-dom | Off. Solo responder | — |
| 8 | lun 21/09 | Follow-up día 4 ola 1 + envío ola 3 | 30 + 30 |
| 9 | mar 22/09 | Puerta a puerta San Nicolás | 20 visitas |
| 10 | mié 23/09 | Puerta a puerta Microcentro sur | 20 visitas |
| 11 | jue 24/09 | Mail a 15 estudios contables + reuniones | 15 |
| 12 | vie 25/09 | Follow-up ola 2 + armado material FIT | 30 |
| 13-14 | sáb-dom | Off. Prep FIT | — |
| 15 | lun 28/09 | **FIT La Rural, día profesional 1** | 20 charlas |
| 16 | mar 29/09 | **FIT día profesional 2** | 20 charlas |
| 17 | mié 30/09 | Cierre de mes: nada de frío. Radiografías reales | 3 entregadas |
| 18 | jue 01/10 | Reuniones de descubrimiento | 4 |
| 19 | vie 02/10 | Radiografías + propuestas | 3 + 2 |
| 20-21 | sáb-dom | Off | — |
| 22 | lun 05/10 | Follow-up FIT + puerta a puerta Retiro | 12 + 20 |
| 23 | mar 06/10 | Reuniones de resultados de Radiografía | 4 |
| 24 | mié 07/10 | **Cierres 1 y 2** + propuestas nuevas | 2 firmados |
| 25 | jue 08/10 | Onboarding cliente 1 + reuniones | 3 |
| 26 | vie 09/10 | Radiografías + follow-up día 9 | 3 + 30 |
| 27-28 | sáb-dom | Off | — |
| 29 | lun 12/10 | **Cierres 3, 4 y 5** | 3 firmados |
| 30 | mar 13/10 | Onboarding + medición del mes + Lista B | 5 activos |

## Los 4 canales, rankeados

**1. Radiografía + mail en frío.** Mejor costo/esfuerzo: 90 contactos escalables desde el escritorio, el regalo adjunto triplica la respuesta contra un mail pelado. Cuello de botella: producir la estimación (12-15 min con plantilla). 2 cierres.

**2. Puerta a puerta en Microcentro.** 70-90 hoteles caminables, recepción abierta 24/7, y **nadie del software B2B hace esto ahí**. Sin competencia por atención. Costo: solo tiempo. Peor escalabilidad, mejor tasa. 2 cierres.

**3. Alianza con estudios contables de hotelería y gastronomía.** El canal de mayor palanca a mediano plazo y el más lento en arrancar. El legajo probatorio **protege al contador**, que es el que hoy carga con el riesgo de la clase T y del informativo del día 15. Un estudio con 12 hoteles vale más que 100 mails. 1 cierre en el mes, muchos más después.

**4. FIT América Latina, 26-29/09/2026 en La Rural** (lunes 28 y martes 29 exclusivos para profesionales). No cerramos ahí: recolectamos. Plan: recorrer stands de hoteles y cámaras (AHT, AHRCC), 20 conversaciones por día con el guion de 60 segundos, pedir permiso explícito para mandar la estimación, anotar en la tarjeta el dato del hotel para el mail del lunes siguiente. **No stand, no folletería masiva.** Objetivo: 12 permisos y 3 reuniones para octubre. Fechas 2027 de Hotelga y Expo Eventos: **SIN VERIFICAR**.

## Piloto: pago, no gratis

**No hay piloto gratis.** Lo gratis no se implementa: recepción no capacita, el contador no se sienta y el export nunca llega. Un piloto sin factura es un cliente que nunca arrancó. Además el descuento fundacional destruye el precio de referencia para los siguientes 20 hoteles.

Lo gratis ya lo dimos: **la Radiografía**. Vale 48 horas de trabajo real y prueba competencia técnica.

Lo que sí se concede a los primeros 5:
- **Precio congelado 12 meses** (sin el ajuste trimestral por índice).
- **Onboarding bonificado** (USD 350 → cero).
- **Salida sin costo con 30 días de aviso**, por escrito.
- Nombre en los materiales solo con autorización.

## Señales de pivoteo, con umbrales

- **Respuesta al mail < 6% sobre 60 enviados** → el asunto o el gancho no funcionan. Reescribir asunto y primera línea antes de mandar los 30 restantes.
- **Reunión→Radiografía < 50%** → el pedido de export asusta. Ofrecer hacerlo sobre 30 días en vez de 90.
- **Radiografía→cierre < 25% con 8 Radiografías entregadas** → problema de oferta, no de embudo. Sospechar precio o que la fuga real es menor al 40% supuesto.
- **Fuga real promedio < 15% en las primeras 5 Radiografías** → el supuesto central del negocio está mal. Frenar y revisar tesis.
- **3 de 5 Radiografías dan menos de ARS 400.000/mes de IVA en juego** → el ICP está mal calibrado, hay que subir tamaño y % de extranjeros.
- **Objeción "ya lo hace mi PMS" en más del 40% de las reuniones** → hay un competidor real. Investigar cuál antes de seguir vendiendo.
- **0 clientes al día 30 con 14 Radiografías entregadas** → no es problema de volumen. Parar el outreach una semana y rehacer la oferta.

## Qué se mide cada semana

Hoteles calificados en Lista A · estimaciones producidas · mails enviados · **tasa de respuesta** · reuniones agendadas · **Radiografías entregadas** · fuga promedio detectada en pesos · propuestas · cierres · MRR firmado · días desde el primer contacto hasta la firma. Un tablero, revisión los lunes a las 9.
