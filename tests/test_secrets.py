from promptsentinel import Scanner


def test_detects_aws_access_key():
    r = Scanner().scan("AKIAIOSFODNN7EXAMPLE is the key")
    assert any(f.detector == "secrets.aws_access_key" for f in r.findings)


def test_detects_github_token():
    r = Scanner().scan("token: ghp_abcdefghijklmnopqrstuvwxyz0123456789")
    assert any(f.detector == "secrets.github_token" for f in r.findings)


def test_detects_openai_key():
    r = Scanner().scan("OPENAI_API_KEY=sk-proj-abcd1234abcd1234abcd1234abcd1234")
    assert any(f.detector == "secrets.openai_key" for f in r.findings)


def test_detects_anthropic_key():
    r = Scanner().scan("ANTHROPIC=sk-ant-api03-abcdef0123456789abcdef0123456789")
    assert any(f.detector == "secrets.anthropic_key" for f in r.findings)


def test_detects_jwt():
    r = Scanner().scan(
        "auth: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.abcdef1234567890abcdef"
    )
    assert any(f.detector == "secrets.jwt" for f in r.findings)


def test_detects_private_key():
    r = Scanner().scan("-----BEGIN RSA PRIVATE KEY-----\nMIIE...\n")
    assert any(f.detector == "secrets.private_key" for f in r.findings)


def test_detects_google_api_key():
    r = Scanner().scan("Google key: AIzaSyA1234567890abcdefghijklmnopqrstuv")
    assert any(f.detector == "secrets.google_api_key" for f in r.findings)


def test_detects_slack_token():
    r = Scanner().scan("Slack token: xoxb-1234567890-abcdefghijkl")
    assert any(f.detector == "secrets.slack_token" for f in r.findings)


def test_detects_stripe_key():
    dummy_key = "sk_" + "test_" + "1234567890abcdefghijklmn"
    r = Scanner().scan(f"Stripe key: {dummy_key}")
    assert any(f.detector == "secrets.stripe_key" for f in r.findings)


def test_detects_aws_secret_key():
    r = Scanner().scan("aws_secret_key = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'")
    assert any(f.detector == "secrets.aws_secret_key" for f in r.findings)


def test_shannon_entropy_empty():
    from promptsentinel.detectors.secrets import _shannon_entropy

    assert _shannon_entropy("") == 0.0
