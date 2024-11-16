from flask_mail import Mail, Message

mail = Mail()

def send_verification_email(user_email, token):
    msg = Message("Verify Your Email", sender="noreply@example.com", recipients=[user_email])
    msg.body = f"Click on the link to verify your email: http://localhost:5000/verify-email/{token}"
    mail.send(msg)
