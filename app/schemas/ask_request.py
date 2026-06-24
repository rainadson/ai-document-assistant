from pydantic import BaseModel, Field


class AskRequest(BaseModel):
    """Schema for the /ask endpoint request body."""

    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The question to ask about the uploaded documents.",
        examples=["Qual é o prazo de cancelamento?"],
    )
