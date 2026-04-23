import pygame # type: ignore #Foi instalado a biblioteca pygame-ce importada como pygame para o exercício 21, para reproduzir um arquivo MP3.
import os 
from mutagen.mp3 import MP3 #Biblioteca mutagen para obter a duração total da música.

'''Código sem barra de progresso, mas com nome da música, tempo atual e tempo total. 
Usei a biblioteca mutagen para obter a duração total da música, já que o pygame não fornece essa informação diretamente. 
O player suporta play/pause, próxima e anterior. A música muda automaticamente quando termina.'''

pygame.init()
pygame.mixer.init()

# Janela
screen = pygame.display.set_mode((900, 200))
pygame.display.set_caption("Player de Música")

font = pygame.font.SysFont(None, 28)

# 📂 Pasta com músicas
pasta = "C:\\Projetos\\backup\\Tarcisio"
playlist = [f for f in os.listdir(pasta) if f.endswith(".mp3")]

indice = 0
pausado = False
duracao_total = 0

#Evento para detectar quando a música termina
MUSICA_TERMINOU = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSICA_TERMINOU)

def tocar(ind):
    global duracao_total, pausado

    caminho = os.path.join(pasta, playlist[ind])

    #Duração total com o mutagen
    audio = MP3(caminho)
    duracao_total = int(audio.info.length)

    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()
    pausado = False

tocar(indice)

clock = pygame.time.Clock()
rodando = True

while rodando:
    screen.fill((30, 30, 30))

    # 🎵 Nome da música
    nome = playlist[indice]
    texto_nome = font.render(f"Tocando: {nome}", True, (255, 255, 255))
    screen.blit(texto_nome, (20, 20))

    # ⏱ Tempo atual
    tempo_ms = pygame.mixer.music.get_pos()
    if tempo_ms < 0:
        tempo_ms = 0
        #tempo_ms = duracao_total * 1000
   
    tempo_seg = tempo_ms // 1000
    min_atual = tempo_seg // 60
    seg_atual = tempo_seg % 60

    # Tempo total
    min_total = duracao_total // 60
    seg_total = duracao_total % 60

    texto_tempo = font.render(
        f"Tempo: {min_atual:02}:{seg_atual:02} / {min_total:02}:{seg_total:02}", 
        True, 
        (200, 200, 200))
    screen.blit(texto_tempo, (20, 60))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == MUSICA_TERMINOU:
            indice = (indice + 1) % len(playlist)
            tocar(indice)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False

            # ▶️ Play / Pause (P)
            elif event.key == pygame.K_p:
                pausado = not pausado
                if pausado:
                    pygame.mixer.music.pause()
                else:
                    pygame.mixer.music.unpause()

            # ⏭ Próxima (N)
            elif event.key == pygame.K_n:
                indice = (indice + 1) % len(playlist)
                tocar(indice)

            # ⏮ Anterior (B)
            elif event.key == pygame.K_b:
                indice = (indice - 1) % len(playlist)
                tocar(indice)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()