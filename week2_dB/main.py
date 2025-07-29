from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from config import Config
from models import Hero , HeroFilter , HeroCreate, HeroUpdate, HeroPublic

connect_args = {"check_same_thread": False}
engine = create_engine(Config.database_url, connect_args=connect_args)
def get_session() -> Session:
    with Session(engine) as session:
        yield session

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes")
def read_heroes(session: SessionDep , filter:Annotated[HeroFilter,Depends()]) -> list[HeroPublic]:
        
    # Safely get the column to order by
    order_column = getattr(Hero, filter.order_by)

    # Apply order direction
    if filter.order.lower() == "desc":
        order_clause = order_column.desc()
    else:
        order_clause = order_column.asc()

    # Build the ORM query
    statement = (
        select(Hero)
        .order_by(order_clause)
        .limit(filter.limit)
        .offset(filter.skip)
    )

    # Execute and return results
    results = session.exec(statement).all()
    return results

@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    statement = select(Hero).where(Hero.id == hero_id)
    hero = session.exec(statement).first()
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero_db)
    session.commit()
    return {"detail": "Hero deleted successfully"}

