from http_client import Http_client, InvalidSLTokenException
from config import Config
from data_miner import Data_miner
import json

class SocialPostsApp:

    _data_miner = Data_miner()

    @staticmethod
    def initialise_app_config(email, name):
        Config.set("email", email)    # set new username value
        Config.set("name", name)    # set new username value

    @staticmethod
    def get_app_token():
        client_id = Config.get("client_id")
        email = Config.get("email")
        name = Config.get("name")
        token_query_data = {"client_id": client_id, "email":email, "name": name}
        sl_token = Http_client.get_token(token_query_data)
        return sl_token

    @staticmethod
    def fetch_all_posts():
        posts = []
        retry = 0
        while True: # Infinite loop to give retries a chance.
            try:
                sl_token = SocialPostsApp.get_app_token()
                for page_no in range(1,11):
                    # sl_token = 'smslt_48cbb38db38_64785040a5623b'
                    fetch_posts_data = {"sl_token":sl_token, "page":page_no}
                    posts_per_page = Http_client.get_posts(fetch_posts_data)

                    posts.extend(posts_per_page)
                break
            except InvalidSLTokenException as e:
                # Try to get latest token 3 times else we raise & terminate
                if retry < 3:
                    retry = retry + 1
                else:
                    raise Exception("Critical error:: Unable to fetch posts -- (Possible reasons -- sltoken invalid & invalid url)")
        return posts

    @staticmethod
    def load_data_miner(data):
        SocialPostsApp._data_miner.load_data(data)

    @staticmethod
    def mine_data():
        data_miner = SocialPostsApp._data_miner
        # # Average character length of a post / month
        avg_char_len_per_month = data_miner.get_avg_vals_per_group("month", "char_cnt")

        # # Longest post by character length / month
        max_char_len_by_month = data_miner.get_max_vals_per_group("month", "char_cnt")
        # df.groupby(["month"])["char_cnt"].max()

        # # Total posts split by week
        total_posts_by_week = data_miner.get_count_vals_per_group("week", "char_cnt")
        # df.groupby(["week"])["char_cnt"].count()

        # Total No of posts for the month
        # posts_per_month = df.groupby(["month"])["char_cnt"].count()
        posts_per_month = data_miner.get_count_vals_per_group("month", "char_cnt")

        # Total no of users per month
        # users_per_month = df.groupby(["month"])["from_id"].nunique()
        unique_users_per_month = data_miner.get_unique_vals_per_group("month", "from_id")

        # Average number of posts per user / month
        avg_posts_per_user_per_month = posts_per_month/unique_users_per_month

        results_dict = {
            "avg_char_len_per_month": avg_char_len_per_month,
            "max_char_len_by_month":max_char_len_by_month,
            "total_posts_by_week":total_posts_by_week,
            "avg_posts_per_user_per_month":avg_posts_per_user_per_month
        }
        return results_dict

if __name__ == "__main__":

    SocialPostsApp.initialise_app_config("m@m.m","MP")
    all_posts = SocialPostsApp.fetch_all_posts()
    SocialPostsApp.load_data_miner(all_posts)

    results = SocialPostsApp.mine_data()

    print(f"Results are::{results}")