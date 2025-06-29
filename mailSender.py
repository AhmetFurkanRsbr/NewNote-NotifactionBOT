import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(changes):
    sender_email = "xshafa@gmail.com"     # gönderen email
    receiver_email = "xasfbas@gmail.com"  # alıcı email
    password = "2941owadafda"             # 2 adımlı doğrulama aktifse 'uygulama şifresi' gerekir

    subject = "OBS Yeni Not Bildirimi"
    body = "Aşağıdaki notlar sisteme yeni girildi veya değiştirildi:\n\n"

    for lesson, notType, notValue in changes:
        body += f"📘 {lesson} - {notType}: {notValue}\n"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {e}")
