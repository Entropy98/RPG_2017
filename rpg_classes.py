import rpg_file_def
import rpg_items

class Player(object):
	def __init__(self,playerx,playery,sprite,height,width,health,hold_point_x,hold_point_y):
		self.x=playerx
		self.y=playery
		self.speed=7
		self.sprite=sprite
		self.height=height
		self.width=width
		self.health=health
		self.inventory_list=[]
		self.hold_point_x=hold_point_x
		self.hold_point_y=hold_point_y
		self.attack_speed=0
		self.common_loot=[]
		self.uncommon_loot=[]
		self.rare_loot=[]
		self.mythic_loot=[]
		self.melee_range=0
		self.projectile_speed=0
		self.armor=0
		self.room=0
		self.animate_weapon_state=0
		self.animate_debuf_state=0
		self.weapon=rpg_items.place_holder
		self.pants=rpg_items.place_holder
		self.helmet=rpg_items.place_holder
		self.chest=rpg_items.place_holder
		self.name=''
		self.debuf={'fire':0}
		self.score=0

	def addWeapon(self,weapon):
		self.weapon=weapon
		self.damage=self.weapon['damage']
		self.attack_speed=self.weapon['attack_speed']
		self.melee_range=self.weapon['spec']
		self.projectile_speed=self.weapon['spec']
		if(self.weapon['type']=='bow'):
			self.projectile=rpg_items.arrow
		elif(self.weapon['type']=='gun'):
			self.projectile=rpg_items.bullet

	def addHelmet(self,helmet):
		self.helmet=helmet
		self.armor=self.helmet['armor']+self.chest['armor']+self.pants['armor']

	def addChest(self,chest):
		self.chest=chest
		self.armor=self.helmet['armor']+self.chest['armor']+self.pants['armor']

	def addPants(self,pants):
		self.pants=pants
		self.armor=self.helmet['armor']+self.chest['armor']+self.pants['armor']

	def addClass(self,name):
		if(name=='warrior'):
			self.hero_type='Warrior'
			self.attack='melee'
			self.health=12
		if(name=='ranger'):
			self.hero_type='Ranger'
			self.attack='projectile'
			self.health=8

class Mob(object):
	def __init__(self,mobx,moby,sprite,height,width,speed,health):
		self.x=mobx
		self.y=moby
		self.sprite=sprite
		self.height=height
		self.width=width
		self.speed=speed
		self.health=health

class Boss(object):
	def __init__(self,sprite,height,width,speed,health,damage,attack_speed,projectile):
		self.sprite=sprite
		self.height=height
		self.width=width
		self.speed=speed
		self.health=health
		self.full_health=health
		self.damage=damage
		self.rank=1
		self.x=(1000/2)-(self.width/2)
		self.y=(700/2)-(self.height/2)
		self.attack_speed=attack_speed
		self.projectile=projectile
		self.projectile_speed=25
		self.loot=hero.mythic_loot
		self.loot_dropped=False
		self.defeated=False

hero=Player(475,475,rpg_file_def.hero_sprite_r1,47,37,10,40,25)

zombie=Mob(75,75,rpg_file_def.zombie_sprite_r1,47,37,2,100)
skeleton=Mob(75,75,rpg_file_def.skeleton_sprite_l1,47,35,4,50)
fire_elemental=Mob(75,75,rpg_file_def.fire_elemental_sprite_r1,30,25,2.5,25)

cookie_man=Boss(rpg_file_def.cookie_man_sprite_r1,47,36,3,10,3,30,rpg_file_def.cookie_sprite)
necromancer=Boss(rpg_file_def.necromancer_sprite_r,50,50,4.5,7,1*((100-hero.armor)/float(100)),30,rpg_file_def.arrow_right_sprite)