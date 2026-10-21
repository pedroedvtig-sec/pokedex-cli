from hectogramas_para_kg import calculo


def test_divisao_exata_vira_numero_inteiro():
    assert calculo(60) == 6
    assert type(calculo(60)) is int


def test_divisao_com_resto_mantem_a_casa_decimal():
    assert calculo(132) == 13.2


def test_peso_menor_que_1_kg():
    assert calculo(1) == 0.1


def test_peso_zero():
    assert calculo(0) == 0


def test_peso_grande():
    assert calculo(9999) == 999.9


def test_texto_sai_sem_ponto_zero():
    assert f"{calculo(60)} kg" == "6 kg"
    assert f"{calculo(132)} kg" == "13.2 kg"
