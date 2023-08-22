#!/usr/bin/python3

import pygame, math
from pygame.locals import *

WIDTH  = 1280
HEIGHT = 720
RED = (250, 0, 0)
SCALE = 1
OLDSCALE = SCALE
PLAYER_SIZE = 25 * SCALE / 1.1
mapOffset = 0

def drawRays3D():
   ra = player.a
   for r in range(1):
      # Checa linhas horizontais
      dof = 0
      atan = -1/math.tan(ra)

      # Raio para cima
      if ra > math.pi and ra < 2*math.pi:
         ry = (int(player.rect.centery >> 6)<<6)-0.0001
         rx = (player.rect.centery - ry) * atan + player.rect.centerx
         yo = -64; xo = -yo*atan

      # Raio para baixo
      if ra < math.pi and ra > 0:
         ry = (int(player.rect.centery >> 6)<<6)+64
         rx = (player.rect.centery - ry) * atan + player.rect.centerx
         yo = 64; xo = -yo*atan

      # Raio reto para esquerda ou direita
      if (ra == 0 or ra == 2*math.pi):
         rx = player.rect.centerx; ry = player.rect.centery; dof = 8
      
      while (dof < 8):
         mx = int(rx) >> 6; my = int(ry) >> 6
         mp = my * mapX + mx

         pygame.draw.line(screen, (10, 206, 27), (player.rect.centerx, player.rect.centery), (rx, ry), 1)
         pygame.display.flip()

         # bateu na parede
         if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
            dof = 8
         else:
            rx += xo; ry += yo; dof += 1

      # Desenha rays
      #pygame.draw.line(screen, (10, 206, 27), (player.rect.centerx, player.rect.centery), (rx, ry), 1)

def xToTile(x, y, s):
   # Calcula indice da tile basedo no x e y do player e em uma escala
   mapScaling = 64 * s
   return ((x - mapScaling/2)/(mapScaling + mapOffset), (y - mapScaling/2)/(mapScaling + mapOffset))

def tileToX(x, y):
   # Calcula posicao x e y baseado no indice da tile
   xo = x * mapS + mapOffset; yo = y * mapS + mapOffset
   return (xo + mapS/2, yo + mapS/2)

class Player():
   def __init__(self):
      super(Player, self).__init__()

      # Icone do player
      self.surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
      self.surf.fill(RED)
      self.rect = self.surf.get_rect()
      # self.rect.center = tileToX(mapX-2, mapY-2)
      self.rect.center = tileToX(2, 6)

      # Direcao inicial
      self.a  = 2*math.pi
      self.dx = math.cos(self.a) * 5; self.dy = math.sin(self.a) * 5

   def update(self, pressed_keys):
      # Se move de acordo com as teclas
      if pressed_keys[K_w]:
         self.rect.move_ip(player.dx, player.dy)

      if pressed_keys[K_s]:
         self.rect.move_ip(-player.dx, -player.dy)

      if pressed_keys[K_a]:
         self.a -= 0.1
         if (self.a < 0.1):           self.a += 2 * math.pi
         if (self.a > 2*math.pi): self.a -= 2 * math.pi
         self.dx = math.cos(self.a) * 5; self.dy = math.sin(self.a) * 5
                           
      if pressed_keys[K_d]:
         self.a += 0.1
         if (self.a < 0.1):           self.a += 2 * math.pi
         if (self.a > 2*math.pi): self.a -= 2 * math.pi
         self.dx = math.cos(self.a) * 5; self.dy = math.sin(self.a) * 5

      # Mantem player na tela
      if self.rect.left < 0:
         self.rect.left = 0
      if self.rect.right > WIDTH:
         self.rect.right = WIDTH
      if self.rect.top <= 0:
         self.rect.top = 0
      if self.rect.bottom >= HEIGHT:
         self.rect.bottom = HEIGHT

mapX = 8; mapY = 8; mapS = 64 * SCALE;
map = [
   1, 1, 1, 1, 1, 1, 1, 1,
   1, 0, 1, 0, 0, 0, 0, 1,
   1, 0, 1, 0, 0, 0, 0, 1,
   1, 0, 1, 0, 0, 0, 0, 1,
   1, 0, 0, 0, 0, 0, 0, 1,
   1, 0, 0, 1, 1, 1, 0, 1,
   1, 0, 0, 0, 0, 1, 0, 1,
   1, 1, 1, 1, 1, 1, 1, 1
]

def drawMap2D():
   for y in range(mapY):
      for x in range(mapX):
         if(map[y*mapX+x] == 1):
            color = (255, 255, 255)
         else:
            color = (0, 0, 0)
            
         # Offset do mapa em relacao ao canto sup esquerdo
         xo = x * mapS + mapOffset; yo = y * mapS + mapOffset

         # Desenha parede no minimapa
         wallSurf = pygame.Surface((mapS, mapS))
         wallSurf.fill(color)
         screen.blit(wallSurf, (xo, yo))

         # Linhas para demarcar tiles
         for i in range(4):
            pygame.draw.line( screen, ((138, 138, 138)), (xo, yo), (xo, yo + mapS), 1)
            pygame.draw.line( screen, ((138, 138, 138)), (xo, yo), (xo + mapS, yo), 1)
            pygame.draw.line( screen, ((138, 138, 138)), (xo, yo + mapS), (xo + mapS, yo + mapS), 1)
            pygame.draw.line( screen, ((138, 138, 138)), (xo + mapS, yo), (xo + mapS, yo + mapS), 1)

   # Desenha linha com a direcao do player
   cx = player.rect.centerx
   cy = player.rect.centery
   pygame.draw.line(
      screen, (RED),
      (cx, cy),
      (cx + player.dx * PLAYER_SIZE / 2, cy + player.dy * PLAYER_SIZE / 2),
      2
   )

# Opcoes booleanas
done = False
mapOn = True
rescale = False


# Inicia jogo e instancia estruturas
pygame.init()
player = Player()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

while not done:
   for event in pygame.event.get():
      if event.type == KEYDOWN:
         if event.key == K_ESCAPE:
            done = True
         if event.key == K_m:
            mapOn = not mapOn

         # Aumenta ou diminui tamanho do minimapa
         if event.key == pygame.K_KP_PLUS:
            if SCALE < 1:
               OLDSCALE = SCALE
               SCALE *= 2
               mapS = 64 * SCALE
               PLAYER_SIZE = 25 * SCALE / 1.1
               rescale = True

         if event.key == pygame.K_KP_MINUS:
            if SCALE > 0.25:
               OLDSCALE = SCALE
               SCALE /= 2
               mapS = 64 * SCALE
               PLAYER_SIZE = 25 * SCALE / 1.1
               rescale = True
      
      elif event.type == QUIT:
         done = True

   
   # Atualiza player com base nas teclas apertadas
   pressed_keys = pygame.key.get_pressed()
   player.update(pressed_keys)

   # Desenha fundo
   screen.fill((105, 105, 105))
   if mapOn:
      drawMap2D()

      # Reescala player recolocando ele na tile onde estava, mas com x e y escalados
      if rescale:
         oldCenter = xToTile(player.rect.centerx, player.rect.centery, OLDSCALE)

         player.surf = pygame.transform.scale(player.surf, (PLAYER_SIZE, PLAYER_SIZE))
         player.rect = player.surf.get_rect()
         player.rect.center = tileToX(oldCenter[0], oldCenter[1])
         
         rescale = False
      screen.blit(player.surf, player.rect)
      pygame.display.flip()
      drawRays3D()

   # Flipa display e espera relogio
   #1pygame.display.flip()
   clock.tick(30)
         