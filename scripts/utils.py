"""Script with re-usable functions."""
import requests
import os
from dotenv import load_dotenv
import fsspec

load_dotenv()

AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')


def download_file(link: str, write_path: str) -> None:
    """Download a file with requests.

    Parameters
    ----------
    link: str
        The download link.

    write_path: str
        The local path to write to.
    """
    response = requests.get(link)

    with open(write_path, 'wb') as file:
        file.write(response.content)


def copy_to_s3(local_path: str, s3_path: str) -> None:
    """Copy a local file to s3 with fsspec.

    Parameters
    ----------
    local_path: str
        The local path of the file.

    s3_path: str
        The s3 path.
    """
    s3_filesystem = fsspec.filesystem(
        's3',
        key=AWS_ACCESS_KEY,
        secret=AWS_SECRET_KEY,
        client_kwargs={'region_name': 'eu-west-1'}
    )
    s3_filesystem.put(local_path, s3_path)
