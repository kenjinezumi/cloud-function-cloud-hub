from flask import jsonify, Request
from google.cloud import bigquery
import re
from typing import Tuple, List, Dict, Any
import functions_framework
@functions_framework.http
def query_bigquery_data(request: Request) -> Tuple[str, int]:
    """
    Cloud Function to execute a query against Google BigQuery.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Tuple[str, int]: The JSON response containing the query results and the HTTP status code.
    """
    request_json = request.get_json(silent=True)

    if request_json and 'query' in request_json:
        query = request_json['query']
    else:
        return 'Please provide a query parameter.', 400

    bq_client = BigQueryClient()

    try:
        records = bq_client.execute_query(query)
        return jsonify(records), 200
    except ValueError as ve:
        return str(ve), 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



class BigQueryClient:
    """
    A client for querying Google BigQuery with basic SQL sanitization to prevent SQL injection.
    """

    def __init__(self):
        """Initializes the BigQuery client."""
        self.client = bigquery.Client()

    def is_safe_query(self, query: str) -> bool:
        """
        Checks if the query string is safe to execute by looking for disallowed keywords.

        Args:
            query (str): The SQL query string.

        Returns:
            bool: True if safe, False otherwise.
        """
        disallowed_keywords = ['DROP']
        pattern = '|'.join(disallowed_keywords)
        return not re.search(pattern, query, re.IGNORECASE)

    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Executes a provided SQL query if it is considered safe.

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
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            raise e
s