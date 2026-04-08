import dask
from dask.distributed import Client
from pathlib import Path
from textwrap import dedent
from wordcloud import WordCloud
import streamlit as st

from dask_utils import count_words_in_csv, merge_counters
from styles import apply_apple_style


DATASET_OPTIONS = {
    "Preguntas (Title + Body)": ("archive/Questions.csv", ["Title", "Body"]),
    "Respuestas (Body)": ("archive/Answers.csv", ["Body"]),
    "Etiquetas (Tag)": ("archive/Tags.csv", ["Tag"]),
}

WIKIPEDIA_PREFIX = "Wikipedia EN - "
WIKIPEDIA_OPTIONS = [f"{WIKIPEDIA_PREFIX}{i}" for i in range(10)]


def get_wikipedia_csv_files(base_archive: str = "archive", folder: str | None = None) -> list[str]:
    """Return sorted CSV paths from archive/0..9 folders, or one specific folder."""
    archive_path = Path(base_archive)
    files: list[str] = []
    folders = [folder] if folder is not None else list(map(str, range(10)))

    for folder_name in folders:
        folder_path = archive_path / folder_name
        if folder_path.is_dir():
            files.extend(str(p) for p in sorted(folder_path.glob("*.csv")))
    return files


def parse_wikipedia_folder(source_label: str) -> str | None:
    """Extract folder number from labels like 'Wikipedia EN - 3'."""
    if not source_label.startswith(WIKIPEDIA_PREFIX):
        return None
    folder = source_label[len(WIKIPEDIA_PREFIX):].strip()
    return folder if folder in {str(i) for i in range(10)} else None

def append_log(message: str) -> None:
    st.session_state.logs.append(message)


def render_logs(container) -> None:
    with container.container():
        st.markdown('<div class="log-card">', unsafe_allow_html=True)
        st.markdown("### Registros del Backend")
        if st.session_state.logs:
            st.code("\n".join(st.session_state.logs), language="text")
        else:
            st.caption("Backend sin actividad.")
        st.markdown("</div>", unsafe_allow_html=True)


def get_scheduler_stats(client: Client) -> tuple[int, int, int]:
    workers = client.scheduler_info().get("workers", {})
    worker_count = len(workers)

    if not workers:
        return 0, 0, 0

    first_worker = next(iter(workers.values()))
    threads = int(first_worker.get("nthreads", 0))
    memory_limit = int(first_worker.get("memory_limit", 0))
    return worker_count, threads, memory_limit


def run_pipeline(
    selected_sources: list[str],
    chunksize: int,
    n_workers: int,
    threads_per_worker: int,
    memory_limit_gb: int,
) -> tuple[dict, str]:
    append_log("Iniciando cliente de Dask...")
    client = Client(
        n_workers=n_workers,
        threads_per_worker=threads_per_worker,
        memory_limit=f"{memory_limit_gb}GiB",
    )
    dashboard_link = client.dashboard_link
    worker_count, threads_per_worker, memory_limit = get_scheduler_stats(client)

    append_log(f"Cliente activo. Link del dashboard de Dask: {dashboard_link}")
    append_log(
        "Configuración seleccionada: "
        f"workers={n_workers}, threads/worker={threads_per_worker}, RAM/worker={memory_limit_gb}GiB"
    )
    append_log(f"Número de workers: {worker_count}")
    append_log(f"Hilos por worker: {threads_per_worker}")
    append_log(f"Memoria límite por worker: {memory_limit} bytes")

    try:
        append_log("Creando las tasks de Dask usando el método delayed...")
        tasks = []
        for source in selected_sources:
            wiki_folder = parse_wikipedia_folder(source)
            if wiki_folder is not None:
                wiki_files = get_wikipedia_csv_files("archive", folder=wiki_folder)
                append_log(f"Wikipedia EN - {wiki_folder}: {len(wiki_files)} archivos CSV detectados")
                for wiki_path in wiki_files:
                    append_log(f"Preparando task: {wiki_path} columnas=['title', 'text']")
                    tasks.append(dask.delayed(count_words_in_csv)(wiki_path, ["title", "text"], chunksize))
            else:
                path, columns = DATASET_OPTIONS[source]
                append_log(f"Preparando task: {path} columnas={columns}")
                tasks.append(dask.delayed(count_words_in_csv)(path, columns, chunksize))

        if not tasks:
            raise ValueError("No se encontraron archivos para procesar.")

        append_log("Reducciendo los resultados con merge_counters...")
        total_counts = dask.delayed(merge_counters)(tasks)

        append_log("Computando resultados con el método compute()...")
        top_words = total_counts.compute().most_common(200)
        append_log(f"Tarea completa, las 200 palabras más comunes son: {len(top_words)}")

        return dict(top_words), dashboard_link
    finally:
        append_log("Cerrando cliente de Dask...")
        client.close()
        append_log("Cliente de Dask cerrado.")


def main() -> None:
    st.set_page_config(page_title="Dashboard para crear una nube de palabras usando Dask", layout="wide")
    apply_apple_style()

    if "logs" not in st.session_state:
        st.session_state.logs = []
    if "running" not in st.session_state:
        st.session_state.running = False
    if "dashboard_link" not in st.session_state:
        st.session_state.dashboard_link = ""
    if "last_image" not in st.session_state:
        st.session_state.last_image = None

    st.markdown(
        dedent(
            """
            ## Nube de Palabras con Dask!

            Esta app procesa datasets CSV grandes con Dask para construir una nube de palabras sin cargar todo en memoria.
            Combina dos fuentes principales: datos de StackOverflow y un subconjunto de artículos de Wikipedia en inglés.

            StackOverflow (StackSample):

            - `Answers.csv` - Pesa 1.5GB.
            - `Questions.csv` - Pesa 1.9GB.
            - `Tags.csv` - Pesa 65MB, pero tiene una cantidad de columnas superior a 104000.

            Wikipedia EN (subconjunto local):

            - Carpetas `archive/0` a `archive/9` con múltiples CSV.
            - Se leen únicamente las columnas `title` y `text` para el conteo de palabras.

            Este enfoque permite escalar el análisis por lotes (chunks) y agregar más archivos en `archive/0..9`
            sin cambiar la lógica principal de la app.

            Si intentamos cargar estos archivos directamente en memoria usando pandas, probablemente nos quedemos
            sin memoria RAM. En cambio, Dask permite procesarlos en partes (chunks) y realizar operaciones de
            reducción para obtener el conteo total de palabras sin necesidad de cargar todo el dataset a la vez.
            """
        )
    )

    left, right = st.columns([1.1, 1.2])

    with left:
        st.subheader("Controles")
        source_options = list(DATASET_OPTIONS.keys()) + WIKIPEDIA_OPTIONS

        selected_sources = st.multiselect(
            "Contar palabras en:",
            options=source_options,
            default=list(DATASET_OPTIONS.keys()),
        )

        chunksize = st.slider(
            "Tamaño del chunk (número de filas por tarea)",
            min_value=5000,
            max_value=50000,
            step=500,
            value=20000,
            help="Los chunks más pequeños reducen el uso pico de memoria pero pueden tardar más en completarse.",
        )

        slider_col, _ = st.columns([1, 3])
        with slider_col:
            n_workers = st.slider(
                "Número de workers",
                min_value=2,
                max_value=4,
                step=1,
                value=2,
            )

            threads_per_worker = st.slider(
                "Hilos por worker",
                min_value=1,
                max_value=2,
                step=1,
                value=1,
            )

            memory_limit_gb = st.slider(
                "RAM máxima por worker (GB)",
                min_value=1,
                max_value=3,
                step=1,
                value=2,
            )

        run_clicked = st.button("Contar palabras", type="primary", disabled=st.session_state.running)


        st.link_button(
            "Abrir dashboard de Dask",
            url=st.session_state.dashboard_link or "http://127.0.0.1:8787/status",
            help="Monitorea el estado de los recursos del sistema en Dask.",
        )

        if run_clicked:
            if not selected_sources:
                st.warning("Elige al menos un dataset.")
            else:
                missing_wiki = []
                for source in selected_sources:
                    wiki_folder = parse_wikipedia_folder(source)
                    if wiki_folder is not None and not get_wikipedia_csv_files("archive", folder=wiki_folder):
                        missing_wiki.append(wiki_folder)

                if missing_wiki:
                    folders = ", ".join(sorted(missing_wiki))
                    st.warning(f"No se encontraron archivos CSV en archive/{folders} para Wikipedia.")
                    return

                st.session_state.logs = []
                st.session_state.running = True
                st.session_state.last_image = None

                with st.spinner("Procesando..."):
                    try:
                        freq_dict, dashboard_link = run_pipeline(
                            selected_sources,
                            chunksize,
                            n_workers,
                            threads_per_worker,
                            memory_limit_gb,
                        )
                        st.session_state.dashboard_link = dashboard_link

                        append_log("Generando nube de palabras...")
                        wc = WordCloud(
                            width=1200,
                            height=600,
                            background_color="white",
                            colormap="viridis",
                        )
                        wc.generate_from_frequencies(freq_dict)
                        st.session_state.last_image = wc.to_array()
                        append_log("Generación de nube de palabras finalizada.")
                    except Exception as exc:
                        append_log(f"Error: {exc}")
                        st.error(f"Fallo en el procesamiento: {exc}")
                    finally:
                        st.session_state.running = False

    with right:
        st.subheader("Nube de palabras")
        if st.session_state.last_image is not None:
            st.image(st.session_state.last_image, caption="Top 200 palabras", use_container_width=True)
        else:
            st.info("Ejecuta el análisis para renderizar la nube de palabras.")

        render_logs(st.container())


if __name__ == "__main__":
    main()
