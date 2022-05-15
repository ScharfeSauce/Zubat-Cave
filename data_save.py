import json
from settings import Settings

def save_state(name, score):

    entry = {"Player Name" : name, "Score" : score}

    with open(Settings.path_data, 'r')as list:
        python_liste = json.load(list)
        python_liste.append(entry)
        print(python_liste)
        with open(Settings.path_data, 'w') as input:
            json.dump(python_liste, input, indent = 4)

def rank():
    with open(Settings.path_data, 'r')as best:
        best_list = []
        list = json.load(best)
        for x in range(0, len(list)):
            best_list.append([list[x]["Score"], list[x]["Player Name"]])
        return sorted(best_list, reverse=True)

#print(rank()[0][0])