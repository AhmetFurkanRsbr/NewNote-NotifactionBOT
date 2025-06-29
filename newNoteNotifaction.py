from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from mailSender import send_email 
from datetime import datetime
import json
import os
import sys
import pyperclip
import re
import logging

userName = "214121"      # Okul numarası
password = "sifrem"      # Parola

obsUrl = "https://ogr.nku.edu.tr/login"        # Öğrenci Bilgi Sistemi URL
googleLensUrl = "https://www.google.com/?olud" # Google Lens URL

logging.basicConfig(
    filename="botLog.txt",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

options = Options()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)

driver = webdriver.Chrome(options=options)

# Bot tespiti için önlemi
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
    """
})

actions = ActionChains(driver)
# OBS sayfasını aç ve handle'ı kaydet
driver.get(obsUrl)
obs_handle = driver.current_window_handle


count=0
def tryLogin(count):
    logging.info(f"{count}. giriş denemesi yapılıyor.")

    if count>=4 :
        print("5 deneme sonrasında giriş başarısız. Program sonlandırılıyor.")
        sys.exit()
        
    # Giriş bilgilerinin girileceği yeri bul ve doldur
    driver.find_element(By.ID, "kullaniciadi").send_keys(userName)
    driver.find_element(By.ID, "kullanicisifre").send_keys(password)

    # Captcha görselinin URL'sini al
    captcha = driver.find_element(By.ID, "myCaptcha")
    captcha_url = captcha.get_property("src")

    # Yeni sekmede Google Lens'i aç 
    driver.execute_script("window.open('');")
    lens_handle = [handle for handle in driver.window_handles if handle != obs_handle][0]
    driver.switch_to.window(lens_handle)
    driver.get(googleLensUrl)
    sleep(2)

    # URL'yi arama kutusuna yapıştır ve analiz et
    lens_input = driver.find_element(By.CLASS_NAME, "cB9M7")
    lens_input.send_keys(captcha_url)
    driver.find_element(By.CLASS_NAME, "Qwbd3").click()

    sleep(10)  # Google Lens sonuçlarının yüklenmesini bekle

    # Görseli aç
    driver.find_element(By.CLASS_NAME, "hhMc9e").click()
    image = driver.find_element(By.CLASS_NAME, "bn6k9b")
    actions.double_click(image).perform()

    # 'Kopyala'ya tıkla captcha ifadesinin metin halini kopyalamış olur
    driver.find_element(By.CLASS_NAME, "oOI73c").click()

    
    sleep(1)
    
    # Panodan metni al
    copiedText = pyperclip.paste()
    # Sadece A-Z ve 0-9 karakterlerini al, diğer her şeyi temizle
    copiedText = re.sub(r'[^A-Z0-9]', '', copiedText.upper())
    print("Çözülen CAPTCHA:", copiedText)

    # OBS sekmesine geri dön
    driver.switch_to.window(obs_handle)
    sleep(1)

    # Captcha input'unun girileceği yeri bul ve metni yaz
    captcha_input = driver.find_element(By.ID, "dogrulamakodu")  
    captcha_input.send_keys(copiedText)
    

    # Bilgiler girildikten sonra giriş butonuna tıklanıyor
    driver.find_element(By.CSS_SELECTOR, ".btn.btn-block.btn-success").click()
    sleep(4)
    if(driver.current_url=="https://ogr.nku.edu.tr/login"):
        logging.warning("Giriş başarısız.")
        
        print("Giriş başarısız")
        count+=1
        print("Deneme sayısı: ", count)
        tryLogin(count)
    else:
        logging.info("Giriş başarılı.")
        print("Giriş başarılı")
        driver.find_element(By.CSS_SELECTOR, ".fa.fa-book").click()
        sleep(5)
        driver.find_element(By.ID, "menu_12").click()

#-------------------------------------------------------------------
# Ders ve notları sayfadan çek 
def getLessonInformation(driver):
    allNotesDict = {}

    lessonRows = driver.find_elements(By.XPATH, "//table//tr")  # Tablo satırları

    for lesson in lessonRows:
        cells = lesson.find_elements(By.TAG_NAME, "td")
        if len(cells) < 10:
            continue  # Geçersiz satırları atla

        lessonName = cells[1].text.strip()
        notesHtml = cells[9].get_attribute("innerHTML")

        soup = BeautifulSoup(notesHtml, "html.parser")
        bold_tags = soup.find_all("b")

        notesDict = {}
        for tag in bold_tags:
            fullTitle = tag.get_text(strip=True)
            key = fullTitle.split("(%")[0].replace(":", "").strip()

            if tag.next_sibling:
                value_text = tag.next_sibling.strip()
                try:
                    value = int(value_text)
                except ValueError:
                    value = None
            else:
                value = None

            notesDict[key] = value

        allNotesDict[lessonName] = notesDict

    return allNotesDict


# JSON dosyasına bilgileri kaydet
def save_notes_to_file(notesDict, filepath="notlar.json"):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(notesDict, f, ensure_ascii=False, indent=4)

# JSON dosyasından bilgileri oku
def load_notes_from_file(filepath="notlar.json"):
    if not os.path.exists(filepath):
        return {}
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

# Yeni ve eski notları karşılaştır, değişiklikleri döndür
def find_new_or_updated_grades(old_notes, new_notes):
    changes = []
    for lesson, notes in new_notes.items():
        if not isinstance(notes, dict):
            logging.warning(f"'{lesson}' dersinin notları liste(dict) tipinde değil, atlanıyor.")
            continue

        if lesson not in old_notes:
            for notType, notValue in notes.items():
                changes.append((lesson, notType, notValue))
        else:
            oldNotes = old_notes.get(lesson, {})
            if not isinstance(oldNotes, dict):
                logging.warning(f"'{lesson}' dersinin eski notları liste(dict) tipinde değil, atlanıyor.")
                oldNotes = {}

            for notType, notValue in notes.items():
                oldValue = oldNotes.get(notType)
                if oldValue != notValue:
                    changes.append((lesson, notType, notValue))
    return changes


def main(driver):
    tryLogin(0)   

    logging.info("\n\n--------------------")
    logging.info(f"Yeni çalıştırma başlatıldı: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
 
    sleep(30)

    old_notes = load_notes_from_file()
    new_notes = getLessonInformation(driver)

    changes = find_new_or_updated_grades(old_notes, new_notes)

    if changes:
        print("Yeni veya değişen notlar tespit edildi:")
        for lesson, notType, notValue in changes:
            print(f"{lesson} - {notType}: {notValue}")

        save_notes_to_file(new_notes)
        
        send_email(changes)     # Yeni eklenen not ve ders bilgileri mail ile gönder
        logging.info("Mail gönderildi.")
        
    else:
        print("Notlarda değişiklik yok.")
        logging.info("Mail gönderilmedi, notlarda değişiklik yok.")

main(driver) 
