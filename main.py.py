import tkinter
import ssl
from urllib.request import urlopen, urlretrieve
from urllib.parse import urlencode, quote_plus
import json


def hawkid():
    return("npipatkittikul")

#
# In HW10 and 11, you will use two Google services, Google Static Maps API
# and Google Geocoding API.  Both require use of an API key.
# 
# When you have the API key, put it between the quotes in the string below
GOOGLEAPIKEY = "AIzaSyCeGycpewBbKTjJSIzoyYE3YPjGfIR7Q_0"

# To run the HW10 program, call the last function in this file: HW10().

# The Globals class demonstrates a better style of managing "global variables"
# than simply scattering the globals around the code and using "global x" within
# functions to identify a variable as global.
#
# We make all of the variables that we wish to access from various places in the
# program properties of this Globals class.  They get initial values here
# and then can be referenced and set anywhere in the program via code like
# e.g. Globals.zoomLevel = Globals.zoomLevel + 1
#
class Globals:
   
   rootWindow = None
   mapLabel = None

   
   defaultLocation = "Mt. Fuji, Japan"
   mapLocation = defaultLocation
   mapFileName = 'googlemap.gif'
   mapSize = 400
   zoomLevel = 9
   mapType = 'roadmap'
   
# Given a string representing a location, return 2-element tuple
# (latitude, longitude) for that location 
#
# See https://developers.google.com/maps/documentation/geocoding/
# for details about Google's geocoding API.
#
#
def geocodeAddress(addressString):
   urlbase = "https://maps.googleapis.com/maps/api/geocode/json?address="
   geoURL = urlbase + quote_plus(addressString)
   geoURL = geoURL + "&key=" + GOOGLEAPIKEY

   # required (non-secure) security stuff for use of urlopen
   ctx = ssl.create_default_context()
   ctx.check_hostname = False
   ctx.verify_mode = ssl.CERT_NONE
   
   stringResultFromGoogle = urlopen(geoURL, context=ctx).read().decode('utf8')
   jsonResult = json.loads(stringResultFromGoogle)
   if (jsonResult['status'] != "OK"):
      print("Status returned from Google geocoder *not* OK: {}".format(jsonResult['status']))
      result = (0.0, 0.0) # this prevents crash in retrieveMapFromGoogle - yields maps with lat/lon center at 0.0, 0.0
   else:
      loc = jsonResult['results'][0]['geometry']['location']
      result = (float(loc['lat']),float(loc['lng']))
   return result

# Contruct a Google Static Maps API URL that specifies a map that is:
# - is centered at provided latitude lat and longitude long
# - is "zoomed" to the Google Maps zoom level in Globals.zoomLevel
# - Globals.mapSize-by-Globals.mapsize in size (in pixels), 
# - will be provided as a gif image
#
# See https://developers.google.com/maps/documentation/static-maps/
#
# YOU WILL NEED TO MODIFY THIS TO BE ABLE TO
# 1) DISPLAY A PIN ON THE MAP
# 2) SPECIFY MAP TYPE - terrain vs road vs ...
#
def getMapUrl():
   lat, lng = geocodeAddress(Globals.mapLocation)
   urlbase = "http://maps.google.com/maps/api/staticmap?"
   args = "center={},{}&zoom={}&size={}x{}&maptype={}&markers=color:blue|{},{}&sensor=false&format=gif".format(lat,lng,Globals.zoomLevel,Globals.mapSize,Globals.mapSize,Globals.mapType,lat,lng)
   args = args + "&key=" + GOOGLEAPIKEY
   mapURL = urlbase + args
   return mapURL

# Retrieve a map image via Google Static Maps API, storing the 
# returned image in file name specified by Globals' mapFileName
#
def retrieveMapFromGoogle():
   url = getMapUrl()
   urlretrieve(url, Globals.mapFileName)

########## 
#  basic GUI code

def displayMap():
   retrieveMapFromGoogle()    
   mapImage = tkinter.PhotoImage(file=Globals.mapFileName)
   Globals.mapLabel.configure(image=mapImage)
   # next line necessary to "prevent (image) from being garbage collected" - http://effbot.org/tkinterbook/label.htm
   Globals.mapLabel.mapImage = mapImage
   
def readEntryAndDisplayMap():
   #### you should change this function to read from the location from an Entry widget
   #### instead of using the default location

   TextInEntry = LocationEntry.get()

   
   Globals.mapLocation = TextInEntry
   displayMap()
   
def UpdateZoom(changeAmount):
    Globals.zoomLevel = Globals.zoomLevel + changeAmount
    return Globals.zoomLevel
   
def UpdateMap(number):
    Globals.mapSize = Globals.mapSize + number
    return Globals.mapSize
    
def updateCountLabel():
    ZoomLabel.configure(text="Zoom : {}".format(UpdateZoom(0)))

def Zoomin():
    UpdateZoom(1)
    displayMap()
    updateCountLabel()

def Zoomout():
    UpdateZoom(-1)
    displayMap()
    updateCountLabel()


def Roadmap():
    global varr

    if varr.get() == 1:
       Globals.mapType = 'roadmap'
       displayMap()

def hybridmap():
    global varr

    if varr.get() == 2:
       Globals.mapType = 'hybrid'
       displayMap()

def Satellitemap():
    global varr

    if varr.get() == 3:
       Globals.mapType = 'satellite'
       displayMap()

def Terrainmap():
    global varr

    if varr.get() == 4:
       Globals.mapType = 'terrain'
       displayMap()
   

       





   


def initializeGUIetc():

   global LocationEntry
   global ZoomLabel
   global varr
   

   Globals.rootWindow = tkinter.Tk()
   Globals.rootWindow.title("HW10")
   
   FirstFrame = tkinter.Frame(Globals.rootWindow) 
   FirstFrame.pack()

   directionLabel = tkinter.Label(FirstFrame, text = "Enter the location:")
   directionLabel.pack(side=tkinter.LEFT)

   LocationEntry = tkinter.Entry(FirstFrame, width = 30)
   LocationEntry.pack()

   

   mainFrame = tkinter.Frame(Globals.rootWindow) 
   mainFrame.pack()

   # until you add code, pressing this button won't change the map (except
   # once, to the Beijing location "hardcoded" into readEntryAndDisplayMap)
   # you need to add an Entry widget that allows you to type in an address
   # The click function should extract the location string from the Entry widget
   # and create the appropriate map.
   readEntryAndDisplayMapButton = tkinter.Button(mainFrame, text="Show me the map!", command=readEntryAndDisplayMap)
   readEntryAndDisplayMapButton.pack()

   # we use a tkinter Label to display the map image
   Globals.mapLabel = tkinter.Label(mainFrame, width=Globals.mapSize, bd=2, relief=tkinter.FLAT)
   Globals.mapLabel.pack()

   SecondFrame = tkinter.Frame(Globals.rootWindow)
   SecondFrame.pack()

   varr = tkinter.IntVar()
   varr.set(1)

   ZoomLabel = tkinter.Label(SecondFrame, text = "Zoom : 9")
   ZoomLabel.pack(side = tkinter.LEFT)

   RoadMapRadioButton = tkinter.Radiobutton(SecondFrame,text = "Road Map",variable=varr, value=1,command=Roadmap)
   RoadMapRadioButton.pack(side = tkinter.RIGHT)

   HyBridMapRadioButton = tkinter.Radiobutton(SecondFrame,text = "HyBrid Map",variable=varr, value=2,command=hybridmap)
   HyBridMapRadioButton.pack(side = tkinter.RIGHT)

   SatelliteMapRadioButton = tkinter.Radiobutton(SecondFrame,text = "Satellite Map",variable=varr, value=3,command=Satellitemap)
   SatelliteMapRadioButton.pack(side = tkinter.RIGHT)

   TerrainMapRadioButton = tkinter.Radiobutton(SecondFrame,text = "Terrain Map",variable=varr, value=4,command=Terrainmap)
   TerrainMapRadioButton.pack(side = tkinter.RIGHT)

   BottonPlus = tkinter.Button(SecondFrame, text ="+",command=Zoomin)
   BottonPlus.pack()

   BottonPlus = tkinter.Button(SecondFrame, text ="-",command=Zoomout)
   BottonPlus.pack()

   


   




   
   

def HW10():
    initializeGUIetc()
    displayMap()
    Globals.rootWindow.mainloop()
