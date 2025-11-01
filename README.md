# 🐍 Python to DOCX Converter - GitHub Edition

O aplicație web care convertește cod Python în documente Word (.docx) și funcționează complet pe GitHub Pages fără backend server.

## ✨ Caracteristici

- ✅ **Rulează complet în browser** - folosește Pyodide (Python în browser)
- ✅ **Zero backend necesar** - funcționează pe GitHub Pages
- ✅ **Suport pentru fișiere .py** - încărcați fișiere Python direct
- ✅ **GitHub Actions workflow** - conversie automată pentru fișiere Python din repository
- ✅ **Interfață modernă și intuitivă**
- ✅ **Descărcare automată** a documentelor generate

## 🚀 Utilizare Rapidă

### Opțiunea 1: Interfață Web (GitHub Pages)

1. Accesați aplicația publicată pe GitHub Pages
2. Fie încărcați un fișier `.py`, fie introduceți cod direct
3. Apăsați "Execută codul și descarcă DOCX"
4. Documentul va fi generat și descărcat automat

### Opțiunea 2: GitHub Actions Workflow

Pentru a converti automat fișiere Python din repository:

#### Metoda A: Manual (workflow_dispatch)

1. Mergi în secțiunea **Actions** din repository
2. Selectează workflow-ul **Python to DOCX Converter**
3. Click pe **Run workflow**
4. Introduce calea către fișierul Python (ex: `example.py`)
5. Workflow-ul va genera DOCX-ul și îl va pune ca artifact

#### Metoda B: Automat la push

Când push-uiți un fișier `.py` în repository, workflow-ul se execută automat.

## 📝 Format Cod Python

Codul Python trebuie să folosească biblioteca `python-docx`:

```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Creăm un document nou
doc = Document()

# Adăugăm titlul
titlu = doc.add_heading('Exemplu de Document', level=0)

# Adăugăm paragraf
p = doc.add_paragraph('Acesta este un paragraf.')
run = p.add_run(' Text formatat.')
run.bold = True
run.font.size = Pt(14)

# NOTĂ: Nu includeți doc.save() - aplicația o face automat!
```

## 🏗️ Structura Proiectului

```
.
├── index.html          # Interfața web principală
├── styles.css          # Stiluri CSS
├── app.js              # Logica JavaScript cu Pyodide
├── .github/
│   └── workflows/
│       └── python-to-docx.yml  # GitHub Actions workflow
└── README.md           # Acest fișier
```

## 🔧 Instalare Locală

Pentru testare locală:

1. Clonează repository-ul:
```bash
git clone https://github.com/me-suzy/Python-to-DOCX-Web-Converter-2.git
cd Python-to-DOCX-Web-Converter-2
```

2. Deschide `index.html` în browser sau folosește un server local:
```bash
# Folosind Python
python -m http.server 8000

# Folosind Node.js
npx serve
```

3. Accesează `http://localhost:8000` în browser

## 📦 Dependențe

Aplicația web nu necesită instalări server-side. Toate dependențele sunt încărcate din CDN:
- **Pyodide** v0.25.1 - Python în browser
- **python-docx** - instalat automat prin Pyodide
- **JSZip** - pentru manipularea arhivelor (opțional)

## 🔄 GitHub Actions Workflow

Workflow-ul `python-to-docx.yml` permite conversia automată:

### Trigger Events:
- **workflow_dispatch**: Execuție manuală cu specificarea fișierului
- **push**: Execuție automată când se push-uiește un fișier `.py`
- **repository_dispatch**: Execuție programată sau API

### Output:
- Documentul DOCX generat este disponibil ca **artifact** în Actions
- La execuție manuală, se creează și un **release** cu documentul

## 🛡️ Limitări și Notă de Securitate

- Codul Python este executat **în browser** (client-side), deci este sigur
- Pyodide rulează într-un mediu izolat în browser
- Nu se trimite cod la server - totul rulează local
- Pentru fișiere mari sau cod complex, poate fi necesar mai mult timp de procesare

## 🤝 Contribuții

Contribuțiile sunt binevenite! Vă rugăm să:

1. Faceți fork la repository
2. Creați un branch pentru feature (`git checkout -b feature/AmazingFeature`)
3. Commit-uiti schimbările (`git commit -m 'Add some AmazingFeature'`)
4. Push la branch (`git push origin feature/AmazingFeature`)
5. Deschideți un Pull Request

## 📄 Licență

Acest proiect este disponibil sub licența MIT. Consultați fișierul LICENSE pentru detalii.

## 🙏 Mulțumiri

- [Pyodide](https://pyodide.org/) - Python în browser
- [python-docx](https://python-docx.readthedocs.io/) - Bibliotecă pentru generarea documentelor Word

## 📞 Suport

Dacă întâmpinați probleme sau aveți întrebări:
- Deschideți un [Issue](https://github.com/me-suzy/Python-to-DOCX-Web-Converter-2/issues) pe GitHub
- Verificați [Actions](https://github.com/me-suzy/Python-to-DOCX-Web-Converter-2/actions) pentru log-uri de eroare

---

**Dezvoltat cu ❤️ pentru comunitatea Python și GitHub**

