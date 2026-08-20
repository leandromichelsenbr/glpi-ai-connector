import pytest

from glpi_ai_connector.core.policy import PolicyDenied, SecurityPolicy


def test_entity_allowlist():
    policy = SecurityPolicy(allowed_entity_ids={0, 2})
    policy.check_entity(0)
    policy.check_entity(2)

    with pytest.raises(PolicyDenied):
        policy.check_entity(99)


def test_close_is_denied_by_default():
    policy = SecurityPolicy()

    with pytest.raises(PolicyDenied, match="close_ticket"):
        policy.require("close_ticket")


def test_close_can_be_enabled():
    policy = SecurityPolicy(allow_close=True)
    policy.require("close_ticket")
