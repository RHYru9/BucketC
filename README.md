## Usage

To use BucketSnatch, run the following command in your terminal:

```bash
python3 scr.py -u 'target url' -f /folder -b mov mp4 jpg jpeg png
```

### Parameters:

- `-u` or `--url`: The target URL to crawl. This should be the URL of the XML bucket you want to scrape.
- `-f` or `--folder`: The folder path where you want to save the downloaded files.
- `-b` or `--blacklist`: A space-separated list of file extensions to blacklist (exclude from downloading). For example, to exclude video and image files, use: `mov mp4 jpg jpeg png`.

### Example:

```bash
python3 scr.py -u 'http://example.domain' -f /path/to/save/folder -b mov mp4 jpg jpeg png
```

This command will:
- Crawl the XML at `http://example.domain`.
- Save the downloaded files to `/path/to/save/folder`.
- Exclude files with the extensions `.mov`, `.mp4`, `.jpg`, `.jpeg`, and `.png`.
