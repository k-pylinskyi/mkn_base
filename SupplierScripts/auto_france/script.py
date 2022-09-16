import os

import pandas as pd

isExist = os.path.exists('../../temp_storage/AUTO_FRANCE')
print(isExist)

tmp = pd.read_csv('../../temp_storage/AUTO_FRANCE/files/autofrance_data.txt')
