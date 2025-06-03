import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# ---------------- GOOGLE SHEETS ----------------

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open("Docentes")
sheet = spreadsheet.sheet1
data = sheet.get_all_records()
df_dni = pd.DataFrame(data)

if "DNI" not in df_dni.columns:
    raise ValueError("❌ La hoja de cálculo debe tener una columna llamada 'DNI'")

dni_list = df_dni["DNI"].dropna().astype(str).tolist()
print(dni_list)

# ---------------- SELENIUM ----------------
chrome_options = Options()
#chrome_options.add_argument("--headless=new")  # SIN INTERFAZ GRÁFICA
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# NO AGREGUES --user-data-dir







chrome_options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
wait = WebDriverWait(driver, 20)

def extraer_datos_tarjeta(tarjeta):
    try:
        encabezados = tarjeta.find_elements(By.TAG_NAME, "h4")
        if len(encabezados) < 2:
            return None
        dni = encabezados[0].text.strip()
        nombre = encabezados[1].text.strip()
        parrafos = tarjeta.find_elements(By.TAG_NAME, "p")
        datos = {}
        for p in parrafos:
            texto = p.text.strip()
            if ":" in texto:
                clave, valor = texto.split(":", 1)
                datos[clave.strip()] = valor.strip()
        return {
            "DNI": dni,
            "Nombre": nombre,
            "Promedio": float(datos.get("Promedio", "0").replace(",", ".")),
            "Puntaje": float(datos.get("Puntaje", "0").replace(",", ".")),
            "Orden": int(datos.get("Orden", "0")),
            "Cargo_Area": datos.get("Cargo Area", "__"),
            "Codigo_Cargo": datos.get("Codigo del cargo", ""),
            "Apto_Fisico": datos.get("Apto Fisico", ""),
            "Distrito": datos.get("Distrito", ""),
            "Rama": datos.get("Rama", ""),
            "Recalificacion": datos.get("Recalificacion laboral", "")
        }
    except Exception as e:
        print(f"⚠️ Error al procesar tarjeta: {e}")
        return None

resultados = []
driver.get("https://abc.gob.ar/listado-oficial/")
for dni_input_value in dni_list:
    print(f"🔍 Buscando DNI: {dni_input_value}")
    try:
        dni_input = wait.until(EC.presence_of_element_located((By.ID,"name")))
        dni_input.clear()
        dni_input.send_keys(dni_input_value)
        driver.find_element(By.ID, "buttonSubmit").click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "containerflex-container")))
        tarjetas = driver.find_elements(By.CLASS_NAME, "containerflex-container")

        for tarjeta in tarjetas:
            datos = extraer_datos_tarjeta(tarjeta)
            if datos:
                resultados.append(datos)

    except Exception as e:
        print(f"Se presenta ERROR con DNI {dni_input_value}: {e}")

driver.quit()

df_resultados = pd.DataFrame(resultados)
print(df_resultados)

df_resultados.to_csv("resultados_docentes.csv", index=False)

try:
    worksheet_output = spreadsheet.worksheet("Resultados")
except gspread.exceptions.WorksheetNotFound:
    worksheet_output = spreadsheet.add_worksheet(title="Resultados", rows="100", cols="20")

worksheet_output.clear()
set_with_dataframe(worksheet_output, df_resultados)

if __name__ == "__main__":
    print("Ejecutando el scraper correctamente desde Docker")
