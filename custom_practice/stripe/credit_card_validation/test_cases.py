from custom_practice.runner import Case


TEST_CASES = [
    Case(
        name="classify three known networks",
        args=((
            ("classify", "4111111111111111"),
            ("classify", "5555555555554444"),
            ("classify", "378282246310005"),
        ),),
        expected=("VISA", "MASTERCARD", "AMEX"),
    ),
    Case(
        name="valid unknown checksum differs from invalid",
        args=((
            ("classify", "79927398713"),
            ("classify", "4111111111111112"),
            ("classify", "4111x11111111111"),
        ),),
        expected=("UNKNOWN", "INVALID", "INVALID"),
    ),
    Case(
        name="single redacted check or prefix digit",
        args=((
            ("count_redacted", "411111111111111?"),
            ("count_redacted", "?111111111111111"),
        ),),
        expected=(1, 1),
    ),
    Case(
        name="two redacted digits enumerate all valid substitutions",
        args=((("count_redacted", "41111111111111??"),),),
        expected=(10,),
    ),
    Case(
        name="repair returns every one-position correction",
        args=((("repair_one_digit", "4111111111111112"),),),
        expected=((
            "4011111111111112",
            "4110111111111112",
            "4111101111111112",
            "4111111011111112",
            "4111111110111112",
            "4111111111101112",
            "4111111111111012",
            "4111111111111111",
            "4111111111111152",
            "4111111111115112",
            "4111111111511112",
            "4111111151111112",
            "4111115111111112",
            "4111511111111112",
            "4151111111111112",
        ),),
    ),
    Case(
        name="repair short nonnetwork number has no candidate",
        args=((("repair_one_digit", "1234"),),),
        expected=((),),
    ),
]
