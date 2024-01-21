from typing import List

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from src import models, schemas, utils
from src.utils import get_hashed_password


# --------------------------TEAM--------------------------------------------
def get_team(db: Session, team_id: int):
    return db.query(models.Team).filter(models.Team.id == team_id).first()


def get_team_by_name(db: Session, name: str):
    return db.query(models.Team).filter(models.Team.name == name).first()


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Team).offset(skip).limit(limit).all()


def create_team(db: Session, team: schemas.TeamCreate):
    try:
        db_team = models.Team(name=team.name, country=team.country, description=team.description)
        db.add(db_team)
        db.commit()
        db.refresh(db_team)
        return db_team
    except:
        db.rollback()
        return {"message": "An error occurred inserting the teams."}, 404


def delete_team(db: Session, team: schemas.Team):
    try:
        db.delete(team)
        db.commit()
    except:
        db.rollback()
        return {"message": "An error occurred deleting the teams."}, 404


def update_team(db: Session, db_team: models.Team, team: schemas.TeamCreate):
    try:
        db_team.name = team.name
        db_team.country = team.country
        db_team.description = team.description
        db.commit()
        db.refresh(db_team)
        return db_team
    except:
        db.rollback()
        return {"message": "An error occurred updating the teams."}, 404


def get_teams_by_competition(db: Session, competition_id: int):
    competition = db.query(models.Competition).get(competition_id)
    if not competition:
        raise ValueError("Competition not found")

    teams = competition.teams
    return teams


# --------------------------COMPETITIONS--------------------------------------------
def get_competition(db: Session, competition_id: int):
    return db.query(models.Competition).filter(models.Competition.id == competition_id).first()


def get_competition_by_name(db: Session, name: str):
    return db.query(models.Competition).filter(models.Competition.name == name).first()


def get_competitions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Competition).offset(skip).limit(limit).all()


def create_competition(db: Session, competitions: schemas.CompetitionCreate):
    try:
        teams = []
        for team_name in competitions.teams:
            team = db.query(models.Team).filter(models.Team.name == team_name.name).first()
            if team is not None:
                teams.append(team)

        db_competitions = models.Competition(name=competitions.name, category=competitions.category.value,
                                             sport=competitions.sport.value, teams=teams)
        db.add(db_competitions)
        db.commit()
        db.refresh(db_competitions)
        return db_competitions
    except:
        db.rollback()
        return {"message": "An error occurred inserting the competition. Check if teams are created"}, 404


def get_competitions_team(db: Session, competitions: schemas.CompetitionCreate):
    return db.query(models.Team).filter(models.Team.id.in_(competitions.teams)).all()


def delete_competition(db: Session, competition: schemas.Competition):
    try:
        db.delete(competition)
        db.commit()
    except:
        db.rollback()
        return {"message": "An error occurred deleting the competitions."}, 404


def update_competition(db: Session, db_competitions: models.Competition, competitions: schemas.CompetitionCreate):
    try:
        db_competitions.name = competitions.name
        db_competitions.sport = competitions.sport.value
        db_competitions.category = competitions.category.value
        teams = []
        for team_name in competitions.teams:
            team = db.query(models.Team).filter(models.Team.name == team_name.name).first()
            if team is not None:
                teams.append(team)

        db_competitions.teams = teams
        db.commit()
        db.refresh(db_competitions)
        return db_competitions
    except:
        db.rollback()
        return {"message": "An error occurred updating the competition. Check if teams are created"}, 404


def get_competitions_by_team(db: Session, team_id: int):
    competitions = db.query(models.Competition).filter(models.Competition.teams.any(models.Team.id == team_id)).all()
    return competitions


# --------------------------MATCHES--------------------------------------------


def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(and_(models.Match.id == match_id)).first()


def get_match_by_details(db: Session, matches: schemas.MatchCreate):
    db_matches = db.query(models.Match).filter(and_(models.Match.date == matches.date,
                                                    models.Match.local_id == matches.local.id,
                                                    models.Match.visitor_id == matches.visitor.id,
                                                    models.Match.competition_id == matches.competition.id,
                                                    models.Match.price == matches.price,
                                                    models.Match.total_available_tickets == matches.total_available_tickets,
                                                    models.Match.url == matches.url.value)).first()
    return db_matches


def get_matches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Match).offset(skip).limit(limit).all()


def create_match(db: Session, match: schemas.MatchCreate):
    try:
        local = get_team(db, match.local.id)
        visitor = get_team(db, match.visitor.id)
        competition = get_competition(db, match.competition.id)

        db_matches = models.Match(date=match.date, price=match.price, local=local,
                                  visitor=visitor, competition=competition,
                                  total_available_tickets=match.total_available_tickets,
                                  url=match.url.value)
        db.add(db_matches)
        db.commit()
        db.refresh(db_matches)
        return db_matches
    except:
        db.rollback()
        return {"message": "An error occurred inserting the Match. Check if teams and competitions are created"}, 404


def delete_match(db: Session, match: schemas.Match):
    try:
        db.delete(match)
        db.commit()
    except:
        db.rollback()
        return {"message": "An error occurred deleting the match."}, 404


def update_match(db: Session, db_matches: models.Match, match: schemas.MatchCreate):
    try:
        db_matches.date = match.date
        db_matches.price = match.price
        db_matches.total_available_tickets = match.total_available_tickets
        db_matches.url = match.url.value
        db_matches.local = get_team(db, match.local.id)
        db_matches.visitor = get_team(db, match.visitor.id)
        db_matches.competition = get_competition(db, match.competition.id)

        db.commit()
        db.refresh(db_matches)
        return db_matches
    except:
        db.rollback()
        return {"message": "An error occurred updating the Match. Check if teams and competitions are created"}, 404


def get_matches_by_team(db: Session, team_id: int):
    matches = db.query(models.Match).filter(
        (models.Match.local_id == team_id) | (models.Match.visitor_id == team_id)).all()
    return matches


def get_matches_by_competition(db: Session, competition_id: int):
    matches = db.query(models.Match).filter(models.Match.competition_id == competition_id).all()
    return matches


# -------------------------------ACCOUNTS---------------------------

def get_account_by_name(db: Session, username: str):
    return db.query(models.Account).filter(models.Account.username == username).first()


def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(username=account.username, password=utils.get_hashed_password(account.password))
    print(db_account.username)
    print(db_account.password)
    try:
        print(db_account)
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except:
        db.rollback()
        return {"message": "An error occurred inserting the Account. Check if all is correct"}, 404


def delete_account(db: Session, account: schemas.Account):
    try:
        db.query(models.Order).filter(models.Order.username == account.username).delete(synchronize_session=False)
        db.delete(account)
        db.commit()
    except:
        db.rollback()
        return {"message": "An error occurred deleting the Account."}, 404


def update_account(db: Session, db_account: models.Account, account: schemas.AccountCreate):
    try:
        db_account.username = account.username
        db_account.password = get_hashed_password(account.password)
        db_account.available_money = account.available_money
        db_account.is_admin = account.is_admin
        db.commit()
        db.refresh(db_account)
        return db_account
    except:
        db.rollback()
        return {"message": "An error occurred updating the Account. Check if all is correct"}, 404


def get_all_accounts(db: Session):
    accounts = db.query(models.Account).all()
    return accounts


def get_order_by_username(db: Session, username: str) -> schemas.Order:
    db_order = db.query(models.Order).filter(models.Order.username == username).all()
    return db_order


def create_order(db: Session, username: str, order: schemas.OrderCreate):
    account = get_account_by_name(db, username=username)
    if account.available_money < order.tickets_bought:
        return {"message": "Not enough money to purchase tickets"}, 404
    match = get_match(db, match_id=order.match_id)
    if match.total_available_tickets < order.tickets_bought:
        return {"message": "Not enough tickets available"}, 404
    try:
        match.total_available_tickets -= order.tickets_bought
        account.available_money -= (match.price * order.tickets_bought)
        new_order = models.Order(match_id=order.match_id, tickets_bought=order.tickets_bought)
        account.orders.append(new_order)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)
        return new_order
    except IntegrityError:
        db.rollback()
        return {"message": "An error occurred while creating the order. Please try again"}, 404


def get_orders(db: Session, skip: int = 0, limit: int = 10) -> List[schemas.Order]:
    db_orders = db.query(models.Order).offset(skip).limit(limit).all()
    return db_orders
