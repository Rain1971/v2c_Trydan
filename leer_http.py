import requests
import re
from sistema import IP_V2C
import json

# Hacemos la solicitud HTTP a la página web
response = requests.get('http://' + IP_V2C + '/RealTimeData')

# Comprobamos que la solicitud se haya realizado correctamente
if response.status_code == 200:
    # Obtenemos el contenido de la respuesta en formato JSON
    #datos = response.json()
    
    # Obtenemos el contenido de la respuesta en formato de cadena y eliminamos los "
    # HACK reparo pequeño gazapo en la cadena
    datos_string = re.sub(r':"', ':', response.text)
    
    # Convierto a json
    datos = json.loads( datos_string )

    if len( datos ) == 17:     
      # Mostramos el contenido del diccionario
      print(datos)
    else:
      print("ERROR de lectura")
else:
    print('Error al obtener los datos')