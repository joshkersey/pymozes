# 
#  Python Wrapper for Mozes API
#  
#  Created by Josh Kersey on 2009-09-22.
#  Copyright 2010 cabedge.com. All rights reserved.

import md5, time, urllib
from xml.dom import minidom

class MozesApi(object):
    '''
    To use Mozes partner APIs, you first need an API key and shared secret. Contact support@mozes-inc.com to request them.
    '''
    
    api_url = "https://www.mozes.com/_/api/mob_" # the base URL to the Mozes API
    api_key = '<< MOZES_API_KEY >>'
    shared_secret = '<< MOZES_SHARED_SECRET >>'
    debug_requests = False # set True to print the URL sent to the server
    debug_responses = False # set True to print the XML received from the server
    
    def subscribe(self, phone, keyword):
        api_type = 'subscribe'
        response = self._api_call(api_type, phone, keyword)
        return response
    
    def unsubscribe(self, phone, keyword):
        api_type = 'unsubscribe'
        response = self._api_call(api_type, phone, keyword)
        return response
        
    def status(self, phone, keyword):
        api_type = 'user_status'
        response = self._api_call(api_type, phone, keyword)
        status = self._parse_status(response)
        if status == "true":
            return True
        return False
        
    def _generate_auth_token(self, salt, phone):
        m = md5.new()
        m.update(self.shared_secret)
        if phone:
            m.update(phone)
        m.update(salt)
        auth_token = m.hexdigest()
        return auth_token
        
    def _api_call(self, api_type, phone, keyword):
        '''
        Accesses the API.
        
        Keyword arguments:
        - api_type: the API type you wish to envoke
        - phone: target phone number for action
        - keyword: target campaign keyword for action
        '''
        salt = str(time.time())
        auth_token = self._generate_auth_token(salt, phone)
        params = urllib.urlencode({
            'partner_login': self.api_key,
            'keyword': keyword,
            'phone': phone,
            'time': salt,
            'token': auth_token
        })
        
        url = self.api_url + api_type + "?" + str(params)
        if self.debug_requests:
            print "Request URL:"
            print url
            
        request = urllib.urlopen(url)
        response = request.read()
        if self.debug_responses:
            print "Response:"
            print response

        return response
        
    def _parse_status(self, response):
        '''
        The Mozes API returns status requests in the format:
        <?xml version="1.0" ?>
            <MozesMobUserStatusResult>
                <Status>SUCCESS</Status>
                <ErrorMsg></ErrorMsg>
                <Keyword>iammobile</Keyword>
                <Phone>15559991234</Phone>
                <IsSubscribed>false</IsSubscribed>
            </MozesMobUserStatusResult>

        This method parses the response and returns the enclosed value for IsSubscribed.

        Keyword arguments:
        - response: the response to parse

        Returns the string value of the response.  You will need to coerce to the required type if different type is needed.
        '''
        doc = minidom.parseString(response)
        if doc.hasChildNodes:
            node = doc.getElementsByTagName("IsSubscribed")
            status = node[0].firstChild.data
            return status
        return None