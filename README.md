# VDBauto
Solución automatizada para la gestión de vulnerabilidades mediante la iteración de reportes Nessus en formato csv.

Para ejecutar la aplicación usando Python3, instalar los modulos necesarios usando el fichero requirements.txt y ejecutar la clase interfaz_main.py

Se puede generar un ejecutable con el objetivo de no tener que instalar Python en el ordenador donde se requiera utilizar. Para ello:
- Descargar el módulo pyinstaller
- Ejecutar el siguiente comando: pyinstaller --onedir --windowed --add-data "C:\Users\<User>\AppData\Local\Programs\Python\Python311\Lib\site-packages/customtkinter;customtkinter/" interfaz_main.py
- La ruta de la flag "--add-data" puede variar de una instalación de Python a otra, para encontrar la suya propia ejecutar: pip show customtkinter, y buscar la ruta de instalación del módulo.
