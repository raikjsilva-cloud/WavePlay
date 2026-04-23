import pygame # type: ignore #Foi instalado a biblioteca pygame-ce importada como pygame para o exercício 21, para reproduzir um arquivo MP3.
import os 
from mutagen.mp3 import MP3 #Biblioteca mutagen para obter a duração total da música.

pygame.init()
pygame.mixer.init()

# Janela
screen = pygame.display.set_mode((750, 200))
pygame.display.set_caption("Player de Música")

font = pygame.font.SysFont(None, 20)
font_pequena = pygame.font.SysFont(None, 16)

# 📂 Pasta com músicas
pasta = "C:\\Projetos\\backup\\Tarcisio"
playlist = [f for f in os.listdir(pasta) if f.endswith(".mp3")]

indice = 0
pausado = False
duracao_total = 0

#Evento para detectar quando a música termina
MUSICA_TERMINOU = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSICA_TERMINOU)

def formatar_tempo(segundos):
    min = segundos // 60
    seg = segundos % 60
    return f"{min:02}:{seg:02}"

def tocar(ind):
    global duracao_total, pausado

    caminho = os.path.join(pasta, playlist[ind])

    #Duração total com o mutagen
    audio = MP3(caminho)
    duracao_total = int(audio.info.length)

    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()
    pausado = False

def desenhar_barra(x, y, largura, altura, progresso):
    pygame.draw.rect(screen, (50, 50, 50), (x, y, largura, altura), border_radius=8)
    largura_preenchida = int(largura * progresso)
    if largura_preenchida > 0:
        pygame.draw.rect(screen, (0,120,120),
                         (x, y, largura_preenchida, altura), 
                         border_radius=8)
if not playlist:
    raise ValueError("Nenhuma música encontrada na pasta especificada.")

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
    
    tempo_atual = tempo_ms // 1000
   
    #evita passar da duração da música
    if tempo_atual > duracao_total:
        tempo_atual = duracao_total

    tempo_restante = max(0, duracao_total - tempo_atual)
    
    #progresso para barra
    progresso = 0
    if duracao_total > 0:
        progresso = tempo_atual / duracao_total

    texto_tempo = font.render(
        f"{formatar_tempo(tempo_atual)} / {formatar_tempo(duracao_total)}",
        True,
        (200, 200, 200))
    screen.blit(texto_tempo, (20, 60))

    texto_restante = font_pequena.render(
        f"Restante: {formatar_tempo(tempo_restante)}",
        True,
        (180, 180, 180)
    )
    screen.blit(texto_restante, (20, 105))

    # Barra de progresso
    desenhar_barra(20, 145, 710, 25, progresso)

    #Status
    status = "Pausado" if pausado else "Reproduzindo"
    texto_status = font_pequena.render(
        f"Status: {status} | P = Pause/Play | N = Próxima | B = Anterior | ESC = Sair",
        True,
        (180, 180, 180)
    )
    screen.blit(texto_status, (20, 180))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == MUSICA_TERMINOU:
            indice = (indice + 1) % len(playlist)
            tocar(indice)

        elif event.type == pygame.KEYDOWN:
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