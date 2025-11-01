import os, json
from shutil import copyfile
import click

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def render_and_write(env):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    # 1) Copia la definición de variables (network.tf.json)
    copyfile(
        os.path.join(MODULE_DIR, "network.tf.json"),
        os.path.join(env_dir, "network.tf.json")
    )

    # 2) Genera main.tf.json solo con recursos
    config = {
        "resource": [
            {
                "null_resource": [
                    {
                        "local_server": [
                            {
                                "triggers": {
                                    "name":    "${var.name}",
                                    "network": "${var.network}",
                                    "port": "${var.port}",
                                    "api_key": "${var.api_key}"
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": "echo 'Arrancando servidor ${var.name} en red ${var.network} y puerto ${var.port} con api_key ${var.api_key}'"
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
        json.dump(config, fp, sort_keys=True, indent=4)

    # 3) Genera terraform.tfvars.json
    tfvars = {
        "name": env["name"]
    }
    if "network" in env:
        tfvars["network"] = env["network"]
    if "port" in env:
        tfvars["port"] = env["port"]
    
    api_key = os.environ.get("API_KEY")
    if api_key:
        tfvars["api_key"] = api_key

    with open(os.path.join(env_dir, "terraform.tfvars.json"), "w") as fp:
        json.dump(tfvars, fp, sort_keys=True, indent=4)

@click.command()
@click.option("--count", default=1, help="Número de entornos a generar.")
@click.option("--prefix", default="app", help="Prefijo para el nombre del entorno.")
@click.option("--port", default=8080, help="Puerto base para los entornos.")
def generate_envs(count, prefix, port):
    """Genera N entornos de Terraform."""
    ENVS = [
        {
            "name": f"{prefix}{i}",
            "network": f"net{i}",
            "port": port + i - 1
        }
        for i in range(1, count + 1)
    ]

    for env in ENVS:
        render_and_write(env)
    
    click.echo(f"Generados {len(ENVS)} entornos en '{OUT_DIR}/'")

if __name__ == "__main__":
    generate_envs()