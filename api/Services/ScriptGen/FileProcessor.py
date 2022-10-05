import pandas as pd


class FileProcessor:
    def __init__(self):
        pass

    def process_file(self, params, url):
        processed_file = pd.read_csv(
            url,
            encoding_errors=params['encoding_errors'],
            sep=params['sep'],
            header=params['header'],
            low_memory=params['low_memory'],
            compression=params['compression'],
            on_bad_lines=params['error_bad_lines'],
            usecols=params['usecols'],
            skiprows=params['skiprows'],
            engine=params['engine'],
            decimal=params['decimal'],
        ) 

        print(processed_file)
