import pygame
import os
import random

print('aqui')

TELA_LARGURA = 500
TELA_ALTURA = 800

IMAGEM_CANO= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','pipe.png')))
IMAGEM_CHAO= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','base.png')))
IMAGEM_BACKGROUND= pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bg.png')))
IMAGEM_PASSARO = [ 
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird1.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird2.png'))),
    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs','bird3.png')))
]    

pygame.font.init()
FONTE_PONTOS = pygame.font.SysFont('arial', 50)

class Passaro:
  IMGS = IMAGEM_PASSARO

  rotacao_maxima = 25
  velocidade_rotacao = 20
  tempo_de_animacao = 5

  def __init__(self, x , y):
    self.x = x
    self.y = y
    self.angulo = 0
    self.velocidade = 0
    self.altura = self.y
    self.tempo = 0
    self.contagem_imagem = 0
    self.imagem = self.IMGS[0]

  def pular(self):
    print('pulando')
    self.velocidade = -10.5
    self.tempo = 0
    self.altura = self.y

  def mover(self):
    self.tempo += 1
    deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo
    if deslocamento > 16:
      deslocamento = 16
    elif deslocamento < 0 :
      deslocamento -= 2 

    self.y += deslocamento   

    if deslocamento < 0 or self.y < (self.altura + 50):
      if self.angulo < self.rotacao_maxima :
        self.altura + self.rotacao_maxima
    else:
      if self.angulo > -90:
        self.angulo -= self.rotacao_maxima

  def desenhar(self, tela):
    self.contagem_imagem += 1

    if self.contagem_imagem < self.tempo_de_animacao:
      self.imagem = self.IMGS[0]
    
    elif self.contagem_imagem < self.tempo_de_animacao * 2:
      self.imagem = self.IMGS[1]
    elif self.contagem_imagem < self.tempo_de_animacao * 3:
      self.imagem = self.IMGS[2]
    elif self.contagem_imagem < self.tempo_de_animacao * 4:
      self.imagem = self.IMGS[1]
    elif self.contagem_imagem >= self.tempo_animacao*4 + 1:
      self.imagem = self.IMGS[0]
      self.contagem_imagem = 0

    if self.angulo <= -80:
      self.imagem = self.IMGS[1]
      self.contagem_imagem = self.tempo_de_animacao * 2

    imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
    pos_centro_imagem = self.imagem.get_rect(topleft=(self.x , self.y)).center 
    retangulo = imagem_rotacionada.get_rect(center= pos_centro_imagem)
    tela.blit(imagem_rotacionada, retangulo.topleft)
  
  def get_mask(self):
    return pygame.mask.from_surface(self.imagem)


class Cano:
  DISTANCIA = 200 
  velocidade = 5

  def __init__(self,x):
    self.x = x
    self.altura = 0
    self.pos_topo =0 
    self.pos_base = 0
    self.CANO_TOPO = pygame.transform.flip(IMAGEM_CANO, False, True)
    self.CANO_BASE = IMAGEM_CANO
    self.passou = False
    self.definir_altura ()

  def definir_altura(self):
    self.altura = random.randrange(50, 450)
    self.pos_base = self.altura - self.CANO_TOPO.get_height()
    self.pos_base = self.altura + self.DISTANCIA

  def mover(self):
    self.x -= self.velocidade

  def desenhar(self, tela):   
    tela.blit(self.CANO_TOPO,(self.x, self.pos_topo))
    tela.blit(self.CANO_BASE,(self.x, self.pos_base))

  def colidir(self, passaro):
    passaro_mask = passaro.get_mask()
    topo_mask = pygame.mask.from_surface(self.CANO_TOPO)
    base_mask = pygame.mask.from_surface(self.CANO_BASE)

    DISTANCIA_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))
    DISTANCIA_base =  (self.x - passaro.x, self.pos_base - round(passaro.y))
    
    topo_ponto = passaro_mask.overlap(topo_mask, DISTANCIA_topo)
    base_ponto = passaro_mask.overlap(base_mask, DISTANCIA_base)

    if base_ponto or topo_ponto:
      return  True
    else:
      return False

class Chao:
  velocidade = 5
  largura = IMAGEM_CHAO.get_width()
  imagem = IMAGEM_CHAO

  def __init__(self, y):
    self.y = y
    self.x1 = 0
    self.x2 = self.largura  

  def mover(self):
    self.x1 -= self.velocidade
    self.x2 -= self.velocidade

    if self.x1 + self.largura < 0:
      self.x1 = self.x1 + self.largura

    if self.x2 + self.largura < 0:
      self.x2 = self.x2 + self.largura

  def desenhar(self, tela):
    tela.blit(self.imagem, (self.x1, self.y))
    tela.blit(self.imagem, (self.x2, self.y))

def desenhar_tela(tela, passaros, canos, chao, pontos):
  tela.blit(IMAGEM_BACKGROUND, (0, 0))
  for passaro in passaros:
    passaro.desenhar(tela)
  for cano in canos:
    cano.desenhar(tela)

  texto = FONTE_PONTOS.render(f"pontuação: {pontos}", 1, (255, 255, 255))
  tela.blit(texto, (TELA_LARGURA - 10 -  texto.get_width(), 10))
  chao.desenhar(tela)
  pygame.display.update()


def main():
  passaros =  [Passaro( 230, 350)]
  chao = Chao(730)
  canos = [Cano(700)]
  tela =  pygame.display.set_mode((TELA_LARGURA,TELA_ALTURA))
  pontos = 0 
  relogio =  pygame.time.Clock()

  print('main')
  rodando = True
  while rodando:
    relogio.tick(30)
    print('rodando')

    for evento in pygame.event.get():
      if evento.type == pygame.QUIT:
        rodando = False
        pygame.quit()
        quit()
      if evento.type == pygame.KEYDOWN:
        if evento.key == pygame.K_SPACE:
          for passaro in passaros: 
            passaro.pular()

    for passaro in passaros:
      passaro.mover()
    chao.mover()

    adicionar_cano = False
    remover_canos = []
    for cano in canos:
      for i, passaro in enumerate(passaros):
        if cano.colidir( passaro):
          passaros.pop(i)
        if not cano.passou and  passaro.x > cano.x:
          cano.passou = True
          adicionar_cano = True

      cano.mover()
      if cano.x + cano.CANO_TOPO.get_width()< 0 :
        remover_canos.append(cano)
    
    if adicionar_cano:
      pontos += 1
      canos.append(cano(600))

    for canos in remover_canos:
      cano.remove(cano)

    for i, passaro in enumerate(passaros):
      if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0 :
        passaros.pop(i)

    desenhar_tela(tela, passaros, canos, chao, pontos)

main()
