from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from .models import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse
from django.contrib import messages
from Candidate.forms import StudentUserForm, CandidateForm, FreezeForm


# Create your views here.


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def home(request):
    if request.user.is_authenticated:
        dict1 = Candidate.objects.filter(user=request.user)

        if len(dict1) > 0:
            if dict1[0].is_admin == 1 :
                return render(request,'Candidate/admin.html')
            else:
                freeze_form = FreezeForm()
                if dict1[0].freeze == 1:
                    return render(request, 'Candidate/freezed.html', {'seat': dict1[0].final_seat})
                else:
                    return render(request, 'Candidate/base.html', {'seat': dict1[0].final_seat, 'freeze': freeze_form})
        else:
            return render(request, 'Candidate/removed.html')
    else:
        # not logged in
        return render(request, 'Candidate/base.html')


def admin_home(request):
    if request.user.is_authenticated:
        dict1 = Candidate.objects.filter(user=request.user)
        if len(dict1) > 0:
            return render(request, 'Candidate/admin.html')
        else:
            return render(request, 'Candidate/admin.html')
    else:
        # not logged in
        return render(request, 'Candidate/base.html')


def register(request):
    registered = False
    if request.method == "POST":
        print("hahaha")
        user_form = StudentUserForm(data=request.POST)
        info_form = CandidateForm(data=request.POST)
        if user_form.is_valid() and info_form.is_valid():
            print("lalala")
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = info_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            if user:
                print("papapa")
                if user.is_active:
                    print("oaoaoa")
                    login(request, user)
                    return HttpResponseRedirect(reverse('home'))

                else:
                    return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponseRedirect(reverse('home'))
    else:
        user_form = StudentUserForm()
        info_form = CandidateForm()
    return render(request, 'Candidate/register_page.html',
                  {'user_form': user_form, 'info_form': info_form, 'registered': registered, 'registerFlag': 0})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)

                # to check the type of user to log in

                dict1 = Candidate.objects.filter(user=request.user)

                if len(dict1) > 0:
                    if dict1[0].is_admin == 1:
                        return HttpResponseRedirect(reverse('admin_home'))
                    else:
                        return HttpResponseRedirect(reverse('home'))
                else:
                    return HttpResponseRedirect(reverse('home'))

            else:
                return HttpResponse('ACCOUNT NOT ACTIVE')
        else:
            print("someone tried to login and failed")
            print("Username: {} Password: {}".format(username, password))
            return HttpResponse("invalid login details supplied")
    else:
        return render(request, 'Candidate/base.html', {})


def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'Candidate/change_password.html', {
        'form': form
    })


def ChoiceFilling(request):
    if request.POST:
        print(request.POST)
        cand = Candidate.objects.get(user=request.user)
        if(cand.locked == 0):
            lock = 0
            if "ADD" in request.POST and "choice" in request.POST:
                arr = []
                branchprefdone = []
                branches = Branch.objects.all()
                pref = cand.preferences
                ask = ""
                if pref is ask:
                    cand.preferences = str(request.POST['choice'])
                else:
                    cand.preferences = str(cand.preferences) + "," + str(request.POST['choice'])
                cand.save()
                pref = cand.preferences
                if pref:
                    arr = pref.split(",")
                    for x in arr:
                        temp = x.split('-')
                        if len(temp) == 2:
                            branchprefdone.append(
                                Branch.objects.get(name=temp[1], college=College.objects.get(name=temp[0])))
                #     branchprefdone = Branch.objects.filter(name__in=brname,college_name__in=coll)
                branchrem = []
                for x in branches:
                    if x not in branchprefdone:
                        branchrem.append(x)
            elif "REMOVE" in request.POST and "Rchoice" in request.POST:
                print(len(request.POST['Rchoice']))
                print("-----------=-=-----------=-=-=--==-=-=-=-==-=-=-=-=-=-=-=-=-=-=-=-==-==-=-=-=-=--=-=-=-")
                arr = []
                branchprefdone = []
                branches = Branch.objects.all()
                cand = Candidate.objects.get(user=request.user)
                pref = cand.preferences
                temppref = ""
                if pref is not None:
                    arr = pref.split(",")
                    for x in arr:
                        if x in request.POST['Rchoice']:
                            pass
                        elif temppref == "":
                            temppref = x
                        else:
                            print(x)
                            temppref = temppref + ',' + x
                cand.preferences = temppref
                cand.save()
                pref = temppref
                if pref:
                    arr1 = pref.split(",")
                    for x in arr1:
                        temp = x.split('-')
                        if len(temp) == 2:
                            branchprefdone.append(
                                Branch.objects.get(name=temp[1], college=College.objects.get(name=temp[0])))
                #     branchprefdone = Branch.objects.filter(name__in=brname,college_name__in=coll)
                branchrem = []
                for x in branches:
                    if x not in branchprefdone:
                        branchrem.append(x)

            else:
                arr = []
                branchprefdone = []
                branches = Branch.objects.all()
                cand = Candidate.objects.get(user=request.user)
                pref = cand.preferences
                if pref:
                    arr = pref.split(",")
                    for x in arr:
                        temp = x.split('-')
                        if len(temp) == 2:
                            branchprefdone.append(
                                Branch.objects.get(name=temp[1], college=College.objects.get(name=temp[0])))
                branchrem = []
                for x in branches:
                    if x not in branchprefdone:
                        branchrem.append(x)
        else:
            lock = 1;
            arr = []
            branchprefdone = []
            branches = Branch.objects.all()
            cand = Candidate.objects.get(user=request.user)
            pref = cand.preferences
            if pref:
                arr = pref.split(",")
                coll = []
                brname = []
                temp = []
                for x in arr:
                    temp = x.split('-')
                    if len(temp) == 2:
                        branchprefdone.append(Branch.objects.get(name=temp[1], college=College.objects.get(name=temp[0])))
            branchrem = []
            for x in branches:
                if x not in branchprefdone:
                    branchrem.append(x)
    else:
        arr = []
        branchprefdone = []
        branches = Branch.objects.all()
        cand = Candidate.objects.get(user=request.user)
        lock = cand.locked
        pref = cand.preferences
        if pref:
            arr = pref.split(",")
            coll = []
            brname = []
            temp = []
            for x in arr:
                temp = x.split('-')
                if len(temp) == 2:
                    branchprefdone.append(Branch.objects.get(name=temp[1], college=College.objects.get(name=temp[0])))
        branchrem = []
        for x in branches:
            if x not in branchprefdone:
                branchrem.append(x)

    return render(request, 'Candidate/choicefilling.html',
                  {'branches': branches, 'branchprefdone': branchprefdone, 'branchrem': branchrem, 'lock':lock})


def brnull(request):
    br = Branch.objects.all()
    for i in br:
        i.gen_capacity_filled = 0
        i.gen_pwd_capacity_filled = 0
        i.obc_ncl_capacity_filled = 0
        i.obc_ncl_pwd_capacity_filled = 0
        i.sc_capacity_filled = 0
        i.sc_pwd_capacity_filled = 0
        i.st_capacity_filled = 0
        i.st_pwd_capacity_filled = 0
        i.save()

    cands = Candidate.objects.filter(freeze=1, removed=0)
    for cand in cands:
        cat = cand.quota_for_seat
        if cat == "GEN":
            cand.final_seat.gen_capacity_filled += 1
            cand.final_seat.save()
        if cat == "OBC":
            cand.final_seat.obc_ncl_capacity_filled += 1
            cand.final_seat.save()
        if cat == "SC":
            cand.final_seat.sc_capacity_filled += 1
            cand.final_seat.save()
        if cat == "ST":
            cand.final_seat.st_capacity_filled += 1
            cand.final_seat.save()
        if cat == "GENPWD":
            cand.final_seat.gen_pwd_capacity_filled += 1
            cand.final_seat.save()
        if cat == "OBCPWD":
            cand.final_seat.obc_ncl_pwd_capacity_filled += 1
            cand.final_seat.save()
        if cat == "SCPWD":
            cand.final_seat.sc_pwd_capacity_filled += 1
            cand.final_seat.save()
        if cat == "STPWD":
            cand.final_seat.st_pwd_capacity_filled += 1
            cand.final_seat.save()

    return HttpResponseRedirect(reverse('admin_home'))


def to_freeze(request):
    if request.POST:
        rollnumber = request.POST['rollnumber']
        cand = Candidate.objects.get(rollnumber=rollnumber)
        cand.freeze = 1
        cand.save()
        return HttpResponseRedirect(reverse('home'))

def to_slide(request):
    if request.POST:
        rollnumber = request.POST['rollnumber']
        cand = Candidate.objects.get(rollnumber=rollnumber)
        fseat = str(cand.final_seat)
        pref = str(cand.preferences)
        if fseat is not None:
            arrrr = fseat.split('-')
            colseat=arrrr[0]
            if pref is not None:
                pref_arr = pref.split(",")
                pref = ""
                for br in pref_arr:
                    br_arr = br.split('-')
                    if(colseat == br_arr[0]):
                        brn = br_arr[1]
                        if pref is "":
                            pref=colseat+"-"+brn
                        else:
                            pref+=","+colseat+"-"+brn
        cand.preferences = pref
        cand.save()
        return HttpResponseRedirect(reverse('home'))

def to_remove(request):
    if request.POST:
        rollnumber = request.POST['rollnumber']
        cand = Candidate.objects.get(rollnumber=rollnumber)
        cand.removed = 1
        id = cand.id
        logout(request)
        Candidate.objects.filter(id=id).delete()
        return HttpResponseRedirect(reverse('home'))


def assign(request):
    cands = Candidate.objects.filter(freeze=0, removed=0, is_admin=0)
    for cand in cands:
        cand.locked = 1
        cand.save()
        if(cand.freeze == 2):
            pass
        else:
            if cand.category == "GEN":
                pref = cand.preferences
                if pref is not None:
                    pref_arr = pref.split(",")
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "OBC":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.obc_ncl_capacity_filled < asd.obc_ncl_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "OBC"
                            cand.save()
                            asd.obc_ncl_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "SC":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.sc_capacity_filled < asd.sc_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "SC"
                            cand.save()
                            asd.sc_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "ST":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.st_capacity_filled < asd.st_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "ST"
                            cand.save()
                            asd.st_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "GENPWD":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.gen_pwd_capacity_filled < asd.gen_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GENPWD"
                            cand.save()
                            asd.gen_pwd_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "OBCPWD":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.gen_pwd_capacity_filled < asd.gen_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GENPWD"
                            cand.save()
                            asd.gen_pwd_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.obc_ncl_capacity_filled < asd.obc_ncl_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "OBC"
                            cand.save()
                            asd.obc_ncl_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.obc_ncl_pwd_capacity_filled < asd.obc_ncl_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "OBCPWD"
                            cand.save()
                            asd.obc_ncl_pwd_capacity_filled += 1
                            asd.save()
                            break
            elif cand.category == "SCPWD":
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.gen_pwd_capacity_filled < asd.gen_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GENPWD"
                            cand.save()
                            asd.gen_pwd_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.sc_capacity_filled < asd.sc_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "SC"
                            cand.save()
                            asd.sc_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.sc_pwd_capacity_filled < asd.sc_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "SCPWD"
                            cand.save()
                            asd.sc_pwd_capacity_filled += 1
                            asd.save()
                            break
            else:
                pref = cand.preferences
                print(pref)
                if pref is not None:
                    pref_arr = pref.split(",")
                    print(pref_arr)
                    for br in pref_arr:
                        br_arr = br.split('-')
                        brn = br_arr[1]
                        print(br_arr[1])
                        clg = College.objects.get(name=br_arr[0])
                        clg_id = clg.id
                        asd = Branch.objects.get(name=brn, college=clg_id)
                        if asd.gen_capacity_filled < asd.gen_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GEN"
                            cand.save()
                            asd.gen_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.gen_pwd_capacity_filled < asd.gen_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "GENPWD"
                            cand.save()
                            asd.gen_pwd_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.st_capacity_filled < asd.st_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "ST"
                            cand.save()
                            asd.st_capacity_filled += 1
                            asd.save()
                            break
                        elif asd.st_pwd_capacity_filled < asd.st_pwd_capacity:
                            cand.final_seat = asd
                            cand.quota_for_seat = "STPWD"
                            cand.save()
                            asd.st_pwd_capacity_filled += 1
                            asd.save()
                            break

    return HttpResponseRedirect(reverse('admin_home'))

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

