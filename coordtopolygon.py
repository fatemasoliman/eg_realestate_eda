import PyShp as shp
from shapely.geometry import Point
import csv
from shapely.geometry.polygon import Polygon

fileName = 'props_clean.csv'                #Open CSV file with points to check   
sf = shp.Reader("egy_admbnda_adm2_capmas_20170421.shp")   #Open Shapefile with shapes to check points against
sfRec = sf.records() #Read records in shapefile

n = 0
m = 1
coor = ''
coorDict = {}
matplotDict = []
muniFinal = {}

for shape in sf.shapeRecords(): #Iterate through shapes in shapefile
    x = [i[0] for i in shape.shape.points[:]] #Initially for use in matplotlib to check shapefile
    y = [i[1] for i in shape.shape.points[:]] #Initially for use in matplotlib to check shapefile
    for i in x:
        matplotDict.append((x[x.index(i)],y[x.index(i)])) #Convert coordinates to be read by Shapely pkg

    munishp = Polygon(matplotDict)
    muniFinal[sfRec[n][1]] = munishp #Store shape in dictionary with key of municipality

    matplotDict = [] #refresh coordinate store for next shape   
    n += 1 


n = 0    



with open(fileName + '.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:

        coor = (row['latitude'],row['longitude'])
        rlat = float(row['latitude'])
        rlong = float(row['longitude'])
        if coor == ' ,   ' or coor == ', ':
            coorDict[row['PrimaryKey']] = 'No Data' #PrimaryKey is my primary key that I will use to write the data back into the .csv 
        else:
            if float(row['longitude']) > 0:
                coorDict[row['PrimaryKey']] = (rlat,rlong)
            else:
                coorDict[row['PrimaryKey']] = (rlong,rlat)
        m += 1

#proof of concept- save the results however you'd like
for j in coorDict:
    for k in muniFinal:
        if muniFinal[k].contains(Point(coorDict[j])):
            print(j, 'in', k)