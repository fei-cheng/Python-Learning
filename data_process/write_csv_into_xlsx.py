import os
import sys
import csv
import xlsxwriter

def write_csv_into_xlsx(output_path, input_path_list):
    workbook = xlsxwriter.Workbook(output_path)
    for csv_file_path in input_path_list:
        if not csv_file_path.endswith('.csv'):
            continue
        basename = (os.path.basename(csv_file_path))[:-4]
        worksheet = workbook.add_worksheet(basename)
        with open(csv_file_path, 'rb') as csv_file:
            csv_reader = csv.reader(csv_file)
            row = -1
            for line in csv_reader:
                row += 1
                worksheet.write_row(row, 0, line)
    workbook.close()

"""
    Called by "python write_csv_into_xlsx.py   A_B.xlsx  A.csv  B.csv"
"""
if __name__ == '__main__':
    write_csv_into_xlsx(sys.argv[1], sys.argv[1:])
