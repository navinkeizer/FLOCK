from matching.games import HospitalResident
import yaml
import time
from matching import Player


with open(r'residents.yml') as file:
    resident_preferences = yaml.full_load(file)
with open(r'capacities.yml') as file:
    hospital_capacities = yaml.full_load(file)
    with open(r'hospitals.yml') as file:
        hospital_preferences = yaml.full_load(file)
print(len(resident_preferences), len(hospital_preferences), sum(hospital_capacities.values()))

print(resident_preferences)
print(hospital_capacities)
print(hospital_preferences)

t1 = time.time()

game = HospitalResident.create_from_dictionaries(
    resident_preferences, hospital_preferences, hospital_capacities
)

matching = game.solve(optimal="resident")
t2 = time.time()
print("Time: " + str(t2-t1) + " seconds")

print(matching)

print(game.check_stability(), game.check_validity())


# suitors = [
#     Player(name="Bingley"),
#     Player(name="Collins"),
#     Player(name="Darcy"),
#     Player(name="Wickham"),
# ]
#
# reviewers = [
#     Player(name="Charlotte"),
#     Player(name="Elizabeth"),
#     Player(name="Jane"),
#     Player(name="Lydia"),
# ]
#
# bingley, collins, darcy, wickham = suitors
# charlotte, elizabeth, jane, lydia = reviewers
#
# bingley.set_prefs([jane, elizabeth, lydia, charlotte])
# collins.set_prefs([jane, elizabeth, lydia, charlotte])
# darcy.set_prefs([elizabeth, jane, charlotte, lydia])
# wickham.set_prefs([lydia, jane, elizabeth, charlotte])
#
# charlotte.set_prefs([bingley, darcy, collins, wickham])
# elizabeth.set_prefs([wickham, darcy, bingley, collins])
# jane.set_prefs([bingley, wickham, darcy, collins])
# lydia.set_prefs([bingley, wickham, darcy, collins])
#
# print(suitors)