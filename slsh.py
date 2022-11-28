from importlib.resources import contents
from typing import Literal
import discord
from discord import app_commands, ui
import random
import json
import time
import math
import png
import cook as cookF

tfile = open('token.txt','r')
tkn = tfile.readline()
tfile.close()

file = open('users.json',)
users = json.load(file)
mFile = open('market.json',)
market = json.load(mFile)
eqFile = open('equipment.json')
equipment = json.load(eqFile)
lcFile = open('locations.json')
locations = json.load(lcFile)
ldbFile = open('leaderboards.json')
leaderboards = json.load(ldbFile)

ver = "0.0.1.9"

class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        #self.tree.copy_global_to(guild=discord.Object(id=901489176384507914))
        await self.tree.sync(guild=discord.Object(id=901489176384507914))
        await self.tree.sync()

    
intents = discord.Intents.default()
bot = BotClient(intents=intents)


@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')
    print (f'Ok {bot.user.name} is online now')
    print(f"Fish bot wants to help | {ver}")

async def createUser(userID):
    users[f'{userID}'] = {
        "pos": len(users),
        "money": 0,
        "fishlog": {
        "bass": 0, "pike": 0, "grunt": 0, "angelfish": 0, "guppy": 0, "anchovy": 0,
        "cod": 0, "marlin": 0, "tang": 0, "mudfish": 0, "trout": 0, "eel": 0,
        "snapper": 0, "tetra": 0, "firefish": 0, "parrotfish": 0, "catfish": 0, "fallfish": 0,
        "bonefish": 0
        }, #Rarity Chance, Extra Fish, Extra Fish Chance, Weight Chance
        "equipment": {"fishEq": {"name": "Stick", "quality": 0.1, "price": 0, "rc": 0, "ef": 0, "efc": 0, "wc": 0}, "boat": {"name": "raft", "cooldown": 5, "dur": 5, "price": 0}, "seasonings": {}, "cooking": {}},
        "owned": {"fishEq": {"Stick": True, "Lillian Butterfly": False, "Azule Etoi": False, "Melo II": False}, "boat": {"raft": True, "Rickety Rowboat": False, "Dubious Dinghy": False, "Stylish Speedboat": False}, "aquariums": {"Fish Bowl": False, "Small Tank": False, "Large Tank": False}},
        "inv": {},
        "contacts": {},
        "reputation": 1,
        "lastFish": 0,
        "isFishing": 0,
        "lastDur": 0,
        "lastCd": 0,
        "location": '0',
        "license": 0,
        "map": {
            "explored": [[17, 6]],
            "last": [17, 6]
        }
    }
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile) 
           
async def pullFish(userPos, loc, userLoc, uID):
    rc = users[f'{uID}']["equipment"]["fishEq"]["rc"]
    wc = users[f'{uID}']["equipment"]["fishEq"]["wc"]
    rr = await rarity(userLoc, loc, rc)
    dpi = await locDepth(loc)
    fish = {"from":userPos, "rarity": rr, "quality": random.random(), "prepBonus": 0, "weight": fishWeights[rr-1]*(1+wc)*(random.randrange(7500,14000,1)/10000+(dpi**.3)*locations[userLoc]["wMulti"])}
    return fish

rarityAr = ['common bass','common pike','common grunt','common\'t cod','common\'t marlin','common\'t tang','rare snapper','rare tetra','rare firefish', 'bonefish', 'common angelfish', 'common guppy', 'common\'t mudfish', 'common\'t trout', 'rare parrotfish', 'rare catfish', 'rubber ducky', 'rare fallfish', 'common anchovy', 'common\'t eel']
rarityGroups = ['common', 'common', 'common', 'commont', 'commont', 'commont', 'rare', 'rare', 'rare', 'event', 'common', 'common', 'commont', 'commont', 'rare', 'rare', 'novelty', 'rare', 'common', 'commont']
fishNames = ['bass', 'pike', 'grunt', 'cod', 'marlin', 'tang', 'snapper', 'tetra', 'firefish', 'bonefish', 'angelfish', 'guppy', 'mudfish', 'trout', 'parrotfish', 'catfish', 'rubber ducky', 'fallfish', 'anchovy', 'eel']
fishWeights = [12, 2.1, .93, 18.5, 210, 1.32, 28, 0.0003, 0.0005, 7, 2, 0.0002, 0.015, 23, 45, 45, 0.011, 2.2, 0.075, 55]
cfArS = [1, 2, 3, 11, 12, 19]
ufArS = [4, 5, 6, 13, 14, 20]
rfArS = [7, 8, 9, 15, 16, 18]

maxWeight = 294

#fishAr = [African glass catfish,African lungfish,Aholehole,Airbreathing catfish,Airsac catfish,Alaska blackfish,Albacore,Alewife,Alfonsino,Algae eater,Alligatorfish,Alligator gar,Amberjack,American sole,Amur pike,Anchovy,Anemonefish,Angelfish,Angler,Angler catfish,Anglerfish,Antarctic cod,Antarctic icefish,Antenna codlet,Arapaima,Archerfish,Arctic char,Armored gurnard,Armored searobin,Armorhead,Armorhead catfish,Armoured catfish,Arowana,Arrowtooth eel,Asian carps,Asiatic glassfish,Atka mackerel,Atlantic bonito,Atlantic cod,Atlantic herring,Atlantic salmon,Atlantic sharpnose shark,Atlantic saury,Atlantic silverside,Australasian salmon,Australian grayling,Australian herring,Australian lungfish,Australian prowfish,Ayu,Baikal oilfish,Bala shark,Ballan wrasse,Bamboo shark,Banded killifish,Bandfish,Banjo,Bangus,Banjo catfish,Barb,Barbel,Barbeled dragonfish,Barbeled houndshark,Barbel-less catfish,Barfish,Barracuda,Barracudina,Barramundi,Barred danio,Barreleye,Basking shark,Bass,Basslet,Batfish,Bat ray,Beachsalmon,Beaked salmon,Beaked sandfish,Beardfish,Beluga sturgeon,Bengal danio,Betta,Bichir,Bicolor goat fish,Bigeye,Bigeye squaretail,Bighead carp,Bigmouth buffalo,Bigscale,Bigscale pomfret,Billfish,Bitterling,Black angelfish,Black bass,Black dragonfish,Blackchin,Blackfin Tuna,Blackfish,Black neon tetra,Blacktip reef shark,Black mackerel,Black scalyfin,Black sea bass,Black scabbardfish,Black swallower,Black tetra,Black triggerfish,Bleak,Blenny,Blind goby,Blind shark,Blobfish,Blowfish,Blue catfish,Blue danio,Blue-redstripe danio,Blue eye trevalla,Bluefin tuna,Bluefish,Bluegill,Blue gourami,Blue shark,Blue triggerfish,Blue whiting,Bluntnose knifefish,Bluntnose minnow,Boafish,Boarfish,Bobtail snipe eel,Bocaccio,Boga,Bombay duck,Bonefish,Bonito,Bonnethead shark,Bonnetmouth,Bonytail,Bonytongue,Bowfin,Boxfish,Bramble shark,Bream,Brill,Bristlemouth,Bristlenose catfish,Broadband dogfish,Bronze corydoras,Brook lamprey,Brook stickleback,Brook trout,Brotula,Brown trout,Buffalo fish,Bullhead,Bullhead shark,Bull shark,Bull trout,Burbot,Bumblebee goby,Buri,Burma danio,Burrowing goby,Butterfish,Butterfly ray,Butterflyfish,California flyingfish,California halibut,Canary rockfish,Candiru,Candlefish,Capelin,Cardinalfish,Cardinal tetra,Carp,Carpetshark,Carpsucker,Catalufa,Catfish,Catla,Cat shark,Cavefish,Celebes rainbowfish,Central mudminnow,Chain pickerel,Channel bass,Channel catfish,Char,Cherry salmon,Chimaera,Chinook salmon,Cherubfish,Chub,Chubsucker,Chum salmon,Cichlid,Cisco,Climbing catfish,Climbing gourami,Climbing perch,Clingfish,Clownfish,Clown loach,Clown triggerfish,Cobbler,Cobia,Cod,Codlet,Codling,Coelacanth,Coffinfish,Coho salmon,Coley,Collared carpetshark,Collared dogfish,Colorado squawfish,Combfish,Combtail gourami,Combtooth blenny,Common carp,Common tunny,Conger eel,Convict blenny,Convict cichlid,Cookie-cutter shark,Coolie loach,Cornetfish,Cowfish,Cownose ray,Cow shark,Crappie,Creek chub,Crestfish,Crevice kelpfish,Croaker,Crocodile icefish,Crocodile shark,Crucian carp,Cuckoo wrasse,Cusk,Cusk-eel,Cutlassfish,Cutthroat eel,Cutthroat trout,Dab,Dace,Daggertooth pike conger,Damselfish,Danio,Darter,Dartfish,Dealfish,Death Valley pupfish,Deep sea eel,Deep sea smelt,Deepwater cardinalfish,Deepwater flathead,Deepwater stingray,Delta smelt,Demoiselle,Denticle herring,Desert pupfish,Devario,Devil ray,Dhufish,Discus,Dogfish,Dogfish shark,Dogteeth tetra,Dojo loach,Dolly Varden trout,Dolphin fish,Dorab wolf-herring,Dorado,Dory,Dottyback,Dragonet,Dragonfish,Dragon goby,Driftfish,Driftwood catfish,Drum,Duckbill,Duckbill eel,Dusky grouper,Dusky shark,Dwarf gourami,Dwarf loach,Eagle ray,Earthworm eel,Eel,Eel cod,Eel-goby,Eelpout,Eeltail catfish,Elasmobranch,Electric catfish,Electric eel,Electric knifefish,Electric ray,Elephant fish,Elephantnose fish,Elver,Ember parrotfish,Emerald catfish,Emperor,Emperor angelfish,Emperor bream,Escolar,Eucla cod,Eulachon,European chub,European eel,European flounder,European minnow,European perch,False brotula,False cat shark,False moray,False trevally,Fangtooth,Fathead sculpin,Featherback,Fierasfer,Fire goby,Filefish,Finback cat shark,Fingerfish,Fire bar danio,Firefish,Flabby whale fish,Flagblenny,Flagfin,Flagfish,Flagtail,Flashlight fish,Flatfish,Flathead,Flathead catfish,Flier,Flounder,Flying gurnard,Flying fish,Footballfish,Forehead brooder,Four-eyed fish,French angelfish,Freshwater eel,Freshwater hatchetfish,Freshwater shark,Frigate mackerel,Frilled shark,Frogfish,Frogmouth catfish,Fusilier fish,Galjoen fish,Ganges shark,Gar,Garden eel,Garibaldi,Garpike,Ghost fish,Ghost flathead,Ghost knifefish,Ghost pipefish,Ghost shark,Ghoul,Giant danio,Giant gourami,Giant sea bass,Gibberfish,Gila trout,Gizzard shad,Glass catfish,Glassfish,Glass knifefish,Glowlight danio,Goatfish,Goblin shark,Goby,Golden dojo,Golden loach,Golden shiner,Golden trout,Goldeye,Goldfish,Gombessa,Goosefish,Gopher rockfish,Gourami,Grass carp,Graveldiver,Grayling,Gray mullet,Gray reef shark,Great white shark,Green swordtail,Greeneye,Greenling,Grenadier,Green spotted puffer,Ground shark,Grouper,Grunion,Grunt,Grunter,Grunt sculpin,Gudgeon,Guitarfish,Gulf menhaden,Gulper eel,Gulper,Gunnel,Guppy,Gurnard,Haddock,Hagfish,Hairtail,Hake,Halfbeak,Halfmoon,Halibut,Halosaur,Hamlet,Hammerhead shark,Hammerjaw,Handfish,Hardhead catfish,Harelip sucker,Hatchetfish,Hawkfish,Herring,Herring smelt,Hickory Shad,Hillstream loach,Hog sucker,Hoki,Horn shark,Horsefish,Houndshark,Huchen,Humuhumunukunukuapua/'a,Hussar,Icefish,Ide,Ilish/Hilsha,Inanga,Inconnu,Jack,Jackfish,Jack Dempsey,Japanese eel,Javelin,Jawfish,Jellynose fish,Jewelfish,Jewel tetra,Jewfish,John Dory,Kafue pike,Kahawai,Kaluga,Kanyu,Kelp perch,Kelpfish,Killifish,King of the herrings,Kingfish,King-of-the-salmon,Kissing gourami,Knifefish,Knifejaw,Koi,Kokanee,Kokopu,Kuhli loach,Labyrinth fish,Ladyfish,Lake chub,Lake trout,Lake whitefish,Lampfish,Lamprey,Lancetfish,Lanternfish,Largemouth bass,Leaffish,Leatherjacket,Lefteye flounder,Lemon shark,Lemon sole,Lemon tetra,Lenok,Leopard danio,Lightfish,Limia,Lined sole,Ling,Ling cod,Lionfish,Livebearer,Lizardfish,Loach,Loach catfish,Loach goby,Loach minnow,Longfin,Longfin dragonfish,Longfin escolar,Longfin smelt,Long-finned char,Long-finned pike,Long-finned sand diver,Longjaw mudsucker,Longneck eel,Longnose chimaera,Longnose dace,Longnose lancetfish,Longnose sucker,Longnose whiptail catfish,Long-whiskered catfish,Loosejaw,Lost River sucker,Louvar,Loweye catfish,Luderick,Luminous hake,Lumpsucker,Lungfish,Mackerel,Mackerel shark,Madtom,Mahi-mahi,Mahseer,Mail-cheeked fish,Mako shark,Mandarinfish,Manefish,Man-of-war fish,Manta ray,Marblefish,Marine hatchetfish,Marlin,Masu salmon,Medaka,Medusafish,Megamouth shark,Menhaden,Merluccid hake,Mexican golden trout,Midshipman fish,Milkfish,Minnow,Minnow of the deep,Modoc sucker,Mojarra,Mola mola,Monkeyface prickleback,Monkfish,Mooneye,Moonfish,Moorish idol,Mora,Moray eel,Morid cod,Morwong,Moses sole,Mosquitofish,Mouthbrooder,Mozambique tilapia,Mrigal,Mud catfish,Mudfish,Mudminnow,Mud minnow,Mudskipper,Mudsucker,Mullet,Mummichog,Murray cod,Muskellunge,Mustache triggerfish,Mustard eel,Naked-back knifefish,Nase,Needlefish,Neon tetra,New World rivuline,New Zealand sand diver,New Zealand smelt,Nibble fish,Noodlefish,North American darter,North American freshwater catfish,North Pacific daggertooth,Northern anchovy,Northern clingfish,Northern lampfish,Northern pike,Northern sea robin,Northern squawfish,Northern stargazer,Notothen,Nurseryfish,Nurse shark,Oarfish,Ocean perch,Ocean sunfish,Oceanic whitetip shark,Oilfish,Oldwife,Old World knifefish,Olive flounder,Opah,Opaleye,Orange roughy,Orangespine unicorn fish,Orangestriped triggerfish,Orbicular batfish,Orbicular velvetfish,Oregon chub,Orfe,Oriental loach,Oscar,Owens pupfish,Pacific albacore,Pacific cod,Pacific hake,Pacific herring,Pacific lamprey,Pacific salmon,Pacific saury,Pacific trout,Pacific viperfish,Paddlefish,Pancake batfish,Panga,Paradise fish,Parasitic catfish,Parore,Parrotfish,Peacock flounder,Peamouth,Pearleye,Pearlfish,Pearl danio,Pearl perch,Pelagic cod,Pelican eel,Pelican gulper,Pencil catfish,Pencilfish,Pencilsmelt,Peppered corydoras,Perch,Peters' elephantnose fish,Pickerel,Pigfish,Pike conger,Pike eel,Pike,Pikeblenny,Pikeperch,Pilchard,Pilot fish,Pineapplefish,Pineconefish,Pink salmon,Píntano,Pipefish,Piranha,Pirarucu,Pirate perch,Plaice,Platy,Platyfish,Pleco,Plownose chimaera,Poacher,Pollyfish,Pollock,Pomfret,Pompano,Pompano dolphinfish,Ponyfish,Popeye catalufa,Porbeagle shark,Porcupinefish,Porgy,Port Jackson shark,Powen,Prickleback,Pricklefish,Prickly shark,Prowfish,Pufferfish,Pumpkinseed,Pupfish,Pygmy sunfish,Queen danio,Queen parrotfish,Queen triggerfish,Quillback,Quillfish,Rabbitfish,Raccoon butterfly fish,Ragfish,Rainbow trout,Rainbowfish,Rasbora,Ratfish,Rattail,Ray,Razorback sucker,Razorfish,Red grouper,Red salmon,Red snapper,Redfin perch,Redfish,Redhorse sucker,Redlip blenny,Redmouth whalefish,Redtooth triggerfish,Red velvetfish,Red whalefish,Reedfish,Reef triggerfish,Remora,Requiem shark,Ribbon eel,Ribbon sawtail fish,Ribbonfish,Rice eel,Ricefish,Ridgehead,Riffle dace,Righteye flounder,Rio Grande perch,River loach,River shark,River stingray,Rivuline,Roach,Roanoke bass,Rock bass,Rock beauty,Rock cod,Rocket danio,Rockfish,Rockling,Rockweed gunnel,Rohu,Ronquil,Roosterfish,Ropefish,Rough scad,Rough sculpin,Roughy,Roundhead,Round herring,Round stingray,Round whitefish,Rudd,Rudderfish,Ruffe,Russian sturgeon,Sábalo,Sabertooth,Saber-toothed blenny,Sabertooth fish,Sablefish,Sacramento blackfish,Sacramento splittail,Sailfin silverside,Sailfish,Salamanderfish,Salmon,Salmon shark,Sandbar shark,Sandburrower,Sand dab,Sand diver,Sand eel,Sandfish,Sand goby,Sand knifefish,Sand lance,Sandperch,Sandroller,Sand stargazer,Sand tiger,Sand tilefish,Sandbar shark,Sarcastic fringehead,Sardine,Sargassum fish,Sauger,Saury,Sawfish,Saw shark,Sawtooth eel,Scabbard fish,Scaly dragonfish,Scat,Scissortail rasbora,Scorpionfish,Sculpin,Scup,Sea bass,Sea bream,Sea catfish,Sea chub,Sea devil,Sea dragon,Sea lamprey,Sea raven,Sea snail,Sea toad,Seahorse,Seamoth,Searobin,Sevan trout,Sergeant major,Shad,Shark,Sharksucker,Sharpnose puffer,Sheatfish,Sheepshead,Sheepshead minnow,Shiner,Shortnose chimaera,Shortnose sucker,Shovelnose sturgeon,Shrimpfish,Siamese fighting fish,Sillago,Silver carp,Silver dollar,Silver dory,Silver hake,Silverside,Silvertip tetra,Sind danio,Sixgill ray,Sixgill shark,Skate,Skilfish,Skipjack tuna,Slender mola,Slender snipe eel,Sleeper,Sleeper shark,Slickhead,Slimehead,Slimy mackerel,Slimy sculpin,Slipmouth,Smalleye squaretail,Smalltooth sawfish,Smelt,Smelt-whiting,Smooth dogfish,Snailfish,Snake eel,Snakehead,Snake mackerel,Snapper,Snipe eel,Snipefish,Snook,Snubnose eel,Snubnose parasitic eel,Sockeye salmon,Soldierfish,Sole,South American darter,South American lungfish,Southern Dolly Varden,Southern flounder,Southern hake,Southern sandfish,Southern smelt,Spadefish,Spaghetti eel,Spanish mackerel,Spearfish,Speckled trout,Spiderfish,Spikefish,Spinefoot,Spiny basslet,Spiny dogfish,Spiny dwarf catfish,Spiny eel,Spinyfin,Splitfin,Spookfish,Spotted climbing perch,Spotted danio,Spottail pinfish,Sprat,Springfish,Squarehead catfish,Squaretail,Squawfish,Squeaker,Squirrelfish,Staghorn sculpin,Stargazer,Starry flounder,Steelhead,Stickleback,Stingfish,Stingray,Stonecat,Stonefish,Stoneroller minnow,Stream catfish,Striped bass,Striped burrfish,Sturgeon,Sucker,Suckermouth armored catfish,Summer flounder,Sundaland noodlefish,Sunfish,Surf sardine,Surfperch,Surgeonfish,Swallower,Swamp-eel,Swampfish,Sweeper,Swordfish,Swordtail,Tadpole cod,Tadpole fish,Tailor,Taimen,Tang,Tapetail,Tarpon,Tarwhine,Telescopefish,Temperate bass,Temperate ocean-bass,Temperate perch,Tench,Tenpounder,Tenuis,Tetra,Thorny catfish,Thornfish,Threadfin,Threadfin bream,Thread-tail,Three spot gourami,Threespine stickleback,Three-toothed puffer,Thresher shark,Tidewater goby,Tiger barb,Tigerperch,Tiger shark,Tiger shovelnose catfish,Tilapia,Tilefish,Titan triggerfish,Toadfish,Tommy ruff,Tompot blenny,Tonguefish,Tope,Topminnow,Torpedo,Torrent catfish,Torrent fish,Trahira,Treefish,Trevally,Triggerfish,Triplefin blenny,Triplespine,Tripletail,Tripod fish,Trout,Trout cod,Trout-perch,Trumpeter,Trumpetfish,Trunkfish,Tubeblenny,Tube-eye,Tube-snout,Tubeshoulder,Tui chub,Tuna,Turbot,Two spotted goby,Uaru,Unicorn fish,Upside-down catfish,Vanjaram,Velvet belly lanternshark,Velvet catfish,Velvetfish,Vendace,Vermilion snapper,Vimba,Viperfish,Wahoo,Walking catfish,Wallago,Walleye,Walleye pollock,Walu,Warmouth,Warty angler,Waryfish,Waspfish,Weasel shark,Weatherfish,Weever,Weeverfish,Wels catfish,Whale catfish,Whalefish,Whale shark,Whiff,Whitebait,White croaker,Whitefish,White marlin,White shark,Whitetip reef shark,Whiting,Wobbegong,Wolf-eel,Wolffish,Wolf-herring,Worm eel,Wormfish,Wrasse,Wrymouth,X-ray tetra,Yellow-and-black triplefin,Yellowback fusilier,Yellowbanded perch,Yellow bass,Yellowedge grouper,Yellow-edged moray,Yellow-eye mullet,Yellowhead jawfish,Yellowfin croaker,Yellowfin cutthroat trout,Yellowfin grouper,Yellowfin tuna,Yellowfin pike,Yellowfin surgeonfish,Yellowfin tuna,Yellow jack,Yellowmargin triggerfish,Yellow moray,Yellow perch,Yellowtail,Yellowtail amberjack,Yellowtail barracuda,Yellowtail clownfish,Yellowtail horse mackerel,Yellowtail kingfish,Yellowtail snapper,Yellow tang,Yellow weaver,Yellowtail catfish,Zander,Zebra bullhead shark,Zebra danio,Zebrafish,Zebra lionfish,Zebra loach,Zebra oto,Zebra pleco,Zebra shark,Zebra tilapia,Zebra turkeyfish,Ziege,Zingel]



async def rarity(userLoc, loc, rc):
    available = locations[userLoc]["population"]
    res = -1
    depth = await locDepth(loc)
    rarity = random.uniform(rc, 1)
    if (userLoc == '0'):
        if (rarity <= .75):
            res = 1
        elif (rarity <= .9):
            res = 4
        else:
            res = 18
    elif (userLoc == '1'):
        if (rarity <= .3):
            res = 1
        elif (rarity <= .55):
            res = 11
        elif (rarity <= .75):
            res = 12
        elif (rarity <= .82):
            res = 6
        elif (rarity <= .87):
            res = 13
        elif (rarity <= .9):
            res = 14
        elif (rarity <= .95):
            res = 18
        elif (rarity <= .98):
            res = 16
        else:
            res = 8
    elif (userLoc == '2'):
        if (rarity <= .3):
            res = 1
        elif (rarity <= .55):
            res = 2
        elif (rarity <= .75):
            res = 3
        elif (rarity <= .80):
            res = 4
        elif (rarity <= .84):
            res = 6
        elif (rarity <= .87):
            res = 5
        elif (rarity <= .9):
            res = 20
        elif (rarity <= .95):
            res = 8
        elif (rarity <= .98):
            res = 7
        else:
            res = 9
    elif (userLoc == '3'):
        if (rarity <= .22):
            res = 1
        elif (rarity <= .39):
            res = 11
        elif (rarity <= .52):
            res = 12
        elif (rarity <= .62):
            res = 2
        elif (rarity <= .69):
            res = 3
        elif (rarity <= .75):
            res = 19
        elif (rarity <= .79):
            res = 4
        elif (rarity <= .81):
            res = 6
        elif (rarity <= .83):
            res = 13
        elif (rarity <= .86):
            res = 14
        elif (rarity <= .88):
            res = 5
        elif (rarity <= .9):
            res = 20
        elif (rarity <= .93):
            res = 16
        elif (rarity <= .96):
            res = 8
        elif (rarity <= .98):
            res = 7
        elif (rarity <= .99):
            res = 9
        else:
            res = 15
    return res
        
async def locDepth(location):
    depth = mp[location[0]][location[1]]
    dpi = 0
    if depth == "s":
        dpi = 1
    elif (depth == "d" or depth == "b"):
        dpi = 2
    return dpi

async def value(rarity, quality, foreign, prep):
    return await cookF.value(rarity, quality, foreign, prep)
    
async def qualify(quality):
    if (quality == 1):
        return "perfect"
    elif (quality > .75):
        return "good"
    elif (quality > .25):
        return "decent"
    else:
        return "bad"

async def createProfile(userID):
    users[f'{userID}']['prof'] = {
        'bio': '',
        'fishTime': 0
    }
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)

@bot.event
async def on_interaction(ctx):
    if not str(ctx.user.id) in users:
        await createUser(ctx.user.id)
        await ctx.response.send_message(f'{ctx.user.display_name}, you now have a bot profile.')

@bot.tree.command(description="Displays information about the bot")
async def help(ctx: discord.Interaction):
    await ctx.response.send_message("Hey there! Fish bot is a semi-idle simulation experience in which you can fish, explore, and expand your skills to become a better fisherman. \n\nWe're currently under active development, and as such the commands available may vary from day-to-day, so for now please rely on the descriptions given by each individual command to determine how they function. \n\nIf you encounter any errors while using the bot, please let us know in our support server - https://discord.com/invite/YtpyMFAtZU. Thanks for using the bot!")

@bot.tree.command(description="Shows your bot profile")
async def profile(ctx: discord.Interaction):
    if users[f'{ctx.user.id}'].get('prof') == None:
        await createProfile(ctx.user.id)
    pf_embed = discord.Embed(
        title = str(f'{ctx.user.display_name}\'s Profile'),
        type = "rich"
    )
    unN = (ctx.user.display_name)
    uAvt = ctx.user.avatar
    pf_embed.set_author(name=unN, icon_url=uAvt)
    pf_embed.add_field(name="Reputation:", value=f"You have a reputation score of {round(users[f'{ctx.user.id}']['reputation'])} adding to your prep skill!", inline=False)
    ub = users[f'{ctx.user.id}']['prof']['bio']
    bioF = ub if(ub != '') else 'No bio set yet!'
    pf_embed.add_field(name="User Bio:", value=bioF, inline=False)
    fTi = round(users[f'{ctx.user.id}']['prof']['fishTime']/60,2)
    pf_embed.add_field(name="Time Spent Fishing:", value=f'{fTi} minutes', inline=False)
    await ctx.response.send_message(embed=pf_embed)


@bot.tree.command(description="Set a personalized bio for your bot profile")
@app_commands.describe(bio='Your new bio')
async def bio(ctx: discord.Interaction, bio: str):
    if users[f'{ctx.user.id}'].get('prof') == None:
        await createProfile(ctx.user.id)
    if (len(bio) > 1000):
        await ctx.response.send_message('Please limit your bio to 1000 characters')
    else:
        users[f'{ctx.user.id}']['prof']['bio'] = bio
        await ctx.response.send_message("Your bio has been set.")
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)


@bot.tree.command(description="Displays your all time fish counts")
async def log(ctx: discord.Interaction):
    fdx = users[f'{ctx.user.id}']['fishlog']
    fd_embed = discord.Embed(
        title = str(f'{ctx.user.display_name}\'s Fish Log'),
        type="rich",
        description=f"Here are your all time fish counts!"
    )
    fd_embed.add_field(name=f"Common Fish:", value=f"Bass: {(fdx[fishNames[cfArS[0]-1]])}\nPike: {(fdx[fishNames[cfArS[1]-1]])}\nGrunt: {(fdx[fishNames[cfArS[2]-1]])}\nAngelfish: {(fdx[fishNames[cfArS[3]-1]])}\nGuppy: {(fdx[fishNames[cfArS[4]-1]])}\nAnchovy: {(fdx[fishNames[cfArS[5]-1]])}")
    fd_embed.add_field(name=f"Common't Fish:", value=f"Cod: {(fdx[fishNames[ufArS[0]-1]])}\nMarlin: {(fdx[fishNames[ufArS[1]-1]])}\nTang: {(fdx[fishNames[ufArS[2]-1]])}\nMudfish: {(fdx[fishNames[ufArS[3]-1]])}\nTrout: {(fdx[fishNames[ufArS[4]-1]])}\nEel: {(fdx[fishNames[ufArS[5]-1]])}")
    fd_embed.add_field(name=f"Rare Fish:", value=f"Snapper: {(fdx[fishNames[rfArS[0]-1]])}\nTetra: {(fdx[fishNames[rfArS[1]-1]])}\nFirefish: {(fdx[fishNames[rfArS[2]-1]])}\nParrotfish: {(fdx[fishNames[rfArS[3]-1]])}\nCatfish: {(fdx[fishNames[rfArS[4]-1]])}\nFallfish: {(fdx[fishNames[rfArS[5]-1]])}")
    await ctx.response.send_message(embed=fd_embed)


# @bot.tree.command(description="Tells you where you are currently fishing")
# async def location(ctx: discord.Interaction):
#     userInfo = users[f'{ctx.user.id}']
#     await ctx.response.send_message(f"You are currently fishing in {locations[userInfo['location']]['knAs']}")

# posLoc = ['bathtub', 'creek', 'pond', 'lake', 'ocean']
# @bot.tree.command(description="Allows you to travel to a new fishing location")
# async def travel(ctx: discord.Interaction, loc: Literal['bathtub', 'creek', 'pond', 'lake', 'ocean']):
#     if users[f'{ctx.user.id}']['license'] < locations[f'{posLoc.index(loc)-1}']['license']:
#         await ctx.response.send_message("You don't have a high enough license level to fish there!")
#     else:
#         users[f'{ctx.user.id}']['location'] = f'{posLoc.index(loc)-1}'
#         with open('users.json', 'w') as outfile:
#             json.dump(users, outfile)
#         await ctx.response.send_message(f"You are now fishing in {locations[users[f'{ctx.user.id}']['location']]['knAs']}")

@bot.tree.command(description="Gives you information on your current license status")
async def license(ctx: discord.Interaction):
    # userInfo = users[f'{ctx.user.id}']
    # uLic = userInfo["license"]
    # uFTot = 0
    # for type in userInfo["fishlog"]:
    #     uFTot = uFTot + userInfo["fishlog"][type]
    # nxL = 'You currently have the highest level license available!'
    # if uLic < 2:
    #     fLCount = [50, 1000]
    #     fLPrice = [100, 5000]
    #     nxL = f"You need to catch a total of {fLCount[uLic]} fish and pay a fee of {fLPrice[uLic]} perles to upgrade your license. If you are ready to upgrade your license, run \"/buy license\""
    # await ctx.response.send_message(f"You currently have a class {uLic} license, and have caught a total of {uFTot} fish. {nxL}")
    await ctx.response.send_message(f"Licenses are currently being reworked.")

@bot.tree.command(description="Displays a random fish gif")
async def gif(ctx: discord.Interaction):
    g =  random.randint(1,3)
    if g == 1:
        await ctx.response.send_message(file=discord.File('Fish-I.gif'))
    elif g == 2:
        await ctx.response.send_message("*Crispy*", file=discord.File('Fish-B.gif'))
    else:
        await ctx.response.send_message(file=discord.File('Fish-N.gif'))

def validExp(dt):
    if (dt == 'd' or dt == 's' or dt == 'b'):
        return True
    return False

def explore(userID):
    explored = users[f'{userID}']['map']['explored']
    stp = explored[random.randint(0,len(explored)-1)]
    place = False
    exp = []
    rep = 0
    if (stp != [17,6]):
        while (not place):
            goto = random.randint(1,4)
            if (goto == 1):
                if (stp[0] < 19):
                    if validExp((mp[stp[0]+1][stp[1]])):
                        place = True
                        exp = [stp[0]+1, stp[1]]
            elif (goto == 2):
                if (stp[0] > 0):
                    if validExp((mp[stp[0]-1][stp[1]])):
                        place = True
                        exp = [stp[0]-1, stp[1]]    
            elif (goto == 3):
                if (stp[1] < 19):
                    if validExp((mp[stp[0]][stp[1]+1])):
                        place = True
                        exp = [stp[0], stp[1]+1]
            else:
                if (stp[1] > 0):
                    if validExp((mp[stp[0]][stp[1]-1])):
                        place = True
                        exp = [stp[0], stp[1]-1]
            if (exp in explored and rep%7 < 6 and rep < 50):
                place = False
                rep += 1
            elif (exp in explored and rep%7 == 6 and rep < 50):
                place = False
                stp = explored[random.randint(0,len(explored)-1)]
                rep += 1
    else:
        goto = random.randint(1,2)
        if (goto == 1):
            exp = [16,6]
        else:
            exp = [18,6]
    if (not exp in explored):
        users[f'{userID}']['map']['explored'].append(exp)
        users[f'{userID}']['map']['last'] = exp
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    return exp

@bot.tree.command(description="Go fishing for something new")
async def fish(ctx: discord.Interaction):
    userInfo = users.get('{}'.format(ctx.user.id))
    if (userInfo["isFishing"] == 0 and (userInfo["lastFish"] - time.time() < 0)):
        users[f'{ctx.user.id}']["lastFish"] = time.time() + userInfo["equipment"]["boat"]["cooldown"] + userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.user.id}']["isFishing"] = 1
        users[f'{ctx.user.id}']["lastDur"] = userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.user.id}']["lastCd"] = userInfo["equipment"]["boat"]["cooldown"]
        await ctx.response.send_message(f'{ctx.user.display_name}, your fishing trip has started! Come back in {userInfo["equipment"]["boat"]["dur"]} seconds to see the results!')
    elif (userInfo["isFishing"] == 1 and (userInfo["lastCd"] >= userInfo["lastFish"] - time.time())):
        if users[f'{ctx.user.id}'].get('prof') == None:
            await createProfile(ctx.user.id)
        users[f'{ctx.user.id}']['prof']['fishTime'] = users[f'{ctx.user.id}']['prof']['fishTime'] + users[f'{ctx.user.id}']["lastDur"]
        totVal = 0
        numCaught = random.randint(0,math.ceil(userInfo["lastDur"]/(3/userInfo["equipment"]["fishEq"]["quality"])))
        loc = explore(ctx.user.id)
        if numCaught == 0:
            numCaught = random.randint(0,1)
        numCaught = numCaught + random.triangular(0, users[f'{ctx.user.id}']["equipment"]['fishEq']["ef"], users[f'{ctx.user.id}']["equipment"]['fishEq']["efc"])
        r = 0
        q = 0
        fdex = users[f'{ctx.user.id}']['fishlog']
        for i in range(numCaught):
            if userInfo.get("location") == "-1":
                r = 17
                numCaught = 1
                totVal = 0
                w = 0.01
            else:
                fish = await pullFish(userInfo.get("pos"), loc, userInfo.get("location"), ctx.user.id)
                dpi = await locDepth(loc)
                if (mp[loc[0]][loc[1]] == "b"):
                    if (users[f"{ctx.user.id}"].get("markets") != None):
                        users[f"{ctx.user.id}"]["markets"] = users[f'{ctx.user.id}']["markets"].append(loc)
                    else:
                        users[f"{ctx.user.id}"]["markets"] = [loc]
                    await ctx.channel.send(f"{ctx.user.display_name}, you just discovered a new market! Use the /markets command for more information!")
                q = fish.get("quality")
                r = fish.get("rarity")
                w = fish.get("weight")
                if leaderboards[f"{fishNames[r-1]}"]["weight"] < w:
                    moneys = users[f'{ctx.user.id}']['money']
                    bonus = 10
                    users[f'{ctx.user.id}']['money'] = moneys + bonus
                    leaderboards[f"{fishNames[r-1]}"] = fish
                    await ctx.channel.send(f'{ctx.user.display_name}, you have found the biggest {fishNames[r-1]} yet! The Siltora Club has rewarded you a 10 perle prize, and you have recieved a place on the leaderboard!')
                users[f'{ctx.user.id}']["inv"][f'{len(userInfo.get("inv"))}'] = fish
                fdex[fishNames[r-1]] = fdex[fishNames[r-1]] + 1
                totVal += await value(r,q,False,0)
        users[f'{ctx.user.id}']['fishlog'] = fdex
        users[f'{ctx.user.id}']["isFishing"] = 0
        outMsg = f'{ctx.user.display_name}, your fishing trip yielded {numCaught} fish! Their total value is {totVal} perles! :fishing_pole_and_fish:'
        if numCaught <= 0:
            outMsg = f'{ctx.user.display_name}, your line snapped before you could catch any fish! Unlucky!'
        elif numCaught == 1:
            outMsg = f'{ctx.user.display_name}, you caught a {rarityAr[r-1]}! It weighs {round(w,2)} lbs and is worth {totVal} perles! :fishing_pole_and_fish:'
        await ctx.response.send_message(outMsg)
    elif (userInfo["lastCd"] < userInfo["lastFish"] - time.time()):
        await ctx.response.send_message(f'{ctx.user.display_name}, you\'re still fishing! Come back in {round(userInfo["lastFish"] - time.time() - userInfo["lastCd"])} seconds!')
    else: 
        await ctx.response.send_message(f'{ctx.user.display_name}, you need to wait {round(userInfo["lastFish"]-time.time())} more seconds before fishing again for conservation reasons!')
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)
    with open('leaderboards.json', 'w') as outfile:
        json.dump(leaderboards, outfile)


@bot.tree.command(description="View the markets that you've encountered")
async def markets(ctx: discord.Interaction):
    await ctx.response.send_message("Markets are still in development, but any markets that you've found will stay in consideration!")

@bot.tree.command(description="Trade a fish from your inventory into the market")
async def trade(ctx: discord.Interaction, slot:int):
    userInfo = users.get('{}'.format(ctx.user.id))
    if (slot < 1 or slot>len(userInfo.get('inv'))):
        await ctx.response.send_message('Invalid inventory slot')
    else:
        slot -= 1
        if (userInfo.get('inv').get(f'{slot}').get("from") == userInfo.get("pos")):
            userFish = userInfo.get('inv').get(f'{slot}')
            marketSlot = random.randint(0,99999)
            marketFish = market.get("slot{}".format(marketSlot))
            while (marketFish["from"] == userInfo["pos"]):
                marketSlot = random.randint(0,99999)
                marketFish = market.get(f"slot{marketSlot}")
            userFish["prepBonus"] = 0
            market["slot{}".format(marketSlot)] = userFish
            userInfo['inv'][f'{slot}'] = marketFish
            q = marketFish.get("quality")
            r = marketFish.get("rarity")
            await ctx.response.send_message(f'{ctx.user.display_name}, your new fish is a {rarityAr[r-1]} and is in {await qualify(q)} condition. It is worth {await value(r,q,True,0)} perles! :fish:')
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)
        else:
            await ctx.response.send_message('You can\'t send this fish back!')

@bot.tree.command(description="Prepare your fish with seasonings or with accumulated skill")
async def prepare(ctx: discord.Interaction, slot:int=1):
    await cookF.prepare(ctx, slot)

@bot.tree.command(guild=discord.Object(901489176384507914), description="Developer Command")
async def special(ctx: discord.Interaction, name:str, num:int):
    if (ctx.user.id == 393586279964475393 or ctx.user.id == 458809225120972800):
        i = 0
        for i in range(num):
            marketSlot = [7541,13501,13938,16595,26773,46262,47663,52353,57710,64896,67709,74790,86063,94945,99082][i]
            market[f'slot{marketSlot}'] = {"from": -2, "rarity": rarityAr.index(name)+1, "quality": 1, "prepBonus": 0, "weight": fishWeights[rarityAr.index(name)]}
        await ctx.response.send_message(f'Extremely rare {name} have entered the market! There\'s a {num/1000}% chance to catch one!')
        with open('market.json', 'w') as outfile:
            json.dump(market, outfile)

@bot.tree.command(description="Displays your inventory")
async def inventory(ctx: discord.Interaction):
    fi = users[f'{ctx.user.id}']['inv']
    fe = users[f'{ctx.user.id}']['equipment']
    i = 0
    uf = []
    wf = []
    for i in range(len(fi)):
        uf.append(rarityGroups[fi[f'{i}']['rarity']-1])
        wf.append(fi[f'{i}']['rarity'])
    cf = len([f for f in uf if f == 'common'])
    ctf = len([f for f in uf if f == 'commont'])
    rf = len([f for f in uf if f == 'rare'])
    ef = len([f for f in uf if f == 'event'])
    evf = f' and **{ef}** event fish!' if ef > 0 else ''
    bt = (fe['boat']['name']).lower()
    rd = (fe['fishEq']['name']).lower()
    #s = fe['seasoning']
    #sS = f'\nYou have enough seasoning for {s} more servings!' if (s > 0) else ''
    in_embed = discord.Embed(
        title = str(f'{ctx.user.display_name}\'s Inventory'),
        type="rich",
        description=f"You have {len(fi)} total fish{evf}\n/storage for a more detailed list of fish"
    )
    in_embed.add_field(name=f"Common Fish: {cf}", value=f"Bass: {len([f for f in wf if f == cfArS[0]])}\nPike: {len([f for f in wf if f == cfArS[1]])}\nGrunt: {len([f for f in wf if f == cfArS[2]])}\nAngelfish: {len([f for f in wf if f == cfArS[3]])}\nGuppy: {len([f for f in wf if f == cfArS[4]])}\nAnchovy: {len([f for f in wf if f == cfArS[5]])}")
    in_embed.add_field(name=f"Common't Fish: {ctf}", value=f"Cod: {len([f for f in wf if f == ufArS[0]])}\nMarlin: {len([f for f in wf if f == ufArS[1]])}\nTang: {len([f for f in wf if f == ufArS[2]])}\nMudfish: {len([f for f in wf if f == ufArS[3]])}\nTrout: {len([f for f in wf if f == ufArS[4]])}\nEel: {len([f for f in wf if f == ufArS[5]])}")
    in_embed.add_field(name=f"Rare Fish: {rf}", value=f"Snapper: {len([f for f in wf if f == rfArS[0]])}\nTetra: {len([f for f in wf if f == rfArS[1]])}\nFirefish: {len([f for f in wf if f == rfArS[2]])}\nParrotfish: {len([f for f in wf if f == rfArS[3]])}\nCatfish: {len([f for f in wf if f == rfArS[4]])}\nFallfish: {len([f for f in wf if f == rfArS[5]])}")
    in_embed.add_field(name=f"Equipment", value=f"Your fishing boat is a {bt}, and you are fishing with a {rd}!")
    await ctx.response.send_message(embed=in_embed)

@bot.tree.command(description="Detailed fish storage information")
@app_commands.describe(page='The page of storage to view')
async def storage(ctx: discord.Interaction, page: int=1):
    num = len(users[f'{ctx.user.id}']['inv'])
    totVal = 0
    i = 0
    while (i < len(users[f'{ctx.user.id}']['inv'])):
        fish = users[f'{ctx.user.id}']['inv'][f'{i}']
        fq = fish.get("quality")
        fr = fish.get("rarity")
        ff = fish.get("from") != users[f'{ctx.user.id}']["pos"]
        fp = fish["prepBonus"]
        totVal += await value(fr, fq, ff, fp)
        i += 1
    if (page==1 and num >24):
        n = 1
        inv_embed = discord.Embed(
            title=str(f'{ctx.user.display_name}\'s storage | Page 1'),
            type="rich",
            description=f"You have {num} fish in your storage worth a combined {totVal} pearles. Here are the first 24."
        )
    elif (num <= 24):
        n = 1
        inv_embed = discord.Embed(
            title=str(f'{ctx.user.display_name}\'s storage | Page 1'),
            type="rich",
            description=f"You have {num} fish in your storage worth a combined {totVal} pearles."
        )
    elif (num >= page*24):
        n = 24*(page-1)+1
        inv_embed = discord.Embed(
            title=str(f'{ctx.user.display_name}\'s storage | Page {page}'),
            type="rich",
            description=f"You have {num} fish in your storage worth a combined {totVal} pearles. Here are fish {n}-{n+23}."
        )
    else:
        n = num-23
        inv_embed = discord.Embed(
            title=str(f'{ctx.user.display_name}\'s storage | Last page'),
            type="rich",
            description=f"You have {num} fish in your storage worth a combined {totVal} pearles. Here are fish {n}-{n+23}."
        )
    i = n-1
    while (i < len(users[f'{ctx.user.id}']['inv']) and i < n+23):
        fish = users[f'{ctx.user.id}']['inv'][f'{i}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.user.id}']["pos"]
        p = fish["prepBonus"]
        w = fish.get("weight")
        prp = " not" if (p == 0) else ""
        inv_embed.add_field(name=f'Slot {i+1}', value=f'A {rarityAr[r-1]} that weighs {round(w,2)} pounds and has{prp} been prepared.')
        i += 1
    await ctx.response.send_message(embed = inv_embed)


@bot.tree.command(description="Check the details of a specific fish in your inventory")
async def checkfish(ctx: discord.Interaction, slot: int):
    if (slot > 0 and slot <= len(users[f'{ctx.user.id}']['inv'])):
        fish = users[f'{ctx.user.id}']['inv'][f'{slot-1}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.user.id}']["pos"]
        p = fish["prepBonus"]
        prp = " not" if (p == 0) else ""
        await ctx.response.send_message(f'{ctx.user.display_name}, the fish in slot {slot} is a {rarityAr[r-1]} that is worth {await value(r,q,f,p)} perles and has{prp} been prepared.')
    else:
        await ctx.response.send_message('Invalid inventory slot')

@bot.tree.command(description="Cook a fish from your inventory")
async def cook(ctx: discord.Interaction, slot:int=1):
    await cookF.cook(ctx, slot)

class aqVw(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @ui.button(label="Transfer fish in", style=discord.ButtonStyle.green)
    async def trnIn(self, ctx: discord.Interaction, button: ui.button):
        aq = users[f'{ctx.user.id}']['equipment']['aquarium']
        if(len(aq['contents']) < aq['size']):
            await ctx.response.send_modal(trnIModal())
        else:
            await ctx.response.send_message("You can't fit any more fish in this aquarium!")
    @ui.button(label="Transfer fish out", style=discord.ButtonStyle.green)
    async def trnOut(self, ctx: discord.Interaction, button: ui.button):
        await ctx.response.send_modal(trnOModal())
    @ui.button(label="View fish", style=discord.ButtonStyle.green)
    async def vwFish(self, ctx: discord.Interaction, button: ui.button):
        aq = users[f'{ctx.user.id}']['equipment']['aquarium']
        aqFish = aq['contents']
        if (len(aqFish) == 0):
            await ctx.response.send_message("You don't have any fish in your aquarium yet!")
        else:
            aqEmbed = discord.Embed (title = f"{ctx.user.display_name}'s Aquarium", description=f'The fish in this tank make {aq.get("passiveVal")} pearles per hour!')
            i = 0
            while (i < len(aqFish) and i < 26):
                fish = aqFish[f'{i}']
                r = fish.get("rarity")
                w = fish.get("weight")
                aqEmbed.add_field(name=f'Fish {i+1}', value=f'A {rarityAr[r-1]} that weighs {round(w,2)} pounds.')
                i += 1
            await ctx.response.send_message(embed=aqEmbed)
    @ui.button(label="Collect passive income", style=discord.ButtonStyle.green)
    async def psCll(self, ctx: discord.Interaction, button: ui.button):
        aq = users[f'{ctx.user.id}']['equipment']['aquarium']
        if (len(aq['contents']) > 0):
            ttnxt = ((time.time()-aq['lastChecked'])/60)%60
            inc = math.floor((time.time()-aq['lastChecked'])/3600)
            users[f'{ctx.user.id}']['equipment']['aquarium']['lastChecked'] = (time.time() - ttnxt*60)
            users[f'{ctx.user.id}']['money'] = users[f'{ctx.user.id}']['money'] + inc*aq['passiveVal']
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            await ctx.response.send_message(f"You made {inc*aq['passiveVal']} from the fish in your tank. You have {math.ceil(60-ttnxt)} more minutes before you can collect income again!")
        else:
            await ctx.response.send_message("You have no fish in your aquarium right now!")
class trnIModal(ui.Modal, title="Transfer In"):
    slot = ui.TextInput(label="Fish Slot Number")
    async def on_submit(self, ctx: discord.Interaction):
        slot = int(f'{self.slot}') - 1
        userF = users[f'{ctx.user.id}']['inv']
        if (userF[f'{slot}'] != None):
            if (userF[f'{slot}']["prepBonus"] == 0):
                aqC = users[f'{ctx.user.id}']['equipment']['aquarium']['contents']
                aqC[f'{len(aqC)}'] = userF[f'{slot}']
                usF = userF[f'{slot}']
                r = usF['rarity']
                q = usF['quality']
                val = await value(r, q, False, 0) 
                users[f'{ctx.user.id}']['equipment']['aquarium']['passiveVal'] = users[f'{ctx.user.id}']['equipment']['aquarium']['passiveVal'] + val
                users[f'{ctx.user.id}']['equipment']['aquarium']['lastChecked'] = time.time()
                users[f'{ctx.user.id}']['equipment']['aquarium']['contents'] = aqC
                newInv = {}
                i = 0
                j = 0
                while i < len(users[f'{ctx.user.id}']['inv']):
                    if i != slot:
                        newInv[f'{j}'] = users[f'{ctx.user.id}']['inv'][f'{i}']
                        j += 1
                    i += 1
                users[f'{ctx.user.id}']['inv'] = newInv
                with open('users.json', 'w') as outfile:
                    json.dump(users, outfile)
                await ctx.response.send_message("Fish transferred. Note: Transferring fish resets passive time.")
            else:
                await ctx.response.send_message("You can't transfer a cooked fish!")
        else:
            await ctx.response.send_message("Invalid inventory slot.")

class trnOModal(ui.Modal, title="Transfer Out"):
    slot = ui.TextInput(label="Fish Slot Number")
    async def on_submit(self, ctx: discord.Interaction):
        slot = int(f'{self.slot}') - 1
        aqC = users[f'{ctx.user.id}']['equipment']['aquarium']['contents']
        if (aqC[f'{slot}'] != None):
            userF = users[f'{ctx.user.id}']['inv']
            aqC = users[f'{ctx.user.id}']['equipment']['aquarium']['contents']
            userF[f'{len(userF)}'] = aqC[f'{slot}']
            usF = aqC[f'{slot}']
            r = usF['rarity']
            q = usF['quality']
            val = await value(r, q, False, 0) 
            users[f'{ctx.user.id}']['equipment']['aquarium']['passiveVal'] = users[f'{ctx.user.id}']['equipment']['aquarium']['passiveVal'] - val
            if (len(aqC) == 1):
                users[f'{ctx.user.id}']['equipment']['aquarium']['passiveVal'] = 0
            users[f'{ctx.user.id}']['equipment']['aquarium']['lastChecked'] = time.time()
            users[f'{ctx.user.id}']['inv'] = userF
            newInv = {}
            i = 0
            j = 0
            while i < len(aqC):
                if i != slot:
                    newInv[f'{j}'] = aqC[f'{i}']
                    j += 1
                i += 1
            users[f'{ctx.user.id}']['equipment']['aquarium']['contents'] = newInv
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            await ctx.response.send_message("Fish transferred. Note: Transferring fish resets passive time.")
        else:
            await ctx.response.send_message("Invalid fish slot.")

@bot.tree.command(description="View the fish in your aquarium")
async def aquarium(ctx: discord.Interaction):
    if (users[f'{ctx.user.id}']['equipment'].get('aquarium') == None):
        await ctx.response.send_message('You don\'t have an aquarium yet! You can buy one in the equipment shop.')
    else:
        await ctx.response.send_message("What would you like to do?", view=aqVw())

unrevealed = [0,0,0]
sand = [243,211,65]
grass = [0,154,23]
shallow = [0,83,255]
deep = [9,1,185]
dock = [169,159,132]
boat = [114,90,61]
lastLoc = [200,1,43]

mp = [['d','d','d','d','d','s','i','i','i','i','i','s','s','d','d','d','d','d','d','d'],['d','d','d','d','d','s','s','i','i','i','i','s','s','d','d','d','d','d','d','d'],['d','d','d','d','d','d','s','s','s','s','s','s','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','s','s','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','b','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['s','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['s','s','s','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['i','s','s','s','s','d','d','d','d','d','d','d','d','d','d','d','d','d','d','d'],['i','i','i','i','s','s','s','d','d','d','d','d','d','d','d','d','d','d','d','d'],['g','g','i','i','i','i','s','d','d','d','d','d','d','d','d','d','d','b','d','d'],['g','g','g','i','i','i','k','k','k','d','d','d','d','d','d','d','d','d','d','d'],['g','b','g','g','i','i','s','s','d','d','d','d','d','d','d','d','d','d','d','d'],['g','g','g','g','g','i','i','s','d','d','d','d','d','d','d','d','d','d','d','d']]
starting = [[14,0],[15,0],[15,1],[15,2],[15,3],[16,0],[16,1],[16,2],[16,3],[16,4],[16,5],[17,0],[17,1],[17,2],[17,3],[17,4],[17,5],[17,6],[17,7],[17,8],[18,0],[18,1],[18,2],[18,3],[18,4],[18,5],[19,0],[19,1],[19,2],[19,3],[19,4],[19,5],[19,6]]
@bot.tree.command(description="View where you've been on the map!")
async def map(ctx: discord.Interaction):
    if (users[f'{ctx.user.id}'].get("map") == None):
        users[f'{ctx.user.id}']['map'] = {"explored": [[17,6]], "last": [17,6]}
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    explored = users[f'{ctx.user.id}']['map']['explored']
    last = users[f'{ctx.user.id}']['map']['last']
    i = 0
    j = 0
    r = []
    p = []
    for i in range(len(mp)*30):
        v = math.floor(i/30)
        for j in range(len(mp[0])):
            tp = mp[v][j]
            col = unrevealed
            if (tp == 'd'):
                col = deep
            elif (tp == 's'):
                col = shallow
            elif (tp == 'g'):
                col = grass
            elif (tp == 'k'):
                col = dock
            elif (tp == 'b'):
                col = boat
            elif (tp == 'i'):
                col = sand
            else:
                col = lastLoc
            if not [v,j] in explored and not [v,j] in starting:
                col = unrevealed
            for k in range(30):
                r.append(col[0])
                r.append(col[1])
                r.append(col[2])
        p.append(r)
        r = []
    rr = 0 + 30*last[0]
    cc = 0 + 90*last[1]
    i = 0
    j = 0
    for i in range(30):
        for j in range(90):
            if (i < 3 or i > 26):
                p[rr+i][cc+j] = lastLoc[j%3]
            elif (j < 9 or j > 78):
                p[rr+i][cc+j] = lastLoc[j%3]
    f = open('swatch.png', 'wb')
    w = png.Writer(600,600, greyscale=False)
    w.write(f, p)
    f.close()
    await ctx.response.send_message("Here's what you've found!", file=discord.File('swatch.png'))

class stVw(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @ui.button(label="Fish", style=discord.ButtonStyle.green)
    async def mrkt(self, ctx: discord.Interaction, button: ui.button):
        market_embed = discord.Embed (title = "The Net, for fish", type = 'rich')
        page = ""
        for i in range(10):
            marketSlot = random.randint(0,99999)
            marketFish = market.get(f"slot{marketSlot}")
            while (marketFish.get("from") == users.get(f'{ctx.user.id}').get("pos") or marketFish.get("from") == -2):
                marketSlot = random.randint(0,99999)
                marketFish = market.get(f"slot{marketSlot}")
            prep = "prepared" if (marketFish.get("prepBonus") > 0) else "Not prepared"
            page += f'**Slot**: {marketSlot}, Origin: {marketFish.get("from")}, Quality: {await qualify(marketFish.get("quality"))}, Type: {rarityAr[marketFish.get("rarity")-1]}. {prep}. \n'
        market_embed.add_field(name="The one stop shop for bass and cod! (and other things maybe)", value = f'{page}', inline = False)
        market_embed.set_thumbnail(url="https://i.etsystatic.com/15020412/r/il/455abc/2328156575/il_1588xN.2328156575_4m7l.jpg")
        await ctx.response.send_message(embed=market_embed, view=mkVw())
    @ui.button(label="Equipment", style=discord.ButtonStyle.green)
    async def store(self, ctx: discord.Interaction, button: ui.button):
        store_embed = discord.Embed (title = "Jerry's Bait Shop (You know the place)", type = "rich")
        fishEq = equipment.get("fishEq")
        rods = fishEq.get("fishRods")
        boats = fishEq.get("boats")
        aquariums = equipment.get("aquariums")
        j = 1
        rdDesc = ["This rod also increases your fish's rarity and weight by 5%!", "With this rod, you have a 5% chance to catch two more fish, and increases your fish's weight by 1%!", "You'll get a 3% rarity boost with this rod alongside a 10% chance to catch one more fish!"]
        for i in range(3):
            rod = rods.get(f'{i+1}')
            store_embed.add_field(name = f'{j}: {rod["name"]}', value = f'This rod fishes at {int(rod["quality"]*20)} fish per minute and goes for {rod["price"]} pearles! {rdDesc[i]} :oyster:', inline = False)
            j=j+1    
        for i in range(3):
            boat = boats.get(f'{i+1}')
            store_embed.add_field(name = f'{j}: {boat["name"]}', value = f'This boat lets you fish for {boat["dur"]} seconds at a time and goes for {boat["price"]} pearles! :person_rowing_boat:', inline = False)
            j=j+1
        for i in range(3):
            aquarium = aquariums.get(f'{i+1}')
            store_embed.add_field(name = f'{j}: {aquarium["name"]}', value = f'This tank fits {aquarium["size"]} fish and goes for {aquarium["price"]} pearles! :bubbles:', inline=False)
            j=j+1
        await ctx.response.send_message(embed=store_embed, view=eqVw())
    @ui.button(label="License", style=discord.ButtonStyle.green)
    async def lics(self, ctx: discord.Interaction, button: ui.button):
        # userInfo = users[f'{ctx.user.id}']
        # uLic = userInfo["license"]
        # uFTot = 0
        # for type in userInfo["fishlog"]:
        #     uFTot = uFTot + userInfo["fishlog"][type]
        # if uLic < 2:
        #     fLCount = [50, 1000]
        #     fLPrice = [100, 5000]
        #     if uFTot >= fLCount[uLic]:
        #         if userInfo["money"] >= fLPrice[uLic]:
        #            await ctx.response.send_message(f"You're about to upgrade your license to tier {uLic + 1}. This will cost {fLPrice[uLic]} pearles. Do you want to continue?", view=lsVw(), ephemeral=True)
        #         else:
        #             await ctx.response.send_message(f"{ctx.user.display_name}, you need to more perles before you can upgrade your license!")
        #     else:
        #         await ctx.response.send_message(f"{ctx.user.display_name}, you need to catch more fish before you can upgrade your license!")
        # else:
        #     await ctx.response.send_message(f"{ctx.user.display_name}, you currently have the highest level license available!")
        await ctx.response.send_message("Licenses are currently undergoing a rework.")
    @ui.button(label="Cooking EQ", style=discord.ButtonStyle.green)
    async def chefsp(self, ctx: discord.Interaction, button: ui.button):
        await cookF.chef(self, ctx, button)

class mkVw(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @ui.button(label="Make a purchase", style=discord.ButtonStyle.green)
    async def mktP(self, ctx: discord.Interaction, button: ui.button):
        await ctx.response.send_modal(FModal())

class eqVw(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @ui.button(label="Make a purchase", style=discord.ButtonStyle.green)
    async def eqpP(self, ctx: discord.Interaction, button: ui.button):
        await ctx.response.send_modal(EModal())

class lsVw(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
    @ui.button(label="Purchase", style=discord.ButtonStyle.green)
    async def licsP(self, ctx: discord.Interaction, button: ui.button):
        userInfo = users[f'{ctx.user.id}']
        uLic = userInfo["license"]
        fLPrice = [100, 5000]
        moneys = users[f'{ctx.user.id}']["money"]
        if (moneys >= fLPrice[uLic]):
            users[f'{ctx.user.id}']['license'] = uLic+1
            users[f'{ctx.user.id}']['money'] = moneys - fLPrice[uLic]
            await ctx.response.send_message(f"{ctx.user.display_name} you upgraded your license to class {uLic+1}! You now have {moneys - fLPrice[uLic]} perles. :card_index:")
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
        else:
            await ctx.response.send_message("You don't have the pearles to make this purchase! :chart_with_downwards_trend:")

class FModal(ui.Modal, title='Market Purchase'):
    slot = ui.TextInput(label="Market Slot Number")
    async def on_submit(self, ctx: discord.Interaction):
        try:
            slot = int(f'{self.slot}')
            if (slot >= 0 and slot <= 99999):
                marketFish = market.get(f'slot{slot}')
                q = marketFish["quality"]
                r = marketFish["rarity"]
                f = marketFish["from"] != users[f'{ctx.user.id}']["pos"]
                if (f):
                    p = marketFish["prepBonus"]
                    cost = await value(r,q,False,p)
                    if (users[f'{ctx.user.id}']["money"] >= cost):
                        users[f'{ctx.user.id}']["money"] -= cost
                        moneys = users[f'{ctx.user.id}']["money"]
                        userInv = users[f'{ctx.user.id}']['inv'] 
                        users[f'{ctx.user.id}']["inv"][f'{len(userInv)}'] = marketFish
                        market[f'slot{slot}'] = await pullFish(users[f'{ctx.user.id}']['pos'], [0,0], users[f'{ctx.user.id}']['location'], ctx.user.id)
                        await ctx.response.send_message(f"{ctx.user.display_name} you bought the fish for {cost} perles! You now have {moneys} perles. :label:")
                        with open('users.json', 'w') as outfile:
                            json.dump(users, outfile)
                        with open('market.json', 'w') as outfile:
                            json.dump(market, outfile)
                    else:
                        await ctx.response.send_message(f"{ctx.user.display_name}, you do not have enough perles to make this transaction! :chart_with_downwards_trend:")
                else:
                    await ctx.response.send_message(f"{ctx.user.display_name}, this was originally your fish! You can't purchase it again.")
            else:
                await ctx.response.send_message("This is not a valid slot.")
        except:
            await ctx.response.send_message("This is not a valid slot.")

eqCost = [100, 100, 100, 300, 5000, 50000, 100, 2500, 40000, 200, 500]
class EModal(ui.Modal, title="Equipment Purchase"):
    slot = ui.TextInput(label="Equipment Slot Number")
    async def on_submit(self, ctx: discord.Interaction):
        #try:
            slot = int(f'{self.slot}')
            if (slot < len(eqCost)+1):
                cost = eqCost[slot-1]
                if (users[f'{ctx.user.id}']["money"] >= cost):
                    await ctx.channel.send('As the bot is still in early development, these items are likely to be reverted as we work on balance')
                    users[f'{ctx.user.id}']["money"] -= cost
                    moneys = users[f'{ctx.user.id}']["money"]
                    userEq = users[f'{ctx.user.id}']['equipment']
                    fishEq = equipment.get("fishEq")
                    rods = fishEq.get("fishRods")
                    boats = fishEq.get("boats")
                    aquariums = equipment.get("aquariums")
                    if (slot > 6):
                        if (userEq.get("aquarium") != None):
                            if (len(userEq["aquarium"]["contents"]) > aquariums[f'{slot-6}']["size"]):
                                users[f'{ctx.user.id}']["money"] += cost
                                await ctx.response.send_message(f"{ctx.user.display_name} your current aquarium has too many fish in it to downgrade!")      
                            else:
                                tempAq = aquariums[f'{slot-6}']
                                if (users[f'{ctx.user.id}']["aquariums"]["owned"][tempAq["name"]]):
                                    users[f'{ctx.user.id}']["money"] += cost
                                    await ctx.response.send_message(f"{ctx.user.display_name}, you already have that!")
                                else:
                                    tempAq = aquariums[f'{slot-6}']
                                    tempAq["contents"] = userEq["aquarium"]["contents"]
                                    tempAq["passiveVal"] = userEq["aquarium"]["passiveVal"]
                                    tempAq["lastChecked"] = userEq["aquarium"]["lastChecked"]
                                    userEq['aquarium'] = tempAq
                        else:
                            userEq['aquarium'] = aquariums[f'{slot-6}']
                    elif (slot > 3):
                        if (users[f'{ctx.user.id}']["owned"]["boats"][boats[f'{slot-3}']["name"]]):
                            users[f'{ctx.user.id}']["money"] += cost
                            await ctx.response.send_message(f"{ctx.user.display_name}, you already have that!")
                        else:
                            userEq['boat'] = boats[f'{slot-3}']
                    else: 
                        if (users[f'{ctx.user.id}']["owned"]["fishEq"][rods[f'{slot}']["name"]]):
                            users[f'{ctx.user.id}']["money"] += cost
                            await ctx.response.send_message(f"{ctx.user.display_name}, you already have that!")
                        else:
                            userEq['fishEq'] = rods[f'{slot}']
                    users[f'{ctx.user.id}']['equipment'] = userEq
                    await ctx.response.send_message(f"{ctx.user.display_name} you bought the item for {cost} perles! You now have {moneys} perles. :label:")
                    with open('users.json', 'w') as outfile:
                        json.dump(users, outfile)
                else:
                    await ctx.response.send_message(f"{ctx.user.display_name}, you do not have enough perles to make this transaction! :chart_with_downwards_trend:")   
            else:
                await ctx.response.send_message("Invalid equipment slot.")
        #except:
        #    await ctx.response.send_message("This is not a valid slot.")

@bot.tree.command(description="Purchase items from the shop")
async def buy(ctx: discord.Interaction):
    await ctx.response.send_message("What are you looking to buy?", view=stVw())

@bot.tree.command(description="View your current pearle count")
async def pearles(ctx: discord.Interaction):
    moneys = users[f'{ctx.user.id}']["money"]
    await ctx.response.send_message(f"You currently have {moneys} pearles!")

bot.run(tkn)