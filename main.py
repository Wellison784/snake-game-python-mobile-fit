import pygame
import random
import os

# 1. Configurações Iniciais
pygame.init()
largura, altura = 600, 480
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Snake Game Evolution - Welison Pro')
relogio = pygame.time.Clock()

# Cores
PRETO = (15, 15, 15)
BRANCO = (255, 255, 255)
VERDE_CABECA = (0, 180, 0)
VERDE_CORPO = (0, 255, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 255, 0)

# Configurações do Jogo
tamanho_bloco = 20
velocidade_inicial = 10

# Fontes
fonte_placar = pygame.font.SysFont("arial", 22, bold=True)
fonte_status = pygame.font.SysFont("arial", 30, bold=True)
fonte_icones = pygame.font.SysFont("arial", 28, bold=True)


# --- SISTEMA DE RECORDE ---
def carregar_recorde():
    if not os.path.exists("recorde.txt"):
        return 0
    with open("recorde.txt", "r") as f:
        try:
            conteudo = f.read().strip()
            return int(conteudo) if conteudo else 0
        except:
            return 0


def salvar_recorde(pontos):
    if pontos > carregar_recorde():
        with open("recorde.txt", "w") as f:
            f.write(str(pontos))


def resetar_recorde_txt():
    if os.path.exists("recorde.txt"):
        os.remove("recorde.txt")


# --- CONFIGURAÇÃO DA UI (CONTROLES JUNTOS) ---
tam_b = 35
margem = 20
# Posicionando as setas em formato de cruz (D-Pad) no canto direito
botoes_pos = {
    'UP': (largura - tam_b * 2 - margem, altura - tam_b * 3 - margem),
    'DOWN': (largura - tam_b * 2 - margem, altura - tam_b - margem),
    'LEFT': (largura - tam_b * 3 - margem, altura - tam_b * 2 - margem),
    'RIGHT': (largura - tam_b - margem, altura - tam_b * 2 - margem)
}
btn_pausa_rect = pygame.Rect(largura - 55, 15, 40, 40)


def desenhar_ui(pontos, recorde, pausado):
    # Placar e Recorde
    tela.blit(fonte_placar.render(f"PONTOS: {pontos}", True, AMARELO), [20, 20])
    tela.blit(fonte_placar.render(f"RECORDE: {recorde}", True, BRANCO), [20, 45])
    tela.blit(fonte_placar.render("Pressione R para Resetar", True, (100, 100, 100)), [20, altura - 30])

    # Botão de Pausa
    pygame.draw.rect(tela, (80, 80, 80), btn_pausa_rect, border_radius=8)
    txt_p = "||" if not pausado else "▶"
    tela.blit(fonte_icones.render(txt_p, True, BRANCO), (btn_pausa_rect.x + 10, btn_pausa_rect.y + 2))

    # Desenho dos Controles (Círculos Juntos)
    for direcao, pos in botoes_pos.items():
        surf = pygame.Surface((tam_b, tam_b), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 255, 255, 40), (tam_b // 2, tam_b // 2), tam_b // 2)
        pygame.draw.circle(surf, BRANCO, (tam_b // 2, tam_b // 2), tam_b // 2, 2)

        simbolos = {'UP': '▲', 'DOWN': '▼', 'LEFT': '◄', 'RIGHT': '►'}
        txt = fonte_icones.render(simbolos[direcao], True, BRANCO)
        surf.blit(txt, txt.get_rect(center=(tam_b // 2, tam_b // 2)))
        tela.blit(surf, pos)


def jogar():
    jogo_encerrado = False
    game_over = False
    pausado = False
    x, y = largura / 2, altura / 3
    dx, dy = 0, 0
    corpo_cobra = []
    comprimento_cobra = 1
    pontos = 0
    velocidade = velocidade_inicial

    comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
    comida_y = round(random.randrange(80, altura - 200) / 20.0) * 20.0

    while not jogo_encerrado:
        recorde_atual = carregar_recorde()

        while game_over:
            salvar_recorde(pontos)
            tela.fill(PRETO)
            msg = fonte_status.render("FIM DE JOGO! Toque Jogar de novo", True, VERMELHO)
            tela.blit(msg, [largura / 2 - 210, altura / 2])
            pygame.display.update()
            for ev in pygame.event.get():
                if ev.type in [pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN]: jogar()
                if ev.type == pygame.QUIT: jogo_encerrado = True; game_over = False

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: jogo_encerrado = True

            if ev.type == pygame.MOUSEBUTTONDOWN:
                if btn_pausa_rect.collidepoint(ev.pos): pausado = not pausado
                if not pausado:
                    # Lógica de clique nos botões direcionais
                    if pygame.Rect(botoes_pos['UP'], (tam_b, tam_b)).collidepoint(ev.pos) and dy == 0:
                        dx, dy = 0, -tamanho_bloco
                    elif pygame.Rect(botoes_pos['DOWN'], (tam_b, tam_b)).collidepoint(ev.pos) and dy == 0:
                        dx, dy = 0, tamanho_bloco
                    elif pygame.Rect(botoes_pos['LEFT'], (tam_b, tam_b)).collidepoint(ev.pos) and dx == 0:
                        dx, dy = -tamanho_bloco, 0
                    elif pygame.Rect(botoes_pos['RIGHT'], (tam_b, tam_b)).collidepoint(ev.pos) and dx == 0:
                        dx, dy = tamanho_bloco, 0

            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_p: pausado = not pausado
                if ev.key == pygame.K_r: resetar_recorde_txt()  # RESET FUNCIONANDO AQUI
                if not pausado:
                    if ev.key == pygame.K_UP and dy == 0:
                        dx, dy = 0, -tamanho_bloco
                    elif ev.key == pygame.K_DOWN and dy == 0:
                        dx, dy = 0, tamanho_bloco
                    elif ev.key == pygame.K_LEFT and dx == 0:
                        dx, dy = -tamanho_bloco, 0
                    elif ev.key == pygame.K_RIGHT and dx == 0:
                        dx, dy = tamanho_bloco, 0

        if not pausado:
            x += dx
            y += dy
            if x >= largura or x < 0 or y >= altura or y < 0: game_over = True

            tela.fill(PRETO)
            pygame.draw.circle(tela, VERMELHO, (int(comida_x + 10), int(comida_y + 10)), 9)

            cabeca = [x, y]
            corpo_cobra.append(cabeca)
            if len(corpo_cobra) > comprimento_cobra: del corpo_cobra[0]
            for bloco in corpo_cobra[:-1]:
                if bloco == cabeca: game_over = True

            for i, bloco in enumerate(corpo_cobra):
                cor = VERDE_CABECA if i == len(corpo_cobra) - 1 else VERDE_CORPO
                pygame.draw.rect(tela, cor, [bloco[0], bloco[1], tamanho_bloco - 1, tamanho_bloco - 1], border_radius=5)
                if i == len(corpo_cobra) - 1:  # Olhinhos Brancos
                    pygame.draw.circle(tela, BRANCO, (int(bloco[0] + 6), int(bloco[1] + 6)), 3)
                    pygame.draw.circle(tela, BRANCO, (int(bloco[0] + 14), int(bloco[1] + 6)), 3)

            if x == comida_x and y == comida_y:
                comida_x = round(random.randrange(0, largura - tamanho_bloco) / 20.0) * 20.0
                comida_y = round(random.randrange(80, altura - 200) / 20.0) * 20.0
                comprimento_cobra += 1
                pontos += 10
                velocidade = velocidade_inicial + (pontos // 50)

        desenhar_ui(pontos, recorde_atual, pausado)
        if pausado:
            tela.blit(fonte_status.render("PAUSADO", True, AMARELO), [largura / 2 - 65, altura / 2 - 20])

        pygame.display.update()
        relogio.tick(velocidade)

    pygame.quit()


jogar()