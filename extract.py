import argparse
import utils
import urllib
from utils.file import FileUtil
from utils import request_api
from requests import RequestException
from bs4 import BeautifulSoup
from utils.regex_utils import SPLITTER_RE, NON_MM_RE
from word_breaker.word_segment_v5 import WordSegment
import time
import re
import os

parser = argparse.ArgumentParser(description="Web Crawler for Burmese wiki.")
parser.add_argument("-l", '--log_dir', action='store', type=str,
                    default='logs', help='Specify logs directory for errors')

# parser.add_argument('--word_seg', '-ws',
#                     action='store_true', help='Whether to segment word on text corpus.')

parser.add_argument('--max_size', type=int, default=1000,
                    help="Specify max size (in MB) to crawl wiki.")

parser.add_argument("--output_dir", '-o', type=str,
                    default="results", help="Output directory for storing corpus (default: results)")

args = parser.parse_args()

WIKI_URL = "https://my.wikipedia.org/wiki/"

MEDIA_API_URL = "https://my.wikipedia.org/w/api.php"

# word_segmenter = WordSegment()

PAGES_PER_REQUEST = 500

current_params = {'action': 'query', 'format': 'json',
                  'apfrom': 'က', 'aplimit': PAGES_PER_REQUEST, 'list': 'allpages'}

# print(len(utils.request_api(args.url, init_params)['query']['pages']))

file_util = FileUtil(args.max_size)


# print(request_api(args.api_url, init_params))

# json_res = request_api(args.api_url, init_params)
#
# # print(type(json_res['query']['pages']))
#
# for key, value in json_res['query']['pages'].items():
#     print("Wiki title", value['title'])


def process_api():
    page_titles = []
    json_res = request_api(MEDIA_API_URL, current_params)
    for value in json_res['query']['allpages']:
        page_titles.append(value['title'])
    return page_titles


def crawl_wiki():
    articles_batch_idx = 0
    # try:
    #     start_time = time.time()
    #     raw_html = utils.simple_get(args.url + 'ကချင်ဒီမိုကရေစီသစ် တပ်မတော်')
    #     if raw_html is not None:
    #         if file_util.check_storage():
    #             html = BeautifulSoup(raw_html, 'html.parser')
    #             content = str(html.find(id="content").text)
    #             # print(content)
    #             sentences = re.split(SPLITTER_RE, content)
    #             sentences = [re.sub(NON_MM_RE, '', sentence) for sentence in sentences]
    #             print("Content list len", len(sentences))
    #             file_util.save_to_txt_file('test.txt', sentences)
    #             stop_time = time.time()
    #             print("Total time passed: ", stop_time - start_time, "sec")
    #         else:
    #             print("specified maximum size reached")
    #             return
    # except RequestException as e:
    #     print(e)
    #     utils.log_error(e, args.log_dir)
    meta_dict = FileUtil.load_meta_dict(args.output_dir)
    if len(list(meta_dict.keys())) > 0:
        last_key = list(meta_dict.keys())[-1]
        current_params['apfrom'] = meta_dict[last_key]
        articles_batch_idx = last_key
        print("continue from batch index {}, Page Title: {}".format(articles_batch_idx, current_params['apfrom']))

    try:
        while file_util.check_storage():
            page_titles = process_api()
            print("processing articles batch", articles_batch_idx)
            file_name = 'mywiki-batch-{}.txt'.format(articles_batch_idx)
            FileUtil.delete_file(os.path.join(args.output_dir, file_name))
            for page_title in page_titles:
                raw_html = utils.simple_get(urllib.parse.urljoin(WIKI_URL, page_title))
                if raw_html is not None:
                    html = BeautifulSoup(raw_html, 'html.parser')
                    content = str(html.find(id="content").get_text())
                    # print(html.find_all('p'))
                    # print(content)
                    # sentences = re.split(SPLITTER_RE, content)
                    sentences = content.split("။")
                    sentences = [re.sub(NON_MM_RE, '', sentence) for sentence in sentences]
                    # file_util.save_to_txt_file('test.txt', sentences)

                    file_util.save_to_txt_file(file_name, sentences,
                                               output_dir=args.output_dir)
                else:
                    print("article is empty. Title: {}".format(page_title))
            articles_batch_idx = articles_batch_idx + 1
            current_params['apfrom'] = json_res['continue']['apcontinue']
            meta_dict[articles_batch_idx] = current_params['apfrom']
    except RequestException as e:
        print(e)
        utils.log_error(e, args.log_dir)


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
