import pandas as pd
import json

class Data_miner:

    _dataF = None
    def load_data(self, data):
        if type(data) is "json":
            dataF = pd.read_json(data)
        elif type(data) is list:
            dataF = pd.DataFrame(data)
        else:
            print("Other types not implemented")
            return
        dataF = Data_miner._process_data(dataF)
        Data_miner._dataF = dataF
        # dataF.to_excel("data_ex.xlsx")
        with open("data_ex.json","a") as fout:
            json.dump(data, fout)

    def print_head(self):
        print(Data_miner._dataF.head())

    def print_info(self):
        print(Data_miner._dataF.info())

    @staticmethod
    def _process_data(dataF):
        dataF['created_time'] = pd.to_datetime(dataF['created_time'])
        dataF['char_cnt'] = dataF['message'].str.len()
        dataF['month'] = dataF['created_time'].dt.month
        dataF['week'] = dataF['created_time'].dt.week
        return dataF

    def get_avg_vals_per_group(self, group_col_name, val_col_name):
        return Data_miner._dataF.groupby([group_col_name])[val_col_name].mean()

    def get_max_vals_per_group(self, group_col_name, val_col_name):
        return Data_miner._dataF.groupby([group_col_name])[val_col_name].max()

    def get_count_vals_per_group(self, group_col_name, val_col_name):
        return Data_miner._dataF.groupby([group_col_name])[val_col_name].count()

    def get_unique_vals_per_group(self, group_col_name, val_col_name):
        return Data_miner._dataF.groupby([group_col_name])[val_col_name].nunique()