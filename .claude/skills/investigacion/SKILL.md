---
name: investigacion
description: Investigación de escritorio para Veintiuno sobre normativa (IVA a no residentes, RG Conjunta 3971/2016, Res. 566/2016, RG 5843/2026, ARCA/AFIP, MinTur), mercado hotelero argentino, competidores y canales. Usalo cuando haya que verificar una afirmación, buscar la fuente primaria de algo marcado SIN VERIFICAR o investigar un tema nuevo para el proyecto. No es para investigar un hotel prospecto puntual: para eso está el paquete investigacion_hotel.
argument-hint: <tema o afirmación a verificar>
---

# Investigación — Veintiuno

Tema: $ARGUMENTS

Todo en castellano rioplatense (voseo). El objetivo es **una afirmación con su fuente**, no un
resumen de lo que dice internet. Si no hay fuente primaria, se dice: eso también es un resultado.

## 1. Antes de buscar

1. Leé lo que el proyecto ya sabe del tema: `grep -rn "<palabra clave>" research/ validation/ business/`.
   Si el tema está marcado `SIN VERIFICAR` o `NO VERIFICADO` en algún lado, anotá archivo y línea:
   el objetivo es resolver esa marca.
2. Si el tema toca el régimen, la descripción canónica es `investigacion_hotel/normativa.py`
   (`MARCO`, `CONDICIONES`, `COMPROBANTE`, `PROHIBIDO`). No la parafrasees: contrastá contra ella.

## 2. Jerarquía de fuentes

Buscá de arriba hacia abajo y quedate con la más alta que encuentres:

| Nivel | Fuente | Etiqueta |
|---|---|---|
| 1 | Texto de la norma: Boletín Oficial (boletinoficial.gob.ar), InfoLEG, biblioteca de ARCA | `[DATO]` |
| 2 | Organismo oficial: ARCA/AFIP, Ministerio/Secretaría de Turismo, INDEC, Ente de Turismo CABA | `[DATO]` |
| 3 | Cámaras y asociaciones: FEHGRA, AHT, AHRCC | `[DATO]` con la cámara como fuente |
| 4 | Estudios contables, prensa especializada, sitios de proveedores | `[SECUNDARIA]`: sirve de pista, nunca cierra un tema normativo |
| — | Cálculo propio a partir de datos citados | `[EST]`, con la cuenta a la vista |
| — | Sin fuente | `SIN VERIFICAR` |

- **Normativa: sólo nivel 1 o 2 la da por verificada.** Un blog contable que cita una RG no
  reemplaza leer la RG.
- Los PDFs (Boletín Oficial, padrones, anuarios estadísticos) se leen con el MCP `markitdown`
  (`convert_to_markdown` con la URL). Si el MCP no está disponible, usá `WebFetch` y dejá anotado
  que la lectura puede tener errores de extracción.
- Para buscar: `WebSearch`. Para leer HTML: `WebFetch`. Temas amplios con varias líneas
  independientes: un subagente `general-purpose` por línea, en paralelo.

## 3. Reglas de dominio (no se reinterpretan)

- El régimen es **RG Conjunta 3971/2016 + Res. 566/2016**: no residente + tarjeta del exterior o
  transferencia del exterior + sólo alojamiento y desayuno, con **factura clase T**.
- **La RG 5843/2026 es otro régimen** (tax free minorista de bienes, factura B). Si una fuente los
  mezcla, eso es un hallazgo: anotalo y no la uses como fuente del régimen.
- **El pago local no habilita**, sin excepción. Si una fuente dice lo contrario, reportalo como
  contradicción y no lo tomes como verdad.
- Quitar el IVA de un precio final es **−17,36%** (1 − 1/1,21), no −21%.
- No se da asesoramiento fiscal ni se predice el resultado de una fiscalización. Si el tema es un
  caso límite, la conclusión es "lo resuelve el contador del hotel", con las fuentes que tendría
  que mirar.
- Nunca se completa un dato por analogía (otro país, otro año, otra provincia) sin marcarlo `[EST]`
  o `SIN VERIFICAR`.

## 4. Dónde va el resultado

- **No edites `research/` ni `validation/`.** Son el registro histórico de la decisión, incluidas
  sus marcas de `SIN VERIFICAR`.
- El resultado va a un archivo nuevo: `notas_investigacion/AAAA-MM-DD-<tema-en-kebab>.md`.
- Si resuelve una marca de `research/`, citá en la nota el archivo y la línea que resuelve. El
  documento original no se toca.
- Las cifras de `README.md` y `business/` no se actualizan solas: si la nota las contradice,
  avisale a Dionisio en el mensaje final.

## 5. Formato de la nota

```markdown
# <Tema>
**Fecha de consulta:** AAAA-MM-DD · **Pregunta:** <qué se quería saber>
**Resuelve:** `research/<archivo>.md:<línea>` (si aplica)

## Respuesta corta
<1-3 líneas. Si no hay fuente primaria: "SIN VERIFICAR" y por qué.>

## Hallazgos
| Afirmación | Etiqueta | Fuente (URL + artículo/página) |
|---|---|---|

## Contradicciones y huecos
<fuentes que se contradicen, qué no se encontró, qué habría que pedir (p. ej. consulta a ARCA)>

## Impacto en Veintiuno
<qué cambia para el producto u oferta, o "ninguno">
```

Citas textuales de normas: cortas y sólo el artículo que sostiene la afirmación. Cada URL tiene
que ser una que efectivamente abriste en esta sesión, no una reconstruida de memoria.

## 6. Mensaje final

Respuesta corta, ruta de la nota, marcas `SIN VERIFICAR` que quedaron resueltas o abiertas, y
contradicciones con `README.md`/`business/` si las hay. Sin commitear: sugerí el mensaje, por
ejemplo `docs(research): verificar <tema> contra fuente primaria`.
