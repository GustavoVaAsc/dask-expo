import dask
from dask.distributed import Client
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


def run_pipeline(selected_sources: list[str], chunksize: int) -> tuple[dict, str]:
    append_log("Iniciando cliente de Dask...")
    client = Client(n_workers=2, threads_per_worker=1, memory_limit="2GiB")
    dashboard_link = client.dashboard_link
    worker_count, threads_per_worker, memory_limit = get_scheduler_stats(client)

    append_log(f"Cliente activo. Link del dashboard de Dask: {dashboard_link}")
    append_log(f"Número de workers: {worker_count}")
    append_log(f"Hilos por worker: {threads_per_worker}")
    append_log(f"Memoria límite por worker: {memory_limit} bytes")

    try:
        append_log("Creando las tasks de Dask usando el método delayed...")
        tasks = []
        for source in selected_sources:
            path, columns = DATASET_OPTIONS[source]
            append_log(f"Preparando task: {path} columnas={columns}")
            tasks.append(dask.delayed(count_words_in_csv)(path, columns, chunksize))

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

            Esta app puede leer tres archivos CSV grandes que contienen preguntas, respuestas y etiquetas de StackOverflow.
            En concreto, del 10% de las preguntas de la plataforma. Estos tres archivos suman más de 1.5GB,
            por lo que se procesan en chunks usando Dask para mantener el uso de memoria bajo control.

            - `Answers.csv` - Pesa 1.5GB.
            - `Questions.csv` - Pesa 1.9GB.
            - `Tags.csv` - Pesa 65MB, pero tiene una cantidad de columnas superior a 104000.

            Si intentamos cargar estos archivos directamente en memoria usando pandas, probablemente nos quedemos
            sin memoria RAM. En cambio, Dask permite procesarlos en partes (chunks) y realizar operaciones de
            reducción para obtener el conteo total de palabras sin necesidad de cargar todo el dataset a la vez.
            """
        )
    )

    left, right = st.columns([1.1, 1.2])

    with left:
        st.subheader("Controles")
        selected_sources = st.multiselect(
            "Contar palabras en:",
            options=list(DATASET_OPTIONS.keys()),
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
                st.session_state.logs = []
                st.session_state.running = True
                st.session_state.last_image = None

                with st.spinner("Procesando..."):
                    try:
                        freq_dict, dashboard_link = run_pipeline(selected_sources, chunksize)
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
