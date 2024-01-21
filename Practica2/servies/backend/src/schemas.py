import enum
from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

from src.models import sports_list, categories_list, url_list


class TeamBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None


class TeamCreate(TeamBase):
    pass


class Team(TeamBase):
    id: int

    class Config:
        orm_mode = True


class CompetitionBase(BaseModel):
    name: str
    category: enum.Enum('category', dict(zip(categories_list, categories_list)))
    sport: enum.Enum('sport', dict(zip(sports_list, sports_list)))
    teams: list[Team] = []


class CompetitionCreate(CompetitionBase):
    pass


class Competition(CompetitionBase):
    id: int

    class Config:
        orm_mode = True


class MatchBase(BaseModel):
    date: datetime
    price: float
    local: Team
    visitor: Team
    competition: Competition
    total_available_tickets: int
    url: enum.Enum('url', dict(zip(url_list, url_list)))


class MatchCreate(MatchBase):
    pass


class Match(MatchBase):
    id: int

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    username: str
    match_id: int
    tickets_bought: int


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    id: int

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    username: str
    available_money: float = 200.0
    is_admin: int = 0


class AccountCreate(BaseModel):
    username: str = Field(..., description="username")
    password: str = Field(..., min_length=8, description="user password")
    is_admin: Optional[int]
    available_money: Optional[float]


class Account(AccountBase):
    orders: list[Order] = []

    class Config:
        orm_mode = True


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str = None
    exp: int = None


class SystemAccount(Account):
    password: str
