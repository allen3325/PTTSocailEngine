from fastapi import FastAPI
import sys
sys.path.append('word_cloud')
sys.path.append('word_fetcher')
from word_cloud import Word_Cloud
from word_fetcher import Word_Fetcher
app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello Test"}

@app.get("/test")
async def test_font_path():
    wc = Word_Cloud()
    return wc.test()


@app.get("/wordcloud/{search_keyword}")
async def generate_word_cloud(search_keyword, K: int = 100):
    print(f"search_keyword is {search_keyword}.")
    wc = Word_Cloud()
    return wc.generate_word_cloud(search_keyword, K)

@app.get("/word_fetcher/{search_keyword}")
async def generate_dictionary(search_keyword, K: int = 100):
    print(f"search_keyword is {search_keyword}.")
    wf = Word_Fetcher()
    return wf.generate_dictionary(search_keyword, K)