"""Tests for KPI analytics."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

import pathlib
import sys

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from analytics.kpis import abc_by, get_basic_kpis
from db.models import Sale
from db.session import Base


def build_session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return sessionmaker(bind=engine)()


def test_basic_kpis(monkeypatch):
    session = build_session()
    session.add_all(
        [
            Sale(
                product="A",
                customer="X",
                amount=100,
                margin=0.3,
                discount=0.1,
                quantity=1,
                batch_id="b1",
            ),
            Sale(
                product="B",
                customer="Y",
                amount=200,
                margin=0.2,
                discount=0.05,
                quantity=2,
                batch_id="b2",
            ),
        ]
    )
    session.commit()

    monkeypatch.setattr("analytics.kpis.ga_fetch", lambda s, e: (0, 0.0))
    monkeypatch.setattr("analytics.kpis.shopify_fetch", lambda s, e: (0, 0.0))

    data = get_basic_kpis(session)
    assert data["turnover"] == 300
    assert data["orders"] == 2
    assert data["ticket_average"] == 150
    assert round(data["margin"], 2) == 100 * 0.3 + 200 * 0.2
    assert round(data["discount"], 2) == 100 * 0.1 + 200 * 0.05


def test_abc_by():
    session = build_session()
    session.add_all(
        [
            Sale(
                product="A",
                customer="X",
                amount=80,
                margin=0,
                discount=0,
                quantity=1,
                batch_id="b1",
            ),
            Sale(
                product="B",
                customer="Y",
                amount=15,
                margin=0,
                discount=0,
                quantity=1,
                batch_id="b2",
            ),
            Sale(
                product="C",
                customer="Z",
                amount=5,
                margin=0,
                discount=0,
                quantity=1,
                batch_id="b3",
            ),
        ]
    )
    session.commit()

    result = abc_by(session, "product")
    assert result["A"][0]["name"] == "A"
    assert any(item["name"] == "B" for item in result["B"])
    assert any(item["name"] == "C" for item in result["C"])
