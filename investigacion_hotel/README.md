# `investigacion_hotel` — investigación comercial de hoteles prospecto

Dado un hotel, junta lo que se puede saber **desde afuera** y produce dos piezas
**separadas a propósito**:

| Archivo | Para quién | Qué lleva |
|---|---|---|
| `dossier.md` | interno, sólo Veintiuno | todo: puntaje ICP, decisor, competencia, objeción esperada |
| `estimacion_preliminar.md` | **es lo único que ve el hotel** | observaciones públicas sobre él, el régimen y el rango estimado |
| `dossier.json` | interno | el mismo dossier, editable a mano, para `--rehacer` |

Es la capa de **pre-venta**: prepara la conversación que termina en una Radiografía
del 21%. No la reemplaza ni la anticipa.

## Qué NO es

- **No es la Radiografía.** La Radiografía mide estadía por estadía sobre el export
  del hotel y resuelve el país emisor de la tarjeta por BIN. Esto estima sobre señales
  públicas, donde **el BIN es invisible**. No importa nada de `motor_radiografia.py` y
  usa nombres de campo distintos (`rango_iva_mensual_estimado_ars`, nunca `iva_en_juego`)
  para que no se puedan confundir.
- **No es un informe fiscal** ni asesoramiento fiscal. Nunca promete el resultado de
  una fiscalización.
- **No construye** legajo probatorio, régimen informativo ni cotización sin IVA. Esas
  hipótesis no están validadas, y la regla del proyecto es que no se construye el
  módulo cuya hipótesis no está validada.

## Instalación

Una sola dependencia. El motor de la Radiografía **sigue siendo stdlib puro**: esta
librería es la única que suma algo.

```bash
pip3 install -r investigacion_hotel/requirements.txt
```

El acceso HTTP y el parseo de HTML son de librería estándar (`urllib`, `html.parser`):
no hay `requests` ni `bs4`, porque son pocos GET simples y un puñado de huellas por
regex.

## Uso

```bash
python3 -m investigacion_hotel --nombre "Hotel X" --ciudad "Buenos Aires" --externo
```

| Flag | Para qué |
|---|---|
| `--offline` | Corre el pipeline entero contra fixtures. Sin red, sin API, **sin costo**. No necesita clave. |
| `--rehacer DIR` | Rehace los documentos desde un `dossier.json` ya guardado, sin llamar a la API. |
| `--externo` | Genera también la estimación de una página que se le manda al hotel. |
| `--sitio URL` | Si ya conocés el sitio, le ahorrás una búsqueda. |
| `--max-busquedas N` / `--max-fetches N` | Topes de la corrida (default 8 y 12). |
| `--esfuerzo low\|medium\|high` | Esfuerzo del modelo (default `medium`). |
| `--padron archivo.csv` | Usa tu copia del padrón en vez de bajarlo, igual que `--bin-map` en el motor. |

Variables de entorno: `ANTHROPIC_API_KEY` (obligatoria salvo `--offline`) y
`GOOGLE_PLACES_API_KEY` (opcional: habilita la herramienta de Places).

## La regla que ordena todo

**El LLM no escribe el dossier.** Registra hallazgos con fuente; Python arma el
documento, calcula el puntaje y la estimación.

Cada hallazgo del modelo necesita una URL y una **cita textual que el código va a
buscar en esa página**. Si la cita no aparece, el dato queda `SIN VERIFICAR`, **suma
cero al puntaje** y se abre una verificación pendiente. Así "no inventar cifras" deja
de ser una instrucción de prompt (que se puede desobedecer) y pasa a ser una propiedad
del tipo de dato.

La excepción es lo que observa el propio código —el padrón, Places, las huellas del
sitio—: eso se registra vía `Investigacion.observar()` y va marcado *"observado por la
herramienta, no afirmado por el modelo"*. Pedirle una cita textual a una respuesta JSON
no agregaría garantía; sólo perdería el dato.

## Cerrar las verificaciones pendientes

El dossier termina con una lista de lo que no se pudo cerrar solo, **con la URL exacta
y la pregunta concreta**. Booking y TripAdvisor bloquean lectura automática, así que
ahí casi siempre queda algo. Se cierra a mano:

1. Abrís la URL que dice el dossier y mirás.
2. Editás ese hallazgo en `dossier.json` (`estado: "verificado"`, la fuente y la cita).
3. `python3 -m investigacion_hotel --rehacer <carpeta>` — sin costo.

El veredicto y la estimación se recalculan solos. Es habitual que el hotel pase de
`indeterminado` a Lista A con ese solo dato: el idioma de las reseñas vale 20 de los
100 puntos y destraba la estimación.

## Qué sale y qué no sale

`salida_investigacion/` y `.cache_investigacion/` están en `.gitignore`. Los datos de
un prospecto real **no entran al repo**: los fixtures son de un hotel inventado.

El renderer externo sólo puede leer campos marcados `publico=True` en `modelo.CAMPOS`.
Pedirle cualquier otro **levanta `CampoNoPublico`**: no hay una segunda lista que se
pueda desincronizar de la primera, y hay un test que mete centinelas en los campos
internos y verifica que no aparezcan en el material que ve el hotel.

## Verificación

```bash
python3 -m unittest discover -s investigacion_hotel/tests -t .
```

112 tests, librería estándar, sin red. Los que importan:

- `test_scoring.py` — las 8 preguntas de `business/ideal-customer.md`, incluida la regla
  dura que descarta aunque sume 60.
- `test_estimacion.py` — que se niegue a emitir número cuando falta un insumo, y la
  calibración contra la corrida real del motor sobre el dataset de la demo.
- `test_render.py` — que ningún dato salga sin fuente, y que nada interno se filtre al
  material externo.
- `test_agente.py` — que una cita inventada no entre como dato, y que agotar el
  presupuesto devuelva un dossier corto en vez de una excepción.

Para ver la salida sin gastar nada:

```bash
python3 -m investigacion_hotel --offline --externo
```

## Límites conocidos

- **Fuera de CABA corre degradado**: el padrón abierto sólo cubre la Ciudad. El dossier
  lo avisa en el encabezado.
- **Places devuelve hasta 5 reseñas, no 30.** El tamaño de muestra viaja siempre pegado
  al porcentaje, y queda una verificación pendiente igual.
- **El costo por corrida todavía no está medido.** Los topes por default (8 búsquedas,
  12 lecturas) son un punto de partida, no un número calibrado.
