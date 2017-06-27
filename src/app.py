import tweepy
import json



# Try authentication via OAuth.
def get_tweepy_api(filepath):
    """
    Try Authentication via tweepy.
    :param filepath: the json file contains consumer/access variables
    :return: True if everything went well, False otherwise
    """
    consumerVariables = []
    accessVariables = []
    iterator = 1

    with open(filepath) as json_data:
        d = json.load(json_data)
        # print(type(d))
        if type(d) is dict:
            if (not "consumerKey" in d) or (not "consumerSecret" in d):
                print("TryAuth: either consumerKey or consumerSecret is invalid.")
                return None

            if (not "accessToken" in d) or (not "accessTokenSecret" in d):
                print("TryAuth: either accessToken or accessTokenSecret is invalid.")
                return None

            consumer_key = d["consumerKey"]
            consumer_secret = d["consumerSecret"]
            consumerVariables.append(consumer_key)
            consumerVariables.append(consumer_secret)

            accessVariables.append(d["accessToken"])
            accessVariables.append(d["accessTokenSecret"])
        else:
            print("TryAuth: Invalid token information file.")
            return None

    auth = tweepy.OAuthHandler(*consumerVariables)
    auth.set_access_token(*accessVariables)

    try:
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print("TryAuth: Failed to get request token.")
        return None

    tweepy_api = tweepy.API(auth_handler=auth)

    '''
    return_value = flatten_quoted_tweets(tweepy_api, 824530730650726401)
    print(return_value)
    '''

    return tweepy_api


# The main recursive flattening function
def flatten_quoted_tweets(tweepy_api, status_id):
    '''
    Flattens quoted tweets, i.e. Shows quoted tweet's status from quote tweet.
    :param tweepy_api: A tweepy API instance
    :param status_id: Target tweet's id
    :return: A string contains all of the tweets
    '''

    status = get_status_safely(tweepy_api, status_id)
    if status is None:
        return '##Inaccessible tweet##'
    if status.is_quote_status is False:
        return status.text
    else:
        return f'{status.text}\n{flatten_quoted_tweets(tweepy_api, status.quoted_status_id)}'


def get_status_safely(tweepy_api, status_id):
    try:
        deleted_status = tweepy_api.get_status(status_id)
        return deleted_status
    except tweepy.TweepError as err:
        # Can be access as err['code'] and err['message']
        print('get_status_safely: Failed with error {}: {}'.format(err.api_code, err.args[0][0]['message']))
        return None


def get_tweet_id_from_url(tweet_url):
    # @TODO: use regex to verify tweet_url is a twitter status url, and get status id from it

    pass


def main():
    print("Hello World!")
    tweepy_api = get_tweepy_api("../Keys.json")
    if tweepy_api:
        # Do the main job
        print("Successfully initialized api object.")
        tweet_address = input("Input target tweet address: ")
        tweet_id = get_tweet_id_from_url(tweet_address)
        flattened_tweets = flatten_quoted_tweets(tweepy_api, status_id=824530730650726401)
        if flattened_tweets:
            print(flattened_tweets)

    else:
        # Bleh I failed
        print("Bleh, failed.")
        pass


if __name__ == "__main__":
    main()
