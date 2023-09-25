from GoogleNews import GoogleNews
from wordcloud import WordCloud
from collections import Counter
import openai
import os
from dotenv import load_dotenv
import re
from NCHU_nlptoolkit.cut import *
import time

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')
search_keyword = '孫易磊'
K = 100
current_directory = os.getcwd()

#TODO 解決 Maximum length 問題，以及目前文字雲太少。
#TODO 字型問題

def checkFolder():
    # 檢查 result 資料夾是否存在
    result_folder = 'result'
    if not os.path.exists(result_folder):
    # 如果不存在，則創建資料夾
        os.makedirs(result_folder)
        print(f'已創建 {result_folder} 資料夾')
    else:
        print(f'{result_folder} 資料夾已存在')

def generate_wordcloud(group_names: list):
    print("=============== Generate Wordcloud ===============")
    global search_keyword
    table = []
    tmpdict = {}
    for i in [0,1,2]:
        tmpdict.clear()
        with open(f"{current_directory}/result/{search_keyword}-{group_names[i]}.txt") as f:
            data_list = f.readlines()
        f.close()
        for data in data_list:
            word = data.split(':')[1].strip()
            freq = data.split(':')[0].strip()
            if word != "" and freq != ":":
                tmpdict[word] = int(freq)
                
        # generate wordcloud
        cloud = WordCloud(background_color="white", font_path=f"{current_directory}/fonts/POP.ttf", width=700, height = 350).generate_from_frequencies(tmpdict)
        cloud.to_file(f'{current_directory}/result/{search_keyword}-{group_names[i]}.png')

def search_by_keyword(keyword: str) -> list:
    # search from google news
    GoogleNews().clear()
    googlenews = GoogleNews(lang='zh-TW', encode='utf-8')
    googlenews.search(keyword)
    
    # extract title and description to list
    title_and_description = []
    for page in range(1,11):
        result_list = googlenews.page_at(page)
        for result in result_list:
            title_and_description += cut_sentence(result['desc'], minword=2) + cut_sentence(result['title'], minword=2)

    return title_and_description

def generate_prompt(table: dict) -> str:
    prompt =  """以下文字的格式為 詞彙:詞頻 。幫我根據這些詞彙分成三個類別分群，每個類別給我25~35個詞彙，並且每個詞彙都要記錄對應的詞頻。\n輸出格式為：\n數字-此類別所代表的主題\n詞彙:詞頻\n文字為以下\n###\n
    """
    for word, freq in table.items():
        prompt += (word + ":" + str(freq) + "\n")
    prompt+="###"
    return prompt

#TODO 不擺詞頻
def chatGPT_classification_words(table: dict):
    while True:
        # Avoid http 502 error
        try:
            print("=============== Call ChatGPT ===============")
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k-0613",
                messages=[{"role": "user", "content": generate_prompt(table)}],
                temperature=0
                # frequency_penalty=0,
                # presence_penalty=0
            )
            # print(f"prompt is \n{generate_prompt(table=table)}")
            return response['choices'][0]['message']['content']
        except:
            time.sleep(3)
            print("some error sleep 3 seconds.")

def save_result(text) -> list:
    print("=============== Save chatGPT response to list ===============")
    global search_keyword
    group_name_list = []
    group_data_list = []
    groups = re.findall(r'\d-\w+', text)
    group_name_list.append(groups[0].split('-')[1])
    group_name_list.append(groups[1].split('-')[1])
    group_name_list.append(groups[2].split('-')[1])

    # split the group
    all_group = re.split(r'\d-\w+', text)
    # split word, frequency in group and append to the list
    for group in all_group:
        group = group.strip()
        group_data = ""
        # delete empty string
        if len(group) > 1:
            for word in group.split("\n"):
                # prevent dirty data like only ":"
                if len(word) > 1:
                    if word.find(":") != -1 and word != "":
                        term, frequency = word.split(":")
                        frequency = int(frequency)
                        group_data += f'{frequency}:{term.strip()}\n'
                    
            if group_data != "":
                group_data_list.append(group_data)

    # save group list into file
    with open(f'{current_directory}/result/{search_keyword}-{group_name_list[0]}.txt','w') as f:
        f.write(f'{group_data_list[0]}')
    with open(f'{current_directory}/result/{search_keyword}-{group_name_list[1]}.txt','w') as f:
        f.write(f'{group_data_list[1]}')
    with open(f'{current_directory}/result/{search_keyword}-{group_name_list[2]}.txt','w') as f:
        f.write(f'{group_data_list[2]}')

    return group_name_list

def save_response(text):
    print("=============== Save chatGPT response ===============")
    global search_keyword
    with open(f'{current_directory}/result/{search_keyword}.txt', 'w') as f:
        f.write(text)

def get_top_K(frequency_counting_table, K) -> dict:
    if len(frequency_counting_table) < K:
        return dict(sorted(frequency_counting_table.items(), key=lambda x:x[1], reverse = 1))
    else:
        return dict(sorted(frequency_counting_table.items(), key=lambda x:x[1], reverse = 1)[0:K])

if __name__ == '__main__':
    checkFolder()
    # generate list about search_keyword
    title_and_description = search_by_keyword(search_keyword)
    # make frequency table about K
    frequency_counting_table = dict(Counter(title_and_description))
    top_K = get_top_K(frequency_counting_table,K)
    # Call chatGPT and save response
    res = chatGPT_classification_words(top_K)
    save_response(res)
    group_name_list = save_result(res)
    # generate wordcloud
    generate_wordcloud(group_name_list)
    print("Done.")