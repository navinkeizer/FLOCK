import time
import pandas as pd
import numpy as np
from collections import Counter
from copy import copy
import random as rnd


def createNodes(i, j):
    clientData = [[1 for x in range(i)] for y in range(j)]
    relayData = [[1 for x in range(j)] for y in range(i)]

    for k in range(j):
        availableC = list(range(1,i+1))
        for z in range(i):
            rc = rnd.choice(availableC)
            clientData[k][z] = rc
            # remove from available
            availableC.remove(rc)


    clients = pd.DataFrame(clientData, index=range(j), columns=range(i))
    # print("clients: ")
    # print(clients)


    for q in range(i):
        availableR = list(range(1, j + 1))
        for p in range(j):
            rr = rnd.choice(availableR)
            relayData[q][p] = rr
            # remove from available
            availableR.remove(rr)


    workers = pd.DataFrame(relayData, index=range(i), columns=range(j))
    # print("workers: ")
    # print(workers)

    return [clients, workers]



client_df, worker_df = createNodes(4,4)
client_list = ['a', 'b', 'c', 'd']
worker_list = ['A', 'B', 'C', 'D']

client_df.columns = client_list
client_df.index = worker_list

worker_df.columns = client_list
worker_df.index = worker_list

print("clients: ")
print(client_df)
print("workers: ")
print(worker_df)


man_list = client_list
man_df = client_df
women_list = worker_list
women_df = worker_df


# man_list = ['a', 'b', 'c', 'd']
# women_list = ['A', 'B', 'C', 'D']
# women_df = pd.DataFrame({'A': [3,4,2,1], 'B': [3,1,4,2], 'C':[2,3,4,1], 'D':[3,2,1,4]})
# women_df.index = man_list
# man_df = pd.DataFrame({'A': [1,1,2,4], 'B': [2,4,1,2], 'C':[3,3,3,3], 'D':[4,2,4,1]})
# man_df.index = man_list


# dict to control which women each man can make proposals
women_available = {man:women_list for man in man_list}
# waiting list of men that were able to create pair on each iteration
waiting_list = []
# dict to store created pairs
proposals = {}
# variable to count number of iterations
count = 0


# while not all men have pairs
while len(waiting_list)<len(man_list):
    # man makes proposals
    for man in man_list:
        if man not in waiting_list:
            # each man make proposal to the top women from it's list
            women = women_available[man]
            best_choice = man_df.loc[man][man_df.loc[man].index.isin(women)].idxmin()
            proposals[(man, best_choice)]=(man_df.loc[man][best_choice],
                                                 women_df.loc[man][best_choice])
    # if women have more than one proposals
    # she will choose the best option
    overlays = Counter([key[1] for key in proposals.keys()])
    # cycle to choose the best options
    for women in overlays.keys():
        if overlays[women]>1:
            # pairs to drop from proposals
            pairs_to_drop = sorted({pair: proposals[pair] for pair in proposals.keys()
                    if women in pair}.items(),
                   key=lambda x: x[1][1]
                  )[1:]
            # if man was rejected by woman
            # there is no pint for him to make proposal
            # second time to the same woman
            for p_to_drop in pairs_to_drop:
                del proposals[p_to_drop[0]]
                _women = copy(women_available[p_to_drop[0][0]])
                _women.remove(p_to_drop[0][1])
                women_available[p_to_drop[0][0]] = _women
    # man who successfully created pairs must be added to the waiting list
    waiting_list = [man[0] for man in proposals.keys()]
    # update counter
    count+=1

print(women_df)
print(man_df)
print(proposals)
print(count)


# # dict to control which workers each client can make proposals
# workers_available = {client:worker_list for client in client_list}
# # waiting list of clients that were able to create pair on each iteration
# waiting_list = []
# # dict to store created pairs
# proposals = {}
# # variable to count number of iterations
# count = 0
#




# t1 = time.time()
# while len(waiting_list)<len(client_list):
#     # client makes proposals
#     for client in client_list:
#         if client not in waiting_list:
#             # each client make proposal to the top workers from it's list
#             worker = workers_available[client]
#             best_choice = client_df.loc[client][client_df.loc[client].index.isin(worker)].idxmin()
#             proposals[(client, best_choice)]=(client_df.loc[client][best_choice],worker_df.loc[client][best_choice])
#
#     # if workers have more than one proposals
#     # they will choose the best option
#     overlays = Counter([key[1] for key in proposals.keys()])
#     # cycle to choose the best options
#     for worker in overlays.keys():
#         if overlays[worker]>1:
#             # pairs to drop from proposals
#             pairs_to_drop = sorted({pair: proposals[pair] for pair in proposals.keys()
#                     if worker in pair}.items(),
#                    key=lambda x: x[1][1]
#                   )[1:]
#
#             # if man was rejected by woman
#             # there is no pint for him to make proposal
#             # second time to the same woman
#             for p_to_drop in pairs_to_drop:
#                 del proposals[p_to_drop[0]]
#                 _worker = copy(workers_available[p_to_drop[0][0]])
#                 _worker.remove(p_to_drop[0][1])
#                 workers_available[p_to_drop[0][0]] = _worker
#     # client who successfully created pairs must be added to the waiting list
#     waiting_list = [client[0] for client in proposals.keys()]
#     # update counter
#     count+=1
#
#
#
# t2 = time.time()
# print("Stable Matching")
# print("Clients: " + str(len(man_list)))
# print("Workers: " + str(len(women_list)))
# print("Time: " + str(t2-t1) + " seconds")
# print("Matching: " + str(proposals))