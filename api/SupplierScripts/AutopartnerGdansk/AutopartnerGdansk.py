import pandas as pd


path = ('../../../TemporaryStorage/AUTO_PARTNER_GDANSK/files/autopartner_gdansk_data.csv')
df = pd.read_csv(path, sep=';', encoding_errors='ignore', error_bad_lines=False,
                 low_memory=False, encoding="utf-8")
print(df)