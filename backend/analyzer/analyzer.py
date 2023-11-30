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
        self.delete_txt()
    
    def delete_txt(self):
        with open('./result/prompt_summary.txt', 'w') as file:
            file.write('')
        with open('./result/GPT_report.txt', 'w') as file:
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
            model="gpt-3.5-turbo-1106",
            messages=[{
                "role": "system", "content": system,
                "role": "user", "content": prompt,
                }],
            temperature=0,
            max_tokens=2048
        )
        print(response['choices'][0]['message']['content'])

        with open('./result/prompt_summary.txt', 'a') as file:
            file.write(response['choices'][0]['message']['content'] + "\n")

        return response['choices'][0]['message']['content']

    def prompt_report(self,system: str,prompt: str):
        print("=============== Call ChatGPT ===============")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=[{
                "role": "system", "content": system,
                "role": "user", "content": prompt,
                }],
            temperature=1,
        )
        print(response['choices'][0]['message']['content'])

        with open('./result/GPT_report.txt', 'a') as file:
            response['choices'][0]['message']['content']=response['choices'][0]['message']['content'].replace('/\n/g', '<br>')
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

        # print(contents)

        # for i in range(K):
        for i in range(len(contents)):
            prompt = """現在給你[文章]以及[留言]，請對文章做200字以內總結\n並且條列式列出你覺得跟這篇文章內容有高度相關的留言(最多100則留言)。回復格式為\n(文章):\n(留言):\n[文章]\n"""+str(contents[i])+"\n[留言]\n"+str(comments[i])
            self.prompt_input("你是一位在臺灣的資深時事分析專家",prompt)
        
        content_and_comment = ""
        content_and_comment_list = []
        with open('./result/prompt_summary.txt','r') as file:
            content_and_comment_list = file.readlines()
        for content in content_and_comment_list:
            content_and_comment += content
        
        prompt ="""你是一位時事分析專家，我會給你幾篇(文章)以及(留言)，請綜合分析這些留言對事件的風向看法，以及留言對事件的觀點為何?\n給出一個對事件總結的標題，以及做一個[表格]分析，[表格]以markdown language呈現，
        (1)列出事件的觀點\n
        (2)對此觀點的詳細描述或是依據\n
        (3)留言對此觀點的看法(每個觀點最多10則留言)\n""" + content_and_comment

        res = self.prompt_report("你是一位在台灣的資深時事分析專家",prompt)
        return res

# if __name__ == '__main__':
#     analyzer_test=Analyzer()
#     analyzer_test.prompt_analyzer(keyword='柯文哲', tag='新聞', K=5, size=10000,start=1697644800,end=1698204889)
