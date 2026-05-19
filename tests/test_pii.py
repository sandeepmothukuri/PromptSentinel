from promptshield import Scanner


def test_detects_email():
    r = Scanner().scan("contact me at john.doe@example.com please")
    names = {f.detector for f in r.findings}
    assert "pii.email" in names


def test_detects_ssn():
    r = Scanner().scan("My SSN is 123-45-6789.")
    assert any(f.detector == "pii.ssn" for f in r.findings)


def test_detects_credit_card_luhn():
    # Valid Luhn test number
    r = Scanner().scan("card: 4111 1111 1111 1111")
    assert any(f.detector == "pii.credit_card" for f in r.findings)


def test_ignores_invalid_credit_card():
    r = Scanner().scan("number: 1234 5678 9012 3456")
    assert not any(f.detector == "pii.credit_card" for f in r.findings)


def test_detects_phone():
    r = Scanner().scan("Call (555) 123-4567 today.")
    assert any(f.detector == "pii.phone" for f in r.findings)


def test_detects_ipv4():
    r = Scanner().scan("server at 192.168.1.1")
    assert any(f.detector == "pii.ipv4" for f in r.findings)
