# BigQuery Query Cloud Function

This Cloud Function serves as an HTTP interface to execute queries on Google BigQuery. It is designed with basic SQL injection prevention measures.

## Getting Started

### Prerequisites

- Google Cloud SDK installed and initialized
- Python 3.7+ and pip installed
- Google Cloud project with Billing and BigQuery API enabled

### Setup and Deployment

1. **Clone the Repository**

   Clone this repository to your local machine or download the source code.

2. **Create a Virtual Environment**

   Navigate to the project directory and create a virtual environment:

   ```sh
   python3 -m venv env
   source env/bin/activate
