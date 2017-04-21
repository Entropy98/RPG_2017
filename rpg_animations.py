import rpg_file_def
import rpg_classes
import rpg_items
import rpg_mechanics
import pygame, sys
from pygame import *

pygame.init()
map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))
background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)
FPS=30
fpsClock=pygame.time.Clock()

def animateSkeletonMovement(animationState,direction):
	sprite=None
	hold_point_x=None
	weapon_sprite=None
	if(direction=='right'):
		hold_point_x=20
		weapon_sprite=rpg_file_def.wood_bow_sprite_r
		if(animationState==0):
			sprite=rpg_file_def.skeleton_sprite_r1
			animationState+=1
		else:
			sprite=rpg_file_def.skeleton_sprite_r2
			animationState-=1
	elif(direction=='left'):
		hold_point_x=2
		weapon_sprite=rpg_file_def.wood_bow_sprite_l
		if(animationState==0):
			sprite=rpg_file_def.skeleton_sprite_l1
			animationState+=1
		else:
			sprite=rpg_file_def.skeleton_sprite_l2
			animationState-=1
	return sprite,hold_point_x,animationState,weapon_sprite

def animateZombieMovement(animationState,direction):
	sprite=None
	if(direction=='right'):
		if(animationState==0):
			sprite=rpg_file_def.zombie_sprite_r1
			animationState+=1
		else:
			sprite=rpg_file_def.zombie_sprite_r2
			animationState-=1
	elif(direction=='left'):
		if(animationState==0):
			sprite=rpg_file_def.zombie_sprite_l1
			animationState+=1
		else:
			sprite=rpg_file_def.zombie_sprite_l2
			animationState-=1
	return sprite,animationState

def animateFireElementalMovement(animationState,direction,attack_state):
	sprite=None
	if(attack_state=='attack'):
		if(direction=='right'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_attack_r1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_attack_r2
				animationState-=1
		elif(direction=='left'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_attack_l1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_attack_l2
				animationState-=1
		elif(direction=='up'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_attack_u1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_attack_u2
				animationState-=1
		elif(direction=='down'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_attack_d1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_attack_d2
				animationState-=1
		return sprite,animationState
	elif(attack_state=='walk'):
		if(direction=='right'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_r1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_r2
				animationState-=1
		elif(direction=='left'):
			if(animationState==0):
				sprite=rpg_file_def.fire_elemental_sprite_l1
				animationState+=1
			else:
				sprite=rpg_file_def.fire_elemental_sprite_l2
				animationState-=1
		return sprite,animationState

def animateWeapon():
	if(rpg_classes.hero.animate_weapon_state==0):
		rpg_items.fire_sword['sprite']=rpg_file_def.fire_sword_sprite
		rpg_items.fire_sword['default_sprite']=rpg_file_def.fire_sword_sprite
		rpg_classes.hero.animate_weapon_state+=1
	else:
		rpg_items.fire_sword['sprite']=rpg_file_def.fire_sword_sprite_2
		rpg_items.fire_sword['default_sprite']=rpg_file_def.fire_sword_sprite_2
		rpg_classes.hero.animate_weapon_state-=1

animationState=0

def animateMovement(direction):
	global animationState
	if(direction=='right'):
		rpg_classes.hero.hold_point_x=40
		rpg_classes.hero.hold_point_y=25
		rpg_items.wood_axe['sprite']=rpg_file_def.wood_axe_sprite_r
		rpg_items.wood_axe['hold_point_x']=15
		rpg_items.wood_bow['sprite']=rpg_file_def.wood_bow_sprite_r
		rpg_items.wood_bow['hold_point_x']=20
		rpg_items.wood_bow['hold_point_y']=25
		rpg_items.glock['sprite']=rpg_file_def.glock_sprite_r
		rpg_items.glock['hold_point_x']=9
		rpg_items.glock['hold_point_y']=7
		rpg_items.crossbow['sprite'] = rpg_file_def.crossbow_sprite_r
		rpg_items.crossbow['hold_point_x'] = 8
		rpg_items.crossbow['hold_point_y'] = 7
		rpg_items.fire_bow['sprite'] = rpg_file_def.fire_bow_sprite_r1
		rpg_items.fire_bow['hold_point_x'] = 20
		rpg_items.fire_bow['hold_point_y'] = 25
		rpg_items.iron_bow['sprite'] = rpg_file_def.iron_bow_sprite_r
		rpg_items.iron_bow['hold_point_x'] = 20
		rpg_items.iron_bow['hold_point_y'] = 25
		rpg_items.platnium_bow['sprite'] = rpg_file_def.platnium_bow_sprite_r
		rpg_items.platnium_bow['hold_point_x'] = 20
		rpg_items.platnium_bow['hold_point_y'] = 25
		rpg_items.iron_helmet['sprite']=rpg_file_def.iron_helmet_sprite_r
		rpg_items.iron_helmet['mount_point_x']=12
		rpg_items.steel_helmet['sprite']=rpg_file_def.steel_helmet_sprite_r
		rpg_items.steel_helmet['mount_point_x']=12
		rpg_items.platinum_helmet['sprite']=rpg_file_def.platinum_helmet_sprite_r
		rpg_items.platinum_helmet['mount_point_x']=12
		rpg_items.leather_cap['sprite']=rpg_file_def.leather_cap_sprite_r
		rpg_items.leather_cap['mount_point_x']=12
		rpg_items.ragged_cloak['mount_point_x']=3
		rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_r
		rpg_items.iron_chestplate['mount_point_x']=6
		rpg_items.iron_chestplate['mount_point_y']=12
		rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_r
		rpg_items.platinum_chestplate['mount_point_x']=6
		rpg_items.platinum_chestplate['mount_point_y']=12
		rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_r
		rpg_items.steel_chestplate['mount_point_x']=6
		rpg_items.steel_chestplate['mount_point_y']=12
		rpg_items.fire_sword['hold_point_x']=15
		rpg_items.fire_sword['hold_point_y']=43
		rpg_items.iron_greeves['mount_point_y']=25
		rpg_items.steel_greeves['mount_point_y']=25
		rpg_items.platinum_greeves['mount_point_y']=25
		rpg_items.headband['sprite'] = rpg_file_def.headband_sprite_r
		rpg_items.headband['mount_point_x'] = 1
		if(animationState==0):
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_r1
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_r1
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_r1
			rpg_items.iron_greeves['mount_point_x']=4
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_r1
			rpg_items.steel_greeves['mount_point_x']=4
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_r1
			rpg_items.platinum_greeves['mount_point_x']=4
			animationState+=1
		else:
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_r2
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_r2
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_r2
			rpg_items.iron_greeves['mount_point_x']=10
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_r2
			rpg_items.steel_greeves['mount_point_x']=10
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_r2
			rpg_items.platinum_greeves['mount_point_x']=10
			animationState-=1
	elif(direction=='left'):
		rpg_classes.hero.hold_point_x=8
		rpg_classes.hero.hold_point_y=25
		rpg_items.wood_axe['sprite']=rpg_file_def.wood_axe_sprite_l
		rpg_items.wood_axe['hold_point_x']=20
		rpg_items.wood_bow['sprite']=rpg_file_def.wood_bow_sprite_l
		rpg_items.wood_bow['hold_point_x']=5
		rpg_items.wood_bow['hold_point_y']=25
		rpg_items.glock['sprite']=rpg_file_def.glock_sprite_l
		rpg_items.glock['hold_point_x']=16
		rpg_items.glock['hold_point_y']=7
		rpg_items.crossbow['sprite']=rpg_file_def.crossbow_sprite_l
		rpg_items.crossbow['hold_point_x'] = 19
		rpg_items.crossbow['hold_point_y'] = 7
		rpg_items.fire_bow['sprite']=rpg_file_def.fire_bow_sprite_l1
		rpg_items.fire_bow['hold_point_x'] = 5
		rpg_items.fire_bow['hold_point_y'] = 25
		rpg_items.iron_bow['sprite'] = rpg_file_def.iron_bow_sprite_l
		rpg_items.iron_bow['hold_point_x'] = 5
		rpg_items.iron_bow['hold_point_y'] = 25
		rpg_items.platnium_bow['sprite'] = rpg_file_def.platnium_bow_sprite_l
		rpg_items.platnium_bow['hold_point_x'] = 5
		rpg_items.platnium_bow['hold_point_y'] = 25
		rpg_items.iron_helmet['sprite']=rpg_file_def.iron_helmet_sprite_l
		rpg_items.iron_helmet['mount_point_x']=11
		rpg_items.platinum_helmet['sprite']=rpg_file_def.platinum_helmet_sprite_l
		rpg_items.platinum_helmet['mount_point_x']=11
		rpg_items.steel_helmet['sprite']=rpg_file_def.steel_helmet_sprite_l
		rpg_items.steel_helmet['mount_point_x']=11
		rpg_items.leather_cap['sprite']=rpg_file_def.leather_cap_sprite_l
		rpg_items.leather_cap['mount_point_x']=11
		rpg_items.ragged_cloak['mount_point_x']=5
		rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_l
		rpg_items.iron_chestplate['mount_point_x']=7
		rpg_items.iron_chestplate['mount_point_y']=12
		rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_l
		rpg_items.platinum_chestplate['mount_point_x']=7
		rpg_items.platinum_chestplate['mount_point_y']=12
		rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_l
		rpg_items.steel_chestplate['mount_point_x']=7
		rpg_items.steel_chestplate['mount_point_y']=12
		rpg_items.fire_sword['hold_point_x']=13
		rpg_items.fire_sword['hold_point_y']=43
		rpg_items.iron_greeves['mount_point_y']=25
		rpg_items.steel_greeves['mount_point_y']=25
		rpg_items.platinum_greeves['mount_point_y']=25
		rpg_items.headband['sprite'] = rpg_file_def.headband_sprite_l
		if(animationState==0):
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_l1
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_l1
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_l1
			rpg_items.iron_greeves['mount_point_x']=7
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_l1
			rpg_items.steel_greeves['mount_point_x']=7
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_l1
			rpg_items.platinum_greeves['mount_point_x']=7
			animationState+=1
		else:
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_l2
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_l2
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_l2
			rpg_items.iron_greeves['mount_point_x']=8
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_l2
			rpg_items.steel_greeves['mount_point_x']=8
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_l2
			rpg_items.platinum_greeves['mount_point_x']=9
			animationState-=1
	elif(direction=='up'):
		rpg_classes.hero.hold_point_x=18
		rpg_classes.hero.hold_point_y=20
		rpg_items.iron_helmet['sprite']=rpg_file_def.iron_helmet_sprite_u
		rpg_items.iron_helmet['mount_point_x']=6
		rpg_items.steel_helmet['sprite']=rpg_file_def.steel_helmet_sprite_u
		rpg_items.steel_helmet['mount_point_x']=5
		rpg_items.platinum_helmet['sprite']=rpg_file_def.platinum_helmet_sprite_u
		rpg_items.platinum_helmet['mount_point_x']=5
		rpg_items.leather_cap['sprite']=rpg_file_def.leather_cap_sprite_u
		rpg_items.leather_cap['mount_point_x']=5
		rpg_items.wood_axe['sprite']=rpg_file_def.wood_axe_sprite_u
		rpg_items.wood_axe['hold_point_x']=7
		rpg_items.wood_bow['sprite']=rpg_file_def.wood_bow_sprite_u
		rpg_items.wood_bow['hold_point_x']=7
		rpg_items.wood_bow['hold_point_y']=15
		rpg_items.fire_sword['hold_point_x']=13
		rpg_items.iron_greeves['mount_point_y']=27
		rpg_items.steel_greeves['mount_point_y']=27
		rpg_items.platinum_greeves['mount_point_y']=27
		rpg_items.glock['sprite']=rpg_file_def.glock_sprite_v
		rpg_items.glock['hold_point_x']=0
		rpg_items.glock['hold_point_y']=2
		rpg_items.crossbow['sprite'] = rpg_file_def.crossbow_sprite_u
		rpg_items.crossbow['hold_point_x']=8
		rpg_items.crossbow['hold_point_y']=16
		rpg_items.fire_bow['sprite']=rpg_file_def.fire_bow_sprite_u1 
		rpg_items.fire_bow['hold_point_x']=7
		rpg_items.fire_bow['hold_point_y']=23
		rpg_items.iron_bow['sprite'] = rpg_file_def.iron_bow_sprite_u
		rpg_items.iron_bow['hold_point_x'] = 7
		rpg_items.iron_bow['hold_point_y'] = 23
		rpg_items.platnium_bow['sprite'] = rpg_file_def.platnium_bow_sprite_u
		rpg_items.platnium_bow['hold_point_x'] = 7
		rpg_items.platnium_bow['hold_point_y'] = 23
		rpg_items.headband['sprite'] = rpg_file_def.headband_sprite_u
		rpg_items.headband['mount_point_x'] = 1
		if(animationState==0):
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_u1
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_u1
			rpg_items.ragged_cloak['mount_point_x']=0
			rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_u1
			rpg_items.iron_chestplate['mount_point_x']=0
			rpg_items.iron_chestplate['mount_point_y']=14
			rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_u1
			rpg_items.steel_chestplate['mount_point_x']=0
			rpg_items.steel_chestplate['mount_point_y']=14
			rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_u1
			rpg_items.platinum_chestplate['mount_point_x']=0
			rpg_items.platinum_chestplate['mount_point_y']=14
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_u1
			rpg_items.iron_greeves['mount_point_x']=7
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_u1
			rpg_items.steel_greeves['mount_point_x']=7
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_u1
			rpg_items.platinum_greeves['mount_point_x']=7
			animationState+=1
		else:
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_u2
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_u2
			rpg_items.ragged_cloak['mount_point_x']=0
			rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_u2
			rpg_items.iron_chestplate['mount_point_x']=0
			rpg_items.iron_chestplate['mount_point_y']=14
			rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_u2
			rpg_items.steel_chestplate['mount_point_x']=0
			rpg_items.steel_chestplate['mount_point_y']=14
			rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_u2
			rpg_items.platinum_chestplate['mount_point_x']=0
			rpg_items.platinum_chestplate['mount_point_y']=14
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_u2
			rpg_items.iron_greeves['mount_point_x']=6
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_u2
			rpg_items.steel_greeves['mount_point_x']=6
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_u2
			rpg_items.platinum_greeves['mount_point_x']=6
			animationState-=1
	elif(direction=='down'):
		rpg_classes.hero.hold_point_x=17
		rpg_classes.hero.hold_point_y=25
		rpg_items.iron_greeves['mount_point_y']=27
		rpg_items.steel_greeves['mount_point_y']=27
		rpg_items.platinum_greeves['mount_point_y']=27
		rpg_items.iron_helmet['sprite']=rpg_file_def.iron_helmet_sprite_d
		rpg_items.iron_helmet['mount_point_x']=5
		rpg_items.steel_helmet['sprite']=rpg_file_def.steel_helmet_sprite_d
		rpg_items.steel_helmet['mount_point_x']=5
		rpg_items.platinum_helmet['sprite']=rpg_file_def.platinum_helmet_sprite_d
		rpg_items.platinum_helmet['mount_point_x']=5
		rpg_items.wood_bow['sprite']=rpg_file_def.wood_bow_sprite_d
		rpg_items.wood_bow['hold_point_x']=7
		rpg_items.wood_bow['hold_point_y']=15
		rpg_items.wood_axe['sprite']=rpg_file_def.wood_axe_sprite_d
		rpg_items.wood_axe['hold_point_x']=7
		rpg_items.leather_cap['sprite']=rpg_file_def.leather_cap_sprite_d
		rpg_items.leather_cap['mount_point_x']=5
		rpg_items.glock['sprite']=rpg_file_def.glock_sprite_v
		rpg_items.glock['hold_point_x']=13
		rpg_items.glock['hold_point_y']=5
		rpg_items.crossbow['sprite']=rpg_file_def.crossbow_sprite_d
		rpg_items.crossbow['hold_point_x']=8
		rpg_items.crossbow['hold_point_y']=4
		rpg_items.fire_bow['sprite'] = rpg_file_def.fire_bow_sprite_u1 # change
		rpg_items.fire_bow['hold_point_x'] = 7
		rpg_items.fire_bow['hold_point_y'] = 20
		rpg_items.iron_bow['sprite'] = rpg_file_def.iron_bow_sprite_d
		rpg_items.iron_bow['hold_point_x'] = 7
		rpg_items.iron_bow['hold_point_y'] = 20
		rpg_items.platnium_bow['sprite'] = rpg_file_def.platnium_bow_sprite_d
		rpg_items.platnium_bow['hold_point_x'] = 7
		rpg_items.platnium_bow['hold_point_y'] = 20
		rpg_items.headband['sprite'] = rpg_file_def.headband_sprite_d
		rpg_items.headband['mount_point_x'] = 3
		rpg_items.headband['mount_point_y'] = 3
		if(animationState==0):
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_d1
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_d1
			rpg_items.iron_greeves['mount_point_x']=6
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_d1
			rpg_items.steel_greeves['mount_point_x']=6
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_d1
			rpg_items.platinum_greeves['mount_point_x']=6
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_d1
			rpg_items.ragged_cloak['mount_point_x']=0
			rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_d1
			rpg_items.iron_chestplate['mount_point_x']=0
			rpg_items.iron_chestplate['mount_point_y']=14
			rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_d1
			rpg_items.steel_chestplate['mount_point_x']=0
			rpg_items.steel_chestplate['mount_point_y']=14
			rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_d1
			rpg_items.platinum_chestplate['mount_point_x']=0
			rpg_items.platinum_chestplate['mount_point_y']=14
			animationState+=1
		else:
			rpg_classes.hero.sprite=rpg_file_def.hero_sprite_d2
			rpg_items.iron_greeves['sprite']=rpg_file_def.iron_greeves_sprite_d2
			rpg_items.iron_greeves['mount_point_x']=7
			rpg_items.steel_greeves['sprite']=rpg_file_def.steel_greeves_sprite_d2
			rpg_items.steel_greeves['mount_point_x']=7
			rpg_items.platinum_greeves['sprite']=rpg_file_def.platinum_greeves_sprite_d2
			rpg_items.platinum_greeves['mount_point_x']=7
			rpg_items.ragged_cloak['sprite']=rpg_file_def.ragged_cloak_sprite_d2
			rpg_items.ragged_cloak['mount_point_x']=0
			rpg_items.iron_chestplate['sprite']=rpg_file_def.iron_chestplate_sprite_d2
			rpg_items.iron_chestplate['mount_point_x']=0
			rpg_items.iron_chestplate['mount_point_y']=14
			rpg_items.steel_chestplate['sprite']=rpg_file_def.steel_chestplate_sprite_d2
			rpg_items.steel_chestplate['mount_point_x']=0
			rpg_items.steel_chestplate['mount_point_y']=14
			rpg_items.platinum_chestplate['sprite']=rpg_file_def.platinum_chestplate_sprite_d2
			rpg_items.platinum_chestplate['mount_point_x']=0
			rpg_items.platinum_chestplate['mount_point_y']=14
			animationState-=1

player_control=True

def enterRoom():
	room_number_label=font.render('Room '+str(rpg_classes.hero.room),1,(0,0,0))
	score_label=font.render('Score: '+str(rpg_classes.hero.score),1,(0,0,0))
	rpg_mechanics.loot
	player_control=False
	animation=True
	door=None
	animationStage=0
	animationState
	if(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,450,boundary_width,100,20)):
		door='top'
	elif(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,450,map_height-boundary_width-rpg_classes.hero.height,100,boundary_width+rpg_classes.hero.height)):
		door='bottom'
	elif(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,0,300,boundary_width+rpg_classes.hero.width,100)):
		door='left'
	elif(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,map_width-boundary_width-boundary_width,300,map_width,100)):
		door='right'
	while(animation):
		DISPLAYSURF.blit(background,(0,0))
		DISPLAYSURF.blit(room_number_label,(30,30))
		DISPLAYSURF.blit(score_label,(30,60))
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
		for i in rpg_mechanics.mobs:
			DISPLAYSURF.blit(i[2],(i[0],i[1]))
			pygame.draw.rect(DISPLAYSURF,(255,255,255),(i[0],i[1]-20,i[7],10))
			pygame.draw.rect(DISPLAYSURF,(255,0,0),(i[0],i[1]-20,(i[7])*(i[5]/float(i[9])),10))
			rpg_mechanics.displayObstacles()
			if(i[4]=='skeleton'):
				DISPLAYSURF.blit(i[16],(i[0]+i[17],i[1]+i[18]))
		for i in rpg_mechanics.loot:
			DISPLAYSURF.blit(i[0]['default_sprite'],(i[1],i[2]))
		if(int(rpg_classes.hero.health)==0):
			DISPLAYSURF.blit(rpg_file_def.broken_heart,(500,20))
		else:
			for i in range(int(rpg_classes.hero.health)):
				DISPLAYSURF.blit(rpg_file_def.heart,(500+(35*i),20))
		if(door=='top'):
			if(animationStage==0):
				if((rpg_classes.hero.y+rpg_classes.hero.height)>-1):
					rpg_classes.hero.y-=rpg_classes.hero.speed*.5
					animateMovement('up')
				else:
					animationStage=1
					rpg_classes.hero.score+=200
					rpg_classes.hero.y=map_height
					rpg_mechanics.resetObstacles()
					rpg_mechanics.populateObstacles()
					if((rpg_classes.hero.room+1)%10==0):
						rpg_mechanics.boss_fight=True
						if(rpg_classes.cookie_man.defeated==False):
							rpg_mechanics.boss=rpg_classes.cookie_man
						elif(rpg_classes.necromancer.defeated==False):
							rpg_mechanics.boss=rpg_classes.necromancer
						else:
							rpg_mechanics.game_complete=True
					rpg_classes.hero.room+=1
					if(rpg_mechanics.boss_fight==False):
						rpg_mechanics.populateMobs()
					rpg_mechanics.loot=[]
			if(animationStage==1):
				if ((rpg_classes.hero.y+rpg_classes.hero.height>map_height-boundary_width) and animationStage==1):
					rpg_classes.hero.y-=rpg_classes.hero.speed*.5
					animateMovement('up')
				else:
					animation=False
		elif(door=='bottom'):
			if(animationStage==0):
				if((rpg_classes.hero.y+rpg_classes.hero.height)<700):
					rpg_classes.hero.y+=rpg_classes.hero.speed*.5
				else:
					animationStage=1
					rpg_classes.hero.score+=200
					rpg_classes.hero.y=0
					rpg_mechanics.resetObstacles()
					rpg_mechanics.populateObstacles()
					if((rpg_classes.hero.room+1)%10==0):
						rpg_mechanics.boss_fight=True
						if(rpg_classes.cookie_man.defeated==False):
							rpg_mechanics.boss=rpg_classes.cookie_man
						elif(rpg_classes.necromancer.defeated==False):
							rpg_mechanics.boss=rpg_classes.necromancer
						else:
							rpg_mechanics.game_complete=True
					rpg_classes.hero.room+=1
					if(rpg_mechanics.boss_fight==False):
						rpg_mechanics.populateMobs()
					rpg_mechanics.loot=[]
			if(animationStage==1):
				if ((rpg_classes.hero.y+rpg_classes.hero.height<boundary_width+rpg_classes.hero.height)):
					rpg_classes.hero.y+=rpg_classes.hero.speed*.5
				else:
					animation=False
		elif(door=='left'):
			if(animationStage==0):
				if((rpg_classes.hero.x+rpg_classes.hero.width)>-1):
					rpg_classes.hero.x-=rpg_classes.hero.speed*.5
					animateMovement('left')
				else:
					animationStage=1
					rpg_classes.hero.score+=200
					rpg_classes.hero.x=map_width
					rpg_mechanics.resetObstacles()
					rpg_mechanics.populateObstacles()
					if((rpg_classes.hero.room+1)%10==0):
						rpg_mechanics.boss_fight=True
						if(rpg_classes.cookie_man.defeated==False):
							rpg_mechanics.boss=rpg_classes.cookie_man
						elif(rpg_classes.necromancer.defeated==False):
							rpg_mechanics.boss=rpg_classes.necromancer
						else:
							rpg_mechanics.game_complete=True
					rpg_classes.hero.room+=1
					if(rpg_mechanics.boss_fight==False):
						rpg_mechanics.populateMobs()
					rpg_mechanics.loot=[]
			if(animationStage==1):
				if ((rpg_classes.hero.x+rpg_classes.hero.width>map_width-boundary_width)):
					rpg_classes.hero.x-=rpg_classes.hero.speed*.5
					animateMovement('left')
				else:
					animation=False
		elif(door=='right'):
			if(animationStage==0):
				if((rpg_classes.hero.x+rpg_classes.hero.width)<1001):
					rpg_classes.hero.x+=rpg_classes.hero.speed*.5
					animateMovement('right')
				else:
					animationStage=1
					rpg_classes.hero.score+=200
					rpg_classes.hero.x=0
					rpg_mechanics.resetObstacles()
					rpg_mechanics.populateObstacles()
					if((rpg_classes.hero.room+1)%10==0):
						rpg_mechanics.boss_fight=True
						if(rpg_classes.cookie_man.defeated==False):
							rpg_mechanics.boss=rpg_classes.cookie_man
						elif(rpg_classes.necromancer.defeated==False):
							rpg_mechanics.boss=rpg_classes.necromancer
						else:
							rpg_mechanics.game_complete=True
					rpg_classes.hero.room+=1
					if(rpg_mechanics.boss_fight==False):
						rpg_mechanics.populateMobs()
					rpg_mechanics.loot=[]
			if(animationStage==1):
				if((rpg_classes.hero.x+rpg_classes.hero.width<boundary_width+rpg_classes.hero.width)):
					rpg_classes.hero.x+=rpg_classes.hero.speed*.5
					animateMovement('right')
				else:
					animation=False
		else:
			animation=False

		animateWeapon()

		pygame.display.update()
		fpsClock.tick(FPS)
	player_control=True