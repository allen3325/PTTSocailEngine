from collections import Counter
from NCHU_nlptoolkit.cut import *
import requests
from text_cleaner.text_cleaner import Text_Cleaner
import json
from GoogleNews import GoogleNews
from bs4 import BeautifulSoup
import time


class Finance_hot_fetcher:
    def __init__(self, K, news_K, news_period):
        self.tc = Text_Cleaner()
        self.all_contents = []
        self.frequency_counting_table = []
        self.company_file = open("./data/上市公司基本資料.json")
        self.all_company = json.load(self.company_file)
        self.complexity_companies = self.__load_complexity_companies()
        self.K = K
        self.news_K = news_K
        self.news_period = news_period

    def fetch_hot_company_today(self, start, end, size, page):
        url = f"https://ptt-search.nlpnchu.org/api/GetByBoard?board=Stock&start={start}&end={end}&size={size}&from={page}"
        f = requests.get(url)
        res = f.json()
        for content in res["hits"]:
            self.all_contents += list(
                cut_sentence(
                    self.tc.clean_text(content["_source"]["content"]), minword=2
                )
            )
        self.frequency_counting_table = dict(Counter(self.all_contents))
        self.frequency_counting_table = sorted(
            self.frequency_counting_table.items(), key=lambda x: x[1], reverse=1
        )
        hot_company_today = self.filt_company(self.frequency_counting_table)[0 : self.K]
        all_company_info = self.fetch_all_company_info(hot_company_today)
        return all_company_info

    def __load_complexity_companies(self):
        with open("./data/易混淆公司.txt", "r", encoding="utf-8") as file:
            complexity_companies = set(word.strip() for word in file)
        return complexity_companies

    def __search_in_all_company(self, value: str):
        for company in self.all_company:
            if value not in self.complexity_companies:
                if value == company["公司代號"] or value in company["公司簡稱"]:
                    print(f"value is {value}, company['公司代號'] is {company['公司代號']}, company['公司簡稱'] is {company['公司簡稱']}")
                    return company["公司簡稱"]
            else:
                if value == company["公司代號"] or value == company["公司簡稱"]:
                    print(f"value is {value}, company['公司代號'] is {company['公司代號']}, company['公司簡稱'] is {company['公司簡稱']}")
                    return company["公司簡稱"]

    def filt_company(self, topK: list):
        companines = []
        for K in topK:
            company_name = self.__search_in_all_company(K[0])
            if company_name:
                new_tuple = (company_name, K[1])
                companines.append(new_tuple)

        return companines

    def get_company_news(self, company):
        googlenews = GoogleNews(
            lang="zh-TW", encode="utf-8", period=f"{self.news_period}d"
        )
        googlenews.enableException(True)
        googlenews.get_news(company)
        all_news = googlenews.results(sort=True)
        googlenews.clear()
        return all_news

    def fetch_company_news_content(self, company_name, company_news):
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/87.0.4280.141 Safari/537.36"
        }
        for news in company_news:
            time.sleep(0.5)
            contents = ""
            url = news["link"]
            # print(f'url is {url}')
            response = requests.get(f"https://{url}", headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            newsUrl = soup.find_all("c-wiz", class_="qFYwOb")[0].find("a").getText()

            # 取得該篇新聞連結內容
            response = requests.get(newsUrl, headers=headers)
            soup = BeautifulSoup(response.text, "html.parser")
            all_p = soup.find_all("p")

            for p in all_p:
                contents += p.getText().strip()

            news["content"] = contents
            news["company"] = company_name
            if "datetime" in news:
                del news["datetime"]
            if "desc" in news:
                del news["desc"]
            if "date" in news:
                del news["date"]
            if "link" in news:
                del news["link"]
            if "img" in news:
                del news["img"]
            if "media" in news:
                del news["media"]
            if "site" in news:
                del news["site"]
            

        return company_news

    def fetch_company_info(self, company, freq):
        company_news_K = self.get_company_news(company=company)[0 : self.news_K]
        print("=" * 80)
        print(f"company is {company} frequency is {freq}\n Fetching...")
        company_news_K = self.fetch_company_news_content(
            company_name=company, company_news=company_news_K
        )
        print("=" * 80)
        return company_news_K

    def fetch_all_company_info(self, hot_company_today):
        all_company_info = []
        for company, freq in hot_company_today:
            all_company_info.append(self.fetch_company_info(company, freq))

        return all_company_info
