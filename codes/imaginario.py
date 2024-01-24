import pygame
from sys import exit
from time import sleep
from random import randint

#inicio básico
pygame.init()
largura = 800
altura = 400
janela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Imaginário')

#score
def score():
    tempo = (pygame.time.get_ticks() - reiniciar) // 1000
    text = pygame.font.Font('font/Yumaro.otf',20)
    mostrar_score = text.render(f'Score: {tempo:05d}', False, (0,0,0))
    janela.blit(mostrar_score,(30,20))
reiniciar = 0

#controle de frames
frame_segundo = pygame.time.Clock() 

#imagens 
cenario = pygame.image.load("sprites/cenario.png").convert_alpha() #colocar a imgame do cenario
chao = pygame.image.load("sprites/chao.png").convert_alpha() #adicionar chão
home = pygame.image.load("sprites/inicio.png").convert_alpha()
mob_formiga = pygame.image.load("mobs/F.png").convert_alpha()
mob_borboleta = pygame.image.load("mobs/borboleta_1.png").convert_alpha()
mob_borboleta_2 = pygame.image.load("mobs/borboleta_2.png").convert_alpha()
player = pygame.image.load("protagonista/Me_1.png").convert_alpha()
player_2 = pygame.image.load("protagonista/Me_2.png").convert_alpha()
player_3 = pygame.image.load("protagonista/Me_3.png").convert_alpha()
player_abaixando = pygame.image.load('protagonista/Me_6.png')

#retangulos das imagens
formiga_rect = mob_formiga.get_rect(midright=(700,291))
borboleta_rect = mob_borboleta.get_rect(midright=(370,210))
player_rect = player.get_rect(midbottom=(100,310))

#sprites
player_caminhar = [player_abaixando,player,player_2,player_3]
player_index = 1
player_sprites = player_caminhar[player_index]
borboleta_voar = [mob_borboleta,mob_borboleta_2]
borboleta_index = 0
borboleta_sprites = borboleta_voar[borboleta_index]

#movimento 
gravidade = 0

#timer
timer = pygame.USEREVENT + 1
pygame.time.set_timer(timer,1600)
borboleta_timer  = pygame.USEREVENT + 2
pygame.time.set_timer(borboleta_timer,200) #quanto maior o valor mais devagar  

#melhorar spawn
lista_retangulos = []

#colisão
def colisão(jogador,lista):
    if lista: #se a lista não estiver vazia
        for elementos in lista:
            if jogador.colliderect(elementos):
                return False
    return True

#animação
def animação():
    global player_sprites,player_index
    if player_rect.bottom < 310:
        player_sprites = player
    else:
        if player_index != 0:
            player_index += 0.1
            if player_index >= len(player_caminhar):
                player_index = 1
            player_sprites = player_caminhar[int(player_index)]
        else:
            player_sprites = player_caminhar[player_index]

#movimentar mobs
def movimento(lista_obstaculos):
    if lista_retangulos:
        for obstaculos in lista_obstaculos:
            obstaculos.x -= 4
            if obstaculos.y == 276:
                janela.blit(mob_formiga,obstaculos)
            else:
                janela.blit(borboleta_sprites,obstaculos)
        lista_obstaculos = [o for o in lista_obstaculos if o.x > -100]
        return lista_obstaculos
    else:
        return []

#inicio
start = False
nome = pygame.image.load("sprites/nome.2.png").convert_alpha()
s = pygame.image.load("sprites/nome.png").convert_alpha()

#fim
game_rodando = True
texto = pygame.font.Font('font/Yumaro.otf',40)
perdeu = texto.render('Perdeu mané',False,'black')
fim = pygame.image.load('sprites/Fim.png')
texto_2 = pygame.font.Font('font/Yumaro.otf',15)
reset = texto_2.render('[Pressione R para jogar novamente]',False,'black')
close = texto_2.render("[Aperte C para fechar]",False,'black')

#audio
pulo = pygame.mixer.Sound('audio/pulo.wav')

#aparecer na janela 
while True:
    for event in pygame.event.get(): #todos os eventos que eu quero confeirr vai dentro do for 
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:  #se apertar em c fecha
                if event.key == pygame.K_c:
                    pygame.quit()
                    exit()
        if game_rodando:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 310:
                    gravidade = -21
                    player_rect.bottom = 310
                    pulo.play()
                if event.key == pygame.K_DOWN:
                    player_index = 0
                    player_rect = player_abaixando.get_rect(midbottom=(100,310)) #abaixar
                if event.key == pygame.K_s:
                    start = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_index = 1 #para levantar
                    player_rect = player.get_rect(midbottom=(100,310))
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                        game_rodando = True
                        reiniciar = pygame.time.get_ticks() 
                        lista_retangulos.clear()
                        pygame.mixer.music.load('audio/fundo.mp3')
                        pygame.mixer.music.play(-1)
                        pygame.mixer.music.set_volume(0.2)
                        gravidade = 0
        if game_rodando:
            if event.type == timer:
                if randint(0,2):
                    formiga_rect = mob_formiga.get_rect(midright=(randint(900,1100),291))
                    lista_retangulos.append(formiga_rect)
                else:
                    borboleta_rect = mob_borboleta.get_rect(midright=(randint(900,1100),215))
                    lista_retangulos.append(borboleta_rect)
            if event.type == borboleta_timer:
                if borboleta_index == 0:
                    borboleta_index = 1
                else:
                    borboleta_index = 0
                borboleta_sprites = borboleta_voar[borboleta_index]
    if start:
        if game_rodando:        
            janela.blit(cenario,(0,0)) #mostrar a imagem do cenario na tela, pois o blit serve para isso
            janela.blit(chao,(0,300))
            animação()
            janela.blit(player_sprites,player_rect) 
            score()

            lista_retangulos = movimento(lista_retangulos) #função para movimentar os mobs, onde vai atualizando a lista

            game_rodando = colisão(player_rect,lista_retangulos)
            
            gravidade += 1
            player_rect.y += gravidade
            if player_rect.bottom >= 310:
                player_rect.bottom = 310
            point = texto_2.render(f"Sua pontuação foi: {(pygame.time.get_ticks() - reiniciar) // 1000}",False,'black')
        else: #tela do gameover
            janela.blit(fim,(0,0)) 
            janela.blit(perdeu,(220,240))
            janela.blit(reset,(220,320))
            janela.blit(close,(270,350))
            janela.blit(point,(275,290))
            pygame.mixer.music.stop()
    else: #tela de inicio
        janela.blit(home,(0,0))
        janela.blit(nome,(10,60))
        janela.blit(s,(60,150))
        pygame.mixer.music.load('audio/fundo.mp3')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.2)
        lista_retangulos.clear()
        reiniciar = pygame.time.get_ticks() 
        gravidade = 0

    pygame.display.update()
    frame_segundo.tick(60) #dizer para o loop máx de rodadas