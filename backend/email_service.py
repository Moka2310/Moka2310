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
                    
                    <a href="{self.frontend_url}/dashboard" class="button">Accéder à mon Dashboard</a>
                    
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
                    
                    <a href="{self.frontend_url}/dashboard" class="button">Soumettre à nouveau</a>
                    
                    <p>Notre équipe est disponible pour vous aider si besoin.</p>
                    
                    <p>Cordialement,<br>L'équipe Tradalife</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

    async def send_account_deletion_confirmation(self, to_email: str, user_name: str):
        """Send account deletion confirmation email (GDPR compliance)"""
        subject = "Confirmation de suppression de votre compte Tradalife"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✓ Suppression de compte confirmée</h1>
                </div>
                <div class="content">
                    <p>Bonjour {user_name},</p>
                    
                    <p>Nous confirmons que votre compte Tradalife et toutes vos données associées ont été <strong>définitivement supprimés</strong> de nos systèmes.</p>
                    
                    <div class="info-box">
                        <strong>📋 Données supprimées :</strong>
                        <ul>
                            <li>Informations de compte</li>
                            <li>Documents KYC</li>
                            <li>Historique d'achats</li>
                            <li>Témoignages soumis</li>
                            <li>Toutes données personnelles</li>
                        </ul>
                    </div>
                    
                    <p><strong>Important :</strong> Cette action est irréversible. Si vous souhaitez utiliser nos services à l'avenir, vous devrez créer un nouveau compte.</p>
                    
                    <p>Nous sommes désolés de vous voir partir et espérons vous revoir bientôt.</p>
                    
                    <p>Si cette suppression n'a pas été initiée par vous, veuillez nous contacter immédiatement.</p>
                    
                    <p>Cordialement,<br>L'équipe Tradalife</p>
                </div>
                <div class="footer">
                    <p>Conformément au RGPD (Règlement Général sur la Protection des Données)</p>
                    <p>© 2025 Tradalife - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_subscription_confirmation(self, to_email: str):
        """Send subscription confirmation email"""
        subject = "✓ Bienvenue - Votre abonnement aux signaux TRADALIFE est activé !"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .success-box {{ background: #d4edda; border-left: 4px solid #28a745; padding: 15px; margin: 20px 0; }}
                .feature {{ background: white; padding: 15px; margin: 10px 0; border-radius: 8px; border-left: 3px solid #7B3FF2; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Abonnement Activé !</h1>
                </div>
                <div class="content">
                    <div class="success-box">
                        <strong>✓ Votre paiement a été traité avec succès !</strong>
                        <p style="margin: 5px 0 0 0;">Vous avez maintenant accès à tous nos signaux de trading.</p>
                    </div>
                    
                    <h2 style="color: #7B3FF2;">📊 Ce que vous obtenez :</h2>
                    
                    <div class="feature">
                        <strong>💹 Signaux en temps réel</strong>
                        <p>Forex, Crypto, Indices, Gold, et plus encore</p>
                    </div>
                    
                    <div class="feature">
                        <strong>📱 Accès aux canaux Telegram privés</strong>
                        <p>Rejoignez notre communauté de traders professionnels</p>
                    </div>
                    
                    <div class="feature">
                        <strong>🔔 Notifications instantanées</strong>
                        <p>Ne ratez aucune opportunité de trading</p>
                    </div>
                    
                    <div class="feature">
                        <strong>📈 Analyses de marché</strong>
                        <p>Décisions basées sur des analyses professionnelles</p>
                    </div>
                    
                    <p style="margin-top: 20px;"><strong>📝 Prochaines étapes :</strong></p>
                    <ol>
                        <li>Connectez-vous à votre Dashboard</li>
                        <li>Cliquez sur "Obtenir le lien Telegram"</li>
                        <li>Rejoignez les canaux de signaux</li>
                        <li>Commencez à recevoir nos signaux !</li>
                    </ol>
                    
                    <div style="text-align: center;">
                        <a href="{self.frontend_url}/dashboard" class="cta-button">Accéder au Dashboard</a>
                    </div>
                    
                    <p style="margin-top: 30px;"><strong>💳 Renouvellement automatique :</strong></p>
                    <p>Votre abonnement se renouvellera automatiquement chaque mois à 150$. Vous pouvez annuler à tout moment depuis votre Dashboard.</p>
                    
                    <p style="margin-top: 20px;">Besoin d'aide ? Notre équipe est disponible 24/7 sur Telegram.</p>
                    
                    <p>Bon trading !<br><strong>L'équipe TRADALIFE</strong></p>
                </div>
                <div class="footer">
                    <p>Abonnement : 150$ / mois | Renouvellement automatique</p>
                    <p>© 2025 TRADALIFE - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_payment_failed_reminder(self, to_email: str):
        """Send payment failed reminder email"""
        subject = "⚠️ Échec de paiement - Action requise pour votre abonnement TRADALIFE"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .warning-box {{ background: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 20px 0; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>⚠️ Échec de Paiement</h1>
                </div>
                <div class="content">
                    <p>Bonjour,</p>
                    
                    <div class="warning-box">
                        <strong>⚠️ Nous n'avons pas pu traiter votre paiement mensuel</strong>
                        <p style="margin: 5px 0 0 0;">Votre abonnement aux signaux TRADALIFE est en attente de paiement.</p>
                    </div>
                    
                    <p><strong>Ce qui se passe maintenant :</strong></p>
                    <ul>
                        <li>✓ Vous conservez l'accès pour encore <strong>3 jours</strong></li>
                        <li>⚠️ Après 3 jours, votre accès sera suspendu</li>
                        <li>❌ Vous serez retiré des canaux Telegram privés</li>
                    </ul>
                    
                    <p><strong>Raisons possibles :</strong></p>
                    <ul>
                        <li>Carte expirée ou invalide</li>
                        <li>Fonds insuffisants</li>
                        <li>Problème avec votre banque</li>
                    </ul>
                    
                    <p><strong>Comment résoudre :</strong></p>
                    <ol>
                        <li>Vérifiez les informations de votre carte</li>
                        <li>Assurez-vous d'avoir des fonds suffisants</li>
                        <li>Mettez à jour votre méthode de paiement dans le Dashboard</li>
                    </ol>
                    
                    <div style="text-align: center;">
                        <a href="{self.frontend_url}/dashboard" class="cta-button">Mettre à jour le paiement</a>
                    </div>
                    
                    <p style="margin-top: 30px;"><strong>Besoin d'aide ?</strong></p>
                    <p>Notre équipe support est disponible 24/7 pour vous aider. Contactez-nous sur Telegram ou par email.</p>
                    
                    <p>Cordialement,<br><strong>L'équipe TRADALIFE</strong></p>
                </div>
                <div class="footer">
                    <p>Abonnement : 150$ / mois</p>
                    <p>© 2025 TRADALIFE - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)
    
    async def send_subscription_canceled(self, to_email: str, end_date: str):
        """Send subscription cancellation confirmation email"""
        subject = "Confirmation d'annulation de votre abonnement TRADALIFE"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #6c757d 0%, #495057 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .info-box {{ background: #d1ecf1; border-left: 4px solid #0c5460; padding: 15px; margin: 20px 0; }}
                .cta-button {{ display: inline-block; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 15px 30px; text-decoration: none; border-radius: 25px; margin: 20px 0; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; color: #666; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Annulation d'abonnement</h1>
                </div>
                <div class="content">
                    <p>Bonjour,</p>
                    
                    <p>Nous avons bien reçu votre demande d'annulation d'abonnement.</p>
                    
                    <div class="info-box">
                        <strong>ℹ️ Information importante :</strong>
                        <p style="margin: 10px 0 0 0;">Vous conserverez l'accès à tous les signaux jusqu'au <strong>{end_date}</strong></p>
                        <p style="margin: 5px 0 0 0;">Aucun prélèvement ne sera effectué après cette date.</p>
                    </div>
                    
                    <p><strong>Ce qui se passe ensuite :</strong></p>
                    <ul>
                        <li>✓ Vous gardez l'accès complet jusqu'à la fin de votre période</li>
                        <li>❌ Aucun renouvellement automatique</li>
                        <li>📱 Retrait automatique des canaux Telegram après la date d'expiration</li>
                    </ul>
                    
                    <p><strong>Vous changez d'avis ?</strong></p>
                    <p>Vous pouvez réactiver votre abonnement à tout moment avant la date d'expiration depuis votre Dashboard.</p>
                    
                    <div style="text-align: center;">
                        <a href="{self.frontend_url}/dashboard" class="cta-button">Réactiver mon abonnement</a>
                    </div>
                    
                    <p style="margin-top: 30px;">Nous sommes désolés de vous voir partir. Si vous avez des suggestions pour améliorer nos services, n'hésitez pas à nous contacter.</p>
                    
                    <p>Cordialement,<br><strong>L'équipe TRADALIFE</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 TRADALIFE - Tous droits réservés</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)


    
    async def send_password_reset_email(self, to_email: str, reset_link: str, user_name: str = ""):
        """Send password reset email"""
        subject = "🔐 Réinitialisation de votre mot de passe - TRADALIFE"
        
        display_name = user_name if user_name else to_email.split('@')[0]
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f7;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 20px auto;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    border-radius: 15px;
                    overflow: hidden;
                    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                }}
                .header {{
                    background: rgba(255,255,255,0.1);
                    padding: 30px 20px;
                    text-align: center;
                }}
                .header h1 {{
                    color: white;
                    margin: 0;
                    font-size: 28px;
                    font-weight: bold;
                }}
                .content {{
                    background: white;
                    padding: 40px 30px;
                }}
                .content h2 {{
                    color: #333;
                    margin-top: 0;
                }}
                .content p {{
                    color: #555;
                    line-height: 1.8;
                    font-size: 16px;
                }}
                .reset-button {{
                    display: inline-block;
                    margin: 30px 0;
                    padding: 15px 40px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white !important;
                    text-decoration: none;
                    border-radius: 50px;
                    font-weight: bold;
                    font-size: 16px;
                    text-align: center;
                    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
                }}
                .reset-button:hover {{
                    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
                }}
                .warning-box {{
                    background: #fff3cd;
                    border-left: 4px solid #ffc107;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 5px;
                }}
                .warning-box p {{
                    margin: 0;
                    color: #856404;
                }}
                .footer {{
                    background: #f8f9fa;
                    padding: 20px;
                    text-align: center;
                    color: #6c757d;
                    font-size: 14px;
                }}
                .footer a {{
                    color: #667eea;
                    text-decoration: none;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 RÉINITIALISATION DE MOT DE PASSE</h1>
                </div>
                <div class="content">
                    <h2>Bonjour {display_name},</h2>
                    
                    <p>Vous avez demandé à réinitialiser votre mot de passe pour votre compte TRADALIFE.</p>
                    
                    <p>Cliquez sur le bouton ci-dessous pour créer un nouveau mot de passe:</p>
                    
                    <center>
                        <a href="{reset_link}" class="reset-button">
                            Réinitialiser mon mot de passe
                        </a>
                    </center>
                    
                    <div class="warning-box">
                        <p><strong>⚠️ Important:</strong></p>
                        <p>• Ce lien est valable pendant <strong>1 heure</strong></p>
                        <p>• Si vous n'avez pas demandé cette réinitialisation, ignorez cet email</p>
                        <p>• Votre mot de passe actuel reste valide jusqu'à ce que vous en créiez un nouveau</p>
                    </div>
                    
                    <p style="font-size: 14px; color: #6c757d; margin-top: 30px;">
                        Si le bouton ne fonctionne pas, copiez et collez ce lien dans votre navigateur:<br>
                        <a href="{reset_link}" style="color: #667eea; word-break: break-all;">{reset_link}</a>
                    </p>
                    
                    <p style="margin-top: 30px;">Pour toute question, contactez-nous sur notre support Telegram.</p>
                    
                    <p>Cordialement,<br><strong>L'équipe TRADALIFE</strong></p>
                </div>
                <div class="footer">
                    <p>© 2025 TRADALIFE - Tous droits réservés</p>
                    <p><a href="https://tradalife.com">tradalife.com</a></p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return await self.send_email(to_email, subject, html_content)

# Create singleton instance
email_service = EmailService()