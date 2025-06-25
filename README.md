# app

![pylint](pylint_badge.svg)

### **app** (or **app-frontend** + **app-service**)

**Overview**
A web application that allows users to submit restaurant reviews for sentiment analysis. Communicates with `model-service` via REST. The frontend is built with React and communicates with the backend via REST. And the backend is built with Flask and communicates with the model service via REST. The personal contribution can be seen from `ACTIVITY.md`. 

#### **Features**

- User-friendly interface for submitting reviews.
- Displays sentiment results (e.g., happy/sad smiley).
- Shows versions of `app` and `model-service`.

#### **Run Locally**

1. Pull the Docker image:

   ```bash
   docker pull ghcr.io/remla25-team16/app:v1.0.0
   ```

2. Start the app (configure `MODEL_SERVICE_URL`):

   ```bash
   docker run -p 8080:8080 -e MODEL_SERVICE_URL=http://model-service:5000 ghcr.io/remla25-team16/app
   ```

   