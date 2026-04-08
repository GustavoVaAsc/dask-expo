# dask-expo

Streamlit app for a Distributed Systems exposition (2026-2), showing how to process large StackOverflow CSV files with Dask and generate a word cloud.

## English

### 1. Requirements

- Python 3.10+
- pip

### 2. Dependencies

Install the required packages:

```bash
python3 -m pip install streamlit dask distributed pandas wordcloud matplotlib
```

### 3. Dataset Download

Download StackSample from Kaggle:

- [StackSample dataset on Kaggle](https://www.kaggle.com/datasets/stackoverflow/stacksample?resource=download)

After downloading, place these files inside the local archive folder:

- archive/Questions.csv
- archive/Answers.csv
- archive/Tags.csv

### 4. Run the App

```bash
python3 -m streamlit run app.py
```

### 5. Quick Test (Smoke Test)

1. Open the Streamlit URL shown in terminal (usually [http://localhost:8501](http://localhost:8501)).
2. In Contar palabras en, keep one or more datasets selected.
3. Set the chunk slider (for example 20000).
4. Click Contar palabras.
5. Confirm a word cloud appears and backend logs update.
6. Click Abrir dashboard de Dask and verify the Dask page opens.

If the word cloud renders and no processing error appears, the app is working correctly.

## Español

### 1. Requisitos

- Python 3.10+
- pip

### 2. Dependencias

Instala los paquetes necesarios:

```bash
python3 -m pip install streamlit dask distributed pandas wordcloud matplotlib
```

### 3. Descarga del Dataset

Descarga StackSample desde Kaggle:

- [Dataset StackSample en Kaggle](https://www.kaggle.com/datasets/stackoverflow/stacksample?resource=download)

Luego coloca estos archivos dentro de la carpeta local archive:

- archive/Questions.csv
- archive/Answers.csv
- archive/Tags.csv

### 4. Ejecutar la App

```bash
python3 -m streamlit run app.py
```

### 5. Prueba Rápida (Smoke Test)

1. Abre la URL de Streamlit que aparece en la terminal (normalmente [http://localhost:8501](http://localhost:8501)).
2. En Contar palabras en, deja seleccionado uno o más datasets.
3. Ajusta el slider de chunks (por ejemplo 20000).
4. Haz clic en Contar palabras.
5. Verifica que aparezca la nube de palabras y que se actualicen los logs del backend.
6. Haz clic en Abrir dashboard de Dask y confirma que abra la página de Dask.

Si la nube se renderiza y no aparecen errores de procesamiento, la app está funcionando correctamente.
