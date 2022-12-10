import threading
import time
from loguru import logger
import requests
# --------------------------------------------------------------------------------

class LecturaDatos(threading.Thread):

  def __init__(self, device_id, apikey ):
    threading.Thread.__init__(self)
    self.isRunning  = True
    self.daemon     = True
    self.device_id  = device_id
    self.apikey     = apikey
    self.datos      = {}
    logger.add("log/hilo_lecturas_remoto.log",
                format="{time} - {level} - {function}:{line} - {message}", rotation="100 MB")
    logger.info("Hilo iniciado ")
    self.start()
        
  def stop(self):
    self.isRunning = False
      
  def run(self):
    try:
      while self.isRunning:
        direccion = "https://v2c.cloud/kong/v2c_service/device/currentstatecharge?deviceId=" + self.device_id
        payload   ={}
        headers   = {
              'apikey': self.apikey
        }
        self.datos = requests.request("POST", direccion, headers=headers, data=payload).json()
        direccion = "https://v2c.cloud/kong/v2c_service/device/reported?deviceId=" + self.device_id
        self.datos.update( requests.request("GET", direccion, headers=headers, data=payload).json() )
        time.sleep(15)
    except Exception as e:
      logger.error("Fallo en la conexion: ")
      logger.error(e)
    
  def valores( self ):
    return self.datos

# --------------------------------------------------------------------------------
