# Decisión del Lead Agent tras el Red Team

## Veredicto del Devil's Advocate sobre "Pulso": MATAR

## Qué de su crítica acepto, y qué no

### Acepto — Bala 2: el competidor gratis ya está adentro del hotel
Booking.com regala el *Opportunity Center* con benchmarking contra comparables y recomendación de precio, en la extranet que el hotelero abre todos los días. SiteMinder vende *Dynamic Revenue Plus* con IDeaS y **aplica el precio automáticamente a los canales** — el paso que Pulso había decidido no hacer. PriceLabs cobra ~USD 10/unidad/mes. Un producto sin marca que recomienda tarifas a USD 150 tiene que ser 10× mejor que lo gratis para justificarse. No lo es.

### Acepto — Bala 3: el foso del benchmark era más flaco de lo que escribí
Verifiqué en vivo: el [Observatorio del Ente de Turismo porteño publica un tablero de ocupación hotelera](https://turismo.buenosaires.gob.ar/es/observatorio/tableros/ocupacion-hotelera) por categoría. El "apagón estadístico" del INDEC es real para el dato nacional, pero la ocupación de CABA no desapareció. Queda un hueco solo en ADR — y el ADR es exactamente el dato que ningún hotelero le entrega a un desconocido. Peor: **[Pxsol ya publicó su página de Revenue Management con la leyenda "Próximamente"](https://www.pxsol.com/es-ar/revenuemanagement)**, con reglas por competencia, demanda y ventana de reserva. Tienen +1.500 hoteles conectados. El dato que yo iba a construir de a un cliente por vez, ellos lo corren con una query.

### Acepto parcialmente — Bala 1: el techo
El cálculo del ARR es correcto, pero mal atribuido: un techo de USD 166k **castiga por igual a las cinco oportunidades**, porque el límite lo puso la consigna (restringir a CABA), no el producto. No sirve para elegir entre opciones. Lo que sí me llevo como restricción de diseño: **CABA es cabecera de playa y cualquier oportunidad cuyo valor sea intrínsecamente porteño está condenada al techo.** Un índice de mercado de CABA es, por definición, un producto de una sola ciudad. Eso sí es un cargo específico contra Pulso.

### Rechazo — el supuesto "error de base"
El Devil's Advocate acusó al equipo de usar 45-50% de ocupación cuando el dato real sería 70-74%. Fui a la fuente: [Ámbito, 29/07/2026](https://www.ambito.com/negocios/hoteles-alerta-la-ocupacion-ronda-el-65-que-estrategias-trazan-sobrevivir-n6304861) dice **~65% general, 4★ arriba de 60%, y 2-3★ en 45-50%**. Los dos números son ciertos: uno es el promedio y el otro es el segmento. La acusación no se sostiene. Lo anoto porque un red team que exagera también hay que auditarlo.

## Decisión: **DESCARTAR Pulso y tomar la segunda opción, modificada**

Uso la opción que el ejercicio habilita explícitamente: descartar y elegir la segunda. Pero no la tomo tal como venía.

**Lo que se descarta:** el copiloto de tarifas y el índice de mercado. Dos balas letales sin respuesta honesta.

**Lo que se toma:** O2 — el circuito de exención de IVA a huéspedes no residentes. **Modificada en su posicionamiento**, de herramienta de cumplimiento a herramienta de ingresos.

## Por qué O2 sobrevive a las mismas balas que mataron a O1

| Bala del Red Team | Contra Pulso | Contra la opción elegida |
|---|---|---|
| Competidor gratis adentro del hotel | Letal: Booking Focus Finder | **No aplica.** Booking no factura, no arma legajos y no presenta regímenes informativos. Ninguna OTA tiene incentivo a construirlo. |
| Incumbente local a punto de lanzar | Letal: Pxsol RM "Próximamente" | **Parcial.** Pxsol y MiniHotel emiten Factura T, pero emitir el comprobante no es detectar la elegibilidad, armar el legajo probatorio ni presentar la DDJJ mensual. Y se vende **al lado** de cualquier PMS, no en su contra. |
| Techo de ARR por ser porteño | Letal: el índice es de una sola ciudad | **No aplica.** El régimen es **nacional** (RG Conjunta 3971/2016 AFIP + Res. 566/2016 MinTur) y alcanza también a agencias de viaje habilitadas. CABA es entrada, no límite. |
| Requiere integración de PMS | Evitado a costa de no cerrar el loop | **Evitado de verdad.** Trabaja sobre el export de reservas y la liquidación de la pasarela/tarjeta; el comprobante lo emite el PMS que ya tiene el hotel. |
| La AI es calcomanía | Cierto: era ETL y reglas | **Falso acá.** Lectura multilingüe de pasaportes y documentos migratorios, extracción y verificación de residencia, y detección de tarjeta emitida en el exterior por BIN. El núcleo es extracción de documentos: AI genuina. |

## Por qué corregí mi propio rechazo anterior
En la síntesis descarté O2 por una confusión regulatoria y por riesgo legal. Resolví la confusión: la **RG 5843/2026** regula el *tax free minorista de bienes* (factura clase B, validación digital en línea) y **no es** el régimen de alojamiento. El de alojamiento es la **RG Conjunta 3971/2016**, con condiciones verificables: pago con tarjeta emitida en el exterior o transferencia desde un banco del exterior, pasaporte y documentación migratoria en legajo, comprobante clase T, y régimen informativo mensual **hasta el día 15 del mes siguiente**. Saber distinguir estos dos regímenes no es un detalle: es exactamente el conocimiento que hace defendible al producto y que un SaaS internacional nunca va a tener.

El riesgo legal se acota por diseño: el producto **prepara y prueba**, no asesora ni firma. El contador del hotel sigue siendo el responsable, y el legajo probatorio que hoy no existe es, precisamente, lo que lo protege a él.

## El giro que convierte cumplimiento en ingresos
Ninguno de los cinco especialistas lo dijo, y es el corazón de la oferta: **la exención vale 21% sobre la tarifa, y el hotel elige qué hacer con ella.** Puede pasarla al huésped y mostrar un precio 17,4% más bajo que el hotel de al lado que no sabe operar el régimen, o retenerla y mejorar el margen. Es la única palanca disponible en este mercado que mejora la competitividad **sin tocar el precio neto**, en un sector que —según AHRCC— "sobrevive con endeudamiento" y donde los 2-3★ están al 45-50% de ocupación. La Ciudad ya [promociona el alojamiento libre de IVA como argumento de venta](https://turismo.buenosaires.gob.ar/en/article/vat-free-accommodation); el hotelero es el que no lo puede ejecutar.

Y hay evidencia directa del fallo operativo, del Pain Miner: un huésped citando a la recepción de un hotel argentino — *"they don't have the software for it"*.

## Producto elegido: **Veintiuno**
Detecta, prueba y presenta la exención de IVA a huéspedes no residentes. Empieza por el diagnóstico —cuánta plata dejó el hotel sobre la mesa en los últimos 90 días— y sigue como servicio mensual.

## Hipótesis que siguen sin validar (heredadas del Red Team)
1. Que el hotelero pague en dólares o indexado. **Mitigación de diseño:** facturación en pesos y opción de precio por performance.
2. Que el hotelero entregue su export de reservas y liquidaciones a un desconocido. Es menos sensible que el ADR, pero sigue siendo un pedido fuerte.
3. Que la fuga sea material. Si el hotel promedio ya lo hace bien, no hay negocio. **Es la hipótesis fatal y se testea con el propio diagnóstico, sin escribir producto.**
