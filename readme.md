# Busqueda de medicamentos con streamlit

## Disclaimer!

Siempre consultar con un medico profesional antes de tomar cualquier
medicamento.

## Instrucciones para generar datos

1. python -m venv .\venv
2. Entrar al vEnv pip install -r requirements.txt
3. Descargar datos venta directa:
   https://datos.gob.cl/datastore/dump/8c8124ab-41ee-46c3-b967-c82a09bc592f?bom=True
   y renombrar a "venta directa.csv"
4. Descargar datos facturas farmacias:
   https://drive.google.com/file/d/17aHIjhMserIEl_2l3-RSW2SsZvSXXGbs/view y
   renombrar a "data cenabast.xlsx"
5. Descargar datos coordenadas:
   https://www.ispch.gob.cl/wp-content/uploads/2024/01/Farmacias-Chile-15.01.2024.xlsx
   y renombrar a "direcciones.xlsx"
6. Correr "python modificacion_data.py"
7. Correr "direcciones.py" lo que entrega "con_direcciones.py"
8. Correr sitio Streamlit
