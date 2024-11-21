from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel
from writer_agent.schemas.io import KeywordResponse

class KeywordPlanner:
    def __init__(self,
                 model: BaseChatModel):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 ("You are an expert SEO Optimizer. "
                  "You have been given an outline on the following topic: '{topic}' \n\n"
                  "---------------------------------------------\n"
                  "Outline:\n"
                  "{outline}\n"
                  "---------------------------------------------\n\n"
                  "Retrieve the relevant keywords for the article. "
                  "Only return the keywords. Do not say anything more. "
                  "Do not go off-topic. ")),
                ("user", 
                 ("Retrieve the relevant keywords users might use to find the article. "
                  "Get the main keyword first, then the secondary keywords. "
                  "Only return the keywords relevant to the outline. "
                  "The language of the keywords should be in {language}. ")),
            ]
        )

        self.model = model
        
        self.chain = self.prompt | self.model.with_structured_output(KeywordResponse)