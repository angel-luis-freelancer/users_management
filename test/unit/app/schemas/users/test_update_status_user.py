import pytest
from pydantic import ValidationError

from app.models.user import UserStatus
from app.schemas import UpdateStatusUserSchema


class TestUpdateStatusUser:

    @pytest.mark.parametrize("invalid_body", [
        {"estado": "active"},
        {"statuz": "pending"},
        {"": "suspended"},
        {},
    ])
    def test_invalid_key(self, invalid_body):
        with pytest.raises(ValidationError) as exc:
            UpdateStatusUserSchema(**invalid_body)
        errors = exc.value.errors()

        assert len(errors) >= 1
        for error in errors:
            assert error["type"] in ("extra_forbidden", "missing")

    @pytest.mark.parametrize("valid_value,expected", [
        ({"status": "active"}, "active"),
        ({"status": "pending"}, "pending"),
        ({"status": "suspended"}, "suspended"),
        ({"status": "deleted"}, "deleted"),
    ])
    def test_valid_status_value(self, valid_value, expected):
        schema = UpdateStatusUserSchema(**valid_value)
        assert schema.status == expected

    @pytest.mark.parametrize("status", [
    "enabled", "banned", "unknown", "", None, "Inactive"
    ])
    def test_invalid_statuses(self, status):
        with pytest.raises(ValueError):
            UpdateStatusUserSchema(status=status)