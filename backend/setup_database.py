import pandas as pd
import weaviate
import numpy as np
from app.services.weaviate_service import get_weaviate_client, setup_weaviate_schema
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import config

def load_and_populate_data(client):
    """
    Loads data. Vectorizes Career data. Loads Support data as plain text for keyword search.
    """
    print("\n--- Starting Data Loading ---")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=config.GOOGLE_API_KEY)

    try:
        # Load and vectorize career data
        print("\nProcessing and vectorizing career data...")
        careers_df = pd.read_csv("data/career_database.csv")
        with client.batch as batch:
            for index, row in careers_df.iterrows():
                properties = { "title": row["title"], "description": row["description"], "skills": row["skills"].split(',') }
                text_to_vectorize = f"Career Title: {row['title']}. Description: {row['description']}. Required Skills: {row['skills']}"
                vector = embeddings.embed_query(text_to_vectorize)
                batch.add_data_object(properties, "Career", vector=vector)
        print("✅ Successfully loaded and vectorized career data.")

        # Load support network data for keyword search
        print("\nProcessing support network data...")
        support_df = pd.read_csv("data/support_network_database.csv")
        with client.batch as batch:
            for index, row in support_df.iterrows():
                properties = {
                    "name": row["name"], "type": row["type"],
                    # --- THIS IS THE FIX ---
                    # Join all focus keywords into a single searchable string
                    "focus": " ".join([kw.strip().lower() for kw in row["focus"].split(',')]),
                    # -----------------------
                    "contact": row["contact"]
                }
                batch.add_data_object(properties, "Support")
        print("✅ Successfully loaded support network data.")

    except Exception as e:
        print(f"\n❌ AN ERROR OCCURRED DURING DATA LOADING: {e}\n")

def main():
    client = get_weaviate_client()
    print("--- Deleting existing schema for a clean setup ---")
    client.schema.delete_all()
    print("\n--- Setting up new schema ---")
    setup_weaviate_schema(client)
    
    load_and_populate_data(client)
    print("\n--- Database is ready. ---")

if __name__ == "__main__":
    main()