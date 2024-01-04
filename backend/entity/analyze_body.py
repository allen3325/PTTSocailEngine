'''
keyword=keyword,
tag=tag,
K=K,
size=size,
start=start,
end=end,
uuid=uuidOfSession,
'''
from pydantic import BaseModel


class AnalyzeBody(BaseModel):
    keyword: str
    uuidOfSession: str
    tag: str | None = None
    K: int = 5
    size: int = 100
    start: int | None = None
    end: int | None = None