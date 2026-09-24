"""
Veintiuno · investigacion_hotel
===============================
Investigacion comercial agentica de hoteles prospecto: dado un hotel, junta lo
que se puede saber DESDE AFUERA y produce dos piezas separadas.

  1. El dossier interno  -> para decidir si vale la pena y con que angulo entrar.
  2. La estimacion de una pagina -> lo unico que se le manda al hotel.

QUE NO ES ESTO
--------------
- No es la Radiografia del 21%. La Radiografia mide sobre el export de reservas
  y la liquidacion de la pasarela; esto estima sobre senales publicas. No
  importa nada de motor_radiografia.py y no comparte nombres de campo con el.
- No es un informe fiscal, ni asesoramiento fiscal. Prepara una conversacion
  comercial. Nunca promete el resultado de una fiscalizacion.
- No es ninguno de los modulos 2, 3 y 4 del producto (legajo probatorio,
  regimen informativo mensual, cotizacion sin IVA). Esas hipotesis no estan
  validadas y la regla del proyecto es que no se construye el modulo cuya
  hipotesis no esta validada.

DATO SENSIBLE
-------------
Todo lo que produce esta libreria es sobre un hotel identificable y es material
interno. La salida va a salida_investigacion/, que esta fuera de git. Nada de
esto se comparte sin autorizacion escrita de Dionisio.
"""

__version__ = "0.1.0"
