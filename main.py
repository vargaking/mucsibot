import discord
import os
import random
import xmltodict
from datetime import datetime
from dotenv import load_dotenv

bot = discord.Client()
welcomes = ['jó reggelt', 'hali', 'szia', 'hello', 'helló', 'sziasztok', 'jo estet', 'jó estét', 'jo napot', 'jó napot', 'hi', 'csá']

load_dotenv()

def kretenKaromkodasok():
    with open('DirtyWords.xml', 'r') as f:
        words = xmltodict.parse(f.read())
    return words['DirtyWords']['Word']
            
kretenKaromkodasokList = kretenKaromkodasok()

def get_random_kreten_karomkodas():
    print("megy a mokazas")

    return random.choice(kretenKaromkodasokList)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='Belga - Egy két há'))
    print('{0.user} is online'.format(bot))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if random.randint(0,100) == 5:
      await message.channel.send('Na ettől fogok talajfertőtlenítőt herbálozni')

    #nem spamelunk
    """if random.randint(0,500) == 50:
      await message.channel.send('Baszass egy #info parancsot és nézd meg mikkel tudlak kényeztetni te kis buzi')"""


    # kivalaszt egy random karomkodast az adatbazisbol
    def randomKaromkodas():
        print("csuhajja valaki karomkodik")
        karomkodasok = open('karomkodasok.txt', 'r')
        karomkodasokStr = karomkodasok.read()
        karomkodasokList = list(map(str, karomkodasokStr.split(';')))
        randomNumber = random.randint(0,len(karomkodasokList) - 1)
        karomkodasok.close()
        return str(karomkodasokList[randomNumber])

    # admin related cucc tbh nemtom mit csinal
    def login():
      logins = open('admin-logins.txt', 'r')
      loggedin = logins.read()
      logins.close()
      if str(message.author) == loggedin:
        return "loggedIn"

    # legacy logging cucc, debug only
    """print(message.channel.id)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    loggingChannel = bot.get_channel(959766785618485259)
    await loggingChannel.send("[{}] [{}]: {}".format(current_time, message.author, message.content))
    logfile = open('logging.txt', 'a')
  
    print("[{}] [{}]: {}".format(current_time, message.author, message.content))
    logfile.writelines("\n[{}] [{}]: {}".format(current_time, message.author, message.content))
    logfile.close()"""

    if message.content.startswith('#káromkoggy'):
        await message.channel.send(randomKaromkodas())

    if message.content.startswith('#kreten'):
        await message.channel.send(get_random_kreten_karomkodas())

    if message.content.lower().startswith('szevasz'):
        await message.channel.send('te fasz')

    if message.content.lower() in welcomes:
        # random number from 0 to 30
        randomNumber = random.randint(0,30)
        if randomNumber == 0:
            await message.channel.send('Szia. A kurvaanyád. Szia')
    
    if message.content.startswith('#info'):
        await message.channel.send(
"""
na jól van te román, mire vagy kíváncsi? haggyad úgy is idióta vagy hozzá, inkább leírok mindent:\n
    #info - parancsok, infók a botról\n
    #káromkoggy - random káromkodás\n
    #add - adj hozzá új káromkodást az adatbázishoz\n
    #anyadat @valaki - küldj el valakit a p-be\n
    #hiddenflex @valaki - a kurvaannyát annak aki flexel\n
    #kiterdekel - mindenki leszar téged, te kis nyomoronc szarcsimbók\n
    #kreten - random kretén káromkodás a Kréta fejlesztőktől (ezúton is köszike Sawarim$-nak)\n
Credit: @vargaking#4225 (discord) @vargaking (github)\n
Ha teccik a bot, oszd meg másokkal is: https://discord.com/api/oauth2/authorize?client_id=820976288395034665&permissions=8&scope=bot\n\n
A teljes forráskód elérhető a https://github.com/vargaking/mucsibot linken
""")

    # egyszer mukodott, perpill nem teszteltem meg
    if message.content.startswith('#add'):
        print(message.author)
        karomkodasokFile = open('waiting_to_approve.txt', 'a+')
        uzenet = message.content
        ujKaromkodas = uzenet[5:len(uzenet)]
        await message.channel.send(ujKaromkodas + " fhuuu. Ezen kiégek xddddd, ez geci jo")
        karomkodasokFile.writelines(';' + ujKaromkodas)
        karomkodasokFile.close()

    if message.content.startswith('#anyadat'): 
        tag = list(map(str, message.content.split()))
        await message.channel.send("Baszódjál meg " + tag[1] + ". " + randomKaromkodas())
        print(str(message.author) + " elküldte " + str(tag[1]) + "-t az anyjába ")
        await message.delete()

    # admin message
    if message.content == "#mucsi-message":
      if login() == "loggedIn":
        uzenet = open('message.txt', 'r')
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")   

      await message.channel.send(uzenet.read())
      await message.delete()

    if message.content == "#mucsi-info":
      karomkodasok = open('karomkodasok.txt', 'r')
      karomkodasokStr = karomkodasok.read()
      karomkodasokList = list(map(str, karomkodasokStr.split(';')))
      await message.channel.send('Ez a bot jelenleg ' + str(len(bot.guilds)) + ' szerveren küld el embereket a picsába és több mint ' + str(len(karomkodasokList)) + ' különböző káromkodást tud, hogy baszódnál meg')
      print(bot.guilds)

    if message.content.lower() == 'imádom a mucsibotot':
      await message.channel.send('Tudom. A kurva anyádat')

    # admin related cuccok
    if message.content.startswith("#login"):
      await message.channel.send("Bejelentkezés a megadott jelszóval...")
      uzenet = list(map(str, message.content.split()))
      if uzenet[1] == os.getenv('admin-password'):
        await message.channel.send('Sikeres bejelentkezés!')
        print(str(message.author) + " bejelentkezett")
        logins = open('admin-logins.txt', 'a')
        logins.writelines(str(message.author))
        logins.close()
      else:
        await message.channel.send('Sikertelen bejelentkezés')
      await message.delete()

    if message.content == "#logout":
      if login() == "loggedIn":
        logins = open('admin-logins.txt', 'w')
        logins.write('')
        await message.channel.send('Sikeresen kijelentkeztél!')
        logins.close()
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")   

    if message.content == "#show-next":
      logins = open('admin-logins.txt', 'r')
      loggedin = logins.read()
      logins.close()
      if "loggedIn" == login():
        approvals = open('waiting_to_approve.txt', 'r+')
        approvalsStr = approvals.read()
        approvalsList = list(map(str, approvalsStr.split(';')))
        await message.channel.send(approvalsList[0])
        approvals.close()
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")

    if message.content == "#approve":
      if login() == "loggedIn":
        approvals = open('waiting_to_approve.txt', 'r+')
        approvalsStr = approvals.read()
        approvalsList = list(map(str, approvalsStr.split(';')))
        await message.channel.send(approvalsList[0] + ' engedélyezve')
        karomkodasokFile = open('karomkodasok.txt','a')
        karomkodasokFile.writelines(';' + approvalsList[0])
        karomkodasokFile.close()
        approvals.close()
        approvals = open('waiting_to_approve.txt', 'w')
        approvals.write("")
        approvals.close()
        approvals = open('waiting_to_approve.txt', 'a')
        approvals.write(approvalsList[1])
        szam = 0
        for karomkodas in approvalsList:
          if szam != 0 and szam != 1:
            approvals.writelines(";" + karomkodas)
          szam+=1
        approvals.close()
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")   

    if message.content == "#deny":
      if login() == "loggedIn":
        approvals = open('waiting_to_approve.txt', 'r')
        approvalsStr = approvals.read()
        approvalsList = list(map(str, approvalsStr.split(';')))
        await message.channel.send(approvalsList[0] + ' elutasítva')
        approvals.close()
        approvals = open('waiting_to_approve.txt', 'w')
        approvals.write("")
        approvals.close()
        approvals = open('waiting_to_approve.txt', 'a')
        approvals.write(approvalsList[1])
        szam = 0
        for karomkodas in approvalsList:
          if szam != 0 and szam != 1:
            approvals.writelines(";" + karomkodas)
          szam+=1
        approvals.close()
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")   

    if message.content.startswith("#hiddenflex"):
        tag = list(map(str, message.content.split()))
        await message.channel.send("Hogy basszon szájba egy targonca " + tag[1] + ". Anyádnak flexeljél kisköcsög. " + randomKaromkodas())
        await message.delete()

    if message.content.startswith("#kiterdekel"):
        await message.channel.send(file=discord.File('pics/kiterdekel.png'))
        await message.delete()

    if len(message.content) > 800:
        await message.channel.send(file=discord.File('pics/kiterdekel.png'))

    # discord presence allito
    if message.content.startswith("#change-music"):
      if "loggedIn" == login():
        tag = list(map(str, message.content.split(':')))
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=tag[1]))
        await message.channel.send('Ez a zene nagyon durván odabasz')  
      else:
        await message.channel.send("Hoppá. Úgy tűnik nem vagy bejelentkezve te gány fos")   
    
    if message.content.startswith(">p"):
      if random.randint(1,10) == 1:
        await message.channel.send('Nem azért, de ez a szám kibaszottul szar')



      


bot.run(os.getenv('TOKEN'))
