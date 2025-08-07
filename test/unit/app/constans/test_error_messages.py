import pytest

from app.constans import error_messages

class TestErrorMessages:
    def test_get_error_message_success(self):
        msg = error_messages.get_error_message(
            'USER_NOT_FOUND',
            field='email',
            value='test@example.com'
        )
        assert msg == "User with email = 'test@example.com' not found"

    def test_get_error_message_missing_key(self):
        msg = error_messages.get_error_message('DOES_NOT_EXIST')
        assert msg == error_messages.ERROR_MESSAGES['UNKNOWN_ERROR']


    def test_get_error_message_missing_param(self):
        msg = error_messages.get_error_message('USER_NOT_FOUND', value='abc')
        assert "Error message template missing parameter" in msg

    @pytest.mark.parametrize(
        "error_type,expected_key,expected_msg_part,extra_kwargs", [
            ('required', 'MISSING_REQUIRED_FIELD', 'Missing required field', {}),
            ('type', 'INVALID_FIELD_TYPE', "must be of type", {'expected_type': 'string'})
        ]
    )
    def test_get_validation_message(self, error_type, expected_key, expected_msg_part, extra_kwargs):
        msg = error_messages.get_validation_message(
            field='username',
            error_type=error_type,
            **extra_kwargs
        )
        assert expected_msg_part in msg
