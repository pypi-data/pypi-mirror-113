#####################################################################
#Programm author: Carmelo Sammarco
#####################################################################

#<CADS - Python Package to add new download services to Copernicus and make easier managing voluminous data requests.>
#Copyright (C) <2021>  <Carmelo Sammarco>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>
#####################################################################

#Import modules 
import pkg_resources
from xml.etree import cElementTree as ET
import xarray as xr
import pandas as pd
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import Scrollbar
import datetime as dt
import time
import calendar
import math
from ftplib import FTP
import xarray as xr
import pandas as pd
import os
import json
import platform


def main(args=None):
    
    window = Tk()

    image = pkg_resources.resource_filename('CADS', 'DATA/LOGO.gif')
    photo = PhotoImage(file=image)
    w = photo.width()
    h = photo.height()
    cv = Canvas(window, width=w, height=h)
    cv.pack(side='top', fill='x')
    cv.create_image(0,0, image=photo, anchor='nw') 

    tab_control = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control)
    tab2 = ttk.Frame(tab_control)
    tab3 = ttk.Frame(tab_control)
    tab_control.add(tab1, text='Motuclient data request')
    tab_control.add(tab2, text='FTP data request')
    tab_control.add(tab3, text='FTP data request AVS')

    window.title("CADS-by-Carmelo-Sammarco")

    OS = platform.system()
    # if OS=="Linux":
    #     window.geometry('450x450')
    # elif OS=="Darwin":
    #     window.geometry('500x680')
    # else:
    #     window.geometry('365x565')
    
    filejason =  pkg_resources.resource_filename('CADS', 'Database/CMEMS_Database.json')
    filejasonselvar =  pkg_resources.resource_filename('CADS', 'Database/CMEMS_Databaseselvar.json')

    
    #################
    #TAB 1 
    #Functions
    #################

    Voutmc1 = StringVar()

    def Outputmotuclient1():
        outMC1 = filedialog.askdirectory() 
        Voutmc1.set(outMC1)

    def downloadmotu1():
        inputValue = txt1.get("1.0","end")
        #print (inputValue)
        os.system(inputValue)


    #################################################
    #For download mechanisms

    a = []
    listnew=[]
    styyyymmdd=[]
    endyyyymmdd=[]
    lines = []
    x = "--variable"
    z = "--depth-max"
    hhstart = str()
    hhend = str()

    ########################
    #Download daily
    ########################

    def downloaddaily():

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

        #################
        #generation days from interval  
        def perdelta(st,ed,delta):
            curr=st
            while curr <= ed:
                yield curr
                curr += delta
        
        #################

        inputValue = txt1.get("1.21",'end-1c')
        print (inputValue)
        a = inputValue.split()
        #print(a)
        nV = countX(a, x)
        dV = countX(a, z)
        #print(nV)
        #print(dV)


        if dV == 0 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
        
            t1 = sd[0:10]
            t2 = ed[0:10]

            #print (t1)
            #print (t2)
            
            date_min = t1 +" 00:00:00"
            date_max = t2 +" 00:00:00"

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
            
            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Voutmc1.get() + "/listdate.txt") as f:
                    
                while True:

                    line = f.readline()
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break   
             

        elif dV == 1 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)

            with open (Voutmc1.get() + "/listdate.txt") as f:

                while True:

                    line = f.readline()  
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    if not line:
                        break


        elif dV == 0 and nV == 2:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)
             
            with open (Voutmc1.get() + "/listdate.txt") as f:

                while True:

                    line = f.readline()  
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                            
                    os.system(command_string)

                    time.sleep(2)

                    if not line:
                        break


        elif dV == 1 and nV == 2:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)
 
            with open (Voutmc1.get() + "/listdate.txt") as f:

                while True:

                    line = f.readline() 
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1)  + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    if not line: 
                        break


        elif dV == 0 and nV == 3:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)
 
            with open (Voutmc1.get() + "/listdate.txt") as f:

                while True:

                    line = f.readline()  
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    if not line:
                        break



        elif dV == 1 and nV == 3:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstart = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            start = dt.datetime(year1,month1,d1,0,0)
            end = dt.datetime(year2,month2,d2,0,0)
            delta = dt.timedelta(days=1)
            
            with open (Voutmc1.get() + "/listdate.txt", 'w') as f:
                for result in perdelta(start,end, delta):
                    print (result, file=f)
 
            with open (Voutmc1.get() + "/listdate.txt") as f:

                while True:

                    line = f.readline() 
                    date_cmd =  line[0:10] +" " +" " + hhstart , line[0:10] +" " + " " + hhend
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                    print(outputname)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1)  + " --variable " + str(variable2)  + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    if not line:
                        break


    #######################
    #Download MONTHLY!! 
    #######################

    def downloadmotumontly1():

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
    

        inputValue = txt1.get("1.21",'end-1c')
        print (inputValue)
        a = inputValue.split()
        #print(a)
        nV = countX(a, x)
        dV = countX(a, z)
        #print(nV)
        #print(dV)


        if dV == 0 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
        
            t1 = sd[0:10]
            t2 = ed[0:10]

            #print (t1)
            #print (t2)
            
            date_min = t1 +" 00:00:00"
            date_max = t2 +" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart ,  date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend

                print (date_end_cmd)
                print (date_cmd)
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)


        elif dV == 1 and nV == 1:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)


        elif dV == 0 and nV == 2:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)


        elif dV == 1 and nV == 2:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 0 and nV == 3:
        
            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            variable1 = str(v1)
            variable2 = str(v2)
            variable3 = str(v3)

            outputdir = str(Outdir)
            outputname = "NONE"
            motu_server = str(Mot)
            product_id = str(Pr)
            dataset_id = str(Ds)

            #depth_min = float(dmin)
            #depth_max = float(dmax)

            lon_min = float(Longmin)
            lon_max = float(Longmax)
            lat_min = float(Latmin)
            lat_max = float(Latmax)
        
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)



        elif dV == 1 and nV == 3:

            lista = inputValue.split('--')[1:]

            listnew = []

            extract_from_link(lista)

            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
            outputname = "NONE"
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            date_min = t1 +" 00:00:00"
            date_max = t2+" 00:00:00"

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

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)
            
            while (date_start <= date_end):
            
                date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                date_cmd =  date_start.strftime("%Y-%m-%d") +" "+ hhstart , date_end_cmd.strftime("%Y-%m-%d") +" "+ hhend 
                
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id + ".nc"

                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_end_cmd + dt.timedelta(days=1)

    #######################
    #Download By DEPTH!! 
    #######################

    def downloadbydepth1():

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

        
        info = "--describe-product"
        inputValue = txt1.get("1.0","end-1c") +" "+ info
        print (inputValue)
        os.system(inputValue)

        modname = fname1.get()[:-3]
        #print (modname)

        tree = ET.parse(Voutmc1.get()+"/"+ modname + ".xml")
        root = tree.getroot()
        depth = root[2].text
        listadepth = []
        listadepth = depth.split(';')
        #print (listadepth)

        inputValue = txt1.get("1.21",'end-1c')
        #print (inputValue)
        a = inputValue.split()
        nV = countX(a, x)
        

        if nV == 1:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            for z in listadepth:

                def truncate(f, n):
                    return math.floor(f * 10 ** n) / 10 ** n 
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01
    
                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(outputdir + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")

                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"
                    
                    print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                    
                    print ("---The min/max depth value is corrected---")
                    print ("####################")
                   
    
        elif nV == 2:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            for z in listadepth:

                def truncate(f, n):
                    return math.floor(f * 10 ** n) / 10 ** n 
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01
    
                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(outputdir + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")

                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"

                    print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    print ("---The min/max depth value is corrected---")
                    print ("####################")


        elif nV == 3:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            proxy_user = None
            proxy_pass = None
            proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            for z in listadepth:

                def truncate(f, n):
                    return math.floor(f * 10 ** n) / 10 ** n 
                
                zformat = truncate(float(z), 2)
                z1 = zformat
                z2 = float(zformat) + 0.01
    
                outputname1 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"
                
                print(outputname1)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)

                exsist = os.path.isfile(outputdir + "/" + outputname1 )

                if exsist:
                    print("---The depth correction is not required---")
                    print ("####################")

                else:
                    outputname2 = "CMEMS_" + tmin[0:10] + "_"+ tmax[0:10] + "_" + "numVar["+ str(nV) +"]_" + product_id + "_" + dataset_id +"-Depth=" +z +".nc"
                    
                    print(outputname2)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    print ("---The min/max depth value is corrected---")
                    print ("####################")



    #######################
    #Download By MONTH+DEPTH
    #######################

    def downloadbydepthMonth():

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

        
        info = "--describe-product"
        inputValue = txt1.get("1.0","end-1c") +" "+ info
        print (inputValue)
        os.system(inputValue)

        modname = fname1.get()[:-3]
        #print (modname)

        tree = ET.parse(Voutmc1.get()+"/"+ modname + ".xml")
        root = tree.getroot()
        depth = root[2].text
        listadepth = []
        listadepth = depth.split(';')
        #print (listadepth)

        inputValue = txt1.get("1.21",'end-1c')
        #print (inputValue)
        a = inputValue.split()
        nV = countX(a, x)
        

        if nV == 1:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            #############################
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
            #############################

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
            
                for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(outputdir + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                        print(command_string)
                            
                        os.system(command_string)

                        time.sleep(2)
                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)
                
                   
    
        elif nV == 2:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            #############################
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
            #############################

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
            
                for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    
                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(outputdir + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                        print(command_string)
                            
                        os.system(command_string)

                        time.sleep(2)
                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)



        elif nV == 3:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format

            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1= sd[0:10]
            t2= ed[0:10]

            #############################
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
            #############################

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend
            
            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start <= date_end):
            
                for z in listadepth:

                    def truncate(f, n):
                        return math.floor(f * 10 ** n) / 10 ** n 
                    
                    zformat = truncate(float(z), 2)
                    z1 = zformat
                    z2 = float(zformat) + 0.01

                    date_end_cmd = (dt.datetime(date_start.year, date_start.month,calendar.monthrange(date_start.year, date_start.month)[1]))
                    date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") + " " + hhend 
                
                    date_min = date_cmd[0]
                    date_max = date_cmd[1]

                    outputname1 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + "_"+z+"-Depth"+".nc"
                
                    print(outputname1)

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z) + " --depth-max " + str(z) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname1)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)

                    exsist = os.path.isfile(outputdir + "/" + outputname1 )

                    if exsist:
                        print("---The depth correction is not required---")
                        print ("####################")

                    else:
                        outputname2 = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] +"_"+z+"-Depth"+ ".nc"

                        print(outputname2)

                        command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(tmin) +  " --date-max " + str(tmax) + " --depth-min " + str(z1) + " --depth-max " + str(z2) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname2)

                        print(command_string)
                            
                        os.system(command_string)

                        time.sleep(2)

                        print ("---The min/max depth value is corrected---")
                        print ("####################")

                    date_start = date_end_cmd + dt.timedelta(days=1)

                
    
    #######################
    #Download By Year
    #######################

    def downloadYearly():

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
    

        inputValue = txt1.get("1.21",'end-1c')
        print (inputValue)
        a = inputValue.split()
        #print(a)
        nV = countX(a, x)
        dV = countX(a, z)
        #print(nV)
        #print(dV)


        if dV == 0 and nV == 1:

            lista = inputValue.split('--')[1:]
            listnew = []
            extract_from_link(lista)
            Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,Outdir,fname = listnew

            #and then finally I obtain the Parameters in the correct format
            cmems_user = str(Us)
            cmems_pass = str(Pw)

            #proxy_user = None
            #proxy_pass = None
            #proxy_server = None

            outputdir = str(Outdir)
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
            
            t1 = sd[0:10]
            t2 = ed[0:10]
            
            #############################
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
            #############################

            hhstar = str(hhstartentry.get())
            hhend = str(hhendentry.get())

            tmin = t1 + " " + hhstar
            tmax = t2 + " " + hhend

            date_start = dt.datetime(year1,month1,d1,0,0)
            date_end = dt.datetime(year2,month2,d2,0,0)

            while (date_start < date_end):
            #while (date_start <= date_end):

                date_end_cmd = date_start + dt.timedelta(days=365)
                #date_end_cmd = (dt.datetime(date_start.year +1, date_start.month, calendar.monthrange(date_start.year, date_start.month)[1]))
                
                date_cmd =  date_start.strftime("%Y-%m-%d") + " " + hhstart , date_end_cmd.strftime("%Y-%m-%d") +  " " + hhend 
            
                date_min = date_cmd[0]
                date_max = date_cmd[1]
                outputname = "CMEMS_" + date_min[0:10] + "_"+ date_max[0:10] + ".nc"
            
                print(outputname)

                command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                print(command_string)
                    
                os.system(command_string)

                time.sleep(2)
            
                date_start = date_start + dt.timedelta(days=365)
                #date_start = date_end_cmd + dt.timedelta(days=365)

            

            if dV == 1 and nV == 1:

                lista = inputValue.split('--')[1:]
                listnew = []
                extract_from_link(lista)
                Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,Outdir,fname = listnew

                #and then finally I obtain the Parameters in the correct format
                cmems_user = str(Us)
                cmems_pass = str(Pw)

                #proxy_user = None
                #proxy_pass = None
                #proxy_server = None

                outputdir = str(Outdir)
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
                
                t1 = sd[0:10]
                t2 = ed[0:10]
                
                #############################
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
                #############################

                hhstar = str(hhstartentry.get())
                hhend = str(hhendentry.get())

                tmin = t1 + " " + hhstar
                tmax = t2 + " " + hhend

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

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                
                    date_start = date_start + dt.timedelta(days=365)
                    #date_start = date_end_cmd + dt.timedelta(days=365)


            if dV == 0 and nV == 2:

                lista = inputValue.split('--')[1:]
                listnew = []
                extract_from_link(lista)
                Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,Outdir,fname = listnew

                #and then finally I obtain the Parameters in the correct format
                cmems_user = str(Us)
                cmems_pass = str(Pw)

                #proxy_user = None
                #proxy_pass = None
                #proxy_server = None

                outputdir = str(Outdir)
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
                
                t1 = sd[0:10]
                t2 = ed[0:10]
                
                #############################
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
                #############################

                hhstar = str(hhstartentry.get())
                hhend = str(hhendentry.get())

                tmin = t1 + " " + hhstar
                tmax = t2 + " " + hhend

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

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                
                    date_start = date_start + dt.timedelta(days=365)
                    #date_start = date_end_cmd + dt.timedelta(days=365)

            

            if dV == 1 and nV == 2:

                lista = inputValue.split('--')[1:]
                listnew = []
                extract_from_link(lista)
                Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,Outdir,fname = listnew

                #and then finally I obtain the Parameters in the correct format
                cmems_user = str(Us)
                cmems_pass = str(Pw)

                #proxy_user = None
                #proxy_pass = None
                #proxy_server = None

                outputdir = str(Outdir)
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
                
                t1 = sd[0:10]
                t2 = ed[0:10]
                
                #############################
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
                #############################

                hhstar = str(hhstartentry.get())
                hhend = str(hhendentry.get())

                tmin = t1 + " " + hhstar
                tmax = t2 + " " + hhend

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

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                
                    date_start = date_start + dt.timedelta(days=365)
                    #date_start = date_end_cmd + dt.timedelta(days=365)



            if dV == 0 and nV == 3:

                lista = inputValue.split('--')[1:]
                listnew = []
                extract_from_link(lista)
                Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,v1,v2,v3,Outdir,fname = listnew

                #and then finally I obtain the Parameters in the correct format
                cmems_user = str(Us)
                cmems_pass = str(Pw)

                proxy_user = None
                proxy_pass = None
                proxy_server = None

                outputdir = str(Outdir)
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
                
                t1 = sd[0:10]
                t2 = ed[0:10]
                
                #############################
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
                #############################

                hhstar = str(hhstartentry.get())
                hhend = str(hhendentry.get())

                tmin = t1 + " " + hhstar
                tmax = t2 + " " + hhend

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

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) +" --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                
                    date_start = date_start + dt.timedelta(days=365)
                    #date_start = date_end_cmd + dt.timedelta(days=365)

            

            if dV == 1 and nV == 3:

                lista = inputValue.split('--')[1:]
                listnew = []
                extract_from_link(lista)
                Us,Pw,Mot,Pr,Ds,Longmin,Longmax,Latmin,Latmax,sd,ed,dmin,dmax,v1,v2,v3,Outdir,fname = listnew

                #and then finally I obtain the Parameters in the correct format
                cmems_user = str(Us)
                cmems_pass = str(Pw)

                proxy_user = None
                proxy_pass = None
                proxy_server = None

                outputdir = str(Outdir)
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
                
                t1 = sd[0:10]
                t2 = ed[0:10]
                
                #############################
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
                #############################

                hhstar = str(hhstartentry.get())
                hhend = str(hhendentry.get())

                tmin = t1 + " " + hhstar
                tmax = t2 + " " + hhend

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

                    command_string = "python -m motuclient --user " + str(cmems_user) + " --pwd " + str(cmems_pass) + " --motu " + str(motu_server) + " --service-id " + str(product_id) + " --product-id " + str(dataset_id)  + " --longitude-min " + str(lon_min) + " --longitude-max " + str(lon_max) + " --latitude-min " + str(lat_min) + " --latitude-max "  + str(lat_max) + " --date-min " + str(date_min) +  " --date-max " + str(date_max) + " --depth-min " + str(depth_min) + " --depth-max " + str(depth_max) + " --variable " + str(variable1) + " --variable " + str(variable2) + " --variable " + str(variable3) + " --out-dir " + str(Outdir) + " --out-name " + str(outputname)

                    print(command_string)
                        
                    os.system(command_string)

                    time.sleep(2)
                    
                    date_start = date_start + dt.timedelta(days=365)
                    #date_start = date_end_cmd + dt.timedelta(days=365)
        
    
    
    
    #########################################
    # LOGIC TO GENERATE LINK for DOWNLOAD....

    dmi1 = StringVar()
    dma1 = StringVar()
    padd1 = StringVar()
    nrt = StringVar()
    my = StringVar()
    sd = StringVar()
    ed = StringVar()

    def gennrt():


        if len(dmin1.get()) == 0 : 
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), Voutmc1.get(), fname1.get()))
            
            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(),  ed.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))

        
        elif len(dmin1.get()) != 0 :  
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :


                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), Voutmc1.get(), fname1.get()))

            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else  :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://nrt.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))


    def genmuy():

        if len(dmin1.get()) == 0 : 
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), Voutmc1.get(), fname1.get()))
            
            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))

        
        elif len(dmin1.get()) != 0 :  
            
            if len(V11.get()) != 0 and len(V12.get()) == 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), Voutmc1.get(), fname1.get()))

            elif len(V11.get()) != 0 and len(V12.get()) != 0 and len(V13.get()) == 0 :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), Voutmc1.get(), fname1.get()))

            else  :

                sd.set(sd1.get()+" "+hhstartentry.get())
                ed.set(ed1.get()+" "+hhendentry.get())

                padd1.set("-TDS")
                nrt.set("http://my.cmems-du.eu/motu-web/Motu")
                dmi1.set("--depth-min")
                dma1.set("--depth-max")
                #with motoclient path as variable
                #txt.insert(INSERT,"python %s/motu-client.py --user %s --pwd %s --motu http://nrt.cmems-du.eu/motu-web/Motu --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --out-dir %s --out-name %s" % (Vpathmc.get(), User.get(), Pwd.get(), Pd.get(), padd.get(), Ds.get(), lomin.get(), lomax.get(), lamin.get(), lamax.get(), sd.get(), ed.get(), dmi.get(), dmin.get(), dma.get(), dmax.get(), V1.get(), Voutmc.get(), fname.get()))
                txt1.insert(INSERT,"python -m motuclient --user %s --pwd %s --motu %s --service-id %s%s --product-id %s --longitude-min %s --longitude-max %s --latitude-min %s --latitude-max %s --date-min %s --date-max %s  %s %s  %s %s --variable %s --variable %s --variable %s --out-dir %s --out-name %s" % (User1.get(), Pwd1.get(), nrt.get(), Pd1.get(), padd1.get(), Ds1.get(), lomin1.get(), lomax1.get(), lamin1.get(), lamax1.get(), sd.get(), ed.get(), dmi1.get(), dmin1.get(), dma1.get(), dmax1.get(), V11.get(), V12.get(), V13.get(), Voutmc1.get(), fname1.get()))


    ############
    # To Clen the Link generated for download 

    def genclean1():
        txt1.delete(1.0,END)

    #END FUNCTIONS###
    ############################

    Username1 = Label(tab1, text="Username")
    Username1.grid(column=0, row=0)
    User1 = Entry(tab1, width=13)
    User1.grid(column=0, row=1)
    ##
    Password1 = Label(tab1, text="Password")
    Password1.grid(column=1, row=0)
    Pwd1 = Entry(tab1, width=13, show="*")
    Pwd1.grid(column=1, row=1)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=2)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=2)
    ##
    Product1 = Label(tab1, text="Product")
    Product1.grid(column=0, row=3)
    Pd1 = Entry(tab1, width=13)
    Pd1.grid(column=0, row=4)
    ##
    Dataset1 = Label(tab1, text="Dataset")
    Dataset1.grid(column=1, row=3)
    Ds1 = Entry(tab1, width=13)
    Ds1.grid(column=1, row=4)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=5)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=5)
    ##
    longmin1 = Label(tab1, text="Long min")
    longmin1.grid(column=0, row=6)
    lomin1 = Entry(tab1, width=13)
    lomin1.grid(column=0, row=7)
    ##
    longmax1 = Label(tab1, text="Long max")
    longmax1.grid(column=1, row=6)
    lomax1 = Entry(tab1, width=13)
    lomax1.grid(column=1, row=7)
    ##
    latmin1 = Label(tab1, text="Lat min")
    latmin1.grid(column=0, row=8)
    lamin1 = Entry(tab1, width=13)
    lamin1.grid(column=0, row=9)
    ##
    latmax1 = Label(tab1, text="Lat max")
    latmax1.grid(column=1, row=8)
    lamax1 = Entry(tab1, width=13)
    lamax1.grid(column=1, row=9)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=10)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=10)
    ##
    depthmin1 = Label(tab1, text="Depth min")
    depthmin1.grid(column=0, row=11)
    dmin1 = Entry(tab1, width=13)
    dmin1.grid(column=0, row=12)
    ##
    depthmax1 = Label(tab1, text="Depth max")
    depthmax1.grid(column=1, row=11)
    dmax1 = Entry(tab1, width=13)
    dmax1.grid(column=1, row=12)
    ##
    space1 = Label(tab1, text=" ")
    space1.grid(column=0, row=13)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=13)
    ##
    stardate1 = Label(tab1, text="From date: YYYY-MM-DD")
    stardate1.grid(column=0, row=14)
    sd1 = Entry(tab1, width=13)
    sd1.grid(column=0, row=15)
    ##
    enddate1 = Label(tab1, text="To date: YYYY-MM-DD")
    enddate1.grid(column=1, row=14)
    ed1 = Entry(tab1, width=13)
    ed1.grid(column=1, row=15)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=16)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=16)
    ##
    hourdate1 = Label(tab1, text="From time: HH:MM:SS")
    hourdate1.grid(column=0, row=17)
    hhstartentry = Entry(tab1, width=13)
    hhstartentry.grid(column=0, row=18)
    ##
    houredate1 = Label(tab1, text="To time: HH:MM:SS")
    houredate1.grid(column=1, row=17)
    hhendentry = Entry(tab1, width=13)
    hhendentry.grid(column=1, row=18)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=19)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=19)
    ##
    Variable1 = Label(tab1, text="Variable-1")
    Variable1.grid(column=0, row=20)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=21)
    ##
    Variable2 = Label(tab1, text="Variable-2")
    Variable2.grid(column=0, row=22)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=23)
    ##
    Variable3 = Label(tab1, text="Variable-3")
    Variable3.grid(column=0, row=24)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=25)

    ##
    V11 = Entry(tab1, width=13)
    V11.grid(column=1, row=20)

    V12 = Entry(tab1, width=13)
    V12.grid(column=1, row=22)

    V13 = Entry(tab1, width=13)
    V13.grid(column=1, row=24)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=25)
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=25)
    ##
    filename1 = Label(tab1, text="File name")
    filename1.grid(column=0, row=26)
    fname1 = Entry(tab1, width=13)
    fname1.grid(column=1, row=26)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=27)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=27)
    ##
    space1 = Label(tab1, text="")
    space1.grid(column=0, row=28)
    space1 = Label(tab1, text="")
    space1.grid(column=1, row=28)
    #
    btn1 = Button(tab1, text="Link-NRT", bg="green", command=gennrt)
    btn1.grid(column=1, row=29)
    ##
    btn1 = Button(tab1, text="Link-MY", bg="green", command=genmuy)
    btn1.grid(column=1, row=30)
    ##
    txt1 = scrolledtext.ScrolledText(tab1,width=45,height=10)
    txt1.grid(column=1,row=31)
    ##
    Out1 = Button(tab1, text="Out-DIR", bg="yellow", command=Outputmotuclient1)
    Out1.grid(column=0, row=31)
    ##
    btn1 = Button(tab1, text="Clean-link", bg="white", command=genclean1)
    btn1.grid(column=1, row=32)
    ##
    btn1 = Button(tab1, text="Download Single-file", bg="red", command=downloadmotu1)
    btn1.grid(column=0, row=33)
    ##
    btn1 = Button(tab1, text="Download Montly", bg="red", command=downloadmotumontly1)
    btn1.grid(column=0, row=34)
    ###
    btn1 = Button(tab1, text="Download Daily", bg="red", command=downloaddaily)
    btn1.grid(column=0, row=35)
    ###
    btn1 = Button(tab1, text="Download by Depths", bg="red", command=downloadbydepth1)
    btn1.grid(column=0, row=36)
    ###
    btn1 = Button(tab1, text="Download by Month&Depth", bg="red", command=downloadbydepthMonth)
    btn1.grid(column=0, row=37)
    ###
    btn1 = Button(tab1, text="Download by Years", bg="red", command=downloadYearly)
    btn1.grid(column=0, row=38)
    ###
    #space1 = Label(tab1, text="")
    #space1.grid(column=0, row=39)
    ##
    
    
    
    ########################################
    #TAB 2
    #FUNCTIONS
    ###########

    def FTPsub():

        ##########################
        # CMEMS LOGIN CREDENTIAL #
        ##########################

        cmems_user = User.get()         
        cmems_pass = Pwd.get() 

        #########################
        # FTP SEARCH PARAMETERS #
        #########################

        pathfiles = FTPlk.get()

        #########################
        # SELECTION TIME WINDOW #
        #########################

        datastart = Ds.get()  
        dataend = De.get()     

        ############################
        # Bounding box information #
        ############################

        bbox = bb.get()  #(YES/NO)

        lon1 = float(lomin.get())     #(WEST)
        lon2 = float(lomax.get())     #(EAST)
        lat1 = float(lamin.get())     #(SOUTH)
        lat2 = float(lamax.get())     #(NORTH)


        #######################
        # SELECTION VARIABLES #
        #######################

        Vs = Vex.get()  #(YES/NO)

        variables = Vexlist.get()
        variableslist = variables.split(',')

        #####################
        # DEPTH INFORMATION #
        #####################

        DL = Dex.get()           #(YES/NO)

        RangeD = Dtype.get()    #(SINGLE/RANGE)

        #For "SINGLE" DEPTH extraction
        depth = sdepth.get()          

        #For "RANGE" DEPTHs extraction
        d1 = Rdepthmin.get()            
        d2 = Rdepthmax.get()

        #################
        # ROOT FOLDER #
        #################
  
        outpath = str(os.getcwd())  

        #########################################################
        # Few important points  before the start of the options #
        #########################################################

        typo = StringVar()
        structure = StringVar()
        ID = StringVar()
        Toidentify = StringVar()
        Pname = StringVar()

        Database = {}
        with open (filejason, "r") as config_file:
            Database = json.load(config_file)
            for key in Database.keys(): 
                if pathfiles in key:
                    #print(pathfiles)
                    
                    listdic = Database.get(pathfiles) 
                    #print(listdic)

                    typo = listdic[0] #(NRT/MY)
                    structure = listdic[1]  #M(monthly)/D(daily)  
                    ID = listdic[2]  #(BACK/FRONT)
                    Toidentify = listdic[3]   #part of the fine name used to select the files  

                    Pname = pathfiles.split("/")[2]

        #########################

        ys, ms, ds = datastart.split('-')
        ye, me, de = dataend.split('-')

        sdata = ys + "-" + ms
        edata = ye + "-" + me

        days = pd.date_range(datastart, dataend, freq='D')
        months = pd.date_range(*(pd.to_datetime([sdata, edata]) + pd.offsets.MonthEnd()), freq='M')


        SPECdatasets = ["/Core/OCEANCOLOUR_ARC_CHL_L4_REP_OBSERVATIONS_009_088/dataset-oc-arc-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_ATL_CHL_L4_REP_OBSERVATIONS_009_091/dataset-oc-atl-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_BS_CHL_L4_REP_OBSERVATIONS_009_079/dataset-oc-bs-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_100km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_25km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_093/dataset-oc-glo-chl-multi_cci-l4-chl_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-bbp443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-cdm443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-kd490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs412_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs555_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs670_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-spm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-zsd_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_MED_CHL_L4_REP_OBSERVATIONS_009_078/dataset-oc-med-chl-multi_cci-l4-chl_1km_monthly-rep-v02/"]

        if lon1 > lon2:
            Crossing = "YES"

            #First request
            w2 = -180
            e2 = lon2
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2
        
        elif lon2 > 180:
            Crossing = "YES"

            factor = lon2 - 180
            lonf = float(factor) - 180 
            
            #First request
            w2 = -180
            e2 = lonf
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2

        else:
            Crossing = "NO"


        ##########################################################################################################################################
        ##########################################################################################################################################
        # MY DAILY 
        #######################

        #BBOX  
        if typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        elif Crossing == "YES":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print(" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit()



        #VAR 
        if typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                #ftp.cwd(pathfiles + str(a) + "/" + str(m))
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")

                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        data = outpath1 + "/" + str(m) + "/" + file_name
                        out1 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variableslist]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ") 

            os.chdir(outpath)                  

            ftp.quit()



        #BBOX + VAR 
        if typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                #ftp.cwd(pathfiles + str(a) + "/" + str(m))
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        elif Crossing == "YES":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print(" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit()



        #BBOX + VAR + DEPTH 
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "YES" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)

                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            
                            DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            
                            DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

            os.chdir(outpath)

            ftp.quit()




        ##########################################################################################################################################
        ##########################################################################################################################################
        # MY - MONTHLY 
        #######################


        #BBOX 
        elif typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")


                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
                        
                        elif Crossing == "YES":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit() 

        
        #VAR
        elif typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        data = outpath1 +  "/" + file_name
                        out1 = outpath1 +  "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variableslist]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ")

            os.chdir(outpath)                                    

            ftp.quit() 
        


        #BBOX + VAR
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DSVar = DS1[variableslist]
                            DSVar.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
                        
                        elif Crossing == "YES":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "Subset_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variableslist]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit() 


        #BBOX + VAR + DEPTH
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "YES":

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 +  "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 +  "/" + "Subset_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name

                            
                            DS = xr.open_dataset(data)
                        
                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variableslist]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

            os.chdir(outpath)                

            ftp.quit()
       
        else:
            print("PROCESS COMPLETED")


    

    ##########################
    # TAB 3 #
    ##########################
    Listvar = []
    
    def extract_var():
        Database = {}
        with open (filejasonselvar, "r") as config_filesv:
            Database = json.load(config_filesv)
            for key in Database.keys(): 
                if FTPlk.get() in key:
                    #print(pathfiles)
                    listdic = Database.get(FTPlk.get()) 
                    Listvar = listdic[11:]
                    for variable in Listvar:
                        lstbox.insert(END, variable)
                        
    def select():
        select.selected_var = [lstbox.get(i) for i in lstbox.curselection()]

    
    def FTPsubselvar():

        ##########################
        # CMEMS LOGIN CREDENTIAL #
        ##########################

        cmems_user = User.get()         
        cmems_pass = Pwd.get() 

        #########################
        # FTP SEARCH PARAMETERS #
        #########################

        pathfiles = FTPlk.get()

        #########################
        # SELECTION TIME WINDOW #
        #########################

        datastart = Ds.get()  
        dataend = De.get()     

        ############################
        # Bounding box information #
        ############################

        bbox = bb.get()  #(YES/NO)

        lon1 = float(lomin.get())     #(WEST)
        lon2 = float(lomax.get())     #(EAST)
        lat1 = float(lamin.get())     #(SOUTH)
        lat2 = float(lamax.get())     #(NORTH)

        #######################
        # SELECTION VARIABLES #
        #######################

        Vs = Vex.get()  #(YES/NO)

        variables = select.selected_var 

        #####################
        # DEPTH INFORMATION #
        #####################

        DL = Dex.get()           #(YES/NO)

        RangeD = Dtype.get()    #(SINGLE/RANGE)

        #For "SINGLE" DEPTH extraction
        depth = sdepth.get()          

        #For "RANGE" DEPTHs extraction
        d1 = Rdepthmin.get()            
        d2 = Rdepthmax.get()

        #################
        # OUTPUT FOLDER #
        #################
  
        outpath = str(os.getcwd())  

        #########################################################
        # Few important points  before the start of the options #
        #########################################################

        typo = StringVar()
        structure = StringVar()
        ID = StringVar()
        Toidentify = StringVar()
        Pname = StringVar()
        di = StringVar() 
        df = StringVar()
        ccbbW = StringVar()
        ccbbE = StringVar()
        ccbbS = StringVar()
        ccbbN = StringVar()

        Database = {}
        with open (filejasonselvar, "r") as config_filesv:
            Database = json.load(config_filesv)
            for key in Database.keys(): 
                if pathfiles in key:
                    #print(pathfiles)
                    
                    listdic = Database.get(pathfiles) 
                    #print(listdic)

                    typo = listdic[0] #(NRT/MY)
                    structure = listdic[1]  #M(monthly)/D(daily)  
                    ID = listdic[2]  #(BACK/FRONT)
                    Toidentify = listdic[3]   #part of the fine name used to select the files 
                    Pname = pathfiles.split("/")[2]
                    di = listdic[4] 
                    df = listdic[5]
                    ccbbW = listdic[6]
                    ccbbE = listdic[7]
                    ccbbS = listdic[8]
                    ccbbN = listdic[9]

        #########################

        ys, ms, ds = datastart.split('-')
        ye, me, de = dataend.split('-')

        sdata = ys + "-" + ms
        edata = ye + "-" + me

        days = pd.date_range(datastart, dataend, freq='D')
        months = pd.date_range(*(pd.to_datetime([sdata, edata]) + pd.offsets.MonthEnd()), freq='M')


        SPECdatasets = ["/Core/OCEANCOLOUR_ARC_CHL_L4_REP_OBSERVATIONS_009_088/dataset-oc-arc-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_ATL_CHL_L4_REP_OBSERVATIONS_009_091/dataset-oc-atl-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_BS_CHL_L4_REP_OBSERVATIONS_009_079/dataset-oc-bs-chl-multi_cci-l4-chl_1km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_100km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_25km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_082/dataset-oc-glo-chl-multi-l4-gsm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_CHL_L4_REP_OBSERVATIONS_009_093/dataset-oc-glo-chl-multi_cci-l4-chl_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-bbp443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-cdm443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-kd490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs412_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs443_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs490_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs555_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-rrs670_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-spm_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_GLO_OPTICS_L4_REP_OBSERVATIONS_009_081/dataset-oc-glo-opt-multi-l4-zsd_4km_monthly-rep-v02/",
                        "/Core/OCEANCOLOUR_MED_CHL_L4_REP_OBSERVATIONS_009_078/dataset-oc-med-chl-multi_cci-l4-chl_1km_monthly-rep-v02/"]

        if lon1 > lon2:
            Crossing = "YES"

            #First request
            w2 = -180
            e2 = lon2
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2
        
        elif lon2 > 180:
            Crossing = "YES"

            factor = lon2 - 180
            lonf = float(factor) - 180 
            
            #First request
            w2 = -180
            e2 = lonf
            s2 = lat1
            n2 = lat2

            #Second request
            w1 = lon1
            e1 = 180
            s1 = lat1
            n1 = lat2

        else:
            Crossing = "NO"

        
        ##########################################################################################################################################
        ##########################################################################################################################################
        # MY DAILY 
        #######################

        #BBOX  
        if typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            
                            DS = xr.open_dataset(data)

                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                        
                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        elif Crossing == "YES":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
                        else:
                            print(" Please to check the bounding box coordinates ")

            os.chdir(outpath)


            ftp.quit()



        #VAR 
        if typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                #ftp.cwd(pathfiles + str(a) + "/" + str(m))
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")

                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        data = outpath1 + "/" + str(m) + "/" + file_name
                        out1 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variables]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ")  

            os.chdir(outpath)

            ftp.quit()



        #BBOX + VAR 
        if typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)
                
                #ftp.cwd(pathfiles + str(a) + "/" + str(m))
                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variables]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        elif Crossing == "YES":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DS1Var = DS1[variables]
                            DS1Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print(" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit()



        #BBOX + VAR + DEPTH 
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "D" and DL == "YES" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for day in days :

                a = day.strftime('%Y')
                m = day.strftime('%m')
                g = day.strftime('%d')

                #########################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                    
                outpath1 = outpath0 + "/" + str(a)
            
                path2 = os.path.join(outpath1, str(m))

                if not os.path.exists(path2):
                    os.mkdir(path2)

                ###########################

                if ID == "BACK":
                    look = day.strftime(Toidentify+'%Y%m%d')
                else:
                    look = day.strftime('%Y%m%d'+ Toidentify)

                ftp.cwd(pathfiles + str(a) + "/" + str(m))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1 + "/" + str(m))
                    outputfile = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variables]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:

                            data = outpath1 + "/" + str(m) + "/" + file_name
                            out1 = outpath1 + "/" + str(m) + "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 + "/" + str(m) + "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 + "/" + str(m) + "/" + "Subset_" + file_name
                            
                            box1 = outpath1 + "/" + str(m) + "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" + str(m) + "/" + "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            
                            DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variables]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
            
            os.chdir(outpath)

            ftp.quit()




        ##########################################################################################################################################
        ##########################################################################################################################################
        # MY - MONTHLY 
        #######################


        #BBOX 
        elif typo == "MY" and bbox == "YES" and Vs == "NO" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################


                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")


                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
                        
                        elif Crossing == "YES":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            os.remove(data)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit() 

        
        #VAR
        elif typo == "MY" and bbox == "NO" and Vs == "YES" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################


                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        data = outpath1 +  "/" + file_name
                        out1 = outpath1 +  "/" + "Subset_" + file_name
                        
                        DS = xr.open_dataset(data)

                        DSVar = DS[variables]
                        DSVar.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                        DS.close()

                        os.remove(data)

                        print("File: " + "Subset_" + file_name + " --> Subset completed")
                        print(" ")

            os.chdir(outpath)                                    

            ftp.quit() 
        


        #BBOX + VAR
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "NO" :

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################

                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    
                    else:
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)
                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            DSVar = DS1[variables]
                            DSVar.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS1.close()

                            os.remove(data)
                            os.remove(out1)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")
                        
                        elif Crossing == "YES":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "Subset_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS2 = xr.open_dataset(out1)

                            DS2Var = DS2[variables]
                            DS2Var.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:
                            print (" Please to check the bounding box coordinates ")

            os.chdir(outpath)

            ftp.quit() 

        


        #BBOX + VAR + DEPTH
        elif typo == "MY" and bbox == "YES" and Vs == "YES" and structure == "M" and DL == "YES":

            print(" ")
            print("Connection to the FTP server...")
            
            ftp = FTP('my.cmems-du.eu', user=cmems_user, passwd=cmems_pass)

            print("Connection exstabilished and download files in progress..")
            print(" ")
            
            for mon in months :

                a = mon.strftime('%Y')
                m = mon.strftime('%m')
                lastd = mon.strftime('%d')

                #################################

                path0 = os.path.join(outpath, Pname)

                if not os.path.exists(path0):
                    os.mkdir(path0)

                outpath0 = outpath + "/" + Pname

                path = os.path.join(outpath0, str(a))

                if not os.path.exists(path):
                    os.mkdir(path)
                   
                outpath1 = outpath0 + "/" + str(a)

                ####################################


                if ID == "BACK":
                    look = mon.strftime(Toidentify+'%Y%m')

                elif pathfiles in SPECdatasets:
                    look = mon.strftime('%Y%m'+'01_m_'+'%Y%m%d' + Toidentify)

                else: #FRONT
                    look = mon.strftime('%Y%m'+ Toidentify)

                ftp.cwd(pathfiles + str(a))

                filenames = ftp.nlst()

                files = pd.Series(filenames)

                for file_name in files[files.str.contains(look)]:

                    os.chdir(outpath1)
                    outputfile = outpath1 + "/"  + "Subset_" + file_name

                    if os.path.isfile(outputfile):
                        print ("File: " + "Subset_" + file_name + " --> File already processed")
                    else:
                
                        ftp.retrbinary('RETR' + " " + file_name, open(file_name, 'wb').write)

                        print("File: " + file_name + " --> Download completed")

                        if Crossing == "NO":

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 +  "/" + "Subset_" + file_name
                            
                            DS = xr.open_dataset(data)
                        
                            #DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))

                            try:
                                DSbbox = DS.sel(longitude=slice(float(lon1),float(lon2)), latitude=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(x=slice(float(lon1),float(lon2)), y=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")
                            try:
                                DSbbox = DS.sel(lon=slice(float(lon1),float(lon2)), lat=slice(float(lat1),float(lat2)))
                            except ValueError:
                                print("")

                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variables]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

                        else:

                            data = outpath1 +  "/" + file_name
                            out1 = outpath1 +  "/" + "SubsetBbox_" + file_name
                            out2 = outpath1 +  "/" + "SubsetDepth_" + file_name
                            out3 = outpath1 +  "/" + "Subset_" + file_name
                            
                            box1 = outpath1 +  "/" + "Box1_" + file_name
                            box2 = outpath1 + "/" +  "Box2_" + file_name
                            
                            DS = xr.open_dataset(data)

                            try:
                                DSbbox1 = DS.sel(longitude=slice(float(w1),float(e1)), latitude=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"  
                                
                            try:
                                DSbbox1 = DS.sel(x=slice(float(w1),float(e1)), y=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox1 = DS.sel(lon=slice(float(w1),float(e1)), lat=slice(float(s1),float(n1)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox1.to_netcdf(path=box1, mode='w', format= 'NETCDF4', engine='h5netcdf')


                            try:
                                DSbbox2 = DS.sel(longitude=slice(float(w2),float(e2)), latitude=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "longitude"   
                                
                            try:
                                DSbbox2 = DS.sel(x=slice(float(w2),float(e2)), y=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "x"  
                                
                            try:
                                DSbbox2 = DS.sel(lon=slice(float(w2),float(e2)), lat=slice(float(s2),float(n2)))
                            except ValueError:
                                print("")
                            else:
                                concat = "lon"

                            DSbbox2.to_netcdf(path=box2, mode='w', format= 'NETCDF4', engine='h5netcdf')

                            DSbbox = xr.concat([DSbbox1,DSbbox2], dim=concat)
                            DSbbox.to_netcdf(path=out1, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS.close()

                            DS1 = xr.open_dataset(out1)

                            if RangeD == "SINGLE" :
                                DSdepth = DS1.sel(depth=int(depth), method="nearest")
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()
                            else:
                                DSdepth = DS1.sel(depth=slice(float(d1),float(d2)))
                                DSdepth.to_netcdf(path=out2, mode='w', format= 'NETCDF4', engine='h5netcdf')
                                DS1.close()

                            DS2 = xr.open_dataset(out2)

                            DS2Var = DS2[variables]
                            DS2Var.to_netcdf(path=out3, mode='w', format= 'NETCDF4', engine='h5netcdf')
                            DS2.close()

                            os.remove(data)
                            os.remove(out1)
                            os.remove(out2)
                            os.remove(box1)
                            os.remove(box2)

                            print("File: " + "Subset_" + file_name + " --> Subset completed")
                            print(" ")

            os.chdir(outpath)

            ftp.quit()

       
       
        else:
            print("PROCESS COMPLETED")




    #END FUNCTIONS
    ##########################
    Username = Label(tab2, text="Username")
    Username.grid(column=0, row=0)
    User = Entry(tab2, width=13)
    User.grid(column=0, row=1)
    ##
    Password = Label(tab2, text="Password")
    Password.grid(column=1, row=0)
    Pwd = Entry(tab2, width=13, show="*")
    Pwd.grid(column=1, row=1)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=2)
    space = Label(tab2, text="")
    space.grid(column=1, row=2)
    ##
    FTPlink = Label(tab2, text="FTP-URL")
    FTPlink.grid(column=0, row=3)
    FTPlk = Entry(tab2, width=13)
    FTPlk.grid(column=1, row=3)
    ##
    space = Label(tab2, text="")
    space.grid(column=1, row=4)
    ##
    Datest = Label(tab2, text="From(YYYY-MM-DD)")
    Datest.grid(column=0, row=6)
    Ds = Entry(tab2, width=13)
    Ds.grid(column=1, row=6)
    ##
    Daten = Label(tab2, text="To(YYYY-MM-DD)")
    Daten.grid(column=0, row=7)
    De = Entry(tab2, width=13)
    De.grid(column=1, row=7)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=8)
    space = Label(tab2, text="")
    space.grid(column=1, row=8)
    ##
    boundingb = Label(tab2, text="Bounding-box?(YES/NO)")
    boundingb.grid(column=0, row=9)
    bb = Entry(tab2, width=13)
    bb.grid(column=1, row=9)
    ##
    longmin = Label(tab2, text="Long-min(W)")
    longmin.grid(column=0, row=10)
    lomin = Entry(tab2, width=8)
    lomin.grid(column=0, row=11)
    ##
    longmax = Label(tab2, text="Long-max(E)")
    longmax.grid(column=1, row=10)
    lomax = Entry(tab2, width=8)
    lomax.grid(column=1, row=11)
    ##
    latmin = Label(tab2, text="Lat-min(S)")
    latmin.grid(column=0, row=12)
    lamin = Entry(tab2, width=8)
    lamin.grid(column=0, row=13)
    ##
    latmax = Label(tab2, text="Lat-max(N)")
    latmax.grid(column=1, row=12)
    lamax = Entry(tab2, width=8)
    lamax.grid(column=1, row=13)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=14)
    space = Label(tab2, text="")
    space.grid(column=1, row=14)
    ##
    Varex = Label(tab2, text="Variables?(YES/NO)")
    Varex.grid(column=0, row=15)
    Vex = Entry(tab2, width=13)
    Vex.grid(column=1, row=15)
    VexY = Label(tab2, text="Variables(var1,var2,...)")
    VexY.grid(column=0, row=16)
    Vexlist = Entry(tab2, width=13)
    Vexlist.grid(column=1, row=16)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=17)
    space = Label(tab2, text="")
    space.grid(column=1, row=17)
    ##
    Depex = Label(tab2, text="Depths?(YES/NO | SINGLE/RANGE)")
    Depex.grid(column=0, row=18)
    Dex = Entry(tab2, width=13)
    Dex.grid(column=1, row=18)
    Dtype = Entry(tab2, width=13)
    Dtype.grid(column=2, row=18)
    ##
    Singledepth = Label(tab2, text="Single-depth")
    Singledepth.grid(column=0, row=19)
    sdepth = Entry(tab2, width=13)
    sdepth.grid(column=1, row=19)
    ##
    Rangedepth = Label(tab2, text="Range-depths(Min|Max)")
    Rangedepth.grid(column=0, row=20)
    Rdepthmin = Entry(tab2, width=13)
    Rdepthmin.grid(column=1, row=20)
    Rdepthmax = Entry(tab2, width=13)
    Rdepthmax.grid(column=2, row=20)
    ##
    space = Label(tab2, text="")
    space.grid(column=0, row=22)
    space = Label(tab2, text="")
    space.grid(column=1, row=22)
    ##
    btn1 = Button(tab2, text="Download", bg="red", command=FTPsub)
    btn1.grid(column=0, row=23)

    ##########################
    #TAB 3
    ##########################
    
    Username = Label(tab3, text="Username")
    Username.grid(column=0, row=0)
    User = Entry(tab3, width=13)
    User.grid(column=0, row=1)
    ##
    Password = Label(tab3, text="Password")
    Password.grid(column=1, row=0)
    Pwd = Entry(tab3, width=13, show="*")
    Pwd.grid(column=1, row=1)
    ##
    space = Label(tab3, text="")
    space.grid(column=0, row=2)
    space = Label(tab3, text="")
    space.grid(column=1, row=2)
    ##
    FTPlink = Label(tab3, text="FTP-URL")
    FTPlink.grid(column=0, row=3)
    FTPlk = Entry(tab3, width=13)
    FTPlk.grid(column=1, row=3)
    ##
    space = Label(tab3, text="")
    space.grid(column=1, row=4)
    ##
    Datest = Label(tab3, text="From(YYYY-MM-DD)")
    Datest.grid(column=0, row=6)
    Ds = Entry(tab3, width=13)
    Ds.grid(column=1, row=6)
    ##
    Daten = Label(tab3, text="To(YYYY-MM-DD)")
    Daten.grid(column=0, row=7)
    De = Entry(tab3, width=13)
    De.grid(column=1, row=7)
    ##
    space = Label(tab3, text="")
    space.grid(column=0, row=8)
    space = Label(tab3, text="")
    space.grid(column=1, row=8)
    ##
    boundingb = Label(tab3, text="Bounding-box?(YES/NO)")
    boundingb.grid(column=0, row=9)
    bb = Entry(tab3, width=13)
    bb.grid(column=1, row=9)
    ##
    longmin = Label(tab3, text="Long-min(W)")
    longmin.grid(column=0, row=10)
    lomin = Entry(tab3, width=8)
    lomin.grid(column=0, row=11)
    ##
    longmax = Label(tab3, text="Long-max(E)")
    longmax.grid(column=1, row=10)
    lomax = Entry(tab3, width=8)
    lomax.grid(column=1, row=11)
    ##
    latmin = Label(tab3, text="Lat-min(S)")
    latmin.grid(column=0, row=12)
    lamin = Entry(tab3, width=8)
    lamin.grid(column=0, row=13)
    ##
    latmax = Label(tab3, text="Lat-max(N)")
    latmax.grid(column=1, row=12)
    lamax = Entry(tab3, width=8)
    lamax.grid(column=1, row=13)
    ##
    space = Label(tab3, text="")
    space.grid(column=0, row=14)
    space = Label(tab3, text="")
    space.grid(column=1, row=14)
    ##
    Varex = Label(tab3, text="Variables?(YES/NO)")
    Varex.grid(column=0, row=15)
    Vex = Entry(tab3, width=13)
    Vex.grid(column=1, row=15)

    exvar = Button(tab3,text="Get-Variables", bg="yellow", command=extract_var)
    exvar.grid(column=0, row=16)
    
    yscroll = Scrollbar(tab3, orient="vertical", )
    lstbox = Listbox(tab3, listvariable=Listvar, selectmode=MULTIPLE, yscrollcommand=yscroll.set, height=5)
    #yscroll.config(command=lstbox.yview)

    # if OS=="Linux":
    #     yscroll.place(x=25, y=285)
    # elif OS=="Darwin":
    #     yscroll.place(x=8, y=417)
    # else:
    #     yscroll.place(x=15, y=350)

    lstbox.grid(column=0, row=17)
    
    confirmvar = Button(tab3,text="Set-Variables", bg="green", command=select)
    confirmvar.grid(column=1, row=17)

    space = Label(tab3, text="")
    space.grid(column=0, row=18)
    space = Label(tab3, text="")
    space.grid(column=1, row=18)
    
    ##
    Depex = Label(tab3, text="Depths?(YES/NO | SINGLE/RANGE)")
    Depex.grid(column=0, row=19)
    Dex = Entry(tab3, width=13)
    Dex.grid(column=1, row=19)
    Dtype = Entry(tab3, width=13)
    Dtype.grid(column=2, row=19)
    ##
    Singledepth = Label(tab3, text="Single-depth")
    Singledepth.grid(column=0, row=20)
    sdepth = Entry(tab3, width=13)
    sdepth.grid(column=1, row=20)
    ##
    Rangedepth = Label(tab3, text="Range-depths(Min|Max)")
    Rangedepth.grid(column=0, row=21)
    Rdepthmin = Entry(tab3, width=13)
    Rdepthmin.grid(column=1, row=21)
    Rdepthmax = Entry(tab3, width=13)
    Rdepthmax.grid(column=2, row=21)
    ##
    space = Label(tab3, text="")
    space.grid(column=0, row=22)
    space = Label(tab3, text="")
    space.grid(column=1, row=22)
    ##

    btn1 = Button(tab3, text="Download", bg="red", command=FTPsubselvar)
    btn1.grid(column=0, row=23)

    space = Label(tab3, text="")
    space.grid(column=0, row=24)
    space = Label(tab3, text="")
    space.grid(column=1, row=24)
    ###############################################################

    print (Listvar)

    tab_control.pack(expand=1, fill='both')

    window.mainloop()

