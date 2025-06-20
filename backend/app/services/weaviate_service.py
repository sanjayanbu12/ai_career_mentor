import weaviate
import config

def get_weaviate_client():
    """Initializes and returns a Weaviate client configured for WCS."""
    client = weaviate.Client(
        url=config.WEAVIATE_URL,
        auth_client_secret=weaviate.auth.AuthApiKey(api_key=config.WEAVIATE_API_KEY)
    )
    return client

def setup_weaviate_schema(client):
    """Sets up the schema in Weaviate."""
    schema = {
        "classes": [
            {
                "class": "Career",
                "description": "Information about various career paths",
                "properties": [
                    {"name": "title", "dataType": ["text"]},
                    {"name": "description", "dataType": ["text"]},
                    {"name": "skills", "dataType": ["text[]"]},
                ],
            },
            {
                "class": "Support",
                "description": "Information about mentors and support groups",
                "properties": [
                    {"name": "name", "dataType": ["text"]},
                    {"name": "type", "dataType": ["text"]},
                    # --- THIS IS THE FIX ---
                    # Change focus to a single text field for better keyword matching
                    {"name": "focus", "dataType": ["text"]},
                    # -----------------------
                    {"name": "contact", "dataType": ["text"]},
                ],
            },
        ]
    }
    client.schema.create(schema)