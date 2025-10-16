import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import List, Optional

class EmailService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_EMAIL", "votre-email@gmail.com")
        self.sender_password = os.getenv("GMAIL_APP_PASSWORD", "votre_mot_de_passe_app")
        self.sender_name = "Tradalife"
        self.frontend_url = os.environ.get("FRONTEND_URL", "https://app.emergent.host")
    
    async def send_email(
        self, 
        to_email: str, 
        subject: str, 
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send an email"""
        try:
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = f"{self.sender_name} <{self.sender_email}>"
            message["To"] = to_email

            # Add text and HTML parts
            if text_content:
                part1 = MIMEText(text_content, "plain")
                message.attach(part1)
            
            part2 = MIMEText(html_content, "html")
            message.attach(part2)

            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    async def send_welcome_email(self, to_email: str, user_name: str = ""):
        """Send welcome email to new user"""
        subject = "Bienvenue chez Tradalife ! 🎉"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Bienvenue chez Tradalife !</h1>
                </div>
                <div class="content">
                    <p>Bonjour{' ' + user_name if user_name else ''},</p>
                    
                    <p>Nous sommes ravis de vous accueillir dans notre communauté de traders ! 🚀</p>
                    
                    <p>Avec Tradalife, vous avez accès à :</p>
                    <ul>
                        <li>✅ Des formations de qualité professionnelle</li>
                        <li>✅ Des canaux Telegram VIP exclusifs</li>
                        <li>✅ Un support 24/7</li>
                        <li>✅ Une communauté de 4000+ traders</li>
                    </ul>
                    
                    <p>Pour commencer, explorez nos formations et rejoignez-nous !</p>
                    
                    <a href="{self.frontend_url}/boutique" class="button">Découvrir les formations</a>
                    
                    <p>À très bientôt,<br>L'équipe Tradalife</p>
                </div>
                <div class="footer">
                    <p>© 2025 Tradalife. Tous droits réservés.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_purchase_confirmation(self, to_email: str, formation_title: str, amount: float):
        """Send purchase confirmation email with training videos and Telegram links"""
        subject = f"Confirmation d'achat - {formation_title} 🎉"
        
        # Training videos (same for all formations)
        video_formation = "https://drive.google.com/file/d/1qfyBxsWWjWRVeosU68xeZcHMbpYw9gjV/view?usp=sharing"
        video_mt4 = "https://drive.google.com/file/d/147kwnZWmHgAVDzQr09x4ZgcmoxWF4jH1/view?usp=sharing"
        
        # Telegram channels
        telegram_channels = [
            {"name": "GOLD", "link": "https://t.me/+BWpLllZBIpxjMWE5"},
            {"name": "FOREX", "link": "https://t.me/+naLR-gXJl8MzZGJh"},
            {"name": "ACTION", "link": "https://t.me/+GBRYqMdHZ4c0YzYx"},
            {"name": "INDICES", "link": "https://t.me/+Z0h36lgNatQxMjFh"},
            {"name": "CRYPTO", "link": "https://t.me/+7NNOp2XGXcpiMDdh"},
            {"name": "COMMODITÉS", "link": "https://t.me/+MXfEUYj4D2oxZGJh"}
        ]
        
        # Exception: TRADALIFE PREMIUM doesn't have access to ACTION channel
        if "PREMIUM" in formation_title.upper():
            telegram_channels = [ch for ch in telegram_channels if ch["name"] != "ACTION"]
        
        # Build Telegram channels HTML
        telegram_html = ""
        for channel in telegram_channels:
            telegram_html += f"""
            <li style="margin: 10px 0;">
                <strong>{channel["name"]}:</strong> 
                <a href="{channel["link"]}" style="color: #E91E8C; text-decoration: none;">{channel["link"]}</a>
            </li>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .purchase-details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .access-section {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #E91E8C; }}
                .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Paiement confirmé !</h1>
                </div>
                <div class="content">
                    <p>Félicitations ! Votre achat a été effectué avec succès.</p>
                    
                    <div class="purchase-details">
                        <h3>📋 Détails de l'achat</h3>
                        <p><strong>Formation :</strong> {formation_title}</p>
                        <p><strong>Montant :</strong> {amount}€</p>
                    </div>
                    
                    <div class="access-section">
                        <h3>🎥 Vos Vidéos de Formation</h3>
                        <p>Accédez immédiatement à vos vidéos de formation :</p>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin: 10px 0;">
                                <strong>📹 Vidéo de Formation :</strong><br>
                                <a href="{video_formation}" style="color: #E91E8C; text-decoration: none;">{video_formation}</a>
                            </li>
                            <li style="margin: 10px 0;">
                                <strong>📹 Utilisation de MT4 :</strong><br>
                                <a href="{video_mt4}" style="color: #E91E8C; text-decoration: none;">{video_mt4}</a>
                            </li>
                        </ul>
                    </div>
                    
                    <div class="access-section">
                        <h3>💬 Vos Canaux Telegram VIP</h3>
                        <p>Rejoignez nos canaux de signaux exclusifs :</p>
                        <ul style="list-style: none; padding: 0;">
                            {telegram_html}
                        </ul>
                    </div>
                    
                    <h3>📋 Prochaine étape : Vérification KYC</h3>
                    <p>Pour finaliser votre accès complet, veuillez compléter votre vérification d'identité (KYC).</p>
                    
                    <p><strong>Documents requis :</strong></p>
                    <ul>
                        <li>Passeport</li>
                        <li>Carte d'identité (recto-verso)</li>
                        <li>Preuve de résidence</li>
                    </ul>
                    
                    <a href="{self.frontend_url}/dashboard" class="button">Compléter mon KYC</a>
                    
                    <p>Merci pour votre confiance et bienvenue dans la communauté Tradalife ! 🚀</p>
                    
                    <p>L'équipe Tradalife</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_kyc_submitted(self, to_email: str):
        """Send KYC submission confirmation"""
        subject = "Votre KYC a été soumis"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⏳ KYC en cours de vérification</h1>
                </div>
                <div class="content">
                    <p>Nous avons bien reçu vos documents KYC.</p>
                    
                    <p>Notre équipe va les vérifier dans les plus brefs délais (généralement 24-48h).</p>
                    
                    <p>Vous recevrez un email dès que votre compte sera validé.</p>
                    
                    <p>Merci pour votre patience !<br>L'équipe Tradalife</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_kyc_approved(self, to_email: str, user_formations: list = None):
        """Send KYC approval email with access to videos and Telegram"""
        subject = "🎉 Votre KYC est approuvé !"
        
        # Training videos (same for all formations)
        video_formation = "https://drive.google.com/file/d/1qfyBxsWWjWRVeosU68xeZcHMbpYw9gjV/view?usp=sharing"
        video_mt4 = "https://drive.google.com/file/d/147kwnZWmHgAVDzQr09x4ZgcmoxWF4jH1/view?usp=sharing"
        
        # Telegram channels
        telegram_channels = [
            {"name": "GOLD", "link": "https://t.me/+BWpLllZBIpxjMWE5"},
            {"name": "FOREX", "link": "https://t.me/+naLR-gXJl8MzZGJh"},
            {"name": "ACTION", "link": "https://t.me/+GBRYqMdHZ4c0YzYx"},
            {"name": "INDICES", "link": "https://t.me/+Z0h36lgNatQxMjFh"},
            {"name": "CRYPTO", "link": "https://t.me/+7NNOp2XGXcpiMDdh"},
            {"name": "COMMODITÉS", "link": "https://t.me/+MXfEUYj4D2oxZGJh"}
        ]
        
        # Check if user has PREMIUM formation (exclude ACTION channel)
        has_premium = False
        if user_formations:
            has_premium = any("PREMIUM" in formation.upper() for formation in user_formations)
        
        if has_premium:
            telegram_channels = [ch for ch in telegram_channels if ch["name"] != "ACTION"]
        
        # Build Telegram channels HTML
        telegram_html = ""
        for channel in telegram_channels:
            telegram_html += f"""
            <li style="margin: 10px 0;">
                <strong>{channel["name"]}:</strong> 
                <a href="{channel["link"]}" style="color: #E91E8C; text-decoration: none;">{channel["link"]}</a>
            </li>
            """
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .access-section {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #E91E8C; }}
                .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Félicitations !</h1>
                </div>
                <div class="content">
                    <p>Votre compte a été vérifié avec succès !</p>
                    
                    <p>Vous avez maintenant un accès complet à tout votre contenu :</p>
                    
                    <div class="access-section">
                        <h3>🎥 Vos Vidéos de Formation</h3>
                        <ul style="list-style: none; padding: 0;">
                            <li style="margin: 10px 0;">
                                <strong>📹 Vidéo de Formation :</strong><br>
                                <a href="{video_formation}" style="color: #E91E8C; text-decoration: none;">{video_formation}</a>
                            </li>
                            <li style="margin: 10px 0;">
                                <strong>📹 Utilisation de MT4 :</strong><br>
                                <a href="{video_mt4}" style="color: #E91E8C; text-decoration: none;">{video_mt4}</a>
                            </li>
                        </ul>
                    </div>
                    
                    <div class="access-section">
                        <h3>💬 Vos Canaux Telegram VIP</h3>
                        <p>Rejoignez nos canaux de signaux exclusifs :</p>
                        <ul style="list-style: none; padding: 0;">
                            {telegram_html}
                        </ul>
                    </div>
                    
                    <a href="https://edushop-portal.preview.emergentagent.com/dashboard" class="button">Accéder à mon Dashboard</a>
                    
                    <p>Bienvenue dans la communauté Tradalife ! 🚀</p>
                    
                    <p>Bon trading !<br>L'équipe Tradalife</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_kyc_rejected(self, to_email: str, reason: str):
        """Send KYC rejection email"""
        subject = "Votre KYC nécessite des modifications"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .reason {{ background: #fff3cd; padding: 15px; border-left: 4px solid #ffc107; border-radius: 5px; margin: 20px 0; }}
                .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Documents à revoir</h1>
                </div>
                <div class="content">
                    <p>Nous avons examiné vos documents KYC, mais nous avons besoin de modifications.</p>
                    
                    <div class="reason">
                        <strong>Raison :</strong><br>
                        {reason}
                    </div>
                    
                    <p>Veuillez soumettre à nouveau vos documents corrigés.</p>
                    
                    <a href="https://edushop-portal.preview.emergentagent.com/dashboard" class="button">Soumettre à nouveau</a>
                    
                    <p>Notre équipe est disponible pour vous aider si besoin.</p>
                    
                    <p>Cordialement,<br>L'équipe Tradalife</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

# Create singleton instance
email_service = EmailService()