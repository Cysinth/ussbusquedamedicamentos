import pandas as pd;
import re;

df_directos = pd.read_csv("venta directa.csv", delimiter=";");
generico_cache = {}
def modify_row(row):
    material = row["Nombre Material Genérico"];
    material_base = hasta_numero(material)
    if material_base in generico_cache:
        return "DIRECTA" if generico_cache[material_base] else "NO DIRECTA"
    else: 
        existe = df_directos["Nombre Producto"].str.contains(material_base, case=False, regex=False).any()
        generico_cache[material_base] = existe
        return "DIRECTA" if existe else "NO DIRECTA"

def hasta_numero(texto) -> str:
    parts = re.split(r'\d', texto, 1)
    return parts[0].strip()

df = pd.read_excel(".\\data cenabast.xlsx");
df = df[df["Region cliente dest"] == 13]
df = df[["Fecha Doc", "Cantidad unitaria", "Nombre destinatario", "Direccion dest", "Comuna cliente dest", "Nombre producto comercial", "Nombre Material Genérico" ]]
df["Condicion"] = df.apply(modify_row, axis=1)
df.to_csv(".\\modified.csv", sep=";")
