import voz
from voz import falar


def test_pokedex_vazia_avisa_e_nao_carrega_a_voz(monkeypatch, capsys):
    voz_carregada = []
    monkeypatch.setattr(voz.PiperVoice, "load", lambda *a, **k: voz_carregada.append(True))

    falar([])

    assert "A pokedex está vazia" in capsys.readouterr().out
    assert voz_carregada == []
