
import os , django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myCoffee.settings')
django.setup()

from allproducts.models import product 
from faker import Faker
import random 







def seed_product(number):
	fake = Faker()
	prices = [20 , 30 , 15 , 22 , 55 , 40]
	images= os.listdir(os.chdir("../products_types"))
	 
	for _ in range(number):
		p=product(
			name = fake.name(),
			image = f'photos/2023/11/04/{images[random.randint(0,11)]}',
			price= prices[random.randint(0,5)],
			description=fake.text()
			)
		p.save()

	print(f'seed {number} producs successfully ')






	


#seed_brand(500)

seed_product(800)





