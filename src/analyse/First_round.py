import pandas as pd
import os


class First_round_analyse:
    file = "src/res/election/firstround.xlsx"
    ideologiesOfCandidatesFile = "src/res/election/canditats_ideologies.json"

    removeColumns = [
        "Code de la commune",
        "Code du département",
        "Etat saisie",
        "Unnamed: 27",
        "Sexe",
        "Unnamed: 26",
        "Unnamed: 27",
        "Unnamed: 33",
        "Unnamed: 34",
        "Unnamed: 40",
        "Unnamed: 41",
        "Unnamed: 47",
        "Unnamed: 48",
        "Unnamed: 54",
        "Unnamed: 55",
        "Unnamed: 61",
        "Unnamed: 62",
        "Unnamed: 68",
        "Unnamed: 69",
        "Unnamed: 75",
        "Unnamed: 76",
        "Unnamed: 82",
        "Unnamed: 83",
        "Unnamed: 89",
        "Unnamed: 90",
        "Unnamed: 96",
        "Unnamed: 97",
        "Nom",
        "Prénom",
        "N°Panneau",
        "Unnamed: 50",
        "Unnamed: 28",
        "Unnamed: 29",
        "Unnamed: 35",
        "Unnamed: 36",
        "Unnamed: 42",
        "Unnamed: 43",
        "Unnamed: 49",
        "Unnamed: 56",
        "Unnamed: 57",
        "Unnamed: 63",
        "Unnamed: 64",
        "Unnamed: 70",
        "Unnamed: 71",
        "Unnamed: 77",
        "Unnamed: 78",
        "Unnamed: 84",
        "Unnamed: 85",
        "Unnamed: 91",
        "Unnamed: 92",
        "Unnamed: 98",
        "Unnamed: 99",
    ]

    renameColumns = {
        "Libellé de la commune": "commune",
        "Libellé du département": "department",
        "Voix": "Voix Nathalie Arthaud",
        "% Voix/Ins": "Voix/ins Nathalie Arthaud",
        "% Voix/Exp": "Voix/exp Nathalie Arthaud",
        "Unnamed: 30": "Voix Fabien Roussel",
        "Unnamed: 31": "Voix/Ins Fabien Roussel",
        "Unnamed: 32": "Voix/Exp Fabien Roussel",
        "Unnamed: 37": "Voix Emmanuel Macron",
        "Unnamed: 38": "Voix/Ins Emmanuel Macron",
        "Unnamed: 39": "Voix/Exp Emmanuel Macron",
        "Unnamed: 44": "Voix Jean Lassalle",
        "Unnamed: 45": "Voix/Ins Jean Lassalle",
        "Unnamed: 46": "Voix/Exp Jean Lassalle",
        "Unnamed: 51": "Voix Marine Le Pen",
        "Unnamed: 52": "Voix/Ins Marine Le Pen",
        "Unnamed: 53": "Voix/Exp Marine Le Pen",
        "Unnamed: 58": "Voix Eric Zemmour",
        "Unnamed: 59": "Voix/Ins Eric Zemmour",
        "Unnamed: 60": "Voix/Exp Eric Zemmour",
        "Unnamed: 65": "Voix Jean-Luc Mélenchon",
        "Unnamed: 66": "Voix/Ins Jean-Luc Mélenchon",
        "Unnamed: 67": "Voix/Exp Jean-Luc Mélenchon",
        "Unnamed: 72": "Voix Anne Hidalgo",
        "Unnamed: 73": "Voix/Ins Anne Hidalgo",
        "Unnamed: 74": "Voix/Exp Anne Hidalgo",
        "Unnamed: 79": "Voix Yannick Jadot",
        "Unnamed: 80": "Voix/Ins Yannick Jadot",
        "Unnamed: 81": "Voix/Exp Yannick Jadot",
        "Unnamed: 86": "Voix Valérie Pécresse",
        "Unnamed: 87": "Voix/Ins Valérie Pécresse",
        "Unnamed: 88": "Voix/Exp Valérie Pécresse",
        "Unnamed: 93": "Voix Philippe Poutou",
        "Unnamed: 94": "Voix/Ins Philippe Poutou",
        "Unnamed: 95": "Voix/Exp Philippe Poutou",
        "Unnamed: 100": "Voix Nicolas Dupont-Aignan",
        "Unnamed: 101": "Voix/Ins Nicolas Dupont-Aignan",
        "Unnamed: 102": "Voix/Exp Nicolas Dupont-Aignan",
    }

    def __init__(self):
        self.df = pd.read_excel(self.file)
        self.df = self.df.drop(columns=self.removeColumns)
        self.df = self.df.dropna(axis=0, how="all")
        self.df = self.df.rename(columns=self.renameColumns)
        ideologies = pd.read_json(self.ideologiesOfCandidatesFile)
        for index, row in ideologies.iterrows():
            self.df["ideologies " + row["candidat"]] = row["ideologies"]

    def get_data(self):
        return self.df

    def create_csv(self):
        if not os.path.exists("src/res/generate"):
            os.makedirs("src/res/generate")
            self.df.to_csv("src/res/generate/firstround_worked.csv", index=False)
        else:
            if not os.path.exists("src/res/generate/firstround_worked.csv"):
                self.df.to_csv("src/res/generate/firstround_worked.csv", index=False)
            else:
                self.df.to_csv("src/res/generate/firstround_worked.csv", index=False)

    def filter_by_department(self, department="Rhône"):
        return self.df[self.df["department"] == department]

    def get_communes_only_by_department(self, department="Rhône"):
        return self.filter_by_department(department)["commune"]

    def qui_a_gagne_id(self, department="Rhône"):
        c = self.filter_by_department(department)
        candidats_columns = [
            "Voix Emmanuel Macron",
            "Voix Marine Le Pen",
            "Voix Jean-Luc Mélenchon",
            "Voix Jean Lassalle",
            "Voix Fabien Roussel",
            "Voix Nathalie Arthaud",
            "Voix Eric Zemmour",
            "Voix Anne Hidalgo",
            "Voix Yannick Jadot",
            "Voix Valérie Pécresse",
            "Voix Philippe Poutou",
            "Voix Nicolas Dupont-Aignan",
        ]
        c.loc[:, "vainqueur_id"] = (
            c[candidats_columns]
            .idxmax(axis=1)
            .apply(lambda x: candidats_columns.index(x))
        )

        return c
