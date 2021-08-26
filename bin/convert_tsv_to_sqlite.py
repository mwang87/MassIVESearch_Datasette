from pathlib import Path
import sys
import sqlite3
import csv_to_sqlite
import csv
import argparse


csv.field_size_limit(sys.maxsize)

def result_file_name(result_file, result_view_name):
    return f'{result_view_name}-main_{result_file.with_suffix(".db").name}'

def rename_table(db, table_name, index_columns):
    renameTable = 'ALTER TABLE "{}" RENAME TO Result'.format(table_name)
    print(renameTable)
    indexOperations = []
    for index in index_columns:
        index_name = index.replace(' ','_').replace('+','_')
        index_columns = ','.join(['"{}"'.format(i) for i in index.split('+') if i != ''])
        indexOperations.append('CREATE INDEX index_{} ON Result ({})'.format(index_name, index_columns))
    connection  = sqlite3.connect(db)
    cursor      = connection.cursor()
    cursor.execute(renameTable)
    for indexOperation in indexOperations:
        print(indexOperation)
        cursor.execute(indexOperation)

def run_mysql_convert(result_file, result_view_name, index_columns, output_folder):
    db = output_folder.joinpath(result_file_name(result_file, result_view_name))
    # all the usual options are supported
    delimiter = '\t'
    if 'csv' in result_file.name:
        delimiter = ','
    options = csv_to_sqlite.CsvOptions(delimiter=delimiter)
    print([str(result_file)])
    csv_to_sqlite.write_csv([str(result_file)], str(db), options)
    rename_table(db,result_file.stem, index_columns)

def main():
    # parser = argparse.ArgumentParser(description='Convert tsv to sqlite')
    # parser.add_argument('integers', 
    #                     help='an integer for the accumulator')
    # # parser.add_argument('--sum', dest='accumulate', action='store_const',
    # #                     const=sum, default=max,
    # #                     help='sum the integers (default: find the max)')

    # args = parser.parse_args()


    output_folder = Path(sys.argv[1])
    outputs = sys.argv[2:]

    if len(outputs) % 1 == 1:
        raise Exception("All outputs must be paired (-result_view_name result_view_file:index1,index2)")

    grouped_outputs = [(outputs[2*i].split(':')[0][1:],Path(outputs[2*i+1]),[s for s in outputs[2*i].split(':')[1].split(',') if s != '']) for i in range(int(len(outputs)/2))]

    for (result_view_name, result_file, index_columns) in grouped_outputs:
        run_mysql_convert(result_file, result_view_name, index_columns, output_folder)

if __name__ == '__main__':
    main()
