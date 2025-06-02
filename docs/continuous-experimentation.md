# Continuous Experimentation Plan

## Hypothesis
We hypothesize that model version v2 has a higher sentiment prediction accuracy than version v1.

## Metrics
- `webapp_predictions_total`: Count of predictions made, labeled by model version and sentiment.
- `webapp_response_latency_seconds`: Response latency of the `/api/analyze` endpoint.
- `webapp_ram_usage_bytes`: RAM usage of the app container.

## Experiment Design
We will deploy two versions of the sentiment analysis service: `v1` and `v2`.

Using Istio VirtualService, traffic will be split 90% to v1 and 10% to v2, simulating a canary deployment.

Sticky sessions will ensure each user remains connected to the same version during testing.

The application exposes Prometheus metrics, which are collected and visualized in a Grafana dashboard.
