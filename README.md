# Myanmar Wiki Crawler

![](https://img.shields.io/badge/python-3.6-blue.svg)
![](https://img.shields.io/badge/License-MIT-green)

Simple program for crawling [Burmese Wikipedia](https://my.wikipedia.org) using media wiki API by querying page from "က" first and **sequentially** crawling until specified size reaches or no more pages to crawl.

[TOC]

## Getting started

Install requirements and you are good to go.

```shell script
pip install -r requirements.txt
```

## Usage

```

python extract.py -h

usage: extract.py [-h] [-l LOG_DIR] [--max_size MAX_SIZE]
                  [--output_dir OUTPUT_DIR]

Web Crawler for Burmese wiki.

optional arguments:
  -h, --help            show this help message and exit
  -l LOG_DIR, --log_dir LOG_DIR
                        Specify logs directory for errors (default: logs)
  --max_size MAX_SIZE   Specify max size (in MB) to crawl wiki. (default: 1000)
  --output_dir OUTPUT_DIR, -o OUTPUT_DIR
                        Output directory for storing corpus (default: results)

```

## License

[MIT license](/License.md)



