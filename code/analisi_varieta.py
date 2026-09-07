import os
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = os.path.join("data", "dataset_completo.csv")
RESULTS_DIR = "results"
os.makedirs(RESULTS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)

required_columns = ["ID", "Tema", "Livello", "Generazione", "Output"]
missing = [col for col in required_columns if col not in df.columns]
if missing:
    raise ValueError(f"Colonne mancanti nel dataset: {missing}")

# Rappresentazione TF-IDF dei testi
vectorizer = TfidfVectorizer(
    lowercase=True,
    strip_accents="unicode",
    ngram_range=(1, 2),
    token_pattern=r"(?u)\b\w+\b"
)
tfidf = vectorizer.fit_transform(df["Output"].fillna(""))

# Matrice delle similarità coseno
similarities = cosine_similarity(tfidf)

pair_rows = []
condition_rows = []

# Per ogni condizione: 5 testi -> 10 confronti a coppie
for (tema, livello), group in df.groupby(["Tema", "Livello"], sort=True):
    indices = group.index.tolist()
    pair_values = []

    for i in range(len(indices)):
        for j in range(i + 1, len(indices)):
            idx_i, idx_j = indices[i], indices[j]
            sim = similarities[idx_i, idx_j]
            pair_values.append(sim)

            pair_rows.append({
                "Tema": tema,
                "Livello": livello,
                "ID_1": df.loc[idx_i, "ID"],
                "ID_2": df.loc[idx_j, "ID"],
                "Similarita_coseno": sim
            })

    mean_similarity = sum(pair_values) / len(pair_values)
    variety = 1 - mean_similarity

    condition_rows.append({
        "Tema": tema,
        "Livello": livello,
        "Similarita_media": mean_similarity,
        "Varieta": variety
    })

pairs_df = pd.DataFrame(pair_rows)
conditions_df = pd.DataFrame(condition_rows)

pairs_df.to_csv(os.path.join(RESULTS_DIR, "similarita_coppie.csv"), index=False)
conditions_df.to_csv(
    os.path.join(RESULTS_DIR, "risultati_varieta_per_condizione.csv"),
    index=False
)

summary = (
    conditions_df.groupby("Livello", sort=True)["Varieta"]
    .mean()
    .reset_index()
)
summary.to_csv(os.path.join(RESULTS_DIR, "riepilogo_varieta.csv"), index=False)

# Grafico A-B-C
plt.figure(figsize=(7, 5))
plt.plot(summary["Livello"], summary["Varieta"], marker="o")
plt.xlabel("Livello di specificità")
plt.ylabel("Varietà media")
plt.title("Varietà media degli output per livello di specificità")
plt.tight_layout()
plt.savefig(
    os.path.join(RESULTS_DIR, "grafico_varieta_media_ABC.png"),
    dpi=150
)
plt.close()

# Grafico per tema
pivot = conditions_df.pivot(
    index="Tema", columns="Livello", values="Varieta"
)
pivot.plot(kind="bar", figsize=(8, 5))
plt.xlabel("Tema")
plt.ylabel("Varietà")
plt.title("Varietà per tema e livello di specificità")
plt.tight_layout()
plt.savefig(
    os.path.join(RESULTS_DIR, "grafico_varieta_per_tema.png"),
    dpi=150
)
plt.close()

print("Analisi completata.")
print(summary)
