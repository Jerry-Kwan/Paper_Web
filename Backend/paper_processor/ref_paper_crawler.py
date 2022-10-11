import os
import difflib
import requests
from bs4 import BeautifulSoup
from .paper_pdf_ext import PaperPdfExtract


def get_similar_rate(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


class RefPaperCrawler:
    def __init__(self, ref_author_list, ref_list):
        self.HEADERS = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)\
            Chrome/55.0.2883.87 Safari/537.36'
        }
        self.URL_QUERY_AUTHOR = 'https://dblp.org/search?q='
        self.CLASS_PAPER = 'entry'
        self.REPLACED_CHAR = [' ', '-', '?', '.', ':']
        self.THRESHOLD = 0.95
        self.ref_author_list = ref_author_list
        self.ref_list = ref_list
        self.ref_num = len(ref_list)

    def get_bib(self, no):
        if self.ref_author_list[no - 1] is None:
            return None

        # only use lower case chars to match
        ss = self._get_replaced_str(self.ref_list[no - 1]).lower()
        lenss = len(ss)

        # search each author
        for au in self.ref_author_list[no - 1]:
            url = self.URL_QUERY_AUTHOR + au.replace(' ', '%20')
            hide_body = BeautifulSoup(requests.get(url, headers=self.HEADERS).content,
                                      'lxml').find(id='completesearch-authors').find(class_='body hide-body')

            # no Exact matches
            if str(hide_body).find('Exact matches') == -1:
                continue

            url = hide_body.find(class_='result-list').find('a')['href']
            hideable = BeautifulSoup(requests.get(url, headers=self.HEADERS).content,
                                     'lxml').find(id='publ-section').find_all(class_='hideable')

            # no paper by this author
            if len(hideable) == 0:
                continue

            for h in hideable:
                entries = h.find(class_='publ-list').find_all(class_=self.CLASS_PAPER)

                # inspect each doc
                for e in entries:
                    title = self._get_replaced_str(str(
                        e.find(class_='data tts-content').find(class_='title').string)).lower()

                    deleted = 0
                    lent = len(title)

                    while lenss - deleted >= lent:
                        if get_similar_rate(ss[deleted:deleted + lent], title) > self.THRESHOLD:
                            url = e.find(class_='publ').find_all(class_='drop-down')[1].find(
                                class_='head').find('a')['href']
                            return self._crawl_bib(url)

                        deleted += 1

        return None

    def _get_replaced_str(self, str):
        for c in self.REPLACED_CHAR:
            str = str.replace(c, '')

        return str

    def _crawl_bib(self, url):
        return str(
            BeautifulSoup(requests.get(url, headers=self.HEADERS).content,
                          'lxml').find(id='bibtex-section').find(class_='verbatim select-on-click').string)


if __name__ == '__main__':
    test_path = '../../tests/testfiles/'
    ignore_file = {'.DS_Store', 'cvpr_2021_01.pdf', 'GLAC.pdf'}

    for name in os.listdir(test_path):
        if name in ignore_file:
            continue

        ppe = PaperPdfExtract(test_path + name)
        rpc = RefPaperCrawler(ppe.partial_ref_author, ppe.clean_split_ref_text)
        print(rpc.get_bib(1))
        print(rpc.get_bib(9))
        input('pause')
