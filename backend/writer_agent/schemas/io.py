from pydantic import BaseModel, Field
from typing import List
from langchain.docstore.document import Document

class SearchInput(BaseModel):
    query: str = Field(title="The search query to be used to search the web.")

class DocumentListResponse(BaseModel):
    """Provide the documents retrieved from the web with this"""
    documents: List[Document] = Field(..., title="List of documents retrieved from the web.")

class KeywordResponse(BaseModel):
    """Provide the relevant keywords retrieved from the outline with this"""
    keywords: List[str] = Field(..., title="List of relevant keywords retrieved from the outline.")