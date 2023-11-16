from fastapi import FastAPI
# from word_cloud.word_cloud import Word_Cloud
# from word_fetcher.word_fetcher import Word_Fetcher
# from comment_fetcher.comment_fetcher import Comment_Fetcher
# from text_cleaner.text_cleaner import Text_Cleaner
from article_fetcher.article_fetcher import Article_Fetcher
from analyzer.analyzer import Analyzer
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/article/{keyword}",description='keyword: 關鍵字, tag: 分類標籤(預設 None), K: TOP K, size: 搜尋幾個(預設100), start: 開始的timestamp(預設 None), end: 結束的timestamp(預設 None)\n 若預設為 None，代表為全抓。')
async def get_article_by_keyword(keyword: str, tag: str = None, K: int = 5, size: int = 100, start: int = None, end: int = None):
    af = Article_Fetcher()
    return af.get_article_by_keyword(keyword=keyword, tag=tag, K=K, size=size, start=start, end=end)


@app.get("/analyze/{keyword}",description='keyword: 關鍵字, tag: 分類標籤(預設 None), K: TOP K, size: 搜尋幾個(預設100), start: 開始的timestamp(預設 None), end: 結束的timestamp(預設 None)\n 若預設為 None，代表為全抓。')
async def analyze_by_keyword(keyword: str,
                             tag: str = None,
                             K: int = 5,
                             size: int = 100,
                             start: int = None,
                             end: int = None):
    if keyword == "test_for_NCHU_NLP_LAB":
        return """# 事件總結標題：柯文哲與侯友宜的合作問題引發網友熱議

| 事件觀點 | 留言對此觀點的看法 |
|---------|------------------|
| 柯文哲秉持開闊的格局，致力整合各方建議與政見，絕非國民黨口中的「串門子」，而是匯聚民間力量，達成政黨輪替的目標。 | - 連柯都要主流民意大聯盟了？ <br> - 人家都提了民調+民主初選 <br> - 柯提出來的辦法都細到連數字都有了，侯辦也沒說柯的民調方案或數字哪一塊，他們不滿要改，反觀柯對侯的民調質疑，侯辦沒一樣認真回應的 |
| 侯友宜願意接受「柯侯配」，但柯文哲要回覆是否同意，否則進入政黨協商。 | - 你是不是很怕柯侯配 <br> - 侯柯這兩個咖洨真的想談 早就同桌坐下來談了啦 <br> - 侯還在堅持不可行沒科學可信度的民主初選根本冥頑不靈 |
| 侯友宜要求柯文哲回覆是否合作，否則進入政黨協商。 | - 柯郭是最佳解，候去旁邊玩沙 <br> - 侯真的被大家看衰，沒救了 <br> - 侯真的好吠 |
| 侯友宜願意接受「柯侯配」，但柯文哲要回覆是否同意，否則進入政黨協商。 | - 侯的說法就像是告訴柯，你吃屎我就當副手 <br> - 在一個對方不可能接受的前題下，才願意當副 <br> - 侯腦想要用條件限制柯，真的科科笑 |

#### 總結：根據留言的分析，網友對於柯文哲與侯友宜的合作問題持有不同的看法。有些人認為柯文哲的做法是為了匯聚民間力量，達成政黨輪替的目標，並且提出了具體的辦法和數字，對於侯友宜的質疑感到不滿。另一方面，也有人認為侯友宜願意接受「柯侯配」，但柯文哲要回覆是否同意，否則進入政黨協商的態度是在限制柯文哲的選擇，並且對侯友宜的做法感到不滿。綜合來看，網友對於柯文哲與侯友宜的合作問題持有不同的觀點，並且對於侯友宜的做法有所質疑。"""
    analyzer_test = Analyzer()
    return analyzer_test.prompt_analyzer(keyword=keyword,
                                         tag=tag,
                                         K=K,
                                         size=size,
                                         start=start,
                                         end=end)

# @app.get("/word/cloud/{search_keyword}")
# async def generate_word_cloud(search_keyword, K: int = 100):
#     print(f"search_keyword is {search_keyword}.")
#     wc = Word_Cloud()
#     return wc.generate_word_cloud(search_keyword, K)


# @app.get("/word/dict/{search_keyword}")
# async def generate_dictionary(search_keyword, K: int = 100):
#     print(f"search_keyword is {search_keyword}.")
#     wf = Word_Fetcher()
#     return wf.generate_dictionary(search_keyword, K)
