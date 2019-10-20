from http_client import HttpClient, InvalidSLTokenException
from config import Config
from data_miner import DataMiner
import json

class SocialPostsApp:

    def __init__(self, client_id, email, name):
        self.__config = Config(client_id, email, name)
        self.__data_miner = DataMiner()

    def get_app_token(self):
        """
        Get App Token.

        Fetches Token required for the application

        Parameters
        ----------

        Returns
        -------
        str
            -- Returns token string.
        """
        client_id = self.__config.get("client_id")
        email = self.__config.get("email")
        name = self.__config.get("name")
        token_query_data = {"client_id": client_id, "email":email, "name": name}
        sl_token = HttpClient.get_token(token_query_data)
        return sl_token

    def fetch_all_posts(self):
        """
        Fetches all the posts.

        Parameters
        ----------

        Returns
        -------
        posts: list
            -- Returns a list of posts available on the server
        """

        posts = []
        retry = 0
        current_page_no = 1
        # Infinite loop to give retries a chance.
        while True:
            try:
                sl_token = self.get_app_token()
                # 1-10 pages of data available on server
                for page_no in range(current_page_no,11):

                    fetch_posts_data = {"sl_token":sl_token, "page":page_no}
                    posts_per_page = HttpClient.get_posts(fetch_posts_data)
                    # save current page_no to ensure we dont start from Page 1 on failure-retry sequence
                    current_page_no = page_no
                    # Reset Retry
                    retry = 0
                    posts.extend(posts_per_page)
                # everything went well break out of the loop
                break
            except InvalidSLTokenException as e:
                # Try to get latest token with a retry (3 times max)
                if retry < 3:
                    retry = retry + 1
                else:
                    raise Exception("Unable to fetch posts -- Check 'sltoken' &/or `url` are valid")
        return posts

    def initialise_data_miner(self, data):
        """
        Loads data miner with data that will be mined further.

        Parameters
        ----------
        data : json/list
            -- Data to be loaded. At the moment engine handles only json or list data

        Returns
        -------

        """

        self.__data_miner.load_data(data)

    def mine_data(self):
        """
        Mines data available in data miner.

        It mines & returns following information --
            1. Average character length of a post / month
            2. Longest post by character length / month
            3. Total posts split by week
            4. Average number of posts per user / month

        Parameters
        ----------

        Returns
        -------
        results:dict
            -- Returns a dictionary of mined results
        """

        # # Average character length of a post / month
        avg_char_len_per_month = self.__data_miner.get_avg_vals_per_group("month", "char_cnt")

        # # Longest post by character length / month
        max_char_len_by_month = self.__data_miner.get_max_vals_per_group("month", "char_cnt")
        # df.groupby(["month"])["char_cnt"].max()

        # # Total posts split by week
        total_posts_by_week = self.__data_miner.get_count_vals_per_group("week", "char_cnt")
        # df.groupby(["week"])["char_cnt"].count()

        # Total No of posts for the month
        # posts_per_month = df.groupby(["month"])["char_cnt"].count()
        posts_per_month = self.__data_miner.get_count_vals_per_group("month", "char_cnt")

        # Total no of users per month
        # users_per_month = df.groupby(["month"])["from_id"].nunique()
        unique_users_per_month = self.__data_miner.get_unique_vals_per_group("month", "from_id")

        # Average number of posts per user / month
        avg_posts_per_user_per_month = posts_per_month/unique_users_per_month

        results_dict = {
            'avg_char_len_per_month({"month", "char_count"})': avg_char_len_per_month.to_json(),
            'max_char_len_by_month({"month", "max_char_count"})':max_char_len_by_month.to_json(),
            'total_posts_by_week({"week","total_posts"})':total_posts_by_week.to_json(),
            'avg_posts_per_user_per_month({"month","avg_no_of_posts"})':avg_posts_per_user_per_month.to_json()
        }
        return results_dict


if __name__ == "__main__":

    client_id = "ju16a6m81mhid5ue1z3v2g0uh"
    email = "m@m.m"
    name = "MP"
    socialapp = SocialPostsApp(client_id, email, name)
    all_posts = socialapp.fetch_all_posts()
    socialapp.initialise_data_miner(all_posts)
    results = socialapp.mine_data()

    print(json.dumps(results, indent=4))
