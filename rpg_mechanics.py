import rpg_classes
import random
import rpg_file_def
import rpg_items
import pygame, sys
from pygame import *
import rpg_animations
import rpg_items
import rpg_class_select

map_height=700
map_width=1000
boundary_width=20
DISPLAYSURF = pygame.display.set_mode((map_width,map_height))
font=pygame.font.SysFont('monospace',15)

double_press_time=5
double_press_timer=double_press_time
player_attack_delay=rpg_classes.hero.attack_speed

selectedClass=0
selectedMenuItem=0
class_select=False
game_over=False
game_complete=False
start_menu=True
controls_menu=False
credits_menu=False
item_selectX=0
item_selectY=0
inventory_menu=False
active_mob_projectile=[]
roomClear=True

def interaction(x1,y1,w1,h1,x2,y2,w2,h2):
	if((x1<=(x2+w2) and x1>=x2) or ((x1+w1)>=x2) and (x1+w1)<=(x2+w2)):
		if((y1<=(y2+h2) and y1>=y2) or ((y1+h1)>=y2) and (y1+h1)<=(y2+h2)):
			return True
	elif((x2<=(x1+w1) and x2>=x1) or ((x2+w2)>=x1) and (x2+w2)<=(x1+w1)):
		if((y2<=(y1+h1) and y2>=y1) or ((y2+h2)>=y1) and (y2+h2)<=(y1+h1)):
			return True
	else:
		return False

def legalMovement(curx,cury,desx,desy):
	ogdesx=desx
	ogdesy=desy
	illegal_locations=rpg_class_select.obstacles
	for i in illegal_locations:
		if(desx>curx):
			if(interaction(desx,cury,rpg_classes.hero.width,rpg_classes.hero.height,i[0][0],i[1][0],i[0][1],i[1][1])):
				desx=((i[0][0]-rpg_classes.hero.width)-1)
				return desx,ogdesy
			#if(((desx+rpg_classes.hero.width)>=i[0][0] and (curx+rpg_classes.hero.width)<i[0][0]) and (cury>i[1][0] and (cury+rpg_classes.hero.height)<i[1][1])):
			#	desx=((i[0][0]-rpg_classes.hero.width)-1)
			#	return desx,ogdesy
		elif(desx<curx):
			if(interaction(desx,cury,rpg_classes.hero.width,rpg_classes.hero.height,i[0][0],i[1][0],i[0][1],i[1][1])):
				desx=(i[0][0]+i[0][1]+1)
				return desx,ogdesy
			#if((desx<=i[0][1] and curx>i[0][0]) and (cury>i[1][0] and (cury+rpg_classes.hero.height)<i[1][1])):
			#	desx=(i[0][1]+1)
			#	return desx,ogdesy
		if(desy>cury):
			if(interaction(curx,desy,rpg_classes.hero.width,rpg_classes.hero.height,i[0][0],i[1][0],i[0][1],i[1][1])):
				desy=((i[1][0]-rpg_classes.hero.height)-1)
				return ogdesx,desy
			#if(((desy+rpg_classes.hero.height)>=i[1][0] and (cury+rpg_classes.hero.height)<i[1][0]) and (curx>i[0][0] and (curx+rpg_classes.hero.width)<i[0][1])):
			#	desy=((i[1][0]-rpg_classes.hero.height)-1)
			#	return ogdesx,desy
		elif(desy<cury):
			if(interaction(curx,desy,rpg_classes.hero.width,rpg_classes.hero.height,i[0][0],i[1][0],i[0][1],i[1][1])):
				desy=(i[1][0]+i[1][1]+1)
				return ogdesx,desy
			#if((desy<=i[1][1] and cury>i[1][0]) and (curx>i[0][0] and (curx+rpg_classes.hero.width)<i[0][1])):
			#	desy=(i[1][1]+1)
			#	return ogdesx,desy
	return ogdesx,ogdesy

poss_mobs=['zombie','skeleton','fire_elemental']
mobs=[]
mob_location=[]
skeleton_attack_time=100
fire_elemental_attack_time=100
def populateMobs():
	max_mobs=2+rpg_classes.hero.room
	if(max_mobs>7):
		max_mobs=7
	num_mobs=random.randint(3,max_mobs)
	animationState=0
	debuf=None
	for i in range(num_mobs):
		randx=random.randint(200,800)
		randy=random.randint(200,500)
		randmob=random.choice(poss_mobs)
		randItemSet=random.randint(0,100)
		if(randItemSet<=1):
			item_set=rpg_classes.hero.mythic_loot
		elif(randItemSet>1 and randItemSet<=6):
			item_set=rpg_classes.hero.rare_loot
		elif(randItemSet>5 and randItemSet<=45):
			item_set=rpg_classes.hero.uncommon_loot
		else:
			item_set=rpg_classes.hero.common_loot
		if(randmob=='zombie'):
			mobs.append([randx,randy,rpg_classes.zombie.sprite,rpg_classes.zombie.speed,'zombie',rpg_classes.zombie.health,item_set,rpg_classes.zombie.width,rpg_classes.zombie.height,rpg_classes.zombie.health,debuf,animationState])
		elif(randmob=='skeleton'):
			repelQuadrant=random.randint(1,4)
			repelRange=150
			projectile_speed=15
			weapon_sprite=rpg_file_def.wood_bow_sprite_l
			hold_point_x=2
			hold_point_y=-6
			attack_time=random.randint(0,100)
			mobs.append([randx,randy,rpg_classes.skeleton.sprite,rpg_classes.skeleton.speed,'skeleton',rpg_classes.skeleton.health,item_set,rpg_classes.skeleton.width,\
				rpg_classes.skeleton.height,rpg_classes.skeleton.health,debuf,animationState,repelQuadrant,repelRange,projectile_speed,attack_time,weapon_sprite,\
				hold_point_x,hold_point_y])
		elif(randmob=='fire_elemental'):
			fire_elemental_attack_state=0
			fire_elemental_attack_range=200
			mobs.append([randx,randy,rpg_classes.fire_elemental.sprite,rpg_classes.fire_elemental.speed,'fire_elemental',rpg_classes.fire_elemental.health,item_set,\
				rpg_classes.fire_elemental.width,rpg_classes.fire_elemental.height,rpg_classes.fire_elemental.health,debuf,animationState,fire_elemental_attack_time,\
				fire_elemental_attack_state,fire_elemental_attack_range])

loot=[]
def killMob():
	global loot
	for i in mobs:
		if(i[5]<=0):
			if(i[4]=='zombie'):
				rpg_classes.hero.score+=50
			elif(i[4]=='skeleton'):
				rpg_classes.hero.score+=75
			elif(i[4]=='fire_elemental'):
				rpg_classes.hero.score+=100
			drop=random.choice(i[6])
			loot.append([drop,i[0],i[1]])
			mobs.remove(i)

boss_fight=False
bosses=[rpg_classes.necromancer,rpg_classes.cookie_man]
necromancer_state='select'
necromancer_corner=1
necromancer_wait_time=100
boss=rpg_classes.cookie_man
boss_attack_time=boss.attack_speed
boss_attack_timer=boss.attack_speed

def melee(direction):
	if(direction=='up'):
		if(boss_fight==True):
			if(interaction(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,boss.x,boss.y,boss.width,boss.height)):
				boss.health-=1
				pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
			for i in mobs:
				if(interaction(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
		else:
			for i in mobs:
				if(interaction(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y-rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
	elif(direction=='down'):
		if(boss_fight==True):
			if(interaction(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,boss.x,boss.y,boss.width,boss.height)):
				boss.health-=1
				pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
			for i in mobs:
				if(interaction(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
		else:
			for i in mobs:
				if(interaction(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x,rpg_classes.hero.y+rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
	elif(direction=='left'):
		if(boss_fight==True):
			if(interaction(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,boss.x,boss.y,boss.width,boss.height)):
				boss.health-=1
				pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
			for i in mobs:
				if(interaction(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
		else:
			for i in mobs:
				if(interaction(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x-rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
	elif(direction=='right'):
		if(boss_fight==True):
			if(interaction(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,boss.x,boss.y,boss.width,boss.height)):
				boss.health-=1
				pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
			for i in mobs:
				if(interaction(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))
		else:
			for i in mobs:
				if(interaction(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range,i[0],i[1],i[7],i[8])):
					i[5]-=rpg_classes.hero.damage
					if(rpg_classes.hero.weapon==rpg_items.fire_sword):
						i[10]='fire'
					pygame.draw.rect(DISPLAYSURF,(255,0,0),(rpg_classes.hero.x+rpg_classes.hero.melee_range,rpg_classes.hero.y,rpg_classes.hero.melee_range,rpg_classes.hero.melee_range))

def legalMobMovement(curx,cury,width,height,direction,speed):
	cur_mob_locations=[]
	illegal_locations=[]
	for i in mobs:
		cur_mob_locations.append(((i[0],i[7]),(i[1],i[8])))
	illegal_locations.extend(rpg_class_select.obstacles)
	illegal_locations.extend(cur_mob_locations)
	for i in illegal_locations:
		if(direction=='right'):
			if((interaction(curx+speed,cury,width,height,i[0][0],i[1][0],i[0][1],i[1][1])) and (i!=((curx,width),(cury,height)))):
				return False
		elif(direction=='left'):
			if((interaction(i[0][0],i[1][0],i[0][1],i[1][1],curx-speed,cury,width,height)) and (i!=((curx,width),(cury,height))) or curx-speed<boundary_width):
				return False
		elif(direction=='up'):
			if((interaction(curx,cury-height,width,height,i[0][0],i[1][0],i[0][1],i[1][1])) and (i!=((curx,width),(cury,height))) or cury-speed<boundary_width):
				return False
		elif(direction=='down'):
			if((interaction(i[0][0],i[1][0],i[0][1],i[1][1],curx,cury+speed,width,height)) and (i!=((curx,width),(cury,height)))):
				return False
	return True

player_face='up'

def move(direction,spritex,spritey,speed):
	ogx=spritex
	ogy=spritey
	global player_face
	if direction:
		if direction == K_w:
			spritey-=speed
			player_face='up'
			rpg_animations.animateMovement('up')
		elif direction == K_s:
			spritey+=speed
			player_face='down'
			rpg_animations.animateMovement('down')
		if direction == K_a:
			spritex-=speed
			player_face='left'
			rpg_animations.animateMovement('left')
		elif direction == K_d:
			spritex+=speed
			player_face='right'
			rpg_animations.animateMovement('right')
	return legalMovement(ogx,ogy,spritex,spritey)

active_projectile=[]
def projectile(direction):
	if(direction=='up'):
		active_projectile.append([rpg_classes.hero.x+(rpg_classes.hero.width/2),rpg_classes.hero.y+(rpg_classes.hero.height/2),rpg_classes.hero.projectile_speed,'up'])
	elif(direction=='down'):
		active_projectile.append([rpg_classes.hero.x+(rpg_classes.hero.width/2),rpg_classes.hero.y+(rpg_classes.hero.height/2),rpg_classes.hero.projectile_speed,'down'])
	elif(direction=='left'):
		active_projectile.append([rpg_classes.hero.x+(rpg_classes.hero.width/2),rpg_classes.hero.y+(rpg_classes.hero.height/2),rpg_classes.hero.projectile_speed,'left'])
	elif(direction=='right'):
		active_projectile.append([rpg_classes.hero.x+(rpg_classes.hero.width/2),rpg_classes.hero.y+(rpg_classes.hero.height/2),rpg_classes.hero.projectile_speed,'right'])

transparentSurface=pygame.Surface((1000,700))
transparentSurface.set_alpha(128)
transparentSurface.fill((153,0,0))

def displayLoot():
	for i in loot:
		DISPLAYSURF.blit(i[0]['default_sprite'],(i[1],i[2]))
		if(i[0]['type']=='life'):
			if(interaction(rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height,i[1],i[2],i[0]['width'],i[0]['height'])):
				loot.remove(i)
				rpg_classes.hero.health+=1
				rpg_classes.hero.debuf['fire']=0
		if(interaction(i[1],i[2],i[0]['width'],i[0]['height'],rpg_classes.hero.x,rpg_classes.hero.y,rpg_classes.hero.width,rpg_classes.hero.height)):
			text_gap=15
			item_name_label_text=i[0]['name']
			item_name_label=font.render(item_name_label_text,1,(255,255,0))
			item_rarity_label_text=i[0]['rarity']
			item_rarity_label=font.render(item_rarity_label_text,1,(255,255,0))
			item_type_label_text='Type: '+i[0]['type']
			item_type_label=font.render(item_type_label_text,1,(255,255,0))
			if(i[0]['type']=='bow' or i[0]['type']=='axe' or i[0]['type']=='gun' or i[0]['type']=='sword'):
				item_damage_label_text='Damage: '+str(i[0]['damage'])
				if(i[0]['damage']>=rpg_classes.hero.weapon['damage']):
					diffDamage=i[0]['damage']-rpg_classes.hero.weapon['damage']
					change_in_damage_label_text='+'+str(diffDamage)
					change_in_damage_label=font.render(change_in_damage_label_text,1,(0,255,0))
				else:
					diffDamage=i[0]['damage']-rpg_classes.hero.weapon['damage']
					change_in_damage_label_text=str(diffDamage)
					change_in_damage_label=font.render(change_in_damage_label_text,1,(255,0,0))
				item_attack_speed_label_text='Attack Speed: '+str(i[0]['attack_speed'])
				if(i[0]['attack_speed']>rpg_classes.hero.weapon['attack_speed']):
					diffattack_speed=i[0]['attack_speed']-rpg_classes.hero.weapon['attack_speed']
					change_in_attack_speed_label_text='+'+str(diffattack_speed)
					change_in_attack_speed_label=font.render(change_in_attack_speed_label_text,1,(255,0,0))
				else:
					diffattack_speed=i[0]['attack_speed']-rpg_classes.hero.weapon['attack_speed']
					change_in_attack_speed_label_text='-'+str(diffattack_speed)
					change_in_attack_speed_label=font.render(change_in_attack_speed_label_text,1,(0,255,0))
				if(i[0]['type']=='bow' or i[0]['type']=='gun'):
					item_spec_label_text='Projectile Speed: '+str(i[0]['spec'])
				else:
					item_spec_label_text='Attack Range: '+str(i[0]['spec'])
				if(i[0]['spec']>=rpg_classes.hero.weapon['spec']):
					diffspec=i[0]['spec']-rpg_classes.hero.weapon['spec']
					change_in_spec_label_text='+'+str(diffspec)
					change_in_spec_label=font.render(change_in_spec_label_text,1,(0,255,0))
				else:
					diffspec=i[0]['spec']-rpg_classes.hero.weapon['spec']
					change_in_spec_label_text=str(diffspec)
					change_in_spec_label=font.render(change_in_spec_label_text,1,(255,0,0))
				item_damage_label=font.render(item_damage_label_text,1,(255,255,0))
				item_attack_speed_label=font.render(item_attack_speed_label_text,1,(255,255,0))
				item_spec_label=font.render(item_spec_label_text,1,(255,255,0))
				in_game_menu_surface=pygame.Surface((240,100))
				in_game_menu_surface.set_alpha(128)
				in_game_menu_surface.fill((30,30,30))
				in_game_menu_x=i[1]
				in_game_menu_y=i[2]
				if(i[1]+240>1000):
					in_game_menu_x=740
				if(i[2]+100>700):
					in_game_menu_y=580
				DISPLAYSURF.blit(in_game_menu_surface,(in_game_menu_x+20,in_game_menu_y+20))
				DISPLAYSURF.blit(item_name_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap))
				DISPLAYSURF.blit(item_rarity_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*2))
				DISPLAYSURF.blit(item_type_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*3))
				DISPLAYSURF.blit(item_damage_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*4))
				DISPLAYSURF.blit(change_in_damage_label,(in_game_menu_x+20+text_gap+190,in_game_menu_y+10+text_gap*4))
				DISPLAYSURF.blit(item_attack_speed_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*5))
				DISPLAYSURF.blit(change_in_attack_speed_label,(in_game_menu_x+20+text_gap+190,in_game_menu_y+10+text_gap*5))
				DISPLAYSURF.blit(item_spec_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*6))
				DISPLAYSURF.blit(change_in_spec_label,(in_game_menu_x+20+text_gap+190,in_game_menu_y+10+text_gap*6))

			elif(i[0]['type']=='helmet' or i[0]['type']=='chest' or i[0]['type']=='pants'):
				item_armor_label_text='Armor: '+str(i[0]['armor'])
				item_armor_label=font.render(item_armor_label_text,1,(255,255,0))
				if(i[0]['armor']>=rpg_classes.hero.helmet['armor'] and i[0]['type']=='helmet'):
					diffarmor=i[0]['armor']-rpg_classes.hero.helmet['armor']
					change_in_armor_label_text='+'+str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(0,255,0))
				elif(i[0]['armor']<rpg_classes.hero.helmet['armor'] and i[0]['type']=='helmet'):
					diffarmor=i[0]['armor']-rpg_classes.hero.helmet['armor']
					change_in_armor_label_text=str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(255,0,0))
				if(i[0]['armor']>=rpg_classes.hero.chest['armor'] and i[0]['type']=='chest'):
					diffarmor=i[0]['armor']-rpg_classes.hero.chest['armor']
					change_in_armor_label_text='+'+str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(0,255,0))
				elif(i[0]['armor']<rpg_classes.hero.chest['armor'] and i[0]['type']=='chest'):
					diffarmor=i[0]['armor']-rpg_classes.hero.chest['armor']
					change_in_armor_label_text=str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(255,0,0))
				if(i[0]['armor']>=rpg_classes.hero.pants['armor'] and i[0]['type']=='pants'):
					diffarmor=i[0]['armor']-rpg_classes.hero.pants['armor']
					change_in_armor_label_text='+'+str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(0,255,0))
				elif(i[0]['armor']<rpg_classes.hero.pants['armor'] and i[0]['type']=='pants'):
					diffarmor=i[0]['armor']-rpg_classes.hero.pants['armor']
					change_in_armor_label_text=str(diffarmor)
					change_in_armor_label=font.render(change_in_armor_label_text,1,(255,0,0))
				in_game_menu_surface=pygame.Surface((240,70))
				in_game_menu_surface.set_alpha(128)
				in_game_menu_surface.fill((30,30,30))
				in_game_menu_x=i[1]
				in_game_menu_y=i[2]
				if(i[1]+240>1000):
					in_game_menu_x=740
				if(i[2]+100>700):
					in_game_menu_y=680
				DISPLAYSURF.blit(in_game_menu_surface,(in_game_menu_x+20,in_game_menu_y+20))
				DISPLAYSURF.blit(item_name_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap))
				DISPLAYSURF.blit(item_rarity_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*2))
				DISPLAYSURF.blit(item_type_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*3))
				DISPLAYSURF.blit(item_armor_label,(in_game_menu_x+20+text_gap,in_game_menu_y+10+text_gap*4))
				DISPLAYSURF.blit(change_in_armor_label,(in_game_menu_x+20+text_gap+190,in_game_menu_y+10+text_gap*4))

Black = (230,230,230)
def inventory():
	x_val=0
	y_val=0
	pygame.draw.rect(DISPLAYSURF, Black, (475,40,70,70))#HELMET
	pygame.draw.rect(DISPLAYSURF, Black, (475,130,70,70))#Chest
	pygame.draw.rect(DISPLAYSURF, Black, (475,220,70,70))#greaves
	pygame.draw.rect(DISPLAYSURF, Black, (390,130,70,70))#gloves
	pygame.draw.rect(DISPLAYSURF, Black, (560,130,70,70))#weapon
	DISPLAYSURF.blit(rpg_classes.hero.weapon['default_sprite'],(560+((70-rpg_classes.hero.weapon['width'])*.5),130+((70-rpg_classes.hero.weapon['height'])*.5)))
	DISPLAYSURF.blit(rpg_classes.hero.helmet['default_sprite'],(475+((70-rpg_classes.hero.helmet['width'])*.5),40+((70-rpg_classes.hero.helmet['height'])*.5)))
	DISPLAYSURF.blit(rpg_classes.hero.chest['default_sprite'],(475+((70-rpg_classes.hero.chest['width'])*.5),130+((70-rpg_classes.hero.chest['height'])*.5)))
	DISPLAYSURF.blit(rpg_classes.hero.pants['default_sprite'],(475+((70-rpg_classes.hero.pants['width'])*.5),220+((70-rpg_classes.hero.pants['height'])*.5)))
	
	for y in range(4):
		for x in range(11): 
			pygame.draw.rect(DISPLAYSURF, Black, (65+(80*x),340+(80*y),70,70))

	for i in range(len(rpg_classes.hero.inventory_list)):
		DISPLAYSURF.blit(rpg_classes.hero.inventory_list[i]['default_sprite'], (65+(80*x_val)+((70-rpg_classes.hero.weapon['width'])*.5),340+(80*y_val)+(70-rpg_classes.hero.weapon['height'])*.5))	
		x_val+=1
		if(x_val>11):
			x_val=0
			y_val+=1

def resetObstacles():
	rpg_class_select.obstacle_locations=[]
	rpg_class_select.obstacles=[((-100,100+boundary_width),(-100,map_height+100)),\
	((-100,map_width+100),(-100,100+boundary_width)),\
	(((map_width - boundary_width),map_width+100),(-100,map_height+100)),\
	((-100,map_width+100),((map_height - boundary_width),map_height+100))]

def populateObstacles():
	obstacle_width=50
	ob_num=random.randint(0,5)
	for i in range(ob_num):
		randx=random.randint(200,800)
		randy=random.randint(200,500)
		rpg_class_select.obstacle_locations.append(((randx,obstacle_width),(randy,obstacle_width)))
	rpg_class_select.obstacles.extend(rpg_class_select.obstacle_locations)

def displayObstacles():
	for i in rpg_class_select.obstacle_locations:
		DISPLAYSURF.blit(rpg_file_def.rock,(i[0][0],i[1][0]))

def tickDOTs():
	for i in rpg_classes.hero.debuf:
		if(i=='fire'):
			if(rpg_classes.hero.debuf['fire']>0):
				if(rpg_classes.hero.animate_debuf_state==0):
					DISPLAYSURF.blit(rpg_file_def.fire_sprite_1,(rpg_classes.hero.x,rpg_classes.hero.y+(rpg_classes.hero.height-20)))
					rpg_classes.hero.animate_debuf_state+=1
				else:
					DISPLAYSURF.blit(rpg_file_def.fire_sprite_2,(rpg_classes.hero.x,rpg_classes.hero.y+(rpg_classes.hero.height-20)))
					rpg_classes.hero.animate_debuf_state-=1
				rpg_classes.hero.debuf['fire']-=1
				rpg_classes.hero.health-=.01*((100-rpg_classes.hero.armor)/float(100))