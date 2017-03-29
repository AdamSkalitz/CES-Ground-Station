'''
Created on 13 Feb 2016
@author: Charlotte Alexandra Wilson

Last revision: 28 March 2017
see bitbucket for details:
https://CharlotteWilson@bitbucket.org/CharlotteWilson/dnnpd.git
---------------------------------------------------------------

Class created for sending out tweets whenever called by another
class/script. Given a string, updates the status of the twitter
account it is connecting to using api.update_status("string")

To set up the twitter app, you must first go to the following:
https://apps.twitter.com/
Follow the instructions, and then go to the tweepy main page or
github page. Download the library, and follow the instructions
on their page for connecting to your app etc.
---------------------------------------------------------------
CES GROUND STATION USAGE: ground_station function
This ammended version is not in the original code, but for use
with clyde space ground station only.
---------------------------------------------------------------
Used in CES ground station for Clyde Space Ltd. as a ground
station status updater.
i.e. A mission is scheduled at a certain time, not nessisarily
now, a satellite will be tracked by the rotators after mission
schedule. When the rotators begin tracking a new satellite or
new pass, a status update including the time, cube sat name
and other relevant information, will be sent to a twitter feed.
'''

import tweepy


class tweet:

    def __init__(self, something):
        # enter the corresponding information from your Twitter application:
        # keep the quotes, replace this with your consumer key
        CONSUMER_KEY = 'IgaWiE746tRu8Zw5CtmxhISit'
        # keep the quotes, replace this with your consumer secret key
        CONSUMER_SECRET = 'SlL3yWL0KUYiLXOjjqK08fSQBfqGhAlNcSgNdxEax91cX2fQ6m'
        # keep the quotes, replace this with your access token
        ACCESS_KEY = '846791513573089281-xia7pUhmibfvyN506XkIE53WWq1tBah'
        # keep the quotes, replace this with your access token secret
        ACCESS_SECRET = 'UHsaektsXLsbTTYhhQyyaXtLriWL1k0IJnbURL1TCYfJ8'
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(something)


def ground_station():
    """ update status of rotators when used: e.g. CUTE-1 is
         now being tracked at (AZEL value) """
    tweet("This is a test")


""" Testing output to cube sat tracker twitter """
ground_station()