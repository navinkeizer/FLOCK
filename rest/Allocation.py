import pandas as pd
import numpy as np
import time
from matching.games import StableMarriage

class Allocation:

    def __init__(self):
        self.client_preferences = pd.read_pickle('c_pref.pkl')
        self.seller_preferences = pd.read_pickle('s_pref.pkl')
        self.valuations = pd.read_pickle('c_value.pkl')
        # print(self.seller_preferences.head())


    def prepare(self):
        print(self.client_preferences)
        print(self.seller_preferences)

        tmp_c = self.client_preferences.copy()
        tmp_s = self.seller_preferences.copy()

        clients = {}
        sellers = {}

        #  TODO: Should do this in Populate rather than here as there the data is prepared. Maybe add prepare function

        # for clients
        for client in self.client_preferences.index:

            # find correct sequence
            node = ''
            rounds = len(self.client_preferences)+1

            while rounds > 1:
                min = len(self.client_preferences) + 1

                for k in self.client_preferences.columns:

                    if tmp_c[k][client] < min:
                        min = tmp_c[k][client]
                        node = k

                # create dict entry
                if client in clients:
                    clients[client].append(node)
                else:
                    clients[client] = [node]

                tmp_c[node][client] = len(self.client_preferences)+1
                rounds -=1

        # print(clients)

        # for sellers
        for seller in self.seller_preferences.index:

            # find correct sequence
            node = ''
            rounds = len(self.seller_preferences)+1

            while rounds > 1:
                min = len(self.seller_preferences) + 1

                for l in self.seller_preferences.columns:

                    if tmp_s[l][seller] < min:
                        min = tmp_s[l][seller]
                        node = l

                # create dict entry
                if seller in sellers:
                    sellers[seller].append(node)
                else:
                    sellers[seller] = [node]

                tmp_s[node][seller] = len(self.seller_preferences)+1
                rounds -=1


        # print(sellers)
        return clients, sellers


    def simple_stable_matching(self, preferences):
        c_pref = preferences[0]
        s_pref = preferences[1]
        print(c_pref, s_pref)

        t1 = time.time()
        game = StableMarriage.create_from_dictionaries(c_pref, s_pref)
        matching = game.solve()
        t2 = time.time()

        print(matching)
        print("Time: " + str(t2 - t1) + " seconds")

    def main(self):
        self.simple_stable_matching(self.prepare())
        # clients_to_preferences = {}


if __name__ == '__main__':
    a = Allocation()
    a.main()