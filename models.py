from typing import Optional

from sqlmodel import Field, SQLModel


class MovieBase(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    author: str
    year: int = Field(ge=0)
    genre: str
    rating: float = Field(ge=0, le=5)


class Movie(MovieBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class MovieCreate(MovieBase):
    pass


class MovieUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    author: Optional[str] = None
    year: Optional[int] = Field(default=None, ge=0)
    genre: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0, le=5)
