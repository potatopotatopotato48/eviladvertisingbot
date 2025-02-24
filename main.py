from scratchclient import ScratchSession
import scratchattach as scratch3
import langdetect, random, threading, time, os # threading is intimidating, but it doesn't seem too complicated

'''
made by your mom <3

module purposes:
scratchclient: comments and stuff
scratchattach: getting the explore page
langdetect: seeing whether a project is japanese
random: random numbers
threading: making the bots
time: delays
os: getting process ids, clearing console

note: this code is messy and definitions are next to the code where they were used. Probably not the best organization but it works.
'''

os.system('cls' if os.name=='nt' else 'clear') # clear the console for cleanliness. The command changes between oses, so I added compatibility for that.



def loginToAccount(details):
    try:
        return ScratchSession(i[0], i[1])
    except Exception as exception:
        print(f"Failed to log into account {i[0]} due to error: {exception}")



botAccounts = [
    # [username, password]
               ]
# botnet support if we ever want to do that


sessions = []

for i in botAccounts:

    sessions.append(loginToAccount(i))

scratchAttachSession = scratch3.login(botAccounts[0][0], botAccounts[0][1])



mike = sessions[0].get_user("username") # the username of the person we are advertising goes here
mikeProjects = mike.get_projects(all=True)



def isStupidProjectWeDontLike(project):
    name = project.title
    keywords = ["platformer","PLATFORMER","Platformer","clicker","Clicker","CLICKER","flappy","Flappy","FLAPPY","run","RUN","Run"]
    
    if  not project.comments_allowed: return False
    if project.author.username == "mike27356894": return False
    if langdetect.detect(name) == "ja": return True

    for word in keywords:
        if word in project.description: return True
        if word in project.credits: return True
        if word in name: return True
    # target japanese projects(is that racist? idk ask "mike" cuz it wasn't my idea), projects with platformer in the name, description or instruction, and it must have comments enabled.

    if random.randint(0,5) <= 2: return True
    return False



def getNumProjectsFromPage(amount,page):
    heldOffset = 0
    heldTargetProjects = []

    while len(heldTargetProjects) <= amount:
        toAdd = scratch3.explore_projects(query="*", mode=page, language="en", limit=40, offset=(heldOffset*40))
        # first you just dump the explore page
        print(f"Got explore page, length {len(heldTargetProjects)}\nFiltering...")

        for f in toAdd:
            if not isStupidProjectWeDontLike(f):
                toAdd.remove(f)
        
        heldTargetProjects += toAdd
        # search for the correct projects

        print(f"Loop, length {len(heldTargetProjects)}")

        heldOffset += 1
        time.sleep(.4)
    
    return heldTargetProjects








numTargets = 500

targetProjects = []

targetProjects += getNumProjectsFromPage(round(numTargets*0.25),"trending")
targetProjects += getNumProjectsFromPage(round(numTargets*0.75),"popular")


targetProjectsNames = []

for i in targetProjects:
    targetProjectsNames.append(i.title)
    # get the names of the projects for prettiness purposes

print(f"Finished. Projects to target: {', '.join(targetProjectsNames)}")


print("\n\n\n\n\n\tSearching complete.")
time.sleep(5)



advertisements = ["I really liked this project, and I was wondering if you could check out this project to help the creator out: {0}", 
                  "This project is awesome, you should play it: {0}", 
                  "{0} This project pretty cool like this one",
                  "{0} this project is super cool!",
                  "{0} funni",
                  "{0} the project of all time",
                  "this project got that ohio grimace shake rizz :skull: {0}",
                  "you should play this game, it's really high quality: {0}",
                  "pls play {0} thanks <3",
                  "OH MY GOSH THIS PROJECT IS SO GOOD {0}",
                  "i like this project, but i like this one too: {0}",
                  "{0}",
                  "{0}{0}{0}{0}",
                  "{0} pls",
                  "play 4 a cookie {0}",
                  "i love this project {0}"
                  ]








# ok  so we know what projects we're commenting on, what projects to advertise, how to advertise, and what accounts to use. now we can start the advertising


def randomMikeProject():
    return mikeProjects[random.randint(0,len(mikeProjects)-1)]

def randomAd():
    return random.choice(advertisements).format(f"https://scratch.mit.edu/projects/{randomMikeProject().id}/")


def advertise(account): # threads take a function as an argument
    pid = threading.current_thread().name
    print(f"Account {pid} now running")
    
    while True:
        targetProject = account.get_project(random.choice(targetProjects).id) # choose a random project to comment on, random.choice(targetProjects).id
        ad = randomAd() # get a random ad
        try:
            targetProject.post_comment(ad) # comment the ad
            randomMikeProject().view() # view a random mike project

        except Exception as error:
            print(f"Failed to post comment/view project due to error: {error}")


        delay = random.randint(205,450)
        print(f"Account {pid} Posted comment {ad} on project {targetProject.title} link:\nscratch.mit.edu/projects/{targetProject.id}/\nNow delaying for {delay} seconds.\n")

        time.sleep(delay) # wait so the bot doesn't get ratelimited




botThreads = []

if __name__ == "__main__": # idk why it's like this
    for botAccount in sessions:
        botThreads.append(threading.Thread(target=advertise, args=(botAccount,), name=botAccount.username)) #add a new thread that will run the advertise function with the argument variable botAccount, and a process name the same as the bot's username
        botThreads[len(botThreads)-1].start() # start the thread
