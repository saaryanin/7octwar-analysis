import pandas as pd
from pathlib import Path


def main():
    # ==================== PATHS ====================
    root = Path(__file__).parent.parent
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"

    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / "oct7database_full.xlsx"  # Updated name
    processed_csv = processed_dir / "oct7database_clean.csv"

    if not raw_path.exists():
        print(f"❌ Error: Raw file not found at {raw_path}")
        print("Please download the full XLSX from oct7database.com")
        print("and save it as 'oct7database_full.xlsx' in data/raw/")
        return

    # ==================== LOAD ====================
    print("Loading English XLSX...")
    df = pd.read_excel(raw_path)

    # Select desired columns
    columns_to_keep = [
        'first name', 'last name', 'Gender', 'Age', 'Residence', 'Country',
        'Role', 'Status', 'Event Date', 'Death Date', 'Front',
        'Cause of Death', 'Event location', 'Death location'
    ]

    available_cols = [col for col in columns_to_keep if col in df.columns]
    df = df[available_cols].copy()

    # ==================== CLEANING ====================
    # Rename to snake_case
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # Gender standardization
    df['gender'] = df['gender'].map({
        'M': 'Male', 'F': 'Female',
        'Male': 'Male', 'Female': 'Female'
    }).fillna(df['gender'])

    # Title Case for all string columns (except dates and age)
    string_cols = ['first_name', 'last_name', 'residence', 'country', 'role',
                   'status', 'front', 'cause_of_death', 'event_location', 'death_location']

    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Special fix for Status (common values)
    status_map = {
        'killed': 'Killed',
        'kidnapped': 'Kidnapped',
        'returned': 'Returned',
        'died in captivity': 'Died In Captivity',
        # Add more if you see them later
    }
    if 'status' in df.columns:
        df['status'] = df['status'].replace(status_map)

    # Basic cleaning
    df = df.drop_duplicates().reset_index(drop=True)

    print(f"✅ Processed dataset: {len(df)} rows, {len(df.columns)} columns")
    print("Columns:", list(df.columns))

    # Sample of cleaned data
    print("\nSample of Status column after cleaning:")
    print(df['status'].value_counts().head(10))

    # ==================== SAVE ====================
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')

    print(f"\n✅ Clean CSV saved to: {processed_csv}")


if __name__ == "__main__":
    main()