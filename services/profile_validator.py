import csv
import os
import json
import pandas as pd
import numpy as np

my_json = {
    "id": 22,
    "name": "milliat",
    "validated": 0,
    "surname": "mickael",
    "encodings": [-0.07509941,  0.09966819,  0.07738455, -0.09642928, -0.18945418,
        0.01215649, -0.02239991, -0.05916007,  0.21017282, -0.01903518,
        0.26672804,  0.03510177, -0.24539176,  0.04913574, -0.04691654,
        0.08022714, -0.12994431, -0.05488232, -0.08392768, -0.11044858,
        0.03674962,  0.10395939, -0.02759009, -0.00555113, -0.10092813,
       -0.37627861, -0.07315867, -0.02385227,  0.07160784, -0.12873805,
        0.0710662 ,  0.10401089, -0.11698695, -0.10150075,  0.06381802,
        0.0614795 , -0.03336444, -0.05638632,  0.14039497,  0.0771363 ,
       -0.11008338,  0.07202417,  0.04400693,  0.35079047,  0.14478807,
        0.06070555,  0.06939472, -0.05129296,  0.10653394, -0.32869241,
        0.11267324,  0.09945321,  0.12838605,  0.02314223,  0.14007574,
       -0.13222076, -0.04644953,  0.1285325 , -0.21347778,  0.18600166,
        0.14856228, -0.06232495, -0.06187056, -0.13201049,  0.20051761,
        0.11778794, -0.15525225, -0.07574394,  0.08729832, -0.12434323,
       -0.11205506,  0.00893894, -0.10380301, -0.15796264, -0.26634046,
        0.12470496,  0.44940594,  0.16090104, -0.22247496, -0.04062485,
       -0.03691912,  0.0350282 ,  0.04650059,  0.03413529, -0.06712194,
       -0.06547642, -0.05934014,  0.0218011 ,  0.20528705,  0.01993666,
       -0.07787866,  0.30743089,  0.02098749,  0.04008951,  0.02034467,
        0.08375082, -0.09949448, -0.07018872, -0.11354105, -0.00857642,
        0.03814591, -0.11354536,  0.01025195,  0.09257237, -0.20284757,
        0.21102493, -0.044951  ,  0.00577252,  0.04196067,  0.0200013 ,
       -0.09998182, -0.0169097 ,  0.20915614, -0.29209873,  0.20520115,
        0.19811693,  0.05810759,  0.15649098,  0.03360184,  0.01021523,
        0.06057822,  0.00485518, -0.05300514, -0.1390626 , -0.0289612 ,
       -0.07420611, -0.01771721,  0.04625626],
    "dob": "19/02/1987",
    "val_num": 0
}

ROOT_DIR = os.path.abspath(os.curdir)
DATA_FILE_PATH = ROOT_DIR + '/data/known_face_encodings.json'


class ProfileJSONHandler:

    def __init__(self):
        with open(DATA_FILE_PATH) as f:
            self.data = pd.DataFrame(json.load(f)).T[["id", "account_id","name", "surname", "dob", "val_num", "validated", "encodings"]]


    def add_line(self, dt):
        # dt = json => np array (dumps json, make it a DataFrame, transpose, set the index to be id and order column
        print(self.data)
        # df = pd.read_json(my_json, orient="index").T.set_index("id")
        # df = df[["name", "surname", "dob", "val_num", "validated", "encodings"]]

        # df = pd.read_json(my_json, orient="index").T.set_index("id")
        # df = df[["name", "surname", "dob", "val_num", "validated", "encodings"]]

        # # check if data exists
        # if (df.index in list(self.data['id'])) or (df['name'].values[0] in list(self.data['name']) and df['surname'].values[0] in list(self.data['surname'])):
        #     return
        # else:
        #     # then add a line
        #     df.to_csv(DATA_FILE_PATH, sep=',', mode='a', header=False)
        # return self.get_updated_data()

    def remove_line(self, idx):
        d = self.data.set_index("id")
        d = d.drop(index=idx)
        d.to_csv(DATA_FILE_PATH, sep=',')
        return self.get_updated_data()

    def update_line(self, idx, updated_data):
        data = self.data.set_index("id")
        for k,v in updated_data.items():
            if k in ["name", "surname", "dob", "val_num", "validated", "encodings"]:
                data.at[idx, k] = v
        data.to_csv(DATA_FILE_PATH, sep=',')
        return self.get_updated_data()

    def get_updated_data(self):
        self.data = pd.read_csv(DATA_FILE_PATH)
        print(self.data)
        return self.data

pr = ProfileJSONHandler()
pr.add_line(my_json)

class ProfileValidator:

    def __init__(self, data):
        self.data = data
        self.known_face_data = ProfileJSONHandler()
        self.name = "unknown"


