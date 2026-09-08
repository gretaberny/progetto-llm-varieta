from pathlib import Path
from itertools import combinations
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "dataset_completo.csv"
RESULTS = ROOT / "results"
RESULTS.mkdir(exist_ok=True)

# 1. Caricamento e controlli di base
df = pd.read_csv(DATA)
required = {"tema", "livello", "generazione", "prompt", "testo"}
missing = required - set(df.columns)
if missing:
    raise ValueError(f"Colonne mancanti: {sorted(missing)}")
if len(df) != 45:
    raise ValueError(f"Attesi 45 testi, trovati {len(df)}")

# 2. TF-IDF con unigrammi e bigrammi
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf = vectorizer.fit_transform(df["testo"].fillna(""))
sim_matrix = cosine_similarity(tfidf)

# 3. Similarità a coppie e varietà per condizione
pair_rows = []
condition_rows = []

for tema in ["Mistero", "Viaggio", "Sogno"]:
    for livello in ["A", "B", "C"]:
        indices = df.index[(df["tema"] == tema) & (df["livello"] == livello)].tolist()
        if len(indices) != 5:
            raise ValueError(f"La condizione {tema}-{livello} non contiene 5 testi.")

        values = []
        for i, j in combinations(indices, 2):
            value = float(sim_matrix[i, j])
            values.append(value)
            pair_rows.append({
                "tema": tema,
                "livello": livello,
                "generazione_1": int(df.loc[i, "generazione"]),
                "generazione_2": int(df.loc[j, "generazione"]),
                "similarita": value,
            })

        mean_similarity = sum(values) / len(values)
        condition_rows.append({
            "tema": tema,
            "livello": livello,
            "similarita_media": mean_similarity,
            "varieta": 1 - mean_similarity,
        })

condition_df = pd.DataFrame(condition_rows)
summary_df = (
    condition_df.groupby("livello", sort=False)
    .agg(
        similarita_media=("similarita_media", "mean"),
        varieta_media=("varieta", "mean"),
    )
    .reset_index()
)
summary_df["livello"] = pd.Categorical(summary_df["livello"], ["A", "B", "C"], ordered=True)
summary_df = summary_df.sort_values("livello")

# 4. Salvataggio risultati
condition_df.to_csv(RESULTS / "risultati_varieta_per_condizione.csv", index=False)
summary_df.to_csv(RESULTS / "riepilogo_varieta.csv", index=False)
pd.DataFrame(pair_rows).to_csv(RESULTS / "similarita_coppie.csv", index=False)

# 5. Grafico A-B-C
plt.figure(figsize=(7, 5))
plt.bar(["A\nBassa", "B\nMedia", "C\nAlta"], summary_df["varieta_media"])
plt.ylabel("Varietà media")
plt.xlabel("Specificità del prompt")
plt.title("Varietà media degli output per livello di specificità")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(RESULTS / "grafico_varieta_media_ABC.png", dpi=300, bbox_inches="tight")
plt.close()

# 6. Grafico per tema
pivot = condition_df.pivot(index="tema", columns="livello", values="varieta")[["A", "B", "C"]]
ax = pivot.plot(kind="bar", figsize=(8, 5))
ax.set_ylabel("Varietà")
ax.set_xlabel("Tema")
ax.set_title("Varietà degli output per tema e livello di specificità")
ax.set_ylim(0, 1)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
ax.legend(title="Livello")
fig = ax.get_figure()
fig.tight_layout()
fig.savefig(RESULTS / "grafico_varieta_per_tema.png", dpi=300, bbox_inches="tight")
plt.close(fig)

print("Analisi completata.")
print("\nVarietà media per livello:")
print(summary_df.to_string(index=False))
print("\nRisultati per condizione:")
print(condition_df.to_string(index=False))
