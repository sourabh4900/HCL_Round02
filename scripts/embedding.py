"""Build Chroma vector index for skills and career profiles."""

from pathlib import Path

import chromadb
import pandas as pd
from sentence_transformers import SentenceTransformer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DIR = PROJECT_ROOT / "chroma_db"
MODEL_NAME = "all-MiniLM-L6-v2"
COLLECTION_NAME = "career_profiles"
BATCH_SIZE = 256


def sanitize_metadata(record: dict) -> dict:
    """Chroma metadata values must be scalar types."""
    clean = {}
    for key, value in record.items():
        if pd.isna(value):
            clean[key] = ""
        elif isinstance(value, (str, int, float, bool)):
            clean[key] = value
        else:
            clean[key] = str(value)
    return clean


def add_in_batches(collection, ids, embeddings, metadatas, documents) -> None:
    for start in range(0, len(ids), BATCH_SIZE):
        end = start + BATCH_SIZE
        collection.add(
            ids=ids[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end],
            documents=documents[start:end],
        )


def main() -> None:
    model = SentenceTransformer(MODEL_NAME)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(COLLECTION_NAME)

    careers = pd.read_csv(DATA_DIR / "careers.csv")
    skills = pd.read_csv(DATA_DIR / "skills.csv")

    career_texts = careers.apply(
        lambda row: f"{row['role']} {row['description']} {row['required_skills']}",
        axis=1,
    ).tolist()
    career_embeddings = model.encode(career_texts, show_progress_bar=True).tolist()
    career_ids = [f"career_{i}" for i in range(len(careers))]
    career_metadatas = [
        sanitize_metadata({**record, "type": "career"}) for record in careers.to_dict("records")
    ]

    skill_texts = skills["skill"].astype(str).tolist()
    skill_embeddings = model.encode(skill_texts, show_progress_bar=True).tolist()
    skill_ids = [f"skill_{i}" for i in range(len(skills))]
    skill_metadatas = [
        sanitize_metadata({"skill": skill, "type": "skill"}) for skill in skill_texts
    ]

    add_in_batches(
        collection,
        career_ids + skill_ids,
        career_embeddings + skill_embeddings,
        career_metadatas + skill_metadatas,
        career_texts + skill_texts,
    )

    print(f"Indexed {len(careers)} careers and {len(skills)} skills in '{COLLECTION_NAME}'.")
    print(f"Chroma DB stored at: {CHROMA_DIR}")


if __name__ == "__main__":
    main()
