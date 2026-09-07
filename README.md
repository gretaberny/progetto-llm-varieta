# Progetto LLM e varietà degli output

## Domanda di ricerca

**Come cambia la varietà degli output di un LLM all'aumentare del livello di specificità del prompt?**

## Ipotesi

All'aumentare della specificità del prompt, la varietà degli output generati dal LLM tende a diminuire, perché un numero maggiore di vincoli limita le possibili modalità di risposta.

## Disegno dell'esperimento

Sono stati utilizzati tre temi narrativi: **Mistero, Viaggio e Sogno**.

Per ogni tema sono stati definiti tre livelli di specificità:
- **A** = bassa specificità
- **B** = media specificità
- **C** = alta specificità

Sono stati quindi utilizzati **9 prompt** complessivi. Ogni prompt è stato generato **5 volte**, per un totale di **45 output**.

## Misura della varietà

Per operazionalizzare la varietà sono state utilizzate le rappresentazioni **TF-IDF** dei testi e la **similarità coseno**.

Per ogni condizione sono stati confrontati a coppie i 5 testi prodotti, ottenendo 10 confronti per gruppo.

**Varietà = 1 − similarità media**

Quindi:
- similarità alta → varietà bassa
- similarità bassa → varietà alta

## Risultati principali

| Livello | Varietà media |
|---|---:|
| A | 0.767 |
| B | 0.696 |
| C | 0.458 |

La varietà diminuisce progressivamente passando dal livello A al livello C.

### Risultati per tema

| Tema | A | B | C |
|---|---:|---:|---:|
| Mistero | 0.847 | 0.691 | 0.452 |
| Viaggio | 0.744 | 0.699 | 0.479 |
| Sogno | 0.711 | 0.699 | 0.442 |

Il risultato è coerente con l'ipotesi: nel campione analizzato, prompt più specifici producono output mediamente più simili tra loro.

## Limiti

Questo è uno studio esplorativo basato su un campione di 45 testi e 5 generazioni per condizione.

La misura TF-IDF + similarità coseno è un'operazionalizzazione della varietà basata sulla rappresentazione dei testi e non coincide con una misura perfetta della similarità semantica.

Inoltre, passando da A a B e C cambiano contemporaneamente più caratteristiche del prompt (personaggi, ambientazione, tono, lunghezza e vincoli narrativi). L'esperimento misura quindi l'effetto complessivo dell'aumento della specificità, non l'effetto di un singolo vincolo isolato.

## Struttura del repository

```text
progetto-llm-varieta/
├── README.md
├── requirements.txt
├── data/
│   └── dataset_completo.csv
├── prompts/
│   └── prompts.txt
├── code/
│   └── analisi_varieta.py
└── results/
    ├── riepilogo_varieta.csv
    ├── risultati_varieta_per_condizione.csv
    ├── similarita_coppie.csv
    ├── grafico_varieta_media_ABC.png
    └── grafico_varieta_per_tema.png
```

## Come riprodurre l'analisi

1. Installare le librerie indicate in `requirements.txt`.
2. Assicurarsi che `data/dataset_completo.csv` sia presente.
3. Eseguire `code/analisi_varieta.py`.
4. I risultati vengono salvati nella cartella `results/`.

## Contenuto

Repository del progetto di **Tecnologie dei Dati e del Linguaggio**: contiene dati, prompt, codice di analisi e risultati dell'esperimento.
