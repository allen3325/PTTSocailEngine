# PTTSocailEngine
---
## 文字雲範例：
example.py(一樣要先設定好OpenAI API KEY)
```bash
python example.py
```
---
## 啟動程式
1. 將 .env.example 複製一份，並改名成 .env，將以下內容填入
``` bash
OPENAI_API_KEY = 你的API KEY
```
2. 跑以下指令
``` bash
pip install -r requirements.txt
```
3. 使用 uvicorn 啟動 fastAPI (Hot reload)
```bash
cd backend
uvicorn main:app --reload
```

---
# 其他
記得 commit 盡量使用 commit message type
## Swagger Doc：localhost:8000/docs