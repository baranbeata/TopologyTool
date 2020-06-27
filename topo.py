# -*- coding: iso-8859-2 -*-
# skrypt topo

import arcpy, os, sys


arcpy.env.overwriteOutput = True

def topo():
    try:

        #inicjowanie niezbednych petli
        liii = []
        lii = []
        li = []
        
        licznik = 0

        #przejecie parametrow od uzytkownika
        folder = arcpy.GetParameterAsText(0)
        nazwa_geo = arcpy.GetParameterAsText(1)
        nazwa_zestaw = arcpy.GetParameterAsText(2)
        shape = arcpy.GetParameterAsText(3)


        #rozdzielenie multiwartosci
        war0 = shape.split(";")

        #utworzenie listy list zawierajacych nazwe warswy, jej zrodlo i odniesienie przestrzenne
        for i in war0:

            desc = arcpy.Describe(i)

            zrodlo = str(desc.path + "\\" + desc.name)

            desc2 = arcpy.Describe( zrodlo )

            lii.append(str(i))
            lii.append(str(zrodlo))
            lii.append(str(desc2.spatialReference.name))
            liii.append(lii)
            lii = []

            licznik += 1   

        #*********************************
        #udalo mi sie utworzyc liste list:
        arcpy.AddWarning(liii)

        #ale pozniej program juz nie chcial ze mna wspolpracowac:


        #arcpy.CreateFileGDB_management(folder, nazwa_geo)
            
        #licz = 0
            
        #for p in liii:
            #arcpy.CreateFeatureDataset_management(folder+"/"+nazwa_geo+".gdb", nazwa_zestaw+str(licz), liii[licz][2] )
            #licz += 1

        #i na razie tego nie mam
        #*********************************

        #***** wersja wrzucajaca wszystko do jednego zestawu danych *****

        war = str(shape).split(";")


        #utworzenie listy zawirajacej wprowadzone przez uzytkownika warstwy, dla ktorych ma zostac stworzona topologia
        for i in war:
            li.append(i)

        #stworzenie geobazy
        arcpy.CreateFileGDB_management(folder, nazwa_geo)
        #stworzenie zestawu danych
        arcpy.CreateFeatureDataset_management(folder+"/"+nazwa_geo+".gdb", nazwa_zestaw)

        #iterator dla petli
        k = 0

        for j in li:
            #przeniesienie klasy obiektów do zestawu w geobazie
            arcpy.FeatureClassToFeatureClass_conversion(folder+"/"+li[k]+".shp",folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw, "shapenowy"+str(k))
            #stworzenie pustej topologii
            arcpy.CreateTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw, "Topology"+str(k))
            #dodanie klasy obiektów do topologii
            arcpy.AddFeatureClassToTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k), folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/shapenowy"+str(k))
            #dodanie regul do topologii
            arcpy.AddRuleToTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k),
                                                "Must Not Intersect (Line)",
                                               folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/shapenowy"+str(k))
            arcpy.AddRuleToTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k),
                                                "Must Not Overlap (Line)",
                                               folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/shapenowy"+str(k))
            arcpy.AddRuleToTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k),
                                                "Must Not Have Pseudo-Nodes (Line)",
                                               folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/shapenowy"+str(k))
            arcpy.AddRuleToTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k),
                                                "Must Not Have Dangles (Line)",
                                               folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/shapenowy"+str(k))
            arcpy.ValidateTopology_management(folder+"/"+nazwa_geo+".gdb"+"/"+nazwa_zestaw+"/Topology"+str(k))
            #inkrementacja iteratora
            k += 1
        
                                           

    except Exception, err:
        arcpy.AddError("Apka nie dziala :(")
        arcpy.AddError(sys.exc_traceback.tb_lineno)
        arcpy.AddError(err.message)

    finally:
        pass

if __name__ == '__main__':
    topo()
