import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import pprint

# Parsing the XML file, add here the file to be parsed. For this to all work properly
#without having to manually run this code for every file, you will need to get 
# access to all the filenames in your hansard xml directory.
#All of this code will then need to be put in a big for loop that iterates through
#each file, holds its file name in a variable, parses the file and then uses the
#filename to save it as a unique csv
tree = ET.parse('hansard test.xml')
root = tree.getroot()

# Setting up the table.
#I've added pretty much all the data types that are there, if you see any more you 
#can just add it to the list and it will automatically pull it out. Just make sure
#that para remains the last item in the list
cols = ["date","parliament.no","session.no","period.no","chamber","page.no","proof","day.start","name","name.id","title","type","electorate","party","role","in.gov","first.speech","para"] 
vals=[]
ind=0
for i in cols:
    vals.append('')
    ind=ind+1
stop="para"
rows = [] 

#This is a recursive function that looks for items in the cols list as children
#of each element. If it finds an item, it gives the value of that item to the list
#and keeps searching. If it comes across an element that doesn't match an item on 
#the list (which is therefore not an element containing data) it calls itself on
#that element and keeps searching. Any time it hits a para it adds an entry to the
#rows variable (which will be the core of the csv) and populates it with the values
#found for all existing items on the list, including the para text.
def xmlDig(thisElement,rows,cols,vals,stop): 
    stopMatchFound=False

    for i in thisElement:
        valMatchFound=False
        ind=0
        for j in cols: 
            if i.tag==j:
                valMatchFound=True
                if i.tag=='name':
                    if i.attrib['role']=='metadata':
                        vals[ind]=i.text
                elif i.tag==stop:
                    vals[ind]=i.text.replace('=','')
                    stopMatchFound=True
                    rows.append(list(vals))
                    break
                else:
                    vals[ind]=i.text
            ind=ind+1
        if not valMatchFound:
            xmlDig(i,rows,cols,vals,stop)
    return rows


#Call the digging function
rows=xmlDig(root,rows,cols,vals,stop) 

#Convert to dataframe
df = pd.DataFrame(rows, columns=cols) 

# Writing dataframe to csv. WIll need to make the file name a variable
# that is determined by the file name of the xml 
df.to_csv("output.csv") 
