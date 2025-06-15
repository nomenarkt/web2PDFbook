from web2pdfbook.config import load_config


def test_load_config_env(monkeypatch):
    monkeypatch.setenv("WEB2PDFBOOK_TIMEOUT", "9999")
    cfg = load_config()
    assert cfg.timeout == 9999
