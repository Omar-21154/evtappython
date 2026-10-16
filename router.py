from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from dependencies import get_session
from models import Movie, MovieCreate, MovieUpdate

router = APIRouter(prefix="/movies", tags=["movies"])


def get_movie_or_404(id: int, session: Session) -> Movie:
    movie = session.get(Movie, id)
    if movie is None:
        raise HTTPException(status_code=404, detail=f"Movie '{id}' not found.")
    return movie


@router.get("", response_model=list[Movie])
def get_all_movies(session: Session = Depends(get_session)):
    return session.exec(select(Movie)).all()


@router.get("/search", response_model=list[Movie])
def search_movies(
    title: str | None = Query(default=None, min_length=1),
    genre: str | None = Query(default=None, min_length=1),
    session: Session = Depends(get_session),
):
    statement = select(Movie)
    if title:
        statement = statement.where(Movie.title.ilike(f"%{title}%"))
    if genre:
        statement = statement.where(Movie.genre.ilike(f"%{genre}%"))
    return session.exec(statement).all()


@router.get("/{id}", response_model=Movie)
def get_movie_by_id(id: int, session: Session = Depends(get_session)):
    return get_movie_or_404(id, session)


@router.post("", response_model=Movie, status_code=201)
def create_movie(movie_data: MovieCreate, session: Session = Depends(get_session)):
    movie = Movie.model_validate(movie_data)
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.put("/{id}", response_model=Movie)
def update_movie_by_id(id: int, movie_data: MovieCreate, session: Session = Depends(get_session)):
    movie = get_movie_or_404(id, session)
    movie.sqlmodel_update(movie_data.model_dump())
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.patch("/{id}", response_model=Movie)
def patch_movie_by_id(id: int, movie_data: MovieUpdate, session: Session = Depends(get_session)):
    movie = get_movie_or_404(id, session)
    movie.sqlmodel_update(movie_data.model_dump(exclude_unset=True))
    session.add(movie)
    session.commit()
    session.refresh(movie)
    return movie


@router.delete("/{id}")
def delete_movie_by_id(id: int, session: Session = Depends(get_session)):
    movie = get_movie_or_404(id, session)
    session.delete(movie)
    session.commit()
    return {"message": f"Movie '{id}' deleted successfully."}
