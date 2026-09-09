# Progetto LLM e varietà degli output

Progetto per il corso di **Tecnologie dei Dati e del Linguaggio**.

---

## 1. Obiettivo del progetto

Il progetto analizza come il livello di specificità di un prompt influenzi la varietà degli output generati da un Large Language Model (LLM).

L'idea è confrontare testi generati a partire da prompt con tre diversi livelli di specificità:

- **A – bassa specificità**
- **B – media specificità**
- **C – alta specificità**

L'obiettivo è verificare se l'aumento dei vincoli presenti nel prompt porti a una diminuzione della varietà degli output.


## 2. Domanda di ricerca

**Come cambia la varietà degli output di un LLM all'aumentare del livello di specificità del prompt?**


## 3. Ipotesi

**All'aumentare della specificità del prompt, la varietà degli output generati dal LLM tende a diminuire, perché un numero maggiore di vincoli limita le possibili modalità di risposta.**


## 4. Disegno sperimentale

Sono stati utilizzati tre temi narrativi:

- **Mistero**
- **Viaggio**
- **Sogno**

Per ciascun tema sono stati costruiti tre prompt con diverso livello di specificità:

- | A | Prompt generico, con pochi vincoli |
- | B | Prompt con un livello intermedio di specificità |
- | C | Prompt molto specifico, con numerosi vincoli |

Per ogni combinazione di tema e livello sono state generate **5 storie**.

Il dataset complessivo contiene quindi:

**3 temi × 3 livelli × 5 generazioni = 45 testi**

La scelta di 5 generazioni per condizione è stata adottata per mantenere l'esperimento gestibile e consentire comunque il confronto tra più output della stessa condizione.

## 5. Modello e generazione dei testi

Per la generazione automatica dei testi è stato utilizzato:

**Qwen/Qwen2.5-0.5B-Instruct**

Il modello è stato eseguito in **Google Colab** utilizzando una GPU **NVIDIA T4**.

La generazione è stata effettuata automaticamente a partire dai nove prompt presenti nella cartella `prompts/`.

Parametri principali utilizzati:

- `max_new_tokens = 700`
- `do_sample = True`
- `temperature = 0.8`
- `top_p = 0.95`

L'utilizzo di `do_sample=True` permette al modello di generare output differenti anche a partire dallo stesso prompt. `temperature` e `top_p` controllano il livello di variabilità del campionamento, mentre `max_new_tokens` limita la lunghezza massima dell'output.

La generazione è quindi stocastica: una nuova esecuzione può produrre testi diversi. Nel codice di riproduzione sono impostati dei seed per rendere la procedura più controllata, ma la riproduzione esatta dei testi può dipendere anche dall'hardware e dalle versioni delle librerie utilizzate.

I risultati riportati nel progetto sono calcolati sul dataset `data/dataset_completo.csv` incluso nel repository.

## 6. Misurazione della varietà

La varietà degli output è stata stimata utilizzando la **similarità coseno** tra rappresentazioni **TF-IDF** dei testi.

### TF-IDF

Ogni testo viene trasformato in un vettore numerico tramite:
Sono quindi considerati sia:

unigrammi, cioè singole parole;
bigrammi, cioè coppie consecutive di parole.

La rappresentazione TF-IDF permette di dare maggiore importanza alle parole caratteristiche dei singoli testi e minore importanza a quelle molto frequenti nell'intero corpus.

**Similarità coseno**

La similarità coseno misura quanto due vettori siano simili.

Nel caso considerato, valori più vicini a 1 indicano una maggiore somiglianza tra i testi, mentre valori più vicini a 0 indicano una minore somiglianza.

Per ogni condizione sperimentale sono presenti 5 testi.

I 5 testi generano:

5 × 4 / 2 = 10 confronti a coppie

Per ogni coppia viene calcolata la similarità coseno e successivamente viene calcolata la similarità media della condizione.

Complessivamente vengono quindi analizzati:

9 condizioni × 10 confronti = 90 confronti a coppie

La varietà viene definita come:

Varietà = 1 − similarità media

Di conseguenza:

similarità alta → varietà bassa;
similarità bassa → varietà alta.

## 7. Risultati

La varietà media ottenuta per i tre livelli di specificità è:

| Livello               | Similarità media | Varietà media |
| --------------------- | ---------------: | ------------: |
| A – bassa specificità |         0.065676 |  **0.934324** |
| B – media specificità |         0.124289 |  **0.875711** |
| C – alta specificità  |         0.227534 |  **0.772466** |


Si osserva una diminuzione progressiva della varietà:

A > B > C

La varietà passa da 0.934 per i prompt a bassa specificità a 0.772 per i prompt ad alta specificità.

La diminuzione assoluta è di circa 0.162, corrispondente a una riduzione relativa di circa 17% rispetto al livello A.

La stessa tendenza A > B > C è osservata anche considerando separatamente i tre temi.

## 8. Grafici

Varietà media per livello di specificità

<img width="2370" height="1466" alt="grafico_varieta_per_tema" src="https://github.com/user-attachments/assets/abdcfc91-a300-4161-9a9d-cbf07c79b566" />

Varietà per tema e livello di specificità

<img width="2370" height="1466" alt="grafico_varieta_per_tema" src="https://github.com/user-attachments/assets/231e1b4e-2ad6-4f1e-a067-79163bed6031" />


## 9. Interpretazione dei risultati

I risultati ottenuti sembrano coerenti con l'ipotesi di ricerca. All'aumentare della specificità del prompt, la similarità media tra gli output aumenta e, di conseguenza, la varietà diminuisce.

Questo suggerisce che l'introduzione di un numero maggiore di vincoli nel prompt possa restringere lo spazio delle possibili risposte del modello.

La tendenza è presente in tutti e tre i temi analizzati:

Mistero: la varietà diminuisce da 0.931 a 0.786;
Viaggio: la varietà diminuisce da 0.925 a 0.801;
Sogno: la varietà diminuisce da 0.948 a 0.730.

Il risultato più evidente si osserva nel tema Sogno, mentre il tema Viaggio presenta una diminuzione leggermente più contenuta. I risultati devono comunque essere interpretati come evidenza esplorativa e non come una dimostrazione generale del comportamento di tutti gli LLM.

## 10. Limiti dell'esperimento

L'esperimento presenta alcuni limiti.

**Dimensione del dataset**

Il dataset contiene 45 testi, con 5 generazioni per ciascuna condizione. Si tratta quindi di un campione relativamente piccolo. Per questo motivo i risultati non possono essere generalizzati a tutti i possibili prompt, modelli o condizioni di generazione.

**Misura della varietà**

La varietà viene misurata attraverso la similarità lessicale basata su TF-IDF e similarità coseno. Questa misura considera soprattutto la sovrapposizione delle caratteristiche testuali e non permette di valutare completamente aspetti più complessi della varietà, come:

- struttura narrativa;
- originalità delle idee;
- stile;
- significato semantico;
- sviluppo dei personaggi.

A causa della dimensione ridotta del campione, l'analisi è stata mantenuta descrittiva ed esplorativa.
Non vengono quindi formulate conclusioni sulla significatività statistica dei risultati.

## 11. Struttura del repository

progetto-llm-varieta/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   └── dataset_completo.csv
│
├── prompts/
│   └── prompts.txt
│
├── code/
│   ├── generazione_qwen.py
│   └── analisi_varieta.py
│
└── results/
    ├── riepilogo_varieta.csv
    ├── risultati_varieta_per_condizione.csv
    ├── similarita_coppie.csv
    ├── grafico_varieta_media_ABC.png
    └── grafico_varieta_per_tema.png

## 12. Riproduzione dell'analisi

L'analisi può essere riprodotta utilizzando lo script:

code/analisi_varieta.py

Lo script:

carica data/dataset_completo.csv;
controlla la struttura del dataset;
costruisce la rappresentazione TF-IDF;
calcola le similarità coseno;
calcola le 10 similarità a coppie per ogni condizione;
calcola la similarità media;
calcola la varietà;
salva i risultati in formato CSV;
genera i due grafici.

I risultati vengono salvati nella cartella results/.

La generazione automatica dei testi può invece essere eseguita tramite:

code/generazione_qwen.py

Questo script utilizza il modello Qwen/Qwen2.5-0.5B-Instruct, legge i prompt da prompts/prompts.txt e genera 5 testi per ciascuno dei 9 prompt.

## 13. Conclusione

L'esperimento mostra, nel campione analizzato, una relazione tra il livello di specificità dei prompt e la varietà degli output.
In particolare, passando da prompt generici a prompt più specifici, la similarità media tra i testi aumenta e la varietà diminuisce.

I risultati ottenuti sono quindi coerenti con l'ipotesi secondo cui una maggiore specificità del prompt restringa le possibili modalità di risposta del modello.

Data la dimensione limitata del dataset e i limiti della misura utilizzata, il risultato deve essere considerato come un'indicazione esplorativa.

ge=(1, 2))
