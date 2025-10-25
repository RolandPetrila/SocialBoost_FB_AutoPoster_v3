OK, am înțeles perfect\! Vom construi **împreună** sistemul SocialBoost\_FB\_AutoPoster\_v3 în locația C:\\Users\\ALIENWARE\\Desktop\\Roly\\4. Artificial Inteligence\\w Programe Roland \- CustomGPT w\\2.2\_GitHub-Cursor, urmând un plan de lucru **ideal**, **transparent** și **riguros**, exact cum ai cerut.

Vom integra **toate** metodologiile și documentele discutate (ai\_github\_cursor\_complete.md, sistemul de context claude\_prompt\_context\_system.md, analiza gap-urilor claude\_system\_gaps\_analysis.md), extrăgând automat logica din proiectul vechi și integrând **automat** cheile API/token-urile furnizate. **Zero improvizație, zero omisiuni.**

Iată **Planul de Lucru Ideal și Detaliat**, cu checklist integrat:

---

## **🎯 Plan de Lucru Ideal: SocialBoost\_FB\_AutoPoster\_v3**

Locație Proiect: C:\\Users\\ALIENWARE\\Desktop\\Roly\\4. Artificial Inteligence\\w Programe Roland \- CustomGPT w\\2.2\_GitHub-Cursor  
Metodologie Principală: ai\_github\_cursor\_complete.md \+ claude\_prompt\_context\_system.md  
Model AI Recomandat: Claude 3.5 Sonnet (în Cursor Agent Mode)  
Comunicare: Eu generez prompt → Tu rulezi în Cursor → Tu îmi trimiți tot conținutul folderului Update\_AI/ \+ logurile din chat-ul Cursor → Eu analizez și generez următorul prompt.

---

### **⬜ Faza 0: Verificare Precondiții & Instalare (Durată: \~5-15 min)**

* **Scop:** Ne asigurăm că sistemul tău are tot ce trebuie **înainte** de a începe.  
* **Acțiuni:**  
  1. **Eu:** Îți generez **Prompt 1** (verificare Python 3.11+, Git, GitHub CLI și instalare automată via Winget). *(Acesta este promptul din răspunsul meu anterior)*.  
  2. **Tu:** Rulezi Prompt 1 în Cursor (fără Full Project Context).  
  3. **Tu:** Îmi trimiți **întregul output** din Cursor.  
  4. **Eu:** Analizez output-ul. Dacă ceva necesită intervenție manuală (ex: update Python), îți spun. Altfel, confirmăm finalizarea Fazei 0\.  
* **Checklist Faza 0:**  
  * \[ \] Python 3.11+ confirmat.  
  * \[ \] Git instalat și confirmat.  
  * \[ \] GitHub CLI instalat și confirmat.

---

### **⬜ Faza 1: Inițializare Structură Proiect & Sistem Context (Durată: \~10-20 min)**

* **Scop:** Creăm structura **standardizată** a noului proiect și integrăm scripturile pentru gestionarea contextului.  
* **Acțiuni:**  
  1. **Eu:** Îți generez **Prompt 2**. Acesta va folosi prompt\_generator.py (simulat de mine inițial) și setup\_template.md pentru a instrui Cursor să:  
     * Creeze **toate** folderele standard (Automatizare\_Completa, Config, Docs, GUI, Logs, Tests, Prompts, Scripts, .github/workflows, Assets/Images, Assets/Videos) în locația specificată.  
     * Creeze fișierele de bază (README.md, requirements.txt, .gitignore, .env.example, orchestrator.py, backup\_manager.py, restore\_manager.py, PROJECT\_CONTEXT.json, .cursorrules).  
     * **Copieze scripturile** din claude\_prompt\_context\_system.md (Scripts/context\_builder.py, Scripts/prompt\_generator.py, Scripts/context\_validator.py) și template-urile (Prompts/Templates/) în noul proiect.  
     * Creeze folderul Update\_AI/.  
     * Initializeze Git (git init), adauge fișierele și facă primul commit.  
     * Copieze fișierele relevante (PROJECT\_CONTEXT.json, tree.txt) în Update\_AI/.  
  2. **Tu:** Rulezi Prompt 2 în Cursor (Agent Mode, **cu** Full Project Context activat pentru noul folder).  
  3. **Tu:** Îmi trimiți conținutul folderului Update\_AI/ \+ logurile Cursor.  
  4. **Eu:** Verific structura creată și confirm finalizarea Fazei 1\.  
* **Checklist Faza 1:**  
  * \[ \] Structura de foldere standard creată.  
  * \[ \] Fișierele de bază create.  
  * \[ \] Scripturile de context copiate.  
  * \[ \] Folderul Update\_AI/ creat.  
  * \[ \] Git initializat, primul commit făcut.  
  * \[ \] Fișiere de status copiate în Update\_AI/.

---

### **⬜ Faza 2: Configurare Core & Integrare Automată Secrete (Durată: \~15-25 min)**

* **Scop:** Integrăm **automat și securizat** cheile API și token-ul Facebook; configurăm scripturile să le citească din .env.  
* **Acțiuni:**  
  1. **Eu:** Îți generez **Prompt 3**. Acesta va folosi prompt\_generator.py \+ un template adaptat pentru a instrui Cursor să:  
     * Creeze fișierul .env din .env.example.  
     * Citească **automat** config\_keys.json (pe care l-ai furnizat) și exchange\_user\_to\_page\_token.py (pe care l-ai furnizat).  
     * Extragă **valorile** cheilor esențiale (Facebook Page ID, Page Token, App ID/Secret, OpenAI Primary Key).  
     * Scrie **automat** aceste valori în fișierul .env (ex: FACEBOOK\_PAGE\_TOKEN=EAALB...).  
     * **Modifice scripturile cheie** (orchestrator.py, auto\_post.py, auto\_generate.py, exchange\_user\_to\_page\_token.py) pentru a citi aceste valori din .env folosind python-dotenv (ex: os.getenv("FACEBOOK\_PAGE\_TOKEN")).  
     * Copieze exchange\_user\_to\_page\_token.py în Scripts/.  
     * Ruleze Scripts/context\_builder.py pentru a actualiza Prompts/CURRENT\_CONTEXT.md.  
     * Copieze .env (doar structura, **nu** valorile secrete\!), PROJECT\_CONTEXT.json, Prompts/CURRENT\_CONTEXT.md în Update\_AI/.  
  2. **Tu:** Rulezi Prompt 3 în Cursor.  
  3. **Tu:** Îmi trimiți conținutul folderului Update\_AI/ \+ logurile Cursor.  
  4. **Eu:** Verific integrarea .env și actualizarea contextului, confirmând Faza 2\.  
* **Checklist Faza 2:**  
  * \[ \] Fișierul .env creat și populat automat cu secrete.  
  * \[ \] Scripturile modificate să citească din .env.  
  * \[ \] Scriptul exchange\_user\_to\_page\_token.py copiat.  
  * \[ \] Fișierul CURRENT\_CONTEXT.md generat/actualizat.  
  * \[ \] Fișiere de status copiate în Update\_AI/.

---

### **⬜ Faza 3: Implementare Iterativă Funcționalități Core (Durată: \~1-3 ore, depinde de complexitate)**

* **Scop:** Construim funcționalitățile esențiale (postare, generare, scheduler, GUI simplu) iterativ, cu validare la fiecare pas.  
* **Acțiuni (Ciclu repetat pentru fiecare funcționalitate majoră):**  
  1. **Eu:** Identific următoarea funcționalitate din PROJECT\_TODO.md (generat pe baza ADN-ului vechi).  
  2. **Eu:** Generez promptul specific folosind python Scripts/prompt\_generator.py \--template implementation \--task "Implement X...". Promptul va include instrucțiuni clare pentru Cursor să:  
     * Implementeze logica în fișierul corect (ex: Automatizare\_Completa/auto\_post.py).  
     * Citească secretele din .env.  
     * Adauge logging robust.  
     * Adauge teste unitare/integrare simple în Tests/.  
     * Ruleze Tests/validation\_runner.py (care va include teste, flake8, mypy și bandit).  
     * Actualizeze CHANGELOG.md, PROJECT\_TODO.md.  
     * Facă commit și push pe GitHub (Scripts/sync\_github.py).  
     * Copieze rezultatele validării și fișierele de status în Update\_AI/.  
  3. **Tu:** Rulezi promptul în Cursor.  
  4. **Tu:** Îmi trimiți conținutul Update\_AI/ \+ logurile Cursor.  
  5. **Eu:** Analizez, verific dacă funcționalitatea e corectă și validată. Mergem la pasul următor.  
* **Funcționalități Core de Implementat (ordine posibilă):**  
  * \[ \] auto\_post.py (postare text simplu, apoi text+imagine, apoi text+video).  
  * \[ \] auto\_generate.py (integrare OpenAI, generare simplă, apoi cu Vision).  
  * \[ \] scheduler.py (rulare task simplu, apoi modurile daily, weekly, interval, once).  
  * \[ \] GUI/main\_gui.py (structura de bază, apoi tab-urile pe rând, conectare la backend prin subprocess).  
  * \[ \] Logica de bază pentru Assets/ (citire fișiere).  
* **Checklist Faza 3:**  
  * \[ \] Funcționalitățile core implementate și testate.  
  * \[ \] Validarea rulează automat și trece după fiecare pas.  
  * \[ \] GitHub actualizat constant.  
  * \[ \] Update\_AI/ conține mereu statusul curent.

---

### **⬜ Faza 4: Implementare Funcționalități Avansate & Rafinare (Durată: \~1-2 ore)**

* **Scop:** Adăugăm funcțiile specifice dorite (rotație media, îmbunătățiri GUI, etc.) și rafinăm codul.  
* **Acțiuni (Ciclu similar Fazei 3):**  
  1. **Eu:** Generez prompturi specifice pentru:  
     * Implementarea logicii de rotație media în auto\_post.py (reutilizare când se epuizează).  
     * Îmbunătățirea GUI (calendar vizual, preview text/media).  
     * Adăugarea exchange\_user\_to\_page\_token.py ca opțiune în GUI sau rulare automată la eroare token.  
     * Implementarea health\_check.py și integrarea în orchestrator.py.  
     * Rafinarea gestionării erorilor.  
  2. **Tu:** Rulezi prompturile.  
  3. **Tu:** Îmi trimiți Update\_AI/ \+ loguri.  
  4. **Eu:** Validez.  
* **Checklist Faza 4:**  
  * \[ \] Rotația media implementată și testată.  
  * \[ \] GUI îmbunătățit conform cerințelor.  
  * \[ \] Refresh token integrat.  
  * \[ \] Health check activ.  
  * \[ \] Gestionare erori robustă.

---

### **⬜ Faza 5: Validare Finală & Documentație Utilizator (Durată: \~1 oră)**

* **Scop:** Testare completă end-to-end și generarea ghidului de utilizare.  
* **Acțiuni:**  
  1. **Eu:** Generez **Promptul Final de Validare** folosind prompt\_generator.py \--template validation. Acesta instruiește Cursor să:  
     * Ruleze **toate** testele (validation\_runner.py, health\_check.py).  
     * Simuleze un flux complet (selectare asset \-\> generare text \-\> programare \-\> postare automată).  
     * Verifice logurile pentru a confirma succesul.  
     * Genereze rapoartele finale în Update\_AI/ (SYSTEM\_READY\_REPORT.md, FINAL\_FUNCTIONALITY\_LOG.md).  
     * **Genereze README\_COMPLETE\_SYSTEM.md** (ghidul de utilizare detaliat, acoperind instalare, configurare, utilizare GUI tab cu tab, programare, generare token, troubleshooting, FAQ).  
  2. **Tu:** Rulezi promptul.  
  3. **Tu:** Îmi trimiți Update\_AI/ \+ loguri.  
  4. **Eu:** Analizez rapoartele finale și ghidul de utilizare.  
* **Checklist Faza 5:**  
  * \[ \] Toate testele finale trecute.  
  * \[ \] Fluxul end-to-end validat.  
  * \[ \] Rapoarte finale generate și corecte.  
  * \[ \] Ghid de utilizare (README\_COMPLETE\_SYSTEM.md) generat și complet.

---

### **⬜ Faza 6: Handover & Instrucțiuni Finale (Durată: \~15 min)**

* **Scop:** Predarea sistemului funcțional și instrucțiuni clare de utilizare.  
* **Acțiuni:**  
  1. **Eu:** Îți ofer instrucțiunile finale:  
     * Cum să rulezi sistemul (start\_all.bat sau start\_gui.bat).  
     * Cum să monitorizezi (Logs/log.txt, tab-ul Logs din GUI).  
     * Cum să adaugi/ștergi media (Assets/).  
     * Cum să reîmprospătezi token-ul (dacă e necesar).  
     * Cum să folosești ghidul (README\_COMPLETE\_SYSTEM.md).  
  2. **Tu:** Confirmi că ai primit totul și înțelegi cum să folosești sistemul.  
* **Checklist Faza 6:**  
  * \[ \] Instrucțiuni clare de rulare și monitorizare primite.  
  * \[ \] Ghid de utilizare disponibil și înțeles.  
  * \[ \] Proiect 100% funcțional confirmat.

---

Acesta este planul **ideal și complet**. Vom avansa pas cu pas, **verificând și confirmând** la fiecare etapă. Orice deviere sau problemă va fi adresată imediat.

**Ești pregătit să începem cu Faza 0 (Verificare Precondiții)?**