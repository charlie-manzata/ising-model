# Modello di Ising ferromagnetico 2D

Simulazione interattiva nel browser del **modello di Ising ferromagnetico bidimensionale**, realizzata con Python, Streamlit e JavaScript.

L'applicazione permette di osservare come la competizione tra **interazione ferromagnetica** e **agitazione termica** produca ordine magnetico a bassa temperatura e disordine ad alta temperatura.

## Funzionalità

- algoritmo di **Metropolis**;
- condizioni periodiche al bordo;
- interazione ferromagnetica con \(J>0\);
- rete regolabile da **10×10 a 150×150**;
- temperatura regolabile in tempo reale;
- velocità della simulazione regolabile;
- pulsanti **Play/Pausa** e **Reset**;
- visualizzazione degli spin tramite frecce;
- visualizzazione in tempo reale di:
  - numero di sweep;
  - magnetizzazione normalizzata \(M/N\);
  - magnetizzazione assoluta \(|M|/N\);
  - energia per spin \(E/N\);
- grafico temporale di \(M/N\) e \(|M|/N\).

## Modello fisico

Il modello di Ising ferromagnetico è descritto dall'Hamiltoniana

\[
H=-J\sum_{\langle i,j\rangle}s_i s_j,
\]

dove ogni spin può assumere i valori

\[
s_i=\pm1
\]

e \(J>0\).

Gli spin paralleli hanno energia di interazione più bassa rispetto agli spin antiparalleli. L'interazione tende quindi a produrre ordine magnetico.

Per un tentativo di inversione di uno spin, la variazione di energia è

\[
\Delta E=2Js_i\sum_{\mathrm{vicini}}s_j.
\]

L'algoritmo di Metropolis accetta il cambiamento con probabilità

\[
P=
\begin{cases}
1 & \Delta E\leq0,\\
e^{-\Delta E/(k_BT)} & \Delta E>0.
\end{cases}
\]

Nella simulazione viene utilizzata l'unità \(k_B=1\), quindi

\[
P=e^{-\Delta E/T}.
\]

Per il modello di Ising 2D quadrato, in assenza di campo magnetico, la temperatura critica esatta è

\[
\frac{k_BT_c}{J}
=
\frac{2}{\ln(1+\sqrt2)}
\simeq2.269.
\]

## Interpretazione della simulazione

A temperature basse, le configurazioni con spin allineati sono favorite energeticamente e tendono a formarsi grandi domini magneticamente ordinati.

A temperature elevate, le fluttuazioni termiche rendono più probabili anche configurazioni energeticamente sfavorevoli e l'ordine magnetico viene progressivamente distrutto.

Il grafico mostra sia

\[
M/N
\]

sia

\[
|M|/N.
\]

La quantità \(|M|/N\) è particolarmente utile sotto la temperatura critica: in un sistema finito la magnetizzazione può cambiare spontaneamente segno, passando da uno stato prevalentemente positivo a uno prevalentemente negativo. In questo caso \(M/N\) può avvicinarsi a zero anche se il sistema rimane fortemente ordinato.

## Utilizzo

I controlli disponibili nell'applicazione sono:

- **Play/Pausa** — avvia o interrompe la simulazione;
- **Reset** — genera una nuova configurazione iniziale;
- **T/J** — modifica la temperatura ridotta;
- **Velocità** — modifica il numero di sweep eseguiti per frame;
- **Rete** — modifica la dimensione della rete da 10×10 a 150×150.

La configurazione iniziale può essere scelta tra:

- **Casuale**;
- **Tutti +1**.

## Installazione locale

Clonare il repository:

```bash
git clone https://github.com/TUO-USERNAME/NOME-REPOSITORY.git
cd NOME-REPOSITORY
