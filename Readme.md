
# 🔎 Docentes ABC Scraper

Este proyecto automatiza la consulta de datos docentes desde el sitio oficial de la Dirección General de Cultura y Educación de la provincia de Buenos Aires (https://abc.gob.ar/listado-oficial/) utilizando **Selenium**, y guarda los resultados en un archivo CSV y una hoja de cálculo de **Google Sheets**.

## 📌 Funcionalidades

- Lee una lista de DNIs desde una hoja de cálculo de Google Sheets.
- Utiliza Selenium para ingresar cada DNI y obtener datos docentesgi del sitio web oficial.
- Extrae información estructurada de las tarjetas de resultados.
- Guarda los resultados:
  - En un archivo local `resultados_docentes.csv`.
  - En una hoja llamada `Resultados` dentro del mismo Google Sheet.

## 📂 Estructura del Proyecto


.
├── credenciales.json        # Claves de API de Google (NO subir a GitHub)
├── resultados_docentes.csv  # Archivo generado automáticamente con los resultados
├── script.py                # Script principal de scraping
└── README.md                # Este archivo
```

## ✅ Requisitos

- Python 3.9 o superior
- Acceso a Google Cloud Platform con claves de servicio (archivo `credenciales.json`)
- Una hoja de cálculo de Google llamada **"Docentes"** con una columna `DNI`
- Google Chrome y conexión a internet

## 🧪 Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/tu-usuario/abc-docentes-scraper.git
cd abc-docentes-scraper
```

2. Crear un entorno virtual y activarlo:

```bash
python -m venv venv
source venv/bin/activate  # En Windows usa: venv\Scripts\activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Asegúrarse de tener el archivo `credenciales.json` en el mismo directorio.

## ▶️ Ejecución

```bash
python script.py
```

- El script va a buscar en la hoja de cálculo los DNIs y procesará cada uno.
- Al finalizar, se obtendrá un archivo `resultados_docentes.csv` con los datos.
- También se actualizará automáticamente la hoja de cálculo.

## 📌 Tecnologías utilizadas

- 🐍 Python
- 📄 Pandas
- 🌐 Selenium
- 🧠 gspread y Google Sheets API
- 💻 WebDriver Manager
- 🔒 OAuth2Client

## 📎 Notas

- Asegurate de que el archivo `credenciales.json` tenga permisos de acceso a la hoja de cálculo.
- No compartas este archivo públicamente ni lo subas al repositorio.

## 📬 Contacto

Si tenés dudas o sugerencias, podés escribirme a: `andreamarigomez@gmail.com`
