class Config:
    __conf = {
        "client_id": "",
        "email": "",
        "name": ""
    }
    __setters = ["client_id", "email", "name"]

    def __init__(self, *args, **kwargs):
        self.set("client_id", args[0])
        self.set("email", args[1])
        self.set("name", args[2])

    def get(self, name):
        """
        Returns configuration value against the key provided

        Parameters
        ----------
        name: str
            -- Name of the Key whose corresponding value needs to be retrived

        Returns
        -------
        str
            -- Returns string value corresponding to the key
        """
        return Config.__conf[name]

    def set(self, name, value):
        """
        Sets Config Variables.

        Configures variables only available in the setter. Anything outside the setter will raise exception

        Parameters
        ----------
        name: str
            -- Name of the setting that needs to be configured

        value: str
            -- Value of the setting that needs to be configured

        Returns
        -------

        Exceptions
        ---------

        NameError
            --  Raises Error when setting is not accepted
        """
        if name in Config.__setters:
            Config.__conf[name] = value
        else:
            raise NameError("Name not accepted in set() method")