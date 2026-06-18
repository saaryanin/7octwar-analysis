import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine

VIEWS = [
    "tableau_monthly_killed_by_type",
    "tableau_age_dist_by_role",
    "tableau_soldiers_by_region",
]


def export_tableau_csvs():
    root = Path(__file__).parent.parent
    db_path = root / "data" / "oct7_analysis.db"
    output_dir = root / "data" / "processed"

    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        print("Run src/create_sqlite_db.py first.")
        return

    engine = create_engine(f"sqlite:///{db_path}")

    for view in VIEWS:
        df = pd.read_sql(f"SELECT * FROM {view}", engine)
        out_path = output_dir / f"{view}.csv"
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"✅ {view}.csv — {len(df)} rows → {out_path}")


if __name__ == "__main__":
    export_tableau_csvs()
