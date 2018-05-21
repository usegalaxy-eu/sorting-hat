class Destination:
    @classmethod
    def custom_spec(cls):
        pass

    @classmethod
    def is_available(cls):
        return False

    @classmethod
    def reroute_to_dedicated(cls, tool_spec, user_roles):
        return {}
