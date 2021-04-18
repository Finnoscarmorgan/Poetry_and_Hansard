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
tree = ET.parse('/Users/fiannualamorgan/Documents/GitHub/Poetry_and_Hansard/hansard-xml/senate/1903/19030723_senate_1_14.xml')
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
                    print(len(list(i)))
                    if len(list(i))>0:
                        vals[ind]=i.text.replace('=','')
                        for k in i:
                            if k.text != None:
                                vals[ind]=vals[ind]+" "+k.text
                            if k.tail != None:
                                vals[ind]=vals[ind]+" "+k.tail
                    else:     
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
df.to_csv("/Users/fiannualamorgan/Documents/GitHub/Poetry_and_Hansard/Test_File_18_04_2021.csv") 

results=[]
ind=0
match=False
checkRange=[1,2,3,4,5]
numBefore=0
numAfter=0
for row in rows:
    if any([row[17].lower().find("poem")!=-1,row[17].lower().find("poet")!=-1]):
        match=True
        speaker=row[8]
         
        for indices in checkRange:
            if rows[ind-indices][8].lower().find(speaker.lower()):
                continue
            else:
                numBefore=indices-1
        for indices in checkRange:
            if rows[ind+indices][8].lower().find(speaker.lower()):
                continue
            else:
                numAfter=indices-1

    results.append(row[17].lower().find("poem")!=-1)
    ind=ind+1        



    



[i for i, x in enumerate(results) if x]