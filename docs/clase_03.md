# Clase 03

### Variables Globales y Constantes
Python no tiene variables globales ni permite definir constantes. 
Una variable que se declara en mayúsculas es una variable que no debe modificarse (esto es una convención)
Buena práctica: usar `config.py` para declarar constantes y luego importarlo
Pero actualmente se usan los yaml. 
Ojo que el .yaml lo pone dentro de src y no en la carpeta principal. 
La estructura recomendada segun el LLM es que yaml y .env estén en la raíz del proyecto ya que ahí es donde las funciones buscan archivos, por default

### Por qué se usa un config.py para cargar los datos del yaml
Porque si no, tendría que cargar los datos del yaml cada vez que los necesito. De este modo puedo directamente poder `from .config import *` en el `__init__.py` dentro de src y luego dentro de main: `from src import *`

### Passwords y otros
Se crea un archivo .env que se debe agregar a gitignore para no subirlo. Ahí van las API Keys y demás. En el YAML se pueden cargar estos valores usando esta sintaxis: 
`API_KEY: ${API_KEY}` para que el YAML lo cargue desde el .env

### NOTA IMPORTANTE
Al config.py le agregué una función que lee variables de entorno: `load_dotenv()` y una función de reemplazo de variables de entorno: `replace_env_vars()`, después de haber instalado `python-dotenv`.  
Esto produce el resultado deseado pero me queda una advertencia del compilador porque el tipo no está definido a la salida de `replace_env_vars()`

![[Pasted image 20260221111601.png]]
Parece que la opción más profesional actualmente incluye el uso de pydantic, pero esto lleva un poco más de estudio. 
https://docs.pydantic.dev/2.6/concepts/pydantic_settings/ 
Lo importante es que así funciona por ahora. 

UPDATE: Lo cambié por la versión con Pydantic. Listo. 
Ahora funciona y el compilador no tira ninguna advertencia. 




