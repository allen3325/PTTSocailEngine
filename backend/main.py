from fastapi import FastAPI
import sys
sys.path.append('word_cloud')
from word_cloud import Word_Cloud
sys.path.append('comment_fetcher')
from comment_fetcher import Comment_Fetcher
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

@app.get("/getcomment/{article_id}")
async def generate_word_cloud(article_id: str, start: int = None, end: int = None):
    cf = Comment_Fetcher()
    return cf.get_comment_list(article_id, start, end)