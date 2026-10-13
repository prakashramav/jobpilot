import pytest

from app.services.apply_service import ApplyService, UnsupportedATSPlatformError


@pytest.fixture
def apply_service():
    return ApplyService()


@pytest.mark.parametrize(
    ("ats_type", "apply_url", "expected_filler"),
    [
        ("greenhouse", "https://boards.greenhouse.io/acme/jobs/1", "greenhouse_filler"),
        ("lever", "https://jobs.lever.co/acme/1", "lever_filler"),
        ("ashby", "https://jobs.ashbyhq.com/acme/1", "ashby_filler"),
    ],
)
def test_select_filler_routes_supported_ats(apply_service, ats_type, apply_url, expected_filler):
    assert apply_service.select_filler(ats_type, apply_url) is getattr(apply_service, expected_filler)


@pytest.mark.parametrize(
    ("ats_type", "apply_url"),
    [
        ("workable", "https://apply.workable.com/acme/j/123/"),
        ("unknown", "https://apply.workable.com/acme/j/123/"),
    ],
)
def test_workable_is_not_routed_to_greenhouse(apply_service, ats_type, apply_url):
    with pytest.raises(UnsupportedATSPlatformError, match="Workable.*apply manually"):
        apply_service.select_filler(ats_type, apply_url)


def test_unknown_ats_is_reported_as_unsupported(apply_service):
    with pytest.raises(UnsupportedATSPlatformError, match="unknown ATS.*apply manually"):
        apply_service.select_filler("generic", "https://careers.example.com/jobs/1")
