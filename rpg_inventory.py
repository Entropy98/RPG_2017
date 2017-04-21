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

def run():
	cur_inventory_select=(11*rpg_mechanics.item_selectY)+rpg_mechanics.item_selectX
	rpg_mechanics.double_press_timer+=1
	pygame.draw.rect(DISPLAYSURF,(200,200,200),(0,0,1000,700))
	text_gap=30
	rpg_mechanics.inventory()

	hero_stat_menu_x=100
	hero_stat_menu_y=50
	armor_label_text='Armor: '+str(rpg_classes.hero.armor)
	damage_label_text='Damage: '+str(rpg_classes.hero.damage)
	if(rpg_classes.hero.hero_type=='Warrior'):
		spec_label_text='Melee Range: '+str(rpg_classes.hero.melee_range)
	else:
		spec_label_text='Projectile Speed: '+str(rpg_classes.hero.projectile_speed)
	class_label_text=rpg_classes.hero.hero_type
	health_label_text='health: '+str(rpg_classes.hero.health)
	attack_speed_label_text='Attack Speed: '+str(rpg_classes.hero.attack_speed)
	armor_label=font.render(armor_label_text,1,(0,0,0))
	damage_label=font.render(damage_label_text,1,(0,0,0))
	spec_label=font.render(spec_label_text,1,(0,0,0))
	class_label=font.render(class_label_text,1,(0,0,0))
	health_label=font.render(health_label_text,1,(0,0,0))
	attack_speed_label=font.render(attack_speed_label_text,1,(0,0,0))

	DISPLAYSURF.blit(class_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap))
	DISPLAYSURF.blit(health_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap*2))
	DISPLAYSURF.blit(armor_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap*3))
	DISPLAYSURF.blit(damage_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap*4))
	DISPLAYSURF.blit(spec_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap*5))
	DISPLAYSURF.blit(attack_speed_label,(hero_stat_menu_x+20+text_gap,hero_stat_menu_y+10+text_gap*6))

	if(rpg_mechanics.item_selectX  == 0 and rpg_mechanics.item_selectY == 0):
		DISPLAYSURF.blit(rpg_file_def.inventory_select,(65,340))
	for event in pygame.event.get():
		if (event.type==QUIT):
			pygame.quit()
			sys.exit()

	if(len(rpg_classes.hero.inventory_list)>cur_inventory_select):
		cur_select_item=rpg_classes.hero.inventory_list[cur_inventory_select]
	else:
		cur_select_item=None

	if(cur_select_item!=None):
		stat_menu_x=650
		stat_menu_y=50
		item_name_label_text=cur_select_item['name']
		item_name_label=font.render(item_name_label_text,1,(0,0,0))
		item_rarity_label_text=cur_select_item['rarity']
		item_rarity_label=font.render(item_rarity_label_text,1,(0,0,0))
		item_type_label_text='Type: '+cur_select_item['type']
		item_type_label=font.render(item_type_label_text,1,(0,0,0))
		if(cur_select_item['type']=='bow' or cur_select_item['type']=='axe' or cur_select_item['type']=='gun' or cur_select_item['type']=='sword'):
			item_damage_label_text='Damage: '+str(cur_select_item['damage'])
			if(cur_select_item['damage']>=rpg_classes.hero.weapon['damage']):
				diffDamage=cur_select_item['damage']-rpg_classes.hero.weapon['damage']
				change_in_damage_label_text='+'+str(diffDamage)
				change_in_damage_label=font.render(change_in_damage_label_text,1,(102,153,0))
			else:
				diffDamage=cur_select_item['damage']-rpg_classes.hero.weapon['damage']
				change_in_damage_label_text=str(diffDamage)
				change_in_damage_label=font.render(change_in_damage_label_text,1,(255,0,0))
			item_attack_speed_label_text='Attack Speed: '+str(cur_select_item['attack_speed'])
			if(cur_select_item['attack_speed']>rpg_classes.hero.weapon['attack_speed']):
				diffattack_speed=cur_select_item['attack_speed']-rpg_classes.hero.weapon['attack_speed']
				change_in_attack_speed_label_text='+'+str(diffattack_speed)
				change_in_attack_speed_label=font.render(change_in_attack_speed_label_text,1,(255,0,0))
			else:
				diffattack_speed=cur_select_item['attack_speed']-rpg_classes.hero.weapon['attack_speed']
				change_in_attack_speed_label_text=str(diffattack_speed)
				change_in_attack_speed_label=font.render(change_in_attack_speed_label_text,1,(102,153,0))
			if(cur_select_item['type']=='bow' or cur_select_item['type']=='gun'):
				item_spec_label_text='Projectile Speed: '+str(cur_select_item['spec'])
			else:
				item_spec_label_text='Attack Range: '+str(cur_select_item['spec'])
			if(cur_select_item['spec']>=rpg_classes.hero.weapon['spec']):
				diffspec=cur_select_item['spec']-rpg_classes.hero.weapon['spec']
				change_in_spec_label_text='+'+str(diffspec)
				change_in_spec_label=font.render(change_in_spec_label_text,1,(102,153,0))
			else:
				diffspec=cur_select_item['spec']-rpg_classes.hero.weapon['spec']
				change_in_spec_label_text=str(diffspec)
				change_in_spec_label=font.render(change_in_spec_label_text,1,(255,0,0))
			item_damage_label=font.render(item_damage_label_text,1,(0,0,0))
			item_attack_speed_label=font.render(item_attack_speed_label_text,1,(0,0,0))
			item_spec_label=font.render(item_spec_label_text,1,(0,0,0))
			DISPLAYSURF.blit(item_name_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap))
			DISPLAYSURF.blit(item_rarity_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*2))
			DISPLAYSURF.blit(item_type_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*3))
			DISPLAYSURF.blit(item_damage_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*4))
			DISPLAYSURF.blit(change_in_damage_label,(stat_menu_x+20+text_gap+190,stat_menu_y+10+text_gap*4))
			DISPLAYSURF.blit(item_attack_speed_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*5))
			DISPLAYSURF.blit(change_in_attack_speed_label,(stat_menu_x+20+text_gap+190,stat_menu_y+10+text_gap*5))
			DISPLAYSURF.blit(item_spec_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*6))
			DISPLAYSURF.blit(change_in_spec_label,(stat_menu_x+20+text_gap+190,stat_menu_y+10+text_gap*6))

		elif(cur_select_item['type']=='helmet' or cur_select_item['type']=='chest' or cur_select_item['type']=='pants'):
			item_armor_label_text='Armor: '+str(cur_select_item['armor'])
			item_armor_label=font.render(item_armor_label_text,1,(0,0,0))
			change_in_armor_label=rpg_file_def.place_holder_sprite
			if(cur_select_item['armor']>=rpg_classes.hero.helmet['armor'] and cur_select_item['type']=='helmet'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.helmet['armor']
				change_in_armor_label_text='+'+str(diffarmor)
				change_in_armor_label=font.render(change_in_armor_label_text,1,(102,153,0))
			elif(cur_select_item['armor']<rpg_classes.hero.helmet['armor'] and cur_select_item['type']=='helmet'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.helmet['armor']
				change_in_armor_label_text=str(diffarmor)
				change_in_armor_label=font.render(change_in_armor_label_text,1,(255,0,0))
			if(cur_select_item['armor']>=rpg_classes.hero.chest['armor'] and cur_select_item['type']=='chest'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.chest['armor']
				change_in_armor_label_text='+'+str(diffarmor)
				change_in_armor_label=font.render(change_in_armor_label_text,1,(102,153,0))
			elif(cur_select_item['armor']<rpg_classes.hero.chest['armor'] and cur_select_item['type']=='chest'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.chest['armor']
				change_in_armor_label_text=str(diffarmor)
				change_in_armor_label=font.render(change_in_armor_label_text,1,(255,0,0))
			if(cur_select_item['armor']>=rpg_classes.hero.pants['armor'] and cur_select_item['type']=='pants'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.pants['armor']
				change_in_armor_label_text='+'+str(diffarmor)
				change_in_armor_label=font.render(change_in_armor_label_text,1,(102,153,0))
			elif(cur_select_item['armor']<rpg_classes.hero.pants['armor'] and cur_select_item['type']=='pants'):
				diffarmor=cur_select_item['armor']-rpg_classes.hero.pants['armor']
				change_in_armor_label_text=str(diffarmor)
			DISPLAYSURF.blit(item_name_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap))
			DISPLAYSURF.blit(item_rarity_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*2))
			DISPLAYSURF.blit(item_type_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*3))
			DISPLAYSURF.blit(item_armor_label,(stat_menu_x+20+text_gap,stat_menu_y+10+text_gap*4))
			DISPLAYSURF.blit(change_in_armor_label,(stat_menu_x+20+text_gap+190,stat_menu_y+10+text_gap*4))

	keys=pygame.key.get_pressed()
	if(rpg_mechanics.double_press_timer>rpg_mechanics.double_press_time):
		if(keys[K_i]):
			rpg_mechanics.inventory_menu=False
			rpg_mechanics.double_press_timer=0
		if(keys[K_d]):
			#move to the right one space
			rpg_mechanics.item_selectX+=1
			if (rpg_mechanics.item_selectX > 10):
				rpg_mechanics.item_selectX=0
			rpg_mechanics.double_press_timer=0
		if(keys[K_a]):
			#move to the left one space
			rpg_mechanics.item_selectX-=1
			if (rpg_mechanics.item_selectX < 0):
				rpg_mechanics.item_selectX=10
			rpg_mechanics.double_press_timer=0
		if(keys[K_w]):
			#move up one space
			rpg_mechanics.item_selectY-=1
			if (rpg_mechanics.item_selectY < 0):
				rpg_mechanics.item_selectY=3
			rpg_mechanics.double_press_timer=0
		if(keys[K_s]):
			#move down one space
			rpg_mechanics.item_selectY+=1
			if (rpg_mechanics.item_selectY > 3):
				rpg_mechanics.item_selectY=0
			rpg_mechanics.double_press_timer=0
		if(keys[K_e]):
			if(cur_select_item!=None):
				if(cur_select_item['type']=='bow' or cur_select_item['type']=='axe' or cur_select_item['type']=='gun' or cur_select_item['type']=='sword'):
					oldItem=rpg_classes.hero.weapon
					rpg_classes.hero.addWeapon(cur_select_item)
					rpg_classes.hero.inventory_list.remove(cur_select_item)
					rpg_classes.hero.inventory_list.append(oldItem)
				elif(cur_select_item['type']=='helmet'):
					oldItem=rpg_classes.hero.helmet
					rpg_classes.hero.addHelmet(cur_select_item)
					rpg_classes.hero.inventory_list.remove(cur_select_item)
					rpg_classes.hero.inventory_list.append(oldItem)
				elif(cur_select_item['type']=='chest'):
					oldItem=rpg_classes.hero.chest
					rpg_classes.hero.addChest(cur_select_item)
					rpg_classes.hero.inventory_list.remove(cur_select_item)
					rpg_classes.hero.inventory_list.append(oldItem)
				elif(cur_select_item['type']=='pants'):
					oldItem=rpg_classes.hero.pants
					rpg_classes.hero.addPants(cur_select_item)
					rpg_classes.hero.inventory_list.remove(cur_select_item)
					rpg_classes.hero.inventory_list.append(oldItem)
				rpg_mechanics.double_press_timer=0
		if(keys[K_r]):
			if(cur_select_item!=None):
				rpg_mechanics.loot.append([cur_select_item,rpg_classes.hero.x,rpg_classes.hero.y])
				rpg_classes.hero.inventory_list.remove(cur_select_item)
				rpg_mechanics.double_press_timer=0
		
	if (0 <= rpg_mechanics.item_selectY < 5 and rpg_mechanics.item_selectX > -1):
		DISPLAYSURF.blit(rpg_file_def.inventory_select,(65+(80*rpg_mechanics.item_selectX),340+(80*rpg_mechanics.item_selectY)))
	
	rpg_animations.animateWeapon()	
	pygame.display.update()
	fpsClock.tick(FPS)