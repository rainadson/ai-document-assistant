from pydantic import BaseModel, Field


class AskResponse(BaseModel):
    """Schema for the /ask endpoint response body."""

    answer: str = Field(..., description="The generated answer based on document context.")
    sources: list[str] = Field(
        default_factory=list,
        description="List of source document filenames used to generate the answer.",
    )
