from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.vectorstores.base import VectorStore
from writer_agent.schemas.article import ArticleSection

class SectionWriter:
    def __init__(self, 
                 model: BaseChatModel,
                 retriever: VectorStore):
        
        self.model = model
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 ("You are an expert SEO Content Writer. "
                 "Complete your assigned ArticleSection from the following outline:\n\n"
                 "{outline}\n\n"
                 "Use the following references:\n\n"
                 "{docs}\n\n")),
                ("user", 
                 "Write the full ArticleSection for the {section} section.\n "
                 "Only write the content related to the section. Do not go off-topic. Do not give conclusions or summaries.\n "
                 "Write in a {article_tone} tone and in {language}. "),
            ]
        )
        self.retriever = retriever

        self.chain = self.retrieve | self.prompt | self.model.with_structured_output(ArticleSection)
    
    async def retrieve(self, inputs: dict):
        docs = await self.retriever.ainvoke(f"{inputs['topic']}: {inputs['section']}")
        formatted = "\n".join(
            [
                (f"<Document href='{doc.metadata['source']}'>\n"
                 f"{doc.page_content}\n"
                 "</Document>")
                 for doc in docs
            ]
        )
        return {"docs": formatted, **inputs}