from pydantic import BaseModel, Field
from typing import Optional, List

class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Description of the subsection")

    @property
    def as_str(self) -> str:
        return (f"### {self.subsection_title}\n\n"
                f"{self.description}\n".strip())
    
class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    description: str = Field(..., title="Content of the section")
    subsections: Optional[List[Subsection]] = Field(
        default=None,
        title="Titles and descriptions for each subsections of the article."
    )

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(subsection.as_str for subsection in self.subsections or [])
        return (f"## {self.section_title}\n\n"
                f"{self.description}\n\n"
                f"{subsections}".strip())
    
class Outline(BaseModel):
    article_title: str = Field(..., title="Title of the article")
    sections: List[Section] = Field(
        default_factory=list,
        title="Titles and descriptions for each section of the article."
    )

    @property
    def as_str(self) -> str:
        sections = "\n\n".join(section.as_str for section in self.sections)
        return (f"# {self.article_title}\n\n"
                f"{sections}".strip())
    
class RelatedSubjects(BaseModel):
    topics: List[str] = Field(
        description="Comprehensive list of related topics to the article as background research."
    )