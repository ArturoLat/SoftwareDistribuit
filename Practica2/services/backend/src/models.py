from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Float, Enum, UniqueConstraint, \
    Table
from sqlalchemy.orm import relationship

from src.database import Base

teams_in_competitions = Table("teams_in_competitions", Base.metadata,
                              Column("id", Integer, primary_key=True),
                              Column("team_id", Integer, ForeignKey("teams.id")),
                              Column("competition_id", Integer, ForeignKey("competitions.id")))

sports_list = ("Volleyball", "Football", "Basketball", "Futsal")
categories_list = ("Senior", "Junior")
url_list = ("../static/voleyball.png", "../static/football.png", "../static/futsal.png", "../static/basketball.png")


class Team(Base):
    __tablename__ = 'teams'  # This is table name

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False, index=True)
    country = Column(String(30), nullable=False)
    description = Column(String(100))


class Competition(Base):
    __tablename__ = 'competitions'  # This is table name
    __table_args__ = (UniqueConstraint('name', 'category', 'sport'),)

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    category = Column(Enum(*categories_list, name='category'), nullable=False)
    sport = Column(Enum(*sports_list, name='sport_competition'), nullable=False)
    teams = relationship("Team", secondary=teams_in_competitions, backref="competitions")
    match = relationship("Match", backref="competitions")


class Match(Base):
    __tablename__ = 'matches'  # This is table name
    __table_args__ = (UniqueConstraint('local_id', 'visitor_id', 'competition_id', 'date', 'total_available_tickets'),)

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    price = Column(Float, nullable=False)
    competition_id = Column(Integer, ForeignKey("competitions.id"), nullable=False)
    competition = relationship("Competition", backref="matches")

    local_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    visitor_id = Column(Integer, ForeignKey("teams.id"), nullable=False)
    local = relationship("Team", foreign_keys=local_id)
    visitor = relationship("Team", foreign_keys=visitor_id)

    total_available_tickets = Column(Integer, nullable=False, default=0)
    url = Column(Enum(*url_list, name='url_matches_foto'))


class Account(Base):
    __tablename__ = 'accounts'

    username = Column(String(30), primary_key=True, unique=True, nullable=False)
    password = Column(String(), nullable=False)
    # 0 not admin/ 1 is admin
    is_admin = Column(Integer, nullable=False)
    available_money = Column(Float, nullable=False)
    orders = relationship('Order', backref='orders', lazy=True)

    def __init__(self, username, password, available_money=200, is_admin=0):
        self.username = username
        self.password = password
        self.available_money = available_money
        self.is_admin = is_admin


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    username = Column(String(30), ForeignKey('accounts.username'), nullable=False)
    match_id = Column(Integer, nullable=False)
    tickets_bought = Column(Integer, nullable=False)

    def __init__(self, match_id, tickets_bought):
        self.match_id = match_id
        self.tickets_bought = tickets_bought
