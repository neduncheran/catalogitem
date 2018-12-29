from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem, User

engine = create_engine('sqlite:///sportscatalog.db')
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

# Create dummy user
pic = "https://pbs.twimg.com/profile_images/"
pic += "2671170543/18debd694829ed78203a5a36dd364160_400x400.png"
User1 = User(name="Cheran", email="donchera@gmail.com",
             picture=pic)
session.add(User1)
session.commit()

# For Hockey
catalog1 = Catalog(user_id=1, name="Soccer")

session.add(catalog1)
session.commit()

# Hockey Equipment Hockey Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Soccer Ball",
                           description="Soccer equipment begins" +
                           " with the ball." +
                           " The football dates to ancient times. " +
                           "Sculls, pig's bladder, and round objects made " +
                           "from animal skins all served to be kicked in" +
                           " competitive, often violent and even " +
                           "ritualistic ways",
                           price="$2.99", category="Soccer", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Hockey Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Soccer Shoes",
                           description="Finding the right shoe is an " +
                           "important part of" +
                           " completing your soccer equipment package. " +
                           "In a few hundred" +
                           " years soccer footwear has gone from" +
                           " a pair of heavy leather" +
                           " boots made by Cornelius Johnson in" +
                           " 1525 and famously worn by " +
                           "King Henry VIII, to high-performing" +
                           " lightweight shoes specially" +
                           " designed for kicking, lifting, " +
                           "and manipulating the ball",
                           price="$2.99", category="Soccer", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# Hockey Equipment Shin pads
catalogitem3 = CatalogItem(user_id=1, title="Soccer Shin Guards",
                           description="This is a necessity for completing " +
                           "your soccer equipment package. " +
                           "We've all banged our shins at some " +
                           "time. It's surprisingly painful! " +
                           "Safety soccer equipment such as " +
                           "shin guards became more prominent " +
                           "after soccer rules (Laws of the Game" +
                           " - 1863) became a permanent fixture " +
                           "to protect against the brutal forces" +
                           " that soccer was famous for",
                           price="$2.99", category="Soccer", catalog=catalog1)

session.add(catalogitem3)
session.commit()

# Hockey Equipment Shin pads
catalogitem4 = CatalogItem(user_id=1, title="Soccer Football Kit Bag",
                           description="Soccer equipment includes " +
                           "the football kit bag. They're inexpensive, " +
                           "and handy for organizing and toting soccer " +
                           "equipment. So it is a must " +
                           "for professional teams. " +
                           "Nike offers a popular " +
                           "design at a reasonable" +
                           " price",
                           price="$2.99",
                           category="Soccer", catalog=catalog1)

session.add(catalogitem4)
session.commit()

# Hockey Equipment Shin pads
catalogitem5 = CatalogItem(user_id=1, title="Soccer Indoor Soccer Equipment",
                           description="Indoor and outdoor soccer" +
                           " equipment share similarities. " +
                           "The main difference is that " +
                           "indoor soccer is played in an" +
                           " enclosed space, as opposed" +
                           " to a field. Among other differences" +
                           ", such as goals and boundaries" +
                           ", generally indoor soccer is " +
                           "faster-paced, has fewer players, " +
                           " and can be more exciting to watch",
                           price="$2.99",
                           category="Soccer", catalog=catalog1)

session.add(catalogitem5)
session.commit()

# For Cricket
catalog1 = Catalog(user_id=1, name="Cricket")

session.add(catalog1)
session.commit()

# Cricket Equipment Cricket Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Cricket Ball",
                           description="A cricket ball is a hard, " +
                           "solid ball used to play cricket. A " +
                           "cricket ball consists of cork covered" +
                           " by leather, and manufacture is regulated" +
                           " by cricket law at first-class level. The" +
                           " manipulation of a cricket ball, through " +
                           "employment of its various physical " +
                           "properties, is a staple component" +
                           " of bowling and dismissing batsmen.",
                           price="$2.99",
                           category="Cricket", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Cricket Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Cricket Bat",
                           description="A cricket bat is a specialised piece" +
                           " of equipment used by batsmen in" +
                           " the sport of cricket to hit the ball" +
                           ", typically consisting of a cane handle " +
                           "attached to a flat-fronted willow-wood blade.",
                           price="$2.99",
                           category="Cricket", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# Cricket Equipment Jock (or jill for girls)
catalogitem3 = CatalogItem(user_id=1, title="Cricket Stumps",
                           description="In cricket, the stumps are " +
                           "the three vertical posts that support the " +
                           "bails and form the wicket. Stumping or being" +
                           " stumped is a method of dismissing a batsma",
                           price="$2.99",
                           category="Cricket", catalog=catalog1)

session.add(catalogitem3)
session.commit()
# Cricket Equipment Jock (or jill for girls)
catalogitem4 = CatalogItem(user_id=1, title="Cricket Sight screen",
                           description="A screen placed at the boundary " +
                           "known as the sight screen. This is " +
                           "aligned exactly parallel to the width " +
                           "of the pitch and behind both " +
                           "pairs of wickets.",
                           price="$2.99",
                           category="Cricket", catalog=catalog1)

session.add(catalogitem4)
session.commit()
# Cricket Equipment Jock (or jill for girls)
catalogitem5 = CatalogItem(user_id=1, title="Cricket Boundary",
                           description="A rope demarcating the " +
                           "perimeter of the field known as " +
                           "the boundary.",
                           price="$2.99",
                           category="Cricket", catalog=catalog1)

session.add(catalogitem5)
session.commit()

# For Baseball
catalog1 = Catalog(user_id=1, name="Baseball")

session.add(catalog1)
session.commit()

# Baseball Equipment Baseball Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Baseball Bat",
                           description="A rounded, solid wooden or " +
                           "hollow aluminum bat. Wooden bats are " +
                           "traditionally made from ash wood, though" +
                           " maple and bamboo is also sometimes used.",
                           price="$2.99",
                           category="Baseball", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Baseball Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Baseball Ball",
                           description="A cork sphere, tightly " +
                           "wound with layers of yarn or string" +
                           " and covered with a stitched leather coat.",
                           price="$2.99",
                           category="Baseball", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# Baseball Equipment Jock (or jill for girls)
catalogitem3 = CatalogItem(user_id=1, title="Baseball Base",
                           description="One of four corners of the " +
                           "infield which must be touched by a runner" +
                           " in order to score a run; more specifically" +
                           ", they are canvas bags (at first" +
                           ", second, and third base) and a rubber " +
                           "plate (at home)",
                           price="$2.99",
                           category="Baseball", catalog=catalog1)

session.add(catalogitem3)
session.commit()
# Baseball Equipment Jock (or jill for girls)
catalogitem4 = CatalogItem(user_id=1, title="Baseball Glove",
                           description="Leather gloves worn by players" +
                           " in the field. Long fingers and a " +
                           "webbed KKK between the thumb" +
                           " and first finger allows " +
                           "the fielder to catch the " +
                           "ball more easily.",
                           price="$2.99",
                           category="Baseball", catalog=catalog1)

session.add(catalogitem4)
session.commit()
# Baseball Equipment Jock (or jill for girls)
catalogitem5 = CatalogItem(user_id=1, title="Baseball Batting helmet",
                           description="Helmet worn by batter " +
                           "to protect the head and the ear facing " +
                           "the pitcher from the ball. Professional" +
                           " models have only one ear protector" +
                           " (left ear for right-handed batters," +
                           " right ear for lefties)",
                           price="$2.99",
                           category="Baseball", catalog=catalog1)

session.add(catalogitem5)
session.commit()

# For Snowboarding
catalog1 = Catalog(user_id=1, name="Snowboarding")

session.add(catalog1)
session.commit()

# Snowboarding Equipment Snowboarding Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Snowboard",
                           description="Snowboards are boards " +
                           "where both feet are secured to the " +
                           "same board, which are wider than" +
                           " skis, with the ability to glide" +
                           " on snow. Snowboards widths are between" +
                           " 6 and 12 inches or 15 to 30 centimeters." +
                           " Snowboards are differentiated from " +
                           "monoskis by the stance of the user.",
                           price="$2.99",
                           category="Snowboarding", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Snowboarding Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Snowboarding Goggles",
                           description="Goggles, or safety glasses," +
                           " are forms of protective eyewear that" +
                           " usually enclose or protect the area " +
                           "surrounding the eye in order to prevent " +
                           "particulates, water or chemicals" +
                           " from striking the eyes.",
                           price="$2.99",
                           category="Snowboarding", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# For Hockey
catalog1 = Catalog(user_id=1, name="Hockey")

session.add(catalog1)
session.commit()

# Hockey Equipment Hockey Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Hockey Helmet",
                           description="A helmet with strap, and" +
                           " optionally a face cage or visor, " +
                           "is required of all ice hockey players.",
                           price="$2.99",
                           category="Hockey", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Hockey Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Hockey Neck guard",
                           description="For skaters, a neck" +
                           " guard typically consists of a " +
                           "series of nylon or ABS plates for" +
                           " puncture resistance, with padding" +
                           "for comfort and fit and a tear-resistant" +
                           " nylon mesh outer covering",
                           price="$2.99",
                           category="Hockey", catalog=catalog1)

session.add(catalogitem2)
session.commit()


# For Rock Climbing
catalog1 = Catalog(user_id=1, name="Rock Climbing")

session.add(catalog1)
session.commit()

# Rock Climbing Equipment Rock Climbing Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Rock Climbing Carabiner",
                           description="Carabiners are metal " +
                           "loops with spring-loaded gates " +
                           "(openings), used as connectors. " +
                           "Once made primarily from steel",
                           price="$2.99",
                           category="Rock Climbing", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Rock Climbing Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Rock Climbing Quickdraw",
                           description="Quickdraws (often referred" +
                           " to as draws) are used by climbers to" +
                           " connect ropes to bolt anchors, or to " +
                           "other traditional protection, allowing " +
                           "the rope to move through the anchoring " +
                           "system with minimal friction.",
                           price="$2.99",
                           category="Rock Climbing", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# For Skating
catalog1 = Catalog(user_id=1, name="Skating")

session.add(catalog1)
session.commit()

# Skating Equipment Skating Equipment bag
catalogitem1 = CatalogItem(user_id=1, title="Skating Soakers",
                           description="Soakers are terry cloth" +
                           " blade covers that protect and keep" +
                           " figure skating blades dry.",
                           price="$2.99",
                           category="Skating", catalog=catalog1)

session.add(catalogitem1)
session.commit()

# Skating Equipment Jock (or jill for girls)
catalogitem2 = CatalogItem(user_id=1, title="Skating Guards",
                           description="Every figure skater " +
                           "should have a pair of ice skate " +
                           "guards inside his or her skate bag. " +
                           "Blades will be ruined if they touch" +
                           " concrete, wood, grass, or any surface " +
                           "besides ice, rubber",
                           price="$2.99",
                           category="Skating", catalog=catalog1)

session.add(catalogitem2)
session.commit()

# Skating Equipment Jock (or jill for girls)
catalogitem3 = CatalogItem(user_id=1, title="Skating Towel or Rag",
                           description="Figure skaters must " +
                           "always dry blades thoroughly after " +
                           "skating. A clean towel or rag should " +
                           "be packed inside a figure skater's " +
                           "skate bag",
                           price="$2.99",
                           category="Skating", catalog=catalog1)

session.add(catalogitem3)
session.commit()
# Skating Equipment Jock (or jill for girls)
catalogitem4 = CatalogItem(user_id=1, title="Skating Music",
                           description="Most figure skater's practice " +
                           "a program to music during every practice" +
                           " session. Keeping your music inside" +
                           " your skate bag will help you to be prepared.",
                           price="$2.99",
                           category="Skating", catalog=catalog1)

session.add(catalogitem4)
session.commit()
# Skating Equipment Jock (or jill for girls)
catalogitem5 = CatalogItem(user_id=1, title="Skating Rulebook",
                           description="Some figure skaters carry " +
                           "a copy of their figure skating" +
                           " federation's rulebook or a notebook",
                           price="$2.99",
                           category="Skating", catalog=catalog1)

session.add(catalogitem5)
session.commit()

print "added catalog items!"
