#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
import jinja2
from google.appengine.api import mail, app_identity
# from google.appengine.api import users

# Lets set it up so we know where we stored the template files
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class AboutHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('templates/about.html')
    	self.response.write(template.render({'title': 'ABOUT'}))

class GalleryHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('templates/gallery.html')
    	self.response.write(template.render({'title': 'GALLERY'}))


class ResumeHandler(webapp2.RequestHandler):
    def get(self):
    	template = JINJA_ENVIRONMENT.get_template('templates/resume.html')
    	self.response.write(template.render({'title': 'RESUME'}))

class MailHandler(webapp2.RequestHandler):
    def get(self):
        template = JINJA_ENVIRONMENT.get_template('templates/mail.html')
        self.response.write(template.render({'title': 'MAIL ME'}))   

    def post(self):
        app_id = app_identity.get_application_id()
        sender = "%s <no-reply@%s.appspotmail.com>" % (app_id, app_id)

        to = self.request.get("to")
        subject = self.request.get("subject")
        body = self.request.get("message") + "This mail was sent by:" + self.request.get("email")

        try:
            message = mail.EmailMessage()
            message.sender = sender
            message.to = "qiongyu@umich.edu"
            message.subject = subject
            message.html = body
            message.send()
        except Exception, e:
            logging.error("Error sending email: %s" % e)

        template = JINJA_ENVIRONMENT.get_template('templates/mail.html')
        self.response.write(template.render({'success_message': 'Email Sent!!'}))

app = webapp2.WSGIApplication([
    ('/', AboutHandler),
    ('/about.html', AboutHandler),
    ('/gallery.html', GalleryHandler),
    ('/resume.html', ResumeHandler), 
    ('/mail.html', MailHandler),  
    #put all the header on one header
], debug=True)










