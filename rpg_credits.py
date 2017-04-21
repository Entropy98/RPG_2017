import pygame, sys
from pygame import *
import rpg_mechanics

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))

background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)

creators_label=font.render('Game Creators:',1,(0,0,0))
harper_label=font.render('Harper Weigle',1,(0,0,0))
alex_label=font.render('Alex Karlson',1,(0,0,0))
testers_label=font.render('Alpha Testers:',1,(0,0,0))
jack_label=font.render('Jack Brown',1,(0,0,0))
supervisor_label=font.render('Supervisors:',1,(0,0,0))
khuds_label=font.render('Katharine Hudson',1,(0,0,0))

press_space_label=font.render('Press [SPACE] to Go Back',1,(0,0,0))

FPS=30
fpsClock=pygame.time.Clock()

text_gap=35
creators_y=100
testers_y=375
supervisor_y=250

def run():
	rpg_mechanics.double_press_timer+=1
	DISPLAYSURF.blit(background,(0,0))

	#pygame.draw.line(DISPLAYSURF,(0,0,0),(500,0),(500,700))

	DISPLAYSURF.blit(creators_label,(435,creators_y))
	DISPLAYSURF.blit(harper_label,(438,creators_y+text_gap*1))
	DISPLAYSURF.blit(alex_label,(442,creators_y+text_gap*2))

	DISPLAYSURF.blit(testers_label,(435,testers_y))
	DISPLAYSURF.blit(jack_label,(448,testers_y+text_gap*1))

	DISPLAYSURF.blit(supervisor_label,(440,supervisor_y))
	DISPLAYSURF.blit(khuds_label,(417,supervisor_y+text_gap*1))

	DISPLAYSURF.blit(press_space_label,(390,630))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
	keys=pygame.key.get_pressed()
	if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
		if(keys[K_SPACE]):
			rpg_mechanics.credits_menu=False
			rpg_mechanics.double_press_timer=0

	pygame.display.update()
	fpsClock.tick(FPS)