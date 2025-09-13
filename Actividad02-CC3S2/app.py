from flask import Flask, jsonify
import os
import sys

# 12-Factor: configuración vía variables de entorno
PORT = int(os.environ.get("PORT", "8080"))
MESSAGE = os.environ.get("MESSAGE", "Hola")
RELEASE = os.environ.get("RELEASE", "v0")

app = Flask(__name__)


@app.route("/")
def root():
    # Logs en stdout (12-Factor: logs como flujos de eventos)
    print(
        f"[INFO] GET /  message={MESSAGE} release={RELEASE}", file=sys.stdout, flush=True)
    return jsonify(
        status="ok",
        message=MESSAGE,
        release=RELEASE,
        port=PORT,
    )


if __name__ == "__main__":
    # 12-Factor: vincular a un puerto
    print(f"[STARTUP] Starting app on port {PORT} with message='{
          MESSAGE}' release='{RELEASE}'", file=sys.stdout, flush=True)
    app.run(host="0.0.0.0", port=PORT)   app.run(host="0.0.0.0", port=PORT)
