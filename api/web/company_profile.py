"""Company profile, executive governance roster, and competitor evidence views."""

from __future__ import annotations

from typing import Any
from pydantic import BaseModel, ConfigDict

from api.research_schemas import (
    CompanyIdentity,
    CompanyOverview,
    CompetitiveEvidence,
    GovernanceProfile,
)
from api.web.formatters import number_label


def is_safe_website_url(url: str | None) -> bool:
    """Return True if URL is non-empty and uses an allowed web scheme (http/https)."""
    if not url:
        return False
    u = url.strip().lower()
    return u.startswith("http://") or u.startswith("https://")


class ExecutiveView(BaseModel):
    model_config = ConfigDict(extra="ignore")
    name: str
    title: str | None = None
    since: int | None = None

    @property
    def display_role(self) -> str:
        parts = [self.name]
        if self.title:
            parts.append(self.title)
        if self.since:
            parts.append(f"since {self.since}")
        return " · ".join(parts)


class CompanyProfileView(BaseModel):
    model_config = ConfigDict(extra="ignore")
    company_name: str | None = None
    ticker: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    country: str | None = None
    headquarters: str | None = None
    website: str | None = None
    is_safe_website: bool = False
    employees: str | None = None
    description: str | None = None
    has_profile: bool = False


class GovernanceView(BaseModel):
    model_config = ConfigDict(extra="ignore")
    ceo_name: str | None = None
    ceo_title: str | None = None
    ceo_display: str = "Insufficient verified data."
    leadership: list[ExecutiveView] = []
    notable_developments: list[str] = []
    note: str = "No sourced management-change assertion is shown."
    has_governance: bool = False


class CompetitorEvidenceView(BaseModel):
    model_config = ConfigDict(extra="ignore")
    status: str = "unavailable"
    note: str = "Insufficient verified competitor data."
    competitors: list[str] = []
    has_competitors: bool = False


def format_company_profile(
    overview: CompanyOverview | None,
    identity: CompanyIdentity | None = None,
) -> CompanyProfileView:
    """Format company overview and identity into a validated profile view."""
    if not overview and not identity:
        return CompanyProfileView()

    ov = overview
    id_obj = identity

    company_name = (ov.company_name if ov and ov.company_name else None) or (id_obj.name if id_obj else None)
    ticker = (ov.ticker if ov and ov.ticker else None) or (id_obj.symbol if id_obj else None)
    exchange = (ov.exchange if ov and ov.exchange else None) or (id_obj.exchange if id_obj else None)
    sector = (ov.sector if ov and ov.sector else None) or (id_obj.sector if id_obj else None)
    industry = (ov.industry if ov and ov.industry else None) or (id_obj.industry if id_obj else None)
    country = ov.country if ov else None
    headquarters = ov.headquarters if ov else None
    raw_website = ov.website.strip() if (ov and ov.website) else None
    safe_website = is_safe_website_url(raw_website)
    website = raw_website if safe_website else None
    employees = (
        number_label(ov.employees)
        if (ov and ov.employees is not None)
        else None
    )
    description = ov.business_description if ov else None

    has_profile = bool(description or country or headquarters or safe_website or employees)

    return CompanyProfileView(
        company_name=company_name,
        ticker=ticker,
        exchange=exchange,
        sector=sector,
        industry=industry,
        country=country,
        headquarters=headquarters,
        website=website,
        is_safe_website=safe_website,
        employees=employees,
        description=description,
        has_profile=has_profile,
    )


def format_governance(gov: GovernanceProfile | None) -> GovernanceView:
    """Format executive governance roster and verified management note."""
    if not gov:
        return GovernanceView()

    ceo_name = gov.ceo.name if gov.ceo else None
    ceo_title = gov.ceo.title if gov.ceo else None
    ceo_display = (
        " · ".join(filter(None, [ceo_name, ceo_title]))
        if ceo_name
        else "Insufficient verified data."
    )

    leadership = [
        ExecutiveView(name=m.name, title=m.title, since=m.since)
        for m in (gov.key_leadership or [])
    ]
    notable = gov.notable_developments or []
    note = " ".join(notable) if notable else "No sourced management-change assertion is shown."
    has_gov = bool(gov.ceo or leadership or notable)

    return GovernanceView(
        ceo_name=ceo_name,
        ceo_title=ceo_title,
        ceo_display=ceo_display,
        leadership=leadership,
        notable_developments=notable,
        note=note,
        has_governance=has_gov,
    )


def format_competitor_evidence(comp: CompetitiveEvidence | None) -> CompetitorEvidenceView:
    """Format competitive evidence notes and competitors list."""
    if not comp:
        return CompetitorEvidenceView()

    competitors = comp.competitors or []
    note = comp.note or "Insufficient verified competitor data."
    has_comp = bool(competitors or (note and note != "Insufficient verified competitor data."))

    return CompetitorEvidenceView(
        status=comp.status,
        note=note,
        competitors=competitors,
        has_competitors=has_comp,
    )
