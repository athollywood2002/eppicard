#!/usr/bin/python

import re
import requests

def login(username, password):
    loginPayload = {'login' : username}
    passPayload = {'password' : password}
    s = requests.Session()

    # POST the username
    url = 'https://www.eppicard.com/nvedcclient/factor2UserId.recip'
    postData = loginPayload.copy()
    response = s.post(url, postData)
    if response.status_code != requests.codes.ok:
        raise ValueError("Bad response in first pass %s" % response.status_code)
    postData.update(passPayload)
    tokenParam = token_search(response.text)
    if tokenParam is not None:
        postData.update(tokenParam)
    else:
        raise ValueError("No token value found!")
    # POST with password and the token
    url = 'https://www.eppicard.com/nvedcclient/siteLogonClient.recip'
    r = s.post(url, postData)
    if r.status_code != 200:
        raise ValueError("Bad response in Second pass %s" % r.status_code)
    bal = findBal(r.text)
    return str(bal)   

def token_search(resp_text):
    # uses regex to find the Token from the HTML
    patFinder2 = re.compile(r"name=\"(org.apache.struts.taglib.html.TOKEN)\"\s+value=\"(.+)\"",re.I)
    findPat2 = re.search(patFinder2, resp_text)

    # if the Token in found it turns it into a dictionary. and prints the dictionary 
    # if no Token is found it prints "nothing found" 
    if findPat2:
        newdict = dict(zip(findPat2.group(1).split(), findPat2.group(2).split()))
        return newdict
    else:
        print "No Token Found"

def logout():
    # do something to logout of the eppicard system. We got in
    pass

def findBal(r_text):
    balFind2 = re.compile(r"rightmain_content\s\list\"\s\w{5}=\"\center\">\s+(\$\d+.\d+)")
    findBal = re.search(balFind2, r_text)

    if(findBal):
        return "Your Balance is:",str(findBal.group(1))
    else:
        return "No Balance Found"

a = login('USERNAME', 'PASSWORD')
a = re.sub(r'^\(|\)|\,|\'','',a)
print a

