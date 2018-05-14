
from stores.models.store_db import StoresDB
from utils.generator.code_generator import CodeGenerator
from app import cache

cache.clear()


amazon_description = """Amazon is an American electronic commerce and cloud computing company based in Seattle, Washington that was founded by Jeff Bezos on July 5, 1994. The tech giant is the largest Internet retailer in the world as measured by revenue and market capitalization, and second largest after Alibaba Group in terms of total sales"""

amazon_uk = StoresDB(store_name='Amazon', store_id= CodeGenerator().generate_hex(), url_prefix='https://www.amazon.co.uk', tag_name='span',
                     description=amazon_description, query={'id': 'priceblock_dealprice'})
amazon_uk.predefined_store = True


ebay_description = """EBay Inc. is a multinational e-commerce corporation based in San Jose, California that facilitates consumer-to-consumer and business-to-consumer sales through its website. <br><br>EBay was founded by Pierre Omidyar in 1995, and became a notable success story of the dot-com bubble. <br><br>eBay is a multibillion-dollar business with operations in about 30 countries, as of 2011. The company manages eBay.com, an online auction and shopping website in which people and businesses buy and sell a wide variety of goods and services worldwide. The website is free to use for buyers, but sellers are charged fees for listing items after a limited number of free listings, and again when those items are sold"""
ebay = StoresDB(store_name="Ebay", store_id=CodeGenerator().generate_hex(), url_prefix='https://www.ebay.com',
                tag_name="span", description=ebay_description, query={"itemprop": "price"}
                )

ebay.predefined_store = True



home_design_description = """A home design store that specialise in selling furniture, chairs, etc"""
home_design = StoresDB(store_name="Home design", store_id=CodeGenerator().generate_hex(), url_prefix='https://inhome-design.co.uk',
                tag_name="span", description=home_design_description, query={"class": "price", "itemprop":"price"},
                )
home_design.predefined_store = True


tesco_direct_description = """Tesco was founded in 1919 and is a British multinational grocery and general merchandise retailer with headquarters in Welwyn Garden City, Hertfordshire, England, United Kingdom.[3] It is the third-largest retailer in the world measured by profits[4][5] and ninth-largest retailer in the world measured by revenues. It has stores in 12 countries across Asia and Europe and is the grocery market leader in the UK (where it has a market share of around 28.4%), Ireland, Hungary[6] and Thailand """
tesco = StoresDB(store_name="tesco", store_id=CodeGenerator().generate_hex(), url_prefix='https://www.tesco.com',
                tag_name="span", description=tesco_direct_description, query={"itemprop":"price"},
                )

tesco.predefined_store = True


game_description = """Game Digital plc is the parent company of Game Retail Limited, a British video game company that trades under the Game brand, stylised as GAME."""
game = StoresDB(store_name="Game", store_id=CodeGenerator().generate_hex(), url_prefix='https://www.game.co.uk',
                tag_name="span", description=game_description, query={"class":"price"},
                )
game.predefined_store = True



print('Clearing database, please wait...')
StoresDB.objects.delete()
print('Done...')
print("Please wait, populating database..")

amazon_uk.save()
ebay.save()
home_design.save()
tesco.save()
game.save()
print('Your database has now been populated')



