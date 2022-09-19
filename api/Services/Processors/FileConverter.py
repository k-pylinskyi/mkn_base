import os
import csv
import pandas as pd


def convert(file_path):
    if file_path.lower().endswith(('.xlsx', 'xls')):
        convert_excel(file_path)
    else:
        convert_csv(file_path)

def convert_excel(file_path):
    df = pd.read_excel(file_path)
    df.to_csv(file_path)


def convert_csv(file_path):
    file_separator = detect_delimiter(file_path, 5)
    df = pd.read_csv(file_path, sep=file_separator)
    print(df.head())
    df.to_csv(file_path, sep='\t')


def get_delimiter(file_path):
    with open(file_path, 'r', encoding="utf8") as csvfile:
        delimiter = str(csv.Sniffer().sniff(csvfile.read()).delimiter)
        return delimiter


def head(filename: str, n: int):
    try:
        with open(filename, encoding="utf-8") as f:
            head_lines = [next(f).rstrip() for x in range(n)]
    except StopIteration:
        with open(filename) as f:
            head_lines = f.read().splitlines()
    return head_lines


def detect_delimiter(filename: str, n=5):
    sample_lines = head(filename, n)
    common_delimiters = [',', ';', '\t', '|', ':']
    for d in common_delimiters:
        ref = sample_lines[0].count(d)
        if ref > 0:
            if all([ref == sample_lines[i].count(d) for i in range(1, n)]):
                return d
    return ';'


class FileConverter:
    def __init__(self):
        root_dir = 'D:\\Work\\MNK_PRICES\\DB_FILES'
        self.suppliers = os.listdir(root_dir)

    def convert_all(self):
        for supplier in self.suppliers:
            files = os.listdir(os.path.join(supplier, 'files'))
            for file in files:
                file = os.path.join(supplier, 'files', file)
                convert(file)
                print('{} converted'.format(file))
