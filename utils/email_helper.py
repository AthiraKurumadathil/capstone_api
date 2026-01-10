import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class EmailHelper:
    """Helper class for sending emails via Google SMTP server (Gmail)"""
    
    def __init__(self, sender_email: Optional[str] = None, sender_password: Optional[str] = None):
        """
        Initialize the EmailHelper with Gmail credentials and SMTP configuration from .env.
        
        Args:
            sender_email: Gmail address (if None, uses GMAIL_ADDRESS from .env)
            sender_password: Gmail App Password (if None, uses GMAIL_PASSWORD from .env)
        """
        self.sender_email = sender_email or os.getenv("GMAIL_ADDRESS")
        self.sender_password = sender_password or os.getenv("GMAIL_PASSWORD")
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        
        if not self.sender_email or not self.sender_password:
            raise ValueError("Gmail credentials not provided. Set GMAIL_ADDRESS and GMAIL_PASSWORD in .env file")
    
    def send_email(
        self,
        recipient_email: str,
        subject: str,
        body: str,
        is_html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> dict:
        """
        Send an email using Gmail SMTP server.
        
        Args:
            recipient_email: Recipient's email address (single email as string)
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML content (default: False for plain text)
            cc: List of CC email addresses (optional)
            bcc: List of BCC email addresses (optional)
            attachments: List of file paths to attach (optional)
        
        Returns:
            Dictionary with status and message
        
        Raises:
            Exception: If email sending fails
        """
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = recipient_email
            message["Subject"] = subject
            
            # Add CC and BCC if provided
            if cc:
                message["Cc"] = ", ".join(cc)
            
            # Add body
            content_type = "html" if is_html else "plain"
            message.attach(MIMEText(body, content_type))
            
            # Add attachments if provided
            if attachments:
                self._attach_files(message, attachments)
            
            # Prepare recipients list
            recipients = [recipient_email]
            if cc:
                recipients.extend(cc)
            if bcc:
                recipients.extend(bcc)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS encryption
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, recipients, message.as_string())
            
            return {
                "status": "success",
                "message": f"Email sent successfully to {recipient_email}",
                "recipient": recipient_email
            }
        
        except smtplib.SMTPAuthenticationError:
            raise Exception("Gmail authentication failed. Check GMAIL_ADDRESS and GMAIL_PASSWORD in .env")
        except smtplib.SMTPException as e:
            raise Exception(f"SMTP error occurred: {str(e)}")
        except Exception as e:
            raise Exception(f"Error sending email: {str(e)}")
    
    def send_bulk_email(
        self,
        recipients: List[str],
        subject: str,
        body: str,
        is_html: bool = False,
        attachments: Optional[List[str]] = None
    ) -> dict:
        """
        Send the same email to multiple recipients.
        
        Args:
            recipients: List of recipient email addresses
            subject: Email subject
            body: Email body content
            is_html: Whether body is HTML content (default: False for plain text)
            attachments: List of file paths to attach (optional)
        
        Returns:
            Dictionary with status and list of results
        """
        results = {
            "status": "completed",
            "total": len(recipients),
            "successful": 0,
            "failed": 0,
            "details": []
        }
        
        for recipient in recipients:
            try:
                result = self.send_email(
                    recipient_email=recipient,
                    subject=subject,
                    body=body,
                    is_html=is_html,
                    attachments=attachments
                )
                results["successful"] += 1
                results["details"].append(result)
            except Exception as e:
                results["failed"] += 1
                results["details"].append({
                    "status": "failed",
                    "recipient": recipient,
                    "error": str(e)
                })
        
        return results
    
    def send_html_email(
        self,
        recipient_email: str,
        subject: str,
        html_body: str,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        attachments: Optional[List[str]] = None
    ) -> dict:
        """
        Convenience method to send HTML email.
        
        Args:
            recipient_email: Recipient's email address
            subject: Email subject
            html_body: HTML content for email body
            cc: List of CC email addresses (optional)
            bcc: List of BCC email addresses (optional)
            attachments: List of file paths to attach (optional)
        
        Returns:
            Dictionary with status and message
        """
        return self.send_email(
            recipient_email=recipient_email,
            subject=subject,
            body=html_body,
            is_html=True,
            cc=cc,
            bcc=bcc,
            attachments=attachments
        )
    
    @staticmethod
    def _attach_files(message: MIMEMultipart, file_paths: List[str]) -> None:
        """
        Attach files to email message.
        
        Args:
            message: MIMEMultipart message object
            file_paths: List of file paths to attach
        """
        from email.mime.base import MIMEBase
        from email import encoders
        import os
        
        for file_path in file_paths:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            "Content-Disposition",
                            f"attachment; filename= {os.path.basename(file_path)}"
                        )
                        message.attach(part)
                except Exception as e:
                    raise Exception(f"Error attaching file {file_path}: {str(e)}")
            else:
                raise Exception(f"File not found: {file_path}")
