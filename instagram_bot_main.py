from selenium import webdriver
from time import sleep


####################################################################################################
def esNumero(char):
		if char == '0':
			return True
		if char == '1':
			return True
		if char == '2':
			return True
		if char == '3':
			return True
		if char == '4':
			return True
		if char == '5':
			return True
		if char == '6':
			return True
		if char == '7':
			return True
		if char == '8':
			return True
		if char == '9':
			return True
		return False 

####################################################################################################

def toInt(string):
	res = ''
	for letter in string:
		if esNumero(letter):
			res = res + letter
		elif letter == "k" or letter == "K":
			res = res + '0'
			res = res + '0'
			res = res + '0'
			return int(res)
		elif letter == ' ':
			return int(res)

####################################################################################################
	

class InstaBot:

	## Se logea en Instagram
	def __init__(self, username, pw):
	
		self.username = username
		self.pw = pw
		self.driver = webdriver.Chrome()


		# Entro a Instagram
		self.driver.get("https://instagram.com")
		sleep(2)

		# Ingreso usuario
		self.driver.find_element_by_xpath("//input[@name=\"username\"]")\
			 .send_keys(username)

		# Ingreso password
		self.driver.find_element_by_xpath("//input[@name=\"password\"]")\
			 .send_keys(pw)

		# Clickeo submit
		self.driver.find_element_by_xpath('//button[@type="submit"]')\
			 .click()
		sleep(8)

		# Clickeo not now
		self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
			 .click()
		sleep(2)

	####################################################################################################

	# Devuelve los non_important del user pasado como parametro
	def get_nonimportant(self,user):

		# Entro al perfil del cliente
		self.driver.get("https://www.instagram.com/{}/".format(user))
		sleep(3)

		# Abro sus seguidos
		self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
        	.click()
		sleep(2)

		# Consigo la python list con sus seguidos (se cierra seguidores)
		followers = self.get_users()

		# Consigo la lista de sus non-importants
		non_important = []
		for user in followers:
			if self.sigueAMas(user):
				non_important.append(user)
		print(non_important)


	####################################################################################################	
	
	# Devuelve los nono_followers del user pasado como parametro
	def get_nonfollowers(self, user):

		# Entro al perfil del cliente
		self.driver.get("https://www.instagram.com/{}/".format(user))
		sleep(3)

		# Abro sus seguidos
		self.driver.find_element_by_xpath("//a[contains(@href,'/following')]")\
        	.click()
		sleep(2)

		# Consigo la python list con sus seguidos (se cierra seguidos)
		following = self.get_users()
		print("El usuario sigue a ",len(following), " personas")

		# Abro seguidores
		self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
			.click()
		sleep(2)

		# Consigo la python list con sus seguidores (se cierra seguidores)
		followers = self.get_users()
		print("Al usuario lo siguen ", len(followers), " personas")

		# Consigo e imprimo la lista de sus non-followers
		no_following_back = [user for user in following if user not in followers]
		print('\n')
		print("Los putos que no me siguen son:" + '\n')
		print(no_following_back)


        # Ignoro las sugerencias
		#sugs = self.driver.find_element_by_xpath('//h4[contains(text(), Suggestions)]')
		#self.driver.execute_script('arguments[0].scrollIntoView()', sugs)
		#sleep(1)



	####################################################################################################
	
	# Devuelve la lista de todos los usuarios que aparecen en la scroll_box previamente abierta
	def get_users(self):
		sleep(2)

		# Scroleo hasta el final del scroll_box (para cargar todas las cuentas) (minuto 8:55)
		scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]") # tomo el scroll_box
		last_ht, ht = 0, 1
		while last_ht != ht: # mientras pueda seguir bajando
			last_ht = ht 
			sleep(1)
			ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight);  
                return arguments[0].scrollHeight;
                """, scroll_box)	## Scroleamos una vez para abajo en el scroll_box y devolemos su nueva altura 
			sleep(8)

		# Creo la python list con los usuarios conseguidos
		links = scroll_box.find_elements_by_tag_name('a') # tomo todos los links que identifican a los usuarios pertenecientes al scroll_box
		names = [name.text for name in links if name.text != ''] # por cada link (usuario) extraigo su nombre
		#print(names)

		# Cierro scroll_box
		self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]")\
			.click()

		# Devuelvo a los seguidores
		return names

	####################################################################################################

	# Devuelve la cantidad de seguidores que tiene el perfil donde estas parado
	def get_followers_count(self):
		fc = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/header/section/ul/li[2]')
		return toInt(fc.text)


		####################################################################################################
	
	# Devuelve true si el user tiene mas seguidos que seguidores	
	def sigueAMas(self, user):
		
		# Entro al perfil del user a analizar
		self.driver.get("https://www.instagram.com/{}/".format(user))
		sleep(4)

		# Consigue la cantidad de seguidres
		cant_followers = self.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers')]".format(user))
		print(cant_followers.text)
		followers = toInt(cant_followers.text)
		print("Lo siguen  ", followers, " usuarios")

		# Consigue la cantidad de seguidos
		cant_following = self.driver.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(user))
		following = toInt(cant_following.text)
		print("Sigue a  ", following , " usuarios")

		if following > followers:
			return True
		else:
			return False
		


# Ejecucion
my_bot = InstaBot('lucaspioncetti', 'cacho123asd')
my_bot.driver.get("https://www.instagram.com/meluabr/")
my_bot.get_followers_count()




#my_bot.driver.get("https://www.instagram.com/{}/".format(user))
#sleep(3)


#cant_followers = my_bot.driver.find_element_by_xpath("//a[contains(@href,'/{}/followers')]".format(user))
#print(cant_followers.text)
#followers = toInt(cant_followers.text)
#print (followers)


#cant_following = my_bot.driver.find_element_by_xpath("//a[contains(@href,'/{}/following')]".format(user))
#print(cant_following.text)
#following = int(cant_following.text)

