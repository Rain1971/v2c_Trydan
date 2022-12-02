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
    self.datos = {'READ_ADDRESS_CHARGE_STATE': 0, 'READ_ADDRESS_CHARGE_POWER': 0, 'READ_ADDRESS_CHARGE_ENERGY': 0, 
                  'READ_ADDRESS_SLAVE_ERROR': 0, 'READ_ADDRESS_CHARGE_TIME': 0, 'READ_ADDRESS_PWM_VALUE': 0, 
                  'READ_ADDRESS_HOUSE_POWER': 0, 'READ_ADDRESS_FV_POWER': 0, 'READ_ADDRESS_PAUSE': 0,
                  'READ_ADDRESS_LOCK': 0, 'READ_ADDRESS_PROMGRAM': 0, 'READ_ADDRESS_INTENSITY': 0,
                  'READ_ADDRESS_DYNAMIC': 0, 'READ_ADDRESS_PAYMENT': 0, 'READ_ADDRESS_OCPP': 0, 
                  'WRITE_ADDRESS_MIN_INTENSITY': 0, 'WRITE_ADDRESS_MAX_INTENSITY': 0}
    
    self.dirs  = {'READ_ADDRESS_CHARGE_STATE': 0x0BC2, 'READ_ADDRESS_CHARGE_POWER': 0x0BC3, 'READ_ADDRESS_CHARGE_ENERGY': 0x0BC4, 
                  'READ_ADDRESS_SLAVE_ERROR': 0x0BC5, 'READ_ADDRESS_CHARGE_TIME': 0x0BC6, 'READ_ADDRESS_PWM_VALUE': 0x0BC7, 
                  'READ_ADDRESS_HOUSE_POWER': 0x0BC8, 'READ_ADDRESS_FV_POWER': 0x0BC9, 'READ_ADDRESS_PAUSE': 0x0BCA,
                  'READ_ADDRESS_LOCK': 0x0BCB, 'READ_ADDRESS_PROMGRAM': 0x0BCC, 'READ_ADDRESS_INTENSITY': 0x0BCD,
                  'READ_ADDRESS_DYNAMIC': 0x0BCE, 'READ_ADDRESS_PAYMENT': 0x0BCF, 'READ_ADDRESS_OCPP': 0x0BD0,
                  'READ_ADDRESS_MIN_INTENSITY': 0x0BD1, 'WRITE_ADDRESS_MAX_INTENSITY': 0x0BD2}
        
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
                for direccion in list( self.dirs ):
                  valor = cliente.read_holding_registers( self.dirs[direccion], 2, unit=1 )
                  if valor:
                    self.datos[direccion] = self.regeneraFloat( valor )
                  
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
