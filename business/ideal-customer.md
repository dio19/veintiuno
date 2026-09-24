# Veintiuno — Cliente ideal (ICP)

La regla que ordena todo: **el valor de Veintiuno es proporcional al IVA que el hotel tiene en juego cada mes**, y ese número es `noches extranjeras × % que paga con tarjeta emitida en el exterior × tarifa neta × 21%`. Todo lo que sigue son proxies **verificables desde afuera** de esas tres variables. Nada acá requiere que el hotel nos atienda el teléfono.

---

## Señales visibles que delatan volumen de extranjeros

| Señal | Dónde se mira | Qué significa |
|---|---|---|
| Idioma de las últimas 30 reseñas | Booking, Google Maps, TripAdvisor | Proxy más fuerte y más barato. ≥50% en inglés/portugués/francés/alemán = huésped no residente real |
| Nacionalidad declarada del reseñador | Booking muestra país | Brasil y Chile pagan mucho con tarjeta local o en pesos: **descontar**. EE.UU., Europa, resto de LatAm suman |
| Sitio propio con versión en inglés real (no traductor) | Web del hotel | Alguien decidió invertir en el mercado externo |
| Precios publicados en USD | Motor de reserva directa | Ya piensa en moneda del huésped; conversación de exención es corta |
| Menciona "VAT free" / "tax free" / "exención de IVA" | Web, FAQ, Booking, IG | **Doble lectura**: o ya lo opera (y le falta el legajo y el informativo), o lo promete y no lo cumple. Las dos son venta |
| Motor de reserva directa propio | Web | Módulo 4 (cotización sin IVA) tiene dónde enchufarse |
| IG con captions en inglés / respuestas en inglés | Instagram | Boutique con receptivo alto |
| Ubicación | Google Maps | Microcentro-San Nicolás, Retiro, Recoleta, Puerto Madero, Palermo Soho/Hollywood |
| PMS visible | Motor de reserva (footer, URL del booking engine) | Cloudbeds, Little Hotelier/SiteMinder, Zeus y desarrollos locales. **Criterio operativo real: que exporte reservas a CSV/Excel.** El mix exacto de PMS en CABA está SIN VERIFICAR |

---

## Segmento primario — hotel independiente 3-4★ de 25 a 90 habitaciones con receptivo alto

Microcentro/San Nicolás, Retiro, Recoleta, Congreso, Palermo. Sin cadena internacional detrás. ADR de ARS 70.000 a 160.000 con IVA. Recepción 24/7 con 3-6 personas. Contador externo (estudio chico, no in-house). PMS que exporta CSV. Entre 35% y 70% de huéspedes extranjeros.

**Por qué compra:** tiene la plata en juego (ARS 1,5 a 4 millones de IVA por mes), no tiene a nadie que ejecute el circuito, y la exención le permite mostrar un precio 17,4% más bajo sin bajar la tarifa neta. Además el legajo lo protege: hoy, si lo aplica, lo aplica mal.

**Decisor real:** dueño o gerente general. Firma solo. **Guardián:** jefe de recepción (filtra el mostrador y el teléfono) y el **contador externo**, que tiene veto técnico — por eso el contador se convierte en aliado, no en obstáculo. **Presupuesto tolerable:** ARS 180.000-360.000/mes; es menos que un ADR-mes y una fracción de lo que paga de comisión de OTA.

**Tamaño:** CABA **60-90 hoteles**. Nacional, extrapolando a los destinos de receptivo alto: **250-400** (estimación, SIN VERIFICAR).

## Segmento secundario — 4-5★ independiente grande y apart-hotel habilitado

90-180 habitaciones, Puerto Madero, Palermo, Recoleta; apart-hoteles con habilitación turística y estadías largas de ejecutivos extranjeros. Ciclo de venta más largo (hay gerente de administración de por medio) y a veces back-office propio, pero el volumen los hace ir a Plan Recupero o Performance.

**Tamaño:** CABA **40-60**. Nacional **150-250** (estimación, SIN VERIFICAR).

## Segmento de expansión — destinos de receptivo fuera de CABA

Bariloche, Mendoza (bodegas con alojamiento), Iguazú, Salta, El Calafate, Ushuaia. Boutique y lodges de ticket alto con proporción de extranjeros arriba del 60%. Se abre recién con 10-15 clientes en CABA y venta 100% remota.

**Tamaño:** **300-500** establecimientos (estimación, SIN VERIFICAR).

---

## Anti-ICP — a quién NO venderle

- **Hoteles con menos de 20-25% de huéspedes extranjeros.** Aunque cierren, el IVA en juego no paga el fee y se dan de baja al tercer mes. Churn caro.
- **Cadenas internacionales (Hilton, Marriott, Accor, Meliá y similares).** Back-office regional, PMS corporativo cerrado, compras por casa matriz. Ciclo de 9 meses para un ticket de USD 240.
- **Hostels y ticket bajo (ADR < ARS 35.000).** Tienen muchísimo extranjero pero el IVA por estadía es chico y la mayoría paga en efectivo o con tarjeta local. La cuenta no cierra para ninguno de los dos.
- **Alquileres temporarios no habilitados y "departamentos turísticos" sin registro.** No hay encuadre limpio para operar el régimen y el riesgo lo heredamos nosotros.
- **Hoteles donde el extranjero paga en pesos, en efectivo o con tarjeta emitida en Argentina.** Es la condición dura del régimen: **pago local no califica**. Un hotel con 80% de extranjeros brasileños pagando en pesos vale cero.
- **Hoteles con deuda o problemas ante ARCA** que no pueden gestionar la autorización previa de clase "T". Ahí el bloqueo no lo resuelve un software.

---

## Checklist de calificación — 8 preguntas, 5 minutos, 100 puntos

| # | Pregunta (respondible mirando internet) | Puntaje |
|---|---|---|
| 1 | De las últimas 30 reseñas en Booking/Google, ¿qué % está en idioma extranjero? | ≥50% = **20** · 25-49% = 10 · <25% = 0 |
| 2 | ¿Cuántas habitaciones tiene? | 25-90 = **10** · 15-24 o 91-150 = 5 · resto = 0 |
| 3 | ¿Es independiente o de cadena? | Independiente = **15** · cadena local ≤5 propiedades = 8 · cadena internacional = 0 |
| 4 | ¿Hay una persona con nombre y mail directo (dueño/GG) en padrón ENTUR, web o LinkedIn? | Sí = **15** · solo mail genérico = 6 · nada = 0 |
| 5 | ¿Tiene sitio propio con inglés real y motor de reserva directa? | Ambos = **10** · uno = 5 · ninguno = 0 |
| 6 | ¿ADR publicado ≥ ARS 70.000 con IVA en fecha alta? | Sí = **10** · 45-70k = 5 · <45k = 0 |
| 7 | ¿Está en Microcentro/San Nicolás, Retiro, Recoleta, Puerto Madero o Palermo? | Sí = **10** · resto de CABA = 4 |
| 8 | ¿Menciona "VAT free"/"tax free"/exención en algún lado, o publica en USD? | Menciona exención = **10** · publica USD = 5 · nada = 0 |

**Umbral:** **65 o más → se produce la estimación preliminar y se contacta esta semana.** 45 a 64 → lista B, contacto masivo sin estimación personalizada. Menos de 45 → no se toca.

Regla dura que anula el puntaje: si la pregunta 1 da menos de 25% **y** el hotel es de barrio periférico, **descartar aunque sume 60**. Sin extranjeros no hay producto.
