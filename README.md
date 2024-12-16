# Como ejecutar EnSort
---
La GUI que usa EnSort fue construida en Flet, un framework de Python creado para el desarrollo facíl y práctico de distintas aplicaciones multiplataforma, en este estado de desarrollo, para poder usar EnSort debe:

1. Crear y activar el entorno virtual de Python 

- **En Linux/macOS:**

   ```bash
   python3 -m venv scp-env
   source scp-env/bin/activate
   ```

- **En Windows:**

   ```powershell
   python -m venv scp-env
   scp-env\Scripts\activate
   ```
   
 2. Instalar flet
Usuarios de Linux:
Es necesario instalar varias librerías adicionales para hacer funcionar Flet. Consulte la [documentación oficial de Flet](https://flet.dev/docs/publish/linux/#prerequisites) para más detalles.
 
     ```
    pip install flet
    ```

Finalmente ejecute el archivo **main.py** desde el entorno virtual, eso debería ser suficiente para usar EnSort, si quiere conocer un poco más de los archivos en el código fuente es recomedable ver el vídeo.
