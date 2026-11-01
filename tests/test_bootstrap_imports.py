"""Bootstrap and import verification tests for the Python foundation."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def test_root_index_export():
    """Verify that root index.py re-exports the canonical FastAPI app."""
    import index
    import api.index

    assert hasattr(index, "app")
    assert index.app is api.index.app


def test_api_module_imports():
    """Verify that all canonical backend modules and services can be imported."""
    import api.agents
    import api.ai_providers
    import api.company_analysis_services
    import api.comparison_services
    import api.fx_services
    import api.groq_finance_agent
    import api.health
    import api.index
    import api.market_intelligence_services
    import api.research
    import api.research_cache
    import api.research_errors
    import api.research_logging
    import api.research_orchestrator
    import api.research_protection
    import api.research_schemas
    import api.research_services
    import api.settings

    assert api.index.app is not None
    assert api.research_orchestrator.ResearchOrchestrator is not None
    assert api.settings.settings is not None


def test_settings_defaults():
    """Verify default configuration without requiring live credentials."""
    from api.settings import settings, DEFAULT_GROQ_MODEL, DEFAULT_OPENROUTER_MODEL, DEFAULT_PROVIDER_ORDER

    assert settings.groq_model_primary == DEFAULT_GROQ_MODEL
    assert settings.openrouter_model == DEFAULT_OPENROUTER_MODEL
    assert settings.provider_order == DEFAULT_PROVIDER_ORDER
    assert settings.devtools_enabled is False


def test_python_version_and_environment():
    """Verify Python version contract."""
    version_file = ROOT / ".python-version"
    assert version_file.exists()
    assert version_file.read_text(encoding="utf-8").strip() == "3.12"
