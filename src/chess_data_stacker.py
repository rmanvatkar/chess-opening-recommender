import pandas as pd

files = ["a", "b", "c", "d", "e"]
frames = [pd.read_csv(f"data/{f}.tsv", sep="\t") for f in files]
openings = pd.concat(frames, ignore_index=True)

print(openings.shape)
print(openings.head())

openings["family"] = openings["name"].str.split(":").str[0]

print(openings.shape)
print(openings["family"].nunique())
print(openings["family"].value_counts().head(20))

main = (
    openings.sort_values("pgn", key=lambda s: s.str.len())
    .drop_duplicates("family")
    .sort_values("eco")
    .reset_index(drop=True)
)

print(main.shape)
print(main["family"].tolist())

main.to_csv("data/openings_main.csv", index=False)

keep = [
    # As White
    "Italian Game", "Ruy Lopez", "Scotch Game", "King's Gambit", "Vienna Game",
    "Four Knights Game", "Three Knights Opening", "Bishop's Opening",
    "Danish Gambit", "Center Game", "Ponziani Opening", "London System",
    "Colle System", "Torre Attack", "Trompowsky Attack", "Queen's Gambit",
    "Catalan Opening", "English Opening", "Réti Opening", "King's Indian Attack",
    "Bird Opening", "Blackmar-Diemer Gambit", "Richter-Veresov Attack",
    "Nimzo-Larsen Attack", "Zukertort Opening",
    # As Black
    "Sicilian Defense", "French Defense", "Caro-Kann Defense",
    "Scandinavian Defense", "Alekhine Defense", "Pirc Defense", "Modern Defense",
    "Philidor Defense", "Petrov's Defense", "Slav Defense", "Semi-Slav Defense",
    "Queen's Gambit Declined", "Queen's Gambit Accepted", "King's Indian Defense",
    "Nimzo-Indian Defense", "Queen's Indian Defense", "Grünfeld Defense",
    "Dutch Defense", "Benoni Defense", "Benko Gambit", "Tarrasch Defense",
    "Bogo-Indian Defense", "Englund Gambit", "Latvian Gambit",
    "Nimzowitsch Defense", "English Defense", "Old Indian Defense",
    "Elephant Gambit",
]

missing = set(keep) - set(main["family"])
print("Not found:", missing)

shortlist = main[main["family"].isin(keep)].reset_index(drop=True)
print(shortlist.shape)

shortlist.to_csv("data/openings_shortlist.csv", index=False)