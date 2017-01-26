import tweepy
import json


# Try authentication via OAuth.
def TryAuth(filepath):
    """
    Try Authentication via tweepy.
    :param filepath: the json file contains consumer/access variables
    :return: True if everything went well, False otherwise
    """
    consumerVariables = []
    accessVariables = []

    with open(filepath) as json_data:
        d = json.load(json_data)
        # print(type(d))
        if type(d) is dict:
            if (not "consumerKey" in d) or (not "consumerSecret" in d):
                print("TryAuth: either consumerKey or consumerSecret is invalid.")
                return False

            consumer_key = d["consumerKey"]
            consumer_secret = d["consumerSecret"]
            consumerVariables.append(consumer_key)
            consumerVariables.append(consumer_secret)

            if (not "accessToken" in d) or (not "accessTokenSecret" in d):
                print("TryAuth: either accessToken or accessTokenSecret is invalid.")
                return False

            accessVariables.append(d["accessToken"])
            accessVariables.append(d["accessTokenSecret"])

    auth = tweepy.OAuthHandler(*consumerVariables)
    auth.set_access_token(*accessVariables)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("TryAuth: Failed to get request token.")

    # session.set("request_token", auth.request_token)

    tweepy_api = tweepy.API(auth_handler=auth)
    info = tweepy_api.get_user("sikinmettugi")

    print(info)

    return True


def main():
    print("Hello World!")
    isSuccess = TryAuth("../Keys.json")
    if isSuccess:
        # Do the main job
        print("Job succeed.")
    else:
        # Bleh I failed
        print("Bleh, failed.")
        pass


if __name__ == "__main__":
    main()
