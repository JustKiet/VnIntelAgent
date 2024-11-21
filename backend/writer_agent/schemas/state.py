from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from writer_agent.schemas.io import DocumentListResponse
from langgraph.graph import MessagesState
from writer_agent.schemas.outline import Outline
from langchain.docstore.document import Document
from typing import List
from writer_agent.schemas.article import ArticleSection
from writer_agent.schemas.config import UserConfig
from writer_agent.schemas.io import KeywordResponse

class State(TypedDict):
    messages: Annotated[list, add_messages]

class ResearcherState(MessagesState):
    final_response: DocumentListResponse

class ArticleState(TypedDict):
    config: UserConfig
    outline: Outline
    documents: List[Document]
    sections: List[ArticleSection]
    description: str
    keywords: KeywordResponse
    article: str