from hilo_lecturas import LecturaDatos
import time

# --------------------- DATOS SISTEMA ------------------------------------
IP_V2C = "10.48.130.141"
# ------------------------------------------------------------------------

datosV2C = LecturaDatos( IP_V2C )

while True:
  time.sleep(5)
  datos = datosV2C.valores()
  for parametro in list( datos ):
    print( '{}: {}'.format( parametro, datos[parametro] ) )


