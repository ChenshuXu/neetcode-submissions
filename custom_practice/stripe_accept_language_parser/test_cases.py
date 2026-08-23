from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="exact matches follow header preference",
        args=("fr-CA, en-US", ("en-US", "fr-CA", "fr-FR")),
        expected=["fr-CA", "en-US"],
    ),
    Case(
        name="base range expands in supported order",
        args=("fr", ("en-US", "fr-FR", "fr-CA", "fr")),
        expected=["fr-FR", "fr-CA", "fr"],
    ),
    Case(
        name="quality overrides textual order",
        args=("fr-CA;q=0.4, en-US;q=1, fr-FR;q=0.8", ("fr-CA", "en-US", "fr-FR")),
        expected=["en-US", "fr-FR", "fr-CA"],
    ),
    Case(
        name="quality ties keep original range order",
        args=("de;q=0.7, fr;q=0.7", ("fr-FR", "de-DE", "fr-CA", "de-AT")),
        expected=["de-DE", "de-AT", "fr-FR", "fr-CA"],
    ),
    Case(
        name="zero quality excludes range",
        args=("en;q=0, fr;q=1", ("en-US", "fr-FR")),
        expected=["fr-FR"],
    ),
    Case(
        name="wildcard appends every remaining supported language",
        args=("fr-FR, *;q=0.1", ("en-US", "fr-FR", "de-DE")),
        expected=["fr-FR", "en-US", "de-DE"],
    ),
    Case(
        name="matching is case insensitive but preserves supported spelling",
        args=("EN-us, FR", ("en-US", "Fr-ca")),
        expected=["en-US", "Fr-ca"],
    ),
    Case(
        name="invalid ranges and duplicate matches are ignored",
        args=("en-US, en-US;q=0.5, bad--tag, fr;q=2, de;q=nope", ("en-US", "fr-FR", "de-DE")),
        expected=["en-US"],
    ),
    Case(
        name="empty header returns empty result",
        args=("", ("en-US", "fr-FR")),
        expected=[],
    ),
]
