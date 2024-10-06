from seasons import Convert


def test_date():
    assert (
        str(Convert(10477))
        == "Fifteen million, eighty-six thousand, eight hundred eighty minutes"
    )
    assert str(Convert(365)) == "Five hundred twenty-five thousand, six hundred minutes"
