# ----------------------------------------------------------------------------
# Created by: Navin V. Keizer
# Latest version: 7-11-2020
# This is used to
# Used for: "scalable, fast, lightweight allocation for blockchain services"
# ----------------------------------------------------------------------------

import random
import pandas as pd
import time
from matching.games import HospitalResident
import sys
import Multi_item.multi_dutch as Auction

class Setup:

    def __init__(self, number_of_clients, number_of_sellers, c_preference_length=1, s_preference_length=1, max_capacity = 3):

        self.Clients = []
        self.Sellers = []
        self.seller_capacities = {}
        self.seller_reserve_prices = {}
        self.cLength = c_preference_length
        self.sLength = s_preference_length
        for c in range(0,number_of_clients):
            self.Clients.append("C" + str(c))
        for s in range(0,number_of_sellers):
            self.Sellers.append("S" + str(s))
            self.seller_capacities["S" + str(s)] = random.randint(1, max_capacity)
            self.seller_reserve_prices["S" + str(s)] = random.randint(5, 60)

        # random.seed(20)

    def generate_simple(self):
        client_valuations = pd.DataFrame(columns=self.Sellers, index=self.Clients)
        client_pref_dict = {}
        sellers_pref_dict = {}

        # set the values for the clients (for the auctions)
        for c in self.Clients:
            for s in self.Sellers:
                client_valuations[s][c] = random.randint(1, 100)

        client_valuations2 = client_valuations.copy()

        if self.cLength != 1:
            limit = self.cLength
        else:
            limit = len(self.Sellers)

        # loop through sellers per client to find preference ordering
        for client in self.Clients:
            empty_spots = limit
            while empty_spots >= 1:
                max = 0
                node = -1

                for seller in self.Sellers:
                    if client_valuations2[seller][client] > max:
                        max = client_valuations2[seller][client]
                        node = seller
                # create dict entry
                if client in client_pref_dict:
                    client_pref_dict[client].append(node)
                else:
                    client_pref_dict[client] = [node]

                client_valuations2[node][client] = 0
                empty_spots -= 1

        # Now we generate the seller preferences
        if self.sLength != 1:
            spa = self.sLength
        else:
            spa = len(self.Clients)

        for sel in self.Sellers:
            available = list(range(0, len(self.Clients)))
            for i in range(0,spa):
                t = random.choice(available)
                available.remove(t)

                # create dict entry
                if sel in sellers_pref_dict:
                    sellers_pref_dict[sel].append('C' + str(t))
                else:
                    sellers_pref_dict[sel] = ['C' + str(t)]


        return client_pref_dict, sellers_pref_dict, client_valuations

    # Use this function when using the HR matching with asymetrical data
    def generate_for_hr(self):
        client_valuations = pd.DataFrame(columns=self.Sellers, index=self.Clients)
        client_pref_dict = {}
        sellers_pref_dict = {}

        # set the values for the clients (for the auctions)
        for c in self.Clients:
            for s in self.Sellers:
                client_valuations[s][c] = random.randint(1, 100)

        client_valuations2 = client_valuations.copy()
        # print(client_valuations)
        if self.cLength != 1:
            limit = self.cLength
        else:
            limit = len(self.Sellers)

        # loop through sellers per client to find preference ordering
        for client in self.Clients:
            empty_spots = limit
            while empty_spots >= 1:
                max = 0
                node = -1

                for seller in self.Sellers:
                    if client_valuations2[seller][client] > max:
                        max = client_valuations2[seller][client]
                        node = seller
                # create dict entry
                if client in client_pref_dict:
                    client_pref_dict[client].append(node)
                else:
                    client_pref_dict[client] = [node]

                client_valuations2[node][client] = 0
                empty_spots -= 1

        # now generate seller data based on the nodes that it has been scored by
        for sel in self.Sellers:
            available = []
            for cli in self.Clients:
                if sel in client_pref_dict[cli]:
                    available.append(cli)

            for i in range(0,len(available)):
                t = random.choice(available)
                available.remove(t)

                # create dict entry
                if sel in sellers_pref_dict:
                    sellers_pref_dict[sel].append(t)
                else:
                    sellers_pref_dict[sel] = [t]

        return client_pref_dict, sellers_pref_dict, client_valuations

    def hr_matching(self, client_pref, seller_pref):
        seller_cap = self.seller_capacities
        tot_cap = 0
        for cap in seller_cap:
            tot_cap += seller_cap[cap]

        # TODO: save all in a log file
        # print("------------------------------------")
        # print('Hospital / Resident Matching Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Total capacity: ' + str(tot_cap))
        # print('Client preferences: ' + str(client_pref))
        # print('Seller preferences: ' + str(seller_pref))
        # print('Seller capacities: ' + str(seller_cap))

        game = HospitalResident.create_from_dictionaries(client_pref, seller_pref,seller_cap)

        t1 = time.time()
        matching = game.solve()
        t2 = time.time()

        # print()
        # print('Matching soluiton: ' + str(matching))
        # print("Runtime: " + str(t2 - t1) + " seconds")

        # clean up the solution and calculate statistics
        d = dict([(k, v) for k, v in matching.items() if len(v) > 0])
        client_count = 0
        for s in d:
            client_count += len(d[s])
        # print()
        # print('Number of Clients matched: ' + str(client_count))
        # print('Number of Sellers matched: ' + str(len(d.keys())))
        # print("Percentage of Clients matched: " + str(float(client_count/len(self.Clients)*100)))
        # print("Percentage of Sellers matched: " + str(float(len(d.keys())/len(self.Sellers)*100)))

        return str(t2 - t1), str(float(client_count/len(self.Clients)*100)), str(float(len(d.keys())/len(self.Sellers)*100))

    def two_largest(self, inlist):
        largest = 0
        second_largest = 0
        index = -1
        count = 0
        for item in inlist:
            if item > largest:
                second_largest = largest
                largest = item
                index = count
            elif largest > item > second_largest:
                second_largest = item
            count += 1
        return largest, second_largest, index

    def vickery(self, valuations):
        # print(self.seller_reserve_prices)
        # print(valuations)
        t1 = time.time()
        solution = {}
        for seller in valuations.columns:
            highest_bid, price, position = self.two_largest(valuations[seller])
            # check if above reserve price
            if price > self.seller_reserve_prices[seller]:
                # create dict entry
                    solution[seller] = ["C" + str(position)]
                    solution[seller].append("$" + str(price))
        t2 = time.time()
        # print("------------------------------------")
        # print('Vickery Auction Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Auction soluiton: ' + str(solution))
        # print('Number of Clients matched: ' + str(len(solution.keys())))
        # print('Number of Sellers matched: ' + str(len(solution.keys())))
        # print("Percentage of Clients matched: " + str(float(len(solution.keys())/len(self.Clients)*100)))
        # print("Percentage of Sellers matched: " + str(float(len(solution.keys())/len(self.Sellers)*100)))
        # print("Time: " + str(t2 - t1) + " seconds")

        return str(t2 - t1)

    def baseline_allocation(self):
        t1 = time.time()
        solution = {}
        if len(self.Clients) > len(self.Sellers):
            available = self.Clients.copy()
            for seller in self.Sellers:
                t = random.choice(available)
                available.remove(t)
                solution[seller] = [t]
        else:
            available = self.Sellers.copy()
            for client in self.Clients:
                t = random.choice(available)
                available.remove(t)
                solution[client] = [t]
        t2 = time.time()
        # print("------------------------------------")
        # print('Random Allocation Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Solution: ' + str(solution))
        # print('Number of Clients matched: ' + str(len(solution.keys())))
        # print('Number of Sellers matched: ' + str(len(solution.keys())))
        # print("Percentage of Clients matched: " + str(float(len(solution.keys()) / len(self.Clients) * 100)))
        # print("Percentage of Sellers matched: " + str(float(len(solution.keys()) / len(self.Sellers) * 100)))
        # print("Time: " + str(t2 - t1) + " seconds")

        return str(t2 - t1)

    def baseline_allocation_with_capacity(self):
        t1 = time.time()
        solution = {}
        available = self.Clients.copy()
        for seller in self.Sellers:
              for i in range(1, self.seller_capacities[seller]+1):
                 if len(available) != 0:
                    t = random.choice(available)
                    available.remove(t)
                    if seller in solution:
                        solution[seller].append(t)
                    else:
                        solution[seller] = [t]
        t2 = time.time()
        # print("------------------------------------")
        # print('Random Allocation with Capacities Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Solution: ' + str(solution))
        # print('Number of Clients matched: ' + str(len(solution.keys())))
        # print('Number of Sellers matched: ' + str(len(solution.keys())))
        # print("Percentage of Clients matched: " + str(float(len(solution.keys()) / len(self.Clients) * 100)))
        # print("Percentage of Sellers matched: " + str(float(len(solution.keys()) / len(self.Sellers) * 100)))
        # print("Time: " + str(t2 - t1) + " seconds")
        return str(t2 - t1)

    def hr_matching_no_cap(self, client_pref, seller_pref):
        seller_cap = {}
        for s in range(0, len(self.Sellers)):
            seller_cap["S" + str(s)] = 1
        # TODO: save all in a log file
        # print("------------------------------------")
        # print('Hospital / Resident Matching Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Client preferences: ' + str(client_pref))
        # print('Seller preferences: ' + str(seller_pref))

        game = HospitalResident.create_from_dictionaries(client_pref, seller_pref, seller_cap)

        t1 = time.time()
        matching = game.solve()
        t2 = time.time()

        # print()
        # print('Matching soluiton: ' + str(matching))
        # print("Runtime: " + str(t2 - t1) + " seconds")

        # clean up the solution and calculate statistics
        d = dict([(k, v) for k, v in matching.items() if len(v) > 0])
        client_count = 0
        for s in d:
            client_count += len(d[s])
        # print()
        # print('Number of Clients matched: ' + str(client_count))
        # print('Number of Sellers matched: ' + str(len(d.keys())))
        # print("Percentage of Clients matched: " + str(float(client_count/len(self.Clients)*100)))
        # print("Percentage of Sellers matched: " + str(float(len(d.keys())/len(self.Sellers)*100)))

        return str(t2 - t1)

    def vda(self, value_matrix):
        seller_cap = self.seller_capacities
        tot_cap = 0
        for cap in seller_cap:
            tot_cap += seller_cap[cap]

        # print(value_matrix)
        Items=[]
        Collection = []
        for seller in self.Sellers:
            for i in range(1, self.seller_capacities[seller] + 1):
                Items.append([str(seller) , str(i)])
                Collection.append(str(seller) + ":"+ str(i))

        # print(str(Collection))
        reser_prices = {}
        valuations = {}
        for client in self.Clients:
            for item in Items:
                # print(value_matrix[item[0]][client])
                valuations[client, item[0] + ':'+ item[1]] = value_matrix[item[0]][client]
                reser_prices[item[0] + ':'+ item[1]] = self.seller_reserve_prices[item[0]]
                # print('{ '+ str(client) + " , " + str(item) +' }')
        # print(valuations)
        # print(reser_prices)
        # print(self.Clients)

        auction = Auction.Auction(Collection, reser_prices, self.Clients, valuations)
        t1 = time.time()
        auction.solve()
        t2 = time.time()
        r = auction.return_assignment()

        # auction.print_assignments()
        # auction.verify()

        # print("------------------------------------")
        # print('VDA Running...')
        # print('Number of Clients: ' + str(len(self.Clients)))
        # print('Number of Sellers: ' + str(len(self.Sellers)))
        # print('Total capacity: ' + str(tot_cap))
        # print('Seller capacities: ' + str(seller_cap))
        # print('Items: ' + str(Collection))
        # print('Bidders: ' + str(self.Clients))
        # print('Seller reserve prices: ' + str(reser_prices))
        # print("Solution: " + str(r))
        # print("Runtime: " + str(t2 - t1) + " seconds")
        return str(t2 - t1)

    # TODO: add vda with one alloc per user
    def vda_single_alloc_per_user(self):
        print("s")

    def vcg(self):
        print("vcg")

    def main(self):
        print('s')


if __name__ == '__main__':
    sys.setrecursionlimit(1500)

    # environment = Setup(1000, 100, 5, 1)
    environment = Setup(10, 10, 1, 1)
    x = environment.generate_for_hr()
    environment.hr_matching(x[0], x[1])
    # environment.vickery(x[2])
    # environment.baseline_allocation()
    # environment.baseline_allocation_with_capacity()
    # environment.hr_matching_no_cap(x[0], x[1])
    environment.vda(x[2])
