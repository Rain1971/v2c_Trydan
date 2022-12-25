import threading
import time
from loguru import logger
import requests
import re
import json
# --------------------------------------------------------------------------------

class LecturaDatos(threading.Thread):

  def __init__(self, IP_V2C ):
    threading.Thread.__init__(self)
    self.isRunning  = True
    self.daemon     = True
    self.datos      = {}
    self.IP_V2C     = IP_V2C
    logger.add("log/hilo_lecturas_remoto.log",
                format="{time} - {level} - {function}:{line} - {message}", rotation="100 MB")
    logger.info("Hilo iniciado ")
    self.start()
        
  def stop(self):
    self.isRunning = False
      
  def run(self):
    try:
      while self.isRunning:
        direccion = 'http://' + self.IP_V2C + '/RealTimeData'
        payload   ={}
        headers   = {}
        response = requests.get( direccion )
        if response.status_code == 200:
          # HACK reparo pequeño gazapo en la cadena
          datos_string = re.sub(r':"', ':', response.text)
          self.datos = json.loads( datos_string )
        time.sleep( 2 )
    except Exception as e:
      logger.error("Fallo en la conexion: ")
      logger.error(e)
    
  def valores( self ):
    return self.datos

# --------------------------------------------------------------------------------
