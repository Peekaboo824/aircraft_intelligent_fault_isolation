from django.shortcuts import render

from django.http import HttpResponse
import xlrd
from .models import FI
from api.models import Image
from django.template import loader

def upload_excel(request):
    # book = xlrd.open_workbook('E:\\2021-2022spring\\mysite\\static\\file\\data.xls')
    # sheet = book.sheet_by_name('Sheet1')
    # print(sheet)
    # value_list = []
    # for i in range(1, sheet.nrows):
    #     value_list.append(FI(
    #         no=int(sheet.row_values(i)[0]),
    #         EICAS=sheet.row_values(i)[1],
    #         MaintenanceMassages=sheet.row_values(i)[2],
    #         MaintenanceMode=sheet.row_values(i)[3],
    #         FaultReportPath=sheet.row_values(i)[4],
    #         FaultReport=sheet.row_values(i)[5],
    #         diagram=sheet.row_values(i)[6],
    #         diagnosis=sheet.row_values(i)[7],
    #         tips=sheet.row_values(i)[8]
    #     ))
    #     # print(sheet.row_values(i))
    # FI.objects.bulk_create(value_list)
    return HttpResponse('Hello World!')

def check_mm(ll):
    MM = FI.objects.all().values('MaintenanceMassages')
    #FR = FI.objects.all().values('FaultReport')
    dd = []
    # print(len(MM))
    # print(len(FRP))
    for i in range(0, len(MM)):
        tmp = []
        x = MM[i]['MaintenanceMassages'].split(',')
        #y = FR[i]['FaultReport'].split('\n')
        for j in range(0, len(x)):
            x[j] = x[j].replace('\n', '')
            x[j] = x[j].replace('\r', '')
        # for j in range(0, len(y)):
        #     y[j] = y[j].replace('\r', '')
        for j in range(len(x) - 1, -1, -1):
            if x[j] == '':
                x.remove('')
        # for j in range(len(y) - 1, -1, -1):
        #     if y[j] == '':
        #         y.remove('')
        tmp.append(i+1)
        tmp.append(x)
        # tmp.append(y)
        dd.append(tmp)
        # print(tmp)
    # for i in range(0, len(MM)):
    #     print(dd[i])
    # ll_0 = sorted(ll[0])
    # ll_1 = sorted(ll[1])
    for i in range(0,len(ll)):
        ll[i]=ll[i].replace(" ","")
        ll[i]=ll[i].upper()
        # print(ll[i])
    print(ll)
    no=[]
    for item in dd:
        if len(item[1])<=len(ll):
            # print(item[1])
            flag=1
            for i in item[1]:
                i=i.replace(" ","")
                i=i.upper()
                # print(i)
                if i not in ll:
                    flag=0
            if flag==1:
                no.append(item[0])

    # print(no)
    return no


def check_fr(num, fr_list):  # num 可能会命中的项
    #print(num)
    no = []
    for i in range(0, len(num)):

        FR = FI.objects.filter(no=num[i]).values('FaultReport')
        FR=list(FR)
        for j in range(0, len(FR)):
            FR[j]=FR[j]['FaultReport'].split(',')
            for k in range(0, len(FR[j])):
                FR[j][k] = FR[j][k].replace('\r', '')
            for k in range(len(FR[j]) - 1, -1, -1):
                if FR[j][k] == '':
                    FR[j].remove('')
        FR.append(num[i])
        # print(FR)

        if len(FR[0]) <= len(fr_list) and len(FR[0])!=0:
            flag = 1
            for i in FR[0]:
                if i not in fr_list:
                    flag = 0
            if flag == 1:
                no.append(FR[1])

    #print(no)
    res=[]
    for i in no:
        tmp = FI.objects.filter(no=i).values('tips')
        tmp=list(tmp)
        tmp=tmp[0]['tips']
        res.append(tmp)


    #print(res)
    if (len(res)>0):
        return (no, res)
    elif (len(res)==0):
        return (-1, 'Not found')









def data_test(request,img):

    # for i in range(1, 11):
    #     with open('E:\\2021-2022spring\\mysite\\static\\file\\testmm'+str(i)+'.txt', "rb") as f:
    #         mm = f.read()
    #         # print(type(mm))
    #     with open('E:\\2021-2022spring\\mysite\\static\\file\\testfr'+str(i)+'.txt', "rb") as f:
    #         fr = f.read()
    #         # print(frp)
    #     mm = mm.decode()
    #     fr = fr.decode()
    #     mm_list=mm.split('\n')
    #     fr_list=fr.split('\n')
    #
    #     # tmp = []
    #     for i in range(0, len(mm_list)):
    #         mm_list[i] = mm_list[i].replace('\r','')
    #     for i in range(0, len(fr_list)):
    #         fr_list[i] = fr_list[i].replace('\r', '')
    #     for i in range(len(mm_list) - 1, -1, -1):
    #         if mm_list[i] == '':
    #             mm_list.remove('')
    #     for i in range(len(fr_list) - 1, -1, -1):
    #         if fr_list[i] == '':
    #             fr_list.remove('')
    #     # tmp.append(mm_list)
    #     # print(mm_list)
    #     # print(fr_list)
    #     # tmp.append(fr_list)
    #     # print(tmp)
    # print(img)
    MM = Image.objects.filter(name_cms=img).values("res_cms")
    MM=list(MM)
    MM=MM[0]["res_cms"]
    # print(MM)
    # print(type(MM))
    MM=MM.replace("[","")
    MM=MM.replace("]","")
    MM=MM.replace("'","")
    # print(MM)
    MM_=MM.split(",")
    # print(MM_)
    # print(type(MM_))
    res = check_mm(MM_)
    # print(res)
    # print(len(res))
    # res_num, res = check_fr(res, fr_list)
    # print(res_num)
    print(res)


    # return render(request, 'table/index.html')
    return HttpResponse("Hello world!")