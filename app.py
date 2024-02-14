from flask import Flask, jsonify, request
from google.cloud import bigquery
import re
from typing import Dict, List, Any

app = Flask(__name__)


class BigQueryClient:
    """
    A client for querying Google BigQuery with basic SQL sanitization to prevent SQL injection.
    """

    def __init__(self):
        """Initializes the BigQuery client."""
        self.client = bigquery.Client()

    def is_safe_query(self, query: str) -> bool:
        """
        Verifies if the provided SQL query string is safe to execute by checking against a list of disallowed keywords.

        Args:
            query (str): The SQL query string.

        Returns:
            bool: True if the query does not contain disallowed keywords, False otherwise.
        """
        disallowed_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE']
        pattern = '|'.join(disallowed_keywords)
        return not re.search(pattern, query, re.IGNORECASE)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a provided SQL query against BigQuery if it is considered safe.

        Args:
            query (str): The SQL query string.

        Returns:
            List[Dict[str, Any]]: The query results as a list of dictionaries.

        Raises:
            ValueError: If the query is determined to be unsafe.
            Exception: For errors encountered during query execution.
        """
        if not self.is_safe_query(query):
            raise ValueError("Unsafe query detected.")

        try:
            query_job = self.client.query(query)
            results = query_job.result()  # Waits for the job to complete.
            return [dict(row) for row in results]
        except Exception as e:
            raise e


@app.route('/query', methods=['POST'])
def query_bigquery_data() -> Tuple[str, int]:
    """
    Endpoint to execute a query against Google BigQuery and return the results.

    Returns:
        Tuple[str, int]: A JSON response containing the query results and the HTTP status code.
    """
    request_json = request.get_json()

    if request_json and 'query' in request_json:
        query = request_json['query']
    else:
        return jsonify({"error": "Please provide a query parameter."}), 400

    bq_client = BigQueryClient()

    try:
        records = bq_client.execute_query(query)
        return jsonify(records), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
from flask import Flask, jsonify, request
from google.cloud import bigquery
import re
from typing import Dict, List, Any

app = Flask(__name__)


class BigQueryClient:
    """
    A client for querying Google BigQuery with basic SQL sanitization to prevent SQL injection.
    """

    def __init__(self):
        """Initializes the BigQuery client."""
        self.client = bigquery.Client()

    def is_safe_query(self, query: str) -> bool:
        """
        Verifies if the provided SQL query string is safe to execute by checking against a list of disallowed keywords.

        Args:
            query (str): The SQL query string.

        Returns:
            bool: True if the query does not contain disallowed keywords, False otherwise.
        """
        disallowed_keywords = ['DROP', 'DELETE', 'INSERT', 'UPDATE']
        pattern = '|'.join(disallowed_keywords)
        return not re.search(pattern, query, re.IGNORECASE)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a provided SQL query against BigQuery if it is considered safe.

        Args:
            query (str): The SQL query string.

        Returns:
            List[Dict[str, Any]]: The query results as a list of dictionaries.

        Raises:
            ValueError: If the query is determined to be unsafe.
            Exception: For errors encountered during query execution.
        """
        if not self.is_safe_query(query):
            raise ValueError("Unsafe query detected.")

        try:
            query_job = self.client.query(query)
            results = query_job.result()  # Waits for the job to complete.
            return [dict(row) for row in results]
        except Exception as e:
            raise e


@app.route('/query', methods=['POST'])
def query_bigquery_data() -> Tuple[str, int]:
    """
    Endpoint to execute a query against Google BigQuery and return the results.

    Returns:
        Tuple[str, int]: A JSON response containing the query results and the HTTP status code.
    """
    request_json = request.get_json()

    if request_json and 'query' in request_json:
        query = request_json['query']
    else:
        return jsonify({"error": "Please provide a query parameter."}), 400

    bq_client = BigQueryClient()

    try:
        records = bq_client.execute_query(query)
        return jsonify(records), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
