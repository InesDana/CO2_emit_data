import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import mapclassify
import folium

df=pd.read_csv('GCB2022v27_MtCO2_flat.csv')
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

#create table with country location information and total cumulative emissions
emissions_total=df[df['Country']!='Global'].groupby(['Country','ISO 3166-1 alpha-3']).sum('Total')
merged_data_total = world.merge(emissions_total, left_on="iso_a3", right_on="ISO 3166-1 alpha-3")

#create table with country location information and averaged per capita emissions
emissions_per_cap=df[df['Country']!='Global'].groupby(['Country','ISO 3166-1 alpha-3']).mean('Per Capita').sort_values('Per Capita',ascending=False)
merged_data_per_cap = world.merge(emissions_per_cap, left_on="iso_a3", right_on="ISO 3166-1 alpha-3")

#map country emissions
m=merged_data_total.explore(column="Total",
                    scheme="quantiles",
                    legend=True,
                    k=10,
                    legend_kwds=dict(colorbar=False, caption="Total cumulative CO2 emissions (Mt), 1750-2021",scale=True),
                    tooltip=['name','Total','Coal','Oil','Gas','Cement','Flaring','Other']
                   )

outfp = r"/Users/dehlert/SQL_tests/CO2_emmissions_by_country/CO2_emit_data/interactive_map_totalCO2emissions.html"

m.save(outfp)


#map country emissions
m1=merged_data_per_cap.explore(column="Per Capita",
                    scheme="quantiles",
                    legend=True,
                    k=10,
                    legend_kwds=dict(colorbar=False, caption="Average per Capita CO2 emissions (Mt), 1750-2021", scale=True),
                    tooltip=['name','Per Capita']
                   )

outfp1 = r"./interactive_map_mean_perCapitaCO2emissions.html"

m1.save(outfp1)