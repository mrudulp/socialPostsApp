import requests

class InvalidSLTokenException(Exception):
    def __init__(self, message, errors):

        # Call the base class constructor with the parameters it needs
        super().__init__(message)

        # Now for your custom code...
        self.errors = errors

class HttpClient:

    __token_registration_url = "https://api.supermetrics.com/assignment/register"
    __posts_url = "https://api.supermetrics.com/assignment/posts"

    @staticmethod
    def get_token(data):
        """
        Gets Token

        Parameters
        ----------
        data : dict
            -- Dictionary of Parameters to the server

        Returns
        -------
        str
           -- Token string (token will only last 1 hour)
        """
        response = requests.post(HttpClient.__token_registration_url, data)
        if response.status_code == 200:
            return HttpClient.__extract_data(response, 'sl_token')
        else: # One would expect to receive tokens, if not its error condition.
            raise Exception(f"Failed to get SL Token::{response.status_code}" \
                            f" & Reason is ::{response.json()['error']['message']}")

    @staticmethod
    def get_posts(data):
        """
        Get Posts.

        Parameters
        ----------
        data : dict
            -- Dictionary of Parameters to the server

        Returns
        -------
        list
            -- List of posts (100 posts per page)

        Exceptions
        ----------

        InvalidSLTokenException
            -- Exception raised when SL Token is invalid

        Exception
            -- Generic Exception raised
        """

        posts_response = requests.get(HttpClient.__posts_url, params=data)
        if posts_response.status_code == 200:
            return HttpClient.__extract_data(posts_response, 'posts')
        else: # we dont retry here, but raise error and leave it to application to decide how to handle it
            reason = posts_response.json()['error']['message']
            if reason == "Invalid SL Token":
                raise InvalidSLTokenException("SL Token is Invalid. Please use latest token", '')
            else:
                raise Exception(f"Failed with Error Code::{posts_response.status_code}" \
                            f" & Reason is ::{posts_response.json()['error']['message']}")

    @staticmethod
    def __extract_data(res, action_key):
        """
        Extracts data from response object for a given key.

        Parameters
        ----------
        res : response
            -- Response Object

        action_key: str
            -- key related to object

        Returns
        -------
        json
            -- Returns json object
        """

        return res.json()['data'][action_key]