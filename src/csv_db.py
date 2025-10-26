import psycopg2
import csv

database = input('d: ').strip()

def convert(file_name, input_file, output_file):
     csv = csv.reader(open(input_file))
     database = database
     table = file_name
     columns = list(next(csv.reader(open(input_file))))[0][0]

     schema = {}
     conn = psycopg2.connect(database = database,
                        user = 'postgres',
                        password = 'c4dc3571c4794f10b3d7ba8c8d83e50f',
                        host = 'localhost',
                        port = 5432)
     cursor = conn.cursor()

     csv_db = '''COPY {table}({columns})
     FROM '{input_file}'
     DELIMITER ','
     CSV HEADER;'''.format(table=table, columns=columns, input_file=input_file)

     cursor.execute(csv_db)
     conn.commit()