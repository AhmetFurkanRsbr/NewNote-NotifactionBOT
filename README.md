<h1 align="center">📢 OBS New Note Notification BOT</h1>

<p align="center">
  <img src="https://github.com/user-attachments/assets/e4005fcd-7f87-4c5f-ba9b-7b9a78244e51" alt="Project Logo" width="180"/>
</p>

---

## 🌍 Project Overview (EN) 

This project is a lightweight automation bot that periodically checks whether new grades have been entered in the university OBS (Online Information System) and does not tire the system (the task is defined to run automatically every hour for 1 week during the exam period). It alerts the user by sending an e-mail notification when a new grade is detected.
I solve the captcha image through Google Lens. Automation performs what is requested by detecting the information entry parts with Web Scraping, entering the information and making the necessary clicks. With the help of Windows Task Scheduler, I automate the task to run every hour between 10 am and 10 pm for 1 week.
 Since there is a possibility that the Captcha image cannot be analyzed correctly, there are 5 failed attempts in each automatic run so that it does not enter an infinite loop and tire the OBS server.

---

## 🛠️ Technologies Used  

- `Python` 
- `selenium` (web interaction)  
- `smtp` (mail notifications)  
- `schedule` / `time` (periodic task scheduling)  
- `gizliBilgiler.txt` (local secure credential storage)

---

## 💼 Features  


- Periodic grade check from the OBS system  
- Instant desktop notification for new grades  
- Logs historical grade changes  
- Reads credentials from a local secure file  
- Can run silently in the background
- With the Windows Task scheduler, the program runs automatically once every hour between 10:00 am - 00:00 pm
---
## 🇹🇷 Proje Özeti (TR)

Bu proje, üniversite OBS (Online Bilgi Sistemi)'nde yeni not girilip girilmediğini periyodik olarak kontrol eden ve sistemi yormayan hafif bir otomasyon botudur(sınav döneminde 1 hafta boyunca her saat başı otomatik olarak çalışacak şekilde görev tanımlanmıştır). Yeni bir not algılandığında mail bildirimi göndererek kullanıcıyı uyarır.
Captcha görselini Google Lens aracılığıyla çözmekteyim. Otomasyon Web Scraping ile bilgi giriş kısımlarını algılayıp bilgileri girerek ve gerekli tıklamaları yaparak istenileni gerçekleştirmektedir. Windows Görev Zamanlayıcısı yardımıyla görevi 1 hafta boyunca sabah 10 ve gece 00 saatleri arasında her saat başı çalıştıracak şekilde otomatikleştirmekteyim.
 Captcha görselinin doğru analiz edilememe ihtimalide olduğundan dolayı sonsuz döngüye girip OBS sunucusunu yormaması için her otomatik çalıştırmada 5 başarısız deneme hakkı bulunmaktadır. 

---
### 🛠️ Kullanılan Teknolojiler

- `Python` 
- `selenium` (web etkileşimi için)  
- `smtp` (mail bildirimi için)  
- `schedule` / `time` (zamanlanmış görevler için)  
- `gizliBilgiler.txt` (güvenli kimlik bilgileri saklama)

---
### 💼 Özellikler

- OBS sisteminden periyodik not kontrolü  
- Yeni notlar için e-posta bildirimi  
- Not geçmişini kayıt altına alma  
- Giriş bilgilerini yerel dosyadan okuma  
- Sessizce arka planda çalışabilme
- Windows Görev zamanlayıcısı ile 10:00 - 00:00 saatleri arasında her saatte bir kere program otomatik olarak çalışmaktadır

---

### 🖼️ Screenshots / Ekran Görüntüleri

<p align="center"> 

  <img src="https://github.com/user-attachments/assets/7cd245ff-211d-4c1e-ba9a-2d43966c09d4" width="400"/> 
  <img src="https://github.com/user-attachments/assets/0ed75ec2-bfb0-474b-b40b-169832e9d274" width="400"/><br><br> 
  <img src="https://github.com/user-attachments/assets/56ac346e-6fae-4e8d-9dde-a2323a43d623" width="400"/> 
  <img src="https://github.com/user-attachments/assets/06bb2806-77d4-4ad8-ad64-bdf7315a7cd4" width="400"/><br><br> 
  <img src="https://github.com/user-attachments/assets/e51c2377-89b7-4b00-9c62-b9a05552c60c"  width="400"/> 
</p>

---

## 🚀 Setup & Usage  / Kurulum ve Kullanım

```bash
# Clone the project / Projeyi klonla
git clone https://github.com/AhmetFurkanRsbr/NewNote-NotifactionBOT.git
cd NewNote-NotifactionBOT

# Install required packages / Gerekli paketleri yükle
pip install -r requirements.txt

# Edit user information for you / Knedine göre kullanıcı bilgilerini düzenle
# //newNotifaction.py line 16,17
# -> username = "obs_kullanici_adi"
# -> password = "obs_sifresi"

# //mailSender.py line 6,7,8
# -> sender_email = "your@gmail.com"   # sender / gönderen email
# -> receiver_email = "yourmail@gmail.com" # receiver / alıcı email
# -> password = "yourPassKey"              # 2 adımlı doğrulama aktifse 'uygulama şifresi' gerekir

# Run / Çalıştır
python newNoteNotifaction.py

