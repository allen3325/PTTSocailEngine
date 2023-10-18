import requests
import json


class Comment_Fetcher:
    def __init__(self) -> None:
        self.base_url = 'http://ptt-search.nlpnchu.org/api/GetCommentByArticle'
        self.headers = {'Accept': 'application/json'}

    def get_comment_list(self, article_id: str, start:int, end: int) -> list:
        all_comment = []
        if start is None:
            url = self.base_url + f'?article_id={article_id}'
        else:
            url = self.base_url + f'?article_id={article_id}&start={start}&end={end}'
        
        print(url)
        res = requests.get(url, self.headers)
        res = res.json()
        for hit in res['hits']:
            all_comment.append(hit['_source']['content'])
        return all_comment