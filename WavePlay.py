import io

import pygame # type: ignore #Foi instalado a biblioteca pygame-ce importada como pygame para o exercício 21, para reproduzir um arquivo MP3.
import os 
from mutagen.mp3 import MP3 #Biblioteca mutagen para obter a duração total da música.
from mutagen.id3 import ID3, ID3NoHeaderError #Para ler as tags ID3 das músicas, como título e artista.

pygame.init()
pygame.mixer.init()

# Janela
LARGURA = 970
ALTURA = 320
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Player de Música")

font = pygame.font.SysFont(None, 20)
font_pequena = pygame.font.SysFont(None, 16)

# 📂 Pasta com músicas
pasta = "sua_pasta_de_musicas" # Substitua pelo caminho da sua pasta de músicas
playlist = [f for f in os.listdir(pasta) if f.endswith(".mp3")]

if not playlist:
    raise ValueError("Nenhuma música encontrada na pasta especificada.")

indice = 0
pausado = False
duracao_total = 0
capa_atual = None


#Evento para detectar quando a música termina
MUSICA_TERMINOU = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSICA_TERMINOU)

COR_FUNDO = (30, 30, 30)
COR_TEXTO = (255, 255, 255)
COR_TEXTO_SEC = (190, 190, 190)
COR_BARRA = (70, 70, 70)
COR_PROGRESSO = (0, 180, 120)
COR_BOTAO = (55, 55, 55)
COR_BOTAO_HOVER = (85, 85, 85)
COR_SEM_CAPA = (60, 60, 60)

react_anterior = pygame.Rect(260, 230, 140, 45)
react_play = pygame.Rect(410, 230, 140, 45)
react_proxima = pygame.Rect(560, 230, 140, 45)

def formatar_tempo(segundos):
    min = segundos // 60
    seg = segundos % 60
    return f"{min:02}:{seg:02}"

def obter_capa(caminho):
    try:
        tags = ID3(caminho)
        apic_list = tags.getall("APIC")
        if apic_list:
            imagem_bytes = apic_list[0].data
            imagem_stream = io.BytesIO(imagem_bytes)
            imagem = pygame.image.load(imagem_stream)
            return pygame.transform.smoothscale(imagem, (200, 200))
    except ID3NoHeaderError:
        pass
    except pygame.error:
        pass
    return None

def tocar(ind):
    global duracao_total, pausado, capa_atual

    caminho = os.path.join(pasta, playlist[ind])

    #Duração total com o mutagen
    audio = MP3(caminho)
    duracao_total = int(audio.info.length)

    capa_atual = obter_capa(caminho)

    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()
    pausado = False



def desenhar_barra(x, y, largura, altura, progresso):
    pygame.draw.rect(screen, COR_BARRA, (x, y, largura, altura), border_radius=8)
    
    largura_preenchida = int(largura * progresso)
    if largura_preenchida > 0:
        pygame.draw.rect(
            screen, 
            COR_PROGRESSO,
            (x, y, largura_preenchida, altura), 
            border_radius=8
        )

def desenhar_botao(rect, texto):
    mouse_pos = pygame.mouse.get_pos()
    cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(screen, cor, rect, border_radius=8)

    txt = font_pequena.render(texto, True, COR_TEXTO)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


def proxima_musica():
    global indice
    indice = (indice + 1) % len(playlist)
    tocar(indice)

def musica_anterior():
    global indice
    indice = (indice - 1) % len(playlist)
    tocar(indice)

def alternar_pause():
    global pausado
    pausado = not pausado
    if pausado:
        pygame.mixer.music.pause()
    else: 
        pygame.mixer.music.unpause()

tocar(indice)

clock = pygame.time.Clock()
rodando = True

while rodando:
    screen.fill(COR_FUNDO)

    # 🎵 Nome da música
    nome = playlist[indice]

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
    progresso = tempo_atual / duracao_total if duracao_total > 0 else 0

    # Capa da música
    capa_x = 30
    capa_y = 40
    if capa_atual:
        screen.blit(capa_atual, (capa_x, capa_y))
    else:
        pygame.draw.rect(screen, COR_SEM_CAPA, (capa_x, capa_y, 200, 200), border_radius=8)
        texto_sem_capa = font_pequena.render("Sem Capa", True, COR_TEXTO)
        rect_sem_capa = texto_sem_capa.get_rect(center=(capa_x + 100, capa_y + 100))
        screen.blit(texto_sem_capa, rect_sem_capa)

    # Nome da música
    texto_nome = font.render(f"{nome}", True, COR_TEXTO)
    screen.blit(texto_nome, (240, 30))

    # Tempos
    texto_tempo = font.render(
        f"{formatar_tempo(tempo_atual)} / {formatar_tempo(duracao_total)}",
        True,
        COR_TEXTO
    )
    screen.blit(texto_tempo, (240, 75))

    texto_restante = font_pequena.render(
        f"Restante: -{formatar_tempo(tempo_restante)}",
        True,
        COR_TEXTO_SEC
    )  
    screen.blit(texto_restante, (240, 120))

    # Barra de progresso
    desenhar_barra(240, 160, 700, 25, progresso)

    # Botões
    desenhar_botao(react_anterior, "Anterior (B)")
    desenhar_botao(react_play, "Pause (P)" if not pausado else "Play (P)")
    desenhar_botao(react_proxima, "Próxima (N)")

    #Status
    status = "Pausado" if pausado else "Reproduzindo"
    texto_status = font_pequena.render(f"Status: {status}", True, COR_TEXTO_SEC)
    screen.blit(texto_status, (240, 290))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == MUSICA_TERMINOU:
            proxima_musica()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            # ▶️ Play / Pause (P)
            elif event.key == pygame.K_p:
                alternar_pause()
            elif pausado:
                proxima_musica()
            elif event.key == pygame.K_b:
                musica_anterior()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if react_anterior.collidepoint(event.pos):
                    musica_anterior()
                elif react_play.collidepoint(event.pos):
                    alternar_pause()
                elif react_proxima.collidepoint(event.pos):
                    proxima_musica()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()