import Algorithm.Setup as setup
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt

class Analyses:

    # constant seller/client numbers
    # HR matching with multiple capacities
    def HR_vary_preferencelist(self, n_clients, n_sellers, cap_max):
        with open('HR_Vary_Pref.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Number of Clients', 'Number of Sellers','Maximum Capaciy', 'Run', 'Preference Length', 'Run Time'])
            for run in range(0, 3, 1):
                for n in range(2, 102, 10):
                    print("------------------------------------")
                    print("Run: " + str(run))
                    print("Preference amount: " + str(n))
                    environment = setup.Setup(n_clients, n_sellers, n, max_capacity=cap_max)
                    x = environment.generate_for_hr()
                    results = environment.hr_matching(x[0], x[1])
                    writer.writerow([n_clients, n_sellers, cap_max, run, n, results[0]])

        # data = np.genfromtxt("HR_Vary_Pref.csv", delimiter=",", names=['NumberofClients', 'NumberofSellers','MaximumCapaciy', 'Run', 'PreferenceLength', 'RunTime'])
        # plt.plot(data['PreferenceLength'], data['RunTime'])

    def compare_algorithms(self, n_sellers, pref_length):

        with open('compare_single_item.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Number of Clients', 'Number of Sellers', 'Run', 'Preference Length', 'Run Time HR', 'Run Time Vickery', 'Run Time Optimal'])
            for run in range(0, 4, 1):
                for client_n in range (1000, 10000, 1000):
                    print("------------------------------------")
                    print("Run: " + str(run))
                    print("Client number: " + str(client_n))
                    environment = setup.Setup(client_n, n_sellers, pref_length)
                    x = environment.generate_for_hr()
                    hr = environment.hr_matching_no_cap(x[0], x[1])
                    optimal = environment.baseline_allocation()
                    vickery = environment.vickery(x[2])
                    writer.writerow([client_n, n_sellers, run, pref_length, hr, vickery, optimal])

    def compare_algorithms_mutli(self, n_sellers, cap_max, pref_length):

        with open('compare_multi_item.csv', 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['Number of Clients', 'Number of Sellers', 'Run', 'Preference Length', 'Run Time HR','Run Time VDA', 'Run Time Optimal'])
            for run in range(0, 5, 1):
                for client_n in range (1000, 10000, 1000):
                    print("------------------------------------")
                    print("Run: " + str(run))
                    print("Client number: " + str(client_n))
                    environment = setup.Setup(client_n, n_sellers, pref_length,  max_capacity=cap_max)
                    x = environment.generate_for_hr()
                    hr = environment.hr_matching(x[0], x[1])
                    optimal = environment.baseline_allocation_with_capacity()
                    vda = environment.vda(x[2])
                    writer.writerow([client_n, n_sellers, run, pref_length, hr[0], vda, optimal])

    def main(self):
        sys.setrecursionlimit(1500)
        # self.HR_vary_preferencelist(500,100,3)
        # self.compare_algorithms(100,5)
        self.compare_algorithms_mutli(100,3,5)

if __name__ == '__main__':
    Analyses().main()