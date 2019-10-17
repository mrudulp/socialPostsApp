import requests

class InvalidSLTokenException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class Http_client:

    token_registration_url = "https://api.supermetrics.com/assignment/register"
    posts_url = "https://api.supermetrics.com/assignment/posts"

    @staticmethod
    def get_token(data):
    # POST: https://api.supermetrics.com/assignment/register

    # PARAMS:
    #     client_id: ju16a6m81mhid5ue1z3v2g0uh
    #     email: your@email.address
    #     name: Your Name

    # RETURNS
    #     sl_token: This token string should be used in the subsequent query. Please note that this token will only last 1 hour from when the REGISTER call happens. You will need to register and fetch a new token as you need it.
    #     client_id: returned for informational purposes only
    #     email: returned for informational purposes only
        response = requests.post(Http_client.token_registration_url, data)
        if response.status_code == 200:
            return Http_client.extract_data(response, 'sl_token')
        else: # One would expect to receive tokens, if not its error condition.
            raise Exception(f"Failed to get SL Token::{response.status_code}" \
                            f" & Reason is ::{response.json()['error']['message']}")
        #'smslt_48cbb38db38_64785040a5623b'

    @staticmethod
    def get_posts(data):

    # GET: https://api.supermetrics.com/assignment/posts

    # PARAMS:
    #     sl_token: Token from the register call
    #     page: integer page number of posts (1-10)

    # RETURNS:
    #     page: What page was requested or retrieved
    #     posts: 100 posts per page

        posts_response = requests.get(Http_client.posts_url, params=data)
        if posts_response.status_code == 200:
            return Http_client.extract_data(posts_response, 'posts')
        else: # we dont retry to get token due to single responsibility principle, hence raise error
            reason = posts_response.json()['error']['message']
            if reason == "Invalid SL Token":
                raise InvalidSLTokenException("SL Token is Invalid. Please use latest token", '')
            else:
                raise Exception(f"Failed with Error Code::{posts_response.status_code}" \
                            f" & Reason is ::{posts_response.json()['error']['message']}")

    @staticmethod
    def extract_data(res, action_key):
        return res.json()['data'][action_key]