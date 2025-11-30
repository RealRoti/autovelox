# Autovelox Italiani Open Source

Questo progetto offre una **interfaccia web semplice e intuitiva** per consultare il censimento pubblico aggiornato degli autovelox italiani. L’obiettivo è rendere accessibile e fruibile a chiunque l’archivio degli autovelox, filtrando e cercando tutti i dispositivi registrati **comune per comune**, senza bisogno di navigare nel confusionario e incompleto PDF rilasciato dal Ministero.

NB: Oltre ai dispositivi in dotazione ai Comuni *(e alle loro forze di polizia locali)*, nel progetto sono presenti anche i velox utilizzati dalla Polizia Stradale, oppure intestati ad enti che non siano i comuni (ad esempio Unioni di Comuni, Comunità Montane...). Tali dispositivi si trovano nella scheda del sito apposita.

⚠ Il Ministero ha affidato agli enti locali il compito di compilare il portale per il censimento con i propri dispositivi, senza però vagliarne i risultati: sono presenti errori grossolani non corretti dal Ministero (che ha semplicemente pubblicato il dump delle risposte, così come sono). Infatti sono frequenti errori di battitura, ma soprattutto dimenticanze come la mancanza del codice catastale del comune. In questo caso è probabile che alcuni dispositivi in dotazione ai Comuni si trovino nella scheda "Altri enti". 

### Aggiornamento dati
Il Ministero ha imposto il 29-11-25 come deadline per la compilazione del censimento (data in cui è anche avvenuta la pubblicazione del file CSV da parte del Ministero). Perciò, i dispositivi che non sono nell'[elenco del Ministero](https://velox.mit.gov.it/dispositivi) sono da considerarsi **non validi** in caso di multe. 

Come previsto dall’art 5 comma 2 del decreto n. 305 del 18 agosto 2025, gli aggiornamenti continueranno anche dopo la scadenza tramite nuove comunicazioni telematiche obbligatorie da parte degli enti competenti. Ogni modifica (nuova installazione, rimozione, sostituzione, correzione) deve essere reinviata tramite la piattaforma della Motorizzazione, che aggiorna automaticamente l’elenco pubblico del Ministero. Solo i dispositivi effettivamente pubblicati nell’elenco aggiornato sono considerati legittimi. 

Per aggiornare i dati all'ultima pubblicazione, è sufficiente collegarsi al [Portale](https://velox.mit.gov.it/dispositivi), scaricare il CSV nuovo e lanciare lo script update.py, che è pensato per importare i dati originali e generare il file JSON usato dal front-end. Se i dati pubblici vengono aggiornati, sostituisci semplicemente il file di origine e riesegui lo script per ottenere un sito aggiornato.


## Demo / Live

Il sito è ospitato su GitHub Pages:  
[https://realroti.github.io/autovelox/](https://realroti.github.io/autovelox/)

## Struttura del progetto
├─ index.html ← pagina principale (UI) con js/css integrati.

├─ velox.json ← elaborazione finale dei dati completi (output di *update.py*)

├─ export-censimento-mit.csv ← file CSV di origine fornito dal MIT

├─ codice-comuni.txt ← file che contiene la corrispondenza *codice catastale-comune*

├─ update.py ← script per generare/aggiornare i dati

└─ img/ ← asset / immagini per il sito


## Installazione locale

Per utilizzare o sviluppare localmente:

1. Clona il repository  
   ```bash
   git clone https://github.com/realroti/autovelox.git
2. Per caricare correttamente il json durante la visualizzazione del sito, consiglio di aprire l'HTML in localhost
   ```bash
   python3 -m http.server
3. Per aggiornare i dati (ad esempio dopo nuovo CSV del MIT)
   ```bash
   python3 -m http.server

Lo script prenderà il file csv, tradurrà i codici catastali in nomi di comuni e province (tramite la corrispondenza nel txt) e riordinerà tutto nel JSON, in modo che possa venire caricato dall'HTML.

## Contributi

Ogni contributo (soprattutto aggiornamento del file JSON) è benvenuto.
L’obiettivo è mantenere il progetto semplice, mantenibile e aggiornato con i dati pubblici più recenti.
