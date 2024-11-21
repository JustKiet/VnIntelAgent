from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.pregel import RetryPolicy
from writer_agent.schemas.state import ArticleState
from IPython.display import display, Image, Markdown
from writer_agent.schemas.config import UserConfig
from writer_agent.schemas.state import ArticleState
from writer_agent.agents.outliner import Outliner, OutlineRefiner
from writer_agent.agents.article_writer import ArticleWriter
from writer_agent.agents.section_writer import SectionWriter
from writer_agent.agents.keywords_planner import KeywordPlanner
from writer_agent.agents.description_writer import DescriptionWriter
from writer_agent.tools.search import SearchAndScrape
from langchain_core.messages import ToolCall, AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langchain.docstore.document import Document
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from uuid import uuid4
from pprint import pprint
from datetime import datetime

class AutomatedSEOContentWriterGraph:
    def __init__(self,
                 user_config: UserConfig | dict,
                 config: dict):
        self._graph = self._initialize_graph()
        self.user_config = UserConfig.model_validate(user_config) if isinstance(user_config, dict) else ValueError(f"Invalid user config type, expected 'dict', got: {type(user_config)}")
        self.config = config
        self.article = None
        self.retriever = None
        self._date = datetime.now().strftime("%Y-%m-%d")

    def _initialize_graph(self):
        workflow = StateGraph(ArticleState)

        workflow.add_node("initialize", self.create_initial_outline, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("research", self.initialize_research, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("retrieval", self.create_retriever, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("refine", self.refine_outline, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("get_keywords", self.get_keywords, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("write_description", self.write_description, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("write_sections", self.write_sections, retry=RetryPolicy(max_attempts=3))
        workflow.add_node("write_article", self.write_article, retry=RetryPolicy(max_attempts=3))

        workflow.set_entry_point("initialize")

        workflow.add_edge("initialize", "research")
        workflow.add_edge("research", "retrieval")
        workflow.add_edge("retrieval", "refine")
        workflow.add_edge("refine", "get_keywords")
        workflow.add_edge("get_keywords", "write_description")
        workflow.add_edge("write_description", "write_sections")
        workflow.add_edge("write_sections", "write_article")
        workflow.add_edge("write_article", END)

        return workflow.compile(checkpointer=MemorySaver())
    
    def visulize_graph(self):
        try:
            display(Image(self._graph.get_graph().draw_mermaid_png()))
        except Exception as e:
            print(e)

    async def astream_(self):
        async for msg, metadata in self._graph.astream(
            {
                "config": self.user_config
            },
            config=self.config,
            stream_mode="messages"
        ):
            if (msg.content and not isinstance(msg, HumanMessage) and metadata["langgraph_node"] == "write_article"):
                yield msg.content

        checkpoint = self._graph.get_state(self.config)
        self.article = checkpoint.values["article"]

    def render_article(self):
        display(Markdown(self.article))

    async def create_initial_outline(self, state: ArticleState):
        keyword = state["config"].keyword
        
        model = ChatOpenAI(
            model=state["config"].model
        )

        outliner = Outliner(
            model=model
        ).chain
        
        initial_outline = await outliner.ainvoke(
            {
                "topic": keyword,
                "language": state["config"].language,
            }
        )

        pprint(initial_outline)

        return {
            **state,
            "outline": initial_outline
        }

    async def initialize_research(self, state: ArticleState):
        outline = state["outline"]
        section_titles = [section.section_title for section in outline.sections]
        section_titles.append(state["config"].keyword)

        search_tool = SearchAndScrape(
            max_results=5
        )

        tool_calls_params = []
        for section in section_titles[:-1]:
            if section == state["config"].keyword:
                tool_call_param = ToolCall(
                    name=search_tool.name, 
                    args={"query": f"{state['config'].keyword} {self._date}"},
                    id=f"search_tool_{uuid4()}",
                    type="tool_call"
                )
            else:
                tool_call_param = ToolCall(
                    name=search_tool.name, 
                    args={"query": f"{state['config'].keyword}: {section} {self._date}"},
                    id=f"search_tool_{uuid4()}",
                    type="tool_call"
                )
            tool_calls_params.append(tool_call_param)

        tool_node = ToolNode(tools=[search_tool])

        parallel_tool_calls = AIMessage(
            content="",
            tool_calls=tool_calls_params
        )

        tool_output = await tool_node.ainvoke({"messages": [parallel_tool_calls]})

        raw_docs = [raw_doc.content for raw_doc in tool_output["messages"]]

        documents = []

        for raw_doc in raw_docs:
            raw_doc = eval(raw_doc)
            [documents.append(doc) for doc in raw_doc if doc not in documents and doc.page_content != '']

        pprint(documents)

        return {
            **state,
            "documents": documents
        }

    async def create_retriever(self, state: ArticleState):
        text_splitter = SemanticChunker(
            embeddings=OpenAIEmbeddings(
                model="text-embedding-3-small"
            ),
            breakpoint_threshold_type="gradient",
        )

        splits = text_splitter.split_documents(documents=state["documents"])

        vectorstore = await FAISS.afrom_documents(
            documents=splits,
            embedding=text_splitter.embeddings
        )

        self.retriever = vectorstore.as_retriever()

        return state

    async def refine_outline(self, state: ArticleState):

        model = ChatOpenAI(
            model=state["config"].model
        )

        outline_refiner = OutlineRefiner(
            model=model
        ).chain

        documents = "\n".join(
            [
                (f"<Document href='{doc.metadata['source']}'>\n"
                f"{doc.page_content}\n"
                "</Document>")
                for doc in state["documents"]
            ]
        )

        updated_outline = await outline_refiner.ainvoke(
            {
                "topic": state["config"].keyword,
                "old_outline": state["outline"].as_str,
                "documents": documents,
                "language": state["config"].language,
            }
        )

        return {
            **state,
            "outline": updated_outline
        }
    
    async def get_keywords(self, state: ArticleState):
        
        model = ChatOpenAI(
            model=state["config"].model
        )

        keyword_planner = KeywordPlanner(
            model=model
        ).chain

        outline = state["outline"]
        keywords = await keyword_planner.ainvoke(
            {
                "topic": state["config"].keyword,
                "outline": outline.as_str,
                "language": state["config"].language,
            }
        )
        return {
            **state,
            "keywords": keywords
        }
    
    async def write_description(self, state: ArticleState):
            
            model = ChatOpenAI(
                model=state["config"].model
            )
    
            description_writer = DescriptionWriter(
                model=model
            ).chain
    
            outline = state["outline"]
            description = await description_writer.ainvoke(
                {
                    "topic": state["config"].keyword,
                    "outline": outline.as_str,
                    "article_tone": state["config"].article_tone,
                    "language": state["config"].language,
                }
            )
            return {
                **state,
                "description": description
            }


    async def write_sections(self, state: ArticleState):

        model = ChatOpenAI(
            model=state["config"].model
        )

        section_writer = SectionWriter(
            model=model,
            retriever=self.retriever
        ).chain
        
        outline = state["outline"]
        sections = await section_writer.abatch(
            [
                {
                    "outline": outline.as_str,
                    "section": section.section_title,
                    "topic": state["config"].keyword,
                    "article_tone": state["config"].article_tone,
                    "language": state["config"].language,
                }
                for section in outline.sections
            ]
        )
        return {
            **state,
            "sections": sections
        }

    async def write_article(self, state: ArticleState):
        
        model = ChatOpenAI(
            model=state["config"].model,
            streaming=True
        )

        writer = ArticleWriter(
            model=model
        ).chain
        topic = state["config"].keyword
        sections = state["sections"]
        draft = "\n\n".join([section.as_str for section in sections])
        article = await writer.ainvoke(
            {
                "topic": topic, 
                "draft": draft,
                "word_count": state["config"].word_count,
                "article_tone": state["config"].article_tone,
                "language": state["config"].language,
            }
        )
        return {
            **state,
            "article": article
        }