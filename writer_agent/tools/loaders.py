from typing import Union, List
from unstructured.partition.html import partition_html
from langchain.docstore.document import Document
import unicodedata
import requests
from bs4 import BeautifulSoup
from unstructured.cleaners.core import group_broken_paragraphs
import re

class UnstructuredURLLoader:
    def __init__(self, url: Union[str, List[str]], title: Union[str, List[str]]) -> None:
        self.url = url
        self.title = title

    def load(self) -> Union[Document, List[Document]]:
        try:
            if type(self.url) == str:
                try:
                    try:
                        elements = partition_html(url=self.url)
                    except Exception as e:
                        print(f"Error at url '{url}': {e}")
                    page_content =  " \n ".join([doc.text for doc in elements])
                    article_content = self._get_article(page_content, self.title)
                    document_object = Document(
                        page_content=article_content,
                        metadata={
                            "source": self.url,
                            "title": self.title,
                        }
                    )
                    return document_object
                except Exception as e:
                    raise e
            
            elif type(self.url) == list:
                try:
                    documents = []
                    for idx, url in enumerate(self.url):
                        try:
                            elements = partition_html(url=url)
                        except Exception as e:
                            print(f"Error at url '{url}': {e}")
                            continue
                        page_content =  " \n ".join([doc.text for doc in elements])
                        article_content = self._get_article(page_content, self.title[idx])
                        document_object = Document(
                            page_content=article_content,
                            metadata={
                                "source": url,
                                "title": self.title[idx],
                            }
                        )
                        documents.append(document_object)

                    return list(documents)
                except Exception as e:
                    raise e
                
        except Exception as e:
            raise e
        
    def _get_article(self, page_content: str, title: str) -> str:
        try:
            normalized_title = self._normalize_string(title)
            normalized_page_content = self._normalize_string(page_content)

            lowered_title = normalized_title.lower()
            lowered_page_content = normalized_page_content.lower()

            start_index = lowered_page_content.find(lowered_title)

            if start_index == -1:
                return page_content
            else:
                return page_content[start_index:]

        except Exception as e:
            raise e
        
    def _normalize_string(self, text: str):
        return unicodedata.normalize("NFC", text)


class HTMLLoader:
    def __init__(self, 
                 url: Union[str, List[str]],
                 title: Union[str, List[str]]) -> None:
        self.url = url
        self.title = title

    def load(self) -> Union[Document, List[Document]]:
        try:
            if type(self.url) == str:
                try:
                    try:
                        response = requests.get(self.url)
                    except Exception as e:
                        print(f"Error at url '{self.url}': {e}")
                    page_content = response.text
                    article_content = self._get_article(page_content, self.title)
                    document_object = Document(
                        page_content=article_content,
                        metadata={
                            "source": self.url,
                            "title": self.title,
                        }
                    )
                    return document_object
                except Exception as e:
                    raise e
            
            elif type(self.url) == list:
                try:
                    documents = []
                    for idx, url in enumerate(self.url):
                        try:
                            response = requests.get(url)
                        except Exception as e:
                            print(f"Error at url '{url}': {e}")
                            continue
                        page_content = response.text
                        article_content = self._get_article(page_content, self.title[idx])
                        document_object = Document(
                            page_content=article_content,
                            metadata={
                                "source": url,
                                "title": self.title[idx],
                            }
                        )
                        documents.append(document_object)

                    return list(documents)
                except Exception as e:
                    raise e
                
        except Exception as e:
            raise e
    
    def _normalize_string(self, text: str):
        return unicodedata.normalize("NFC", text)
        

    def _parse_title(self, title: str) -> str:
        title = re.split(r"[|:\-–]", title, 1)[0]
        return title.strip()

    
    def _get_title(self, soup, title: str):
        try:
            parsed_title = self._parse_title(title)
            title_element = soup.find(["h1", "title", "h2"], string=re.compile(parsed_title.lower(), re.IGNORECASE))
            if title_element:
                return title_element.find_parent()
            if title_element is None:
                title_element = soup.find(string=re.compile(parsed_title.lower(), re.IGNORECASE))
                if title_element:
                    return title_element.find_parent()
        except Exception:
            print(f"Can't get title element of: {title}")
            return None
    
    def _get_element_text_length(self, element) -> int:
        return len(element.get_text())
        
    def _get_article(self, page_content: str, title: str) -> str:
        # Cào dữ liệu HTML sử dụng kỹ thuật duyệt ngược từ title element (backtracking)
        try:
            soup = BeautifulSoup(page_content, "html.parser").body

            title_element = self._get_title(soup, title)

            if title_element:
                print(f"Crawling article: {title}")
                suspect_element = title_element.parent
                difference_log = [
                    {
                        "element": title_element,
                        "text_length": len(title_element.get_text()),
                        "difference": 0
                    }
                ]

                while suspect_element.parent.name != "body":
                    suspect_text_length = self._get_element_text_length(suspect_element)
                    difference = suspect_text_length - difference_log[-1]['text_length']

                    if difference < difference_log[-1]['difference']:
                        if difference_log[-1]['text_length'] > (self._get_element_text_length(soup) * 0.3):
                            return group_broken_paragraphs(difference_log[-1]['element'].get_text().strip())
                        
                    difference_log.append({
                        "element": suspect_element,
                        "text_length": suspect_text_length,
                        "difference": difference
                    })

                    suspect_element = suspect_element.parent


        # Failsafe: Nếu không thể crawl bài viết, ta sẽ sử dụng thư viện Unsctructured để cào dữ liệu
            try:
                elements = partition_html(text=page_content)
            except Exception as e:
                print(f"Error partitioning html at '{title}': {e}")

            page_content =  "\n\n".join([doc.text for doc in elements if doc.category in ["NarrativeText", "UncategorizedText", "Table", "Formula"]])

            try:
                print(f"Partitioning article: {title}")
                normalized_title = self._normalize_string(title)
                normalized_page_content = self._normalize_string(page_content)
                
                lowered_title = normalized_title.lower()
                lowered_page_content = normalized_page_content.lower()

                start_index = lowered_page_content.find(lowered_title)

                if start_index == -1:
                    return page_content
                else:
                    return page_content[start_index:]

            except Exception as e:
                print(f"Error getting content at '{title}': {e}")

        except Exception as e:
            raise f"Error Loading HTML: {e}"