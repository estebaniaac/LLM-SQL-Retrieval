import sqlite3
import pandas as pd

# Paths
excel_file_path = 'sql/example_outdoor_spaces.xlsx'
db_path = 'sql/example_outdoor_spaces.db'

# Connect to SQLite DB
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Drop all existing tables
def drop_all_tables(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")
    print("✅ Existing tables dropped.")

drop_all_tables(cursor)
conn.commit()

# Load all Excel sheets
sheets_dict = pd.read_excel(excel_file_path, sheet_name=None)

# Loop through and insert each sheet into a corresponding SQL table
for sheet_name, df in sheets_dict.items():
    df.columns = df.columns.str.strip()  # remove any accidental whitespace
    df.to_sql(sheet_name, conn, if_exists='replace', index=False)
    print(f"✅ Inserted sheet '{sheet_name}' into table '{sheet_name}'.")

conn.close()
print("✅ Done.")
