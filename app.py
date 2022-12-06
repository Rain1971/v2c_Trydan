from hilo_lecturas import LecturaDatos
from flask import Flask

app = Flask(__name__)

# --------------------- DATOS SISTEMA ------------------------------------
IP_V2C              = '10.48.130.141'
CONTROLV2C_HOSTNAME = '0.0.0.0'
CONTROLV2C_PORT     = 5002
CONTROLV2C_DEBUG    = True
# ------------------------------------------------------------------------

datosV2C = None

@app.route('/estado')
def estado():
  global datosV2C
  if datosV2C is not None:
    datos   = datosV2C.valores()
    cadena  = ""
    for parametro in list( datos ):
      cadena += '<p> {}: {} </p>'.format( parametro, datos[parametro] )
    return cadena
  else:
    datosV2C = LecturaDatos( IP_V2C )
    return "No inicializado, refresca la página en unos segundos"

@app.route('/')
def inicio():
  global datosV2C 
  if datosV2C is None:
    datosV2C = LecturaDatos( IP_V2C )
  return 'Control de estado para cargador V2C!'


if __name__ == "__main__":
  app.run( host = CONTROLV2C_HOSTNAME, 
           port = CONTROLV2C_PORT, 
           threaded = True,
           debug = CONTROLV2C_DEBUG )
