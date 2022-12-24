from src.domain.user import UserReply


class Test_UserReply:
    def test_valid_reply(self):
        # Act
        result = UserReply("/command reply")

        # Assert
        assert result.is_valid is True
        assert result.value == "reply"

    def test_invalid_reply(self):
        # Act
        result = UserReply("/command")

        # Assert
        assert result.is_valid is False
