
import os, numpy as np, pandas as pd
from datetime import datetime as dt

class Bidamic(object):
    
    def __init__(self, file_path):
        
        print("LOADING CSV.... PLEASE WAIT")
        
        
        
        self.file_path = file_path
        
        self.data = pd.read_csv(self.file_path, engine="python", sep="\t", encoding="UTF-16")
        
        self.columns = {self.data.columns[i]: i for i in range(len(self.data.columns))}
        
        self.df = np.array(self.data)
        
        self.output = {"search_term": [], "clicks": [], "cost": [], "impressions": [],
                 "conversion_value": [], "roas": []}
        
        self.currency= "GBP" ### The only currency in the coding_challenge_data.csv file. Also, for sake of time.
        
        self.path = os.getcwd()
        
        if os.path.isdir(self.path + "/processed") == False:
            os.mkdir(self.path + "/processed")
        
        self.saved_df = None


    def get_processed_df(self):
        
        if self.saved_df is not None:
            
            
            return self.saved_df
        
        else:
            print("No pandas dataframe yet")
            return None
        
    def show_arr(self):
        
        return self.df
        
    def show_data(self):
        
        return self.data
    
    
    def get_columns(self):
        
        return self.columns
    
    
    
    def save_csv_file(self):
        
        
        """Requires a pandas dataframe, saved_df = dataframe"""
        
        if self.saved_df is not None:
        
            timestamp = dt.strftime(dt.now(), "%Y-%m-%d_%H-%M-%S")

            does_currency_path_exist = os.path.isdir(self.path + "/processed/{}".format(self.currency))

            print("DOES PATH EXIST?", does_currency_path_exist)
            
            if does_currency_path_exist == False:

                os.mkdir(self.path +"/processed/{}".format(self.currency))
                os.mkdir(self.path + "/processed/{}/search_terms".format(self.currency))
                self.saved_df.to_csv(self.path + "/processed/{}/search_terms/{}.csv".format(*[self.currency, timestamp]))

            else:

                print("CURRENCY PATH ALREADY EXISTS")
#            self.
                self.saved_df.to_csv(self.path + "/processed/{}/search_terms/{}.csv".format(*[self.currency, timestamp]))

        else:
            
            print("ERROR. REQUIRES A PANDAS DATAFRAME")
    
    
    
    def search_multi_word_term(self, multi_term = None):

        if multi_term is None:

            multi_term = input("Enter multiple words for search term: ")

            check = multi_term.split(" ")
            
            list_terms = check

        else:

            check = multi_term.split(" ")

            list_terms = check

        st_list = []

        for i in range(self.df.shape[0]):
            
            check_data_bool = all(term in self.df[0:, 0][i]  for term in  list_terms)
            
            if check_data_bool:

                st_list.append(self.df[i].tolist())

        for i in range(len(st_list)):

            try:

                conversion = st_list[i][self.columns["Conversions"]]
                cost = st_list[i][self.columns["Cost"]]

                value = int(conversion) / int(cost)
                
            except ZeroDivisionError:
                
                value = 0
                
            self.output["search_term"].append(list_terms)
            self.output["clicks"].append(st_list[i][5])
            self.output["cost"].append(st_list[i][7])
            self.output["impressions"].append(st_list[i][8])
            self.output["conversion_value"].append(st_list[i][10])
            self.output["roas"].append(float(value))
        #     output["currency"].append(st_list[i][6])

        # search_term, clicks, cost, impressions, conversion_value, roas
        self.saved_df = pd.DataFrame(self.output)

        self.save_csv_file()

    def search_one_word_term(self, search_term =None):
        
        
        if search_term is None:
            search_term = input("Enter one word for search term: ")
        
        check = search_term.split(" ")
        
        if len(check) != 1:
            
            print("""Must be one word search.
            For multiple words, please use search_multi_word_term method""")
            
        else:
        
            st_list = [self.df[i].tolist() for i in range(self.df.shape[0])
                      if search_term in str(self.df[i][0])]
            print(len(st_list))

            
            for i in range(len(st_list)):

                try:

                    conversion = st_list[i][self.columns["Conversions"]]
                    cost = st_list[i][self.columns["Cost"]]

                    value = int(conversion) / int(cost)
                except ZeroDivisionError:
                    value = 0
                #roas.append(value)

                self.output["search_term"].append(search_term)
                self.output["clicks"].append(st_list[i][5])
                self.output["cost"].append(st_list[i][7])
                self.output["impressions"].append(st_list[i][8])
                self.output["conversion_value"].append(st_list[i][10])
                self.output["roas"].append(float(value))
            #     output["currency"].append(st_list[i][6])

            # search_term, clicks, cost, impressions, conversion_value, roas
            self.saved_df = pd.DataFrame(self.output)
            self.save_csv_file()
            
        
        
