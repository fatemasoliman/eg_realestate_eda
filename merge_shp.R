library(leaflet)
library(dplyr)
library(rgdal)


egprops = read.csv('props_clean.csv')

adm3shp = readOGR(dsn = ".", layer = "egy_admbnda_adm3_capmas_20170421")

adm3shp %>% 
  leaflet() %>% 
  addTiles() %>% 
  addPolygons(popup=~ADM2_EN)


adm2shp = readOGR(dsn = ".", layer = "egy_admbnda_adm2_capmas_20170421")

adm2shp %>% 
  leaflet() %>% 
  addTiles() %>% 
  addPolygons(popup=~ADM2_EN)

