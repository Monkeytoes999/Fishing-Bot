from asyncio import base_tasks
from asyncio.windows_events import NULL
import discord
from discord.ext import tasks, commands
import random
import json
import time
import math

tfile = open('token.txt','r')
token = tfile.readline()
tfile.close()

file = open('users.json',)
users = json.load(file)
mFile = open('market.json',)
market = json.load(mFile)
eqFile = open('equipment.json')
equipment = json.load(eqFile)
lcFile = open('locations.json')
locations = json.load(lcFile)

bot = commands.Bot(command_prefix =['f.', 'fb ', 'F.', 'Fb ', 'FB ', 'fB '], case_insensitive=(True))
TOKEN = token

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user.name}')
    print (f'Ok {bot.user.name} is online now')

async def createUser(userID):
    users[f'{userID}'] = {
        "pos": len(users),
        "money": 0,
        "fishlog": {
        "bass": 0, "pike": 0, "grunt": 0, "angelfish": 0, "guppy": 0,
        "cod": 0, "marlin": 0, "tang": 0, "mudfish": 0, "trout": 0,
        "snapper": 0, "tetra": 0, "firefish": 0, "parrotfish": 0, "catfish": 0,
        "bonefish": 0
        },
        "equipment": {"fishEq":{"name": "Stick", "quality": 0.1, "price": 0}, "boat":{"name": "raft", "cooldown": 5, "dur": 5, "price": 0}, "seasoning": 0},
        "inv": {},
        "contacts": {},
        "reputation": 1,
        "lastFish": 0,
        "isFishing": 0,
        "lastDur": 0,
        "lastCd": 0
    }
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile) 
           
async def pullFish(userPos, userLoc):
    rr = await rarity(userLoc)
    fish = {"from":userPos, "rarity": rr, "quality": random.random(), "prepBonus": 0, "weight": 1}
    return fish

rarityAr = ['common bass','common pike','common grunt','common\'t cod','common\'t marlin','common\'t tang','rare snapper','rare tetra','rare firefish', 'bonefish', 'common angelfish', 'common guppy', 'common\'t mudfish', 'common\'t trout', 'rare parrotfish', 'rare catfish', 'rubber ducky']
rarityGroups = ['common', 'common', 'common', 'commont', 'commont', 'commont', 'rare', 'rare', 'rare', 'event', 'common', 'common', 'commont', 'commont', 'rare', 'rare', 'novelty']
fishNames = ['bass', 'pike', 'grunt', 'cod', 'marlin', 'tang', 'snapper', 'tetra', 'firefish', 'bonefish', 'angelfish', 'guppy', 'mudfish', 'trout', 'parrotfish', 'catfish', 'rubber ducky']
fishWeights = []
cfArS = [1, 2, 3, 11, 12]
ufArS = [4, 5, 6, 13, 14]
rfArS = [7, 8, 9, 15, 16]

#fishAr = [African glass catfish,African lungfish,Aholehole,Airbreathing catfish,Airsac catfish,Alaska blackfish,Albacore,Alewife,Alfonsino,Algae eater,Alligatorfish,Alligator gar,Amberjack,American sole,Amur pike,Anchovy,Anemonefish,Angelfish,Angler,Angler catfish,Anglerfish,Antarctic cod,Antarctic icefish,Antenna codlet,Arapaima,Archerfish,Arctic char,Armored gurnard,Armored searobin,Armorhead,Armorhead catfish,Armoured catfish,Arowana,Arrowtooth eel,Asian carps,Asiatic glassfish,Atka mackerel,Atlantic bonito,Atlantic cod,Atlantic herring,Atlantic salmon,Atlantic sharpnose shark,Atlantic saury,Atlantic silverside,Australasian salmon,Australian grayling,Australian herring,Australian lungfish,Australian prowfish,Ayu,Baikal oilfish,Bala shark,Ballan wrasse,Bamboo shark,Banded killifish,Bandfish,Banjo,Bangus,Banjo catfish,Barb,Barbel,Barbeled dragonfish,Barbeled houndshark,Barbel-less catfish,Barfish,Barracuda,Barracudina,Barramundi,Barred danio,Barreleye,Basking shark,Bass,Basslet,Batfish,Bat ray,Beachsalmon,Beaked salmon,Beaked sandfish,Beardfish,Beluga sturgeon,Bengal danio,Betta,Bichir,Bicolor goat fish,Bigeye,Bigeye squaretail,Bighead carp,Bigmouth buffalo,Bigscale,Bigscale pomfret,Billfish,Bitterling,Black angelfish,Black bass,Black dragonfish,Blackchin,Blackfin Tuna,Blackfish,Black neon tetra,Blacktip reef shark,Black mackerel,Black scalyfin,Black sea bass,Black scabbardfish,Black swallower,Black tetra,Black triggerfish,Bleak,Blenny,Blind goby,Blind shark,Blobfish,Blowfish,Blue catfish,Blue danio,Blue-redstripe danio,Blue eye trevalla,Bluefin tuna,Bluefish,Bluegill,Blue gourami,Blue shark,Blue triggerfish,Blue whiting,Bluntnose knifefish,Bluntnose minnow,Boafish,Boarfish,Bobtail snipe eel,Bocaccio,Boga,Bombay duck,Bonefish,Bonito,Bonnethead shark,Bonnetmouth,Bonytail,Bonytongue,Bowfin,Boxfish,Bramble shark,Bream,Brill,Bristlemouth,Bristlenose catfish,Broadband dogfish,Bronze corydoras,Brook lamprey,Brook stickleback,Brook trout,Brotula,Brown trout,Buffalo fish,Bullhead,Bullhead shark,Bull shark,Bull trout,Burbot,Bumblebee goby,Buri,Burma danio,Burrowing goby,Butterfish,Butterfly ray,Butterflyfish,California flyingfish,California halibut,Canary rockfish,Candiru,Candlefish,Capelin,Cardinalfish,Cardinal tetra,Carp,Carpetshark,Carpsucker,Catalufa,Catfish,Catla,Cat shark,Cavefish,Celebes rainbowfish,Central mudminnow,Chain pickerel,Channel bass,Channel catfish,Char,Cherry salmon,Chimaera,Chinook salmon,Cherubfish,Chub,Chubsucker,Chum salmon,Cichlid,Cisco,Climbing catfish,Climbing gourami,Climbing perch,Clingfish,Clownfish,Clown loach,Clown triggerfish,Cobbler,Cobia,Cod,Codlet,Codling,Coelacanth,Coffinfish,Coho salmon,Coley,Collared carpetshark,Collared dogfish,Colorado squawfish,Combfish,Combtail gourami,Combtooth blenny,Common carp,Common tunny,Conger eel,Convict blenny,Convict cichlid,Cookie-cutter shark,Coolie loach,Cornetfish,Cowfish,Cownose ray,Cow shark,Crappie,Creek chub,Crestfish,Crevice kelpfish,Croaker,Crocodile icefish,Crocodile shark,Crucian carp,Cuckoo wrasse,Cusk,Cusk-eel,Cutlassfish,Cutthroat eel,Cutthroat trout,Dab,Dace,Daggertooth pike conger,Damselfish,Danio,Darter,Dartfish,Dealfish,Death Valley pupfish,Deep sea eel,Deep sea smelt,Deepwater cardinalfish,Deepwater flathead,Deepwater stingray,Delta smelt,Demoiselle,Denticle herring,Desert pupfish,Devario,Devil ray,Dhufish,Discus,Dogfish,Dogfish shark,Dogteeth tetra,Dojo loach,Dolly Varden trout,Dolphin fish,Dorab wolf-herring,Dorado,Dory,Dottyback,Dragonet,Dragonfish,Dragon goby,Driftfish,Driftwood catfish,Drum,Duckbill,Duckbill eel,Dusky grouper,Dusky shark,Dwarf gourami,Dwarf loach,Eagle ray,Earthworm eel,Eel,Eel cod,Eel-goby,Eelpout,Eeltail catfish,Elasmobranch,Electric catfish,Electric eel,Electric knifefish,Electric ray,Elephant fish,Elephantnose fish,Elver,Ember parrotfish,Emerald catfish,Emperor,Emperor angelfish,Emperor bream,Escolar,Eucla cod,Eulachon,European chub,European eel,European flounder,European minnow,European perch,False brotula,False cat shark,False moray,False trevally,Fangtooth,Fathead sculpin,Featherback,Fierasfer,Fire goby,Filefish,Finback cat shark,Fingerfish,Fire bar danio,Firefish,Flabby whale fish,Flagblenny,Flagfin,Flagfish,Flagtail,Flashlight fish,Flatfish,Flathead,Flathead catfish,Flier,Flounder,Flying gurnard,Flying fish,Footballfish,Forehead brooder,Four-eyed fish,French angelfish,Freshwater eel,Freshwater hatchetfish,Freshwater shark,Frigate mackerel,Frilled shark,Frogfish,Frogmouth catfish,Fusilier fish,Galjoen fish,Ganges shark,Gar,Garden eel,Garibaldi,Garpike,Ghost fish,Ghost flathead,Ghost knifefish,Ghost pipefish,Ghost shark,Ghoul,Giant danio,Giant gourami,Giant sea bass,Gibberfish,Gila trout,Gizzard shad,Glass catfish,Glassfish,Glass knifefish,Glowlight danio,Goatfish,Goblin shark,Goby,Golden dojo,Golden loach,Golden shiner,Golden trout,Goldeye,Goldfish,Gombessa,Goosefish,Gopher rockfish,Gourami,Grass carp,Graveldiver,Grayling,Gray mullet,Gray reef shark,Great white shark,Green swordtail,Greeneye,Greenling,Grenadier,Green spotted puffer,Ground shark,Grouper,Grunion,Grunt,Grunter,Grunt sculpin,Gudgeon,Guitarfish,Gulf menhaden,Gulper eel,Gulper,Gunnel,Guppy,Gurnard,Haddock,Hagfish,Hairtail,Hake,Halfbeak,Halfmoon,Halibut,Halosaur,Hamlet,Hammerhead shark,Hammerjaw,Handfish,Hardhead catfish,Harelip sucker,Hatchetfish,Hawkfish,Herring,Herring smelt,Hickory Shad,Hillstream loach,Hog sucker,Hoki,Horn shark,Horsefish,Houndshark,Huchen,Humuhumunukunukuapua/'a,Hussar,Icefish,Ide,Ilish/Hilsha,Inanga,Inconnu,Jack,Jackfish,Jack Dempsey,Japanese eel,Javelin,Jawfish,Jellynose fish,Jewelfish,Jewel tetra,Jewfish,John Dory,Kafue pike,Kahawai,Kaluga,Kanyu,Kelp perch,Kelpfish,Killifish,King of the herrings,Kingfish,King-of-the-salmon,Kissing gourami,Knifefish,Knifejaw,Koi,Kokanee,Kokopu,Kuhli loach,Labyrinth fish,Ladyfish,Lake chub,Lake trout,Lake whitefish,Lampfish,Lamprey,Lancetfish,Lanternfish,Largemouth bass,Leaffish,Leatherjacket,Lefteye flounder,Lemon shark,Lemon sole,Lemon tetra,Lenok,Leopard danio,Lightfish,Limia,Lined sole,Ling,Ling cod,Lionfish,Livebearer,Lizardfish,Loach,Loach catfish,Loach goby,Loach minnow,Longfin,Longfin dragonfish,Longfin escolar,Longfin smelt,Long-finned char,Long-finned pike,Long-finned sand diver,Longjaw mudsucker,Longneck eel,Longnose chimaera,Longnose dace,Longnose lancetfish,Longnose sucker,Longnose whiptail catfish,Long-whiskered catfish,Loosejaw,Lost River sucker,Louvar,Loweye catfish,Luderick,Luminous hake,Lumpsucker,Lungfish,Mackerel,Mackerel shark,Madtom,Mahi-mahi,Mahseer,Mail-cheeked fish,Mako shark,Mandarinfish,Manefish,Man-of-war fish,Manta ray,Marblefish,Marine hatchetfish,Marlin,Masu salmon,Medaka,Medusafish,Megamouth shark,Menhaden,Merluccid hake,Mexican golden trout,Midshipman fish,Milkfish,Minnow,Minnow of the deep,Modoc sucker,Mojarra,Mola mola,Monkeyface prickleback,Monkfish,Mooneye,Moonfish,Moorish idol,Mora,Moray eel,Morid cod,Morwong,Moses sole,Mosquitofish,Mouthbrooder,Mozambique tilapia,Mrigal,Mud catfish,Mudfish,Mudminnow,Mud minnow,Mudskipper,Mudsucker,Mullet,Mummichog,Murray cod,Muskellunge,Mustache triggerfish,Mustard eel,Naked-back knifefish,Nase,Needlefish,Neon tetra,New World rivuline,New Zealand sand diver,New Zealand smelt,Nibble fish,Noodlefish,North American darter,North American freshwater catfish,North Pacific daggertooth,Northern anchovy,Northern clingfish,Northern lampfish,Northern pike,Northern sea robin,Northern squawfish,Northern stargazer,Notothen,Nurseryfish,Nurse shark,Oarfish,Ocean perch,Ocean sunfish,Oceanic whitetip shark,Oilfish,Oldwife,Old World knifefish,Olive flounder,Opah,Opaleye,Orange roughy,Orangespine unicorn fish,Orangestriped triggerfish,Orbicular batfish,Orbicular velvetfish,Oregon chub,Orfe,Oriental loach,Oscar,Owens pupfish,Pacific albacore,Pacific cod,Pacific hake,Pacific herring,Pacific lamprey,Pacific salmon,Pacific saury,Pacific trout,Pacific viperfish,Paddlefish,Pancake batfish,Panga,Paradise fish,Parasitic catfish,Parore,Parrotfish,Peacock flounder,Peamouth,Pearleye,Pearlfish,Pearl danio,Pearl perch,Pelagic cod,Pelican eel,Pelican gulper,Pencil catfish,Pencilfish,Pencilsmelt,Peppered corydoras,Perch,Peters' elephantnose fish,Pickerel,Pigfish,Pike conger,Pike eel,Pike,Pikeblenny,Pikeperch,Pilchard,Pilot fish,Pineapplefish,Pineconefish,Pink salmon,Píntano,Pipefish,Piranha,Pirarucu,Pirate perch,Plaice,Platy,Platyfish,Pleco,Plownose chimaera,Poacher,Pollyfish,Pollock,Pomfret,Pompano,Pompano dolphinfish,Ponyfish,Popeye catalufa,Porbeagle shark,Porcupinefish,Porgy,Port Jackson shark,Powen,Prickleback,Pricklefish,Prickly shark,Prowfish,Pufferfish,Pumpkinseed,Pupfish,Pygmy sunfish,Queen danio,Queen parrotfish,Queen triggerfish,Quillback,Quillfish,Rabbitfish,Raccoon butterfly fish,Ragfish,Rainbow trout,Rainbowfish,Rasbora,Ratfish,Rattail,Ray,Razorback sucker,Razorfish,Red grouper,Red salmon,Red snapper,Redfin perch,Redfish,Redhorse sucker,Redlip blenny,Redmouth whalefish,Redtooth triggerfish,Red velvetfish,Red whalefish,Reedfish,Reef triggerfish,Remora,Requiem shark,Ribbon eel,Ribbon sawtail fish,Ribbonfish,Rice eel,Ricefish,Ridgehead,Riffle dace,Righteye flounder,Rio Grande perch,River loach,River shark,River stingray,Rivuline,Roach,Roanoke bass,Rock bass,Rock beauty,Rock cod,Rocket danio,Rockfish,Rockling,Rockweed gunnel,Rohu,Ronquil,Roosterfish,Ropefish,Rough scad,Rough sculpin,Roughy,Roundhead,Round herring,Round stingray,Round whitefish,Rudd,Rudderfish,Ruffe,Russian sturgeon,Sábalo,Sabertooth,Saber-toothed blenny,Sabertooth fish,Sablefish,Sacramento blackfish,Sacramento splittail,Sailfin silverside,Sailfish,Salamanderfish,Salmon,Salmon shark,Sandbar shark,Sandburrower,Sand dab,Sand diver,Sand eel,Sandfish,Sand goby,Sand knifefish,Sand lance,Sandperch,Sandroller,Sand stargazer,Sand tiger,Sand tilefish,Sandbar shark,Sarcastic fringehead,Sardine,Sargassum fish,Sauger,Saury,Sawfish,Saw shark,Sawtooth eel,Scabbard fish,Scaly dragonfish,Scat,Scissortail rasbora,Scorpionfish,Sculpin,Scup,Sea bass,Sea bream,Sea catfish,Sea chub,Sea devil,Sea dragon,Sea lamprey,Sea raven,Sea snail,Sea toad,Seahorse,Seamoth,Searobin,Sevan trout,Sergeant major,Shad,Shark,Sharksucker,Sharpnose puffer,Sheatfish,Sheepshead,Sheepshead minnow,Shiner,Shortnose chimaera,Shortnose sucker,Shovelnose sturgeon,Shrimpfish,Siamese fighting fish,Sillago,Silver carp,Silver dollar,Silver dory,Silver hake,Silverside,Silvertip tetra,Sind danio,Sixgill ray,Sixgill shark,Skate,Skilfish,Skipjack tuna,Slender mola,Slender snipe eel,Sleeper,Sleeper shark,Slickhead,Slimehead,Slimy mackerel,Slimy sculpin,Slipmouth,Smalleye squaretail,Smalltooth sawfish,Smelt,Smelt-whiting,Smooth dogfish,Snailfish,Snake eel,Snakehead,Snake mackerel,Snapper,Snipe eel,Snipefish,Snook,Snubnose eel,Snubnose parasitic eel,Sockeye salmon,Soldierfish,Sole,South American darter,South American lungfish,Southern Dolly Varden,Southern flounder,Southern hake,Southern sandfish,Southern smelt,Spadefish,Spaghetti eel,Spanish mackerel,Spearfish,Speckled trout,Spiderfish,Spikefish,Spinefoot,Spiny basslet,Spiny dogfish,Spiny dwarf catfish,Spiny eel,Spinyfin,Splitfin,Spookfish,Spotted climbing perch,Spotted danio,Spottail pinfish,Sprat,Springfish,Squarehead catfish,Squaretail,Squawfish,Squeaker,Squirrelfish,Staghorn sculpin,Stargazer,Starry flounder,Steelhead,Stickleback,Stingfish,Stingray,Stonecat,Stonefish,Stoneroller minnow,Stream catfish,Striped bass,Striped burrfish,Sturgeon,Sucker,Suckermouth armored catfish,Summer flounder,Sundaland noodlefish,Sunfish,Surf sardine,Surfperch,Surgeonfish,Swallower,Swamp-eel,Swampfish,Sweeper,Swordfish,Swordtail,Tadpole cod,Tadpole fish,Tailor,Taimen,Tang,Tapetail,Tarpon,Tarwhine,Telescopefish,Temperate bass,Temperate ocean-bass,Temperate perch,Tench,Tenpounder,Tenuis,Tetra,Thorny catfish,Thornfish,Threadfin,Threadfin bream,Thread-tail,Three spot gourami,Threespine stickleback,Three-toothed puffer,Thresher shark,Tidewater goby,Tiger barb,Tigerperch,Tiger shark,Tiger shovelnose catfish,Tilapia,Tilefish,Titan triggerfish,Toadfish,Tommy ruff,Tompot blenny,Tonguefish,Tope,Topminnow,Torpedo,Torrent catfish,Torrent fish,Trahira,Treefish,Trevally,Triggerfish,Triplefin blenny,Triplespine,Tripletail,Tripod fish,Trout,Trout cod,Trout-perch,Trumpeter,Trumpetfish,Trunkfish,Tubeblenny,Tube-eye,Tube-snout,Tubeshoulder,Tui chub,Tuna,Turbot,Two spotted goby,Uaru,Unicorn fish,Upside-down catfish,Vanjaram,Velvet belly lanternshark,Velvet catfish,Velvetfish,Vendace,Vermilion snapper,Vimba,Viperfish,Wahoo,Walking catfish,Wallago,Walleye,Walleye pollock,Walu,Warmouth,Warty angler,Waryfish,Waspfish,Weasel shark,Weatherfish,Weever,Weeverfish,Wels catfish,Whale catfish,Whalefish,Whale shark,Whiff,Whitebait,White croaker,Whitefish,White marlin,White shark,Whitetip reef shark,Whiting,Wobbegong,Wolf-eel,Wolffish,Wolf-herring,Worm eel,Wormfish,Wrasse,Wrymouth,X-ray tetra,Yellow-and-black triplefin,Yellowback fusilier,Yellowbanded perch,Yellow bass,Yellowedge grouper,Yellow-edged moray,Yellow-eye mullet,Yellowhead jawfish,Yellowfin croaker,Yellowfin cutthroat trout,Yellowfin grouper,Yellowfin tuna,Yellowfin pike,Yellowfin surgeonfish,Yellowfin tuna,Yellow jack,Yellowmargin triggerfish,Yellow moray,Yellow perch,Yellowtail,Yellowtail amberjack,Yellowtail barracuda,Yellowtail clownfish,Yellowtail horse mackerel,Yellowtail kingfish,Yellowtail snapper,Yellow tang,Yellow weaver,Yellowtail catfish,Zander,Zebra bullhead shark,Zebra danio,Zebrafish,Zebra lionfish,Zebra loach,Zebra oto,Zebra pleco,Zebra shark,Zebra tilapia,Zebra turkeyfish,Ziege,Zingel]


async def rarity(userLoc):
    available = locations[userLoc]["population"]
    res = -1
    while (res == -1):
        rarity = random.random()
        if (rarity < .75):
            res =  cfArS[random.randint(0,len(available["cAr"])-1)]
        elif (rarity < .95):
            res = ufArS[random.randint(0,len(available["uAr"])-1)]
        elif (available.get("rAr") != NULL):
            res = available["rAr"][random.randint(0,len(available["rAr"])-1)]
    return res
        

async def value(rarity, quality, foreign, prep):
    if rarity in cfArS:
        rarity = 1
    elif rarity in ufArS:
        rarity = 2
    elif rarity in rfArS:
        rarity = 3
    else:
        rarity = 4
    if (foreign):
        return round(3 + rarity*5 + quality*5 + prep) 
    else:
        return round(rarity*5 + quality*5 + prep)
    
async def qualify(quality):
    if (quality == 1):
        return "perfect"
    elif (quality > .75):
        return "good"
    elif (quality > .25):
        return "decent"
    else:
        return "bad"

async def satisfaction(r, q, p):
    if r in cfArS:
        r = 1
    elif r in ufArS:
        r = 2
    elif r in rfArS:
        r = 3
    else:
        r = 4
    return r+3*q+random.randint(0,2)+p*2

async def createProfile(userID):
    users[f'{userID}']['prof'] = {
        'bio': '',
        'fishTime': 0
    }
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)

@bot.event
async def on_command(ctx):
    if not str(ctx.author.id) in users:
        await createUser(ctx.author.id)
        await ctx.send(f'{ctx.author.display_name}, you now have a bot profile.')
    if not 'seasoning' in users[f'{ctx.author.id}']['equipment']:
        users[f'{ctx.author.id}']['equipment']['seasoning'] = 0
    if not 'location' in users[f'{ctx.author.id}']:
        users[f'{ctx.author.id}']['location'] = '0'

# @bot.command()
# async def kill(ctx):
#     await bot.logout()

#@bot.command()
# async def fdUdt(ctx):
#     for u in users:    
#         users[u]['fishlog'] = {
#         "bass": 0, "pike": 0, "grunt": 0, "angelfish": 0, "guppy": 0,
#         "cod": 0, "marlin": 0, "tang": 0, "mudfish": 0, "trout": 0,
#         "snapper": 0, "tetra": 0, "firefish": 0, "parrotfish": 0, "catfish": 0,
#         "bonefish": 0
#         }

@bot.command()
async def profile(ctx):
    if users[f'{ctx.author.id}'].get('prof') == None:
        await createProfile(ctx.author.id)
    pf_embed = discord.Embed(
        title = str(f'{ctx.author.display_name}\'s Profile'),
        type = "rich"
    )
    pf_embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    pf_embed.add_field(name="Reputation:", value=f"You have a reputation score of {round(users[f'{ctx.author.id}']['reputation'])} adding to your prep skill!", inline=False)
    ub = users[f'{ctx.author.id}']['prof']['bio']
    bioF = ub if(ub != '') else 'No bio set yet!'
    pf_embed.add_field(name="User Bio:", value=bioF, inline=False)
    fTi = round(users[f'{ctx.author.id}']['prof']['fishTime']/60,2)
    pf_embed.add_field(name="Time Spent Fishing:", value=f'{fTi} minutes', inline=False)
    await ctx.channel.send(embed=pf_embed)    

@bot.command(aliases=['bio', 'biography'])
async def setBio(ctx):
    if users[f'{ctx.author.id}'].get('prof') == None:
        await createProfile(ctx.author.id)
    ms = ctx.message.content.split()
    preL = 0
    if (ms[0] == 'fb'):
        preL = 3 + len(ms[1])
    else: 
        preL = len(ms[0])
    if (len(ctx.message.content) > 1000 + preL):
        await ctx.channel.send("Your bio contents must be less than 1000 characters!")
    elif(len(ctx.message.content) == preL):
       await ctx.channel.send("Please include your new bio!") 
    else:
        users[f'{ctx.author.id}']['prof']['bio'] = ctx.message.content[preL:]
        await ctx.channel.send("Your bio has been set.")
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)

@bot.command(aliases=['fishidex', 'fishlog', 'fish log'])
async def fishdex(ctx):
    fdx = users[f'{ctx.author.id}']['fishlog']
    fd_embed = discord.Embed(
        title = str(f'{ctx.author.display_name}\'s Fish Log'),
        type="rich",
        description=f"Here are your all time fish counts!"
    )
    fd_embed.add_field(name=f"Common Fish:", value=f"Bass: {(fdx[fishNames[cfArS[0]-1]])}\nPike: {(fdx[fishNames[cfArS[1]-1]])}\nGrunt: {(fdx[fishNames[cfArS[2]-1]])}\nAngelfish: {(fdx[fishNames[cfArS[3]-1]])}\nGuppy: {(fdx[fishNames[cfArS[4]-1]])}")
    fd_embed.add_field(name=f"Common't Fish:", value=f"Cod: {(fdx[fishNames[ufArS[0]-1]])}\nMarlin: {(fdx[fishNames[ufArS[1]-1]])}\nTang: {(fdx[fishNames[ufArS[2]-1]])}\nMudfish: {(fdx[fishNames[ufArS[3]-1]])}\nTrout: {(fdx[fishNames[ufArS[4]-1]])}")
    fd_embed.add_field(name=f"Rare Fish:", value=f"Snapper: {(fdx[fishNames[rfArS[0]-1]])}\nTetra: {(fdx[fishNames[rfArS[1]-1]])}\nFirefish: {(fdx[fishNames[rfArS[2]-1]])}\nParrotfish: {(fdx[fishNames[rfArS[3]-1]])}\nCatfish: {(fdx[fishNames[rfArS[4]-1]])}")
    await ctx.channel.send(embed=fd_embed)

@bot.command()
async def location(ctx):
    userInfo = users[f'{ctx.author.id}']
    await ctx.channel.send(f"You are currently fishing in {locations[userInfo['location']]['knAs']}")

@bot.command()
async def fish(ctx):
    userInfo = users.get('{}'.format(ctx.author.id))
    if (userInfo["isFishing"] == 0 and (userInfo["lastFish"] - time.time() < 0)):
        users[f'{ctx.author.id}']["lastFish"] = time.time() + userInfo["equipment"]["boat"]["cooldown"] + userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.author.id}']["isFishing"] = 1
        users[f'{ctx.author.id}']["lastDur"] = userInfo["equipment"]["boat"]["dur"]
        users[f'{ctx.author.id}']["lastCd"] = userInfo["equipment"]["boat"]["cooldown"]
        await ctx.send(f'{ctx.author.display_name}, your fishing trip has started! Come back in {userInfo["equipment"]["boat"]["dur"]} seconds to see the results!')
    elif (userInfo["isFishing"] == 1 and (userInfo["lastCd"] >= userInfo["lastFish"] - time.time())):
        if users[f'{ctx.author.id}'].get('prof') == None:
            await createProfile(ctx.author.id)
        users[f'{ctx.author.id}']['prof']['fishTime'] = users[f'{ctx.author.id}']['prof']['fishTime'] + users[f'{ctx.author.id}']["lastDur"]
        totVal = 0
        numCaught = round(math.pow(userInfo["equipment"]["fishEq"]["quality"],1.151)*random.uniform(.75,1.25)*userInfo["lastDur"])
        if numCaught == 0:
            numCaught = random.randint(0,1)
        r = 0
        q = 0
        fdex = users[f'{ctx.author.id}']['fishlog']
        for i in range(numCaught):
            if userInfo.get("location") == "-1":
                r = 17
                numCaught = 1
                totVal = 0
                w = 0.01
            else: 
                fish = await pullFish(userInfo.get("pos"), userInfo.get("location"))
                users[f'{ctx.author.id}']["inv"][f'{len(userInfo.get("inv"))}'] = fish
                q = fish.get("quality")
                r = fish.get("rarity")
                w = fish.get("weight")
                fdex[fishNames[r-1]] = fdex[fishNames[r-1]] + 1
                totVal += await value(r,q,False,0)
        users[f'{ctx.author.id}']['fishlog'] = fdex
        users[f'{ctx.author.id}']["isFishing"] = 0
        outMsg = f'{ctx.author.display_name}, your fishing trip yielded {numCaught} fish! Their total value is {totVal} perles! :fishing_pole_and_fish:'
        if numCaught == 0:
            outMsg = f'{ctx.author.display_name}, your line snapped before you could catch any fish! Unlucky!'
        elif numCaught == 1:
            outMsg = f'{ctx.author.display_name}, you caught a {rarityAr[r-1]}. It weighs {w} lbs and worth {totVal} perles! :fishing_pole_and_fish:'
        await ctx.send(outMsg)
    elif (userInfo["lastCd"] < userInfo["lastFish"] - time.time()):
        await ctx.send(f'{ctx.author.display_name}, you\'re still fishing! Come back in {round(userInfo["lastFish"] - time.time() - userInfo["lastCd"])} seconds!')
    else: 
        await ctx.send(f'{ctx.author.display_name}, you need to wait {round(userInfo["lastFish"]-time.time())} more seconds before fishing again for conservation reasons!')
    with open('users.json', 'w') as outfile:
        json.dump(users, outfile)

@bot.command()
async def trade(ctx, slot:int):
    userInfo = users.get('{}'.format(ctx.author.id))
    if (slot>len(userInfo.get('inv'))):
        await ctx.channel.send('Invalid inventory slot')
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
            await ctx.send(f'{ctx.author.display_name}, your new fish is a {rarityAr[r-1]} and is in {await qualify(q)} condition. It is worth {await value(r,q,True,0)} perles! :fish:')
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)
        else:
            await ctx.channel.send('You can\'t send this fish back!')

@bot.command(aliases=['prep'])
async def prepare(ctx, slot:int=1):
    if (slot>len(users.get(f'{ctx.author.id}').get('inv'))):
        await ctx.channel.send('Invalid inventory slot')
    elif (users[f'{ctx.author.id}']['inv'][f'{slot-1}']['prepBonus'] == 0):
        slot -= 1
        fish = users.get(f'{ctx.author.id}').get('inv').get(f'{slot}')
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.author.id}']["pos"]
        if r in cfArS:
            pr = 1
        elif r in ufArS:
            pr = 2
        elif r in rfArS:
            pr = 3
        else:
            pr = 4
        oVal = await value(r,q,f,0)
        skill = users.get(f'{ctx.author.id}').get(f'{"reputation"}')/100
        if (3**(pr-1) < skill): skill = 3**(pr-1)
        p = .1
        p += 2 if (users[f'{ctx.author.id}']['equipment'].get('stove') != None) else 0
        sS = ''
        if (users[f'{ctx.author.id}']['equipment']['seasoning'] > 0):
            p += 6
            sLeft = users[f'{ctx.author.id}']['equipment']['seasoning'] - 1
            users[f'{ctx.author.id}']['equipment']['seasoning'] = sLeft
            sS = f'\nYou used some basic seasoning, you have enough left for {sLeft} servings.'
        users[f'{ctx.author.id}']['inv'][f'{slot}']['prepBonus'] += (p+skill)
        nVal = await value(r,q,f,(p+skill))
        await ctx.channel.send(f'{ctx.author.display_name}, you were able to increase the value of this fish by {nVal-oVal} perles! It is now worth {nVal} perles! :cook:{sS}')
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    else:
        await ctx.channel.send('This fish has already been prepared!')

@bot.command()
async def special(ctx, name, num:int):
    if (ctx.author.id == 393586279964475393 or ctx.author.id == 458809225120972800):
        i = 0
        for i in range(num):
            marketSlot = [7541,13501,13938,16595,26773,46262,47663,52353,57710,64896,67709,74790,86063,94945,99082][i]
            market[f'slot{marketSlot}'] = {"from": -2, "rarity": rarityAr.index(name)+1, "quality": 1, "prepBonus": 0}
        await ctx.channel.send(f'Extremely rare {name} have entered the market! There\'s a {num/1000}% chance to catch one!')
        with open('market.json', 'w') as outfile:
            json.dump(market, outfile)
        
@bot.command(aliases=['inventory'])
async def inv(ctx):
    fi = users[f'{ctx.author.id}']['inv']
    fe = users[f'{ctx.author.id}']['equipment']
    i = 0
    uf = []
    wf = []
    for i in range(len(fi)-1):
        uf.append(rarityGroups[fi[f'{i}']['rarity']-1])
        wf.append(fi[f'{i}']['rarity'])
    cf = len([f for f in uf if f == 'common'])
    ctf = len([f for f in uf if f == 'commont'])
    rf = len([f for f in uf if f == 'rare'])
    ef = len([f for f in uf if f == 'event'])
    evf = f'\n **{ef}** event fish' if ef > 0 else ''
    bt = (fe['boat']['name']).lower()
    rd = (fe['fishEq']['name']).lower()
    s = fe['seasoning']
    sS = f'\nYou have enough seasoning for {s} more servings!' if (s > 0) else ''
    in_embed = discord.Embed(
        title = str(f'{ctx.author.display_name}\'s Inventory'),
        type="rich",
        description=f"You have {len(fi)} total fish\nf.storage for a more detailed list of fish"
    )
    in_embed.add_field(name=f"Common Fish: {cf}", value=f"Bass: {len([f for f in wf if f == cfArS[0]])}\nPike: {len([f for f in wf if f == cfArS[1]])}\nGrunt: {len([f for f in wf if f == cfArS[2]])}\nAngelfish: {len([f for f in wf if f == cfArS[3]])}\nGuppy: {len([f for f in wf if f == cfArS[4]])}")
    in_embed.add_field(name=f"Common't Fish: {ctf}", value=f"Cod: {len([f for f in wf if f == ufArS[0]])}\nMarlin: {len([f for f in wf if f == ufArS[1]])}\nTang: {len([f for f in wf if f == ufArS[2]])}\nMudfish: {len([f for f in wf if f == ufArS[3]])}\nTrout: {len([f for f in wf if f == ufArS[4]])}")
    in_embed.add_field(name=f"Rare Fish: {rf}", value=f"Snapper: {len([f for f in wf if f == rfArS[0]])}\nTetra: {len([f for f in wf if f == rfArS[1]])}\nFirefish: {len([f for f in wf if f == rfArS[2]])}\nParrotfish: {len([f for f in wf if f == rfArS[3]])}\nCatfish: {len([f for f in wf if f == rfArS[4]])}")
    in_embed.add_field(name=f"Equipment", value=f"Your fishing boat is a {bt}, and you are fishing with a {rd}!{sS}")
    await ctx.channel.send(embed=in_embed)

@bot.command()
async def storage(ctx, page=1):
    num = len(users[f'{ctx.author.id}']['inv'])
    if (page==1 and num >24):
        n = 1
        inv_embed = discord.Embed(
            title=str(f'{ctx.author.display_name}\'s storage | Page 1'),
            type="rich",
            description=f"You have {num} fish in your storage. Here are the first 24."
        )
    elif (num <= 24):
        n = 1
        inv_embed = discord.Embed(
            title=str(f'{ctx.author.display_name}\'s storage | Page 1'),
            type="rich",
            description=f"You have {num} fish in your storage."
        )
    elif (num >= page*24):
        n = 24*(page-1)+1
        inv_embed = discord.Embed(
            title=str(f'{ctx.author.display_name}\'s storage | Page {page}'),
            type="rich",
            description=f"You have {num} fish in your storage. Here are fish {n}-{n+23}."
        )
    else:
        n = num-23
        inv_embed = discord.Embed(
            title=str(f'{ctx.author.display_name}\'s storage | Last page'),
            type="rich",
            description=f"You have {num} fish in your storage. Here are fish {n}-{n+23}."
        )
    i = n-1
    while (i < len(users[f'{ctx.author.id}']['inv']) and i < n+23):
        fish = users[f'{ctx.author.id}']['inv'][f'{i}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.author.id}']["pos"]
        p = fish["prepBonus"]
        prp = " not" if (p == 0) else ""
        inv_embed.add_field(name=f'Slot {i+1}', value=f'A {rarityAr[r-1]} that is worth {await value(r,q,f,p)} perles and has{prp} been prepared.')
        i += 1
    await ctx.channel.send(embed = inv_embed)

@bot.command()
async def checkFish(ctx, slot:int):
    if (slot > 0 and slot <= len(users[f'{ctx.author.id}']['inv'])):
        fish = users[f'{ctx.author.id}']['inv'][f'{slot-1}']
        q = fish.get("quality")
        r = fish.get("rarity")
        f = fish.get("from") != users[f'{ctx.author.id}']["pos"]
        p = fish["prepBonus"]
        prp = " not" if (p == 0) else ""
        await ctx.channel.send(f'{ctx.author.display_name}, This is a {rarityAr[r-1]} that is worth {await value(r,q,f,p)} perles and has{prp} been prepared.')
    else:
        await ctx.channel.send('Invalid inventory slot')

@bot.command(aliases=['serve'])
async def cook(ctx, slot:int=1):
    if (slot <= len(users[f'{ctx.author.id}']['inv'])):
        fish = users[f'{ctx.author.id}']['inv'][f'{slot-1}']
        q = fish['quality']
        r = fish['rarity']
        f = fish['from'] != users[f'{ctx.author.id}']["pos"]
        p = fish['prepBonus']
        yum = await satisfaction(r,q,p)
        if yum > 12: yum = 12
        if yum < 3:
            users[f'{ctx.author.id}']['reputation'] -= 3-yum
            om = f'{ctx.author.display_name}, your customer hated your fish!'
        elif yum > 6:
            users[f'{ctx.author.id}']['reputation'] += yum-6
            om = f'{ctx.author.display_name}, your customer liked your fish!'
        else:
            om = f'{ctx.author.display_name}, your customer thought that your fish was alright'
        users[f'{ctx.author.id}']['money'] += await value(r,q,f,p)
        moneys = users[f'{ctx.author.id}']['money']
        i = 0
        j = 0
        newInv = {}
        while i < len(users[f'{ctx.author.id}']['inv']):
            if i != slot-1:
                newInv[f'{j}'] = users[f'{ctx.author.id}']['inv'][f'{i}']
                j += 1
            i += 1
        users[f'{ctx.author.id}']['inv'] = newInv
        await ctx.channel.send(f'{om}\nYou have sold your fish for {await value(r,q,f,p)} perles. You now have {moneys} perles!')
        with open('users.json', 'w') as outfile:
            json.dump(users, outfile)
    else:
        await ctx.channel.send('Invalid inventory slot')

@bot.command(aliases=['market'])
async def mrkt(ctx): #pulls up an embedded that displays market slots and fish
    market_embed = discord.Embed (title = "The Net, for fish", type = 'rich', description = "If you'd like to buy something, type 'f.buy market [market slot number]!'")
    page = ""
    for i in range(10):
       marketSlot = random.randint(0,99999)
       marketFish = market.get(f"slot{marketSlot}")
       while (marketFish.get("from") == users.get(f'{ctx.author.id}').get("pos") or marketFish.get("from") == -2):
           marketSlot = random.randint(0,99999)
           marketFish = market.get(f"slot{marketSlot}")
       prep = "prepared" if (marketFish.get("prepBonus") > 0) else "Not prepared"
       page += f'**Slot**: {marketSlot}, Origin: {marketFish.get("from")}, Quality: {await qualify(marketFish.get("quality"))}, Type: {rarityAr[marketFish.get("rarity")-1]}. {prep}. \n'
    market_embed.add_field(name="The one stop shop for bass and cod! (and other things maybe)", value = f'{page}', inline = False)
    market_embed.set_thumbnail(url="https://i.etsystatic.com/15020412/r/il/455abc/2328156575/il_1588xN.2328156575_4m7l.jpg")
    await ctx.send(embed = market_embed)

eqCost = [500, 2000, 10000, 1000, 5000, 50000, 200, 500]
@bot.command(aliases = ['shop', 'equipment store', 'equipment shop', 'eq store', 'eq shop'])
async def store(ctx):
    store_embed = discord.Embed (title = "Jerry's Bait Shop (You know the place)", type = "rich", description = "If you'd like to buy something, type 'f.buy equipment []'")
    fishEq = equipment.get("fishEq")
    rods = fishEq.get("fishRods")
    boats = fishEq.get("boats")
    j = 1
    for i in range(3):
        rod = rods.get(f'{i+1}')
        store_embed.add_field(name = f'{j}: {rod["name"]}', value = f'This rod fishes at {int(rod["quality"]*20)} fish per minute and goes for {rod["price"]} pearles! :oyster:', inline = False)
        j=j+1    
    for i in range(3):
        boat = boats.get(f'{i+1}')
        store_embed.add_field(name = f'{j}: {boat["name"]}', value = f'This boat lets you fish for {boat["dur"]} seconds at a time and goes for {boat["price"]} pearles! :person_rowing_boat:', inline = False)
        j=j+1
    store_embed.add_field(name=f"{j}: Seasonings", value="Increase your prep bonus by 6! 50 servings for 200 pearles.")
    j=j+1
    store_embed.add_field(name=f"{j}: Gas Stove", value="Boosts your food quality by 1 at the price of 500 pearles!")
    await ctx.send(embed = store_embed)

@bot.command()
async def buy(ctx, shoop:str, slot:int):
    if shoop == 'market':
        marketFish = market.get(f'slot{slot}')
        q = marketFish["quality"]
        r = marketFish["rarity"]
        f = marketFish["from"] != users[f'{ctx.author.id}']["pos"]
        p = marketFish["prepBonus"]
        cost = await value(r,q,f,p)
        if (users[f'{ctx.author.id}']["money"] >= cost):
            users[f'{ctx.author.id}']["money"] -= cost
            moneys = users[f'{ctx.author.id}']["money"]
            userInv = users[f'{ctx.author.id}']['inv'] 
            users[f'{ctx.author.id}']["inv"][f'{len(userInv)}'] = marketFish
            market[f'slot{slot}'] = await pullFish(users[f'{ctx.author.id}']['pos'])
            await ctx.send(f"{ctx.author.display_name} you bought the fish for {cost} perles! You now have {moneys} perles. :label:")
            with open('users.json', 'w') as outfile:
                json.dump(users, outfile)
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)
        else:
            await ctx.send(f"{ctx.author.display_name}, you do not have enough perles to make this transaction! :chart_with_downwards_trend:")   
    if shoop == 'equipment':
        if (slot < len(eqCost)+1):
            cost = eqCost[slot-1]
            if (users[f'{ctx.author.id}']["money"] >= cost):
                if (slot > 7):
                    await ctx.send('These items have not yet been implemented fully. We apologize')
                else:
                    await ctx.send('As the bot is still in early development, these items are likely to be reverted as we work on balance')
                    users[f'{ctx.author.id}']["money"] -= cost
                    moneys = users[f'{ctx.author.id}']["money"]
                    userEq = users[f'{ctx.author.id}']['equipment']
                    fishEq = equipment.get("fishEq")
                    rods = fishEq.get("fishRods")
                    boats = fishEq.get("boats")
                    if (slot > 6):
                        if (slot == 7):
                            userEq['seasoning'] = userEq['seasoning'] + 50
                    elif (slot > 3):
                        userEq['boat'] = boats[f'{slot-3}']
                    else: 
                        userEq['fishEq'] = rods[f'{slot}']
                    users[f'{ctx.author.id}']['equipment'] = userEq
                    await ctx.send(f"{ctx.author.display_name} you bought the item for {cost} perles! You now have {moneys} perles. :label:")
                    with open('users.json', 'w') as outfile:
                        json.dump(users, outfile)
            else:
                await ctx.send(f"{ctx.author.display_name}, you do not have enough perles to make this transaction! :chart_with_downwards_trend:")   
        else:
            await ctx.send("Invalid equipment slot.")

@bot.command(aliases=['pearles', 'perles', 'pearls', 'coins', 'moneys', 'moneyz', 'cash', 'dollars', 'fish blood', 'a', 'mooners'])
async def money(ctx):
    moneys = users[f'{ctx.author.id}']["money"]
    await ctx.send(f"You currently have {moneys} pearles!")

#@bot.event
async def on_message(message):
    if (message.content[0:2]=="--"):
        if (users.get('{}'.format(message.author.id))==None):
            createUser(message.author.id)
        userInfo = users.get('{}'.format(message.author.id))
        
        if (message.content[2:] == 'fish'):
            fish = await pullFish(userInfo["pos"])

        if (message.content[2:] == 'createMarket'):
            if (True):
                market = {}
            i = 0
            while i < 100000:
                marketFish = await pullFish(-1)
                market['slot{}'.format(i)] = marketFish
                i += 1
            with open('market.json', 'w') as outfile:
                json.dump(market, outfile)

bot.run(TOKEN)