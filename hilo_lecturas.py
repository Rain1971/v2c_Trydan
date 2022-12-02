import threading
import time
from loguru import logger
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient

# --------------------------------------------------------------------------------


class LecturaDatos(threading.Thread):

  def __init__(self, ip ):
    threading.Thread.__init__(self)
    self.isRunning = True
    self.daemon = True
    self.ip = ip
    logger.add("log/hilo_lecturas.log",
                format="{time} - {level} - {function}:{line} - {message}", rotation="100 MB")
    logger.info("Hilo iniciado ")
    self.start()
    self.datos = {'READ_ADDRESS_PWM_VALUE': 0, 'READ_ADDRESS_HOUSE_POWER': 0, 'READ_ADDRESS_FV_POWER': 0, 'READ_ADDRESS_PAUSE': 0 }
    
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

  def run(self):
      try:
        cliente = ModbusTcpClient( host=self.ip, port=502 )
        connection = cliente.connect()

        while self.isRunning:
            time.sleep(1)
            try:
              if connection:
                valor = cliente.read_holding_registers( 0x0BC7, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_PWM_VALUE'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BC8, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_HOUSE_POWER'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BC9, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_FV_POWER'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BCA, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_PAUSE'] = self.regeneraFloat( valor )
              else:
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
