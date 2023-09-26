from fastapi import FastAPI
import sys
sys.path.append('word_cloud')
from word_cloud import Word_Cloud
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Test"}

@app.get("/test")
async def test():
    wc = Word_Cloud()
    return wc.test()


@app.get("/wordcloud/{search_keyword}")
async def generate_word_cloud(search_keyword, K: int = 100):
    print(f"search_keyword is {search_keyword}.")
    wc = Word_Cloud()
    return wc.generate_word_cloud(search_keyword, K)