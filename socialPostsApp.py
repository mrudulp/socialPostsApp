from http_client import Http_client
class SocialPostsApp:
  __conf = {
    "client_id": "ju16a6m81mhid5ue1z3v2g0uh",
    "email": "",
    "name": ""
  }
  __setters = ["email", "name"]

  @staticmethod
  def config(name):
    return SocialPostsApp.__conf[name]

  @staticmethod
  def set(name, value):
    if name in SocialPostsApp.__setters:
      SocialPostsApp.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")

if __name__ == "__main__":
    # from config import App
    SocialPostsApp.config("client_id")     # return 3306
    SocialPostsApp.set("email", "your@email.address")    # set new username value
    SocialPostsApp.set("name", "MP")    # set new username value

    #    token_reg_url = SocialPostsApp.config("token_registration_url")
    client_id = SocialPostsApp.config("client_id")
    email = SocialPostsApp.config("email")
    name = SocialPostsApp.config("name")
    token_query_data = {"client_id": client_id, "email":email, "name": name}
    sl_token = Http_client.get_token(token_query_data)
    # sl_token = 'smslt_48cbb38db38_64785040a5623b'
    fetch_posts_data = {"sl_token":sl_token, "page":1}
    posts = Http_client.get_posts(fetch_posts_data)
    # Format the final result with expected values in json format

    print("ending")