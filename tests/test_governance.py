"""Tests for executive governance roster, competitor evidence, and verified leadership mapping."""

from __future__ import annotations

import pytest
from fastapi.templating import Jinja2Templates

from api.research_schemas import CompetitiveEvidence, GovernanceProfile, LeadershipMember
from api.web.company_profile import (
    CompetitorEvidenceView,
    ExecutiveView,
    GovernanceView,
    format_competitor_evidence,
    format_governance,
)


def test_governance_full_mapping():
    """Verify CEO, key leadership roster, and notable developments are mapped."""
    gov = GovernanceProfile(
        ceo=LeadershipMember(name="Tim Cook", title="Chief Executive Officer", since=2011),
        key_leadership=[
            LeadershipMember(name="Luca Maestri", title="Senior Vice President and CFO", since=2014),
            LeadershipMember(name="Jeff Williams", title="Chief Operating Officer", since=2015),
            LeadershipMember(name="Deirdre O'Brien", title="Senior VP of Retail + People", since=2019),
        ],
        notable_developments=["Luca Maestri transitioning from CFO role effective January 2025."],
    )

    view = format_governance(gov)

    assert view.ceo_name == "Tim Cook"
    assert view.ceo_title == "Chief Executive Officer"
    assert view.ceo_display == "Tim Cook · Chief Executive Officer"
    assert len(view.leadership) == 3
    assert view.leadership[0].display_role == "Luca Maestri · Senior Vice President and CFO · since 2014"
    assert "Luca Maestri transitioning" in view.note
    assert view.has_governance is True


def test_governance_missing_ceo_and_roster():
    """Verify unverified governance data shows standardized fallbacks without inventing names."""
    gov = GovernanceProfile(
        ceo=None,
        key_leadership=[],
        notable_developments=[],
    )

    view = format_governance(gov)

    assert view.ceo_display == "Insufficient verified data."
    assert len(view.leadership) == 0
    assert view.note == "No sourced management-change assertion is shown."
    assert view.has_governance is False


def test_governance_none_profile():
    """Verify None profile behaves cleanly."""
    view = format_governance(None)
    assert view.ceo_display == "Insufficient verified data."
    assert len(view.leadership) == 0
    assert view.note == "No sourced management-change assertion is shown."
    assert view.has_governance is False


def test_competitor_evidence_mapping():
    """Verify competitor evidence notes and competitor names are mapped."""
    comp = CompetitiveEvidence(
        status="available",
        competitors=["Microsoft", "Alphabet", "Amazon"],
        note="Competes across consumer hardware, digital services, and operating systems.",
    )

    view = format_competitor_evidence(comp)

    assert view.status == "available"
    assert len(view.competitors) == 3
    assert "Microsoft" in view.competitors
    assert "consumer hardware" in view.note
    assert view.has_competitors is True


def test_competitor_evidence_missing():
    """Verify missing competitor evidence displays standardized fallback."""
    comp = CompetitiveEvidence(
        status="unavailable",
        competitors=[],
        note="Insufficient verified competitor data.",
    )

    view = format_competitor_evidence(comp)

    assert view.status == "unavailable"
    assert len(view.competitors) == 0
    assert view.note == "Insufficient verified competitor data."
    assert view.has_competitors is False


def test_governance_template_rendering():
    """Verify governance template renders CEO and leadership roster correctly."""
    templates = Jinja2Templates(directory="templates")

    gov = GovernanceProfile(
        ceo=LeadershipMember(name="Satya Nadella", title="Chairman and CEO", since=2014),
        key_leadership=[
            LeadershipMember(name="Amy Hood", title="EVP and CFO", since=2013),
            LeadershipMember(name="Brad Smith", title="Vice Chair and President", since=2015),
        ],
        notable_developments=["No recent executive departure announcements."],
    )
    view = format_governance(gov)

    html = templates.get_template("partials/governance.html").render({"governance": view})

    assert "Governance" in html
    assert "Satya Nadella" in html
    assert "Chairman and CEO" in html
    assert "Amy Hood" in html
    assert "Brad Smith" in html


def test_competitor_template_rendering():
    """Verify competitor evidence template renders notes and competitor items."""
    templates = Jinja2Templates(directory="templates")

    comp = CompetitiveEvidence(
        status="available",
        competitors=["Apple", "Google", "Amazon"],
        note="Direct cloud and productivity suite competition.",
    )
    view = format_competitor_evidence(comp)

    html = templates.get_template("partials/competitor_evidence.html").render({"competitors": view})

    assert "Competitive evidence" in html
    assert "Direct cloud and productivity" in html
    assert "Apple" in html
    assert "Google" in html
    assert "Amazon" in html
