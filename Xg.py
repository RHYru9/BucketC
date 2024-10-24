import requests
from bs4 import BeautifulSoup
import os
import argparse

def download_file(url, save_path):
    """Download a file from the given URL and save it to the specified path."""
    try:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, 'wb') as f:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print(f"[+] {url} saved to {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"[-] Failed to download {url}: {e}")

def is_blacklisted(path, blacklist):
    """Check if the file extension is blacklisted."""
    extension = os.path.splitext(path)[1].lstrip(".").lower()
    return extension in blacklist

def crawl_and_save(base_url, folder, blacklist):
    """Crawl the given URL, extract file keys, and save them."""
    try:
        folder = os.path.abspath(folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        print(f"[+] Crawling {base_url}")

        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'xml')

        keys = soup.find_all('Key')
        downloaded_files = set()

        for key in keys:
            path = key.text.strip()

            if path.endswith('/'):
                print(f"[-] Skipping directory: {path}")
                continue

            if is_blacklisted(path, blacklist):
                print(f"[-] {path} is blacklisted. Skipping...")
                continue

            file_url = f"{base_url.rstrip('/')}/{path}"
            save_path = os.path.join(folder, path)

            if path not in downloaded_files and not os.path.exists(save_path):
                print(f"[*] Downloading: {file_url}")
                download_file(file_url, save_path)
                downloaded_files.add(path)
            else:
                print(f"[-] {file_url} already exists. Skipping...")

    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Crawl XML Key URLs and download files.")
    parser.add_argument("-u", "--url", required=True, help="Base URL to crawl")
    parser.add_argument("-f", "--folder", required=True, help="Folder to save downloaded files")
    parser.add_argument("-b", "--blacklist", nargs='+', help="Extensions to blacklist, e.g., 'mov mp4'", default=[])
    args = parser.parse_args()

    blacklist = [ext.lower() for ext in args.blacklist]

    crawl_and_save(args.url, args.folder, blacklist)
