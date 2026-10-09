from detector.features import FEATURE_NAMES, extract_features, explain_url, feature_vector


def test_feature_vector_shape():
    vector = feature_vector("https://example.com/login")
    assert len(vector) == len(FEATURE_NAMES)


def test_ip_hostname_is_detected():
    features = extract_features("http://192.168.1.10/login")
    assert features["has_ip_address"] == 1


def test_https_is_detected():
    features = extract_features("https://example.com")
    assert features["has_https"] == 1


def test_punycode_is_detected():
    features = extract_features("https://xn--e1afmkfd.xn--p1ai/login")
    assert features["has_punycode"] == 1


def test_explanation_returns_text():
    signals = explain_url("http://192.168.1.10/account/verify")
    assert signals
    assert all(isinstance(item, str) for item in signals)
