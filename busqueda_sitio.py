import streamlit as st
import pandas as pd
import requests
import folium as fl
import streamlit_folium as stfl



if 'marcadores' not in st.session_state:
    st.session_state["marcadores"] = []


st.set_page_config(page_title="Buscador de Medicamentos 🇨🇱", layout="wide")


@st.cache_data
def cargar_datos():
    archivo = "con_direcciones.csv"
    
    try:

        df = pd.read_csv(archivo, sep=';')
      
        df.columns = df.columns.str.strip()
        
     
        if 'Comuna cliente dest' in df.columns:
            df['Comuna cliente dest'] = df['Comuna cliente dest'].astype(str).str.upper().str.strip()
        
        return df
    except FileNotFoundError:
        st.error(f"Error: No se encuentra el archivo '{archivo}'. Asegúrate de haber ejecutado el script de clasificación primero.")
        return pd.DataFrame()


df_local = cargar_datos()


st.sidebar.header("Filtros de Búsqueda")


lista_comunas = ["TODAS"] + sorted(df_local['Comuna cliente dest'].unique().tolist()) if not df_local.empty else []
filtro_comuna = st.sidebar.selectbox(" Seleccionar Comuna:", lista_comunas)


lista_venta = ["TODOS"] + sorted(df_local['Condicion'].unique().tolist()) if not df_local.empty and 'Condicion' in df_local.columns else []
filtro_venta = st.sidebar.selectbox(" Condición de Venta:", lista_venta)



st.title(" Buscador Unificado de Medicamentos")
st.markdown("""
Esta herramienta cruza datos del **Registro Sanitario (API)** con el **Stock en Farmacias (CSV)**.
""")
st.divider()

nombre_medicamento = st.text_input(
    "Ingrese el nombre del medicamento:",
    placeholder="Ejemplo: paracetamol, ibuprofeno..."
)

limit_results = st.slider("Límite de resultados API:", 5, 100, 20)


if nombre_medicamento:
    

    st.subheader(" Disponibilidad en Farmacias (Base de Datos Local)")
    
    if not df_local.empty:
       
        mask_nombre = (
            df_local['Nombre producto comercial'].str.contains(nombre_medicamento, case=False, na=False) |
            df_local['Nombre Material Genérico'].str.contains(nombre_medicamento, case=False, na=False)
        )
        df_filtrado = df_local[mask_nombre].copy()
        
        
        if filtro_comuna != "TODAS":
            df_filtrado = df_filtrado[df_filtrado['Comuna cliente dest'] == filtro_comuna]
            
        
        if filtro_venta != "TODOS":
            df_filtrado = df_filtrado[df_filtrado['Condicion'] == filtro_venta]
        
     
        if not df_filtrado.empty:
            df_display_csv = df_filtrado.drop_duplicates()
            mapa = fl.Map((-33.45694, -70.64827), width=480, height=480)

            for index, item in df_filtrado.iterrows():
                coordenadas: list[str]= item['Coordenadas'][1:-1].split(',')
                fl.Marker(
                    icon=fl.Icon(icon="capsules", color="lightgreen", prefix="fa"),
                    location=[ float(coordenadas[0].strip()[1:-1]), float(coordenadas[1].strip()[1:-1])],
                    tooltip=item["Nombre destinatario"],
                    popup=item['Nombre producto comercial'],
                ).add_to(mapa);
           

            stfl.folium_static(mapa, width=480, height=480)

            cols_mostrar = [
                'Nombre producto comercial', 'Condicion', 
                'Nombre destinatario', 'Direccion dest', 'Comuna cliente dest', 'Cantidad unitaria'
            ]
          
            cols_finales = [c for c in cols_mostrar if c in df_display_csv.columns]
            
            st.success(f"✅ Se encontraron {len(df_display_csv)} registros en farmacias.")
            st.dataframe(df_display_csv[cols_finales], use_container_width=True)
        else:
            st.warning(" No se encontraron resultados en el CSV con los filtros seleccionados.")
    else:
        st.error("No hay datos locales cargados.")

    st.divider()

    st.subheader("📋 Registro Oficial ISP (API Gobierno)")
    
    ID_RECURSO = "8c8124ab-41ee-46c3-b967-c82a09bc592f" 
    URL_API = "https://datos.gob.cl/api/3/action/datastore_search"
    
    params = {
        "resource_id": ID_RECURSO,
        "limit": limit_results,
        "q": nombre_medicamento
    }
    
    try:
        with st.spinner("Consultando API en tiempo real..."):
            response = requests.get(URL_API, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data and data.get("success"):
                records = data["result"]["records"]
                if records:
                    df_api = pd.DataFrame(records)
                    
                   
                    cols_api_map = {
                        'title': 'Nombre Oficial',
                        'registro_sanitario': 'Registro',
                        'titular': 'Laboratorio/Titular',
                        'condicion_venta': 'Condición Venta (API)' 
                    }
                    
                    
                    cols_existentes = {k: v for k, v in cols_api_map.items() if k in df_api.columns}
                    
                    if cols_existentes:
                        df_show_api = df_api[list(cols_existentes.keys())].rename(columns=cols_existentes)
                    else:
                        df_show_api = df_api.iloc[:, :5] 
                    
                    
                    df_show_api = df_show_api.drop_duplicates()

                    st.info(f"ℹ️ Información de referencia: {len(df_show_api)} registros oficiales.")
                    st.dataframe(df_show_api, use_container_width=True)
                else:
                    st.caption("No se encontró información en la API para este término.")
    except Exception as e:
        st.error(f"Error de conexión con la API: {e}")

else:
    st.info("👆 Inicia tu búsqueda arriba.")