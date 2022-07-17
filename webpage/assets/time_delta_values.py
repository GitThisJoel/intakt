class TimeDeltaValues:
    _time_options = {
        "daily": {
            "pattern": "(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])",
            "placeholder": "YYYY-MM-DD",
        },
        "weekly": {
            "pattern": "(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])",
            "placeholder": "YYYY-MM-DD",
        },
        "monthly": {
            "pattern": "(\d{4})-(0[1-9]|1[0-2])",
            "placeholder": "YYYY-MM",
        },
        "quarterly": {
            "pattern": "(\d{4})-([1-4])",
            "placeholder": "YYYY-Q",
        },
        "biannually": {
            "pattern": "(\d{4})",
            "placeholder": "YYYY",
        },
        "yearly": {
            "pattern": "(\d{4})",
            "placeholder": "YYYY",
        },
        "custom": {
            "pattern": "(\d{4})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])",
            "placeholder": "YYYY-MM-DD",
        },
    }

    @classmethod
    def options(cls):
        return [{"label": o.capitalize(), "value": o.lower()} for o in cls._time_options.keys()]

    @classmethod
    def patterns(cls):
        return cls._time_options
