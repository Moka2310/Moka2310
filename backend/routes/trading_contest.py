"""
Routes pour le concours de trading
"""
from fastapi import APIRouter, HTTPException, Depends
from models import TradingContestParticipant, TradingContestCreate, TradingContestUpdate, TradingContestResponse, User
from dependencies import get_db, get_current_user, require_admin
from datetime import datetime
import uuid
import logging

router = APIRouter(prefix="/trading-contest", tags=["Trading Contest"])
logger = logging.getLogger(__name__)

def calculate_win_rate(winning_trades: int, total_trades: int) -> float:
    """Calculer le pourcentage de réussite: Trades gagnants / Total trades × 100"""
    if total_trades == 0:
        return 0.0
    return round((winning_trades / total_trades) * 100, 2)

async def recalculate_rankings(db):
    """Recalculer les classements de tous les participants actifs"""
    # Récupérer tous les participants actifs
    participants = await db.trading_contest.find({"isActive": True}).to_list(1000)
    
    # Trier par winRate décroissant
    participants_sorted = sorted(participants, key=lambda x: x.get('winRate', 0), reverse=True)
    
    # Attribuer les rangs
    for rank, participant in enumerate(participants_sorted, start=1):
        await db.trading_contest.update_one(
            {"id": participant["id"]},
            {"$set": {"rank": rank, "updatedAt": datetime.utcnow()}}
        )
    
    logger.info(f"✅ Rankings recalculated for {len(participants_sorted)} participants")

@router.get("/participants", response_model=list[TradingContestResponse])
async def get_all_participants():
    """
    Récupérer tous les participants actifs du concours (PUBLIC)
    Triés par classement
    """
    db = get_db()
    
    try:
        participants = await db.trading_contest.find(
            {"isActive": True}
        ).sort("rank", 1).to_list(1000)
        
        return [TradingContestResponse(**p) for p in participants]
    except Exception as e:
        logger.error(f"❌ Error fetching participants: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des participants")

@router.post("/admin/add", dependencies=[Depends(require_admin)])
async def add_participant(
    participant_data: TradingContestCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Ajouter un participant au concours (ADMIN ONLY)
    Le pourcentage et le classement sont calculés automatiquement
    """
    db = get_db()
    
    try:
        # Valider les données
        if participant_data.totalTrades < 0 or participant_data.winningTrades < 0:
            raise HTTPException(status_code=400, detail="Les nombres de trades ne peuvent pas être négatifs")
        
        if participant_data.winningTrades > participant_data.totalTrades:
            raise HTTPException(status_code=400, detail="Le nombre de trades gagnants ne peut pas dépasser le total")
        
        # Calculer le win rate
        win_rate = calculate_win_rate(participant_data.winningTrades, participant_data.totalTrades)
        
        # Créer le participant
        participant = TradingContestParticipant(
            id=str(uuid.uuid4()),
            firstName=participant_data.firstName,
            lastName=participant_data.lastName,
            totalTrades=participant_data.totalTrades,
            winningTrades=participant_data.winningTrades,
            winRate=win_rate,
            date=participant_data.date,
            rank=0,  # Sera recalculé
            isActive=True,
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        await db.trading_contest.insert_one(participant.dict())
        
        # Recalculer les classements
        await recalculate_rankings(db)
        
        logger.info(f"✅ Participant added: {participant.firstName} {participant.lastName} - {win_rate}%")
        
        return {
            "success": True,
            "message": "Participant ajouté avec succès",
            "participant": TradingContestResponse(**participant.dict())
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error adding participant: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'ajout: {str(e)}")

@router.put("/admin/update/{participant_id}", dependencies=[Depends(require_admin)])
async def update_participant(
    participant_id: str,
    update_data: TradingContestUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Modifier un participant (ADMIN ONLY)
    Le pourcentage et le classement sont recalculés automatiquement
    """
    db = get_db()
    
    try:
        participant = await db.trading_contest.find_one({"id": participant_id})
        
        if not participant:
            raise HTTPException(status_code=404, detail="Participant introuvable")
        
        # Préparer les mises à jour
        update_dict = {"updatedAt": datetime.utcnow()}
        
        if update_data.firstName is not None:
            update_dict["firstName"] = update_data.firstName
        if update_data.lastName is not None:
            update_dict["lastName"] = update_data.lastName
        if update_data.date is not None:
            update_dict["date"] = update_data.date
        if update_data.isActive is not None:
            update_dict["isActive"] = update_data.isActive
        
        # Si les trades sont modifiés, recalculer le win rate
        if update_data.totalTrades is not None or update_data.winningTrades is not None:
            total_trades = update_data.totalTrades if update_data.totalTrades is not None else participant["totalTrades"]
            winning_trades = update_data.winningTrades if update_data.winningTrades is not None else participant["winningTrades"]
            
            if total_trades < 0 or winning_trades < 0:
                raise HTTPException(status_code=400, detail="Les nombres de trades ne peuvent pas être négatifs")
            
            if winning_trades > total_trades:
                raise HTTPException(status_code=400, detail="Le nombre de trades gagnants ne peut pas dépasser le total")
            
            update_dict["totalTrades"] = total_trades
            update_dict["winningTrades"] = winning_trades
            update_dict["winRate"] = calculate_win_rate(winning_trades, total_trades)
        
        # Mettre à jour
        await db.trading_contest.update_one(
            {"id": participant_id},
            {"$set": update_dict}
        )
        
        # Recalculer les classements
        await recalculate_rankings(db)
        
        logger.info(f"✅ Participant updated: {participant_id}")
        
        return {
            "success": True,
            "message": "Participant modifié avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating participant: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la modification: {str(e)}")

@router.delete("/admin/delete/{participant_id}", dependencies=[Depends(require_admin)])
async def delete_participant(
    participant_id: str,
    current_user: User = Depends(get_current_user)
):
    """
    Supprimer un participant (ADMIN ONLY)
    """
    db = get_db()
    
    try:
        result = await db.trading_contest.delete_one({"id": participant_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Participant introuvable")
        
        # Recalculer les classements
        await recalculate_rankings(db)
        
        logger.info(f"✅ Participant deleted: {participant_id}")
        
        return {
            "success": True,
            "message": "Participant supprimé avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting participant: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")

@router.get("/admin/all", dependencies=[Depends(require_admin)])
async def get_all_participants_admin(current_user: User = Depends(get_current_user)):
    """
    Récupérer tous les participants (actifs et inactifs) pour l'admin
    """
    db = get_db()
    
    try:
        participants = await db.trading_contest.find({}).sort("rank", 1).to_list(1000)
        return participants
    except Exception as e:
        logger.error(f"❌ Error fetching all participants: {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de la récupération des participants")
