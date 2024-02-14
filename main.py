from flask import escape, jsonify, Request
from bigquery_client import BigQueryClient
from typing import Tuple

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
