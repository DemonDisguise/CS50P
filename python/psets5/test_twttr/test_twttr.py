from twttr import shorten

def test_assert():
    assert shorten("hello world") == "hll wrld"
    assert shorten("HELL@ WORLD") == "HLL@ WRLD"
    assert shorten("hell3 world4") == "hll3 wrld4"
    assert shorten("h@llo w*rld!!") == "h@ll w*rld!!"
