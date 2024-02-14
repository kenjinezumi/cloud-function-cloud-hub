# BigQuery Query Cloud Run Service

This Cloud Run service provides an HTTP interface to execute queries on Google BigQuery, incorporating basic SQL injection prevention measures.

## Getting Started

### Prerequisites

- Google Cloud SDK installed and initialized.
- Docker installed on your local machine.
- Python 3.7+ and pip installed.
- A Google Cloud project with Billing and BigQuery API enabled.

### Setup and Deployment

1. **Prepare the Application**

   Set up a new directory for your project and navigate into it:
   ```sh
   mkdir bigquery-cloud-run-app && cd bigquery-cloud-run-app

2. **Create a Python virtual environment and activate it:**

   ```sh
   python3 -m venv env
   source env/bin/activate

Install the necessary Python packages by creating a requirements.txt file with the following content and then running pip install:

   ```sh
   gunicorn==20.1.0
   google-cloud-bigquery==2.34.2
   ```


Run the following command to install the dependencies:

   ```shell
   pip install -r requirements.txt

   ```

## Build and Push Your Container Image

Use Cloud Build to build your container image and push it to Google Container Registry (GCR):

```sh
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/bigquery-cloud-run-app