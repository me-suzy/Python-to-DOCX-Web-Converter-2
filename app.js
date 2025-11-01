let pyodide = null;
let isLoading = false;

// Exemplu de cod Python
const EXAMPLE_CODE = `from docx import Document
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

# Notă: Nu includeți doc.save() - aplicația o face automat`;

// Inițializare Pyodide
async function initializePyodide() {
    if (pyodide) return pyodide;
    
    showStatus('⏳ Se încarcă Pyodide (Python în browser)...', 'info');
    
    try {
        pyodide = await loadPyodide({
            indexURL: "https://cdn.jsdelivr.net/pyodide/v0.25.1/full/"
        });
        
        // Instalăm python-docx folosind micropip
        showStatus('📦 Se instalează biblioteca python-docx...', 'info');
        await pyodide.loadPackage("micropip");
        const micropip = pyodide.pyimport("micropip");
        await micropip.install("python-docx");
        
        showStatus('✅ Pyodide încărcat cu succes!', 'success');
        setTimeout(() => hideStatus(), 3000);
        
        return pyodide;
    } catch (error) {
        showError('Eroare la inițializarea Pyodide: ' + error.message);
        throw error;
    }
}

// Afișare mesaj de status
function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('statusMessage');
    statusEl.textContent = message;
    statusEl.className = `status-message ${type}`;
    statusEl.style.display = 'block';
}

function hideStatus() {
    const statusEl = document.getElementById('statusMessage');
    statusEl.style.display = 'none';
}

// Afișare eroare
function showError(message) {
    const errorBox = document.getElementById('errorBox');
    errorBox.textContent = message;
    errorBox.style.display = 'block';
    hideStatus();
}

function hideError() {
    const errorBox = document.getElementById('errorBox');
    errorBox.style.display = 'none';
}

// Procesare cod Python și generare DOCX
async function executePythonCode() {
    if (isLoading) return;
    
    const code = document.getElementById('pythonCode').value.trim();
    if (!code) {
        showError('Vă rugăm introduceți cod Python!');
        return;
    }
    
    isLoading = true;
    const executeBtn = document.getElementById('executeBtn');
    const btnText = document.getElementById('btnText');
    const spinner = document.getElementById('loadingSpinner');
    
    executeBtn.disabled = true;
    btnText.style.display = 'none';
    spinner.style.display = 'inline-block';
    hideError();
    hideStatus();
    
    try {
        // Inițializăm Pyodide dacă nu este deja făcut
        if (!pyodide) {
            await initializePyodide();
        }
        
        showStatus('🔄 Se execută codul Python...', 'info');
        
        // Pregătim codul: eliminăm orice linii de save și adăugăm logica de generare DOCX în memorie
        let processedCode = code;
        
        // Eliminăm linii care salvează fișierul (pattern matching pentru doc.save)
        processedCode = processedCode.replace(/doc\.save\([^)]+\)/gi, '');
        processedCode = processedCode.replace(/document\.save\([^)]+\)/gi, '');
        
        // Adăugăm cod pentru a genera DOCX în memorie
        const wrapperCode = `
import io
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

# Codul utilizatorului
${processedCode}

# Generăm DOCX în memorie
output = io.BytesIO()
doc.save(output)
output.seek(0)

# Returnăm conținutul ca bytes
docx_bytes = output.getvalue()
`;
        
        // Executăm codul
        pyodide.runPython(wrapperCode);
        
        // Obținem bytes-ul documentului
        const docxBytes = pyodide.runPython('docx_bytes');
        const bytes = new Uint8Array(docxBytes.toJs());
        
        // Creăm și descărcăm fișierul
        const blob = new Blob([bytes], { 
            type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' 
        });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'document_generat.docx';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
        
        showStatus('✅ Documentul a fost generat și descărcat cu succes!', 'success');
        setTimeout(() => hideStatus(), 5000);
        
    } catch (error) {
        console.error('Eroare la executare:', error);
        let errorMessage = error.toString();
        if (error.message) {
            errorMessage = error.message;
        }
        showError(`Eroare la executarea codului:\n\n${errorMessage}\n\nVă rugăm verificați codul și încercați din nou.`);
    } finally {
        isLoading = false;
        executeBtn.disabled = false;
        btnText.style.display = 'inline';
        spinner.style.display = 'none';
    }
}

// Încărcare fișier .py
function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!file.name.endsWith('.py')) {
        showError('Vă rugăm încărcați un fișier .py!');
        return;
    }
    
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('pythonCode').value = e.target.result;
        hideError();
        showStatus('✅ Fișier încărcat cu succes!', 'success');
        setTimeout(() => hideStatus(), 3000);
    };
    reader.readAsText(file);
}

// Evenimente
document.addEventListener('DOMContentLoaded', async () => {
    // Inițializare Pyodide în background
    initializePyodide().catch(err => {
        console.error('Eroare inițializare:', err);
    });
    
    document.getElementById('executeBtn').addEventListener('click', executePythonCode);
    document.getElementById('uploadBtn').addEventListener('click', () => {
        document.getElementById('fileInput').click();
    });
    document.getElementById('fileInput').addEventListener('change', handleFileUpload);
    document.getElementById('exampleBtn').addEventListener('click', () => {
        document.getElementById('pythonCode').value = EXAMPLE_CODE;
        hideError();
    });
    document.getElementById('clearBtn').addEventListener('click', () => {
        document.getElementById('pythonCode').value = '';
        hideError();
        hideStatus();
    });
});

