from fastapi import FastAPI
from word_cloud.word_cloud import Word_Cloud
from word_fetcher.word_fetcher import Word_Fetcher
from comment_fetcher.comment_fetcher import Comment_Fetcher
from text_cleaner.text_cleaner import Text_Cleaner
from article_fetcher.article_fetcher import Article_Fetcher
from analyzer.analyzer import Analyzer

app = FastAPI()


@app.get("/article/{keyword}",description='keyword: 關鍵字, tag: 分類標籤(預設 None), K: TOP K, size: 搜尋幾個(預設100), start: 開始的timestamp(預設 None), end: 結束的timestamp(預設 None)\n 若預設為 None，代表為全抓。')
async def get_article_by_keyword(keyword: str, tag: str = None, K: int = 5, size: int = 100, start: int = None, end: int = None):
    af = Article_Fetcher()
    return af.get_article_by_keyword(keyword=keyword, tag=tag, K=K, size=size, start=start, end=end)


@app.get("/analyze/{keyword}",description='keyword: 關鍵字, tag: 分類標籤(預設 None), K: TOP K, size: 搜尋幾個(預設100), start: 開始的timestamp(預設 None), end: 結束的timestamp(預設 None)\n 若預設為 None，代表為全抓。')
async def analyze_by_keyword(keyword: str, tag: str = None, K: int = 5, size: int = 100, start: int = None, end: int = None):
    analyzer_test = Analyzer()
    return analyzer_test.prompt_analyzer(keyword=keyword, tag=tag, K=K, size=size, start=start, end=end)

@app.get("/word/cloud/{search_keyword}")
async def generate_word_cloud(search_keyword, K: int = 100):
    print(f"search_keyword is {search_keyword}.")
    wc = Word_Cloud()
    return wc.generate_word_cloud(search_keyword, K)


@app.get("/word/dict/{search_keyword}")
async def generate_dictionary(search_keyword, K: int = 100):
    print(f"search_keyword is {search_keyword}.")
    wf = Word_Fetcher()
    return wf.generate_dictionary(search_keyword, K)