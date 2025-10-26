import psycopg2

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

    sql_db = '''CREATE DATABASE {database};'''.format(database=database)
    
    cursor.execute(sql_db)
    cursor.execute('''GRANT ALL PRIVILEGES ON DATABASE {database} TO {user};'''.format(database=database, user='postgres'))
    cursor.execute(sql)
    conn.commit()
    conn.close()