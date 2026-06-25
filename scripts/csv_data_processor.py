"""Process csv files and write to s3."""
import os
import pandas as pd
from utils import copy_to_s3

# VARIABLES
INPUT_FILEPATH = 'datasets/output_data'
OUTPUT_FILEPATH = 'datasets/final_data'


def transform_data(filename: str) -> None:
    """Perform transformations on a csv file.

    Parameters
    ----------
    filename: str
        The local path of the csv file.

    """
    try:
        df = pd.read_csv(f'{INPUT_FILEPATH}/{filename}')
        df.columns = [column.replace('TermntdRcrd.', '')
                      for column in df.columns]

        df['a_count'] = (
            df['FinInstrmGnlAttrbts.FullNm']
            .apply(lambda x: x.lower().count('a'))
            )
        df['contains_a'] = (
            df['a_count']
            .apply(lambda x: 'YES' if x > 0 else 'NO')
            )

        df.to_csv(f'{OUTPUT_FILEPATH}/{filename.replace('.csv', '')}.csv',
                  index=False)

    except Exception as e:
        print(e)


# transform and copy to s3
files = os.listdir(INPUT_FILEPATH)
os.makedirs(OUTPUT_FILEPATH, exist_ok=True)

for file in files:
    try:
        transform_data(file)

        local_path = f'{OUTPUT_FILEPATH}/{file}'
        s3_path = f's3://curated-datasets-oamen/output_xml_to_csv/{file}'
        copy_to_s3(local_path, s3_path)
    except Exception as e:
        print(e)
        continue
