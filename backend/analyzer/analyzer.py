import openai
import os
from dotenv import load_dotenv

from article_fetcher.article_fetcher import Article_Fetcher
from text_cleaner.text_cleaner import Text_Cleaner
from comment_fetcher.comment_fetcher import Comment_Fetcher

class Analyzer:
    def __init__(self) -> None:
        load_dotenv()
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.current_directory = os.getcwd()
        self.AF = Article_Fetcher()
        self.TC = Text_Cleaner()
        self.check_folder()
        self.delete_test_result()
    
    def delete_test_result(self):
        with open('./result/test_result.txt', 'w') as file:
            file.write('')

    def check_folder(self):
        # 檢查 result 資料夾是否存在
        result_folder = 'result'
        if not os.path.exists(result_folder):
            # 如果不存在，則創建資料夾
            os.makedirs(result_folder)
            print(f'已創建 {result_folder} 資料夾')
        else:
            print(f'{result_folder} 資料夾已存在')
    
    def prompt_input(self,system: str,prompt: str):
        print("=============== Call ChatGPT ===============")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=[{
                "role": "system", "content": system,
                "role": "user", "content": prompt,
                # "role": "assistant", "content": assistant,
                }],
            temperature=0,
            max_tokens=2048
            # frequency_penalty=0,
            # presence_penalty=0
        )
        print(response['choices'][0]['message']['content'])
        # 打开一个文件以进行追加
        with open('./result/test_result.txt', 'a') as file:
            file.write(response['choices'][0]['message']['content'] + "\n")

        return response['choices'][0]['message']['content']
    
    def prompt_analyzer(self, keyword: str, tag: str, K: int, size: int, start: int, end: int):
        # keyword=keyword, tag=tag, K=K, size=10000,start=1697644800,end=1698204889
        prompt_AF=self.AF.get_article_by_keyword(keyword=keyword, tag=tag, K=K, size=size, start=start, end=end)
        contents=[]
        comments=[]
        
        for article in prompt_AF:
            article.content=self.TC.clean_text(article.content)
            contents.append(article.content)
            comments.append(article.get_all_comment_list())

        for i in range(K):
            # prompt = """現在給你[文章]以及[留言]，請對文章做總結\n並且列出你覺得跟這篇文章內容有高度相關的代表性留言。回復格式為\n(文章):\n(留言):\n[文章]\n"""+str(contents[i])+"\n[留言]\n"+str(comments[i])
            prompt = """現在給你[文章]以及[留言]，請對文章做總結\n並且條列式列出你覺得跟這篇文章內容有高度相關的代表性留言。回復格式為\n(文章):\n(留言):\n[文章]\n"""+str(contents[i])+"\n[留言]\n"+str(comments[i])
            self.prompt_input("你是一位在中文報社的時事分析專家",prompt)
        
        content_and_comment = ""
        content_and_comment_list = []
        with open('./result/test_result.txt','r') as file:
            content_and_comment_list = file.readlines()
        for content in content_and_comment_list:
            content_and_comment += content
            
        # prompt ="你是一位時事分析專家，我會給你幾篇(文章)以及(留言)，請綜合分析這些留言對事件的風向看法，以及留言對事件的觀點為何?\n給出一個對事件總結的標題，以及做一個[表格]分析，[表格]以markdown language呈現，需要列出事件的觀點，以及留言對此觀點的看法\n" + content_and_comment
        prompt ="我會給你幾篇(文章)以及(留言)，請綜合分析這些留言對事件的風向看法，以及留言對事件的觀點為何?\n給出一個對事件總結的標題。以及做一個表格分析，表格以markdown language呈現，需要列出事件的觀點，以及留言對此觀點的看法\n" + content_and_comment
        print(prompt)

        res = self.prompt_input("你是一位在中文報社的時事分析專家",prompt)

        return res

# if __name__ == '__main__':
    # analyzer_test=Analyzer()
    # analyzer_test.prompt_analyzer(keyword='柯文哲', tag='新聞', K=5, size=10000,start=1697644800,end=1698204889)