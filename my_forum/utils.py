'''
Created on 15 nov. 2012

@author: naamane.othmane
'''

class ThreadsReport():
    def __init__(self, title ="", slug="",last_post_user= None, replies=0):
        self.title = title
        self.slug = slug
        self.last_post_user = last_post_user
        self.replies = replies