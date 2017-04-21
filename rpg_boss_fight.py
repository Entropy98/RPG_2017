import pygame, sys
from pygame import *
import random
import math
import rpg_file_def
import rpg_items
import rpg_mechanics
import rpg_animations
import rpg_classes
import rpg_game_over
import rpg_class_select
import rpg_inventory

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))
pygame.display.set_caption('RPG')
pygame.key.set_repeat(10,10)
skeleton_attack_timer=rpg_mechanics.skeleton_attack_time
background=pygame.image.load('rpg_background_with_doors.png')
font=pygame.font.SysFont('monospace',15)
FPS=30
fpsClock=pygame.time.Clock()

def run():
	while(rpg_mechanics.inventory_menu):
		rpg_inventory.run()

	while(rpg_mechanics.game_over):
		rpg_game_over.run1()

	while(rpg_mechanics.game_complete):
		rpg_game_over.run2()

	if(rpg_mechanics.boss.health>0):
		rpg_mechanics.roomClear=False

	if(rpg_classes.cookie_man.defeated==True and rpg_classes.necromancer.defeated==True):
		rpg_mechanics.game_complete=True

	direction=None
	DISPLAYSURF.blit(background,(0,0))
	room_number_label=font.render('Room '+str(rpg_classes.hero.room),1,(0,0,0))
	score_label=font.render('Score: '+str(rpg_classes.hero.score),1,(0,0,0))
	DISPLAYSURF.blit(room_number_label,(30,30))
	DISPLAYSURF.blit(score_label,(30,60))
	if(rpg_mechanics.boss.health>0):
		DISPLAYSURF.blit(rpg_mechanics.boss.sprite,(rpg_mechanics.boss.x,rpg_mechanics.boss.y))
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

	rpg_mechanics.displayLoot()
	rpg_mechanics.displayObstacles()

	rpg_mechanics.player_attack_delay+=1
	rpg_mechanics.double_press_timer+=1
	rpg_mechanics.boss_attack_timer+=1
	rpg_mechanics.killMob()

	if(rpg_classes.hero.name=='ranger'):
		for i in rpg_class_select.obstacles:
			for j in rpg_mechanics.active_projectile:
				if(rpg_mechanics.interaction(j[0],j[1],rpg_classes.hero.projectile['x_width'],rpg_classes.hero.projectile['x_height'],i[0][0],i[1][0],i[0][1],i[1][1])):
					rpg_mechanics.active_projectile.remove(j)

	if(rpg_mechanics.roomClear==False):
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(450,-1,100,boundary_width))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(0,300,boundary_width,100))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(450,map_height-boundary_width,100,boundary_width))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(map_width-boundary_width,300,boundary_width,100))

		if(rpg_classes.hero.name=='ranger'):
			for i in rpg_mechanics.active_projectile:
				if(i[3]=='up'):
					i[1]-=rpg_classes.hero.projectile_speed
					DISPLAYSURF.blit(rpg_classes.hero.projectile['up_sprite'],(i[0],i[1]))
				elif(i[3]=='down'):
					i[1]+=rpg_classes.hero.projectile_speed
					DISPLAYSURF.blit(rpg_classes.hero.projectile['down_sprite'],(i[0],i[1]))
				elif(i[3]=='left'):
					i[0]-=rpg_classes.hero.projectile_speed
					DISPLAYSURF.blit(rpg_classes.hero.projectile['left_sprite'],(i[0],i[1]))
				elif(i[3]=='right'):
					i[0]+=rpg_classes.hero.projectile_speed
					DISPLAYSURF.blit(rpg_classes.hero.projectile['right_sprite'],(i[0],i[1]))
				if(rpg_mechanics.interaction(rpg_mechanics.boss.x,rpg_mechanics.boss.y,rpg_mechanics.boss.width,rpg_mechanics.boss.height,i[0],i[1],rpg_items.arrow['x_width'],rpg_items.arrow['x_height'])):
					rpg_mechanics.boss.health-=1
					rpg_mechanics.active_projectile.remove(i)

			for i in rpg_mechanics.mobs:
				for j in rpg_mechanics.active_projectile:
					if(j[3]=='up' or j[3]=='down'):
						if(rpg_mechanics.interaction(j[0],j[1],rpg_classes.hero.projectile['x_height'],rpg_classes.hero.projectile['x_width'],i[0],i[1],i[7],i[8])):
							if(rpg_classes.hero.weapon==rpg_items.fire_bow):
								i[10]='fire'
							i[5]-=rpg_classes.hero.damage
							rpg_mechanics.active_projectile.remove(j)
					elif(j[3]=='left' or j[3]=='right'):
						if(rpg_mechanics.interaction(j[0],j[1],rpg_classes.hero.projectile['x_width'],rpg_classes.hero.projectile['x_height'],i[0],i[1],i[7],i[8])):
							if(rpg_classes.hero.weapon==rpg_items.fire_bow):
								i[10]='fire'
							i[5]-=rpg_classes.hero.damage
							rpg_mechanics.active_projectile.remove(j)

		if(rpg_mechanics.boss==rpg_classes.cookie_man):
			if(rpg_classes.hero.x>rpg_mechanics.boss.x):
				if(rpg_mechanics.legalMobMovement(rpg_mechanics.boss.x,rpg_mechanics.boss.y,rpg_mechanics.boss.width,rpg_mechanics.boss.height,'right',rpg_mechanics.boss.speed)):
					rpg_mechanics.boss.x+=rpg_mechanics.boss.speed
			elif(rpg_classes.hero.x<rpg_mechanics.boss.x):
				if(rpg_mechanics.legalMobMovement(rpg_mechanics.boss.x,rpg_mechanics.boss.y,rpg_mechanics.boss.width,rpg_mechanics.boss.height,'left',rpg_mechanics.boss.speed)):
					rpg_mechanics.boss.x-=rpg_mechanics.boss.speed
			if(rpg_classes.hero.y>rpg_mechanics.boss.y):
				if(rpg_mechanics.legalMobMovement(rpg_mechanics.boss.x,rpg_mechanics.boss.y,rpg_mechanics.boss.width,rpg_mechanics.boss.height,'down',rpg_mechanics.boss.speed)):
					rpg_mechanics.boss.y+=rpg_mechanics.boss.speed
			elif(rpg_classes.hero.y<rpg_mechanics.boss.y):
				if(rpg_mechanics.legalMobMovement(rpg_mechanics.boss.x,rpg_mechanics.boss.y,rpg_mechanics.boss.width,rpg_mechanics.boss.height,'up',rpg_mechanics.boss.speed)):
					rpg_mechanics.boss.y-=rpg_mechanics.boss.speed

			if(len(rpg_mechanics.active_mob_projectile)==0 and rpg_mechanics.boss_attack_timer>=rpg_mechanics.boss_attack_time):
				x_dist=rpg_classes.hero.x-rpg_mechanics.boss.x
				y_dist=rpg_classes.hero.y-rpg_mechanics.boss.y
				if(x_dist>y_dist):
					if(x_dist<0):
						direction='left'
					else:
						direction='right'
				else:
					if(y_dist<0):
						direction='up'
					else:
						direction='down'
				z_dist=math.sqrt((float(x_dist)**2)+(y_dist**2))
				x_unit_dist=x_dist/float(z_dist)
				y_unit_dist=y_dist/float(z_dist)
				rpg_mechanics.active_mob_projectile.append([rpg_mechanics.boss.x+(rpg_mechanics.boss.width/float(2)),rpg_mechanics.boss.y+6,(x_unit_dist*rpg_mechanics.boss.projectile_speed),(y_unit_dist*rpg_mechanics.boss.projectile_speed),direction])
				rpg_mechanics.boss_attack_timer=0

			if(len(rpg_mechanics.active_mob_projectile)==0):
				rpg_classes.cookie_man.sprite=rpg_file_def.cookie_man_sprite_r1
			else:
				rpg_classes.cookie_man.sprite=rpg_file_def.cookie_man_sprite_r1_headless

		right=850
		left=100
		up=100
		down=550
		x_speed=rpg_mechanics.boss.speed
		y_speed=rpg_mechanics.boss.speed
		if(rpg_mechanics.boss==rpg_classes.necromancer):
			if(rpg_mechanics.necromancer_state=='select'):
				rpg_mechanics.necromancer_corner=random.randint(1,4)
				if(rpg_mechanics.necromancer_corner==1):
					x_dist=right-rpg_mechanics.boss.x
					y_dist=up-rpg_mechanics.boss.y
				elif(rpg_mechanics.necromancer_corner==2):
					x_dist=left-rpg_mechanics.boss.x
					y_dist=up-rpg_mechanics.boss.y
				elif(rpg_mechanics.necromancer_corner==3):
					x_dist=left-rpg_mechanics.boss.x
					y_dist=down-rpg_mechanics.boss.y
				elif(rpg_mechanics.necromancer_corner==4):
					x_dist=right-rpg_mechanics.boss.x
					y_dist=down-rpg_mechanics.boss.y

				z_dist=math.sqrt((float(x_dist)**2)+(y_dist**2))
				x_unit_dist=x_dist/float(z_dist)
				y_unit_dist=y_dist/float(z_dist)
				x_speed=x_unit_dist*rpg_mechanics.boss.speed
				y_speed=y_unit_dist*rpg_mechanics.boss.speed
				rpg_mechanics.necromancer_state='walk'
			elif(rpg_mechanics.necromancer_state=='walk'):
				if(rpg_mechanics.necromancer_corner==1):
					if(rpg_mechanics.boss.x<right):
						rpg_mechanics.boss.x+=x_speed
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_sprite_r
					if(rpg_mechanics.boss.y>up):
						rpg_mechanics.boss.y-=y_speed
					if(rpg_mechanics.boss.x>=right and rpg_mechanics.boss.y<=up):
						rpg_mechanics.necromancer_state='attack'
				if(rpg_mechanics.necromancer_corner==2):
					if(rpg_mechanics.boss.x>left):
						rpg_mechanics.boss.x-=x_speed
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_sprite_l
					if(rpg_mechanics.boss.y>up):
						rpg_mechanics.boss.y-=y_speed
					if(rpg_mechanics.boss.x<=left and rpg_mechanics.boss.y<=up):
						rpg_mechanics.necromancer_state='attack'
				if(rpg_mechanics.necromancer_corner==3):
					if(rpg_mechanics.boss.x>left):
						rpg_mechanics.boss.x-=x_speed
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_sprite_l
					if(rpg_mechanics.boss.y<down):
						rpg_mechanics.boss.y+=y_speed
					if(rpg_mechanics.boss.x<=left and rpg_mechanics.boss.y>=down):
						rpg_mechanics.necromancer_state='attack'
				if(rpg_mechanics.necromancer_corner==4):
					if(rpg_mechanics.boss.x<right):
						rpg_mechanics.boss.x+=x_speed
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_sprite_r
					if(rpg_mechanics.boss.y<down):
						rpg_mechanics.boss.y+=y_speed
					if(rpg_mechanics.boss.x>=right and rpg_mechanics.boss.y>=down):
						rpg_mechanics.necromancer_state='attack'
			if(rpg_mechanics.necromancer_state=='attack'):
				repelQuadrant=random.randint(1,4)
				repelRange=150
				projectile_speed=15
				weapon_sprite=rpg_file_def.wood_bow_sprite_l
				hold_point_x=2
				hold_point_y=-6
				debuf=None
				animationState=0
				mobs_spawned=False
				if(mobs_spawned==False):
					if(rpg_mechanics.necromancer_corner==1 or rpg_mechanics.necromancer_corner==4):
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_attack_sprite_l
					else:
						rpg_mechanics.boss.sprite=rpg_file_def.necromancer_attack_sprite_r
					rpg_mechanics.mobs.append([rpg_mechanics.boss.x+rpg_mechanics.boss.width,rpg_mechanics.boss.y,rpg_classes.skeleton.sprite,rpg_classes.skeleton.speed,'skeleton',rpg_classes.skeleton.health,[rpg_items.one_up],rpg_classes.skeleton.width,\
						rpg_classes.skeleton.height,rpg_classes.skeleton.health,debuf,animationState,4,repelRange,projectile_speed,0,weapon_sprite,\
						hold_point_x,hold_point_y])
					rpg_mechanics.mobs.append([rpg_mechanics.boss.x-rpg_classes.skeleton.width,rpg_mechanics.boss.y,rpg_classes.skeleton.sprite,rpg_classes.skeleton.speed,'skeleton',rpg_classes.skeleton.health,[rpg_items.one_up],rpg_classes.skeleton.width,\
						rpg_classes.skeleton.height,rpg_classes.skeleton.health,debuf,animationState,2,repelRange,projectile_speed,50,weapon_sprite,\
						hold_point_x,hold_point_y])
					rpg_mechanics.mobs.append([rpg_mechanics.boss.x,rpg_mechanics.boss.y-rpg_classes.skeleton.height,rpg_classes.skeleton.sprite,rpg_classes.skeleton.speed,'skeleton',rpg_classes.skeleton.health,[rpg_items.one_up],rpg_classes.skeleton.width,\
						rpg_classes.skeleton.height,rpg_classes.skeleton.health,debuf,animationState,3,repelRange,projectile_speed,75,weapon_sprite,\
						hold_point_x,hold_point_y])
					rpg_mechanics.mobs.append([rpg_mechanics.boss.x,rpg_mechanics.boss.y+rpg_mechanics.boss.height,rpg_classes.skeleton.sprite,rpg_classes.skeleton.speed,'skeleton',rpg_classes.skeleton.health,[rpg_items.one_up],rpg_classes.skeleton.width,\
						rpg_classes.skeleton.height,rpg_classes.skeleton.health,debuf,animationState,1,repelRange,projectile_speed,25,weapon_sprite,\
						hold_point_x,hold_point_y])
					mobs_spawned=True
				rpg_mechanics.necromancer_wait_time=0
				rpg_mechanics.necromancer_state='wait'
			if(rpg_mechanics.necromancer_state=='wait'):
				rpg_mechanics.necromancer_wait_time+=1
				if(rpg_mechanics.necromancer_wait_time>=100):
					rpg_mechanics.necromancer_state='select'

		for i in rpg_mechanics.mobs:
			rpg_mechanics.mob_location.append(((i[0],i[7]),(i[1],i[8])))

		for i in rpg_mechanics.mobs:
			if(i[4]=='skeleton'):
				i[15]+=1
				if(i[15]>rpg_mechanics.skeleton_attack_time):
					x_dist=rpg_classes.hero.x-i[0]
					y_dist=rpg_classes.hero.y-i[1]
					if(x_dist>y_dist):
						if(x_dist<0):
							direction='left'
						else:
							direction='right'
					else:
						if(y_dist<0):
							direction='up'
						else:
							direction='down'
					z_dist=math.sqrt((float(x_dist)**2)+(y_dist**2))
					x_unit_dist=x_dist/float(z_dist)
					y_unit_dist=y_dist/float(z_dist)
					rpg_mechanics.active_mob_projectile.append([i[0]+(i[7]/float(2)),i[1]+(i[8]/float(2)),(x_unit_dist*i[14]),(y_unit_dist*i[14]),direction])
					i[15]=0

		for i in rpg_mechanics.mobs:
			DISPLAYSURF.blit(i[2],(i[0],i[1]))
			pygame.draw.rect(DISPLAYSURF,(255,255,255),(i[0],i[1]-20,i[7],10))
			pygame.draw.rect(DISPLAYSURF,(255,0,0),(i[0],i[1]-20,(i[7])*(i[5]/float(i[9])),10))
			if(i[4]=='skeleton'):
				DISPLAYSURF.blit(i[16],(i[0]+i[17],i[1]+i[18]))

		for i in rpg_mechanics.mobs:
			if(i[10]=='fire'):
				i[5]-=.5
				if(i[11]==1):
					DISPLAYSURF.blit(rpg_file_def.fire_sprite_1,(i[0],i[1]+i[8]-20))
				else:
					DISPLAYSURF.blit(rpg_file_def.fire_sprite_2,(i[0],i[1]+i[8]-20))

			if(i[4]=='skeleton'):
				if(i[12]==1):
					if(rpg_classes.hero.x+i[13]>i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'right')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
					elif(rpg_classes.hero.x+i[13]<i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'left')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
					if(rpg_classes.hero.y-i[13]<i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]
					elif(rpg_classes.hero.y-i[13]>i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
				elif(i[12]==2):
					if(rpg_classes.hero.x-i[13]<i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'left')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
					elif(rpg_classes.hero.x-i[13]>i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'right')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
					if(rpg_classes.hero.y-i[13]<i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]
					elif(rpg_classes.hero.y-i[13]>i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
				elif(i[12]==3):
					if(rpg_classes.hero.x-i[13]<i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'left')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
					elif(rpg_classes.hero.x-i[13]>i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'right')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
					if(rpg_classes.hero.y+i[13]>i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
					elif(rpg_classes.hero.y+i[13]<i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]
				elif(i[12]==4):
					if(rpg_classes.hero.x+i[13]>i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'right')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
					elif(rpg_classes.hero.x+i[13]<i[0]):
						i[2],i[17],i[11],i[16]=rpg_animations.animateSkeletonMovement(i[11],'left')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
					if(rpg_classes.hero.y+i[13]>i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
					elif(rpg_classes.hero.y+i[13]<i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]

		for i in rpg_class_select.obstacles:
			for j in rpg_mechanics.active_mob_projectile:
				if(rpg_mechanics.interaction(j[0],j[1],13,13,i[0][0],i[1][0],i[0][1],i[1][1])):
					rpg_mechanics.active_mob_projectile.remove(j)

		for i in rpg_mechanics.active_mob_projectile:
			i[0]+=i[2]
			i[1]+=i[3]
			if(i[4]=='up'):
				DISPLAYSURF.blit(rpg_mechanics.boss.projectile,(i[0],i[1]))
			elif(i[4]=='down'):
				DISPLAYSURF.blit(rpg_mechanics.boss.projectile,(i[0],i[1]))
			elif(i[4]=='left'):
				DISPLAYSURF.blit(rpg_mechanics.boss.projectile,(i[0],i[1]))
			elif(i[4]=='right'):
				DISPLAYSURF.blit(rpg_mechanics.boss.projectile,(i[0],i[1]))
			if(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,i[0],i[1],13,13)):
				rpg_classes.hero.health-=rpg_mechanics.boss.damage
				rpg_mechanics.active_mob_projectile.remove(i)

	if(int(rpg_classes.hero.health)==0):
		DISPLAYSURF.blit(rpg_file_def.broken_heart,(500,20))
	else:
		for i in range(int(rpg_classes.hero.health)):
			DISPLAYSURF.blit(rpg_file_def.heart,(500+(35*i),20))

	for i in range(int(rpg_mechanics.boss.health)):
		DISPLAYSURF.blit(rpg_file_def.heart,(30+(35*i),20))

	if(rpg_mechanics.boss.health<=0):
		if(rpg_mechanics.boss.loot_dropped==False):
			rpg_mechanics.roomClear=True
			rpg_mechanics.boss.loot_dropped=True
			drop=random.choice(rpg_classes.hero.mythic_loot)
			rpg_mechanics.loot.append([drop,rpg_mechanics.boss.x,rpg_mechanics.boss.y])
			rpg_classes.hero.score+=500
		if(rpg_mechanics.boss==rpg_classes.cookie_man):
			rpg_classes.cookie_man.defeated=True
		if(rpg_mechanics.boss==rpg_classes.necromancer):
			rpg_classes.necromancer.defeated=True

	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()
	if(rpg_animations.player_control==True):
		keys=pygame.key.get_pressed()
		if(keys[K_w]):
			direction=K_w
		if(keys[K_s]):
			direction=K_s
		if(keys[K_a]):
			direction=K_a
		if(keys[K_d]):
			direction=K_d
		if(keys[K_UP]):
			if(rpg_mechanics.player_attack_delay>=rpg_classes.hero.attack_speed):
				if(rpg_classes.hero.attack=='melee'):
					rpg_mechanics.melee('up')
				if(rpg_classes.hero.attack=='projectile'):
					rpg_mechanics.projectile('up')
				rpg_mechanics.player_attack_delay=0
		if(keys[K_LEFT]):
			if(rpg_mechanics.player_attack_delay>=rpg_classes.hero.attack_speed):
				if(rpg_classes.hero.attack=='melee'):
					rpg_mechanics.melee('left')
				if(rpg_classes.hero.attack=='projectile'):
					rpg_mechanics.projectile('left')
				rpg_mechanics.player_attack_delay=0
		if(keys[K_RIGHT]):
			if(rpg_mechanics.player_attack_delay>=rpg_classes.hero.attack_speed):
				if(rpg_classes.hero.attack=='melee'):
					rpg_mechanics.melee('right')
				if(rpg_classes.hero.attack=='projectile'):
					rpg_mechanics.projectile('right')
				rpg_mechanics.player_attack_delay=0
		if(keys[K_DOWN]):
			if(rpg_mechanics.player_attack_delay>=rpg_classes.hero.attack_speed):
				if(rpg_classes.hero.attack=='melee'):
					rpg_mechanics.melee('down')
				if(rpg_classes.hero.attack=='projectile'):
					rpg_mechanics.projectile('down')
				rpg_mechanics.player_attack_delay=0
		if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
			if(len(rpg_classes.hero.inventory_list)<44):
				if(keys[K_e]):
					for i in rpg_mechanics.loot:
						if(i[0]['type']=='bow' or i[0]['type']=='axe' or i[0]['type']=='gun' or i[0]['type']=='sword'):
							if(rpg_mechanics.interaction(i[1],i[2],i[0]['width'],i[0]['height'],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
								if(i[0] not in rpg_classes.hero.inventory_list):
									if(rpg_classes.hero.weapon!=i[0]):
										rpg_classes.hero.inventory_list.append(rpg_classes.hero.weapon)
										rpg_classes.hero.addWeapon(i[0])
								else:
									rpg_classes.hero.inventory_list.remove(i[0])
									rpg_classes.hero.inventory_list.append(rpg_classes.hero.weapon)
									rpg_classes.hero.addWeapon(i[0])
								rpg_mechanics.loot.remove(i)
								rpg_mechanics.double_press_timer=0
						elif(i[0]['type']=='helmet'):
							if(rpg_mechanics.interaction(i[1],i[2],i[0]['width'],i[0]['height'],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
								if(i[0] not in rpg_classes.hero.inventory_list):
									if(rpg_classes.hero.helmet!=i[0]):
										if(rpg_classes.hero.helmet!=rpg_items.place_holder):
											rpg_classes.hero.inventory_list.append(rpg_classes.hero.helmet)
											rpg_classes.hero.addHelmet(i[0])
										else:
											rpg_classes.hero.addHelmet(i[0])
								else:
									rpg_classes.hero.inventory_list.remove(i[0])
									rpg_classes.hero.inventory_list.append(rpg_classes.hero.helmet)
									rpg_classes.hero.addHelmet(i[0])
								rpg_mechanics.loot.remove(i)
								rpg_mechanics.double_press_timer=0
						elif(i[0]['type']=='chest'):
							if(rpg_mechanics.interaction(i[1],i[2],i[0]['width'],i[0]['height'],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
								if(i[0] not in rpg_classes.hero.inventory_list):
									if(rpg_classes.hero.chest!=i[0]):
										if(rpg_classes.hero.chest!=rpg_items.place_holder):
											rpg_classes.hero.inventory_list.append(rpg_classes.hero.chest)
											rpg_classes.hero.addChest(i[0])
										else:
											rpg_classes.hero.addChest(i[0])
								else:
									rpg_classes.hero.inventory_list.remove(i[0])
									rpg_classes.hero.inventory_list.append(rpg_classes.hero.chest)
									rpg_classes.hero.addChest(i[0])
								rpg_mechanics.loot.remove(i)
								rpg_mechanics.double_press_timer=0
						elif(i[0]['type']=='pants'):
							if(rpg_mechanics.interaction(i[1],i[2],i[0]['width'],i[0]['height'],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
								if(i[0] not in rpg_classes.hero.inventory_list):
									if(rpg_classes.hero.pants!=i[0]):
										if(rpg_classes.hero.pants!=rpg_items.place_holder):
											rpg_classes.hero.inventory_list.append(rpg_classes.hero.pants)
											rpg_classes.hero.addPants(i[0])
										else:
											rpg_classes.hero.addPants(i[0])
								else:
									rpg_classes.hero.inventory_list.remove(i[0])
									rpg_classes.hero.inventory_list.append(rpg_classes.hero.pants)
									rpg_classes.hero.addPants(i[0])
								rpg_mechanics.loot.remove(i)
								rpg_mechanics.double_press_timer=0
				if(keys[K_i]):
					rpg_mechanics.inventory_menu=True
					rpg_mechanics.double_press_timer=0
				if(rpg_mechanics.roomClear==True):
					if(keys[K_r]):
						rpg_mechanics.boss_fight=False
						rpg_animations.enterRoom()

	rpg_classes.hero.x,rpg_classes.hero.y=rpg_mechanics.move(direction,rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.speed)

	if(rpg_classes.hero.health<=0):
		rpg_mechanics.game_over=True

	rpg_animations.animateWeapon()	
	rpg_mechanics.tickDOTs()
	pygame.display.update()
	fpsClock.tick(FPS)