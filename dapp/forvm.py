# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from contractvmd import config, dapp
from contractvmd.chain.message import Message
from contractvmd.proto import Protocol


logger = logging.getLogger(config.APP_NAME)

class ForvmProto:
    DAPP_CODE = [0x01, 0x04]

    METHOD_CREATEPOST = 0x02
    METHOD_COMMENT = 0x03
    METHOD_CREATEPOLL = 0x05
    METHOD_VOTE = 0x06
    
    METHOD_LIST = [METHOD_CREATEPOST, METHOD_COMMENT, METHOD_CREATEPOLL, METHOD_VOTE]

 #class EmptyMessage (Message):
 #	def toJSON (self):
 #		data = super (EmptyMessage, self).toJSON ()
 #		return data

class CreateNewPostMessage(Message):
    def post (user, title, text):
        m = CreateNewPostMessage ()
        m.User = user
        m.Title = title
        m.Text = text
        m.DappCode = ForvmProto.DAPP_CODE
        m.Method = ForvmProto.METHOD_CREATEPOST
        return m

    def toJSON (self):
        data = super (CreateNewPostMessage, self).toJSON ()

        if self.Method == ForvmProto.METHOD_CREATEPOST:
            data['user'] = self.User
            data['title'] = self.Title
            data['text'] = self.Text
        else:
            return None

        return data

class CommentPostMessage(Message):
    def commentPost(user, post_id, text):
        m = CommentPostMessage ()
        m.User = user
        m.Post_id = post_id
        m.Text = text
        m.DappCode = ForvmProto.DAPP_CODE
        m.Method = ForvmProto.METHOD_COMMENT
        return m

    def toJSON(self):
        data = super(CommentPostMessage, self).toJSON ()
        if self.Method == ForvmProto.METHOD_COMMENT:
            data['user'] = self.User
            data['post_id'] = self.Post_id
            data['text'] = self.Text
        return data

    
class CreatePollMessage(Message):
    def createPoll(user, title, choices, deadline):
        m = CreatePollMessage ()
        m.User = user
        m.Title = title
        m.Choices = choices
        m.Deadline = deadline
        m.DappCode = ForvmProto.DAPP_CODE
        m.Method = ForvmProto.METHOD_CREATEPOLL
        return m

    def toJSON(self):
        data = super(CreatePollMessage, self).toJSON ()
        if self.Method == ForvmProto.METHOD_CREATEPOLL:
            data['user'] = self.User
            data['title'] = self.Title
            data['choices'] = self.Choices
            data['deadline'] = self.Deadline
        return data

class VoteMessage(Message):
    def vote(user, pollID, answer):
        m = VoteMessage ()
        m.User = user
        m.PollID = pollID
        m.Answer = answer
        m.DappCode = ForvmProto.DAPP_CODE
        m.Method = ForvmProto.METHOD_VOTE
        return m

    def toJSON(self):
        data = super(VoteMessage, self).toJSON ()
        if self.Method == ForvmProto.METHOD_VOTE:
            data['user'] = self.User
            data['pollid'] = self.PollID
            data['answer'] = self.Answer
        return data
    
class ForvmAPI (dapp.API):
    def __init__ (self, vm, dht, api):
        self.api = api
        self.vm = vm
        self.dht = dht

        rpcmethods = {}
        rpcmethods['writenewpost'] = {"call": self.method_writenewpost, "help":{"args":["user", "title", "text"], "return": {}}}
        rpcmethods['listposts'] = {"call": self.method_listposts, "help": {"args": [], "return":{}}}
        rpcmethods['getpostinfo'] = {"call": self.method_getpostinfo, "help": {"args": ["post_id"], "return":{}}}
        rpcmethods['commentpost'] = {"call": self.method_commentpost, "help":{"args":["user", "pid", "com"], "return": {}}}

        rpcmethods['createpoll'] = {"call": self.method_createpoll, "help":{"args":["user", "title", "choices", "deadline"], "return": {}}}
        rpcmethods['listpolls'] = {"call": self.method_listpolls, "help":{"args":[], "return": {}}}
        rpcmethods['getpollinfo'] = {"call": self.method_getpollinfo, "help": {"args": ["poll_id"], "return":{}}}
        
        rpcmethods['vote'] = {"call": self.method_vote, "help":{"args":["user", "pollid", "answer"], "return": {}}}

        
        errors = {}

        
        super (ForvmAPI, self).__init__(vm, dht, rpcmethods, errors)

    def method_writenewpost (self, user, title, text):
        msg = CreateNewPostMessage.post (user, title, text)
        return self.createTransactionResponse(msg)

    def method_listposts (self):
        return self.core.listPosts ()

    def method_getpostinfo(self, post_id):
        return self.core.getPostInfo(post_id)

    def method_commentpost (self, user, post_id, comment):
        msg = CommentPostMessage.commentPost (user, post_id, comment)
        return self.createTransactionResponse(msg)

    def method_createpoll (self, user, title, choices, deadline):
        msg = CreatePollMessage.createPoll (user, title, choices, deadline)
        return self.createTransactionResponse(msg)

    def method_listpolls (self):
        return self.core.listPolls ()

    def method_getpollinfo(self, poll_id):
        return self.core.getPollInfo(poll_id)
    
    def method_vote (self, user, pollID, answer):
        msg = VoteMessage.vote (user, pollID, answer)
        return self.createTransactionResponse(msg)

class ForvmCore (dapp.Core):
    def __init__ (self, chain, database):
        database.init('posts_db', [])
        database.init('polls_db', [])

        ## posts_db = [{'id': id0, user: 'user0', 'title': title0, comments:[{'id': idCom0, user: 'user0' text: 'text0'}, {'id': idCom1, ...}, {'id': idComn, ...}],{}, ..., {'id': 'idm', ....}]
        ## polls_db = [{'id': id0, user: 'user0', 'title': title0, choices: {cho1:[A, A, ..., A], cho2:[A, A, ... A], ... chon: [...] },{}, ... , {}]
        ## A = {'id': voteid0, 'user': userID} 

        super (ForvmCore, self).__init__ (chain, database)

    ### UTILITIES ###
    def postExist(self, post_ID, postList):
        for post in postList:
            if post['id'] == post_ID:
                return True
        return False

    def commentExist(self, post_ID, postList, comment_ID):
        for post in postList:
            if post['id'] == post_ID:
                for comment in post['comments']:
                    if comment['id'] == comment_ID:
                        return True
        return False

    def alreadyVote(self, poll_id, poll_list, user):
        for poll in poll_list:
            if poll['id'] == poll_id:
                dict_choices = poll['choices'].keys()
                for choice in dict_choices:
                    for vote in poll['choices'][choice]:
                       if vote['user'] == user :
                            return True
        return False
    
    #################################################

    
            
    def writeNewPost(self, user, postID, title, text):        
        postList = self.database.get('posts_db')
                                
        query = {'user': user, 'id': postID, 'title': title, 'text': text, 'comments': []}

        if not self.postExist(postID, postList):        
            self.database.listappend('posts_db', query)

    def listPosts(self):
        data = self.database.get('posts_db')
        l = []
        for elm in data:
            if 'id' in elm:
                l.append(elm)
        return l

    def getPostInfo(self, post_id):
        data = self.database.get('posts_db')

        for post in data:
            if post['id'] == post_id:
                return post
        return None
        
    def commentPost(self, user, post_id, comment_id, text):
        data = self.database.get('posts_db')
        query = {'user': user, 'id' : comment_id, 'text': text}
    
        for post in data:
            if not (self.commentExist(post_id, data, comment_id)):
                post['comments'].append(query)
        self.database.set('posts_db', data)

    def find_pollID(self, poll_ID):
        data = self.database.get('polls_db')
        for poll in data:
            if poll['id'] == poll_ID:
                return True
        return False

    def createPoll(self, user, poll_id, title, choices, deadline):
        choices_dict = {}
        for choice in choices:
            choices_dict[choice] = []        
        
        data = self.database.get('polls_db')    
        query = {'user': user, 'id': poll_id, 'title': title, 'choices': choices_dict, 'deadline': deadline}

        if not self.find_pollID(poll_id):
            self.database.listappend('polls_db', query)
            
    def listPolls(self):
        data = self.database.get('polls_db')
        l = []
        for elm in data:
            if 'id' in elm:
                l.append(elm)
        return l

    def getPollInfo(self, poll_id):
        data = self.database.get('polls_db')

        for poll in data:
            if poll['id'] == poll_id:
                return poll
        return None

    def vote(self, vote_id, user, poll_id, answer):
        data = self.database.get('polls_db')
        query = {'id': vote_id, 'user': user}

        if self.alreadyVote(poll_id, data, user):
            raise ValueError('user ' + user + ' has already vote')
        
        for elm in data:
            if elm['id'] == poll_id:                    
                if answer in elm['choices']:                        
                    elm['choices'][answer].append(query)
                    self.database.set('polls_db', data)
        
class forvm (dapp.Dapp):
    def __init__ (self, chain, db, dht, apimaster):
        self.core = ForvmCore (chain, db)
        api = ForvmAPI (self.core, dht, apimaster)		
        super (forvm, self).__init__(ForvmProto.DAPP_CODE, ForvmProto.METHOD_LIST, chain, db, dht, api)
		
    def handleMessage (self, m):
        if m.Method == ForvmProto.METHOD_CREATEPOST :
            logger.pluginfo("Found new post! >  id: %s title: %s text: %s", m.Hash, m.Data['title'], m.Data['text'])
            self.core.writeNewPost(m.Data['user'], m.Hash, m.Data['title'], m.Data['text'])

        if m.Method == ForvmProto.METHOD_COMMENT :
            logger.pluginfo("Found new comment! >  post_id: %s, comment_id: %s" , m.Data['post_id'], m.Hash)
            try:
                self.core.commentPost(m.Data['user'], m.Data['post_id'], m.Hash, m.Data['text'])
            except Exception as err:
                logger.error(err)
                
        if m.Method == ForvmProto.METHOD_CREATEPOLL :
            logger.pluginfo("Found new poll! >  id: %s title: %s deadline: %s", m.Hash, m.Data['title'], m.Data['deadline'])
            self.core.createPoll(m.Data['user'], m.Hash, m.Data['title'],  m.Data['choices'], m.Data['deadline'])

        if m.Method == ForvmProto.METHOD_VOTE :
            logger.pluginfo("Found new vote! > pollID: %s", m.Data['pollid'])
            try:
                self.core.vote(m.Hash, m.Data['user'], m.Data['pollid'], m.Data['answer'])
            except ValueError as err:
                logger.error(err)
