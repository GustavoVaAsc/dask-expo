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

Download both datasets from Kaggle:

- [StackSample dataset](https://www.kaggle.com/datasets/stackoverflow/stacksample?resource=download)
- [Wikipedia Index and Plaintext 20230801](https://www.kaggle.com/datasets/bwandowando/wikipedia-index-and-plaintext-20230801)

Place StackOverflow files inside `archive/`:

- `archive/Questions.csv`
- `archive/Answers.csv`
- `archive/Tags.csv`

Place Wikipedia CSV files in numeric folders inside `archive/`:

- `archive/0`, `archive/1`, ..., `archive/9`
- The app reads only `title` and `text` columns from Wikipedia CSV files.

### 4. Run the App

```bash
python3 -m streamlit run app.py
```

### 5. Quick Test (Smoke Test)

1. Open the Streamlit URL shown in terminal (usually [http://localhost:8501](http://localhost:8501)).
2. In Contar palabras en, select one or more sources.
3. You can select Wikipedia folders individually as `Wikipedia EN - 0` ... `Wikipedia EN - 9`.
4. Set the chunk slider (for example 20000).
5. (Optional) tune workers, threads per worker, and RAM per worker.
6. Click Contar palabras.
7. Confirm a word cloud appears and backend logs update.
8. Click Abrir dashboard de Dask and verify the Dask page opens.

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

Descarga ambos datasets desde Kaggle:

- [Dataset StackSample](https://www.kaggle.com/datasets/stackoverflow/stacksample?resource=download)
- [Wikipedia Index and Plaintext 20230801](https://www.kaggle.com/datasets/bwandowando/wikipedia-index-and-plaintext-20230801)

Coloca los archivos de StackOverflow dentro de `archive/`:

- `archive/Questions.csv`
- `archive/Answers.csv`
- `archive/Tags.csv`

Coloca los CSV de Wikipedia en carpetas numéricas dentro de `archive/`:

- `archive/0`, `archive/1`, ..., `archive/9`
- La app lee únicamente las columnas `title` y `text` de los CSV de Wikipedia.

### 4. Ejecutar la App

```bash
python3 -m streamlit run app.py
```

### 5. Prueba Rápida (Smoke Test)

1. Abre la URL de Streamlit que aparece en la terminal (normalmente [http://localhost:8501](http://localhost:8501)).
2. En Contar palabras en, selecciona una o más fuentes.
3. Puedes elegir carpetas de Wikipedia individualmente como `Wikipedia EN - 0` ... `Wikipedia EN - 9`.
4. Ajusta el slider de chunks (por ejemplo 20000).
5. (Opcional) configura workers, hilos por worker y RAM por worker.
6. Haz clic en Contar palabras.
7. Verifica que aparezca la nube de palabras y que se actualicen los logs del backend.
8. Haz clic en Abrir dashboard de Dask y confirma que abra la página de Dask.

Si la nube se renderiza y no aparecen errores de procesamiento, la app está funcionando correctamente.
