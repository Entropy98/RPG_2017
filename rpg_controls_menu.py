import pygame, sys
from pygame import *
import rpg_mechanics

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))

background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)

menu_controls_label=font.render('Menu Controls:',1,(0,0,0))
select_label=font.render('Select => [SPACE]',1,(0,0,0))
game_controls_label=font.render('Game Controls:',1,(0,0,0))
move_up_label=font.render('Move Up => [W]',1,(0,0,0))
move_down_label=font.render('Move Down => [S]',1,(0,0,0))
move_left_label=font.render('Move Left => [D]',1,(0,0,0))
move_right_label=font.render('Move Right => [A]',1,(0,0,0))
inventory_label=font.render('Open Inventory => [I]',1,(0,0,0))
enter_room_label=font.render('Enter Room => [R]',1,(0,0,0))
pick_up_label=font.render('Equip => [E]',1,(0,0,0))
attack_up_label=font.render('Attack Up => [UP]',1,(0,0,0))
attack_down_label=font.render('Attack Down => [DOWN]',1,(0,0,0))
attack_left_label=font.render('Attack Left => [LEFT]',1,(0,0,0))
attack_right_label=font.render('Attack Right => [RIGHT]',1,(0,0,0))
inventory_controls_label=font.render('Inventory Controls:',1,(0,0,0))
drop_label=font.render('Drop => [R]',1,(0,0,0))
press_space_label=font.render('Press [SPACE] to Go Back',1,(0,0,0))

FPS=30
fpsClock=pygame.time.Clock()

game_controls_y=75
menu_controls_y=75
inventory_control_y=350
col1=250
col2=600
text_gap=35

def run():
	rpg_mechanics.double_press_timer+=1
	DISPLAYSURF.blit(background,(0,0))

	DISPLAYSURF.blit(menu_controls_label,(col1,menu_controls_y))
	DISPLAYSURF.blit(select_label,(col1,menu_controls_y+text_gap*1))
	DISPLAYSURF.blit(move_up_label,(col1,menu_controls_y+text_gap*2))
	DISPLAYSURF.blit(move_down_label,(col1,menu_controls_y+text_gap*3))
	DISPLAYSURF.blit(move_right_label,(col1,menu_controls_y+text_gap*4))
	DISPLAYSURF.blit(move_left_label,(col1,menu_controls_y+text_gap*5))

	DISPLAYSURF.blit(inventory_controls_label,(col1,inventory_control_y))
	DISPLAYSURF.blit(pick_up_label,(col1,inventory_control_y+text_gap*1))
	DISPLAYSURF.blit(drop_label,(col1,inventory_control_y+text_gap*2))
	DISPLAYSURF.blit(move_up_label,(col1,inventory_control_y+text_gap*3))
	DISPLAYSURF.blit(move_down_label,(col1,inventory_control_y+text_gap*4))
	DISPLAYSURF.blit(move_right_label,(col1,inventory_control_y+text_gap*5))
	DISPLAYSURF.blit(move_left_label,(col1,inventory_control_y+text_gap*6))

	DISPLAYSURF.blit(game_controls_label,(col2,game_controls_y))
	DISPLAYSURF.blit(inventory_label,(col2,game_controls_y+text_gap*1))
	DISPLAYSURF.blit(enter_room_label,(col2,game_controls_y+text_gap*2))
	DISPLAYSURF.blit(pick_up_label,(col2,game_controls_y+text_gap*3))
	DISPLAYSURF.blit(move_up_label,(col2,game_controls_y+text_gap*4))
	DISPLAYSURF.blit(move_down_label,(col2,game_controls_y+text_gap*5))
	DISPLAYSURF.blit(move_right_label,(col2,game_controls_y+text_gap*6))
	DISPLAYSURF.blit(move_left_label,(col2,game_controls_y+text_gap*7))
	DISPLAYSURF.blit(attack_up_label,(col2,game_controls_y+text_gap*8))
	DISPLAYSURF.blit(attack_down_label,(col2,game_controls_y+text_gap*9))
	DISPLAYSURF.blit(attack_right_label,(col2,game_controls_y+text_gap*10))
	DISPLAYSURF.blit(attack_left_label,(col2,game_controls_y+text_gap*11))

	DISPLAYSURF.blit(press_space_label,(390,630))

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
	keys=pygame.key.get_pressed()
	if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
		if(keys[K_SPACE]):
			rpg_mechanics.controls_menu=False
			rpg_mechanics.double_press_timer=0

	pygame.display.update()
	fpsClock.tick(FPS)