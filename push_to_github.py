"""
Script Python pentru push automat pe GitHub
- Creează (dacă lipsește) repository-ul pe GitHub prin API
- Face commit și push pe branch-ul main
"""

import subprocess
import os
import sys
from pathlib import Path
import json
import urllib.request
import urllib.error
import base64

# Fix encoding pentru Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# ========================================
# CONFIGURARE
# ========================================
USER_GITHUB = "me-suzy"
TOKEN_GITHUB = "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"
REPO_NAME = "Python-to-DOCX-Web-Converter-2"
REPO_OWNER = "me-suzy"
PRIVATE_REPO = False
REPO_DESCRIPTION = "O aplicație web pentru conversia codului Python în documente Word (.docx) - funcționează pe GitHub Pages"
# ========================================

def check_repo_exists():
    """Verifică dacă repository-ul există pe GitHub."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", f"token {TOKEN_GITHUB}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    
    try:
        with urllib.request.urlopen(req) as response:
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return False
        raise

def create_repo():
    """Creează repository-ul pe GitHub dacă nu există."""
    if check_repo_exists():
        print(f"✅ Repository-ul {REPO_NAME} există deja pe GitHub.")
        return True
    
    url = "https://api.github.com/user/repos"
    data = {
        "name": REPO_NAME,
        "description": REPO_DESCRIPTION,
        "private": PRIVATE_REPO,
        "auto_init": False
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'))
    req.add_header("Authorization", f"token {TOKEN_GITHUB}")
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("Content-Type", "application/json")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"✅ Repository-ul {REPO_NAME} a fost creat cu succes!")
            return True
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8')
        print(f"❌ Eroare la crearea repository-ului: {error_msg}")
        return False

def run_command(cmd, cwd=None, check=True):
    """Execută o comandă shell și returnează output-ul."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if check and result.returncode != 0:
            print(f"❌ Eroare la execuția comenzii: {cmd}")
            print(f"Output: {result.stdout}")
            print(f"Error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Excepție la execuția comenzii {cmd}: {e}")
        return None

def init_git_repo():
    """Inițializează repository-ul Git local."""
    repo_dir = Path(__file__).parent
    
    # Verifică dacă .git există deja
    if (repo_dir / ".git").exists():
        print("✅ Repository Git există deja.")
        return True
    
    # Inițializează Git
    print("📦 Inițializez repository-ul Git...")
    run_command("git init", cwd=repo_dir)
    run_command('git config user.name "me-suzy"', cwd=repo_dir)
    run_command('git config user.email "me-suzy@users.noreply.github.com"', cwd=repo_dir)
    
    return True

def add_and_commit():
    """Adaugă fișierele și face commit."""
    repo_dir = Path(__file__).parent
    
    print("📝 Adaug fișierele...")
    run_command("git add .", cwd=repo_dir)
    
    print("💾 Fac commit...")
    result = run_command('git commit -m "Initial commit: Python to DOCX Converter with GitHub Pages support"', cwd=repo_dir, check=False)
    
    if result is None:
        # Verifică dacă există deja commit-uri
        status = run_command("git status --porcelain", cwd=repo_dir)
        if not status:
            print("ℹ️  Nu există modificări de commit.")
            return True
        else:
            print("❌ Eroare la commit.")
            return False
    
    return True

def push_to_github():
    """Face push pe GitHub."""
    repo_dir = Path(__file__).parent
    
    # Configurează remote
    remote_url = f"https://{TOKEN_GITHUB}@github.com/{REPO_OWNER}/{REPO_NAME}.git"
    
    # Verifică dacă remote-ul există
    remotes = run_command("git remote -v", cwd=repo_dir)
    if "origin" not in (remotes or ""):
        print("🔗 Adaug remote-ul origin...")
        run_command(f'git remote add origin {remote_url}', cwd=repo_dir)
    else:
        print("🔗 Actualizez remote-ul origin...")
        run_command(f'git remote set-url origin {remote_url}', cwd=repo_dir)
    
    # Push pe main
    print("🚀 Fac push pe GitHub...")
    result = run_command("git push -u origin main", cwd=repo_dir, check=False)
    
    if result is None:
        # Încearcă să verifice dacă există branch-ul main
        branches = run_command("git branch", cwd=repo_dir)
        if "main" not in (branches or ""):
            # Creează branch-ul main
            run_command("git branch -M main", cwd=repo_dir)
            result = run_command("git push -u origin main", cwd=repo_dir, check=False)
    
    if result is not None:
        print("✅ Push realizat cu succes!")
        print(f"🔗 Repository: https://github.com/{REPO_OWNER}/{REPO_NAME}")
        return True
    else:
        print("❌ Eroare la push. Verifică log-urile de mai sus.")
        return False

def main():
    """Funcția principală."""
    print("=" * 60)
    print("🚀 PUSH PE GITHUB - Python to DOCX Converter")
    print("=" * 60)
    print()
    
    # Creează repository-ul pe GitHub
    print("1️⃣  Verific și creez repository-ul pe GitHub...")
    if not create_repo():
        print("❌ Nu s-a putut crea repository-ul. Opresc.")
        return
    
    # Inițializează Git local
    print("\n2️⃣  Inițializez repository-ul Git local...")
    if not init_git_repo():
        print("❌ Nu s-a putut inițializa Git. Opresc.")
        return
    
    # Adaugă și commit
    print("\n3️⃣  Adaug fișierele și fac commit...")
    if not add_and_commit():
        print("⚠️  Eroare la commit, dar continui...")
    
    # Push pe GitHub
    print("\n4️⃣  Fac push pe GitHub...")
    if not push_to_github():
        print("❌ Nu s-a putut face push.")
        return
    
    print("\n" + "=" * 60)
    print("✅ FINALIZAT CU SUCCES!")
    print("=" * 60)
    print(f"🌐 Repository URL: https://github.com/{REPO_OWNER}/{REPO_NAME}")
    print(f"📄 GitHub Pages (după activare): https://{REPO_OWNER}.github.io/{REPO_NAME}/")
    print()
    print("📋 Pași următori:")
    print("   1. Accesează repository-ul pe GitHub")
    print("   2. Mergi la Settings → Pages")
    print("   3. Selectează branch-ul 'main' și folderul '/ (root)'")
    print("   4. Salvează - aplicația va fi disponibilă pe GitHub Pages!")

if __name__ == "__main__":
    main()

