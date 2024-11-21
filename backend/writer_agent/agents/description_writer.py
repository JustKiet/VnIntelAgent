from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel

class DescriptionWriter:
    def __init__(self,
                 model: BaseChatModel):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 ("You are an expert SEO Content Writer. "
                 "Write the complete fully optimized SEO Description on the keyword: {topic}, here's the outline for reference:\n\n"
                 "{outline}\n\n"
                 "Only return the complete description. Do not say anything more. "
                 "Do not go off-topic. ")),
                ("user", 
                 ("Write the complete Article Description"
                  "The description MUST BE LESS THAN 150 characters long. "
                  "The description needs to answer the question of 'What is this article about?'. "
                  "The description needs to contain the keyword as the first sentence. "
                  "The description needs to use benefit-driven language. "
                  "The description needs to be written in a {article_tone} tone and in {language}. "
                  "If your description exceed my expectations, I will give you a 200$ bonus!")),
            ]
        )

        self.model = model
        
        self.chain = self.prompt | self.model | StrOutputParser()