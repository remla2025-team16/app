from flask import Flask, jsonify, request
import requests
from lib_version.version_util import VersionUtil
from flasgger import Swagger
from flask_cors import CORS
import os
from prometheus_client import Counter, Gauge, Histogram, generate_latest
import psutil

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'webapp_predictions_total', 
    'Total number of predictions made',
    ['model_version', 'prediction_class']
)

RAM_USAGE = Gauge(
    'webapp_ram_usage_bytes', 
    'Current RAM usage of the web application'
)

RESPONSE_LATENCY = Histogram(
    'webapp_response_latency_seconds',
    'Histogram of response latency for analyze endpoint',
    ['endpoint']
)


app = Flask(__name__)
CORS(app)
swagger = Swagger(app)

@app.route('/api/analyze', methods=['POST'])
def analyze():
    """
    ---
    tags:
      - App Service
    parameters:
      - name: text
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
              example: "The pasta was cold."
    responses:
      200:
        description: Analysis result
        schema:
          type: object
          properties:
            sentiment:
              type: integer
              enum: [0, 1]
              description: "0 for negative sentiment, 1 for positive sentiment"
      502:
        description: Model service unavailable
    """
    with RESPONSE_LATENCY.labels('analyze').time():
      # 1. Validate input
      text = request.json.get('text')
      if not text:
          return jsonify({"error": "Missing text"}), 400
      
      # 2. Call model-service (configured via ENV)
      try:
          model_service_url = os.getenv("MODEL_SERVICE_URL", "http://model-service:5010")
          response = requests.post(
              f"{model_service_url}/api/model",
              json={"text": text},
              timeout=5
          )
          
          res_2 = requests.get(
              f"{model_service_url}/api/version",
              timeout=5
          )
          
          prediction_class = response.json().get("sentiment", "unknown")
          model_version = res_2.json().get("model_version", "unknown") 

          # 3. Update Prometheus metrics
          REQUEST_COUNT.labels(model_version=model_version, prediction_class=prediction_class).inc()

          return jsonify(response.json()), response.status_code
      except requests.exceptions.RequestException:
          return jsonify({"error": "Model service unavailable"}), 502

@app.route('/api/version', methods=['GET'])
def version():
    """
    ---
    tags:
      - App Service
    responses:
      200:
        description: System versions
        schema:
          type: object
          properties:
            app_version:
              type: string
            model_version:
              type: string
    """
    return jsonify({
        "app_version": VersionUtil.get_version(),  # From lib-version
        # "model_version": get_model_version()       # Call model-service's version API
    })

@app.route('/api/feedback', methods=['POST'])
def feedback():
    """
    ---
    tags:
      - Feedback
    parameters:
      - name: data
        in: body
        required: true
        schema:
          type: object
          properties:
            text:
              type: string
            predicted_sentiment:
              type: integer
            actual_sentiment:
              type: integer
    responses:
      200:
        description: Feedback recorded
    """
    # Store feedback in database/file for future model training
    return jsonify({"status": "success"})

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/metrics', methods=['GET'])
def metrics():
  """
  tags:
    - Metrics
  responses:
    200:
      description: Prometheus metrics
      schema:
        type: string
    502:
      description:  Metrics unavailable    
  """

    # Update RAM usage
  process = psutil.Process()
  ram_usage = process.memory_info().rss  # in bytes
  RAM_USAGE.set(ram_usage)

  return generate_latest(), 200, {'Content-Type': 'text/plain; version=0.0.4; charset=utf-8'}


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)