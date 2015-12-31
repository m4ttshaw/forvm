# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import time
from libcontractvm import Wallet, ConsensusManager, DappManager

class ForvmManager (DappManager.DappManager):
    def __init__ (self, consensusManager, wallet = None, user = None):
        super (ForvmManager, self).__init__(consensusManager, wallet)
        self.User = user

    def createPost (self, title, text):
        cid = self.produceTransaction('forvm.writenewpost', [self.User, title, text])
        return cid

    def listPosts(self):
        return self.consensusManager.jsonConsensusCall('forvm.listposts', [])['result']

    def getPostInfo(self, post_id):
        return self.consensusManager.jsonConsensusCall('forvm.getpostinfo', [post_id])['result']
        
    def commentPost(self, post_id, comment):
        cid = self.produceTransaction('forvm.commentpost', [self.User, post_id, comment])
        return cid
    
    def createPoll(self, title, choices, deadline):
        cid = self.produceTransaction('forvm.createpoll', [self.User, title, choices, deadline])
        return cid

    def listPolls(self):
        return self.consensusManager.jsonConsensusCall('forvm.listpolls',[])['result']

    def getPollInfo(self, poll_id):
        return self.consensusManager.jsonConsensusCall('forvm.getpollinfo',[poll_id])['result']
    
    def vote(self, pollID, answer):
        cid = self.produceTransaction('forvm.vote', [self.User, pollID, answer])
        return cid
