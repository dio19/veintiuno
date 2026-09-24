# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repo

**Veintiuno**: micro-SaaS para hoteles argentinos que detecta la fuga de IVA en el régimen de
exención a huéspedes no residentes. No es un repo de producto — es el expediente de un ejercicio
de validación de negocio (investigación → red team → decisión → oferta), con **una sola pieza de
código que corre**: el motor de la Radiografía del 21%.

Todo el contenido está en castellano rioplatense (voseo). Escribí en ese registro: documentos,
comentarios de código y mensajes al usuario.

Repositorio git, rama `main`. No tiene remoto configurado.

## Git

**Nunca commitees.** Los commits los hace Dionisio, siempre, aunque el cambio sea trivial, aunque
el árbol quede sucio al terminar la tarea y aunque él haya pedido el cambio explícitamente. Pedir
permiso para commitear tampoco corresponde: dejá el trabajo en el working tree y listo. Lo mismo
vale para `git push`, `git reset --hard`, `git checkout` sobre archivos modificados y cualquier
otra cosa que reescriba historial o descarte cambios.

Al terminar un cambio, **recomendale el mensaje de commit** en formato
[Conventional Commits](https://www.conventionalcommits.org/), en un bloque de código para que lo
copie:

```
<tipo>(<alcance opcional>): <descripción en imperativo, minúscula, sin punto final>

<cuerpo opcional: el porqué, no el qué>
```

Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `perf`, `style`, `build`, `ci`.
Alcances habituales de este repo: `motor`, `skill`, `demo`, `business`, `research`.
Un cambio que rompe compatibilidad lleva `!` antes de los dos puntos.

## Comandos

Python 3, sólo librería estándar. No hay build, ni linter, ni suite de tests.

Ambos scripts viven en el skill; se corren desde la raíz del repo.

Regenerar el dataset sintético de la demo:

```bash
python3 .claude/skills/radiografia-21/references/generar_datos_demo.py --salida demo/datos
```

Correr el motor sobre ese dataset:

```bash
python3 .claude/skills/radiografia-21/scripts/motor_radiografia.py --reservas demo/datos/reservas.csv --liquidacion demo/datos/liquidacion.csv --hotel "Demo Recoleta 42" --salida demo/salida --demo
```

El generador usa semilla fija (`SEED = 21`): la misma corrida da siempre el mismo dataset, así que
el cambio en `detalle_estadias.csv` es la forma de verificar que una modificación al motor no alteró
la clasificación. Comparalo con `diff` contra la salida anterior antes de dar por buena una edición.

`--demo` es lo único que cambia el aviso de `radiografia.json`. **El default es datos reales**: sin
el flag, la salida se marca como confidencial. Nunca lo pases por costumbre.

`--bin-map archivo.csv` (columnas `bin,pais`) reemplaza la tabla BIN ilustrativa. Esa es la vía para
usar un proveedor real de BIN — no editar `BIN_PAIS` adentro del script.

`--anonimizar` reemplaza el nombre del huésped por un seudónimo estable en `detalle_estadias.csv`.
Ese archivo arrastra las columnas del export: con datos reales es una lista nominada de pasajeros
extranjeros con su situación documental. Va anonimizada en cualquier copia que salga del hotel.

## Arquitectura

El motor es un pipeline de un solo paso, sin estado ni dependencias:

```
reservas.csv (PMS) ─┐
                    ├─→ evaluar() por estadía ─→ radiografia.json (KPIs + cortes)
liquidacion.csv ────┘        + tabla BIN          detalle_estadias.csv (estado + motivo)
  (pasarela)
```

Las dos entradas se cruzan por `reserva_id`; la liquidación sólo aporta el `bin` que resuelve el
país emisor del plástico.

**`evaluar()` en `.claude/skills/radiografia-21/scripts/motor_radiografia.py` es la única fuente
de verdad de la regla de negocio.**
Aplica las tres condiciones del régimen y devuelve `(estado, motivo, neto, iva_en_juego)`. Todo lo
demás en el archivo es agregación y formato. Cualquier cambio de criterio de clasificación pasa por
esa función y por ninguna otra.

**No vuelvas a duplicar el motor.** Hubo copias en `demo/motor/` y un `skill.md` en la raíz; se
borraron justamente porque divergen. El código vive sólo en `.claude/skills/radiografia-21/`
(`scripts/` el motor, `references/` el generador) y `demo/` quedó con los datos, la salida y el
informe HTML.

Existe un skill de proyecto, `radiografia-21`, que encapsula estas reglas para correr radiografías
de hoteles reales. Si vas a cambiar el criterio de clasificación, la CLI o las columnas esperadas,
actualizá también `.claude/skills/radiografia-21/SKILL.md`: es lo que otra sesión va a leer.

### Los cinco estados

`correcto` · `fuga` · `riesgo_legajo` · `revisar` · `no_elegible`, cada uno con su motivo en texto.
`revisar` (BIN no reconocido) **nunca se colapsa** dentro de `fuga` ni de `correcto` para redondear
el informe: decir "esto no se pudo clasificar" es parte del producto.

### La cadena documental

`research/` (cinco especialistas) → `research/00-sintesis-lead-agent.md` → `validation/` (red team y
decisión) → `business/` (la oferta) → `demo/` (la muestra). Es un registro histórico de una decisión,
no documentación viva: el red team **mató** la idea original ("Pulso", copiloto de tarifas) y la
decisión tomó la segunda opción. No reintroduzcas Pulso como si siguiera en pie, y no edites los
documentos de research/validation para que concuerden con el estado actual — ahí está justamente el
razonamiento que llevó al pivot.

Las cifras de `README.md` y `demo/README.md` son la salida de una corrida concreta del motor. Si
cambiás el cálculo, esos números quedan desactualizados: revisalos o avisá. (Hoy hay una diferencia
conocida: el README cita ARS 15.490.336 anualizados, calculados sobre 90 días fijos; el motor ahora
deriva la ventana de las fechas y da 15.320.113.)

## Reglas de dominio que no se reinterpretan

- **Marco aplicable**: RG Conjunta 3971/2016 (AFIP/ARCA) + Res. 566/2016 (MinTur). Tres condiciones
  simultáneas: no residente, pago con tarjeta emitida en el exterior o transferencia del exterior, y
  sólo alojamiento + desayuno incluido. Comprobante: factura clase T.
- **No confundir con la RG 5843/2026** (tax free minorista de bienes, factura B): es otro régimen.
  La distinción es parte del valor del producto; equivocarla lo invalida.
- **El pago local no habilita**, sin excepción ni documentación de respaldo que lo salve.
- **No damos asesoramiento fiscal.** El producto prepara y prueba; el contador del hotel firma.
  Nunca prometas el resultado de una fiscalización.
- **Convención `SIN VERIFICAR`**: toda afirmación normativa o cifra de mercado sin fuente primaria
  se marca con ese literal en vez de completarse por analogía. Se usa en todo `research/`.
- **Quitar el IVA de un precio final es −17,36%** (1 − 1/1,21), no −21%.
- **No se construye el módulo cuya hipótesis no está validada.** De los cuatro módulos del producto,
  sólo el detector de fuga (módulo 1) tiene código. Si te piden construir legajo probatorio, régimen
  informativo o cotización sin IVA, recordá la regla y proponé el test que resuelve la hipótesis
  antes de escribir código.
- **Datos de hoteles reales son confidenciales**: ni el nombre del establecimiento ni sus cifras van
  a material público sin permiso escrito, y el detalle por estadía sale anonimizado (`--anonimizar`)
  si va a salir del hotel.
