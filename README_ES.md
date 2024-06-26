# TusDatos App  - Prueba Tecnica Desarrollador Backend

## Introducción
En la implementación realizada se desarrollaron dos objetivos:

1. Extraer datos de la página [Función Judicial Ecuador - Búsqueda Avanzada de Procesos Judiciales](https://procesosjudiciales.funcionjudicial.gob.ec/expel-busqueda-avanzada) utilizando web scraping, para posteriormente crear una base de datos.
   
2. Se habilitó una API utilizando FastAPI para acceder a los datos.

## Detalles de Implementación

1. **Extracción de Datos:**
   Inicialmente, se realizó un desarrollo para acceder a la plataforma. Utilizando WebDriver de Selenium, se automatizó la navegación por la plataforma para acceder a cada uno de los lugares donde se visualizan los datos a extraer. Posteriormente, se capturaron los datos y se les dio un formato para ser almacenados con una estructura definida en un archivo JSON.

1. **Notas del Almacenamiento:**
    Ademas de estructurar el Json con los datos obtenido de la Web, se le agregaron 2 propiedades las cuales son:
        - `documento` : Donde se almacena el documento por el cual se realizó la consulta
        - `tipo` : Hace referencia al filtro por el cual se consulto ej: actor/ofendido (plantiff) || demandado/procesado (defendant)
   
2. **API:**
   Se desarrollaron endpoints para listar y buscar los datos almacenados en el paso anterior. Además, se creó un endpoint para el inicio de sesión y autenticación, necesario para acceder a los datos previamente mencionados. Estos endpoints son los siguientes:
   
   - **Autenticación:**
     ```
     URL: ${HOST}/api/login
     Parámetros:
         - username: Nombre de usuario a validar (Ejemplo: Mauricio Carmona)
         - email: Email del usuario, debe ser un email válido ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
     Respuesta: Entrega un token de autenticación
     ```

   - **Listar Todo:**
     ```
     URL: ${HOST}/api/process
     Cabecera:
         Authorization: Token de autenticación
     Parámetros:
         - offset: Posición de inicio a listar
         - limit: Cantidad de objetos a obtener
     Respuesta: Entrega una lista de objetos aplicando paginación
     ```

   - **Buscar Uno:**
     ```
     URL: ${HOST}/api/process/{id}
     Cabecera:
         Authorization: Token de autenticación
     Respuesta: Entrega un objeto específico filtrado por su propiedad ID
     ```
* NOTA: Para ejecutar estos endpoints, sigue estos pasos (todos responden después de iniciar la aplicación):
    * Accede a la documentación generada por FastAPI [Docs](http://localhost:8000/docs)
    * Utiliza la colección de Postman llamada TusDatos.postman_collection.json

## Extraccion de datos
1. Para la extraccion de datos ejecutamos el siguiente comando en consola:
    ```
    python .\src\scrapper\main.py
    ```
## Configuración

1. Iniciamos habilitando un entorno virtual para nuestro proyecto con el siguiente comando:

    ```
    python -m virtualenv venv
    ```

2. Activamos el entorno:

    ```
    .\venv\Scripts\activate
    ```

3. Instalamos las dependencias necesarias:

    ```
    pip install -r requirements.txt
    ```

4. Ponemos a correr nuestra aplicación, en este caso, nuestra API:

    ```
    python .\src\api\main.py
    ```
  
## Test
* Para ejecutar las pruebas, ejecuta el siguiente comando:
    ```
    pytest -v 
    ```
