class BaseValidator:
    def __init__(self, values: dict = None) -> None:
        self.values = values
        self.reasons = []
        self.is_valid = False
