import pygame, sys
from pygame import *
import rpg_mechanics
import rpg_controls_menu
import rpg_credits

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))

background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)
press_space_label=font.render('Press [SPACE] to Select',1,(0,0,0))

FPS=30
fpsClock=pygame.time.Clock()

items=['start','controls','credits']

def run():
	rpg_mechanics.double_press_timer+=1
	DISPLAYSURF.blit(background,(0,0))

	while(rpg_mechanics.controls_menu):
		rpg_controls_menu.run()

	while(rpg_mechanics.credits_menu):
		rpg_credits.run()

	if(items[rpg_mechanics.selectedMenuItem]=='start'):
		start_label=font.render('start',1,(0,0,204))
	else:
		start_label=font.render('start',1,(0,0,0))
	if(items[rpg_mechanics.selectedMenuItem]=='controls'):
		controls_label=font.render('controls',1,(0,0,204))
	else:
		controls_label=font.render('controls',1,(0,0,0))
	if(items[rpg_mechanics.selectedMenuItem]=='credits'):
		credits_label=font.render('credits',1,(0,0,204))
	else:
		credits_label=font.render('credits',1,(0,0,0))

	#pygame.draw.line(DISPLAYSURF,(0,0,0),(500,0),(500,700))
	DISPLAYSURF.blit(start_label,(478,250))
	DISPLAYSURF.blit(controls_label,(465,300))
	DISPLAYSURF.blit(credits_label,(469,350))
	DISPLAYSURF.blit(press_space_label,(390,500))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
	keys=pygame.key.get_pressed()
	if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
		if(keys[K_SPACE]):
			if(items[rpg_mechanics.selectedMenuItem]=='start'):
				rpg_mechanics.class_select=True
				rpg_mechanics.start_menu=False
				rpg_mechanics.double_press_timer=0
			elif(items[rpg_mechanics.selectedMenuItem]=='controls'):
				rpg_mechanics.controls_menu=True
				rpg_mechanics.double_press_timer=0
			elif(items[rpg_mechanics.selectedMenuItem]=='credits'):
				rpg_mechanics.credits_menu=True
				rpg_mechanics.double_press_timer=0
		if(keys[K_s]):
			rpg_mechanics.selectedMenuItem+=1
			if(rpg_mechanics.selectedMenuItem>len(items)-1):
				rpg_mechanics.selectedMenuItem=0
			rpg_mechanics.double_press_timer=0
		if(keys[K_w]):
			rpg_mechanics.selectedMenuItem-=1
			if(rpg_mechanics.selectedMenuItem<0):
				rpg_mechanics.selectedMenuItem=len(items)-1
			rpg_mechanics.double_press_timer=0

	pygame.display.update()
	fpsClock.tick(FPS)