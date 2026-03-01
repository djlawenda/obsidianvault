from pydantic import BaseModel, Field
from typing import List, Optional

class Theme(BaseModel):
    name: str = Field(description="The name of the core theme, e.g., 'Risk vs Uncertainty'")
    description: str = Field(description="A brief, paragraph-length description of how this theme manifests in the book.")

class Learning(BaseModel):
    concept: str = Field(description="The name of the specific concept or actionable insight.")
    explanation: str = Field(description="A detailed, multi-sentence explanation of the concept and its importance.")

class BookSummary(BaseModel):
    title: str = Field(description="The full title of the book.")
    author: str = Field(description="The author(s) of the book.")
    high_level_summary: str = Field(description="A concise summary of the book's main thesis and arguments.")
    core_themes: List[Theme] = Field(description="A list of the 3-5 most important core themes of the entire book.")
    key_learnings: List[Learning] = Field(description="An exhaustive list of 10-15 highly detailed key learnings and concepts.")
    tags: List[str] = Field(description="3-5 relevant tags for the book.")

class KnowledgeNode(BaseModel):
    name: str
    description: str
    excerpts: List[str] = Field(default_factory=list)

class HubNode(KnowledgeNode):
    pass

class ConceptNode(KnowledgeNode):
    parent_hub: str

class TechNode(KnowledgeNode):
    parent_concept: str

class KnowledgeExtraction(BaseModel):
    hubs: List[HubNode] = Field(default_factory=list)
    concepts: List[ConceptNode] = Field(default_factory=list)
    technologies: List[TechNode] = Field(default_factory=list)
