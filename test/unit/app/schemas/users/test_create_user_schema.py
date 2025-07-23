import pytest
from pydantic import ValidationError
from app.schemas import CreateUserSchema

class TestCreateUserSchema:
    def test_valid_user_schema(self):
        user = CreateUserSchema(
            first_name="jOhn",
            middle_name="pAul",
            last_name="doE",
            email="JOHN.DOE@Email.Com",
            phone="(123) 456-7890"
        )

        assert user.first_name == "John"
        assert user.middle_name == "Paul"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@email.com"
        assert user.phone == "(123) 456-7890"


    def test_optional_fields_can_be_none(self):
        user = CreateUserSchema(
            first_name="Ana",
            last_name="Silva",
            email="ana.silva@example.com"
        )

        assert user.middle_name is None
        assert user.phone is None


    @pytest.mark.parametrize("first_name", ["A", "x"*31, "J0hn", "Jean!"])
    def test_invalid_first_name(self, first_name):
        with pytest.raises(ValidationError):
            CreateUserSchema(
                first_name=first_name,
                last_name="Doe",
                email="valid@email.com"
            )


    @pytest.mark.parametrize("last_name", ["B", "x"*40, "L33t", "Smith#"])
    def test_invalid_last_name(self, last_name):
        with pytest.raises(ValidationError):
            CreateUserSchema(
                first_name="John",
                last_name=last_name,
                email="valid@email.com"
            )


    @pytest.mark.parametrize("middle_name", ["", "x"*100, "M@ria"])
    def test_invalid_middle_name(self, middle_name):
        with pytest.raises(ValidationError):
            CreateUserSchema(
                first_name="Maria",
                middle_name=middle_name,
                last_name="Lopez",
                email="maria@example.com"
            )


    @pytest.mark.parametrize("email", ["plainaddress", "missing@dot", "missingatsign.com"])
    def test_invalid_email(self, email):
        with pytest.raises(ValidationError):
            CreateUserSchema(
                first_name="John",
                last_name="Doe",
                email=email
            )


    @pytest.mark.parametrize("phone", ["abc-123", "1234567890x", "123_456_7890"])
    def test_invalid_phone(self, phone):
        with pytest.raises(ValidationError):
            CreateUserSchema(
                first_name="John",
                last_name="Doe",
                email="john@example.com",
                phone=phone
            )
    
    def test_capitalize_single_letter_words(self):
        user = CreateUserSchema(
            first_name="a b",
            middle_name="c c",
            last_name="d c",
            email="abc@example.com"
        )

        assert user.first_name == "A B"
        assert user.middle_name == "C C"
        assert user.last_name == "D C"


    def test_phone_normalization(self):
        user = CreateUserSchema(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone=" +1 (123) 456-7890 "
        )
        assert user.phone == "+1 (123) 456-7890"