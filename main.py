#!/usr/bin/python3

import pygame, math, asyncio
from pygame.locals import *

WIDTH  = 1024
HEIGHT = 512
RED = (250, 0, 0)
DARKRED = (150, 0, 0)
SCALE = 1
OLDSCALE = SCALE
PLAYER_SIZE = 8

DR = 0.0174533 # um grau em radianos
def dist(x1, y1, x2, y2):
   return math.sqrt( ((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)) )

def drawRays2D():
   ra = player.a + math.radians(30)
   if ra < 0:           ra += 2*math.pi
   if ra > 2*math.pi:   ra -= 2*math.pi
   px = player.rect.centerx
   py = player.rect.centery

   for r in range(60):
      ######################### Checa vertical ###############################
      dof = 0; distV=1000000
      ntan = math.tan(ra)
      
      # Raio para esquerda
      if math.cos(ra) > 0.001:
         rx = (int(px >> 6)<<6)+64
         ry = (px - rx) * ntan + py
         xo = 64; yo = -xo*ntan

      # Raio para direita
      elif math.cos(ra) < -0.001:
         rx = (int(px >> 6)<<6)-0.0001
         ry = (px - rx) * ntan + py
         xo = -64; yo = -xo*ntan

      # Raio reto para cima ou baixo
      else: rx = px; ry = py; dof = 8
      
      while (dof < 8):
         mx = int(rx) >> 6; my = int(ry) >> 6
         mp = my * mapX + mx

         # bateu na parede
         if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
            distV=math.cos(ra)*(rx-px)-math.sin(ra)*(ry-py); dof = 8
         else: rx += xo; ry += yo; dof += 1
      vx=rx; vy=ry

   ######################### Checa horizontal ###############################
      # Checa linhas horizontais
      distH=1000000; dof = 0
      atan = 1/ntan

      # Raio para cima
      if math.sin(ra) > 0.001:
         ry = (int(py >> 6)<<6)-0.0001
         rx = (py - ry) * atan + px
         yo = -64; xo = -yo*atan

      # Raio para baixo
      elif math.sin(ra) < -0.001:
         ry = (int(py >> 6)<<6)+64
         rx = (py - ry) * atan + px
         yo = 64; xo = -yo*atan

      # Raio reto para esquerda ou direita
      else: rx = px; ry = py; dof = 8
      
      while (dof < 8):
         mx = int(rx) >> 6; my = int(ry) >> 6
         mp = my * mapX + mx

         # bateu na parede
         if(mp > 0 and mp < mapX*mapY and map[mp] == 1):
            distH=math.cos(ra)*(rx-px)-math.sin(ra)*(ry-py); dof = 8
         else: rx += xo; ry += yo; dof += 1

      # Desenha rays
      color = DARKRED
      if distV < distH: rx = vx; ry = vy; distH=distV; color = RED
      
      if mapOn: pygame.draw.line(screen, (22, 255, 53), (px, py), (rx, ry), 2)

      ######################### Desenha 3D ###############################
      # Fix fisheye
      ca = player.a - ra
      if ca < 0:           ca += 2*math.pi
      if ca > 2*math.pi:   ca -= 2*math.pi
      distH*=math.cos(ca)

      lineH = (mapS*320)/distH
      if lineH > 320: lineH = 320

      lineO=160-lineH/2

      pygame.draw.line(screen, color, (8*r+530,lineO), (8*r+530,lineH+lineO), 8)

      # Aumenta angulo do proximo ray
      ra -= DR;
      if ra < 0:           ra += 2*math.pi
      if ra > 2*math.pi:   ra -= 2*math.pi

   #Desenha linha com a direcao do player
   cx = player.rect.centerx; cy = player.rect.centery
   if mapOn: 
      pygame.draw.line(
         screen, (RED),
         (cx, cy),
         (cx + player.dx * 20, cy - player.dy * 20),
         2
      )

def xToTile(x, y, s):
   # Calcula indice da tile basedo no x e y do player e em uma escala
   mapScaling = 64 * s
   return ((x - mapScaling/2)/(mapScaling), (y - mapScaling/2)/(mapScaling))

def tileToX(x, y):
   # Calcula posicao x e y baseado no indice da tile
   xo = x * mapS; yo = y * mapS
   return (xo + mapS/2, yo + mapS/2)

class Player():
   def __init__(self):
      super(Player, self).__init__()

      # Icone do player
      self.surf = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
      self.surf.fill(RED)
      self.rect = self.surf.get_rect()
      self.rect.center = tileToX(mapX-2, mapY-2)

      # Direcao inicial
      self.a  = math.pi/2
      self.dx = math.cos(self.a); self.dy = math.sin(self.a)

   def update(self, pressed_keys):
      # Se move de acordo com as teclas
      if pressed_keys[K_w]:
         self.rect.move_ip(player.dx*5, -player.dy*5)

      if pressed_keys[K_s]:
         self.rect.move_ip(-player.dx*5, player.dy*5)

      if pressed_keys[K_a]:
         self.a += 0.1
         if (self.a < 0.1):       self.a += 2 * math.pi
         if (self.a > 2*math.pi): self.a -= 2 * math.pi
         self.dx = math.cos(self.a); self.dy = math.sin(self.a)
                           
      if pressed_keys[K_d]:
         self.a -= 0.1
         if (self.a < 0.1):       self.a += 2 * math.pi
         if (self.a > 2*math.pi): self.a -= 2 * math.pi
         self.dx = math.cos(self.a); self.dy = math.sin(self.a)

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
         xo = x * mapS; yo = y * mapS

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



# Opcoes booleanas
done = False
mapOn = True
rescale = False

# Inicia jogo e instancia estruturas
pygame.init()
player = Player()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

async def main():
   global done, mapOn

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
         screen.blit(player.surf, player.rect)
      drawRays2D()

      # Flipa display e espera relogio
      pygame.display.flip()
      clock.tick(30)
      await asyncio.sleep(0)
   
asyncio.run(main())