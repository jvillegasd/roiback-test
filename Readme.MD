# Prueba técnica de ROIBACK

La prueba técnica consiste en la creación de un blog usando Django, con un plazo de entrega de 8 días.
El dia de entrega es el **sabado, 16 de enero del 2021**.


## Requerimientos

-   Usar Python 2.7+ o superior
-   Si usará Django entonces 1.11+ o superior
-   La base de datos debe ser PostgreSQL
-   Debe tener Login/registro de usuarios
-   Puedo programar la fecha en que se publica y/o desactiva un post
-   Se puede dar like/unlike a los post
-   Se pueden dejar comentarios por cada post 
-   El post puede tener categorías y tags
-   Se puede filtrar por categorías, tags o autor
-   Solo usuarios autenticados pueden crear, modificar o comentar Posts
-   Un usuario solo puede modificar o eliminar sus propios posts 
-   Solo los administradores pueden eliminar o modificar posts de otros usuarios.
-   Debe estar en un repositorio Git.
-   Debe conservar un histórico de transacciones.
-   No es válido usar el admin de DJANGO
-   Se debe dejar documentación de ejecución, dependencias… etc

## Dependencias

- asgiref == 3.3.1
- Django == 3.1.5
- django-taggit == 1.3.0
- pytz == 2020.5
- sqlparse == 0.4.1
- psycopg2-binary == 2.8.6
- django-simple-history == 2.12.0

## Historial de transacciones

Para cumplir con el requerimiento de mantener un histórico de transacciones, se optó por el uso del paquete de Python "django-simple-history".

## Interfaz de usuario

La interfaz de usuario fue realizada con los templates de Django en conjunto con Bootstrap 4. Los archivos CSS usados para mantener un diseño de los componentes visuales, se encuentra guardades en la carpeta `static/blog` de la aplicación.

## Ejecutar proyecto

El proyecto se encuentra dockerizado, por lo cual no hay porque preocuparse por las dependencias del proyecto y del sistema operativo. Para correr el proyecto, ejecute la siguiente linea de comando en su terminal:
`docker-compose up -d --build`.

## Entrypoint y Dockerfile

El archivo Dockerfile que representa la imagen Docker, se encuentra dentro de la carpeta del proyecto `mysite`. Para evitar de que se tengan que realizar las migraciones de la base de datos de manera manual, este proceso se encuentra automatizado por medio de la creación de un script bash que funciona como entrypoint del container, este archivo lo pueden encontrar en `mysite/entrypoint.sh`.