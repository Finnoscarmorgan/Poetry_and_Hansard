import xml.etree.ElementTree as ET
import xmltodict
import pandas as pd
import pprint
import os
                     
# Setting up the table.
#I've added pretty much all the data types that are there, if you see any more you 
#can just add it to the list and it will automatically pull it out. Just make sure
#that para remains the last item in the list
cols = ["date","parliament.no","session.no","period.no","chamber","page.no","proof","day.start","name","name.id","title","type","electorate","party","role","in.gov","first.speech","para"] 
stop="para"
output=[]

#load subdirectories with Hansard
path = '/Users/fiannualamorgan/Documents/GitHub/Poetry_and_Hansard/hansard-xml/senate'
directory_contents = os.listdir(path)

# get directory contents for folders
for f in directory_contents:
    if f==".DS_Store":
        continue
    subpath = path + '/' + f + '/'
    sub_directory_contents = os.listdir(subpath)
    for f1 in sub_directory_contents:
        if f1==".DS_Store":
            continue
        final_path = subpath + '/' + f1

        # Parsing the XML file, add here the file to be parsed. For this to all work properly
        #without having to manually run this code for every file, you will need to get 
        # access to all the filenames in your hansard xml directory.
        #All of this code will then need to be put in a big for loop that iterates through
        #each file, holds its file name in a variable, parses the file and then uses the
        #filename to save it as a unique csv
        tree = ET.parse(final_path)
        root = tree.getroot()

        vals=[]
        ind=0
        for i in cols:
            vals.append('')
            ind=ind+1
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
                            #if i.attrib['role']=='metadata':
                                vals[ind]=i.text
                        elif i.tag==stop:
                            if len(list(i))>0:
                                if i.text==None:
                                    vals[ind]=''
                                else:
                                    vals[ind]=i.text
                                for k in i:
                                    if k.text != None:
                                        vals[ind]=vals[ind]+" "+k.text
                                        stopMatchFound=True
                                    if k.tail != None:
                                        vals[ind]=vals[ind]+" "+k.tail
                                        stopMatchFound=True
                                    if stopMatchFound:
                                        rows.append(list(vals))
                                        break                  
                            elif i.text==None:
                                continue
                            else:     
                                vals[ind]=i.text
                                stopMatchFound=True
                                rows.append(list(vals))
                                break
                        else:
                            vals[ind]=i.text
                    ind=ind+1
                if not valMatchFound:
                    xmlDig(i,rows,cols,vals,stop)
            return rows

        df=pd.DataFrame(rows,columns=cols)
        #Call the digging function
        rows=xmlDig(root,rows,cols,vals,stop) 

        ind=0
        match=False
        checkRange=[1,2,3,4,5]
        numBefore=0
        numAfter=0
        for row in rows:
            if any([row[17].lower().find("poem")!=-1,row[17].lower().find("poet")!=-1]):
                speakerInfo=row
                match=True
                speaker=row[8]
                colInd=0
                for col in cols:
                    if speakerInfo==None:
                        for row1 in rows:
                            if row1[8]==speaker and row1[colInd]!=None:
                                speakerInfo[colInd]=row1[colInd]
                                break
                    colInd=colInd+1

                for indices in checkRange:
                    if rows[ind-indices][8].lower().find(speaker.lower())!=-1:
                        if ind-indices==0:
                            numBefore=indices
                            break
                        else:
                            continue
                    else:
                        numBefore=indices-1
                        break
                for indices in checkRange:
                    if rows[ind+indices][8].lower().find(speaker.lower())!=-1:
                        if ind+indices==len(rows)-1:
                            numAfter=indices
                            break
                        else:
                            continue
                    else:
                        numAfter=indices-1
                        break
                concatRange=list(range(ind-numBefore,ind+numAfter+1))
                speech=''
                for i in concatRange:
                    speech= speech+"\n \n"+rows[i][17]
                speakerInfo[17]=speech

                output.append(speakerInfo)
            ind=ind+1        


output=pd.DataFrame(output,columns=cols)

# Writing dataframe to csv
output.to_csv("/Users/fiannualamorgan/Documents/GitHub/Poetry_and_Hansard/Senate_Poetry_list.csv") 
print("DONE!")