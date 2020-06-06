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

## Step-by-step Procedure

- This program will first query for pages using Media Wiki API to get page titles in batches (500 pages per batch - maximum page limit allowed by Media Wiki).

- It then uses these titles to make html request to individual page and collect text from content field of that page.

- It then stores text into file by using sentence-level segmentation  and regex to store only Burmese characters. (from unicode u1000 to u1100).

- It stores one text file per batch using batch index which starts from 0.



## TODOS

- Sending Request concurrently to maximize network utilization.

- Remove max_size limit.

- Better filtering of burmese characters.

- Optimize corpus storing.

## License

[MIT license](/License.md)



