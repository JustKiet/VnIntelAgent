from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.language_models.chat_models import BaseChatModel

class ArticleWriter:
    def __init__(self,
                 model: BaseChatModel):
        self.prompt = ChatPromptTemplate.from_messages(
            [
                ("system",
                 ("You are an expert SEO Content Writer. "
                 "Write the complete fully optimized SEO Article on the keyword: {topic}, using the following section drafts:\n\n"
                 "{draft}\n\n"
                 "Only return the complete article. Do not say anything more. "
                 "Do not go off-topic. ")),
                ("user", 
                 ("Write the complete Article using Markdown format.\n "
                  "Avoid plagiarism, duplication and ensure the content is unique.\n "
                  "Ensure that the title contains the keyword.\n "
                  "The article MUST STRICTLY be NO LONGER THAN {word_count} words long.\n "
                  "Cut off any information that is unrelated to the topic.\n "
                  "If there are any equations, write in default string format. Do not use LaTeX.\n "
                  "Make sure to follow the Experience - Expertise - Authorative - Trustworthy (E-E-A-T) guidelines.\n "
                  "If the section topic is a 'Your Money or Your Life' (YMYL) topic, ensure that the content is accurate and trustworthy.\n "
                  "There can only be one conclusion at the end of the article. Do not include any conclusions or summaries in the sections.\n "
                  "The article needs to be written in a {article_tone} tone and in {language}.\n "
                  "If your article exceed my expectations, I will give you a 200$ bonus!")),
            ]
        )

        self.model = model
        
        self.chain = self.prompt | self.model | StrOutputParser()