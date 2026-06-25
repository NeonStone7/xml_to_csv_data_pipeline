"""Download xml files and extract the zipped files."""
import logging
from xml.etree import ElementTree as ET
import zipfile
from utils import download_file
import os

# build logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# create dir
os.makedirs('datasets/raw_data/', exist_ok=True)

# ----variables----
LINK = "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&indent=true&start=0&rows=100"  # noqa: E501
ORIGINAL_XML_FILEPATH = 'datasets/raw_data/all_xml.xml'
OUTPUT_FILEPATH = 'datasets/raw_data/{filename}.zip'


# ------ download initial xml file ------
logger.info('Downloading from original link....')
download_file(LINK, ORIGINAL_XML_FILEPATH)


# ---- parse the xml to retreive the download_link and filename ------
links = {}


def parse_xml():
    """Parse XML file."""
    logger.info('Parsing xml.....')
    # ET.parse() loads the XML file into an element tree.
    # getroot() retrieves the root element of the XML structure
    tree = ET.parse(ORIGINAL_XML_FILEPATH).getroot()

    try:
        for element in tree.iter():
            if (element.tag == 'str' and element.attrib.get('name') == 'download_link'):  # noqa: E501
                download_link = element.text

                filename = download_link.split('/')[-1].split('.')[0]

                # extract second zipped file
                if 'DLTINS_20210119_01of02' in filename:
                    links[filename] = download_link

    except Exception as e:
        logger.error(e)


parse_xml()


# ------ download the zipped files
for filename in links:

    # download the zipped files
    logger.info(f'Downloading file: {filename}')
    download_file(links[filename], OUTPUT_FILEPATH.format(filename=filename))

    # list out the files under the zipped file
    filename_under_zip = zipfile.ZipFile(OUTPUT_FILEPATH.format(filename=filename), 'r').namelist()[0]  # noqa: E501

    # create an object of the downloaded zipped file
    zobject = zipfile.ZipFile(OUTPUT_FILEPATH.format(filename=filename))

    # extract file
    zobject.extract(filename_under_zip, 'datasets/extracted_data')
    logger.info(f'Extracted file: {filename_under_zip}')

    zobject.close()
