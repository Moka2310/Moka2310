"""
Route publique pour télécharger TRADABOT
"""
from fastapi import APIRouter
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(prefix="/api", tags=["download"])

@router.get("/download-tradabot")
async def download_tradabot():
    """
    Télécharge le package TRADABOT
    Route PUBLIQUE - pas besoin d'être connecté
    """
    
    zip_path = Path("/app/TRADABOT_Package.zip")
    
    if not zip_path.exists():
        return {"error": "Package not found"}
    
    return FileResponse(
        path=str(zip_path),
        media_type='application/zip',
        filename='TRADABOT_Package.zip',
        headers={
            "Content-Disposition": "attachment; filename=TRADABOT_Package.zip"
        }
    )
