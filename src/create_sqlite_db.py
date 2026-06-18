import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine


def create_database():
    root = Path(__file__).parent.parent
    processed_csv = root / "data" / "processed" / "oct7database_clean.csv"
    db_path = root / "data" / "oct7_analysis.db"

    print("Creating SQLite database...")
    df = pd.read_csv(processed_csv)

    engine = create_engine(f'sqlite:///{db_path}')
    df.to_sql('idf_casualties', engine, if_exists='replace', index=False)

    print(f"✅ Database created successfully at: {db_path}")
    print(f"Total rows: {len(df)}")
    print("Table name: idf_casualties")


if __name__ == "__main__":
    create_database()