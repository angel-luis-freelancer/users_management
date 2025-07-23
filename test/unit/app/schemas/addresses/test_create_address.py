import pytest
from pydantic import ValidationError
from app.schemas.addresses import CreateAddressSchema

class TestCreateAddressSchema:
    def test_valid_complete_address(self):
        """Test con todos los campos válidos"""
        data = {
            "street": "Calle Mayor",
            "number": 123,
            "city": "Madrid",
            "state": "Madrid",
            "country": "España",
            "instructions": "Porton azul, segundo piso"
        }
        schema = CreateAddressSchema(**data)
        assert schema.street == "Calle Mayor"
        assert schema.number == 123
        assert schema.city == "Madrid"
        assert schema.state == "Madrid"
        assert schema.country == "España"
        assert schema.instructions == "Porton azul, segundo piso"

    def test_valid_minimal_address(self):
        """Test solo con campo obligatorio (country)"""
        data = {"country": "España"}
        schema = CreateAddressSchema(**data)
        assert schema.street is None
        assert schema.number is None
        assert schema.city is None
        assert schema.state is None
        assert schema.country == "España"
        assert schema.instructions is None

    def test_missing_required_country(self):
        """Test falla cuando falta el campo obligatorio country"""
        data = {
            "street": "Calle Mayor",
            "number": 123,
            "city": "Madrid"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "country" in str(exc_info.value)

    # Tests para validación de longitud de campos
    def test_street_max_length_valid(self):
        """Test street con longitud máxima válida (50 caracteres)"""
        data = {
            "street": "A" * 50,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert len(schema.street) == 50


    def test_street_max_length_invalid(self):
        """Test street excede longitud máxima"""
        data = {
            "street": "A" * 51,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "String should have at most 50 characters" in str(exc_info.value)

    def test_city_max_length_valid(self):
        """Test city con longitud máxima válida (30 caracteres)"""
        data = {
            "city": "B" * 30,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert len(schema.city) == 30

    def test_city_max_length_invalid(self):
        """Test city excede longitud máxima"""
        data = {
            "city": "B" * 31,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "String should have at most 30 characters" in str(exc_info.value)

    def test_state_max_length_valid(self):
        """Test state con longitud máxima válida (30 caracteres)"""
        data = {
            "state": "C" * 30,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert len(schema.state) == 30

    def test_state_max_length_invalid(self):
        """Test state excede longitud máxima"""
        data = {
            "state": "C" * 31,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "String should have at most 30 characters" in str(exc_info.value)

    def test_country_max_length_valid(self):
        """Test country con longitud máxima válida (30 caracteres)"""
        data = {
            "country": "D" * 30
        }
        schema = CreateAddressSchema(**data)
        assert len(schema.country) == 30

    def test_country_max_length_invalid(self):
        """Test country excede longitud máxima"""
        data = {
            "country": "D" * 31
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "String should have at most 30 characters" in str(exc_info.value)

    def test_instructions_max_length_valid(self):
        """Test instructions con longitud máxima válida (255 caracteres)"""
        data = {
            "instructions": "E" * 255,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert len(schema.instructions) == 255

    def test_instructions_max_length_invalid(self):
        """Test instructions excede longitud máxima"""
        data = {
            "instructions": "E" * 256,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "String should have at most 255 characters" in str(exc_info.value)

    # Tests para validación de number
    def test_number_valid_positive(self):
        """Test number con valor positivo válido"""
        data = {
            "number": 123,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.number == 123

    def test_number_invalid_zero(self):
        """Test number con valor cero (inválido)"""
        data = {
            "number": 0,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Input should be greater than 0" in str(exc_info.value)

    def test_number_invalid_negative(self):
        """Test number con valor negativo (inválido)"""
        data = {
            "number": -5,
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Input should be greater than 0" in str(exc_info.value)

    # Tests para validación de caracteres en campos de texto
    def test_address_fields_valid_characters(self):
        """Test campos con caracteres válidos incluyendo acentos y ñ"""
        data = {
            "street": "Calle José María",
            "city": "Alcañiz",
            "state": "Aragón",
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.street == "Calle José María"
        assert schema.city == "Alcañiz"
        assert schema.state == "Aragón"
        assert schema.country == "España"

    def test_address_fields_valid_special_characters(self):
        """Test campos con caracteres especiales válidos (guiones, puntos, comas)"""
        data = {
            "street": "Av. San José, 123-A",
            "city": "Sant-Cugat",
            "state": "Barcelona",
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.street == "Av. San José, 123-A"
        assert schema.city == "Sant-Cugat"

    def test_street_invalid_characters(self):
        """Test street con caracteres inválidos"""
        data = {
            "street": "Calle #@$%",
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Contains invalid characters" in str(exc_info.value)

    def test_city_invalid_characters(self):
        """Test city con caracteres inválidos"""
        data = {
            "city": "Madrid@#$",
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Contains invalid characters" in str(exc_info.value)

    def test_state_invalid_characters(self):
        """Test state con caracteres inválidos"""
        data = {
            "state": "Madrid&*()",
            "country": "España"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Contains invalid characters" in str(exc_info.value)

    def test_country_invalid_characters(self):
        """Test country con caracteres inválidos"""
        data = {
            "country": "España@#$"
        }
        with pytest.raises(ValidationError) as exc_info:
            CreateAddressSchema(**data)
        assert "Contains invalid characters" in str(exc_info.value)

    # Tests para limpieza de espacios
    def test_address_fields_extra_spaces_cleanup(self):
        """Test limpieza de espacios extras en campos de dirección"""
        data = {
            "street": "   Calle    Mayor   ",
            "city": "  Madrid  ",
            "state": "   Madrid   ",
            "country": "  España  "
        }
        schema = CreateAddressSchema(**data)
        assert schema.street == "Calle Mayor"
        assert schema.city == "Madrid"
        assert schema.state == "Madrid"
        assert schema.country == "España"

    def test_instructions_spaces_cleanup(self):
        """Test limpieza de espacios en instructions"""
        data = {
            "instructions": "   Casa azul con portón   ",
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.instructions == "Casa azul con portón"

    def test_instructions_none_value(self):
        """Test instructions con valor None"""
        data = {
            "instructions": None,
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.instructions is None

    def test_instructions_empty_string(self):
        """Test instructions con string vacío después de strip"""
        data = {
            "instructions": "   ",
            "country": "España"
        }
        schema = CreateAddressSchema(**data)
        assert schema.instructions == ""

    # Tests de casos edge
    def test_all_optional_fields_none(self):
        """Test con todos los campos opcionales como None"""
        data = {
            "street": None,
            "number": None,
            "city": None,
            "state": None,
            "country": "España",
            "instructions": None
        }
        schema = CreateAddressSchema(**data)
        assert schema.street is None
        assert schema.number is None
        assert schema.city is None
        assert schema.state is None
        assert schema.country == "España"
        assert schema.instructions is None

    def test_numeric_strings_in_text_fields(self):
        """Test campos de texto con solo números"""
        data = {
            "street": "12345",
            "city": "08001",
            "state": "123",
            "country": "123"
        }
        schema = CreateAddressSchema(**data)
        assert schema.street == "12345"
        assert schema.city == "08001"
        assert schema.state == "123"
        assert schema.country == "123"