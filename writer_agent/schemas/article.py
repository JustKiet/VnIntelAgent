from pydantic import BaseModel, Field
from typing import Optional, List

class SubSection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    content: str = Field(..., title="Full content of the subsection")

    @property
    def as_str(self) -> str:
        return (f"### {self.subsection_title}\n\n"
                f"{self.content}\n".strip())
    
class ArticleSection(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    content: str = Field(..., title="Full content of the section")
    subsections: Optional[List[SubSection]] = Field(
        default=None,
        title="Titles and descriptions for each subsections of the article."
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(subsection.as_str for subsection in self.subsections or [])
        return (f"## {self.section_title}\n\n"
                f"{self.content}\n\n"
                f"{subsections}".strip())