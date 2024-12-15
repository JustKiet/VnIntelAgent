from typing import Optional, Type
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
from langchain_community.tools import TavilySearchResults
from writer_agent.schemas.io import SearchInput
from writer_agent.tools.loaders import UnstructuredURLLoader, HTMLLoader
from uuid import uuid4

class SearchAndScrape(BaseTool):
    name: str = "search_and_scrape"
    description: str = "Use this tool to search and scrape the web for information."
    args_schema: Type[BaseModel] = SearchInput
    return_direct: bool = True
    max_results: int = 5

    def _run(self,
             query: str,
             run_manager: Optional[CallbackManagerForToolRun] = None,) -> str:
        """Use the tool."""
        search_tool = TavilySearchResults(
            max_results=self.max_results,
        )
        results = search_tool.invoke(
            {
                "args": {
                    "query": query,
                },
                "type": "tool_call",
                "id": f"search_and_scrape_{uuid4()}",
                "name": "search_and_scrape_tavily",
            }
        ).artifact["results"]

        urls = [result["url"] for result in results]
        titles = [result["title"] for result in results]

        loader = HTMLLoader(
            url=urls,
            title=titles,
        )
        documents = loader.load()
        return documents
    
    async def _arun(self,
                    query: str,
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        """Use the tool asynchronously."""
        return self._run(
            query=query, 
            run_manager=run_manager.get_sync()
        )