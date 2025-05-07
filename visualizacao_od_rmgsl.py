
import pandas as pd
import plotly.express as px

# Carregar o arquivo CSV
df = pd.read_csv("Pesquisa_Origem_Destino_RMGSL.csv")

# Gerar matriz OD
od_matrix = df.groupby(['Qual o município de ORIGEM', 'Qual o município de DESTINO']).size().reset_index(name='Viagens')
od_matrix_filtered = od_matrix[od_matrix['Viagens'] > 0]

# Coordenadas
municipios_coords = {
    "São Luís": (-2.5307, -44.3068),
    "Paço do Lumiar": (-2.5169, -44.1067),
    "São José de Ribamar": (-2.5600, -44.0620),
    "Raposa": (-2.4264, -44.0978),
    "Alcântara": (-2.4013, -44.4151),
    "Bacabeira": (-2.9647, -44.3164),
    "Morros": (-2.8531, -44.0386),
    "Presidente Juscelino": (-2.9168, -44.0634),
    "Rosário": (-2.9385, -44.2497),
    "FORA DA RMGSL": (-2.7, -44.2),
}

od_matrix_filtered['Origem_lat'] = od_matrix_filtered['Qual o município de ORIGEM'].map(lambda x: municipios_coords.get(x, (None, None))[0])
od_matrix_filtered['Origem_lon'] = od_matrix_filtered['Qual o município de ORIGEM'].map(lambda x: municipios_coords.get(x, (None, None))[1])
od_matrix_filtered['Destino_lat'] = od_matrix_filtered['Qual o município de DESTINO'].map(lambda x: municipios_coords.get(x, (None, None))[0])
od_matrix_filtered['Destino_lon'] = od_matrix_filtered['Qual o município de DESTINO'].map(lambda x: municipios_coords.get(x, (None, None))[1])

# Plot
fig = px.scatter_mapbox(od_matrix_filtered,
                        lat="Origem_lat",
                        lon="Origem_lon",
                        hover_name="Qual o município de ORIGEM",
                        hover_data=["Qual o município de DESTINO", "Viagens"],
                        zoom=8,
                        height=700)

for i, row in od_matrix_filtered.iterrows():
    fig.add_trace(px.line_mapbox(
        lat=[row['Origem_lat'], row['Destino_lat']],
        lon=[row['Origem_lon'], row['Destino_lon']],
        hover_name=[row['Qual o município de ORIGEM'], row['Qual o município de DESTINO']],
    ).data[0])

fig.update_layout(mapbox_style="open-street-map",
                  title="Fluxos OD RMGSL - Pesquisa Eletrônica",
                  showlegend=False)

fig.show()
