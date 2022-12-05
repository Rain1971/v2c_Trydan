from hilo_lecturas import LecturaDatos
from flask import Flask

app = Flask(__name__)

# --------------------- DATOS SISTEMA ------------------------------------
IP_V2C              = '10.48.130.141'
CONTROLV2C_HOSTNAME = '0.0.0.0'
CONTROLV2C_PORT     = 5002
CONTROLV2C_DEBUG    = True
# ------------------------------------------------------------------------


datosV2C = LecturaDatos( IP_V2C )

@app.route('/estado')
def estado():
  datos   = datosV2C.valores()
  cadena  = ""
  for parametro in list( datos ):
    cadena += '<p> {}: {} </p>'.format( parametro, datos[parametro] )
  return cadena

@app.route('/')
def inicio():
    return 'Control de estado para cargador V2C!'

if __name__ == "__main__":

  app.run( host = CONTROLV2C_HOSTNAME, 
           port = CONTROLV2C_PORT, 
           threaded = False,
           debug = CONTROLV2C_DEBUG )
