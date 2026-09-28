import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='db_dal'
    )
    return connection

def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM pddikti_example"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# =========================
# AMBIL DATA DARI MYSQL
# =========================
data = get_data_from_db()


# =========================
# SIDEBAR
# =========================
st.sidebar.title("Pilih halaman")

halaman = st.sidebar.radio(
    "",
    ["Dataset", "Visualisasi", "Form Input"]
)


# =========================
# HALAMAN DATASET
# =========================
if halaman == "Dataset":

    st.title("Streamlit Simple App")
    st.header("Halaman Dataset")

    st.dataframe(data)


# =========================
# HALAMAN VISUALISASI
# =========================
elif halaman == "Visualisasi":

    st.title("Streamlit Simple App")
    st.header("Halaman Visualisasi")

    # Pilihan universitas
    universitas = st.selectbox(
        "Pilih Universitas",
        data["universitas"].unique()
    )

    # Filter data berdasarkan universitas
    data_universitas = data[
        data["universitas"] == universitas
    ]

    # Membuat grafik
    fig, ax = plt.subplots()

    for program_studi in data_universitas["program_studi"].unique():

        data_prodi = data_universitas[
            data_universitas["program_studi"] == program_studi
        ]

        ax.plot(
            data_prodi["semester"],
            data_prodi["jumlah"],
            marker='o',
            label=program_studi
        )

    ax.set_title(
        f"Visualisasi Data untuk {universitas}"
    )

    ax.set_xlabel("Semester")
    ax.set_ylabel("Jumlah")

    ax.legend()

    plt.xticks(rotation=45)

    st.pyplot(fig)

# =========================
# HALAMAN FORM INPUT
# =========================
elif halaman == "Form Input":

    st.header("Halaman Form Input")

    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input('Jumlah', min_value=0, format='%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')

    if submit_button:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO pddikti_example(semester, jumlah, program_studi, universitas)
        VALUES (%s, %s, %s, %s)
        """

        cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
        conn.commit()
        conn.close()
        st.success("Data successfully submitted to the database!")