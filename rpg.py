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
import rpg_boss_fight
import rpg_start_menu

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
zombie_attack_time=10
zombie_attack_timer=zombie_attack_time
skeleton_attack_timer=rpg_mechanics.skeleton_attack_time
transparentSurface=pygame.Surface((1000,700))
transparentSurface.set_alpha(128)
transparentSurface.fill((153,0,0))
rpg_mechanics.boss_fight=False
#main loop
while(True):

	while(rpg_mechanics.start_menu):
		rpg_start_menu.run()

	while(rpg_mechanics.game_over):
		rpg_game_over.run1()

	while(rpg_mechanics.class_select):
		rpg_class_select.run()

	while(rpg_mechanics.inventory_menu):
		rpg_inventory.run()

	while(rpg_mechanics.boss_fight):
		rpg_boss_fight.run()

	direction=None
	DISPLAYSURF.blit(background,(0,0))
	room_number_label=font.render('Room '+str(rpg_classes.hero.room),1,(0,0,0))
	score_label=font.render('Score: '+str(rpg_classes.hero.score),1,(0,0,0))
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

	zombie_attack_timer+=1
	rpg_mechanics.player_attack_delay+=1
	rpg_mechanics.double_press_timer+=1
	rpg_mechanics.killMob()

	if(len(rpg_mechanics.mobs)!=0):
		rpg_mechanics.roomClear=False

	rpg_mechanics.displayObstacles()
	if(rpg_mechanics.roomClear==True):
		rpg_mechanics.displayLoot()

	if(int(rpg_classes.hero.health)==0):
		DISPLAYSURF.blit(rpg_file_def.broken_heart,(500,20))
	else:
		for i in range(int(rpg_classes.hero.health)):
			DISPLAYSURF.blit(rpg_file_def.heart,(500+(35*i),20))

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

		for i in rpg_class_select.obstacles:
			for j in rpg_mechanics.active_projectile:
				if(rpg_mechanics.interaction(j[0],j[1],rpg_classes.hero.projectile['x_width'],rpg_classes.hero.projectile['x_height'],i[0][0],i[1][0],i[0][1],i[1][1])):
					rpg_mechanics.active_projectile.remove(j)

	for i in rpg_class_select.obstacles:
		for j in rpg_mechanics.active_mob_projectile:
				if(j[4]=='left' or j[4]=='right'):
					if(rpg_mechanics.interaction(i[0][0],i[1][0],i[0][1],i[1][1],j[0],j[1],rpg_items.arrow['x_height'],rpg_items.arrow['x_width'])):
						rpg_mechanics.active_mob_projectile.remove(j)
				if(j[4]=='up' or j[4]=='down'):
					if(rpg_mechanics.interaction(i[0][0],i[1][0],i[0][1],i[1][1],j[0],j[1],rpg_items.arrow['x_width'],rpg_items.arrow['x_height'])):
						rpg_mechanics.active_mob_projectile.remove(j)

	if(rpg_mechanics.roomClear==False):
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(450,-1,100,boundary_width))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(0,300,boundary_width,100))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(450,map_height-boundary_width,100,boundary_width))
		pygame.draw.rect(DISPLAYSURF,(166,124,82),(map_width-boundary_width,300,boundary_width,100))
		rpg_mechanics.displayLoot()

		for i in rpg_mechanics.mobs:
			rpg_mechanics.mob_location.append(((i[0],i[7]),(i[1],i[8])))

		for i in rpg_mechanics.mobs:
			if(i[4]=='zombie'):
				if(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,i[0],i[1],i[7],i[8])):
					if(zombie_attack_timer>zombie_attack_time):
						DISPLAYSURF.blit(transparentSurface,(0,0))
						rpg_classes.hero.health-=1*((100-rpg_classes.hero.armor)/float(100))
						zombie_attack_timer=0
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
			if(i[4]=='fire_elemental'):
				i[12]+=1
				if(i[13]==0):
					i[3]=rpg_classes.fire_elemental.speed
					if(rpg_classes.hero.x>i[0]):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'right','walk')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
					elif(rpg_classes.hero.x<i[0]):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'left','walk')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
					if(rpg_classes.hero.y>i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
					elif(rpg_classes.hero.y<i[1]):
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]

					if(i[12]>rpg_mechanics.fire_elemental_attack_time):
						if((rpg_mechanics.interaction(i[0],i[1],i[7]+i[14],i[8],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height))):
							i[13]=1
							i[12]=0
						elif((rpg_mechanics.interaction(i[0],i[1],i[7]-i[14],i[8],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height))):
							i[13]=2
							i[12]=0
						elif((rpg_mechanics.interaction(i[0],i[1],i[7],i[8]-i[14],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height))):
							i[13]=3
							i[12]=0
						elif((rpg_mechanics.interaction(i[0],i[1],i[7],i[8]+i[14],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height))):
							i[13]=4
							i[12]=0
				elif(i[13]==1):
					i[3]=10
					if(i[0]<rpg_classes.hero.x+rpg_classes.hero.width):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'right','attack')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
							i[0]+=i[3]
						else:
							i[13]=0
					else:
						i[13]=0
				elif(i[13]==2):
					i[3]=10
					if(i[0]>rpg_classes.hero.x):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'left','attack')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
							i[0]-=i[3]
						else:
							i[13]=0
					else:
						i[13]=0
				elif(i[13]==3):
					i[3]=10
					if(i[1]>rpg_classes.hero.y):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'up','attack')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
							i[1]-=i[3]
						else:
							i[13]=0
					else:
						i[13]=0
				elif(i[13]==4):
					i[3]=10
					if(i[1]<rpg_classes.hero.y+rpg_classes.hero.height):
						i[2],i[11]=rpg_animations.animateFireElementalMovement(i[11],'down','attack')
						if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
							i[1]+=i[3]
						else:
							i[13]=0
					else:
						i[13]=0

				if(rpg_mechanics.interaction(i[0],i[1],i[7],i[8],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
					rpg_classes.hero.debuf['fire']=90


		for i in rpg_mechanics.active_mob_projectile:
			i[0]+=i[2]
			i[1]+=i[3]
			if(i[4]=='up'):
				DISPLAYSURF.blit(rpg_file_def.arrow_up_sprite,(i[0],i[1]))
			elif(i[4]=='down'):
				DISPLAYSURF.blit(rpg_file_def.arrow_down_sprite,(i[0],i[1]))
			elif(i[4]=='left'):
				DISPLAYSURF.blit(rpg_file_def.arrow_left_sprite,(i[0],i[1]))
			elif(i[4]=='right'):
				DISPLAYSURF.blit(rpg_file_def.arrow_right_sprite,(i[0],i[1]))

		for i in rpg_mechanics.active_mob_projectile:
			if(i[4]=='left' or i[4]=='right'):
				if(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,i[0],i[1],rpg_items.arrow['x_height'],rpg_items.arrow['x_width'])):
					DISPLAYSURF.blit(transparentSurface,(0,0))
					rpg_classes.hero.health-=1*((100-rpg_classes.hero.armor)/float(100))
					rpg_mechanics.active_mob_projectile.remove(i)
			if(i[4]=='up' or i[4]=='down'):
				if(rpg_mechanics.interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,i[0],i[1],rpg_items.arrow['x_width'],rpg_items.arrow['x_height'])):
					DISPLAYSURF.blit(transparentSurface,(0,0))
					rpg_classes.hero.health-=1*((100-rpg_classes.hero.armor)/float(100))
					rpg_mechanics.active_mob_projectile.remove(i)

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

			if(i[4]=='zombie'):
				if(rpg_classes.hero.x>i[0]):
					i[2],i[11]=rpg_animations.animateZombieMovement(i[11],'right')
					if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'right',i[3])):
						i[0]+=i[3]
				elif(rpg_classes.hero.x<i[0]):
					i[2],i[11]=rpg_animations.animateZombieMovement(i[11],'left')
					if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'left',i[3])):
						i[0]-=i[3]
				if(rpg_classes.hero.y>i[1]):
					if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'down',i[3])):
						i[1]+=i[3]
				elif(rpg_classes.hero.y<i[1]):
					if(rpg_mechanics.legalMobMovement(i[0],i[1],i[7],i[8],'up',i[3])):
						i[1]-=i[3]

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

		if(len(rpg_mechanics.mobs)==0):
			rpg_mechanics.roomClear=True

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
								if(i[0]['rarity']=='Common'):
									rpg_classes.hero.score+=25
								elif(i[0]['rarity']=='Uncommon'):
									rpg_classes.hero.score+=50
								elif(i[0]['rarity']=='Rare'):
									rpg_classes.hero.score+=100
								elif(i[0]['rarity']=='Mythic'):
									rpg_classes.hero.score+=200
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
								if(i[0]['rarity']=='Common'):
									rpg_classes.hero.score+=25
								elif(i[0]['rarity']=='Uncommon'):
									rpg_classes.hero.score+=50
								elif(i[0]['rarity']=='Rare'):
									rpg_classes.hero.score+=100
								elif(i[0]['rarity']=='Mythic'):
									rpg_classes.hero.score+=200
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
								if(i[0]['rarity']=='Common'):
									rpg_classes.hero.score+=25
								elif(i[0]['rarity']=='Uncommon'):
									rpg_classes.hero.score+=50
								elif(i[0]['rarity']=='Rare'):
									rpg_classes.hero.score+=100
								elif(i[0]['rarity']=='Mythic'):
									rpg_classes.hero.score+=200
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
								if(i[0]['rarity']=='Common'):
									rpg_classes.hero.score+=25
								elif(i[0]['rarity']=='Uncommon'):
									rpg_classes.hero.score+=50
								elif(i[0]['rarity']=='Rare'):
									rpg_classes.hero.score+=100
								elif(i[0]['rarity']=='Mythic'):
									rpg_classes.hero.score+=200
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
						rpg_animations.enterRoom()

	rpg_classes.hero.x,rpg_classes.hero.y=rpg_mechanics.move(direction,rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.speed)

	if(rpg_classes.hero.health<=0):
		rpg_mechanics.game_over=True

	rpg_animations.animateWeapon()
	rpg_mechanics.tickDOTs()

	rpg_mechanics.mob_location=[]
	pygame.display.update()
	fpsClock.tick(FPS)