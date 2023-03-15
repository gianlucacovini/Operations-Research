#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 10:39:31 2022

@author: gianlucacovini
"""
Pi = range(3600) # Considero un'ora a partire da tempo 0
S = [0, 1, 2] # Immagino di avere tre fermate a, b, c
T = [{0: (0, 2), 2: (2000, 2001), 1: (2570, 2575)}, {1: (7, 10), 2: (150, 170)}, {0: (2, 3), 1: (5, 6)}]
    # Ho tre viaggi: ad es. il primo il mezzo arriva in a a tempo 0,
    # parte a tempo 2, arriva in c a tempo 200, riparte a tempo 201,
    # arriva in b a tempo 570, riparte a tempo 575
R = T
    # ogni itinerario è una lista di viaggi
F = {(0,1): 500, (1, 2): 200, (2, 0): 450}

pS = 0
pT = 2
tau = 1
itmax = 2000


def RAPTOR(Pi, S, T, R, F, pS, pT, tau, itmax):
    """
    Input: 
        - Pi lista di secondi del tipo range(len(Pi))
        - S lista di fermate indicate con un numero a partire da 0
        - T lista di viaggi: ogni viaggio è un dizionario del tipo "fermata: (tempo di partenza, tempo di arrivo)"
        - R lista di itinerari: ogni itinerario lo penso come una lista di viaggi con le stesse fermate. Per semplicità qui prendiamo un viaggio per lista
        - F è un dizionario con delle coppie di stop (p, p'): l(p,p') lunghezza (in termini di tempo)
        - pS fermata di partenza in S
        - pT fermata di arrivo in S
        - tau in Pi tempo di partenza
        - itmax numero massimo di iterazioni
    """
    if not(pS in S and pT in S and tau in Pi):
        raise "Inserire dati corretti" # controllo i dati
    
    else:
        # Inizializzazione dei tempi e delle fermate segnate
        tP = [float('inf') for j in range(itmax)] # Inizializzo a infinito la lista dei tempi per ogni k per una singola fermata
        n = len(S)
        tempo = [tP for j in range(n)] # Inizializzo la lista dei tempi tau_k(p)
        tempoStar = [float('inf')  for j in range(n)] # Inizializzo a infinito la lista dei tempi tauStar(p)
        
        tempo[pS][0] = tau # Inizializzo il tempo tau_0(pS) a tau
        mS = [pS] # lista con tutti i marked stops
        
        it = 0
        # Iterazioni dell'algoritmo
        for k in range(itmax+1):
            it += 1
            Q = [] # è una lista di tuple (r,p)
            for p in mS: # Fisso una marked stop
                for r in filter(lambda r: p in r, R): # Controllo tutte le route che passano per p
                    c = 0  # Il contatore tiene conto se ho già rimpiazzato (r,q)                                
                    for q in S: # Controlla tutte le fermate    
                        if (r,q) in Q: # Se trovo una fermata q per cui (r,q) sta in Q la sostituisco con (r,p)
                            c += 1
                            rS = list(r.keys()) # Riscrivo la route come sequenza delle sue fermate
                            if rS.index(p)<rS.index(q): 
                                Q.remove((r,q))
                                Q.append((r,p))
                    if c == 0:  # Controlla se non ci sono stati rimpiazzamenti in Q
                        Q.append((r,p))
            mS = []

            for (r,p) in Q:
                rS = list(r.keys())
                indice = rS.index(p)
                t = r
                
                for p in rS[indice:]:
                    if pS in t:
                        if t[p][1] < min([tempoStar[p], tempoStar[pT]]):  
                             tempo[p][k] = t[p][1]
                             tempoStar[p] = t[p][1]
                             mS.append(p)
                    else:
                        if t[p][1] + min(filter(lambda q: tempoStar.index(q) in t, tempoStar)) < min([tempoStar[p], tempoStar[pT]]):
                             tempo[p][k] = t[p][1]
                             tempoStar[p] = t[p][1]
                             mS.append(p)
                            
            tmS = []
            for p in mS:
                for f in filter(lambda f: f[0] == p, F): 
                    q = f[1]
                    tempo[q][k] = min(tempo[q][k], tempo[p][k]+F[f])
                    tmS.append(q)
            mS = mS +tmS
            
            if mS == []:
                it = it-1
                return tempoStar[pT], it 