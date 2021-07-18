from openresume.settings import BASE_DIR,MEDIA_ROOT,STATIC_DIR
from pathlib import Path
from .percent_rem import percentReplacerString
from .percent_rem import percentReplacerDict
import os

LATEX_ROOT = os.path.join(STATIC_DIR,'latex')

def createTextFile(latex_file_name,name,rollno,stream,branch,minor,college,email,iitgmail,mobileno,linkedin,education,internships,projects,techskills,keyCourses,por,achievements):
    
    PDFGEN_DIR = os.path.join(BASE_DIR,'app')

    base_file_path = os.path.join(PDFGEN_DIR,"base.txt")
    latexFile_path = os.path.join(LATEX_ROOT,latex_file_name)

    print(str(latexFile_path))
    readfile = open(str(base_file_path),"rt")
    writefile=open(str(latexFile_path),"w")

    lines=readfile.readlines()

    #write some static code
    for i in range(0,87):
        writefile.write(lines[i])

    #Heading Dynamic Code
    #if Minor is there 
    writefile.write(r"\textbf{\huge "+name+r"}\\")
    writefile.write("\n")

    calculation_list = {"left":[ 
                                len('Roll No. 190101037'),
                                len(stream + ' - '+branch),
                                len(college),
                                len(minor),
                            ],
                            "right":[
                                len(email),
                                len(mobileno),
                                len(iitgmail),
                                len(linkedin),
                            ]
                        }
    hskip_value = hskip_measure(calculation_list)

    writefile.write(r"\begin{tabular*}{\textwidth}{l@{\hskip" + str(hskip_value) +r"cm}r}")

    for i in range(88,91):
        writefile.write(lines[i])
    
    

    if (minor!=""):
        writefile.write(r"{Roll No. "+rollno+r"}&\href{mailto:"+email+r"}{ "+email+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+stream +" - "+ branch + r"}& Mobile : "+mobileno+r"\\")
        writefile.write("\n")
        writefile.write(r"{Minor in "+minor+r"}&\href{mailto:"+iitgmail+r"}{ "+iitgmail+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+ college +r"} & \href{"+linkedin+r"/}{"+linkedin+r"}\\")
        writefile.write("\n")
    #else
    else:
        writefile.write(r"{Roll No. "+rollno+r"}&\href{mailto:"+email+r"}{ "+email+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+stream +" - "+ branch + r"}& Mobile : "+mobileno+r"\\")
        writefile.write("\n")
        writefile.write(r"{"+ college +r"}&\href{mailto:"+iitgmail+r"}{ "+iitgmail+r"}\\")
        writefile.write("\n")
        writefile.write(r"{"+"} & \href{"+linkedin+r"/}{"+linkedin+r"}")
        writefile.write("\n")

    #write some static code
    for i in range(96,112):
        writefile.write(lines[i])

    #Education Dynamic code
    #education=[["d1","c1","p1","y1"],["d2","c2","p2","y2"],["d3","c3","p3","y3"]]
    for sublist in education:
        if(sublist[0]!=""):
            for i in range(len(sublist)):
                # sublist[i]=percentReplacerString(sublist[i])
                sublist[i]=sublist[i].replace('%',r'\%')
                sublist[i]=sublist[i].replace('_',r'\_')

            writefile.write(r"\hline "+sublist[0] +r"& "+sublist[1]+ r"& "+sublist[2] +r"& "+sublist[3] +r"\\")
            writefile.write("\n")
   
    for i in range(115,120):
        writefile.write(lines[i])

    internFlag = False
    for inlist in internships:
        if(inlist[0]!=""):
            internFlag = True
            break


    # internships start here
    # [[exp1,[expDes1,2 , ..]],]
    if(internFlag):
        #indent
        writefile.write(r'\vspace{4pt}')
        writefile.write("\n")
        writefile.write("\n")
        writefile.write(r"\section{Internships and Experience}")
        writefile.write("\n")
        writefile.write(r"\resumeSubHeadingListStart")
        writefile.write("\n")
        for sublist in internships:
            sublist[0] = percentReplacerString(sublist[0])
            for i in range(len(sublist[1])):
                sublist[1][i] = percentReplacerString(sublist[1][i])
            if (sublist[0] != ""):
                writefile.write(r"\resumeSubItem{" + sublist[0] + r"}")
                writefile.write("\n")
                writefile.write(r"{\vspace{-7pt} \begin{itemize}")
                writefile.write("\n")
                for sub_desc in sublist[1]:
                    if(sub_desc.isspace() or sub_desc==""):
                        continue
                    writefile.write(r"\item "+sub_desc)
                    writefile.write("\n")
                writefile.write(r"\end{itemize} }")
                writefile.write("\n")
                writefile.write("\n")
        writefile.write(r"\resumeSubHeadingListEnd")



    #write some static code
    for i in range(119,125):
        writefile.write(lines[i])

    proFlag = False
    for sl in projects:
        if(sl[0]!=""):
            proFlag = True
            break
    if(proFlag):
        writefile.write(lines[125])
        writefile.write(lines[126])
        writefile.write(lines[127])
    #Projects Dynamic code
    #projects=[["title1","club1",["desc1","desc2" .. ]"link1","date1"],["title2","club2","desc2","link2","date2"],["title3","club3","desc3","link3","date3"],["title4","club4","desc4","link4","date4"]]
    for sublist in projects:
        sublist_3_str = percentReplacerString(sublist[3])
        for i in range(len(sublist)):
            if(i!=3 and i!=2):
                sublist[i]=percentReplacerString(sublist[i])
        for i in range(len(sublist[2])):
            sublist[2][i] = percentReplacerString(sublist[2][i])
            
        if(sublist[0]!="" and sublist[1]!="" and sublist[2]!="" and sublist[3]!="" and sublist[4]!=""):
            writefile.write(r"\resumeSubheading{"+sublist[0]+r"}{"+sublist[4]+r"}{"+sublist[1]+r"}{\href{"+sublist[3]+r"}{\textit{\small "+sublist_3_str+r"   }}}")
            writefile.write("\n")
            writefile.write(r"\begin{itemize}")
            writefile.write("\n")
            for i in range(len(sublist[2])):
                writefile.write(r"\item "+sublist[2][i])
            # writefile.write(r"\item "+sublist[2])
            # writefile.write("\n")
            writefile.write(r" \end{itemize}")
            writefile.write("\n")
            writefile.write(r"\vspace{2pt}")
            writefile.write("\n")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[151])
    if(proFlag):
        writefile.write(lines[152])

    for i in range(153,160):
        writefile.write(lines[i])

    tsFlag = False
    for i in techskills.keys():
        if(techskills[i]!=""):
            tsFlag = True
            break

    if(tsFlag):
        writefile.write(lines[160])
        writefile.write(lines[161])
        writefile.write(lines[162])
        writefile.write(lines[163])
        #Technical Skills Dynamic code
        #techskills=["pllang","webtech","dbms","os","miscell","otherskills"]
        for key in techskills.keys():
            if(techskills[key]!=""):
                writefile.write(r"\resumeSubItem{"+ key +r"}{" +techskills[key] + r"}")
                writefile.write("\n")
        

        #write some static code
        for i in range(170,174):
            writefile.write(lines[i])
    

    for i in range(174,186):
        writefile.write(lines[i])

    cFlag = False
    for course in keyCourses:
        if(course!=""):
            cFlag = True
            break
    
    if(cFlag==False):
        writefile.write(r"\item null")
    #Key courses Dynamic code
    # keyCourses=["ma101","webd101","cpp110"]
    for course in keyCourses:
        course=percentReplacerString(course)
        if(course!=""):
            writefile.write(r"\item "+course)
            writefile.write("\n")
    
    #write some static code
    for i in range(194,205):
        writefile.write(lines[i])


    porFlag = False
    for pors in por:
        if(pors[0]!=""):
            porFlag = True
            break

    if(porFlag):
        writefile.write(lines[205])
        writefile.write(lines[206])
        writefile.write(lines[207])
    #POR Dynamic code
    #por=[["title1",["desc1", "desc2" ... ]],["title2","desc2"],["title3","desc3"],["title4","desc4"]]
    for sublist in por:
        sublist[0] = percentReplacerString(sublist[0])
        for i in range(len(sublist[1])):
            sublist[1][i]=percentReplacerString(sublist[1][i])
        if(sublist[0]!=""):
            writefile.write(r"\resumeSubItem{"+sublist[0]+r"}")
            writefile.write("\n")
            writefile.write(r"{\vspace{-7pt}")
            writefile.write("\n")
            writefile.write(r"\begin{itemize}")
            writefile.write("\n")
            for sub_desc in sublist[1]:
                if(sub_desc.isspace() or sub_desc==""):
                    continue
                writefile.write(r"\item "+sub_desc)
                writefile.write("\n")
            writefile.write(r"\end{itemize} }")
            writefile.write("\n")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[231])
    if(porFlag):   
        writefile.write(lines[232])
        writefile.write(lines[233])
    
    for i in range(234,241):
        writefile.write(lines[i])

    achFlag = False
    for ach in achievements:
        if(ach[0]!=""):
            achFlag = True
            break
    if(achFlag):
        writefile.write(lines[241])
        writefile.write(lines[242])
    writefile.write(lines[243])
    #Achievements Dynamic code
    #achievements=[["title1",["desc1", "desc2", ..]],["title2","desc2"],["title3","desc3"],["title4","desc4"],["title5","desc5"],["title6","desc6"]]
   
    for sublist in achievements:
        sublist[0] = percentReplacerString(sublist[0])
        for i in range(len(sublist[1])):
            sublist[1][i]=percentReplacerString(sublist[1][i])
        if(sublist[0]!=""):
            writefile.write(r"\resumeSubItem{"+sublist[0]+r"}") # {"+sublist[1]+r"}")
            writefile.write("\n")
            writefile.write(r"{\vspace{-7pt} \begin{itemize}")
            writefile.write("\n")
            for sub_desc in sublist[1]:
                if(sub_desc.isspace() or sub_desc==""):
                    continue
                writefile.write(r"\item "+sub_desc)
                writefile.write("\n")
            writefile.write(r"\end{itemize} }")
            writefile.write("\n")
            writefile.write("\n")
    
    #write some static code
    writefile.write(lines[250])
    if(achFlag):
        writefile.write(lines[251])
    for i in range(252,256):
        writefile.write(lines[i])

def hskip_measure(calculation_list):
    max1 = -1
    max2 = -2
    letter_per_cm = 5.77
    length_for_text = 15.75
    total_letters_allowed = 90
    for val in calculation_list["left"]:
        max1 = max(max1, val)
    for val in calculation_list["right"]:
        max2 = max(max2, val)
    total_nos = max1+max2
    total_length = round(total_nos/letter_per_cm,2)

    return length_for_text - total_length
    
    

"""
createTextFile(name="Nikitha",rollno="190102052",stream="Btech",branch="ECE",minor="CSE",college="IITG",
              email="nikithareddy@gmail.com",iitgmail="m.nikitha@iitg.ac.in",mobileno="9848670705",
              linkedin="linkedin.com/in/nikitha2309",
              education=[["d1","c1","p1","y1"],["d2","c2","p2","y2"],["","","",""]],
              projects=[["title1","club1","desc1","link1","date1"],["title2","club2","desc2","link2","date2"],["title3","club3","desc3","link3","date3"],["title4","club4","desc4","link4","date4"]],
              techskills=["pllang","webtech","dbms","os","miscell","otherskills"],
              keyCourses=["ma101","webd101","cpp110"],
              por=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"]],
              achievements=[["title1","desc1"],["title2","desc2"],["title3","desc3"],["title4","desc4"],["title5","desc5"],["title6","desc6"]])
"""



