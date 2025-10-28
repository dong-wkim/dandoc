import psycopg2
import csv
import pandas as pd

def convert(file_name, input_file, output_file):
    with open(input_file, 'r') as f:
         sql = f.read()
    database = input('d: ').strip()
    table = file_name

    schema = {}
    conn = psycopg2.connect(database = database,
                        user = 'postgres',
                        password = 'c4dc3571c4794f10b3d7ba8c8d83e50f',
                        host = 'localhost',
                        port = 5432)
    cursor = conn.cursor()
    cursor.execute(sql)

    if sql.strip().lower().startswith('select'):
        rows = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(rows, columns=col_names)
        df.to_csv(output_file, index=False)
        print(f"Query result exported to {output_file}")
    else:
        conn.commit()
        print("SQL executed successfully (no SELECT to export).")
    conn.commit()
    conn.close()