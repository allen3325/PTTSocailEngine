import os
import sys
from text_cleaner import Text_Cleaner
from article_fetcher import Article_Fetcher

AF=Article_Fetcher()
TC=Text_Cleaner()
prompt_AF=AF.get_article_by_keyword(keyword=哈登, tag=新聞, K=5, size=10000, start=1696089600, end=1698822879)
for art in prompt_AF:
    art.content=TC.clean_text(art.content)
    print(art.content)