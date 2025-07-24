import pytest
from pydantic import ValidationError
from app.schemas import UpdateUserSchema  # ajusta si tu path es diferente

class TestUpdateUserSchema:
    def test_valid_first_name_only(self):
        user = UpdateUserSchema(first_name="joHN")
        assert user.first_name == "John"

    def test_valid_last_name_and_phone(self):
        user = UpdateUserSchema(last_name="peRez", phone=" 123-456-7890 ")
        assert user.last_name == "Perez"
        assert user.phone == "123-456-7890"

    def test_full_name_normalization(self):
        user = UpdateUserSchema(first_name="ANdrE luIs")
        assert user.first_name == "Andre Luis"

    def test_phone_normalization(self):
        user = UpdateUserSchema(phone=" +1 (123) 456-7890 ")
        assert user.phone == "+1(123)456-7890"

    def test_single_letter_names_are_capitalized(self):
        user = UpdateUserSchema(first_name="a b", phone="123456")
        assert user.first_name == "A B"

    def test_no_fields_provided(self):
        with pytest.raises(ValidationError) as exc_info:
            UpdateUserSchema()
        assert "At least one field must be provided" in str(exc_info.value)

    @pytest.mark.parametrize("name_field,value", [
        ("first_name", "A"),            # muy corto
        ("middle_name", "a"*31),        # muy largo
        ("last_name", "John123"),       # contiene números
    ])
    def test_invalid_name_fields(self, name_field, value):
        with pytest.raises(ValidationError):
            UpdateUserSchema(**{name_field: value})

    @pytest.mark.parametrize("phone", [
        "abc-123",               # letras no permitidas
        "1234567890x",           # sufijo inválido
        "123_456_7890",          # carácter inválido "_"
    ])
    def test_invalid_phone(self, phone):
        with pytest.raises(ValidationError) as exc_info:
            UpdateUserSchema(first_name="John", phone=phone)
        assert any(err["loc"] == ("phone",) for err in exc_info.value.errors())

    def test_extra_field_should_fail(self):
        with pytest.raises(ValidationError) as exc_info:
            UpdateUserSchema(first_name="Jane", extra_field="not allowed")
        assert "Extra inputs are not permitted" in str(exc_info.value)