import os

import psutil
import requests
from flasgger import Swagger
from flask import Flask, jsonify, request
from flask_cors import CORS
from lib_version.version_util import VersionUtil
from prometheus_client import Counter, Gauge, Histogram, generate_latest

REQUEST_COUNT = Counter(
    "webapp_predictions_total",
    "Total number of predictions made",
    ["model_version", "prediction_class"],
)

RAM_USAGE = Gauge("webapp_ram_usage_bytes", "Current RAM usage of the web application")

RESPONSE_LATENCY = Histogram(
    "webapp_response_latency_seconds",
    "Histogram of response latency for analyze endpoint",
    ["endpoint"],
)

app = Flask(__name__)
CORS(app)
swagger = Swagger(app)


@app.route("/api/analyze", methods=["POST"])
def analyze():
    with RESPONSE_LATENCY.labels("analyze").time():
        text = request.json.get("text")
        if not text:
            return jsonify({"error": "Missing text"}), 400

        try:
            model_service_url = os.getenv(
                "MODEL_SERVICE_URL", "http://model-service:5010"
            )
            response = requests.post(
                f"{model_service_url}/api/model", json={"text": text}, timeout=5
            )

            res_2 = requests.get(f"{model_service_url}/api/version", timeout=5)

            prediction_class = response.json().get("sentiment", "unknown")
            model_version = res_2.json().get("model_version", "unknown")

            REQUEST_COUNT.labels(
                model_version=model_version, prediction_class=prediction_class
            ).inc()

            result = response.json()
            result["model_version"] = model_version
            return jsonify(result), response.status_code
        except requests.exceptions.RequestException:
            return jsonify({"error": "Model service unavailable"}), 502


@app.route("/api/version", methods=["GET"])
def version():
    return jsonify(
        {
            "app_version": VersionUtil.get_version(),
        }
    )


@app.route("/api/feedback", methods=["POST"])
def feedback():
    return jsonify({"status": "success"})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/api/metrics", methods=["GET"])
def metrics():
    process = psutil.Process()
    ram_usage = process.memory_info().rss
    RAM_USAGE.set(ram_usage)

    return (
        generate_latest(),
        200,
        {"Content-Type": "text/plain; version=0.0.4; charset=utf-8"},
    )


@app.route("/api/app-service-version", methods=["GET"])
def app_service_version():
    return jsonify({"app-service-version": "v2.0.0"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
