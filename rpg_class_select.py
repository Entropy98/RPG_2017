import pygame, sys
from pygame import *
import random
import math
import rpg_file_def
import rpg_items
import rpg_mechanics
import rpg_animations
import rpg_classes

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))
pygame.display.set_caption('RPG')
pygame.key.set_repeat(10,10)

background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)
FPS=30
fpsClock=pygame.time.Clock()

classes=['warrior','ranger']
class_select_label=font.render('Select a Class',1,(0,0,0))

obstacles=[((-100,100+boundary_width),(-100,map_height+100)),\
	((-100,map_width+100),(-100,100+boundary_width)),\
	(((map_width - boundary_width),map_width+100),(-100,map_height+100)),\
	((-100,map_width+100),((map_height - boundary_width),map_height+100))]
obstacle_locations=[]


def run():
	rpg_mechanics.boss_fight=False
	rpg_mechanics.boss.loot_dropped=False
	rpg_mechanics.defeated_bosses=0
	for i in rpg_mechanics.bosses:
		i.health=i.full_health
	rpg_classes.hero.debuf={'fire':0}
	rpg_classes.hero.room=0
	rpg_classes.hero.helmet=rpg_items.place_holder
	rpg_classes.hero.chest=rpg_items.place_holder
	rpg_classes.hero.pants=rpg_items.place_holder
	rpg_classes.hero.score=0
	rpg_mechanics.double_press_timer+=1
	rpg_classes.hero.inventory_list=[]
	obstacle_locations=[]
	rpg_classes.hero.x=475
	rpg_classes.hero.y=475
	rpg_classes.cookie_man.defeated=False
	rpg_classes.necromancer.defeated=False
	rpg_classes.game_complete=False
	DISPLAYSURF.blit(background,(0,0))
	#pygame.draw.line(DISPLAYSURF,(0,0,0),(500,0),(500,700))
	DISPLAYSURF.blit(class_select_label,(440,100))
	for i in range(len(classes)):
		pygame.draw.rect(DISPLAYSURF,(216,216,216),(325+(200*i),200,150,150))

	if(rpg_mechanics.selectedClass==0):
		DISPLAYSURF.blit(rpg_file_def.menu_select,(325,200))
	else:
		DISPLAYSURF.blit(rpg_file_def.menu_select,(525,200))

	DISPLAYSURF.blit(rpg_file_def.warrior_emblem,(340,215))
	DISPLAYSURF.blit(rpg_file_def.ranger_emblem,(540,215))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
	keys=pygame.key.get_pressed()
	if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
		if(keys[K_SPACE]):
			rpg_classes.hero.addClass(classes[rpg_mechanics.selectedClass])
			if(classes[rpg_mechanics.selectedClass]=='warrior'):
				rpg_classes.hero.name='warrior'
				rpg_classes.hero.addWeapon(rpg_items.sparring_sword)
				rpg_classes.hero.common_loot=rpg_items.common_warrior_items
				rpg_classes.hero.uncommon_loot=rpg_items.uncommon_warrior_items
				rpg_classes.hero.rare_loot=rpg_items.rare_warrior_items
				rpg_classes.hero.mythic_loot=rpg_items.mythic_warrior_items
			elif(classes[rpg_mechanics.selectedClass]=='ranger'):
				rpg_classes.hero.name='ranger'
				rpg_classes.hero.addWeapon(rpg_items.wood_bow)
				rpg_classes.hero.common_loot=rpg_items.common_ranger_items
				rpg_classes.hero.uncommon_loot=rpg_items.uncommon_ranger_items
				rpg_classes.hero.rare_loot=rpg_items.rare_ranger_items
				rpg_classes.hero.mythic_loot=rpg_items.mythic_ranger_items
			rpg_mechanics.boss.loot=rpg_classes.hero.mythic_loot
			rpg_mechanics.class_select=False
		if(keys[K_d]):
			rpg_mechanics.selectedClass+=1
			if(rpg_mechanics.selectedClass>len(classes)-1):
				rpg_mechanics.selectedClass=0
			rpg_mechanics.double_press_timer=0
		if(keys[K_a]):
			rpg_mechanics.selectedClass-=1
			if(rpg_mechanics.selectedClass<0):
				rpg_mechanics.selectedClass=len(classes)-1
			rpg_mechanics.double_press_timer=0

	pygame.display.update()
	fpsClock.tick(FPS)