import streamlit as st
import requests
import pandas as pd
from io import BytesIO

# Configuración visual de la página
st.set_page_config(page_title="Radar B2B SMV", page_icon="🎯", layout="wide")

st.title("🎯 Radar de Prospección Mayorista")
st.markdown("Rastreador de revendedores independientes en Mercado Libre para ofrecer stock físico directo.")
st.markdown("---")

# Interfaz de búsqueda
col1, col2 = st.columns([3, 1])
with col1:
    producto = st.text_input("🔍 ¿Qué producto venden tus futuros clientes? (Ej: JBL Charge 6, S26 Plus):")
with col2:
    limite = st.number_input("Publicaciones a escanear:", min_value=10, max_value=200, value=50, step=10)

# Botón de ejecución
if st.button("🚀 Iniciar Rastreo", type="primary"):
    if producto:
        with st.spinner('Escaneando la base de datos de Mercado Libre...'):
            # Conexión a la API pública con disfraz de navegador (User-Agent)
            url = f"https://api.mercadolibre.com/sites/MLA/search?q={producto}&condition=new&limit={limite}"
            
            cabeceras = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            }
            
            respuesta = requests.get(url, headers=cabeceras)

            if respuesta.status_code == 200:
                datos = respuesta.json()
                resultados = datos.get('results', [])

                lista_vendedores = []

                # Procesamiento de datos
                for item in resultados:
                    # Filtro de oro: ignoramos Tiendas Oficiales
                    if item.get('official_store_id') is None:
                        vendedor = item.get('seller', {})
                        nickname = vendedor.get('nickname', 'Oculto')
                        
                        lista_vendedores.append({
                            "Vendedor (Nickname)": nickname,
                            "Producto Detectado": item.get('title'),
                            "Precio de Venta ($)": item.get('price'),
                            "Link ML": item.get('permalink')
                        })

                if lista_vendedores:
                    # Convertimos la lista a un DataFrame de Pandas
                    df = pd.DataFrame(lista_vendedores)
                    
                    # Limpiamos duplicados para no contactar a la misma persona dos veces
                    df_unicos = df.drop_duplicates(subset=['Vendedor (Nickname)'])
                    
                    st.success(f"✅ ¡Rastreo completo! Se encontraron {len(df_unicos)} posibles clientes únicos.")
                    
                    # Mostramos la tabla en la web
                    st.dataframe(df_unicos, use_container_width=True)

                    # --- Lógica para descargar el Excel ---
                    output = BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        df_unicos.to_excel(writer, index=False, sheet_name='Prospectos')
                    datos_excel = output.getvalue()

                    st.download_button(
                        label="📥 Descargar Base de Datos (Excel)",
                        data=datos_excel,
                        file_name=f"Prospectos_{producto.replace(' ', '_')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.warning("No se encontraron revendedores independientes para este producto en este escaneo.")
            else:
                st.error(f"Error de conexión con Mercado Libre. Código: {respuesta.status_code}")
    else:
        st.warning("Por favor, ingresá una categoría o producto para buscar.")
