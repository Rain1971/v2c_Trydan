# V2C trydan Modbus TCP
## Índice

- [Acerca de](#about)
- [Como empezar](#getting_started)
- [Uso](#usage)

## Acerca de <a name = "about"></a>

Pretendo tener control del cargador V2C trydan para hacer un mejor control de excedentes en mi instalación.

## Como empezar <a name = "getting_started"></a>

Estas instruccines pretenden ser una pequeña ayuda. Mira [instalar](#instalar) Para ver como iniciar.

### Prerequisitos

Necesitas tener git, python3, source, venv y pip.

### Instalar <a name = "deployment"></a>

<p>git clone https://github.com/Rain1971/v2c_Trydan.git</p>
<p>cd v2c_Trydan</p>
<p>python3 -m venv venv</p>
<p>source venv/bin/activate</p>
<p>pip3 install -r requirements.txt</p>

## Uso <a name = "usage"></a>

<p>python3 app.py</p>
<p>Se accede a los valores desde un navegador con direcciones:</p>
      <p>http://ip:5002/json_estado  <- Retorna un json con los valores actuales</p>
      <p>http://ip:5002/estado       <- Retorna web simple con los valores actuales</p>
