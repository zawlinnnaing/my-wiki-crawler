import argparse
import utils
import urllib
import multiprocessing as mp
from utils.file import FileUtil
from utils.timer import Timer
from utils.helper import request_api, log_error, simple_get
from requests import RequestException
from bs4 import BeautifulSoup
from utils.regex_utils import SPLITTER_RE, MM_RE
from word_breaker.word_segment_v5 import WordSegment
import time
import re
import os

parser = argparse.ArgumentParser(description="Web Crawler for Burmese wiki.")
parser.add_argument("-l", '--log_dir', action='store', type=str,
                    default='logs', help='Specify logs directory for errors (default: logs')

# parser.add_argument('--word_seg', '-ws',
#                     action='store_true', help='Whether to segment word on text corpus.')

parser.add_argument("-cpu", "--cpu_num", type=int, help="Number of cpu to use parallelization. (default: 4)", default=4)

parser.add_argument('--max_size', type=int, default=1000,
                    help="Specify max size (in MB) to crawl wiki. (default: 1000")

parser.add_argument("--output_dir", '-o', type=str,
                    default="results", help="Output directory for storing corpus (default: results)")

args = parser.parse_args()

mpPool = mp.Pool()

WIKI_URL = "https://my.wikipedia.org/wiki/"

MEDIA_API_URL = "https://my.wikipedia.org/w/api.php"

# Please do not change this to prevent putting load on wiki server.
PAGES_PER_REQUEST = 500

current_params = {'action': 'query', 'format': 'json',
                  'apfrom': 'က', 'aplimit': PAGES_PER_REQUEST, 'list': 'allpages'}

# print(len(utils.request_api(args.url, init_params)['query']['pages']))

file_util = FileUtil(args.max_size)


def process_api():
    page_titles = []
    json_res = request_api(MEDIA_API_URL, current_params)
    for value in json_res['query']['allpages']:
        page_titles.append(value['title'])
    return page_titles, json_res


def parse_page(page_title: str, file_name: str):
    """
    @param page_title: Title of wiki page
    @param file_name: File name to be saved.
    """
    raw_html = simple_get(urllib.parse.urljoin(WIKI_URL, page_title))
    if raw_html is not None:
        html = BeautifulSoup(raw_html, 'html.parser')
        content = str(html.find(id="content").get_text())

        sentences = content.split("။")
        sentences = [''.join(re.findall(MM_RE, sentence)) + "။" if sentence is not "\n" else '' for sentence
                     in sentences]
        FileUtil.save_to_txt_file(file_name, sentences, output_dir=args.output_dir)
    else:
        print("article is empty. Title: {}".format(page_title))


def crawl_wiki():
    articles_batch_idx = 0
    meta_dict = FileUtil.load_meta_dict(args.output_dir)
    if len(list(meta_dict.keys())) > 0:
        last_key = list(meta_dict.keys())[-1]
        current_params['apfrom'] = meta_dict[last_key]
        articles_batch_idx = int(last_key) + 1
        print("continue from batch index {}, Page Title: {}".format(articles_batch_idx, current_params['apfrom']))

    try:
        while file_util.check_storage():
            start_time = time.perf_counter()
            page_titles, json_res = process_api()
            print("processing articles batch", articles_batch_idx)
            file_name = 'mywiki-batch-{}.txt'.format(articles_batch_idx)
            file_path = os.path.join(args.output_dir, file_name)
            FileUtil.delete_file(file_path)
            # Sequential executing
            # for page_title in page_titles:
            # raw_html = utils.simple_get(urllib.parse.urljoin(WIKI_URL, page_title))
            # if raw_html is not None:
            #     html = BeautifulSoup(raw_html, 'html.parser')
            #     content = str(html.find(id="content").get_text())
            #
            #     sentences = content.split("။")
            #     sentences = [''.join(re.findall(MM_RE, sentence)) + "။" if sentence is not "\n" else '' for sentence
            #                  in sentences]
            #     file_util.save_to_txt_file(file_name, sentences,
            #                                output_dir=args.output_dir)
            # else:
            #     print("article is empty. Title: {}".format(page_title))

            # Parallel Executing
            with Timer(articles_batch_idx):
                with mp.Pool(args.cpu_num) as p:
                    p.starmap(parse_page, [(page_title, file_name) for page_title in page_titles])

            file_util.add_storage(file_path)
            current_params['apfrom'] = json_res['continue']['apcontinue']
            meta_dict[str(articles_batch_idx)] = current_params['apfrom']
            FileUtil.save_meta_dict(meta_dict, args.output_dir)
            print("Saved batch index {} \n\n".format(articles_batch_idx))
            articles_batch_idx = articles_batch_idx + 1
    except RequestException as e:
        print(e)
        log_error(e, args.log_dir)


def add_norm_words_to_words_set(normalized_words: list, words_set: set):
    """
    normalized_words -- Normalized words got from word breaker.
    words_set -- Words set to add words from word breaker. 
    """
    for words in normalized_words:
        for word in words:
            words_set.add(word)


if __name__ == '__main__':
    crawl_wiki()
