import wave
import subprocess
from piper import PiperVoice

def falar(pokedex):
    if pokedex:
        motor = PiperVoice.load("pt_BR-jeff-medium.onnx")
        for i in pokedex:
            apelido = i.get('apelido') or 'sem apelido'
            with wave.open("pokedex.wav", "wb") as arquivo:
                motor.synthesize_wav(f"Pokemón: {i['nome']} Apelido: {apelido} Tipo: {', '.join(i['tipos'])} Peso: {i['peso']/10} kg", arquivo)
            subprocess.run(["paplay", "pokedex.wav"])
    else:
        print("A pokedex está vazia, capture um pokemón para que o programa possa ler e falar.")