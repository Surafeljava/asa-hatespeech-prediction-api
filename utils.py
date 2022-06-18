import re
# import sys
# sys.path.append('/var/www/webApp/webApp')


class Utils:

    def __init__(self):
        pass

    def checkIfValidTweetId(self, tweetId):
        # regex to check if a tweet id is valid
        check = re.match('[0-9]{18}', tweetId)
        # print(True if check else False)
        return check
