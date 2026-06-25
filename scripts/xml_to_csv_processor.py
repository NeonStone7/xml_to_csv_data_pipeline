"""Extract the XML data and write to csv."""
import pandas as pd
import os
import xml.etree.ElementTree as ET
import logging


# ---build logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# --variables--
INPUT_FILEPATH = 'datasets/extracted_data'
OUTPUT_FILEPATH = 'datasets/output_data'
files = os.listdir(INPUT_FILEPATH)
NS = "urn:iso:std:iso:20022:tech:xsd:auth.036.001.02"
record_tag = f"{{{NS}}}TermntdRcrd"

os.makedirs(OUTPUT_FILEPATH, exist_ok=True)


def recursive_flatten(element: ET, parent_key: str = '') -> dict:
    """Recursively flatten data within XML file.

    Parameters
    ----------
    element: ElementTree
        The element tree.

    parent_key: str
        The parent key

    Returns
    -------
    dict
        The extracted rows.
    """
    data = {}

    # strip ns from the tag
    tag = element.tag.split('}', 1)[-1]

    key = f'{parent_key}.{tag}' if parent_key else tag

    # if the element has no children, return the text value
    if len(element) == 0:
        data[key] = (element.text or '').strip()
        return data

    # if the element has children, recursively flatten them
    for child in element:
        data.update(recursive_flatten(child, key))

    return data


def xml_to_csv(path: str) -> pd.DataFrame:
    """Parse an XML into a pandas dataframe.

    Parameters
    ----------
    path: str
        The local path of the xml file.

    Returns
    -------
    pd.DataFrame
        The pandas dataframe.
    """
    tree = ET.parse(path).getroot()
    rows = tree.findall(f'.//{record_tag}')

    all_data = [recursive_flatten(row) for row in rows]

    # write to pandas df
    df = pd.DataFrame(all_data)

    return df


# --- parse and save to csv
files = os.listdir(INPUT_FILEPATH)
paths = {file.split('.')[0]: f'{INPUT_FILEPATH}/{file}' for file in files}


for filename, input_path in paths.items():

    logger.info('Extracting data...')
    df = xml_to_csv(input_path)

    df.to_csv(f'{OUTPUT_FILEPATH}/{filename}.csv', index=False)
