# Síntesis del Lead Agent — cruce de los 5 especialistas
_Nicho: hotelería independiente en CABA · Formato buscado: micro-SaaS con recurrencia · Septiembre 2026_

## 1. Los seis hechos que gobiernan la decisión

**H1 — La ventana de reserva colapsó a ~3 días.** Camilo Suárez, presidente de la Cámara de Hoteles de AHRCC: *"La planificación prácticamente desapareció. Hoy muchas reservas ingresan apenas tres días antes del viaje"* (Ámbito, 29/07/2026). Alejandra Rodríguez Díaz (FEHGRA) confirma estadías más cortas y reservas de último momento. Es la evidencia **más fuerte del cuerpo entero**: dos dirigentes sectoriales, con nombre, fecha y medio, en 2026, describiendo un cambio estructural. No es contenido de vendor.

**H2 — El mercado se partió en dos y la mitad de abajo está en problemas.** Julio 2026: 4★ arriba del 60% de ocupación, 2-3★ en 45-50%. El receptivo internacional a CABA creció 19% i.a., pero el margen se comió la mejora: energía +1.000%, salarios hasta 55% de las ventas, $60 de impuestos cada $100 facturados (AHT). AHRCC: *"El sector sobrevive con endeudamiento"*.

**H3 — Apagón estadístico.** El INDEC dejó de publicar la Encuesta de Ocupación Hotelera; el último informe difundido corresponde a diciembre 2025, y la causa fue que la Secretaría de Turismo no renovó el convenio de financiamiento ([0223, 10/03/2026](https://www.0223.com.ar/nota/2026-3-10-12-39-0-apagon-estadistico-el-indec-dejo-de-publicar-la-encuesta-de-ocupacion-hotelera)). El portal de carga `eoh.indec.gob.ar` sigue en línea. Lectura: **el hotelero puede seguir cargando datos y ya no recibe nada a cambio.** Se quedó sin espejo justo cuando más lo necesita.

**H4 — El mejor RMS del mundo para hoteles chicos no puede entrar a Argentina.** RoomPriceGenie tiene 80+ integraciones de PMS y **cero latinoamericanas**. El hotel que eligió un PMS argentino para cumplir con ARCA quedó, por esa misma decisión, excluido de la herramienta de pricing de su tamaño. Es un hueco creado por la estructura del mercado, no por descuido.

**H5 — El carril del chatbot ya tiene dueño local.** WeSpeak: 500+ hoteles, cadenas grandes, 125.000 reservas en 2025, ticket de referencia USD 247/mes. Asksuite trae 606 hoteles en Brasil. Entrar de frente a "AI + WhatsApp + reservas" es pelear contra distribución instalada sin marca.

**H6 — El universo de CABA es chico y hay que decirlo en voz alta.** 440 hoteles, ~150-220 independientes reales, **60-90 en el ICP**. Al ticket de referencia del mercado, el 100% de CABA son ~USD 960k de ARR. **CABA es cabecera de playa, no mercado.** Cualquier oportunidad que no sea replicable a Córdoba, Mendoza, Bariloche, Montevideo y Santiago está muerta al nacer.

## 2. El filtro que aplico

Tres tests eliminatorios, derivados de lo que encontraron los especialistas:

- **Test del conector:** ¿requiere integrarse al PMS del cliente? Los PMS argentinos son los que menos incentivo tienen a abrir API. Todo lo que dependa de eso muere en la etapa de implementación.
- **Test del mes 6:** ¿por qué sigue pagando cuando el valor inicial ya se entregó? El Radar de Paridad se agota en el mes 3; es un gancho, no un producto.
- **Test de la AI honesta:** ¿la AI es el motor o la calcomanía? El Offer Architect fue explícito: en varias opciones el núcleo es ETL y una planilla. No es descalificante, pero prohíbe vender "AI" como si fuera la ventaja.

## 3. Las cinco oportunidades finalistas

**O1 · Copiloto de tarifas + benchmark ("Pulso").** Recomendación diaria de tarifa por fecha para hoteles independientes, leyendo demanda desde los canales públicos y el propio pace del hotel, sin integración de PMS. Devuelve además el benchmark de ocupación y ADR de CABA que el INDEC dejó de publicar, construido con los datos anonimizados de los propios clientes.

**O2 · Fisco Huésped.** Automatización del circuito Factura T / exención de IVA a no residentes, con legajo probatorio y conciliación contra libro IVA.

**O3 · Recepción 24/7 en WhatsApp.** Agente que cotiza con disponibilidad y tarifa real, reserva y cobra seña por Mercado Pago.

**O4 · Cotizador de grupos y corporativos.** Hoy es Excel + mail + WhatsApp. Cero productos en todo el mapa competitivo.

**O5 · Parte diario unificado.** Consolida PMS, POS, caja y Mercado Pago en un reporte a las 8 AM.

## 4. Matriz de evaluación (1-5)

| Criterio | O1 Pulso | O2 Fisco | O3 Recepción | O4 Grupos | O5 Parte diario |
|---|---|---|---|---|---|
| Intensidad del problema | **5** | 4 | 4 | 3 | 3 |
| Frecuencia | **5** | 4 | 5 | 2 | 5 |
| Facilidad para encontrar clientes | 4 | 3 | 4 | 3 | 3 |
| Capacidad de pago | 4 | **5** | 4 | 4 | 3 |
| Velocidad al MVP | 4 | 4 | 2 | 3 | 4 |
| Diferenciación | **5** | 4 | 1 | **5** | 3 |
| Potencial de recurrencia | **5** | **5** | 4 | 2 | 4 |
| **Total (máx. 35)** | **32** | **29** | 24 | 22 | 25 |

## 5. Oportunidad elegida: **O1 — Pulso**

**Copiloto de tarifas para hoteles independientes, con el benchmark de mercado incorporado.**

La evidencia que decidió, en orden de peso:

1. **Es el único dolor con evidencia primaria de máxima calidad.** H1 no viene de un blog de proveedor: son dos dirigentes gremiales, citados textualmente, en 2026, describiendo exactamente el problema que el producto resuelve. El Pain Miner clasificó todo lo demás en confianza media o baja, y descartó explícitamente "overbooking" y "responder reseñas" por ser dolores fabricados por vendors.
2. **Pasa el test del conector.** Se alimenta de tarifas públicas de los canales y de un export de reservas; no necesita que un PMS argentino abra su API. Esto elimina la barrera que, según el Competitor Analyst, es el foso de toda la industria.
3. **Tiene un hueco estructural, no coyuntural.** H4: el líder de la categoría no puede entrar por una razón que no va a cambiar pronto. No es que nadie lo pensó; es que a nadie de afuera le conviene resolverlo.
4. **El benchmark resuelve el test del mes 6 y construye foso.** H3 dejó un vacío informativo real. Cada cliente nuevo mejora el dato agregado, que mejora el producto para todos, y ese dato no lo tiene ningún PMS internacional ni se puede comprar. Es la única de las cinco donde la retención mejora con el tiempo en vez de degradarse.
5. **El valor se mide en ingresos, no en horas ahorradas.** A un hotel que sobrevive con endeudamiento (H2) no se le vende "te ahorro tiempo". Se le vende RevPAR.

**Por qué NO elegí O2 (Fisco Huésped), que puntuó segundo y que el Offer Architect había puesto primero:** tres razones. Primero, hay una confusión regulatoria en el cuerpo de investigación que hay que corregir antes de que llegue a un pitch: la RG 5843/2026 de ARCA regula el **reintegro de IVA en compras de bienes** (tax free minorista, factura clase B) y no es el mismo régimen que la **Factura T de alojamiento** a no residentes. Construir una oferta sobre una norma mal leída es un pasivo. Segundo, Pxsol y MiniHotel ya lo venden como feature del PMS: hay demanda probada y también incumbente. Tercero, y decisivo, un producto de cumplimiento fiscal tiene responsabilidad legal asimétrica — el upside es un ahorro administrativo, el downside es una sanción del cliente.

**La advertencia que me llevo:** el Pain Miner encontró evidencia sólida de dolor y **evidencia débil de intención de pago**. Ni un solo hotelero argentino escribiendo "estoy pagando X por Y". Eso no invalida la elección, pero define la primera hipótesis a matar.
