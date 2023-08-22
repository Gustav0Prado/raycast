#!/usr/bin/python3

import pygame, math
from pygame.locals import *

WIDTH  = 1280
HEIGHT = 720
RED = (250, 0, 0)
SCALE = 1
OLDSCALE = SCALE
PLAYER_SIZE = 25 * SCALE / 1.1

DR = 0.0174533 # um grau em radianos

mapOffset = 0

def dist(x1, y1, x2, y2, ang):
   return math.sqrt( ((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)) )

def drawRays2D():
   ######################### Checa horizontal ###############################
   ra = player.a - DR
   if ra < 0:           ra += 2*math.pi
   if ra > 2*math.pi:   ra -= 2*math.pi
   px = player.rect.centerx
   py = player.rect.centery

   for r in range(60):
      # Checa linhas horizontais
      distH=1000000; hx = px; hy = py
      dof = 0
      atan = -1/math.tan(ra)

      # Raio para cima
      if ra > math.pi and ra < 2*math.pi:
         ry = (int(py >> 6)<<6)-0.0001
         rx = (py - ry) * atan + px
         yo = -64; xo = -yo*atan

      # Raio para baixo
      if ra < math.pi and ra > 0:
         ry = (int(py >> 6)<<6)+64
         rx = (py - ry) * atan + px
         yo = 64; xo = -yo*atan

      # Raio reto para esquerda ou direita
      if (ra == 0 or ra == 2*math.pi):
         rx = px; ry = py; dof = 8
      
      while (dof < 8):
         mx = int(rx) >> 6; my = int(ry) >> 6
         mp = my * mapX + mx

         # bateu na parede
         if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
            hx = rx; hy = ry; distH=dist(px, py, hx, hy, ra); dof = 8
         else:
            rx += xo; ry += yo; dof += 1

      ######################### Checa vertical ###############################
      dof = 0
      ntan = -math.tan(ra)
      distV=1000000; vx = px; vy = py

      # Raio para esquerda
      if ra > math.pi/2 and ra < 3*math.pi/2:
         rx = (int(px >> 6)<<6)-0.0001
         ry = (px - rx) * ntan + py
         xo = -64; yo = -xo*ntan

      # Raio para direita
      if ra < math.pi/2 or ra > 3*math.pi/2:
         rx = (int(px >> 6)<<6)+64
         ry = (px - rx) * ntan + py
         xo = 64; yo = -xo*ntan

      # Raio reto para cima ou baixo
      if (ra == math.pi/2 or ra == 3*math.pi/2):
         rx = px; ry = py; dof = 8
      
      while (dof < 8):
         mx = int(rx) >> 6; my = int(ry) >> 6
         mp = my * mapX + mx

         # bateu na parede
         if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
            vx = rx; vy = ry; distV=dist(px, py, vx, vy, ra); dof = 8
         else:
            rx += xo; ry += yo; dof += 1

      # Desenha rays
      if distV < distH: rx = vx; ry = vy
      if distV > distH: rx = hx; ry = hy
      
      pygame.draw.line(screen, (22, 255, 53), (px, py), (rx, ry), 2)

      # Aumenta angulo do proximo ray
      ra += DR
      if ra < 0:           ra += 2*math.pi
      if ra > 2*math.pi:   ra -= 2*math.pi

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
      self.a  = 7*math.pi/4
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
   # cx = player.rect.centerx
   # cy = player.rect.centery
   # pygame.draw.line(
   #    screen, (RED),
   #    (cx, cy),
   #    (cx + player.dx * PLAYER_SIZE / 2, cy + player.dy * PLAYER_SIZE / 2),
   #    2
   # )

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
      drawRays2D()

   # Flipa display e espera relogio
   pygame.display.flip()
   clock.tick(30)
         