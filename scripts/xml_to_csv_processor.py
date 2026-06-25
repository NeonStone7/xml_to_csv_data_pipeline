import pandas as pd
import os
import xml.etree.ElementTree as ET
import logging
# pd.set_option('display.max_column_name', None)
INPUT_FILEPATH = 'datasets/extracted_data'
OUTPUT_FILEPATH = 'datasets/output_data'
files = os.listdir(INPUT_FILEPATH)
NS = "urn:iso:std:iso:20022:tech:xsd:auth.036.001.02"
record_tag = f"{{{NS}}}TermntdRcrd"

os.makedirs(OUTPUT_FILEPATH, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def convert_xml_to_csv(file: str):
    
    all_rows = []

    # parse the xml file
    tree = ET.parse(f'{INPUT_FILEPATH}/{file}')

    # ----extract column names ----
    logger.info('extracting the column names.....')
    elemlist = []
    for elem in tree.iter():
        elemlist.append(elem.tag.split('}')[-1])

    elemlist = set(elemlist)

    # --- retrieve rows ---
    logger.info('retrieving rows.....')
    for _, elem in ET.iterparse(f"{INPUT_FILEPATH}/{file}", events=("end",)):

        if elem.tag == record_tag:
            row = {col: elem.findtext(f".//{{{NS}}}{col}") for col in elemlist}
            all_rows.append(row)
            elem.clear()
            
    # convert to pandas df and write to csv
    logger.info('Writing to csv....')
    df = pd.DataFrame(all_rows)
    df.to_csv(f'{OUTPUT_FILEPATH}/{file.replace('.xml', '')}.csv', index=False)


for file in files:
    convert_xml_to_csv(file)