from hilo_lecturas_http import LecturaDatos
from flask import Flask
from flask import jsonify
from sistema import IP_V2C

app = Flask(__name__)

# --------------------- DATOS SISTEMA ------------------------------------
CONTROLV2C_HOSTNAME = '0.0.0.0'
CONTROLV2C_PORT     = 5002
CONTROLV2C_DEBUG    = False
# ------------------------------------------------------------------------

datosV2C = LecturaDatos( IP_V2C )

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
