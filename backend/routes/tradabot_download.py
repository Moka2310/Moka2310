"""
Route pour télécharger le package TRADABOT
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import zipfile
import os
from pathlib import Path
from dependencies import verify_admin

router = APIRouter(prefix="/api/tradabot", tags=["tradabot-download"])

@router.get("/download-package")
async def download_tradabot_package(admin = Depends(verify_admin)):
    """
    Télécharge le package complet TRADABOT pour Windows
    Accessible uniquement aux admins
    """
    
    # Chemin vers le dossier tradabot-app
    tradabot_dir = Path("/app/tradabot-app")
    
    if not tradabot_dir.exists():
        raise HTTPException(status_code=404, detail="TRADABOT package not found")
    
    # Créer un fichier ZIP temporaire
    zip_path = Path("/tmp/TRADABOT_Package.zip")
    
    # Créer le ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Parcourir tous les fichiers
        for root, dirs, files in os.walk(tradabot_dir):
            # Ignorer certains dossiers
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'dist', 'build', 'logs', 'data']]
            
            for file in files:
                if file.endswith(('.py', '.txt', '.md', '.bat', '.ico')):
                    file_path = Path(root) / file
                    # Ajouter au ZIP avec le chemin relatif
                    arcname = file_path.relative_to(tradabot_dir.parent)
                    zipf.write(file_path, arcname)
    
    # Retourner le fichier
    return FileResponse(
        path=str(zip_path),
        media_type='application/zip',
        filename='TRADABOT_Package.zip',
        headers={
            "Content-Disposition": "attachment; filename=TRADABOT_Package.zip"
        }
    )

@router.get("/package-info")
async def get_package_info():
    """
    Retourne les informations sur le package TRADABOT
    """
    return {
        "version": "1.0.0",
        "size_estimate": "5-10 MB",
        "platform": "Windows 10/11",
        "requirements": [
            "Python 3.11+",
            "MetaTrader 4 ou 5",
            "Compte tradalife.com avec accès TRADABOT"
        ],
        "files_included": [
            "Code source complet",
            "Scripts de build",
            "Documentation",
            "Guide d'installation"
        ]
    }
