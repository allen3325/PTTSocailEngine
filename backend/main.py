from fastapi import FastAPI
from word_cloud.word_cloud import Word_Cloud
from word_fetcher.word_fetcher import Word_Fetcher
from comment_fetcher.comment_fetcher import Comment_Fetcher
from text_cleaner.text_cleaner import Text_Cleaner

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

@app.get("/getcomment/{article_id}")
async def get_comment_list(article_id: str, start: int = None, end: int = None):
    cf = Comment_Fetcher()
    return cf.get_comment_list(article_id, start, end)

@app.get("/cleantest/{article_id}")
async def get_comment_list(article_id: str, start: int = None, end: int = None):
    cf = Comment_Fetcher()
    tc = Text_Cleaner()
    res_list = []
    comment_list = cf.get_comment_list(article_id, start, end)
    for comment in comment_list:
        comment = tc.clean_text(comment)
        if comment != "":
            res_list.append(comment)
    return res_list
