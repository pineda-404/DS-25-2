import os, json, re

LEGACY_DIR = "legacy"
OUT_DIR    = "migrated_env"

def migrate():
    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Read legacy config
    with open(os.path.join(LEGACY_DIR, "config.cfg"), "r") as f:
        config_content = f.read()
    
    port_match = re.search(r"PORT=(\d+)", config_content)
    port = int(port_match.group(1)) if port_match else 8080

    with open(os.path.join(LEGACY_DIR, "run.sh"), "r") as f:
        run_script_content = f.read()
    
    command = run_script_content.splitlines()[1].replace("$PORT", str(port))

    # 2. Generate network.tf.json
    network_config = {
        "variable": {
            "port": {
                "type": "number",
                "default": port
            }
        }
    }
    with open(os.path.join(OUT_DIR, "network.tf.json"), "w") as f:
        json.dump(network_config, f, indent=4)

    # 3. Generate main.tf.json
    main_config = {
        "resource": {
            "null_resource": {
                "legacy_server": {
                    "triggers": {
                        "port": "${var.port}"
                    },
                    "provisioner": [
                        {
                            "local-exec": {
                                "command": command
                            }
                        }
                    ]
                }
            }
        }
    }
    with open(os.path.join(OUT_DIR, "main.tf.json"), "w") as f:
        json.dump(main_config, f, indent=4)

if __name__ == "__main__":
    migrate()
    print(f"Entorno migrado en '{OUT_DIR}/'")