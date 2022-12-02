from hilo_lecturas import LecturaDatos
import time

# --------------------- DATOS SISTEMA ------------------------------------
IP_V2C = "10.48.130.141"
# ------------------------------------------------------------------------

datosV2C = LecturaDatos( IP_V2C )

while True:
  time.sleep(5)
  datos = datosV2C.valores()
  
  print( 'READ_ADDRESS_PWM_VALUE: {}'.format( datos['READ_ADDRESS_PWM_VALUE'] ) )
  print( 'READ_ADDRESS_HOUSE_POWER: {}'.format( datos['READ_ADDRESS_HOUSE_POWER'] ) )
  print( 'READ_ADDRESS_FV_POWER: {}'.format( datos['READ_ADDRESS_FV_POWER'] ) )
  print( 'READ_ADDRESS_PAUSE: {}'.format( datos['READ_ADDRESS_PAUSE'] ) )


