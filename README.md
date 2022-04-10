# Marketplace

VELO DARIO 331CA
Scopul temei este sa gasim metode de sincronizare pentru a diferentia actiunile Producatorului si 
Consumatorului in modul in care folosesc Produsele. Pentru aceasta metoda m-am gandit sa folosesc semafoare. Un Semaphore 
mentine un contor intern care este decrementat de un apel acquire() si incrementat de un apel release(). Metoda acquire() nu va 
permite decrementarea contorului sub valoarea 0, ea blocand executia thread-ului in acest caz pana cand contorul este 
incrementat de un release(). Am folosit initial 2 semafoare, unul pentru Consumator si unul pentru Producator.Aceste semafoare 
initializate cu 1, ii vor identifica acesti componenti prin id-uri. In acest fel, in momentul in care un Producator intra in 
flow, el va primi id,iar apoi va continua sa isi publice produsele, conform conditiile de asteptare daca esuaza. Daca un produs 
este adaugat cu succes, el ii se va alatura unui dictionar cu cheie id-ul si valoare un append la fiecare produs publicat pentru 
acest producator + disponibilitatea produsului. Disponibilitatea produsului la producator difera pe baza actiunilor 
consumatorului in marketplace. Si consumatorii au dictionarul lor, avand ca cheie id si valoare o lista de produse.Daca un 
consumator adauga un produs in cartul lui, in lista lui se va adauga acest produs, iar in dictionarul de producator acest 
produs nu va mai fi disponibil. Pentru disponibilitate am initializat o variabila de tip bool. Un alt semafor este folosit in 
momentul in care sunt afisate produsele finale unui consumator. Motivul pentru acesta este pentru ca in fisierele cu input mare, 
existau cazuri de race condition si produsele nu erau afisate cum trebuie. Am folosit logging aproape in fiecare functie, pentru 
a urmari rezultatele din ambele clase cu extensia .info si cazurile delicate de erori cu extensia .error. Fisierele de log sunt 
impartite cu un maxBytes=100000.
