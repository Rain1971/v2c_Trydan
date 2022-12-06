import threading
import time
from loguru import logger
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient
from pymodbus.constants import Defaults

# --------------------------------------------------------------------------------


class LecturaDatos(threading.Thread):

  def __init__(self, ip ):
    threading.Thread.__init__(self)
    self.isRunning = True
    self.daemon = True
    self.ip = ip
    Defaults.Timeout = 10
    logger.add("log/hilo_lecturas.log",
                format="{time} - {level} - {function}:{line} - {message}", rotation="100 MB")
    logger.info("Hilo iniciado ")
    self.start()
    self.datos = {'READ_ADDRESS_CHARGE_STATE': 0, 'READ_ADDRESS_CHARGE_POWER': 0, 'READ_ADDRESS_CHARGE_ENERGY': 0, 
                  'READ_ADDRESS_SLAVE_ERROR': 0, 'READ_ADDRESS_CHARGE_TIME': 0, 'READ_ADDRESS_PWM_VALUE': 0, 
                  'READ_ADDRESS_HOUSE_POWER': 0, 'READ_ADDRESS_FV_POWER': 0, 'READ_ADDRESS_PAUSE': 0,
                  'READ_ADDRESS_LOCK': 0, 'READ_ADDRESS_PROMGRAM': 0, 'READ_ADDRESS_INTENSITY': 0,
                  'READ_ADDRESS_DYNAMIC': 0, 'READ_ADDRESS_PAYMENT': 0, 'READ_ADDRESS_OCPP': 0, 
                  'READ_ADDRESS_MIN_INTENSITY': 0, 'READ_ADDRESS_MAX_INTENSITY': 0}
        
  def stop(self):
    self.isRunning = False
      
  def regeneraFloat( self, lectura ):
    if not lectura.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            lectura.registers,
            byteorder=Endian.Big, wordorder=Endian.Big
        )   
        return float('{0:.0f}'.format(decoder.decode_32bit_float()))
    else:
        return None

  def divide(self, lista, num):
    out = []
    ultimo = 0.0

    while ultimo < len(lista):
        out.append(lista[int(ultimo):int(ultimo + num)])
        ultimo += num
    return out

  def run(self):
    try:
      with ModbusTcpClient( host=self.ip, port=502, timeout=10 ) as cliente:
        connection = cliente.connect()
        time.sleep(2)
        while self.isRunning:       
          try:
            if connection:
              distancia = len( self.datos ) * 2
              valor = cliente.read_holding_registers( 0x0BC2, distancia, unit=1 )
              time.sleep(2)
              if len(valor.registers) == distancia:
                lista = self.divide( valor.registers, 2 )
                posicion = 0
                for direccion in list( self.datos ):
                  valor.registers = lista[posicion]
                  self.datos[direccion] = self.regeneraFloat( valor )
                  posicion += 1
              else:
                logger.error("No hay recepcion de datos ")  
            else:
              logger.error("Conexion perdida con V2C ")
              cliente = ModbusTcpClient( host=self.ip, port=502 )
              connection = cliente.connect()
          except Exception as e:
              logger.error("Error en captura de datos: ")
              logger.error(e)
    except Exception as e:
      logger.error("Fallo en la conexion: ")
      logger.error(e)
    
  def valores( self ):
    return self.datos

# --------------------------------------------------------------------------------
