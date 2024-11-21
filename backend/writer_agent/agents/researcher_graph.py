from writer_agent.tools.search import SearchAndScrape
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from writer_agent.schemas.state import ResearcherState
from writer_agent.schemas.io import DocumentListResponse
from langchain_core.language_models.chat_models import BaseChatModel

class ResearcherGraph:
    def __init__(self, 
                 llm: BaseChatModel):
        self.search_tool = SearchAndScrape()
        self.tools = [self.search_tool, DocumentListResponse]
        self.model = llm
        self.model_with_tool = self.model.bind_tools(
            tools=self.tools,
            tool_choice="any"
        )
        self.graph = self._initialize_graph()

    def call_model(self, state: ResearcherState):
        response = self.model_with_tool.invoke(state["messages"])
        return {"messages": [response]}

    
    def respond(self, state: ResearcherState) -> dict:
        response = DocumentListResponse(**state["messages"][-1].tool_calls[0]["args"])
        return {"final_response": response}

    
    def should_continue(self, state: ResearcherState):
        messages = state["messages"]
        last_message = messages[-1]
        if (len(last_message.tool_calls) == 1 and last_message.tool_calls[0]["name"] == "DocumentListResponse"):
            return "respond"
        else:
            return "continue"
        
    def _initialize_graph(self):
        workflow = StateGraph(ResearcherState)

        workflow.add_node("agent", self.call_model)
        workflow.add_node("respond", self.respond)
        workflow.add_node("tools", ToolNode(self.tools))

        workflow.set_entry_point("agent")

        workflow.add_conditional_edges(
            source="agent",
            path=self.should_continue,
            path_map={
                "continue": "tools",
                "respond": "respond",
            }
        )

        workflow.add_edge("tools", "agent")
        workflow.add_edge("respond", END)
        
        return workflow.compile()