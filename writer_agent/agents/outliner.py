from writer_agent.schemas.outline import Outline
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel

class Outliner:
    def __init__(self,
                 model: BaseChatModel):
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                ("You are an SEO Content Writer. "
                "Write an outline for an article about an user-provided topic. "
                "Be comprehensive and specific. "
                "Think of the user's intention when searching for the topic to further optimize the article. "
                "Only return the outline, no yapping. "
                "Write in {language}.")),
                ("user", "{topic}"),
            ]
        )

        self.model = model
        self.chain = self.prompt | self.model.with_structured_output(Outline)

class OutlineRefiner:
    def __init__(self,
                 model: BaseChatModel):
        
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                ("You are an SEO Content Writer. "
                "You have gathered information from the internet about the topic/keyword {topic}. "
                "Now, you are refining the outline of the article. "
                "Be comprehensive and specific. "
                "Only return the outline, no yapping. "
                "Think of the user's intention when searching for the topic to further optimize the article. "
                "Write in {language}. "
                "Old outline: \n\n"
                "{old_outline}")),
                ("user", 
                ("Refine the outline based on the information you have gathered:\n\n"
                "{documents}\n\n"
                "Write the refined outline in {language}.")),
            ]
        )

        self.model = model
        self.chain = self.prompt | self.model.with_structured_output(Outline)