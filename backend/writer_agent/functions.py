from writer_agent.schemas.state import ArticleState
from writer_agent.agents.outliner import Outliner, OutlineRefiner
from writer_agent.agents.article_writer import ArticleWriter
from writer_agent.agents.section_writer import SectionWriter
from writer_agent.tools.search import SearchAndScrape
from langchain_core.messages import ToolCall, AIMessage
from langgraph.prebuilt import ToolNode
from langchain.docstore.document import Document # Do not delete this import
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from uuid import uuid4

async def create_initial_outline(state: ArticleState):
    keyword = state["config"].keyword
    outliner = Outliner(
        model=state["config"].model
    ).chain
    initial_outline = await outliner.ainvoke(
        {
            "topic": keyword,
            "language": state["config"].language,
        }
    )
    return {
        **state,
        "outline": initial_outline
    }

async def initialize_research(state: ArticleState):
    outline = state["outline"]
    section_titles = [section.section_title for section in outline.sections]

    search_tool = SearchAndScrape()

    tool_calls_params = []
    for section in section_titles[:-1]:
        tool_call_param = ToolCall(
            name=search_tool.name, 
            args={"query": section},
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

    return {
        **state,
        "documents": documents
    }

async def create_retriever(state: ArticleState):
    text_splitter = SemanticChunker(
        embeddings=OpenAIEmbeddings(
            model="text-embedding-3-small"
        ),
        breakpoint_threshold_type="gradient",
    )

    splits = text_splitter.split_documents(documents=state["documents"])

    vectorstore = FAISS.from_documents(
        documents=splits,
        embedding=text_splitter.embeddings
    )

    retriever = vectorstore.as_retriever()

    return {
        **state,
        "retriever": retriever
    }

async def refine_outline(state: ArticleState):
    outline_refiner = OutlineRefiner(
        model=state["config"].model
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

async def write_sections(state: ArticleState):
    section_writer = SectionWriter(
        model=state["config"].model,
        retriever=state["retriever"]
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

async def write_article(state: ArticleState):
    writer = ArticleWriter(
        model=state["config"].model
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