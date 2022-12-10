from hilo_lecturas_remotas import LecturaDatos
from flask import Flask
from flask import jsonify
from sistema import DEVICE_ID, APIKEY

# --------------------- DATOS SISTEMA ------------------------------------
CONTROLV2C_HOSTNAME = '0.0.0.0'
CONTROLV2C_PORT     = 5002
CONTROLV2C_DEBUG    = False
# ------------------------------------------------------------------------

app = Flask(__name__)

datosV2C = LecturaDatos( DEVICE_ID, APIKEY )

@app.route('/estado')
def estado():
  datos   = datosV2C.valores()
  cadena  = ""
  for parametro in list( datos ):
    cadena += '<p> {}: {} </p>'.format( parametro, datos[parametro] )
  return cadena

@app.route('/json_estado')
def json_estado():
  datos   = datosV2C.valores()
  return jsonify(datos)

@app.route('/')
def inicio():
  return 'Control de estado para cargador V2C!'


if __name__ == "__main__":
  app.run( host = CONTROLV2C_HOSTNAME, 
           port = CONTROLV2C_PORT, 
           threaded = True,
           debug = CONTROLV2C_DEBUG )
