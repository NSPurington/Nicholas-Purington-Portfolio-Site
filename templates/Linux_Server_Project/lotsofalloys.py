from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import BaseMetal, Base, Alloy, User
 
engine = create_engine('psql:///metalcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


#Types for Aluminium
basemetal1 = BaseMetal(name = "Aluminium", user_id = "0")

session.add(basemetal1)
session.commit()

alloy1 = Alloy(name = "Magnalium", description = "Magnalium is an aluminium alloy with magnesium and small amounts of nickel and tin.[1] Some alloys, intended for particular uses at the cost of poor corrosion resistance, may consist of up to 50% magnesium. It finds use in engineering and pyrotechnics.",  basemetal = basemetal1, user_id = "0")

session.add(alloy1)
session.commit()


#Types for Chromium
basemetal2 = BaseMetal(name = "Chromium", user_id = "0")

session.add(basemetal2)
session.commit()

alloy2 = Alloy(name = "Nichrome", description = "Nichrome (NiCr, nickel-chrome, chrome-nickel, etc.) is any of various alloys of nickel, chromium, and often iron (and possibly other elements). The most common usage is as resistance wire, although they are also used in some dental restorations (fillings) and in a few other applications.",  basemetal = basemetal2, user_id = "0")

session.add(alloy2)
session.commit()


#Types for Cobalt
basemetal3 = BaseMetal(name = "Cobalt", user_id = "0")

session.add(basemetal3)
session.commit()

alloy3 = Alloy(name = "Stellite", description = "Stellite alloy is a range of cobalt-chromium alloys designed for wear resistance. It may also contain tungsten or molybdenum and a small but important amount of carbon.",  basemetal = basemetal3)

session.add(alloy3)
session.commit()


#Types for Copper
basemetal4 = BaseMetal(name = "Copper", user_id = "0")

session.add(basemetal4)
session.commit()

alloy4 = Alloy(name = "Brass", description = "Brass is a metallic alloy that is made of copper and zinc. The proportions of zinc and copper can vary to create different types of brass alloys with varying mechanical and electrical properties.[1] It is a substitutional alloy: atoms of the two constituents may replace each other within the same crystal structure.",  basemetal = basemetal4, user_id = "0")

session.add(alloy4)
session.commit()

#Types for Gold
basemetal5 = BaseMetal(name = "Gold", user_id = "0")

session.add(basemetal5)
session.commit()

alloy5 = Alloy(name = "Rose Gold", description = "Rose gold is a gold-copper alloy[5] widely used for specialized jewelry. Rose gold, also known as pink gold and red gold, was popular in Russia at the beginning of the nineteenth century, and was also known as Russian gold, although this term is now obsolete. Rose gold jewelry is becoming more popular in the 21st century, and is commonly used for wedding rings, bracelets, and other jewelry.",  basemetal = basemetal5, user_id = "0")

session.add(alloy5)
session.commit()

#Types for Iron
basemetal6 = BaseMetal(name = "Iron", user_id = "0")

session.add(basemetal6)
session.commit()

alloy6 = Alloy(name = "Cast Iron", description = "Cast iron is a group of iron-carbon alloys with a carbon content greater than 2%.[1] Its usefulness derives from its relatively low melting temperature. The alloy constituents affect its colour when fractured: white cast iron has carbide impurities which allow cracks to pass straight through, grey cast iron has graphite flakes which deflect a passing crack and initiate countless new cracks as the material breaks, and ductile cast iron has spherical graphite 'nodules' which stop the crack from further progressing.",  basemetal = basemetal6, user_id = "0")

session.add(alloy6)
session.commit()

#Types for Lead
basemetal7 = BaseMetal(name = "Lead", user_id = "0")

session.add(basemetal7)
session.commit()

alloy7 = Alloy(name = "Solder", description = "Solder is a fusible metal alloy used to create a permanent bond between metal workpieces. The word solder comes from the Middle English word soudur, via Old French solduree and soulder, from the Latin solidare, meaning 'to make solid'.[3] In fact, solder must first be melted in order to adhere to and connect the pieces together after cooling, which requires that an alloy suitable for use as solder have a lower melting point than the pieces being joined. The solder should also be resistant to oxidative and corrosive effects that would degrade the joint over time. Solder used in making electrical connections also needs to have favorable electrical characteristics.",  basemetal = basemetal7, user_id = "0")

session.add(alloy7)
session.commit()


#Types for Nickel
basemetal8 = BaseMetal(name = "Nickel", user_id = "0")

session.add(basemetal8)
session.commit()

alloy8 = Alloy(name = "Alumel", description = "Alumel is an alloy consisting of approximately 95% nickel, 2% aluminum, 2% manganese, and 1% silicon. This magnetic alloy is used for thermocouples and thermocouple extension wire. Alumel is a registered trademark of Concept Alloys, Inc.",  basemetal = basemetal8, user_id = "0")

session.add(alloy8)
session.commit()


#Types for Silver
basemetal9 = BaseMetal(name = "Silver", user_id = "0")

session.add(basemetal9)
session.commit()

alloy9 = Alloy(name = "Platinum Sterling", description = "Platinum Sterling is a registered trademark name of ABI Precious Metals, Inc. The trademark covers a range of alloys whose primary constituents are platinum and silver, primarily used in jewellery.[1] The range of Platinum Sterling alloys was developed in 2003 by Marc Robinson, and its solder was created by Chuck Bennett.",  basemetal = basemetal9, user_id = "0")

session.add(alloy9)
session.commit()


#Types for Tin
basemetal10 = BaseMetal(name = "Tin", user_id = "0")

session.add(basemetal10)
session.commit()

alloy10 = Alloy(name = "Pewter", description = "Pewter is a malleable metal alloy. It is traditionally composed of 85-99 percent tin, mixed with copper, antimony, bismuth, and sometimes lead, although the use of lead is less common today. Silver is also sometimes used. Copper and antimony act as hardeners while lead is more common in the lower grades of pewter, which have a bluish tint. Pewter had a low melting point, depending on the exact mixture of metals. The word pewter is probably a variation of the word spelter, a term for zink alloys (originally a colloquial name for zinc).",  basemetal = basemetal10, user_id = "0")

session.add(alloy10)
session.commit()


#Add User
newUser1 = User(username = "Nick Purington", email = "nickpurington@gmail.com", picture = "https://lh4.googleusercontent.com/-fUhBCupxjJA/AAAAAAAAAAI/AAAAAAAAAAk/K60p8iirx6E/photo.jpg")

session.add(newUser1)
session.commit()


print "Added new alloys! Ready to get started"
