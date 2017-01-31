import models

f = open('telepules_lista.csv', 'r')

for i in f:
    line1 = i.split("\n")
    line2 = line1[0].split(',')
    print(line2[0],line2[1])
    models.City.create(city_name=line2[0],location=line2[1])
