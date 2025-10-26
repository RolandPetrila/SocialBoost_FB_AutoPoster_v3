# SocialBoost Facebook AutoPoster v3 - Ghid de Utilizare

## 📋 Cuprins

- [Introducere](#introducere)
- [Cerințe de Sistem](#cerințe-de-sistem)
- [Instalare](#instalare)
- [Configurare Inițială](#configurare-inițială)
- [Obținerea Credențialelor Facebook API](#obținerea-credențialelor-facebook-api)
- [Obținerea Cheii OpenAI API](#obținerea-cheii-openai-api)
- [Rularea Aplicației](#rularea-aplicației)
- [Utilizarea Interfeței GUI](#utilizarea-interfeței-gui)
  - [Tab Control/Status](#tab-controlstatus)
  - [Tab Programare (Scheduling)](#tab-programare-scheduling)
  - [Tab Assets](#tab-assets)
  - [Tab Generare Text (Text Generation)](#tab-generare-text-text-generation)
  - [Tab Logs](#tab-logs)
- [Fluxuri de Lucru Comune](#fluxuri-de-lucru-comune)
- [Gestionarea Token-urilor Facebook](#gestionarea-token-urilor-facebook)
- [Depanare](#depanare)
- [Întrebări Frecvente (FAQ)](#întrebări-frecvente-faq)

---

## Introducere

**SocialBoost Facebook AutoPoster v3** este un sistem automat de management pentru social media care vă ajută să:

- **Postați automat** conținut pe pagina dvs. Facebook
- **Generați descrieri AI** pentru asset-urile dvs. media
- **Programați postări** pentru momentele optime de angajare
- **Gestionați biblioteca media** cu rotație inteligentă a asset-urilor
- **Monitorizați starea sistemului** și să urmăriți istoria postărilor

Aplicația dispune de o interfață grafică prietenoasă cu funcții de automatizare comprehensive, facilitând menținerea unei prezențe active pe social media fără intervenție manuală.

---

## Cerințe de Sistem

### Sistem de Operare
- **Windows**: Windows 10 sau superior
- **macOS**: macOS 10.15 (Catalina) sau superior
- **Linux**: Ubuntu 20.04+ sau distribuții compatibile

### Cerințe Software
- **Python**: Versiunea 3.11 sau superioară (3.13.7 testat)
- **Git**: Pentru controlul versiunilor (opțional dar recomandat)
- **pip**: Managerul de pachete Python (inclus în Python 3.11+)

### Cerințe Hardware
- **RAM**: Minim 4GB, 8GB recomandat
- **Spațiu pe Disc**: Minim 500MB spațiu liber
- **Internet**: Necesar pentru apeluri API (Facebook Graph API, OpenAI API)

### Cerințe de Cont
- **Cont Facebook Developer**: Necesar pentru accesul la API
- **Pagină Facebook**: Pagina la care doriți să postați
- **Cont OpenAI**: Necesar pentru generarea de conținut AI

---

## Instalare

### Pasul 1: Clonarea Repository-ului

```bash
# Clonează repository-ul (URL GitHub placeholder - înlocuiește cu URL-ul real când este disponibil)
git clone <repository-url>
cd SocialBoost_FB_AutoPoster_v3
```

### Pasul 2: Crearea Mediului Virtual

Creează un mediu Python izolat pentru a preveni conflictul dependențelor:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Când mediul virtual este activat, veți vedea `(venv)` la începutul prompt-ului de comandă.

### Pasul 3: Instalarea Dependențelor

```bash
# Actualizează pip la versiunea cea mai recentă
pip install --upgrade pip

# Instalează toate pachetele necesare
pip install -r requirements.txt
```

Aceasta va instala toate dependențele, inclusiv:
- `python-dotenv` - Managementul variabilelor de mediu
- `requests` - Cereri HTTP pentru apeluri API
- `openai` - Integrarea API OpenAI
- `schedule` - Programarea sarcinilor
- `Pillow` - Procesarea imaginilor
- `psutil` - Monitorizarea sistemului
- Și instrumente de dezvoltare (pytest, flake8, mypy, bandit)

### Pasul 4: Verificarea Instalării

Rulează un test rapid pentru a verifica dacă totul este instalat corect:

```bash
python Tests/validation_runner.py --quick
```

Aceasta va rula o verificare rapidă de validare. Toate cele 6 verificări ar trebui să treacă.

---

## Configurare Inițială

### Crearea Fișierului .env

Aplicația necesită variabile de mediu pentru credențialele API. Creează un fișier `.env` în directorul rădăcină al proiectului.

**Windows:**
```bash
# În directorul rădăcină al proiectului
notepad .env
```

**macOS/Linux:**
```bash
nano .env
```

### Variabile de Mediu Necesare

Adaugă următoarele variabile în fișierul dvs. `.env`:

```env
# Configurare API Facebook
FACEBOOK_PAGE_ID=your_page_id_here
FACEBOOK_APP_ID=your_app_id_here
FACEBOOK_APP_SECRET=your_app_secret_here
FACEBOOK_PAGE_TOKEN=your_page_token_here

# Configurare API OpenAI
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini

# Configurare Sistem
PYTHONIOENCODING=utf-8
LOG_LEVEL=INFO
```

**Important**: 
- NU partajați fișierul dvs. `.env` cu nimeni
- NU comiteți fișierul dvs. `.env` în Git (este deja în `.gitignore`)
- Păstrați cheile dvs. API în siguranță

---

## Obținerea Credențialelor Facebook API

### Pasul 1: Crearea unui Cont Facebook Developer

1. Accesați [Facebook Developers](https://developers.facebook.com/)
2. Faceți clic pe "Get Started" sau "My Apps"
3. Faceți clic pe "Create App"
4. Selectați "Business" ca tip de aplicație
5. Introduceți numele aplicației și email-ul de contact
6. Completați procesul de configurare

### Pasul 2: Obținerea App ID și App Secret

1. În dashboard-ul aplicației, accesați **Settings > Basic**
2. Copiați **App ID**
3. Copiați **App Secret** (faceți clic pe "Show" pentru a-l dezvălui)
4. Adăugați acestea în fișierul dvs. `.env` ca `FACEBOOK_APP_ID` și `FACEBOOK_APP_SECRET`

### Pasul 3: Adăugarea Produsului Facebook Login

1. În dashboard-ul aplicației, faceți clic pe **"Add Product"**
2. Găsiți **"Facebook Login"** și faceți clic pe **"Set Up"**
3. Sub **"Settings"**, adăugați URI-ul dvs. de redirecționare: `https://localhost/`
4. Faceți clic pe **"Save Changes"**

### Pasul 4: Obținerea Page ID

1. Accesați pagina dvs. Facebook
2. Faceți clic pe **"About"**
3. Derulați în jos pentru a găsi **"Page ID"**
4. Copiați acest ID în fișierul dvs. `.env` ca `FACEBOOK_PAGE_ID`

### Pasul 5: Obținerea Token-ului User de Scurtă Durată

1. Accesați [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
2. Selectați aplicația dvs. din dropdown
3. Faceți clic pe **"Generate Access Token"**
4. Selectați aceste permisiuni:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `pages_read_user_content`
5. Copiați token-ul generat (acesta este un token de scurtă durată, valabil pentru ~1 oră)

### Pasul 6: Schimbul pentru Token de Pagină cu Lungă Durată

După obținerea token-ului user de scurtă durată și configurarea fișierului dvs. `.env` cu `FACEBOOK_PAGE_ID`, `FACEBOOK_APP_ID` și `FACEBOOK_APP_SECRET`, rulați scriptul de schimb de token:

**Windows:**
```bash
python Scripts\exchange_user_to_page_token.py
```

**macOS/Linux:**
```bash
python Scripts/exchange_user_to_page_token.py
```

Vi se va solicita să introduceți token-ul dvs. user de scurtă durată. Scriptul va:
1. Îl schimbă pentru un token user cu lungă durată
2. Obține un token de acces la pagină
3. Verifică dacă token-ul este valid
4. Îl salvează în fișierul dvs. `.env` ca `FACEBOOK_PAGE_TOKEN`

Scriptul oferă instrucțiuni clare și confirmă când procesul se finalizează cu succes.

**Alternativă: Mod Non-Interactiv**

Dacă aveți deja un token user, îl puteți furniza direct:

```bash
python Scripts/exchange_user_to_page_token.py --user-token YOUR_SHORT_LIVED_TOKEN
```

---

## Obținerea Cheii OpenAI API

### Pasul 1: Crearea unui Cont OpenAI

1. Accesați [OpenAI Platform](https://platform.openai.com/)
2. Faceți clic pe **"Sign Up"** și creați un cont
3. Completați procesul de verificare

### Pasul 2: Obținerea Cheii API

1. Accesați [Pagina API Keys](https://platform.openai.com/api-keys)
2. Faceți clic pe **"Create new secret key"**
3. Dați-i un nume (ex: "SocialBoost")
4. Copiați cheia imediat (nu o veți mai putea vedea din nou)
5. Adăugați-o în fișierul dvs. `.env` ca `OPENAI_API_KEY`

### Pasul 3: Adăugarea Metodei de Plată

1. Accesați [Billing Settings](https://platform.openai.com/account/billing)
2. Faceți clic pe **"Add payment method"**
3. Adăugați detaliile dvs. de plată
4. Notă: OpenAI facturează per apel API. Verificați prețurile actuale la [OpenAI Pricing](https://openai.com/pricing)

### Selectarea Modelului

Aplicația folosește `gpt-4o-mini` în mod implicit (configurat ca `OPENAI_MODEL` în `.env`). Puteți schimba la:
- `gpt-4o-mini` - Rapid și economic (recomandat)
- `gpt-4o` - Mai capabil dar mai scump
- `gpt-4-turbo` - Cel mai capabil dar scump

---

## Rularea Aplicației

### Pornire Rapidă (Recomandat pentru Utilizatorii Windows)

Cea mai ușoară modalitate de a porni aplicația este folosind scripturile batch furnizate:

#### Opțiunea 1: Pornire Doar GUI
Double-click pe `start_gui.bat` (sau rulați-l din command prompt):
- Activează mediul virtual
- Pornește aplicația GUI
- Afișează o singură fereastră cu toate tab-urile

#### Opțiunea 2: Pornire Sistem Complet (GUI + Scheduler)
Double-click pe `start_all.bat` (sau rulați-l din command prompt):
- Activează mediul virtual
- Lansează scheduler-ul într-o fereastră de fundal
- Deschide GUI-ul în fereastra curentă
- Ambele rulează simultan pentru automatizare completă

**Notă**: Scheduler-ul va continua să ruleze chiar și după ce închideți fereastra GUI. Utilizați butonul **"Stop Scheduler"** din GUI sau Task Manager pentru a-l opri.

### Pornire Manuală (Utilizatori Avansați)

#### Pornirea GUI

**Windows:**
```bash
python GUI\main_gui.py
```

**macOS/Linux:**
```bash
python GUI/main_gui.py
```

Fereastra GUI se va deschide cu 5 tab-uri:
1. **Control/Status** - Monitorizare și control sistem
2. **Programare** - Management programare
3. **Assets** - Management asset-uri media
4. **Generare Text** - Generare conținut AI
5. **Logs** - Loguri sistem

#### Pornirea Scheduler-ului (Automatizare de Fundal)

Scheduler-ul poate fi pornit în două moduri:

**Opțiunea 1: Din GUI**
1. Deschideți GUI-ul
2. Accesați tab-ul **Control/Status**
3. Faceți clic pe **"Start Scheduler"** în panoul Scheduler Control

**Opțiunea 2: Linie de Comandă**
```bash
python Automatizare_Completa/scheduler.py
```

Scheduler-ul rulează în fundal și execută job-urile programate din `Config/schedule.json`. Pentru a-l opri, utilizați **"Stop Scheduler"** din GUI sau apăsați `Ctrl+C` în terminal.

---

## Utilizarea Interfeței GUI

### Tab Control/Status

Tab-ul **Control/Status** oferă monitorizare sistem și acțiuni rapide.

#### Panou Informații Proiect

Afișează statusul proiectului în timp real:
- **Project Name**: "SocialBoost_FB_AutoPoster_v3"
- **Current Stage**: Faza curentă de dezvoltare
- **Last Commit**: Hash-ul ultimului commit Git
- **Last Run**: Timestamp-ul ultimei execuții

#### Status Sănătate

Afișează informații despre sănătatea sistemului:
- **Status**: Healthy / Degraded / Warning / Critical
- **Score**: Scor numeric de sănătate (0.00 la 1.00)

Sistemul rulează 6 verificări de sănătate:
1. Compatibilitatea versiunii Python
2. Statusul repository-ului Git
3. Fișierele necesare există
4. Dependențele sunt instalate
5. Conectivitatea GitHub
6. Spațiul pe disc disponibil

#### Status Token Facebook

Afișează statusul de validitate al token-ului dvs. de pagină Facebook:
- **VALID ✅** (verde) - Token-ul este valid și gata de folosit
- **INVALID/EXPIRED ❌** (roșu) - Token-ul trebuie actualizat
- **NOT FOUND** (portocaliu) - Token-ul nu este configurat

Statusul este verificat automat la pornire. Utilizați **"Refresh Facebook Token"** pentru a-l actualiza.

#### Acțiuni Rapide

**Run Health Check**: Execută toate cele 6 verificări de sănătate și afișează rezultatele.

**Create Backup**: Creează un backup complet al:
- Fișierelor de configurare
- Datelor de tracking asset-uri
- Datelor de programare
- Asset-urilor selectate

Backup-urile sunt salvate în directorul `Backups/` cu timestamp.

**Start Scheduler**: Pornește programatorul de sarcini automate în fundal.

**Stop Scheduler**: Oprește scheduler-ul (activat doar când scheduler-ul rulează).

#### Acțiuni Test

**Postează Text Test**: Postează un mesaj de test pe pagina dvs. Facebook.

**Generează Text Test**: Generează un mesaj AI de test.

#### Loguri Recente

Afișează ultimele 20 linii din `Logs/system.log` pentru referință rapidă.

### Tab Programare (Scheduling)

Tab-ul **Programare** vă permite să gestionați sarcini automate programate.

#### Vizualizarea Job-urilor Programate

Panoul stâng afișează toate job-urile programate într-un tabel:

| Coloană | Descriere |
|--------|-------------|
| **#** | Număr job |
| **Tip** | Tip job (daily, weekly, interval, once) |
| **Ora/Interval** | Specificația de timp sau interval |
| **Task** | Script de executat |
| **Activat** | Status activare (Da/Nu) |
| **Ultima Rulare** | Timestamp ultimei execuții |

#### Adăugarea unui Job Nou

1. Selectați tipul de job din dropdown:
   - **Daily**: Rulează în fiecare zi la o oră specifică
   - **Weekly**: Rulează într-o zi specifică a săptămânii
   - **Interval**: Rulează la fiecare N minute
   - **Once**: Rulează o dată la o dată/oră specifică

2. Completați câmpurile necesare bazate pe tipul de job:

   **Job Zilnic:**
   - **Ora (HH:MM)**: Ora în format 24 de ore (ex: 09:00, 14:30)

   **Job Săptămânal:**
   - **Ziua**: Ziua săptămânii (Monday, Tuesday, etc.)
   - **Ora (HH:MM)**: Ora în format 24 de ore

   **Job cu Interval:**
   - **Interval (minute)**: Numărul de minute între rulări

   **Job O Singură Dată:**
   - **Data și Ora (YYYY-MM-DD HH:MM)**: Dată și oră specifică

3. Introduceți **Task**: Numele fișierului script Python (ex: `auto_post.py`, `auto_generate.py`)

4. Bifați **Activat** dacă doriți ca job-ul să fie activat imediat

5. Faceți clic pe **"Add Job"**

#### Ștergerea unui Job

1. Selectați un job din listă
2. Faceți clic pe **"Delete Selected"**
3. Confirmați ștergerea în dialog

#### Reîmprospătarea Listei

Faceți clic pe **"Refresh List"** pentru a reîncărca job-urile din `Config/schedule.json`.

#### Exemple de Programe

**Post Matinal Zilnic:**
```
Tip: daily
Ora: 09:00
Task: auto_post.py
Activat: Yes
```

**Post Luni Săptămânal:**
```
Tip: weekly
Ziua: monday
Ora: 10:00
Task: auto_post.py
Activat: Yes
```

**Generare Conținut la Fiecare 3 Ore:**
```
Tip: interval
Interval: 180
Task: auto_generate.py
Activat: Yes
```

### Tab Assets

Tab-ul **Assets** gestionează biblioteca dvs. media (imagini și videouri).

#### Vizualizarea Asset-urilor Disponibile

Panoul stâng listează toate fișierele media din:
- `Assets/Images/` - Fișiere imagini (PNG, JPG, JPEG, GIF, BMP, WebP)
- `Assets/Videos/` - Fișiere videouri (MP4, MOV, AVI, MKV, WebM)

Fiecare fișier afișează:
- **Nume Fișier**: Numele fișierului
- **Tip**: Tipul fișierului (Imagine / Video)

#### Preview Imagine

Când selectați o singură imagine, apare un thumbnail de preview în panoul drept. Preview-ul:
- Menține raportul de aspect
- Scalare pentru a se potrivi (max 300x300 pixeli)
- Afișează erori pentru imaginile corupte

**Notă**: Preview-urile pentru videouri nu sunt suportate. Veți vedea "Preview disponibil doar pentru imagini" când selectați videouri.

#### Selectarea Asset-urilor

1. **Selecție Simplă**: Faceți clic pe un fișier pentru a-l selecta și a vedea preview-ul
2. **Selecție Multiplă**: 
   - **Windows/Linux**: Țineți `Ctrl` și faceți clic pe mai multe fișiere
   - **macOS**: Țineți `Command` și faceți clic pe mai multe fișiere
   - Selectați mai multe fișiere prin tragere

3. **Salvarea Selecției**:
   - Faceți clic pe **"Save Selection"**
   - Asset-urile sunt salvate în `selected_assets.json` în rădăcina proiectului
   - Un dialog de confirmare afișează numărul de imagini și videouri salvate

4. **Postarea Asset-urilor Selectate**:
   - Faceți clic pe **"Post Selected Assets"**
   - Confirmați postarea în dialog
   - Asset-urile vor fi postate pe Facebook cu descrieri generate de AI

#### Reîmprospătarea Listei

Faceți clic pe **"Refresh List"** pentru a reîncărca asset-urile din foldere. Utilizați această funcție după:
- Adăugarea de fișiere noi în `Assets/Images/` sau `Assets/Videos/`
- Ștergerea de fișiere din foldere
- Când fișierele nu apar în listă

#### Fluxul de Lucru pentru Selecția Asset-urilor

1. Adăugați fișierele media în foldere `Assets/Images/` sau `Assets/Videos/`
2. Deschideți tab-ul **Assets**
3. Faceți clic pe **"Refresh List"** pentru a vedea fișierele dvs.
4. Selectați fișierele pe care doriți să le postați (utilizați Ctrl/Cmd pentru mai multe)
5. Faceți clic pe **"Save Selection"** pentru a salva selecția dvs.
6. (Opțional) Accesați tab-ul **Generare Text** pentru a genera descrieri
7. Faceți clic pe **"Post Selected Assets"** pentru a posta cu conținut AI generat

### Tab Generare Text (Text Generation)

Tab-ul **Generare Text** folosește OpenAI pentru a genera conținut AI pentru asset-urile dvs. selectate.

#### Introducerea unui Prompt

Prompt-ul spune AI-ului ce tip de conținut să genereze:

**Exemple:**
- "Generează un post Facebook despre importanța tehnologiei în viața de zi cu zi"
- "Creează o descriere captivantă pentru această imagine"
- "Generează un mesaj de plată pentru acest videoclip"

#### Informații Asset

Sub input-ul de prompt, veți vedea:
- Numărul de imagini selectate pentru generarea de descrieri
- Numărul de videouri selectate pentru generarea de text de postare

Aceasta vă ajută să înțelegeți ce va fi generat înainte de a apăsa butonul.

#### Generarea Conținutului

1. Introduceți prompt-ul dvs. în zona de text
2. Examinați informațiile despre asset-uri (X imagini, Y videouri)
3. Faceți clic pe **"Generează Text"**

Sistemul va:
- Procesa fiecare asset selectat individual
- Genera conținut adecvat bazat pe tipul de fișier:
  - **Imagini**: Descrieri detaliate folosind OpenAI Vision API
  - **Videouri**: Text de postare bazat pe numele fișierului și context
- Afișa rezultatele în zona de output
- Salva conținutul generat pentru utilizare ulterioară

#### Vizualizarea Rezultatelor

Conținutul generat apare în zona **"Rezultat Generare"** sub input. Output-ul afișează:
- Text generat pentru fiecare asset
- Status de succes/eșec
- Orice erori întâmpinate

#### Fluxul de Lucru cu Asset-uri

**Flux Complet:**
1. Accesați tab-ul **Assets**
2. Selectați imagini/videouri pe care doriți să le postați
3. Faceți clic pe **"Save Selection"**
4. Accesați tab-ul **Generare Text**
5. Introduceți prompt-ul dvs. (sau lăsați-l implicit)
6. Faceți clic pe **"Generează Text"**
7. Examinați conținutul generat
8. Reveniți la tab-ul **Assets**
9. Faceți clic pe **"Post Selected Assets"** pentru a posta cu conținut AI generat

**Notă**: Sistemul folosește automat conținutul generat cel mai recent la postare.

### Tab Logs

Tab-ul **Logs** oferă acces la logurile sistemului pentru monitorizare și depanare.

#### Vizualizarea Logurilor

Vizualizatorul de loguri afișează conținutul din `Logs/system.log`:
- **Actualizare Automată**: Logurile se actualizează automat la fiecare 5 secunde
- **Actualizare Manuală**: Faceți clic pe **"Refresh Logs"** pentru actualizare imediată
- **Fișiere Mari**: Dacă fișierul de log este foarte mare (1000+ linii), se afișează doar ultimele 1000 linii

#### Conținut Log

Logurile includ:
- Pornirea și închiderea aplicației
- Detalii despre apeluri API (Facebook, OpenAI)
- Mesaje de succes/eșec
- Mesaje de eroare și stack traces
- Execuții de job-uri programate
- Acțiuni GUI și interacțiuni utilizator

#### Utilizarea Logurilor pentru Depanare

**Tipare Comune de Log:**

**Post Reușit:**
```
2025-10-26 10:30:15 - auto_post - INFO - Posting text message...
2025-10-26 10:30:16 - auto_post - INFO - ✓ Post successful! Post ID: page_id_post_id
```

**Eroare API:**
```
2025-10-26 10:30:15 - auto_post - ERROR - API response status: 401
2025-10-26 10:30:15 - auto_post - ERROR - Invalid token
```

**Eroare Rețea:**
```
2025-10-26 10:30:15 - auto_post - ERROR - Connection error: Connection refused
```

Verificați tab-ul **Logs** regulat pentru a monitoriza sănătatea sistemului și pentru a identifica probleme.

---

## Fluxuri de Lucru Comune

### Fluxul de Lucru 1: Postare Imediată cu Descriere AI Generată

**Obiectiv**: Postați o singură imagine sau videoclip imediat cu descriere AI generată.

**Pași**:
1. Adăugați fișierul dvs. media în `Assets/Images/` sau `Assets/Videos/`
2. Deschideți GUI: `python GUI/main_gui.py`
3. Accesați tab-ul **Assets**
4. Faceți clic pe **"Refresh List"**
5. Selectați imaginea/videoclipul dvs.
6. Faceți clic pe **"Save Selection"**
7. Accesați tab-ul **Generare Text**
8. Introduceți un prompt (ex: "Generează un post despre...")
9. Faceți clic pe **"Generează Text"**
10. Așteptați finalizarea generării
11. Reveniți la tab-ul **Assets**
12. Faceți clic pe **"Post Selected Assets"**
13. Confirmați postarea în dialog

**Timp**: 2-3 minute

### Fluxul de Lucru 2: Programare Postări Zilnice cu Rotație Automată

**Obiectiv**: Programați postări automate zilnice care se rotesc prin biblioteca dvs. media.

**Pași**:
1. Adăugați mai multe fișiere media în `Assets/Images/` și/sau `Assets/Videos/`
2. Deschideți GUI
3. Accesați tab-ul **Programare**
4. Adăugați un job zilnic:
   - Tip: `daily`
   - Ora: `09:00` (sau ora dvs. preferată)
   - Task: `auto_post.py`
   - Activat: Yes
   - Faceți clic pe **"Add Job"**
5. Accesați tab-ul **Control/Status**
6. Faceți clic pe **"Start Scheduler"**
7. Sistemul va face automat:
   - Va selecta asset-urile nepostate mai întâi
   - Se va roti la cele mai vechi asset-uri postate când toate sunt postate
   - Va genera descrieri AI pentru fiecare post
   - Va posta pe Facebook la ora programată

**Avansat**: Puteți adăuga mai multe job-uri pentru ore diferite:
- 09:00 - Post matinal
- 14:00 - Post după-amiază
- 18:00 - Post seară

### Fluxul de Lucru 3: Generare Batch și Postare Manuală

**Obiectiv**: Generați descrieri pentru mai multe asset-uri, apoi postați-le manual mai târziu.

**Pași**:
1. Adăugați mai multe asset-uri în foldere
2. Deschideți GUI
3. Accesați tab-ul **Assets**, selectați mai multe fișiere
4. Faceți clic pe **"Save Selection"**
5. Accesați tab-ul **Generare Text**
6. Introduceți un prompt de batch (ex: "Generează post-uri despre...")
7. Faceți clic pe **"Generează Text"**
8. Examinați toate conținuturile generate în zona de output
9. Mai târziu, accesați tab-ul **Assets** și faceți clic pe **"Post Selected Assets"**

Acest flux de lucru separă generarea de postare, oferindu-vă control asupra timing-ului.

---

## Gestionarea Token-urilor Facebook

### Înțelegerea Token-urilor

Aplicația folosește Token-uri de Acces la Pagina Facebook pentru postare:

1. **Token User de Scurtă Durată** (validitate 1 oră)
   - Obținut din Graph API Explorer
   - Folosit pentru schimbul la token cu lungă durată

2. **Token User cu Lungă Durată** (validitate 60 zile)
   - Schimbat din token de scurtă durată
   - Poate fi extins

3. **Token Pagină cu Lungă Durată** (validitate 60 zile, poate fi indefinit)
   - Obținut din token user cu lungă durată
   - Folosit pentru postare pe pagina Facebook
   - Salvat în `.env` ca `FACEBOOK_PAGE_TOKEN`

### Verificarea Statusului Token-ului

**Din GUI:**
1. Deschideți GUI-ul
2. Accesați tab-ul **Control/Status**
3. Verificați panoul **"Facebook Token Status"**:
   - **VALID ✅** - Token-ul funcționează
   - **INVALID/EXPIRED ❌** - Trebuie actualizat
   - **NOT FOUND** - Trebuie configurat

**Din Linia de Comandă:**
```bash
python Scripts/exchange_user_to_page_token.py --check-only
```

Coduri de ieșire:
- `0` - Token-ul este valid
- `1` - Token-ul este invalid/expirat
- `2` - Token-ul nu este găsit

### Actualizarea Token-ului Dvs.

**Din GUI (Recomandat):**
1. Accesați tab-ul **Control/Status**
2. Faceți clic pe **"Refresh Facebook Token"**
3. Se deschide o nouă fereastră de terminal
4. Urmați instrucțiunile:
   - Dacă aveți un token user, lipiți-l când vi se solicită
   - Dacă nu, obțineți unul de la [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
5. Token-ul este salvat automat în `.env`

**Din Linia de Comandă:**
```bash
# Mod interactiv
python Scripts/exchange_user_to_page_token.py

# Mod non-interactiv (dacă aveți token user)
python Scripts/exchange_user_to_page_token.py --user-token YOUR_USER_TOKEN
```

### Expirarea Token-ului

Token-urile de pagină ar trebui să dureze 60 de zile, dar pot expira mai devreme dacă:
- Parola utilizatorului este schimbată
- Utilizatorul revocă permisiunile
- Politicile de securitate Facebook necesită actualizare

**Cea Mai Bună Practică**: Verificați statusul token-ului săptămânal folosind GUI-ul sau comanda `--check-only`.

### Securitatea Token-urilor

**Important**: 
- NU partajați niciodată `FACEBOOK_PAGE_TOKEN`
- NU comiteți-l în controlul versiunilor (este deja în `.gitignore`)
- Păstrați fișierul dvs. `.env` în siguranță
- Nu postați token-ul online sau în forumuri de support

---

## Depanare

### Problema: GUI Nu Pornește

**Simptome**: 
- Mesaj de eroare la rularea `python GUI/main_gui.py`
- Fereastra nu se deschide

**Soluții**:
1. **Verificați versiunea Python**: Rulați `python --version` (ar trebui să fie 3.11+)
2. **Verificați mediul virtual**: Asigurați-vă că este activat (`venv` în prompt)
3. **Reinstalați dependențele**: `pip install -r requirements.txt --force-reinstall`
4. **Verificați logurile**: Căutați în `Logs/system.log` pentru mesaje de eroare

**Eroare: "Module not found"**
```bash
# Soluție: Reinstalați dependențele
pip install -r requirements.txt
```

### Problema: Postarea pe Facebook Eșuează

**Simptome**:
- Postarea eșuează cu "Invalid token" sau "Permission denied"
- Statusul token-ului afișează INVALID

**Soluții**:
1. **Actualizați token-ul**: Utilizați butonul **"Refresh Facebook Token"** din GUI
2. **Verificați permisiunile**: Verificați aceste permisiuni în Graph API Explorer:
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_show_list`
3. **Verificați ID-ul paginii**: Verificați `FACEBOOK_PAGE_ID` în `.env` se potrivește cu pagina dvs.
4. **Verificați token-ul manual**: Rulați `python Scripts/exchange_user_to_page_token.py --check-only`

**Eroare: "OAuthException"**
- Soluție: Token-ul a expirat. Rulați script-ul de actualizare token.

### Problema: Generarea OpenAI Eșuează

**Simptome**:
- Mesaj de eroare la generarea textului
- "API key not found" sau "Rate limit exceeded"

**Soluții**:
1. **Verificați cheia API**: Verificați `OPENAI_API_KEY` în `.env` este corectă
2. **Verificați facturarea**: Asigurați-vă că contul dvs. OpenAI are o metodă de plată activă
3. **Verificați cota**: Verificați că nu ați depășit cota OpenAI
4. **Verificați rețeaua**: Verificați conexiunea la internet
5. **Așteptați și reîncercați**: Dacă sunteți limitați la rată, așteptați câteva minute și încercați din nou

**Eroare: "Rate limit exceeded"**
- Soluție: Acest lucru este normal cu nivelul gratuit. Așteptați 1-2 minute între cereri.

### Problema: Scheduler-ul Nu Rulează Job-uri

**Simptome**:
- Scheduler-ul rulează dar job-urile nu se execută
- Job-urile sunt activate dar nu rulează niciodată

**Soluții**:
1. **Verificați configurația job-ului**: Verificați job-urile din `Config/schedule.json` sunt corecte
2. **Verificați câmpul "enabled"**: Asigurați-vă că `"enabled": true` în configurația job-ului
3. **Verificați formatul timpului**: Verificați că timpul este în formatul corect (HH:MM pentru daily/weekly)
4. **Verificați că fișierul task există**: Fișierul task (ex: `auto_post.py`) trebuie să existe în `Automatizare_Completa/`
5. **Verificați logurile**: Căutați în `Logs/scheduler.log` pentru mesaje de eroare

**Eroare: "Task file not found"**
```bash
# Soluție: Asigurați-vă că fișierul task există
ls Automatizare_Completa/auto_post.py  # Ar trebui să existe
```

### Problema: Asset-urile Nu Se Afișează

**Simptome**:
- Fișiere în foldere dar nu apar în GUI
- "Refresh List" nu actualizează

**Soluții**:
1. **Verificați locațiile fișierelor**: Fișierele trebuie să fie în `Assets/Images/` sau `Assets/Videos/`
2. **Verificați extensiile de fișiere**: Formate suportate:
   - Imagini: PNG, JPG, JPEG, GIF, BMP, WebP
   - Videouri: MP4, MOV, AVI, MKV, WebM
3. **Reîmprospătați manual**: Faceți clic pe butonul **"Refresh List"**
4. **Verificați permisiunile fișierelor**: Asigurați-vă că fișierele sunt citibile (nu blocate)
5. **Verificați numele fișierelor**: Evitați caractere speciale în numele fișierelor

**Eroare: "No files found"**
```bash
# Soluție: Verificați structura de fișiere
Assets/
  Images/
    file1.jpg  # Fișierele ar trebui să fie aici
  Videos/
    file1.mp4
```

### Problema: Erori de Encodare

**Simptome**:
- Mesaje de eroare despre encodare (UTF-8)
- Caractere speciale nu se afișează corect

**Soluții**:
1. **Verificați `.env`**: Asigurați-vă că `PYTHONIOENCODING=utf-8` este setat
2. **Reinstalați**: Rulați `pip install --upgrade pip` și reinstalați pachetele
3. **Verificați conținutul fișierelor**: Asigurați-vă că numele asset-urilor nu au caractere problematice

### Problema: GUI Este Lent sau Se Blochează

**Simptome**:
- GUI devine nerezponsiv
- Butoanele nu răspund
- Fereastra se blochează

**Soluții**:
1. **Închideți alte aplicații**: Eliberați resursele sistemului
2. **Verificați spațiul pe disc**: Asigurați-vă că există suficient spațiu pe disc (500MB+)
3. **Reporniți GUI**: Închideți și redeschideți aplicația
4. **Verificați logurile**: Căutați erori în `Logs/system.log`
5. **Actualizați dependențele**: Rulați `pip install --upgrade -r requirements.txt`

### Obținerea Mai Multor Ajutor

**Verificați Logurile**:
- Log-uri principale: `Logs/system.log`
- Log-uri scheduler: `Logs/scheduler.log`
- Verificare sănătate: `Logs/health_check.json`

**Rulați Verificare Sănătate**:
- Din GUI: Accesați tab-ul **Control/Status**, faceți clic pe **"Run Health Check"**
- Din linia de comandă: `python Automatizare_Completa/health_check.py`

**Validare**:
- Rulați: `python Tests/validation_runner.py`
- Verificați că toate cele 6 verificări de validare trec

---

## Întrebări Frecvente (FAQ)

### Pot posta pe mai multe pagini Facebook?

**În prezent**: Nu, aplicația suportă postarea pe o singură pagină Facebook la un moment dat. Puteți crea instalări separate cu fișiere `.env` diferite pentru mai multe pagini.

**Viitor**: Suportul pentru mai multe pagini poate fi adăugat în versiunile viitoare.

### Cum adaug asset-uri noi?

Copiază pur și simplu fișierele dvs. imagine/video în:
- `Assets/Images/` pentru imagini (PNG, JPG, JPEG, GIF, BMP, WebP)
- `Assets/Videos/` pentru videouri (MP4, MOV, AVI, MKV, WebM)

Apoi faceți clic pe **"Refresh List"** în tab-ul Assets.

### Cât costă API-ul OpenAI?

Verificați prețurile actuale la [OpenAI Pricing](https://openai.com/pricing). Cu modelul implicit `gpt-4o-mini`, costurile sunt de obicei foarte scăzute (sub $0.01 per post).

### Pot folosi propriile descrieri în loc de cele generate de AI?

**În prezent**: Generarea AI este integrată. Descrierile manuale ar necesita editarea conținutului generat înainte de postare.

**Workaround**: Puteți genera descrieri, le copiați într-un editor de text, le modificați, apoi le postați manual prin interfața Facebook.

### Cât de des pot posta?

**Limite Facebook**: 
- Pagini standard: Până la 25 de postări la fiecare 24 de ore
- Pagini verificate: Se aplică limite mai mari

**Cea Mai Bună Practică**: Nu depășiți 3-5 postări pe zi pentru a evita să păreați spam.

### Ce se întâmplă dacă token-ul meu expiră în timp ce scheduler-ul rulează?

Scheduler-ul va eșua job-urile cu erori de token. Logurile vor afișa eroarea. Pentru a rezolva:
1. Opriți scheduler-ul din GUI
2. Faceți clic pe **"Refresh Facebook Token"** în tab-ul Control/Status
3. Reporniți scheduler-ul

### Pot programa postări cu prompturi diferite pentru asset-uri diferite?

**În prezent**: Nu. Sistemul de programare folosește rotația implicită de asset-uri. Pentru prompturi personalizate per asset, generați-le manual în GUI mai întâi.

**Workaround**: Generați conținut diferit pentru selecții diferite de asset-uri, apoi postați-le manual.

### Cum fac backup configurației?

**Automat**: Faceți clic pe **"Create Backup"** în tab-ul Control/Status. Backup-urile sunt salvate în `Backups/` cu timestamp.

**Manual**: Copiați aceste fișiere:
- `.env` (păstrați în siguranță!)
- `Config/schedule.json`
- `Config/asset_tracking.json`
- `selected_assets.json`

### Pot rula scheduler-ul pe un server?

**Da!** Scheduler-ul rulează independent și poate rula pe orice computer sau server care:
- Are Python 3.11+ instalat
- Are fișierul `.env` configurat
- Poate accesa internetul (pentru apeluri API)
- Poate accesa folderele `Assets/`

### Cum opresc toate postările automate?

**Opțiunea 1**: Opriți scheduler-ul
- Din GUI: Tab-ul **Control/Status** → **"Stop Scheduler"**
- Din linia de comandă: Apăsați `Ctrl+C` în terminal

**Opțiunea 2**: Dezactivați toate job-urile
- Editați `Config/schedule.json`
- Setați `"enabled": false` pentru toate job-urile
- Scheduler-ul nu va executa job-urile dezactivate

### Trebuie să las GUI-ul deschis pentru ca scheduler-ul să funcționeze?

**Nu!** Scheduler-ul rulează independent ca proces de fundal. Puteți închide GUI-ul și scheduler-ul va continua să ruleze. Amintiți-vă doar să-l opriți înainte de a închide computerul.

---

## Suport și Actualizări

### Verificarea Versiunii

Rulați verificarea de sănătate pentru a vedea statusul actual al sistemului:
```bash
python Automatizare_Completa/health_check.py
```

### Obținerea Actualizărilor

Când sunt disponibile actualizări:
1. Trageți ultimele schimbări: `git pull`
2. Reinstalați dependențele: `pip install -r requirements.txt --upgrade`
3. Reporniți aplicația

### Raportarea Problemelor

Când raportați probleme, vă rugăm să includeți:
1. Versiunea Python: `python --version`
2. Sistemul de operare și versiunea
3. Mesajele de eroare din `Logs/system.log`
4. Pașii pentru a reproduce problema
5. Rezultatele verificării de sănătate

---

## Apendice: Structura Fișierelor

```
SocialBoost_FB_AutoPoster_v3/
├── Assets/                    # Fișierele dvs. media
│   ├── Images/               # Fișiere imagini (PNG, JPG, etc.)
│   └── Videos/               # Fișiere videouri (MP4, etc.)
├── Automatizare_Completa/    # Scripturi de automatizare
│   ├── auto_post.py          # Postare Facebook
│   ├── auto_generate.py     # Generare conținut AI
│   ├── scheduler.py          # Programator sarcină
│   └── health_check.py       # Monitorizare sănătate sistem
├── Config/                    # Fișiere de configurare
│   ├── schedule.json         # Job-uri programate
│   └── asset_tracking.json   # Istorie postare asset-uri
├── Docs/                     # Documentație
│   ├── README_COMPLETE_SYSTEM.md  # Acest fișier
│   └── CHANGELOG.md          # Istoric versiuni
├── GUI/                      # Aplicație GUI
│   └── main_gui.py           # Fereastră GUI principală
├── Logs/                     # Loguri sistem
│   ├── system.log           # Loguri principale aplicație
│   ├── scheduler.log        # Loguri scheduler
│   └── health_check.json    # Rezultate verificare sănătate
├── Scripts/                  # Scripturi utilitare
│   ├── exchange_user_to_page_token.py  # Management token
│   ├── context_builder.py   # Generare context
│   └── prompt_generator.py  # Template-uri prompt
├── Tests/                    # Suite de teste
│   ├── test_auto_post.py    # Teste postare
│   ├── test_auto_generate.py  # Teste generare
│   ├── validation_runner.py # Runner teste
│   └── test_gui.py          # Teste GUI
├── .env                      # Variabile mediu (creați acesta!)
├── requirements.txt          # Dependențe Python
└── selected_assets.json      # Asset-uri selectate pentru postare
```

---

**Ultima Actualizare**: 26 Octombrie 2025  
**Versiune**: 3.0  
**Status**: Faza 5 - Testare Finală și Validare

Pentru întrebări sau suport, vă rugăm să consultați documentația proiectului sau verificați logurile pentru informații detaliate despre erori.

