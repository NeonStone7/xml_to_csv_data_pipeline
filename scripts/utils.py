import requests

def download_file(link: str, write_path: str) -> None:

    response = requests.get(link)

    with open(write_path, 'wb') as file:
        file.write(response.content)