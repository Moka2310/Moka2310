"""
Route pour télécharger le package TRADABOT
"""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
import zipfile
import os
from pathlib import Path
from dependencies import get_current_admin

router = APIRouter(prefix="/api/tradabot", tags=["tradabot-download"])

@router.get("/download-package")
async def download_tradabot_package(admin = Depends(get_current_admin)):
    """
    Télécharge le package complet TRADABOT pour Windows
    Accessible uniquement aux admins
    """
    
    # Utiliser le package déjà créé
    zip_path = Path("/app/TRADABOT_Package.zip")
    
    if not zip_path.exists():
        raise HTTPException(status_code=404, detail="TRADABOT package not found")
    
    # Retourner le fichier
    return FileResponse(
        path=str(zip_path),
        media_type='application/zip',
        filename='TRADABOT_Package.zip',
        headers={
            "Content-Disposition": "attachment; filename=TRADABOT_Package.zip"
        }
    )
