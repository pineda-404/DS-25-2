# Actividad 13: Infraestructura como Código con Terraform

---

## El Propósito del Proyecto

- Automatizar la generación de configuraciones de Terraform a partir de plantillas base.
- Analizar y gestionar el "drift" (desviación de la configuración) en la infraestructura.
- Desarrollar un proceso para migrar sistemas preexistentes (legacy) a una gestión basada en IaC.
- Implementar buenas prácticas de codificación, como la parametrización, la gestión de secretos y la nomenclatura consistente de recursos.

## Estructura del Proyecto

El repositorio está organizado de la siguiente manera:

```
├── README.md
├── environments
│   ├── app1
│   │   ├── main.tf.json
│   │   ├── network.tf.json
│   │   ├── terraform.tfstate
│   │   ├── terraform.tfstate.backup
│   │   └── terraform.tfvars.json
│   ├── app2
│   │   ├── main.tf.json
│   │   ├── network.tf.json
│   │   ├── terraform.tfstate
│   │   ├── terraform.tfstate.backup
│   │   └── terraform.tfvars.json
│   ├── env3
│   │   ├── main.tf.json
│   │   ├── network.tf.json
│   │   └── terraform.tfvars.json
│   ├── staging1
│   │   ├── main.tf.json
│   │   ├── network.tf.json
│   │   └── terraform.tfvars.json
│   ├── staging2
│   │   ├── main.tf.json
│   │   ├── network.tf.json
│   │   └── terraform.tfvars.json
│   └── staging3
│   ├── main.tf.json
│   ├── network.tf.json
│   └── terraform.tfvars.json
├── generate_envs.py
├── legacy
│   ├── config.cfg
│   └── run.sh
├── migrate_legacy.py
├── migrated_env
│   ├── main.tf.json
│   ├── network.tf.json
│   └── terraform.tfstate
├── modules
│   └── simulated_app
│   ├── main.tf.json
│   └── network.tf.json
└── requirements.txt

```

_Nota: Los archivos presentes en la estructura que no seran versionados son: terraform.tfstate, terraform.tfstate.backup y terraform.tfvars.json ._

## Guía de Inicio

Para replicar el proyecto, se requieren las siguientes herramientas:

- Python 3
- Terraform
- `jq`

**Pasos para la ejecución:**

1.  **Configuración del Entorno de Python:**
    Se recomienda utilizar un entorno virtual para gestionar las dependencias del proyecto.

    ```bash
    # 1. Crear el entorno virtual
    python3 -m venv .venv

    # 2. Activar el entorno
    source .venv/bin/activate

    # 3. Instalar las dependencias
    pip install -r requirements.txt
    ```

    _Nota: Para desactivar el entorno más tarde, simplemente ejecuta `deactivate`._

2.  **Generación de Entornos:**
    El script `generate_envs.py` ha sido refactorizado a una CLI para permitir la generación dinámica de entornos.

    ```bash
    # Ejemplo: Generar 3 entornos con prefijo "staging" y puerto base 3000
    # (Asegúrate de tener el entorno virtual activado)
    python generate_envs.py --count 3 --prefix staging --port 3000
    ```

3.  **Operaciones de Terraform:**
    Para cada entorno generado, se pueden ejecutar los comandos estándar de Terraform.

    ```bash
    # Navegar al directorio del entorno
    cd environments/staging1

    # Inicializar el backend y los proveedores
    terraform init

    # Previsualizar los cambios en la infraestructura
    terraform plan

    # Aplicar los cambios
    terraform apply
    ```

## Análisis de la Fase 1: Gestión de Cambios

- **Interpretación de Terraform ante un cambio de variable:**
  Terraform mantiene un archivo de estado (`.tfstate`) que representa la última configuración conocida de la infraestructura. Al ejecutar `terraform plan`, compara este estado con la configuración actual definida en los archivos `.tf.json` y `.tfvars`. Si detecta una discrepancia (por ejemplo, un cambio en el valor `default` de una variable no sobreescrita), lo identifica como un cambio necesario y propone un plan de ejecución para alinear la infraestructura con el código.

- **Diferencia entre modificar el JSON vs. modificar el recurso directamente:**
  Modificar el archivo de configuración JSON es la metodología central de IaC; el cambio es declarativo, versionable y auditable. Modificar el recurso directamente en el entorno de ejecución (cambio "out-of-band") introduce "drift". Terraform detectará esta desviación en la siguiente ejecución y propondrá un plan para revertir el cambio manual, reforzando el código como la única fuente de verdad.

- **Recreación de recursos vs. cambios "in-place":**
  La decisión de recrear o modificar un recurso depende del tipo de cambio y de las capacidades del proveedor de Terraform. En nuestro caso, al modificar un `trigger` en un `null_resource`, se fuerza su reemplazo. Sin embargo, para muchos otros tipos de recursos y atributos (ej. actualizar una etiqueta en una instancia de nube), Terraform y su proveedor pueden estar optimizados para aplicar el cambio "in-place", lo cual es más eficiente y menos disruptivo.

- **Impacto de editar `main.tf.json` directamente:**
  Editar directamente un archivo `main.tf.json` en un entorno generado es una mala práctica, ya que se considera un artefacto de construcción. Estos archivos están diseñados para ser sobreescritos por el script `generate_envs.py`. Cualquier cambio manual se perderá en la siguiente ejecución del generador, lo que subraya la necesidad de tratar el código fuente (el generador y las plantillas) como la autoridad.

## Discusión de la Fase 4: Escalabilidad y Buenas Prácticas

- **Extensión del patrón a 50 módulos y 100 entornos:**
  Para escalar este modelo, sería necesario externalizar la configuración de los entornos (ej. a archivos YAML) en lugar de mantenerla en una lista de Python. Los módulos de Terraform deberían ser versionados y alojados en un repositorio de Git propio, desde donde se podrían referenciar de forma remota. El generador se volvería más sofisticado, capaz de leer la configuración externa y construir un grafo de dependencias entre entornos.

- **Prácticas de revisión de código para `.tf.json`:**
  La revisión de código no debe centrarse en los archivos `.tf.json` generados, sino en sus fuentes: el script generador y las plantillas en `modules/`. Un pipeline de CI/CD debería automatizar la validación, ejecutando `terraform validate` y `terraform plan` para cada cambio propuesto en un Pull Request. El resultado del plan debe ser publicado para que los revisores puedan evaluar el impacto de los cambios.

- **Gestión de secretos en producción (sin Vault):**
  La estrategia implementada (leer desde variables de entorno) es un estándar de la industria. En un entorno de producción, estas variables de entorno serían inyectadas de forma segura por el sistema de CI/CD (ej. GitHub Actions Secrets, AWS Secrets Manager). Esto asegura que los secretos no se almacenen en el repositorio de código y solo existan en el contexto de la ejecución del despliegue.

- **Workflows de revisión para los JSON generados:**
  El workflow principal sería la automatización a través de CI. Se pueden añadir hooks de pre-commit que ejecuten validadores de formato como `jq --check` para asegurar la consistencia del código antes de que sea subido al repositorio. El pipeline de CI se encargaría de la validación semántica (con `terraform plan`) y de reportar los resultados, previniendo la integración de cambios que rompan la infraestructura.

## Ejercicios Opcionales Completados

- **Ejercicio 2: CLI Interactiva:**
  Se ha refactorizado el script `generate_envs.py` utilizando la librería `click` para crear una interfaz de línea de comandos. Esto permite la generación dinámica de entornos mediante parámetros, mejorando la flexibilidad y la reutilización del script. Por ejemplo:
  `python generate_envs.py --count 5 --prefix dev --port 8000`
