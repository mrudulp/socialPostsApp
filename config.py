class Config:
  __conf = {
    "client_id": "ju16a6m81mhid5ue1z3v2g0uh",
    "email": "",
    "name": ""
  }
  __setters = ["email", "name"]

  @staticmethod
  def get(name):
    return Config.__conf[name]

  @staticmethod
  def set(name, value):
    if name in Config.__setters:
      Config.__conf[name] = value
    else:
      raise NameError("Name not accepted in set() method")