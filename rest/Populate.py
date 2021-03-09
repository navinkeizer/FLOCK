import numpy as np
import random
import pandas as pd
import time
import yaml


class Populate:

    def __init__(self, clients, sellers):
        self.Clients = clients
        self.Sellers = sellers
        # uncomment to replicate results
        # random.seed(20)

    # Function to populate the allocations for the first evaluation
    # This is excluding budget and assumes binary items
    # This can be applied to our use case for the Filecoin retrieval market
    # Data to be used in SMI and second price auction simulations
    def populate1(self, clients, sellers, reserve_prices, capacities, client_preference_amount = 1, seller_preference_amount =1):

        client_valuations = pd.DataFrame(columns=sellers, index=clients)
        client_preferences = pd.DataFrame(index=clients, columns=sellers)
        seller_preferences = pd.DataFrame(index=sellers, columns=clients)

        for x in range(0, len(client_valuations.index)):
            for y in range(0, len(client_valuations.columns)):
                client_valuations['S'+str(y)]['C' + str(x)] = random.randint(1, 100)

        client_valuations2 = client_valuations.copy()

        if client_preference_amount != 1:
            es=client_preference_amount
        else:
            es = len(client_valuations2.columns)

        for i in range(0, len(clients)):
            empty_spots = es
            rnd = 1

            while empty_spots >=1:
                max = 0
                node = -1

                for j in range(0, len(sellers)):

                    if client_valuations2['S' + str(j)]['C'+str(i)] > max:
                        max = client_valuations2['S'+str(j)]['C' + str(i)]
                        node = j

                client_preferences['S' + str(node)]['C' + str(i)] = rnd
                client_valuations2['S' + str(node)]['C' + str(i)] = 0

                rnd = rnd +1
                empty_spots = empty_spots - 1

        # TODO: add variance in preference list sizes

        if seller_preference_amount !=1:
            spa = seller_preference_amount+1
        else:
            spa = len(clients) + 1
        for k in range(len(seller_preferences.index)):
            available = list(range(1, len(seller_preferences.columns) + 1))
            for l in range(len(seller_preferences.columns)):
                t = random.choice(available)
                if t < spa:
                    seller_preferences['C' + str(l)]['S' + str(k)] = t
                available.remove(t)

        # print(client_valuations)
        # print(client_preferences)
        # print(seller_preferences)
        # print(reserve_prices)
        # print(capacities)

        client_valuations.to_pickle('c_value.pkl')
        client_preferences.to_pickle('c_pref.pkl')
        seller_preferences.to_pickle('s_pref.pkl')

        # df = pd.read_pickle('c_value.pkl')
        # print(df)

    # Start creating data files
    def start_fill(self, capacity_max, c_preference_amount, s_preference_amount):
        # create client and seller lists
        clients = []
        sellers = []
        seller_capacity = []
        seller_reserve_price = []

        for client in range(0, self.Clients):
            clients.append("C" + str(client))

        for seller in range(0, self.Sellers):
            sellers.append("S" + str(seller))

            # TODO: switch to more reliable/applicable distribution for random number
            seller_capacity.append(float(random.randint(1, capacity_max)))
            seller_reserve_price.append(float(random.randint(5, 40)))

        # print(clients)
        # print(sellers)
        # print(seller_capacity)
        # print(seller_reserveprice)

        self.populate1(clients, sellers, seller_reserve_price, seller_capacity, c_preference_amount,s_preference_amount)





if __name__ == '__main__':
    t1 = time.time()
    p1 = Populate (10, 10)
    p1.start_fill(8, 1, 1)
    t2 = time.time()
    print("Time: " + str(t2-t1) + " seconds")
