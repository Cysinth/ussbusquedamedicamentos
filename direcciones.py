import pandas as pd
from unidecode import unidecode
direcciones = pd.read_excel(".\\direcciones.xlsx")
df = pd.read_csv(".\\modified.csv", delimiter=";")

def remover_numero(direccion):
    return direccion.replace("N° ", "")

direcciones = direcciones[direcciones["Región"] == "METROPOLITANA"]
direcciones = direcciones[["Dirección", "Latitud", "Longitud"]]

direcciones = direcciones.dropna()
direcciones["Dirección"] = direcciones["Dirección"].str.replace(r'\s+', ' ', regex=True)
direcciones["Dirección"] = direcciones["Dirección"].str.replace('-', '')
direcciones["Dirección"] = direcciones["Dirección"].apply(remover_numero)
direcciones['Dirección'] = direcciones['Dirección'].str.casefold()
direcciones["Dirección"] = direcciones["Dirección"].apply(unidecode)


direccion_cache = {}
notfound = set()
def add_fechas(row):
    direccion: str = row["Direccion dest"]
    direccion = direccion.split(",")[0]
    direccion = direccion.replace("AV ", "AVENIDA ")
    direccion = direccion.replace("AVENIDA ", "")
    direccion = direccion.replace("AVDA ", "")
    direccion = direccion.casefold()
    direccion = direccion.replace("ohiggins", "o'higgins")
    direccion = direccion.replace("bdo", "bernardo")
    #direccion = direccion.replace("LOC", "LOCAL")
    #direccion = direccion.replace(", L4", "")
    if direccion in direccion_cache:
        return direccion_cache[direccion]
    
    else:
        direccion_posible = direcciones[direcciones['Dirección'].str.contains(direccion)]
        if len(direccion_posible) > 0:
            direccion_posible = direccion_posible.iloc[0]
            if not direccion_posible["Latitud"] or not direccion_posible["Longitud"]:
                direccion_cache[direccion]= None
                return None
            coordenadas = [direccion_posible["Latitud"].replace(',', ''), direccion_posible["Longitud"].replace(',', '')]
            direccion_cache[direccion] = coordenadas
            return coordenadas
        else: 
            direccion_cache[direccion]= None
            notfound.add(direccion)
            return None

df["Coordenadas"] = df.apply(add_fechas, axis=1)
print(len(notfound))
print(notfound)
df = df.dropna()
df.to_csv(".\\con_direcciones.csv", sep=";")