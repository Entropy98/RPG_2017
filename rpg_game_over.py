import pygame, sys
from pygame import *
import random
import math
import rpg_file_def
import rpg_items
import rpg_mechanics
import rpg_animations
import rpg_classes
import rpg_class_select

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))

background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)

transparentSurface=pygame.Surface((1000,700))
transparentSurface.set_alpha(128)

FPS=30
fpsClock=pygame.time.Clock()

def run1():
	transparentSurface.fill((153,0,0))
	game_over_label=font.render('GAME OVER',1,(255,255,255))
	restart_label=font.render('Press C to Try Again',1,(255,255,255))
	room_number_label=font.render('Room '+str(rpg_classes.hero.room),1,(255,255,255))
	score_label=font.render('Score: '+str(rpg_classes.hero.score),1,(255,255,255))
	rpg_mechanics.double_press_timer+=1
	DISPLAYSURF.blit(background,(0,0))
	if(rpg_mechanics.player_face=='up'):
		DISPLAYSURF.blit(rpg_classes.hero.weapon['sprite'],((rpg_classes.hero.x+rpg_classes.hero.hold_point_x)-rpg_classes.hero.weapon['hold_point_x'],(rpg_classes.hero.y+rpg_classes.hero.hold_point_y)-rpg_classes.hero.weapon['hold_point_y']))
		DISPLAYSURF.blit(rpg_classes.hero.sprite,(rpg_classes.hero.x,rpg_classes.hero.y))
		DISPLAYSURF.blit(rpg_classes.hero.pants['sprite'],((rpg_classes.hero.x+rpg_classes.hero.pants['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.pants['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.chest['sprite'],((rpg_classes.hero.x+rpg_classes.hero.chest['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.chest['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.helmet['sprite'],((rpg_classes.hero.x+rpg_classes.hero.helmet['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.helmet['mount_point_y'])))
	else:		
		DISPLAYSURF.blit(rpg_classes.hero.sprite,(rpg_classes.hero.x,rpg_classes.hero.y))
		DISPLAYSURF.blit(rpg_classes.hero.pants['sprite'],((rpg_classes.hero.x+rpg_classes.hero.pants['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.pants['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.chest['sprite'],((rpg_classes.hero.x+rpg_classes.hero.chest['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.chest['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.helmet['sprite'],((rpg_classes.hero.x+rpg_classes.hero.helmet['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.helmet['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.weapon['sprite'],((rpg_classes.hero.x+rpg_classes.hero.hold_point_x)-rpg_classes.hero.weapon['hold_point_x'],(rpg_classes.hero.y+rpg_classes.hero.hold_point_y)-rpg_classes.hero.weapon['hold_point_y']))
	for i in rpg_mechanics.loot:
		DISPLAYSURF.blit(i[0]['default_sprite'],(i[1],i[2]))

	for i in rpg_mechanics.mobs:
		DISPLAYSURF.blit(i[2],(i[0],i[1]))
		pygame.draw.rect(DISPLAYSURF,(255,255,255),(i[0],i[1]-20,i[7],10))
		pygame.draw.rect(DISPLAYSURF,(255,0,0),(i[0],i[1]-20,(i[7])*(i[5]/float(i[9])),10))
		if(i[4]=='skeleton'):
			DISPLAYSURF.blit(i[16],(i[0]+i[17],i[1]+i[18]))
	if(rpg_mechanics.boss_fight==True):
		if(rpg_mechanics.boss.health>0):
			DISPLAYSURF.blit(rpg_mechanics.boss.sprite,(rpg_mechanics.boss.x,rpg_mechanics.boss.y))

	rpg_mechanics.displayObstacles()

	DISPLAYSURF.blit(transparentSurface,(0,0))
	DISPLAYSURF.blit(room_number_label,(30,30))
	DISPLAYSURF.blit(game_over_label,(440,100))
	DISPLAYSURF.blit(restart_label,(400,600))
	DISPLAYSURF.blit(score_label,(440,200))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
		if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
			if(event.type==KEYDOWN):
				if(event.key==K_c):
					rpg_mechanics.game_over=False
					rpg_mechanics.boss_fight=False
					rpg_mechanics.class_select=True
					rpg_mechanics.double_press_timer=0
					hero=rpg_classes.Player(475,475,rpg_file_def.hero_sprite_r1,47,37,10,40,25)
					rpg_mechanics.mobs=[]
					rpg_mechanics.loot=[]
					rpg_mechanics.active_projectile=[]
					rpg_mechanics.active_mob_projectile=[]

	pygame.display.update()
	fpsClock.tick(FPS)

def run2():
	transparentSurface.fill((0,153,255))
	restart_label=font.render('Press C to Play Again',1,(255,255,0))
	game_complete_label=font.render('YOU WON',1,(255,255,0))
	room_number_label=font.render('Room '+str(rpg_classes.hero.room),1,(255,255,0))
	score_label=font.render('Score: '+str(rpg_classes.hero.score),1,(255,255,0))
	rpg_mechanics.double_press_timer+=1
	DISPLAYSURF.blit(background,(0,0))
	if(rpg_mechanics.player_face=='up'):
		DISPLAYSURF.blit(rpg_classes.hero.weapon['sprite'],((rpg_classes.hero.x+rpg_classes.hero.hold_point_x)-rpg_classes.hero.weapon['hold_point_x'],(rpg_classes.hero.y+rpg_classes.hero.hold_point_y)-rpg_classes.hero.weapon['hold_point_y']))
		DISPLAYSURF.blit(rpg_classes.hero.sprite,(rpg_classes.hero.x,rpg_classes.hero.y))
		DISPLAYSURF.blit(rpg_classes.hero.pants['sprite'],((rpg_classes.hero.x+rpg_classes.hero.pants['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.pants['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.chest['sprite'],((rpg_classes.hero.x+rpg_classes.hero.chest['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.chest['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.helmet['sprite'],((rpg_classes.hero.x+rpg_classes.hero.helmet['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.helmet['mount_point_y'])))
	else:		
		DISPLAYSURF.blit(rpg_classes.hero.sprite,(rpg_classes.hero.x,rpg_classes.hero.y))
		DISPLAYSURF.blit(rpg_classes.hero.pants['sprite'],((rpg_classes.hero.x+rpg_classes.hero.pants['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.pants['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.chest['sprite'],((rpg_classes.hero.x+rpg_classes.hero.chest['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.chest['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.helmet['sprite'],((rpg_classes.hero.x+rpg_classes.hero.helmet['mount_point_x']),(rpg_classes.hero.y+rpg_classes.hero.helmet['mount_point_y'])))
		DISPLAYSURF.blit(rpg_classes.hero.weapon['sprite'],((rpg_classes.hero.x+rpg_classes.hero.hold_point_x)-rpg_classes.hero.weapon['hold_point_x'],(rpg_classes.hero.y+rpg_classes.hero.hold_point_y)-rpg_classes.hero.weapon['hold_point_y']))
	for i in rpg_mechanics.loot:
		DISPLAYSURF.blit(i[0]['default_sprite'],(i[1],i[2]))

	for i in rpg_mechanics.mobs:
		DISPLAYSURF.blit(i[2],(i[0],i[1]))
		pygame.draw.rect(DISPLAYSURF,(255,255,255),(i[0],i[1]-20,i[7],10))
		pygame.draw.rect(DISPLAYSURF,(255,0,0),(i[0],i[1]-20,(i[7])*(i[5]/float(i[9])),10))
		if(i[4]=='skeleton'):
			DISPLAYSURF.blit(i[16],(i[0]+i[17],i[1]+i[18]))
	if(rpg_mechanics.boss_fight==True):
		if(rpg_mechanics.boss.health>0):
			DISPLAYSURF.blit(rpg_mechanics.boss.sprite,(rpg_mechanics.boss.x,rpg_mechanics.boss.y))

	rpg_mechanics.displayObstacles()

	DISPLAYSURF.blit(transparentSurface,(0,0))
	DISPLAYSURF.blit(room_number_label,(30,30))
	DISPLAYSURF.blit(game_complete_label,(440,100))
	DISPLAYSURF.blit(restart_label,(400,600))
	DISPLAYSURF.blit(score_label,(440,200))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
		if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
			if(event.type==KEYDOWN):
				if(event.key==K_c):
					rpg_mechanics.game_complete=False
					rpg_mechanics.boss_fight=False
					rpg_mechanics.class_select=True
					rpg_mechanics.double_press_timer=0
					hero=rpg_classes.Player(475,475,rpg_file_def.hero_sprite_r1,47,37,10,40,25)
					rpg_mechanics.mobs=[]
					rpg_mechanics.loot=[]
					rpg_mechanics.active_projectile=[]
					rpg_mechanics.active_mob_projectile=[]

	pygame.display.update()
	fpsClock.tick(FPS)