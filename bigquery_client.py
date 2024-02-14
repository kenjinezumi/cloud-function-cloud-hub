from google.cloud import bigquery
import re
from typing import List, Dict, Any

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