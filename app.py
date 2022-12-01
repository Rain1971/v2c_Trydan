from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client import ModbusTcpClient


# --------------------- DATOS SISTEMA ------------------------------------
IP_V2C = "10.48.130.141"
# ------------------------------------------------------------------------

def regeneraFloat( lectura ):
    if not lectura.isError():
        decoder = BinaryPayloadDecoder.fromRegisters(
            lectura.registers,
            byteorder=Endian.Big, wordorder=Endian.Big
        )   
        return float('{0:.0f}'.format(decoder.decode_32bit_float()))
    else:
        return None

cliente = ModbusTcpClient( host=IP_V2C, port=502 )
connection = cliente.connect()

if connection:
  valor = cliente.read_holding_registers( 0x0BC7, 2, unit=1 )
  if valor:
    READ_ADDRESS_PWM_VALUE = regeneraFloat( valor )
    print( 'READ_ADDRESS_PWM_VALUE: {}'.format(int(READ_ADDRESS_PWM_VALUE)) )

  valor = cliente.read_holding_registers( 0x0BC8, 2, unit=1 )
  if valor:
    READ_ADDRESS_HOUSE_POWER = regeneraFloat( valor )
    print( 'READ_ADDRESS_HOUSE_POWER: {}'.format(int(READ_ADDRESS_HOUSE_POWER)) )

  valor = cliente.read_holding_registers( 0x0BC9, 2, unit=1 )
  if valor:
    READ_ADDRESS_FV_POWER = regeneraFloat( valor )
    print( 'READ_ADDRESS_FV_POWER: {}'.format(int(READ_ADDRESS_FV_POWER)) )

  valor = cliente.read_holding_registers( 0x0BCA, 2, unit=1 )
  if valor:
    READ_ADDRESS_PAUSE = regeneraFloat( valor )
    print( 'READ_ADDRESS_PAUSE: {}'.format(int(READ_ADDRESS_PAUSE)) )


