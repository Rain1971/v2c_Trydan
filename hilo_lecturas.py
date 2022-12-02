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
                  'READ_ADDRESS_DYNAMIC': 0, 'READ_ADDRESS_PAYMENT': 0, 'READ_ADDRESS_OCPP': 0}
    
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
                valor = cliente.read_holding_registers( 0x0BC2, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_CHARGE_STATE'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BC3, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_CHARGE_POWER'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BC4, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_CHARGE_ENERGY'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BC5, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_SLAVE_ERROR'] = self.regeneraFloat( valor )                
                valor = cliente.read_holding_registers( 0x0BC6, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_CHARGE_TIME'] = self.regeneraFloat( valor )                
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

                valor = cliente.read_holding_registers( 0x0BCB, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_LOCK'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BCC, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_PROMGRAM'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BCD, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_INTENSITY'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BCE, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_DYNAMIC'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BCF, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_PAYMENT'] = self.regeneraFloat( valor )
                valor = cliente.read_holding_registers( 0x0BD0, 2, unit=1 )
                if valor:
                  self.datos['READ_ADDRESS_OCPP'] = self.regeneraFloat( valor )                  
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
