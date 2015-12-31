from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forvm import ForvmManager
import sys
import time
from datetime import datetime, timedelta
#import config
 

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

walletA = WalletExplorer.WalletExplorer (wallet_file='AA.wallet')
walletB = WalletExplorer.WalletExplorer (wallet_file='BB.wallet')

inA = open('AA.wallet')
publicA = (inA.readline().split(','))[0]
inA.close()

inB = open('BB.wallet')
publicB = (inB.readline().split(','))[0]
inB.close()

bsMan = ForvmManager.ForvmManager (consMan, wallet=walletA, user=publicA)
bsMan2 = ForvmManager.ForvmManager (consMan, wallet=walletB, user=publicB)

## def find_post(listPost, post_id):
##     for elm in listPost:
##         if elm['id'] == post_id:
##             return True
##     return False

## def post_owner(listPost, post_id):
##     for elm in listPost:
##         if elm['id'] == post_id:
##             return elm['user']
##     return None

## def createPost_key(manager):
##     print('-> NEW POST |')
##     ytitle = input ('\tTitle: ')
##     ytext = input('\tText: ')
##     print('-> CREATION COMPLETED')
##     return manager.createPost (ytitle, ytext)

## def getAllPost_key(manager):
##     print('-> POST LIST')
##     c_list = manager.listPosts ()
##     if len(c_list) <= 0:
##         print("\tNo one post founded")
##     else:
##         print ('\tid(s)')
##         for c_elm in c_list:
##             print ('\t' , c_elm['id'])

## def getPostInfo_key(manager):
##     print('-> POST INFO')

##     postlist = []
##     counter = 0

##     print('\tWhich post?')
##     for elm in manager.listPosts():
##         print("\t(" + str(counter) + ") " + elm['id'])
##         counter += 1
##         postlist.append(elm['id'])

##     while True:
##         try:
##             yid = int(input())
##             if (yid >= 0) and (yid < len(postlist)):
##                 break
##             print("-> Invalid input, retry")
##         except ValueError:
##             print("-> Invalid input, retry")
    
##     c_list = manager.listPosts ()
##     for c_elm in c_list:
##         if (c_elm['id'] == postlist[yid]):
##             print (str(c_elm))
##             return
##     print ("Post doesn't found")

## def editPost_key(manager):
##     print('-> EDIT POST')
##     yid = input('\tInsert post id: ')

##     c_list = manager.listPosts()  
##     if find_post(c_list, yid):
##         print('\tPost Founded')
##         ytext = input('\tInsert new text:')
##     else:
##         print("\tPost doesn't exist")
##         return      
    
    
## def commentPost_key(manager):
##     yid = input('Insert post id: ')
##     ycomment = input('insert a comment: ')

##     c_list = manager.listPosts()
##     for c_elm in c_list:
##         if c_elm['id'] == yid:
##             return manager.commentPost(yid, ycomment)
##     else:
##         print("You cannot comment, post doesn't exist")

## def parse_deadline(deadline_str):
##     try:
##         return time.strptime(deadline_str, '%d/%m/%Y-%H:%M')
##     except ValueError:
##         date = datetime.today()
##         date += timedelta(days=1)
##         print("Input Format Error, we use the default value, " + str(date))
##         return date.strftime('%d/%m/%Y-%H:%M')
            
## def createPoll_key(manager):
##     ytitle = input('Insert a title: ')
##     choices = []
##     while True:
##         print('There are ' + str(len(choices)) + ' choices already uploaded')
##         choice = input('Write another choice or just press enter: ')     
##         if len(choice) > 0:
##             choices.append(choice)
##         else:
##             break

##     ydeadline = input('Insert a deadline [gg/mm/yyyy-HH:MM]')
##     parsed_deadline = parse_deadline(ydeadline)
##     print('paresed_deadline %s', parsed_deadline)
##     return manager.createPoll(ytitle, choices, parsed_deadline)

## def listPolls_key(manager):    
##     c_list = manager.listPolls ()
##     if len(c_list) <= 0:
##         print("There aren't any polls")
##     else:
##         print ('id(s)')
##         for c_elm in c_list:
##             print ('\t' , c_elm['id'])

## def getChoices(poll):
##     #{A: 0, B: 0 ....}
##     choices = poll['choices']
##     return choices.keys()
            
## def vote_key(manager):

##     listPolls_key(manager)
    
##     yid = input('Insert poll id: ')
   
    
##     c_list = manager.listPolls()
##     for c_elm in c_list:
##         if c_elm['id'] == yid:
            
##             #controlliamo se l'utente ha già espresso il suo voto
##             for v_user in c_elm['choices']:
##                 if manager.User in c_elm['choices'][v_user]:
##                     print('This user has already choose')
##                     return
            
##             #check sulla deadline
##             deadline = c_elm['deadline']
##             print ('deadline: ' + str(deadline))
##             if datetime.strptime(deadline, '%d/%m/%Y-%H:%M') < datetime.now():
##                 print('poll closed')
##                 return None
            
##             #stampiamo le scelte
##             choices = c_elm['choices'].keys()
##             print('choices:')
##             for choice in choices:
##                 print(choice)

##             #acquisiamo la risposta
##             while True:
##                 yanswer = input('answer: ')
##                 if yanswer in choices:
##                     return manager.vote(yid, yanswer)
##                 else:
##                     print('No valid answer, try again')
##                     return None            
##     else:
##         print("You cannot vote, poll doesn't exist")
##         return None 

## def getPollInfo_key(manager):
##     print ("-> POLL INFO")

##     polllist = []
##     counter = 0

##     print('\tWhich poll?')
##     for elm in manager.listPolls():
##         print("\t(" + str(counter) + ") " + elm['id'])
##         counter += 1
##         polllist.append(elm['id'])

##     while True:
##         try:
##             yid = int(input())
##             if (yid >= 0) and (yid < len(polllist)):
##                 break
##             print("-> Invalid input, retry")
##         except ValueError:
##             print("-> Invalid input, retry")
    
##     c_list = manager.listPolls ()
##     for c_elm in c_list:
##         if c_elm['id'] == polllist[yid]:
##             print(c_elm)
##             return
##     print ("Poll doesn't found")


def waitPost(post_id):
    
    while True:
        postList = bsMan.listPosts()
        for post in postList:
            if post['id'] == post_id:
                print('post ' + post_id + ' founded')
                return
        print('waiting post ' + post_id)
        time.sleep(60)

def waitComment(post_id, comment_id):
    while True:
        postList = bsMan.listPosts()
        for post in postList:
            if post['id'] == post_id:
                for comment in post['comments']:
                    if comment['id'] == comment_id:
                        print ('comment ' + comment_id + ' founded in post ' + post_id)
                        return
        print('waiting comment ' + comment_id)
        time.sleep(60)

def waitPoll(poll_id):
    while True:
        pollList = bsMan.listPolls()
        for poll in pollList:
            if poll['id'] == poll_id:
                print ('poll ' + poll_id + ' founded')
                return
        print('waiting poll ' + poll_id)
        time.sleep(60)

def waitVote(poll_id, vote_id):

    while True:
        pollList = bsMan.listPolls()
        for poll in pollList:
            if poll['id'] == poll_id:
                #scorriamo le scelte
                choices = poll['choices'].keys()
                for choice in choices:
                    for elm in poll['id'][choice]:
                        if elm['id'] == vote_id:
                            print('vote ' + vote_id + ' founded in poll ' + poll_id)
                            return
        print('waiting vote ' + vote_id)
        time.sleep(60)
                    
if __name__ == "__main__":
    if len (sys.argv) > 1:
        ## if sys.argv[1] == 'createPost':
        ##     c_id = createPost_key(bsMan)
        ##     print(c_id)
        ##     sys.exit (0)
        ## elif sys.argv[1] == 'listPosts':
        ##     getAllPost_key (bsMan)
        ##     sys.exit (0)
        ## elif sys.argv[1] == 'getPostInfo':
        ##     getPostInfo_key(bsMan)
        ##     sys.exit(0)
        ## elif sys.argv[1] == 'commentPost':
        ##     commentPost_key(bsMan)
        ##     sys.exit(0)
        ## elif sys.argv[1] == 'createPoll':
        ##     createPoll_key(bsMan)
        ##     sys.exit(0)
        ## elif sys.argv[1] == 'listPolls':
        ##     listPolls_key(bsMan)
        ##     sys.exit(0)
        ## elif sys.argv[1] == 'getPollInfo':
        ##     getPollInfo_key(bsMan)
        ##     sys.exit(0)
        ## elif sys.argv[1] == 'vote':
        ##     vote_key(bsMan)
        ##     sys.exit(0)
        if sys.argv[1] == 'test':
            #postid = bsMan.createPost('Hello post', 'Post di test')
            postid = '2d0b2d981a8337a743de70b7d425704bb88d2169406d667c448f0ca145241e92'
            waitPost(postid)
            print(bsMan.listPosts())

            commid = bsMan.commentPost(postid, 'This is a comment')

            waitComment(postid, commid)
            print(bsMan.getPostInfo(commid))
            
            postid2 = bsMan2.createPost('Hello post 2', 'Post di test2')
            commid2 = bsMan2.commentPost(postid, 'This is a comment of B')

            waitComment(postid, commid2)
            print(bsMan.getPostInfo(postid))
            print ("Test passed")
            
        elif sys.argv[1] == 'test2':
            deadline = time.strptime('12/12/2016-10:15', '%d/%m/%Y-%H:%M')
            pollid = bsMan.createPoll('Title', ['answer1', 'answer2'], deadline)

            waitPoll(pollid)
            bsMan.listPolls()
            
            voteid1 = bsMan.vote(pollid, 'answer1')
            voteid2 = bsMan.vote(pollid, 'answer2')

            waitVote(voteid1)
            bsMan.getPollInfo(pollid)
                
            voteid3 = bsMan2.vote(pollid, 'answer2')
            waitVote(voteid3)            
            bsMan.getPollInfo(pollid)

            
            pollid2 = bsMan2.createPoll('Title', ['answer1', 'answer2'], deadline)
            waitPoll(pollid2)
            bsMan.listPolls()
            
        print ('usage:', sys.argv[0], 'createPost | listPosts | getPostInfo | commentPost | createPoll | listPolls | getPollInfo | editPost | test | test2')
