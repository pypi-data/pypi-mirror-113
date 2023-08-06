from xml.etree import cElementTree as ET
import ftputil
import os
import datetime as dt
import time
import calendar
import sys
import math
import subprocess
import getpass



def download():

    # Main functions 
    
    print("<ads4mo>  Copyright (C) <2018>  <Carmelo Sammarco>")
    print("This program comes with ABSOLUTELY NO WARRANTY")
    print("This is free software, and you are welcome to redistribute it under the GPLv3 conditions.")

    def countX(lst, x):
        count = 0
        for ele in a:
            if (ele==x):
                count = count+1
        return count


    def extract_from_link(lista):
        for element in lista:
            e = element.split(' ')[1]
            listnew.append(e)


    def extractstart(listast):
        for element in listast:
            e = element.split(' ')
            styyyymmdd.append(e)


    def extractend(listaend):
        for element in listaend:
            e = element.split(' ')
            endyyyymmdd.append(e)


    def perdelta(st,ed,delta):
        curr=st
        while curr <= ed:
            yield curr
            curr += delta

    def truncate(f, n):
        return math.floor(f * 10 ** n) / 10 ** n


    #Line of code from which I extract the information(examples)
    #string = "--user ##### --pwd ###### --motu http://my.cmems-du.eu/motu-web/Motu --service-id NORTHWESTSHELF_REANALYSIS_PHY_004_009-TDS --product-id MetO-NWS-PHY-mm-CUR --longitude-min -19.888885498046875 --longitude-max 12.999671936035156 --latitude-min 40.06666564941406 --latitude-max 65.0001220703125 --date-min "2016-08-16 12:00:00" --date-max "2016-12-16 12:00:00" --depth-min -1 --depth-max 1  --variable vo --variable uo --out-dir /home/parallels/Desktop --out-name file.nc"
    #string = "--user #### --pwd ##### --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id BALTICSEA_ANALYSIS_FORECAST_WAV_003_010-TDS --product-id dataset-bal-analysis-forecast-wav-hourly --longitude-min 15 --longitude-max 30.207738876342773 --latitude-min 60 --latitude-max 70 --date-min "2017-08-07 03:00:00" --date-max "2017-11-04 12:00:00" --variable VTPK --out-dir /home/parallels/Desktop/xml --out-name file.nc

    # MONTH, DEPTH, DAY, MONTH&DEPTH, YEAR

    cmems_user = getpass.getpass("Please enter your USERNAME: ")
    cmems_pass = getpass.getpass("Please enter your PASSWORD: ")

    #cmems_user = input("Please enter your USERNAME: ")
    #cmems_pass = input("Please enter your PASSWORD: ")

    typology = input("Please enter which type of download | MONTH | DEPTH | DAY | MONTH&DEPTH | YEAR |: ")

    string = input("Based on the selection criteria (showed in the documentation), please input the motuclient script: ")

    hhstart = input("Please to insert the STARTING-TIME as HH:MM:SS. If nothing is inserted the default value of 12:00:00 is going to be used: ")
    if hhstart == "":
        hhstart = "12:00:00"


    hhend = input("Please to insert the ENDING-TIME as HH:MM:SS. If nothing is inserted the default value of 12:00:00 is going to be used: ")
    if hhend == "":
        hhend = "12:00:00"

    print(" ")
    
    Out = str(os.getcwd())

    fname = "none.nc"

    lista = string.split('--')[1:]
    listnew = []
    extract_from_link(lista)
    namenc = fname
    name = namenc.split('.')[0]
    
    a = string.split()
    x = "--variable"
    z = "--depth-max"

    nV = countX(a, x)
    dV = countX(a, z)

    text1 = "The number of variables are = " + str(nV)      
    text2 = "Your request includes DEPTHS[=1] | SURFACE[=0] --> " + "value = " + str(dV)
    text3 = "Please wait... Download in progress using a loop by " + typology 

    print ("#####")
    print (text1)
    print ("#####")
    print (text2)
    print ("#####")
    print (text3)
    print ("#####")

    if typology == "MONTH":

        if dV == 0 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            
            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            
            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start <= date_end):
                    
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]

                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                print(outputname)
                
                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                
                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 1 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            
            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start <= date_end):
                    
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") +" " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"

                print(outputname)
                
                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                

                
                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 0 and nV == 2:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
    
            while (date_start <= date_end):
                
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)
               
                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                

                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 1 and nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start <= date_end):
                
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                

                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 0 and nV == 3:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start <= date_end):
                
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                

                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)


        elif dV == 1 and nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
   
            while (date_start <= date_end):
                
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)
                
                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)   
                os.system(command_string)
                
                time.sleep(2)
                
                date_start = date_end_cmd + dt.timedelta(days=1)

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact Carmelo Sammarco")   



    #################################################################################

    if typology == "DEPTH":

        if nV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            #outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)

            t1= sd[1:11]
            t2= ed[1:11]
 
            tmin = t1 +" " + hhstart
            tmax = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)
            
            for z in listadepth:
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01

                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                #print(command_string)    
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(Out + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")
                
                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"

                    #print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                    #print(command_string)    
                    os.system(command_string)

                    time.sleep(2)

                    print ("---The min/max depth value is corrected---")
                    print ("####################")

        elif nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            #outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1= sd[1:11]
            t2= ed[1:11]

            tmin = t1 +" " + hhstart
            tmax = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)
            
            for z in listadepth: 
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01

                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                #print(command_string)   
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(Out + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")

                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"

                    #print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                    #print(command_string)   
                    os.system(command_string)

                    time.sleep(2)

                    print ("---The min/max depth value is corrected---")
                    print ("####################")


        elif nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            #outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1= sd[1:11]
            t2= ed[1:11]

            tmin = t1 +" " + hhstart
            tmax = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)
            
            for z in listadepth: 
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01

                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                #print(command_string)  
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(Out + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")

                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10]  +"_"+z+"-Depth"+ ".nc"
                    
                    #print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                    #print(command_string) 
                    os.system(command_string)

                    time.sleep(2)
                    print ("---The min/max depth value is corrected---")
                    print ("####################")

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact Carmelo Sammarco") 

            

    ##################################################################################


    if typology == "DAY":

        if nV == 1 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Out + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] +  ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                    #print(command_string)  
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break 

        
        elif nV == 2 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])
                
            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

                with open (Out + "/listdate.txt") as f:
                        
                    while True:

                        line = f.readline()
                        date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                        date_min = date_cmd[0]
                        date_max = date_cmd[1]

                        outputname = "CMEMS_" + date_min[0:10]  + ".nc"

                        print(outputname)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                        #print(command_string)  
                        os.system(command_string)

                        time.sleep(2)

                        if not line: 
                            break 


        elif nV == 3 and dV == 0:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(od)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])
                
            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Out + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                    #print(command_string)  
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break 

                        

        elif nV == 1 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])
                
            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Out + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] +  ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                    #print(command_string)  
                    os.system(command_string)

                    time.sleep(2)

                    if not line:
                        break 



        elif nV == 2 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])
                
            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Out + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1)  + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                    #print(command_string) 
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break 

        elif nV == 3 and dV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]

            #print (t1)
            #print (t2)
                
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            #print(date_min)
            #print (date_max)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                    
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])
                
            hhstartdaily = hhstart
            hhenddaily = hhend

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
                
            with open (Out + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Out + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstartdaily , line[0:10] +" " + " " + hhenddaily
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1)  + " --variable " + str(variable2)  + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                    #print(command_string)  
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break 

    #############################################################################

    if typology == "MONTH&DEPTH":

        #stringxml = "python -m motuclient " + string + " --out-dir " + Out + " --out-name " + name + ".nc"  + " --describe-product"
        #print (stringxml)
        #os.system(stringxml)
        #tree = ET.parse( Out + "/" + name + ".xml")
        #root = tree.getroot()
        #depth = root[2].text
        #listadepth = depth.split(';')
        #print (listadepth)

        if nV == 1:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
                
                for z in listadepth: 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01
            
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                    #print(command_string)  
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(Out + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        #print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                        #print(command_string)  
                        os.system(command_string)

                        time.sleep(2)

                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)
        
        elif nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
                
                for z in listadepth: 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01
            
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                    #print(command_string) 
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(Out + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        #print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                        #print(command_string) 
                        os.system(command_string)

                        time.sleep(2)

                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)

        elif nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            stringxml = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + "name.nc"  + " --describe-product"
            #print (stringxml)
            os.system(stringxml)
            tree = ET.parse( Out + "/" + "name.xml" )
            root = tree.getroot()
            depth = root[2].text
            listadepth = depth.split(';')
            #print (listadepth)

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
                
                for z in listadepth: 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01
            
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname1)

                    #print(command_string) 
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(Out + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        #print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname2)

                        #print(command_string) 
                        os.system(command_string)

                        time.sleep(2)

                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)
        
        
        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact Carmelo Sammarco")

    ############################################################################################

    if typology == "YEAR":

        if dV == 0 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format
            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start < date_end):
            #while (date_start <= date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year +1, date_start.month, calendar.monthrange(date_start.year, date_start.month)[1]))
                
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)  
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)
                #date_start = date_end_cmd + dt.timedelta(days=365)
                    



        elif dV == 1 and nV == 1:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start < date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)



        elif dV == 0 and nV == 2:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
  
            while (date_start < date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string) 
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)



        elif dV == 1 and nV == 2:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start < date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)



        elif dV == 0 and nV == 3:
            
            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start < date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string) 
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)


        elif dV == 1 and nV == 3:

            lista = string.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,od,on,Us,Pw = listnew

            #and then finally I obtain the Parameters in the correct format

            #cmems_user = str(Us)
            #cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            #outputdir = str(Outdir)
            outputname = str(fname)
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            depth_min = float(dmin)
            depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
            
            t1 = sd[1:11]
            t2 = ed[1:11]
            
            date_min = t1 +" " + hhstart
            date_max = t2+" " + hhend

            styyyymmdd = []
            endyyyymmdd = []

            listast = t1.split('-')
            listaend = t2.split('-')
                
            extractstart(listast) 
            extractend(listaend)

            yyyystart,mmstart,dds = styyyymmdd
            yyyyend,mmend,dde = endyyyymmdd

            year1 = int(yyyystart[0])
            month1 = int(mmstart[0])
            d1 = int(dds[0])

            year2 = int(yyyyend[0])
            month2 = int(mmend[0])
            d2 = int(dde[0])

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
                
            while (date_start < date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))

                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Out) + " --out-name " + str(outputname)

                #print(command_string)
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)

        else:
            print("ERROR: Number of variables not supported. If you need more variables please to contact Carmelo Sammarco")  
