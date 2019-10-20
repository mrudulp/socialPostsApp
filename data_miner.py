import pandas as pd
import json

class DataMiner:

    def load_data(self, data):
        """
        Loads data that miner uses further.

        Parameters
        ----------
        data : json/list
            -- Data to be loaded. At the moment engine handles only json or list data

        Returns
        -------

        """

        if type(data) is "json":
            dataF = pd.read_json(data)
        elif type(data) is list:
            dataF = pd.DataFrame(data)
        else:
            print("Other types not implemented")
            return
        dataF = self.__process_data(dataF)
        self.__dataF = dataF

    def __process_data(self, dataF):
        """
        Process Data

        Processes data to create further custom columns that can be utiliesed later on.

        Parameters
        ----------
        dataF : dataframe
            -- Table/Dataframe that needs futher processing

        Returns
        -------
        dataF
            -- Processed Dataframe containing requisite information.
        """

        dataF['created_time'] = pd.to_datetime(dataF['created_time'])
        dataF['char_cnt'] = dataF['message'].str.len()
        dataF['month'] = dataF['created_time'].dt.month
        dataF['week'] = dataF['created_time'].dt.week

        return dataF


    def get_avg_vals_per_group(self, group_col_name, val_col_name):
        """
        Get Average/Mean values per group.

        Average/Mean values for a given column

        Parameters
        ----------
        group_col_name : str
            -- Name of the column by which to group data

        val_col_name : str
            -- Column name from which Unique values need to be retrived

        Returns
        -------
        list
            -- Returns list of average/mean values
        """

        return self.__dataF.groupby([group_col_name])[val_col_name].mean()


    def get_max_vals_per_group(self, group_col_name, val_col_name):
        """
        Get Max values per group.

        Max values for a given column

        Parameters
        ----------
        group_col_name : str
            -- Name of the column by which to group data

        val_col_name : str
            -- Column name from which Unique values need to be retrived

        Returns
        -------
        list
            -- Returns list of max values
        """

        return self.__dataF.groupby([group_col_name])[val_col_name].max()


    def get_count_vals_per_group(self, group_col_name, val_col_name):
        """
        Get Count of values per group.

        Count of values for a given column

        Parameters
        ----------
        group_col_name : str
            Name of the column by which to group data

        val_col_name : str
            Column name from which Unique values need to be retrived

        Returns
        -------
        list
            Returns list of count
        """

        return self.__dataF.groupby([group_col_name])[val_col_name].count()


    def get_unique_vals_per_group(self, group_col_name, val_col_name):
        """
        Get Unique values per group.

        Unique values for a given column

        Parameters
        ----------
        group_col_name : str
            -- Name of the column by which to group data

        val_col_name : str
            -- Column name from which Unique values need to be retrived

        Returns
        -------
        list
            -- Returns list of unique values
        """

        return self.__dataF.groupby([group_col_name])[val_col_name].nunique()