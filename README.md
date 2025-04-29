# Python-to-DOCX Web Converter 2.0

## Descriere
O aplicație web simplificată pentru execuția codului Python care generează documente Word (.docx). Această versiune îmbunătățită oferă o interfață mai intuitivă și focusată exclusiv pe conversia Python la documente Word prin execuție directă.

## Caracteristici
- Interfață web simplă și intuitivă
- Execuție directă a codului Python care generează documente Word
- Descărcare automată a documentului generat
- Interfață curată cu instrucțiuni clare pentru utilizatori
- Gestionare robustă a erorilor

## Tehnologii utilizate
- Python 3.x
- Flask (framework web)
- python-docx (generare documente Word)
- HTML, CSS și JavaScript (interfața utilizator)

## Cerințe
```
flask
python-docx
```

## Instalare și utilizare
1. Clonați acest repository
2. Instalați dependențele:
   ```
   pip install flask python-docx
   ```
3. Rulați aplicația in folderul:
   ```
   python app.py
   ```

1. Intri in directorul in care ai aplicatia  app.py
2. Deschizi CMD in director si scrii    python app.py
3. Trebuie sa iti apara sa ceva in CMD:
4. 
	- Deschideți browserul web
	- Accesați aplicația în browser la adresa: http://127.0.0.1:5001 sau alternativa  http://127.0.0.1:5000
	- Veți vedea interfața web a aplicației de conversie a codului Python în documente Word
	- Puteți introduce cod Python, încărca exemplul sau șterge conținutul

## Structura proiectului
- `app.py` - Serverul Flask care gestionează rutele și execuția codului Python
- `templates/index.html` - Interfața web pentru introducerea și execuția codului

## Cum funcționează
1. Utilizatorul copiază și inserează codul Python în textarea
2. Codul trebuie să utilizeze biblioteca python-docx pentru a genera un document Word
3. La apăsarea butonului "Execută codul și descarcă rezultatul", serverul:
   - Modifică codul pentru a salva documentul într-o locație temporară
   - Execută codul Python în siguranță
   - Trimite documentul generat înapoi utilizatorului pentru descărcare

## Exemplu de cod Python pentru utilizare
```python
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Creăm un document nou
doc = Document()

# Adăugăm titlul
titlu = doc.add_heading('Exemplu de Document Simplu', level=0)
titlu.alignment = WD_ALIGN_PARAGRAPH.CENTER

# Adăugăm primul paragraf
p1 = doc.add_paragraph('Acesta este primul paragraf al documentului. ')
run1 = p1.add_run('Această parte este formatată diferit.')
run1.bold = True
run1.font.size = Pt(14)
run1.font.color.rgb = RGBColor(0, 0, 255)  # Albastru

# Adăugăm al doilea paragraf
p2 = doc.add_paragraph('Acesta este al doilea paragraf. ')
run2 = p2.add_run('Folosim un alt font aici.')
run2.italic = True
run2.font.name = 'Arial'
run2.font.size = Pt(12)
run2.font.color.rgb = RGBColor(255, 0, 0)  # Roșu

# Salvăm documentul
doc.save('document_simplu.docx')
```

## Îmbunătățiri în versiunea 2.0
- Interfață mai curată și simplificată
- Eliminarea funcționalităților redundante
- Flux de lucru optimizat pentru utilizatori
- Instrucțiuni mai clare pentru utilizare
- Design responsiv și modern
- Gestionare mai robustă a erorilor de execuție
- Tratarea inteligentă a căilor de fișiere în codul Python

## Notă de securitate
Această aplicație execută cod Python arbitrar pe server. Utilizați-o doar în medii sigure și controlate. Nu este recomandată expunerea acestei aplicații pe internet fără măsuri suplimentare de securitate.

## Contribuții
Contribuțiile sunt binevenite! Vă rugăm să creați un "fork" al acestui repository și să trimiteți un "pull request" cu îmbunătățirile propuse.

## Licență
Acest proiect este disponibil sub licența MIT. Consultați fișierul LICENSE pentru detalii.

---

*Notă: Această aplicație este concepută pentru uz educațional și demonstrativ. Este ideală pentru generarea rapidă a documentelor Word folosind Python, fără a necesita instalarea bibliotecilor sau a mediului de dezvoltare pe computerul utilizatorului.*
