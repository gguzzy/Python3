# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 21:40:38 2020

@author: S238669
"""

# -*- coding: utf-8 -*-
#import requests
import cherrypy
import json
import urllib3
import os, os.path

@cherrypy.expose
class LibraryBook(object):
    exposed = True
    
    def GET(self): #read the sensors data and return the value for the iteration with index  
        #loading sensors of library using Yun and a GET connection to its JSON data stored
        name, temperature, n_people, max_people, condition, empty_seats = self.readSensors() #read values from yun
        html = open("mainpage_f.html").read().format(**locals()) 
        return html #dbJson
        
    def readSensors(self):
        #url = "http://62.10.94.250:"
        #port = "5555"
        http = urllib3.PoolManager()
        #r = {}
        #read json content from a get page of arduino device YUN and load the data in a python dictionary
        #r = json.loads(requests.get(url + port + '/arduino/biblio').text) #python dictionary using requests
        request_biblio = http.request('GET', 'http://62.10.94.250:5555/arduino/biblio') #using urllib3
        request_booking = http.request('GET', 'http://62.10.94.250:5555/arduino/booking')
        b = json.loads(request_biblio.data.decode('utf-8'))
        bk = json.loads(request_booking.data.decode('utf-8'))
        #storing values
        name = b['bn']
        temperature = b["e"][0]['v']
        n_people = b["e1"][0]['p']
        max_people = b["e1"][0]['max_val']
        condition = bk["e2"][0]['v']
        empty_seats = bk["e2"][0]['s']
        return name, temperature, n_people, max_people, condition, empty_seats

if __name__ == '__main__':
	app_config = {
		'/': {
			'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
			'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
        '/css': {
            'tools.staticdir.on': True, 
            'tools.staticdir.dir':'./css' 
        }, 
        '/js': { 
            'tools.staticdir.on': True, 
            'tools.staticdir.dir':'./js' 
        },
	}
    
    #application configuration
	cherrypy.tree.mount(LibraryBook(), '/', app_config)
    #server-socket configuration
	cherrypy.config.update({'server.socket_host': '127.0.0.1'})
	cherrypy.config.update({'server.socket_port': 8083})
    #running web-app
	cherrypy.engine.start()
	cherrypy.engine.block()
