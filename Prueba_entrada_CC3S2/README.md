# Sección 1

Hago uso de **make help** para obtener todos los targets del archivo makefile. Compruebo con **make tools** que tenga las dependencias necesarias.

![](imagenes/1-captura.png)

Para el caso de **pytest** voy a crear un entorno virtual e instalarlo ahí.

![](imagenes/2-captura.png)

Compruebo con **make tools** y corroboro que tengo todas las dependencias.

![](imagenes/3-captura.png)

Finalmente ejecuto **make all** y genero el directorio **/reports** juntos a los archivos .txt

![](imagenes/4-captura.png)

Los 4 archivos .txt fueron analizados y se completo las respuestas.

# Sección 2

### Seccion 2.3: Flujo Git

- **Merge Fast-Forward (FF):** Es el merge mas simple de todos, ocurre cuando fusionamos una rama que está directamente por delante de la rama destino. En lugar de crear un commit de merge, git simplemente mueve el puntero de la rama destino hacia adelante

- **Rebase:** Este comando reescribe la historia. Toma los commits de una rama y los vuelve a aplicar sobre el ultimo commit de otra rama. El resultado es también un historial lineal, como si todo el trabajo se hubiera hecho en serie

- **Cherry-pick:** Es una herramienta que nos permite copiar un único commit específico de una rama a otra. Es muy útil para aplicar un parche(hotfix) a una rama de producción sin tener que fusionar toda la rama de desarrollo que contiene otras funcionalidades que aun no se han completado

# Sección 3
