import psycopg2
import pandas as pd
from pathlib import Path

def convert(file_name, input_file, output_file):
    """
    Import a CSV into PostgreSQL table (named file_name) and export as SQL dump.
    """
    # Ensure output folder exists
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Prompt for database credentials
    database = input("Database name: ").strip()
    user = input("User (default postgres): ").strip() or 'postgres'
    password = input("Password: ").strip()
    host = input("Host (default localhost): ").strip() or 'localhost'
    port = input("Port (default 5432): ").strip() or 5432

    # Read CSV
    df = pd.read_csv(input_file)
    table = file_name
    cols = df.columns.tolist()

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    cursor = conn.cursor()

    # Create table dynamically
    create_sql = f"CREATE TABLE IF NOT EXISTS {table} ({', '.join([f'{c} TEXT' for c in cols])});"
    cursor.execute(create_sql)

    # Insert CSV rows
    for row in df.itertuples(index=False):
        values = ', '.join([f"'{str(v).replace('\'','\'\'')}'" for v in row])
        cursor.execute(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({values});")

    conn.commit()

    # Export table to SQL file
    with open(output_file, 'w') as f:
        for row in df.itertuples(index=False):
            vals = ', '.join([f"'{str(v).replace('\'','\'\'')}'" if v is not None else 'NULL' for v in row])
            f.write(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({vals});\n")

    cursor.close()
    conn.close()
    print(f"CSV {input_file} imported into {table} and SQL dump written to {output_file}")
