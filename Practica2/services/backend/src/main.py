import os

from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import Field
from sqlalchemy.orm import Session
from src import models, repository, schemas
from fastapi.middleware.cors import CORSMiddleware
from src.database import SessionLocal, engine
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.security import OAuth2PasswordRequestForm
from src.dependencies import get_current_user
from src.utils import verify_password, create_access_token, create_refresh_token
from src.database import production

models.Base.metadata.create_all(bind=engine)  # Creem la base de dades amb els models que hem definit a SQLAlchemy
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# --------------------------TEAMS--------------------------------------------

# Funciona
@app.get("/teams/", response_model=list[schemas.Team])
def read_teams(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_teams(db, skip=skip, limit=limit)


# Funciona
@app.post("/teams/", response_model=schemas.Team)
def create_team(team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, name=team.name)
    if db_team:
        raise HTTPException(status_code=400, detail="Team already Exists, Use put for updating")
    else:
        return repository.create_team(db=db, team=team)


# Funciona
@app.get("/team/{team_name}", response_model=schemas.Team)
def read_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    return team


# Funciona
@app.delete("/teams/{team_name}", response_model=schemas.Team)
def delete_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")
    repository.delete_team(db=db, team=team)
    return team


# Funciona
@app.put("/teams/{team_name}", response_model=schemas.Team)
def update_team(team_name: str, team: schemas.TeamCreate, db: Session = Depends(get_db)):
    db_team = repository.get_team_by_name(db, name=team_name)
    if not db_team:
        return repository.create_team(db=db, team=team);
    updated_team = repository.update_team(db=db, db_team=db_team, team=team)
    return updated_team


# retorna tots els equips d'una competició, donada el seu nom. Funciona
@app.get("/competitions/{competition_name}/teams", response_model=list[schemas.Team])
def get_teams_by_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    teams = repository.get_teams_by_competition(db, competition_id=competition.id)
    return teams


# retorna l'equip local i visitant d'un partit, donat el seu id. Funciona
@app.get("/matches/{match_id}/teams", response_model=list[schemas.Team])
def get_teams_by_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    teams = [match.local, match.visitor]
    return teams


# --------------------------COMPETITIONS--------------------------------------------

# Funciona
@app.get("/competitions/", response_model=list[schemas.Competition])
def read_competitions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_competitions(db, skip=skip, limit=limit)


# Funciona
@app.get("/competition/{competitions_id}", response_model=schemas.Competition)
def read_competition(competitions_id: int, db: Session = Depends(get_db)):
    competition = repository.get_competition(db, competition_id=competitions_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    return competition


# Funciona
@app.post("/competitions/", response_model=schemas.Competition)
def create_competition(competition: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    db_competition = repository.get_competition_by_name(db, name=competition.name)
    if db_competition:
        raise HTTPException(status_code=400, detail="Competition already exists, use put for updating")
    created_competition = repository.create_competition(db=db, competitions=competition)
    return created_competition


# Funciona
@app.delete("/competitions/{competitions_id}", response_model=schemas.Competition)
def delete_competitions(competitions_id: int, db: Session = Depends(get_db)):
    competition = repository.get_competition(db, competition_id=competitions_id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")
    repository.delete_competition(db=db, competition=competition)
    return competition


# Funciona
@app.put("/competitions/{competitions_id}", response_model=schemas.Competition)
def update_competitions(competitions_id: int, competitions: schemas.CompetitionCreate, db: Session = Depends(get_db)):
    db_competitions = repository.get_competition(db, competition_id=competitions_id)
    if not db_competitions:
        return repository.create_competition(db=db, competitions=competitions);
    updated_competition = repository.update_competition(db=db, db_competitions=db_competitions,
                                                        competitions=competitions)
    return updated_competition


# retorna totes les competicions d'un equip, donat el seu nom. Funciona
@app.get("/teams/{team_name}/competitions", response_model=list[schemas.Competition])
def get_competitions_by_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    team_id = team.id

    competitions = repository.get_competitions_by_team(db, team_id=team_id)
    return competitions


# retorna la competició d'un partit, donat el seu id. Funciona
@app.get("/matches/{match_id}/competition", response_model=schemas.Competition)
def get_competition_by_match(match_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id=match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")

    competition = repository.get_competition(db, competition_id=match.competition.id)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    return competition


# --------------------------MATCHES--------------------------------------------

# Funciona
@app.get("/matches/", response_model=list[schemas.Match])
def read_matches(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_matches(db, skip=skip, limit=limit)


# Funciona
@app.get("/match/{matches_id}", response_model=schemas.Match)
def read_match(matches_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id=matches_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    return match


# Funciona
@app.post("/matches/", response_model=schemas.Match)
def create_matches(matches: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_local = repository.get_team(db=db, team_id=matches.local.id)
    if not db_local:
        raise HTTPException(status_code=400, detail="Local doesn't exists, create the team before")

    db_visitor = repository.get_team(db=db, team_id=matches.visitor.id)
    if not db_visitor:
        raise HTTPException(status_code=400, detail="Visitor doesn't exists, create the team before")

    db_competition = repository.get_competition(db=db, competition_id=matches.competition.id)
    if not db_competition:
        raise HTTPException(status_code=400, detail="Competition doesn't exists, create the competition before")

    db_match = repository.get_match_by_details(db, matches=matches)
    if db_match:
        raise HTTPException(status_code=400, detail="Match already Exists, Use put for updating")
    else:
        return repository.create_match(db=db, match=matches)


# FUNCIONA
@app.delete("/matches/{matches_id}", response_model=schemas.Match)
def delete_matches(matches_id: int, db: Session = Depends(get_db)):
    match = repository.get_match(db, match_id=matches_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    repository.delete_match(db=db, match=match)
    return match


# Funciona
@app.put("/matches/{matches_id}", response_model=schemas.Match)
def update_matches(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    db_local = repository.get_team(db=db, team_id=match.local.id)
    if not db_local:
        raise HTTPException(status_code=400, detail="Local doesn't exists, create the team before")

    db_visitor = repository.get_team(db=db, team_id=match.visitor.id)
    if not db_visitor:
        raise HTTPException(status_code=400, detail="Visitor doesn't exists, create the team before")

    db_competition = repository.get_competition(db=db, competition_id=match.competition.id)
    if not db_competition:
        raise HTTPException(status_code=400, detail="Competition doesn't exists, create the competition before")

    db_matches = repository.get_match_by_details(db, matches=match)
    if not db_matches:
        return repository.create_match(db=db, match=match)
    updated_match = repository.update_match(db=db, db_matches=db_matches, match=match)
    return updated_match


# retorna tots els partits d'un equip, donat el seu nom. Funciona
@app.get("/teams/{team_name}/matches", response_model=list[schemas.Match])
def get_matches_by_team(team_name: str, db: Session = Depends(get_db)):
    team = repository.get_team_by_name(db, name=team_name)
    if not team:
        raise HTTPException(status_code=404, detail="Team not found")

    team_id = team.id

    matches = repository.get_matches_by_team(db, team_id=team_id)
    return matches


# retorna tots els partits d'una competició, donada el seu nom. Funciona
@app.get("/competitions/{competition_name}/matches", response_model=list[schemas.Match])
def get_matches_by_competition(competition_name: str, db: Session = Depends(get_db)):
    competition = repository.get_competition_by_name(db, name=competition_name)
    if not competition:
        raise HTTPException(status_code=404, detail="Competition not found")

    competition_id = competition.id

    matches = repository.get_matches_by_competition(db, competition_id=competition_id)
    return matches


# --------------------------------------ACCOUNTS--------------------------------------------
# Funciona
"""
@app.get("/account/{username}")
def get_account(username: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_name(db, name=username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
"""


# Funciona
@app.post('/account', summary="Create new user", response_model=schemas.Account)
def create_user(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = repository.get_account_by_name(db, username=account.username)
    if db_account:
        raise HTTPException(status_code=400, detail="Account already exists")
    created_account = repository.create_account(db=db, account=account)
    return created_account


@app.delete('/account/{username}', response_model=schemas.Account)
def delete_account(username: str, db: Session = Depends(get_db)):
    account = repository.get_account_by_name(db, username=username)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    repository.delete_account(db=db, account=account)
    return account


@app.put('/account/{username}', response_model=schemas.Account)
def update_account(username: str, account: schemas.AccountCreate, db: Session = Depends(get_db)):
    db_account = repository.get_account_by_name(db, username=username)
    if not db_account:
        return repository.create_account(db=db, account=account)
    updated_account = repository.update_account(db=db, db_account=db_account, account=account)
    return updated_account


@app.get('/accounts')
def get_all_accounts(db: Session = Depends(get_db)):
    accounts = repository.get_all_accounts(db)
    return accounts


@app.get('/orders/{username}', response_model=list[schemas.Order])
def get_order(username: str, db: Session = Depends(get_db)):
    return repository.get_order_by_username(db=db, username=username)


@app.post('/orders/{username}', response_model=schemas.Order)
def create_order(username: str, order: schemas.OrderCreate, db: Session = Depends(get_db)):
    return repository.create_order(db=db, username=username, order=order)


@app.get('/orders', response_model=list[schemas.Order])
def get_all_orders(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return repository.get_orders(db=db, skip=skip, limit=limit)


@app.post('/login', summary="Create access and refresh tokens for user", response_model=schemas.TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    username = form_data.username
    password = form_data.password

    # Get user from database
    user = repository.get_account_by_name(db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Verify password
    if not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    # Create access and refresh tokens

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
    }


#  --------------------------------------------PROTEGITS-------------------------------------------

@app.get('/account', summary='Get details of currently logged in user', response_model=schemas.SystemAccount)
async def get_me(user: schemas.SystemAccount = Depends(get_current_user)):
    return user


@app.post('/orders', summary='Post order of user logged', response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, user: schemas.SystemAccount = Depends(get_current_user),
                       db: Session = Depends(get_db)):
    return repository.create_order(db, username=user.username, order=order)
