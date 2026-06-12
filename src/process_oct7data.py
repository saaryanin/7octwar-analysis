import pandas as pd
from pathlib import Path


def main():
    # ==================== PATHS ====================
    root = Path(__file__).parent.parent
    raw_dir = root / "data" / "raw"
    processed_dir = root / "data" / "processed"

    processed_dir.mkdir(parents=True, exist_ok=True)

    raw_path = raw_dir / "oct7database_full.xlsx"
    processed_csv = processed_dir / "oct7database_clean.csv"

    if not raw_path.exists():
        print("❌ Raw file not found at:", raw_path)
        print(
            "Please download the full XLSX from oct7database.com and save it as 'oct7database_full.xlsx' in data/raw/")
        return

    # ==================== LOAD DATA ====================
    print("Loading dataset...")
    df = pd.read_excel(raw_path)

    # Select desired columns
    columns_to_keep = [
        'first name', 'last name', 'Gender', 'Age', 'Residence', 'Country',
        'Role', 'Status', 'Event Date', 'Death Date', 'Front',
        'Cause of Death', 'Event location', 'Death location'
    ]

    available = [col for col in columns_to_keep if col in df.columns]
    df = df[available].copy()

    # Rename to snake_case
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    # ==================== BASIC CLEANING ====================
    # Gender
    df['gender'] = df['gender'].map({'M': 'Male', 'F': 'Female'}).fillna(df['gender'])

    # Title case for all string columns
    string_cols = ['first_name', 'last_name', 'residence', 'country', 'role', 'status',
                   'front', 'cause_of_death', 'event_location', 'death_location']
    for col in string_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.title()

    # Fix dirty data
    df['first_name'] = df['first_name'].replace('(Res.)', 'Unknown').str.strip()

    # ==================== DERIVED COLUMNS ====================
    # Is Soldier flag
    df['is_soldier'] = df['role'].str.contains('soldier', case=False, na=False)

    # Improved Status Simple
    def simplify_status(s):
        if not isinstance(s, str):
            return 'Other'
        s_lower = s.lower()

        if 'killed' in s_lower:
            if 'kidnapped' in s_lower:
                return 'Kidnapped and Killed'
            return 'Killed'
        elif 'released' in s_lower and 'died' in s_lower:
            return 'Released then Died'
        elif 'died in captivity' in s_lower:
            return 'Died In Captivity'
        elif any(word in s_lower for word in ['released', 'returned', 'rescued', 'retrieved']):
            return 'Released / Rescued'
        elif 'kidnapped' in s_lower:
            return 'Kidnapped'
        return 'Other'

    df['status_simple'] = df['status'].apply(simplify_status)

    # ==================== DEATH DATE HANDLING ====================
    df['death_date'] = df['death_date'].astype(str).str.strip()

    df['death_date_clean'] = pd.to_datetime(df['death_date'], errors='coerce')
    df['death_year'] = pd.to_numeric(df['death_date'].str[:4], errors='coerce')

    def get_year_month(date_str):
        date_str = str(date_str).strip()
        if len(date_str) >= 7 and date_str[4] == '-':
            return date_str[:7]  # e.g. "2024-02"
        elif len(date_str) == 4 and date_str.isdigit():
            return date_str  # e.g. "2023"
        return pd.NA

    df['death_year_month'] = df['death_date'].apply(get_year_month)

    # ==================== FINAL CLEANING & SAVE ====================
    df = df.drop_duplicates().reset_index(drop=True)

    print(f"✅ Final dataset: {len(df)} rows")
    print("Columns:", list(df.columns))
    print(f"\nSoldiers: {df['is_soldier'].sum()}")
    print("\nStatus Simple distribution:")
    print(df['status_simple'].value_counts())

    # Save
    df.to_csv(processed_csv, index=False, encoding='utf-8-sig')
    print(f"\n✅ Clean file saved to: {processed_csv}")


if __name__ == "__main__":
    main()