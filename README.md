# Progetto LLM e varietà degli output

Progetto per il corso di **Tecnologie dei Dati e del Linguaggio**.

## 1. Domanda di ricerca

**Come cambia la varietà degli output di un LLM all'aumentare del livello di specificità del prompt?**

## 2. Ipotesi

**All'aumentare della specificità del prompt, la varietà degli output generati dal LLM tende a diminuire, perché un numero maggiore di vincoli limita le possibili modalità di risposta.**

## 3. Disegno dell'esperimento

Sono stati scelti tre temi narrativi: **Mistero, Viaggio e Sogno**.

Per ogni tema sono stati definiti tre livelli di specificità:

- **A** = bassa specificità
- **B** = media specificità
- **C** = alta specificità

Sono quindi presenti **9 prompt**. Ogni prompt è stato usato per **5 generazioni**, ottenendo **45 testi complessivi**.

La generazione è stata effettuata automaticamente con **Qwen/Qwen2.5-0.5B-Instruct** in Google Colab, utilizzando una GPU T4. I parametri principali sono stati `temperature=0.8`, `top_p=0.95` e `max_new_tokens=700`.

## 4. Misura della varietà

La varietà viene operazionalizzata attraverso la distanza tra gli output testuali.

1. I testi vengono trasformati in vettori **TF-IDF**, usando unigrammi e bigrammi (`ngram_range=(1, 2)`).
2. Si calcola la **similarità coseno** tra i testi.
3. Per ogni condizione (tema × livello) vengono confrontate tutte le coppie dei 5 output: sono **10 confronti** per condizione.
4. Si calcola la similarità media.
5. La varietà viene definita come:

**Varietà = 1 − similarità media**

Di conseguenza, una similarità maggiore corrisponde a una varietà minore.

## 5. Risultati

### Varietà media per livello

| Livello | Varietà media |
|---|---:|
| A – bassa | 0.934 |
| B – media | 0.876 |
| C – alta | 0.773 |

La varietà diminuisce progressivamente passando da A a B e da B a C.

### Risultati per tema

| Tema | A | B | C |
|---|---:|---:|---:|
| Mistero | 0.931 | 0.864 | 0.786 |
| Viaggio | 0.925 | 0.863 | 0.801 |
| Sogno | 0.948 | 0.900 | 0.730 |

La stessa tendenza A > B > C è presente in tutti e tre i temi.

## 6. Interpretazione

Nel campione analizzato, l'aumento della specificità del prompt è associato a una diminuzione della varietà degli output. Il risultato è quindi **coerente con l'ipotesi di ricerca**.

La differenza tra la varietà media del livello A e quella del livello C è di circa 0.162 punti, corrispondente a una diminuzione relativa di circa il 17% rispetto ad A.

Il risultato va interpretato come evidenza **esplorativa**: non permette di generalizzare il comportamento a tutti gli LLM, perché l'esperimento utilizza un solo modello e un campione di 45 testi.

## 7. Limiti

- Il campione è relativamente piccolo: 45 testi e 5 generazioni per condizione.
- È stato utilizzato un solo modello, Qwen2.5-0.5B-Instruct.
- TF-IDF + similarità coseno misura la somiglianza sulla base della rappresentazione lessicale e non cattura perfettamente la similarità semantica.
- Aumentando la specificità da A a B e C cambiano contemporaneamente più caratteristiche del prompt (personaggi, ambientazione, tono, lunghezza e vincoli). L'esperimento misura quindi l'effetto complessivo dell'aumento della specificità e non l'effetto isolato di un singolo vincolo.
- Non vengono formulate conclusioni di significatività statistica, dato il carattere esplorativo e la dimensione del campione.

## 8. Struttura del repository

```text
progetto-llm-varieta/
├── README.md
├── requirements.txt
├── data/
│   └── dataset_completo.csv
├── prompts/
│   └── prompts.txt
├── code/
│   ├── generazione_qwen.py
│   └── analisi_varieta.py
└── results/
    ├── riepilogo_varieta.csv
    ├── risultati_varieta_per_condizione.csv
    ├── similarita_coppie.csv
    ├── grafico_varieta_media_ABC.png
    └── grafico_varieta_per_tema.png
```

## 9. Riproduzione

### Analisi

Dopo aver installato le dipendenze:

```bash
pip install -r requirements.txt
python code/analisi_varieta.py
```

L'analisi legge `data/dataset_completo.csv` e rigenera i tre CSV e i due grafici nella cartella `results/`.

### Generazione

La generazione automatica è documentata in `code/generazione_qwen.py`. Lo script utilizza il modello `Qwen/Qwen2.5-0.5B-Instruct` e richiede `transformers`, `accelerate`, `torch` e una risorsa di calcolo adeguata; per la generazione originale è stata usata Google Colab con GPU T4.

La generazione non richiede alcuna API key.

## 10. Conclusione

L'esperimento mostra una relazione coerente con l'ipotesi: **maggiore specificità del prompt → minore varietà media degli output** nel campione analizzato.

Il progetto non pretende di stabilire una legge generale sul comportamento degli LLM, ma mostra come una domanda sul comportamento di un modello possa essere trasformata in un esperimento riproducibile, con dati, metodologia, metrica quantitativa e risultati interpretabili.
