# Progetto LLM e varietà degli output



Progetto per il corso di Tecnologie dei Dati e del Linguaggio.



## 1. Obiettivo del progetto



Questo progetto analizza il rapporto tra la **specificità del prompt** e la **varietà degli output** prodotti da un Large Language Model (LLM).



L'idea di base è verificare se, aumentando il numero di vincoli e di indicazioni presenti nel prompt, gli output generati dal modello tendano a diventare più simili tra loro.



L'esperimento è stato progettato come uno studio esplorativo, con generazione automatica dei testi, una metrica quantitativa di varietà e un confronto tra diversi livelli di specificità.



---



## 2. Domanda di ricerca



> **Come cambia la varietà degli output di un LLM all'aumentare del livello di specificità del prompt?**



---



## 3. Ipotesi



> **All'aumentare della specificità del prompt, la varietà degli output generati dal LLM tende a diminuire, perché un numero maggiore di vincoli limita le possibili modalità di risposta.**



In altre parole, l'ipotesi prevede che prompt più dettagliati portino il modello verso un insieme più ristretto di possibili risposte.



---



## 4. Disegno dell'esperimento



Sono stati scelti tre temi narrativi:



- **Mistero**

- **Viaggio**

- **Sogno**



Per ogni tema sono stati definiti tre livelli di specificità:



- **A = bassa specificità**

- **B = media specificità**

- **C = alta specificità**



Sono quindi presenti:



**3 temi × 3 livelli = 9 prompt**



Ogni prompt è stato utilizzato per **5 generazioni**, ottenendo:



**9 prompt × 5 generazioni = 45 testi**



Il dataset finale contiene quindi **45 output generati automaticamente**.



### Modello utilizzato



La generazione è stata effettuata con:



Qwen/Qwen2.5-0.5B-Instruct



La generazione originale è stata eseguita in **Google Colab** utilizzando una **GPU T4**.



I principali parametri di generazione sono stati:



- `temperature = 0.8`

- `top\_p = 0.95`

- `max\_new\_tokens = 700`

- `do\_sample = True`



L'utilizzo della generazione automatica permette di applicare la stessa procedura a tutti i prompt e di rendere l'esperimento più riproducibile.



---



## 5. Misura della varietà



Per misurare la varietà degli output è stata utilizzata una procedura basata su **TF-IDF** e **similarità coseno**.



### 5.1 Rappresentazione dei testi



I testi vengono trasformati in vettori numerici attraverso **TF-IDF**, utilizzando sia unigrammi sia bigrammi:



ngram\_range=(1, 2)



In questo modo ogni testo viene rappresentato in base alla presenza e all'importanza delle parole e delle coppie di parole.



### 5.2 Similarità coseno



Successivamente viene calcolata la **similarità coseno** tra le rappresentazioni dei testi.



La similarità coseno assume valori compresi tra 0 e 1:



- valori vicini a **1** → testi più simili;

- valori vicini a **0** → testi meno simili.



### 5.3 Confronto tra le generazioni



Per ogni condizione, cioè per ogni combinazione:



**tema × livello di specificità**



sono presenti 5 generazioni.



Le 5 generazioni vengono confrontate a coppie.



Il numero di confronti è:



**5 × 4 / 2 = 10 confronti per condizione**



Sono quindi calcolate 10 similarità per ciascuna delle 9 condizioni.



### 5.4 Definizione della varietà



La varietà viene definita come:



> **Varietà = 1 − similarità media**



Di conseguenza:



- similarità media alta → varietà bassa;

- similarità media bassa → varietà alta.



Questa misura considera soprattutto la **somiglianza lessicale** tra i testi.



---



## 6. Risultati



### 6.1 Varietà media per livello di specificità



| Livello | Varietà media |

|---|---:|

| A – bassa specificità | 0.934 |

| B – media specificità | 0.876 |

| C – alta specificità | 0.772 |



La varietà diminuisce progressivamente passando da A a B e da B a C.



Il valore medio passa da **0.934** nel livello A a **0.772** nel livello C.



La diminuzione complessiva è quindi di circa **0.162 punti**, corrispondente a una diminuzione relativa di circa **17%** rispetto al livello A.



### 6.2 Risultati per tema



| Tema | A | B | C |

|---|---:|---:|---:|

| Mistero | 0.931 | 0.864 | 0.786 |

| Viaggio | 0.925 | 0.863 | 0.801 |

| Sogno | 0.948 | 0.900 | 0.730 |



La stessa tendenza **A > B > C** è presente in tutti e tre i temi.



Questo significa che, nel campione analizzato, il passaggio da prompt meno specifici a prompt più specifici è associato a una riduzione della varietà degli output.






## 7. Grafici



### Varietà media per livello di specificità



!\[Varietà media degli output per livello di specificità](results/grafico\_varieta\_media\_ABC.png)



### Varietà degli output per tema e livello di specificità



!\[Varietà degli output per tema e livello di specificità](results/grafico\_varieta\_per\_tema.png)



---



## 8. Interpretazione dei risultati



I risultati ottenuti nel campione analizzato sono **coerenti con l'ipotesi di ricerca**.



All'aumentare della specificità del prompt si osserva una diminuzione della varietà media degli output:



**A → B → C**



La tendenza è presente in tutti e tre i temi considerati.



Il risultato può essere interpretato in questo modo: aumentando il numero di vincoli presenti nel prompt, il modello dispone di un insieme più ristretto di possibilità narrative e, di conseguenza, le risposte tendono a essere più simili tra loro.



È però importante sottolineare che questo risultato costituisce **un'evidenza esplorativa** e non permette di affermare che la relazione valga per tutti gli LLM o per qualsiasi tipo di prompt.



---



## 9. Limiti dello studio



L'esperimento presenta alcuni limiti.



### Campione ridotto



Sono stati analizzati 45 testi, con 5 generazioni per ciascuna condizione.



Un campione più grande permetterebbe di ottenere una valutazione più robusta della tendenza osservata.



\### Un solo modello



L'esperimento utilizza un solo modello:



Qwen/Qwen2.5-0.5B-Instruct



Non è quindi possibile stabilire se lo stesso comportamento si verifichi anche con altri LLM.



### Limiti della metrica



TF-IDF e similarità coseno misurano principalmente la somiglianza sulla base della rappresentazione lessicale.



Due testi possono essere semanticamente simili pur utilizzando parole diverse, oppure possono condividere molte parole pur presentando contenuti differenti.



Per questo motivo la misura utilizzata non cattura perfettamente la similarità semantica.



\### Più caratteristiche cambiano contemporaneamente



Passando dal livello A al livello B e poi al livello C cambiano contemporaneamente diverse caratteristiche dei prompt, tra cui:



- personaggi;

- ambientazione;

- tono;

- lunghezza richiesta;

- eventi;

- dialoghi;

- vincoli narrativi;

- struttura del finale.



L'esperimento misura quindi l'effetto complessivo dell'aumento della specificità e non l'effetto isolato di un singolo vincolo.



\### Nessun test di significatività



Dato il carattere esplorativo dell'esperimento e la dimensione ridotta del campione, non vengono formulate conclusioni di significatività statistica.



---



## 10. Struttura del repository



```text

progetto-llm-varieta/

├── README.md

├── requirements.txt

├── data/

│   └── dataset\_completo.csv

├── prompts/

│   └── prompts.txt

├── code/

│   ├── generazione\_qwen.py

│   └── analisi\_varieta.py

└── results/

&#x20;   ├── riepilogo\_varieta.csv

&#x20;   ├── risultati\_varieta\_per\_condizione.csv

&#x20;   ├── similarita\_coppie.csv

&#x20;   ├── grafico\_varieta\_media\_ABC.png

&#x20;   └── grafico\_varieta\_per\_tema.png

