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
                    
                    <a href="https://videocourse.preview.emergentagent.com/boutique" class="button">Découvrir les formations</a>
                    
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
        """Send purchase confirmation email"""
        subject = f"Confirmation d'achat - {formation_title}"
        
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
                .button {{ display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>✅ Paiement confirmé !</h1>
                </div>
                <div class="content">
                    <p>Votre achat a été effectué avec succès.</p>
                    
                    <div class="purchase-details">
                        <h3>Détails de l'achat</h3>
                        <p><strong>Formation :</strong> {formation_title}</p>
                        <p><strong>Montant :</strong> {amount}€</p>
                    </div>
                    
                    <h3>📋 Prochaine étape : Vérification KYC</h3>
                    <p>Pour accéder à votre formation et aux canaux Telegram VIP, veuillez compléter votre vérification d'identité (KYC).</p>
                    
                    <p><strong>Documents requis :</strong></p>
                    <ul>
                        <li>Passeport</li>
                        <li>Carte d'identité (recto-verso)</li>
                        <li>Preuve de résidence</li>
                    </ul>
                    
                    <a href="https://videocourse.preview.emergentagent.com/dashboard" class="button">Compléter mon KYC</a>
                    
                    <p>Une fois votre KYC validé, vous recevrez un email de confirmation et pourrez accéder à tout le contenu.</p>
                    
                    <p>Merci pour votre confiance !<br>L'équipe Tradalife</p>
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
    
    async def send_kyc_approved(self, to_email: str):
        """Send KYC approval email"""
        subject = "🎉 Votre KYC est approuvé !"
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                .container { max-width: 600px; margin: 0 auto; padding: 20px; }
                .header { background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
                .content { background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }
                .button { display: inline-block; padding: 12px 30px; background: linear-gradient(135deg, #E91E8C 0%, #7B3FF2 100%); color: white; text-decoration: none; border-radius: 25px; margin: 20px 0; }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Félicitations !</h1>
                </div>
                <div class="content">
                    <p>Votre compte a été vérifié avec succès !</p>
                    
                    <p>Vous avez maintenant accès à :</p>
                    <ul>
                        <li>✅ Toutes vos formations vidéo</li>
                        <li>✅ Les canaux Telegram VIP</li>
                        <li>✅ Le support premium</li>
                    </ul>
                    
                    <a href="https://videocourse.preview.emergentagent.com/dashboard" class="button">Accéder à mes formations</a>
                    
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
                    
                    <a href="https://videocourse.preview.emergentagent.com/dashboard" class="button">Soumettre à nouveau</a>
                    
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