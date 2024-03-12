class Settings:
    is_register_open: bool = False
    facts: dict
    traits: list = ['name', 'about', 'job', 'relation', 'behavior', 'hobby', 'dark_side', 'gift',
                    'additional', 'first_fact', 'second_fact', 'third_fact']
    is_poll_open: bool = False
    current_poll_users: dict = {}
    current_poll_voted_users: list = []
    users: dict = {}

    def __init__(self):
        self.facts = {}
        for trait in self.traits:
            self.facts[trait] = True


settings = Settings()
