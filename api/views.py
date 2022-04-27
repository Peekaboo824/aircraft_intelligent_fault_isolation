import json
import os
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import Image
from .edge_detection import edge_detection
from PaddleOCR.paddleocr import PaddleOCR
import cv2
from django.shortcuts import render
from PaddleOCR.ppocr.utils.logging import get_logger
from django.shortcuts import redirect
from django.http import JsonResponse
import json
import xlrd

cms_dataset = {'HYD3：SYSTEM3PRESSURETRANSDUCER': [35, 36],
               'P-ACE3-1FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 88, 117, 119],
               'P-ACE2-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87],
               'P-ACE3-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89],
               'GIOM1L-AHC-4INTERFACEFAULT': [9, 10, 11, 51],
               'GIOM2B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 46, 47, 51, 52],
               'PACE3：P-ACE3-1FSECU2INTERFACEFAULT': [70], 'P-ACE2-2FCBATTBUSINTERFACEFAULT': [116],
               'P-ACE1-1PACU1INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87], 'HYD1：SYSTEM1PRESSURETRANSDUCER': [33],
               'P-ACE5-1FSECU2INTERFACEFAULT': [73], 'PITCHCONTROLDU：PITCHDISCOUNITFAIL': [37],
               'P-ACE6-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
               'DCPUMP:DCFUELSTARTPUMP/PRSW/WRG/DCPUMPRLYFAULT': [36], 'FSECU1：NOFSECUDATATODCU': [36],
               'P-ACE1-1L-DCESSBUSINTERFACEFAULT': [108], 'IRS2：NOOUTPUT': [14],
               'LENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [36], 'NIC1：ASCBSECONDARYBUSFAULT': [48, 49],
               'P-ACE5-1L-DCBUSINTERFACEFAULT': [126], 'FUELLEFTPUMP2：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [36],
               'P-ACE6-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
               'FCM2APACU1INTERFACEFAULT': [30, 36, 37, 51],
               '/': [7, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 39, 50, 57, 58, 63, 64, 95, 101, 113, 118, 125],
               'P-ACE4-1FEECU1INTERFACEFAULT': [72],
               'FCM2BBCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
               'P-ACE6-2R-DCESSBUSINTERFACEFAULT': [131],
               'P-ACE6-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94], 'FCM1AP-ACU1INTERFACEFAULT': [15, 16],
               'FSECU2：NOFSECUOUTPUTTODCU': [43, 45, 46, 47], 'HYD1：HYD1SOVFAIL': [36],
               'P-ACE4-1FCBATTBUSINTERFACEFAULT': [123], 'FCM2AR-DCESSBUSINTERFACEFAULT': [106],
               'GIOM2R-AHC-4INTERFACEFAULT': [12, 13, 14, 48, 52], 'P-ACE2-1L-DCBUSINTERFACEFAULT': [114],
               'NICAPM1：APM1FAULT': [51], 'P-ACE6-1FSECU2INTERFACEFAULT': [75],
               'FUELXFEEDSOV:XFEEDSOV/WRG/DCUFAULT': [37],
               'FCM1BBCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
               'FCM2AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
               'P-ACE2-1FAULT': [53, 54, 55, 56, 77, 78, 81, 82, 83, 84, 86, 87, 112, 114],
               'GIOM2A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 51, 78, 86, 87, 96],
               'P-ACE1-2R-DCESSBUSINTERFACEFAULT': [110], 'PACE2：P-ACE2-2FSECU1INTERFACEFAULT': [68, 69],
               'PACE3：P-ACE3-2FAULT': [71], 'FUELRIGHTPUMP2：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [37], 'APM1FAULT': [52],
               'FCM2BP-ACU2INTERFACEFAULT': [15, 16], 'P-ACE1：P-ACE1-1FAULT': [65], 'ADC2：NOOUTPUT': [6],
               'P-ACE6-2FAULT': [54, 56, 76, 77, 78, 81, 82, 83, 86, 87, 94, 132], 'P-ACE5-1FSECU1INTERFACEFAULT': [73],
               'P-ACE6-1L-DCESSBUSINTERFACEFAULT': [129],
               'FCM2BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
               'P-ACE5-2L-DCESSBUSINTERFACEFAULT': [128], 'GIOM2R-DCU-9INTERFACEFAULT': [16, 29, 30, 36, 37, 51, 52],
               'PACE2：P-ACE2-1FSECU2INTERFACEFAULT': [67],
               'P-ACE6-1FAULT': [54, 56, 75, 77, 78, 81, 82, 83, 86, 87, 93, 129, 130],
               'P-ACE2-2L-DCESSBUSINTERFACEFAULT': [115],
               'P-ACE1-1PACU2INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87], 'IRS1：NOOUTPUT': [11],
               'GIOM2R-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51, 52], 'P-ACE5-2FSECU1INTERFACEFAULT': [74],
               'FUELRIGHTPUMP1：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [36], 'LEFTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52],
               'NIC1FAULT': [51, 52], 'HS-ACE1FAULT': [53, 56],
               'P-ACE4-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90], 'WRONGRELAYOUTPUT': [133],
               'PACE3：P-ACE3-1FSECU1INTERFACEFAULT': [70], 'NIC1：ASCBPRIMARYBUSFAULT': [48, 49],
               'P-ACE1-2PACU1INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
               'PACE1：P-ACE1-2FSECU1INTERFACEFAULT': [66],
               'GIOM1FAULT': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 30, 36, 37, 38, 40, 41, 47, 51, 52, 77, 78, 81,
                              82, 83, 86, 87, 96], 'P-ACE6-1R-DCBUSINTERFACEFAULT': [130],
               'P-ACE3-1L-DCESSBUSINTERFACEFAULT': [117], 'HS-ACE2FAULT': [54, 55], 'DCU1：NOOUTPUT': [36],
               'P-ACE2-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87],
               'FCM1BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
                              104, 105], 'PACE1：P-ACE1-1FSECU1INTERFACEFAULT': [65],
               'FCM1BP-ACU2INTERFACEFAULT': [15, 16], 'P-ACE2：P-ACE2-2FAULT': [68, 69],
               'GIOM1L-DCUINTERFACEFAULT': [16],
               'FCM1APACU1INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87],
               'PACE2：P-ACE2-2FSECU2INTERFACEFAULT': [68, 69],
               'P-ACE1-1FAULT': [53, 55, 77, 78, 79, 81, 82, 83, 86, 87, 108, 109], 'FCM2：CANBUS2BFAULT': [56],
               'FCM1：CANBUS1AFAULT': [53], 'P-ACE2：P-ACE2-1FAULT': [67], 'P-ACE6-2FSECU1INTERFACEFAULT': [76],
               'HSACE2/WRG[STICKSHAKER]FAULT': [98, 99, 100],
               'GIOM2FAULT': [1, 2, 3, 4, 5, 6, 8, 12, 13, 14, 15, 16, 30, 36, 37, 38, 40, 41, 47, 48, 51, 52, 78, 86,
                              87, 96], 'GSCMFAULT': [15, 16, 29, 36, 51, 52], 'RENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [37],
               'P-ACE6-1FSECU1INTERFACEFAULT': [75], 'P-ACE1-2PACU2INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
               'HYD2：HYD2SOVFAIL': [36], 'LPS:OXYPRSW/WRGFAULT': [37], 'P-ACE6-2FCBATTBUSINTERFACEFAULT': [132],
               'P-ACE4-1FAULT': [53, 55, 72, 77, 78, 81, 82, 83, 86, 87, 90, 122, 123], 'ADC1:NOOUTPUT': [3],
               'FCM1ABCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
               'FSECU2：SLATBIOC6INPUTNOTPRESENT': [42, 44], 'FCM1BR-DCBUSINTERFACEFAULT': [105],
               'FCM2AP-ACU1INTERFACEFAULT': [15, 16], 'OILLEVEL/TEMPSENSOR:LENGOILTEMPSENSOROUTOFRANGE': [36, 37],
               'P-ACE1-2FCBATTBUSINTERFACEFAULT': [111],
               'P-ACE1-2FAULT': [54, 56, 77, 78, 80, 81, 82, 83, 86, 87, 110, 111], 'DCU2：NOOUTPUT': [37],
               'APM1NIC1INTERFACEFAULT': [51, 52],
               'P-ACE5-2FAULT': [53, 55, 74, 77, 78, 81, 82, 83, 86, 87, 92, 127, 128],
               'FCM1AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
                              104, 105], 'FSECU2：NOFSECUDATATODCU': [37], 'PACE3：P-ACE3-1FAULT': [70],
               'P-ACE6-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94],
               'PACE2：P-ACE2-1FSECU1INTERFACEFAULT': [67], 'P-ACE5-2R-DCBUSINTERFACEFAULT': [127],
               'FCM2BPACU2INTERFACEFAULT': [30, 36, 37, 51], 'P-ACE5-2FSECU2INTERFACEFAULT': [74],
               'P-ACE3-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88],
               'P-ACE5-1FAULT': [54, 56, 73, 77, 78, 81, 82, 83, 86, 87, 91, 124, 126],
               'P-ACE5-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92],
               'FCM1BPACU2INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87],
               'P-ACE3-1FCBATTBUSINTERFACEFAULT': [119], 'FCM1：CANBUS1BFAULT': [54],
               'GIOM1A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 46, 47, 51, 52, 78, 86, 87, 96],
               'P-ACE1-1R-DCBUSINTERFACEFAULT': [109], 'NOTTR-TX-1BUSOUTPUT': [133], 'GSCM:GSCMFAULT': [37],
               'GIOM1L-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51],
               'FCM2ABCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
               'P-ACE4-1R-DCESSBUSINTERFACEFAULT': [122], 'GIOM1A-ADC-6INTERFACEFAULT': [52],
               'FSECU1：SLATBIOC6INPUTNOTPRESENT': [43, 45, 46],
               'P-ACE5-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92],
               'RIGHTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52], 'GIOM2R-DCUINTERFACEFAULT': [15], 'HYD2SOVFAIL': [37],
               'P-ACE5-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91], 'HSACE1FAULT': [96, 97],
               'P-ACE1：P-ACE1-2FAULT': [66], 'ROLLCONTROLDU：ROLLDISCOUNITFAIL': [36],
               'P-ACE3-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89], 'P-ACE4-1FSECU2INTERFACEFAULT': [72],
               'FCM2BL-DCBUSINTERFACEFAULT': [107], 'APUSOV:APUCONTROLRELAY/WRGFAULT': [36, 37],
               'P-ACE5-1R-DCESSBUSINTERFACEFAULT': [124], 'HYD2：SYSTEM2PRESSURETRANSDUCER': [34],
               'PACE1：P-ACE1-2FSECU2INTERFACEFAULT': [66],
               'P-ACE5-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91], 'HCLE:HCLEPARTITION2FAILURE': [37],
               'APM2FAULT': [52], 'APM2NIC2INTERFACEFAULT': [51, 52], 'HSACE2FAULT': [98, 99, 100],
               'P-ACE3-2FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 89, 120, 121],
               'P-ACE2-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87], 'FCM1AL-DCESSBUSINTERFACEFAULT': [104],
               'ADC2：NOR-ADC-6BUSOUTPUT': [4], 'HCLE：HCLEPARTITION1FAILURE': [36],
               'PACE3：P-ACE3-2FSECU1INTERFACEFAULT': [71], 'P-ACE2-1R-DCESSBUSINTERFACEFAULT': [112],
               'TW:TAWSFAULTREPORTED': [46], 'P-ACE3-2R-DCESSBUSINTERFACEFAULT': [120],
               'PACE1：P-ACE1-1FSECU2INTERFACEFAULT': [65],
               'P-ACE3-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88], 'NICAPM2：APM2FAULT': [51],
               'GIOM1L-DCU-9INTERFACEFAULT': [15, 29, 30, 36, 37, 51, 52, 77, 78, 81, 82, 83, 86, 87],
               'P-ACE2-2FAULT': [54, 56, 77, 78, 81, 82, 83, 85, 86, 87, 115, 116], 'FCM2：CANBUS2AFAULT': [55],
               'P-ACE6-2FSECU2INTERFACEFAULT': [76], 'HSACE1/WRG[STICKSHAKER]FAULT': [96, 97],
               'FSECU1：NOFSECUOUTPUTTODCU': [42, 44, 47],
               'P-ACE4-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90], 'P-ACE3-2L-DCBUSINTERFACEFAULT': [121],
               'P-ACE2-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87],
               'GIOM1B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 52],
               'PACE3：P-ACE3-2FSECU2INTERFACEFAULT': [71], 'FUELLEFTPUMP1：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [37]}


class Ocr:
    def __init__(self, image_path, det_model_dir, cls_model_dir, rec_model_dir):
        self.image_path = image_path
        self.det_model_dir = det_model_dir
        self.cls_model_dir = cls_model_dir
        self.rec_model_dir = rec_model_dir
        self.img = cv2.imread(self.image_path)
        if self.img is None:
            logger = get_logger()
            logger.error("error in loading image:{}".format(self.image_path))

    def identify(self):
        # Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
        # 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
        ocr = PaddleOCR(self.det_model_dir, self.cls_model_dir, self.rec_model_dir, use_angle_cls=True, lang="ch")
        result = ocr.ocr(self.img, cls=True)
        return result


def CMS(request):
    CMS_list = []
    if request.method == "POST":
        imageSrc = request.FILES.getlist('image')
        if imageSrc:
            for i in range(0, len(imageSrc)):
                image = imageSrc[i]
                # new_img = Image(
                #     name=image.name,
                #     image=image,
                #     res=""
                # )
                # new_img.name_cms=image.name
                # new_img.image_cms=image
                # new_img.save()
                with open("static/image/CMS/" + image.name, 'wb') as f:
                    for c in image.chunks():
                        f.write(c)
                img_path = "static/image/CMS/" + image.name
                print(img_path)
                edge_detection(img_path)

                det_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_det_infer"
                cls_model_dir = "PaddleOCR/inference/ch_ppocr_mobile_v2.0_cls_infer"
                rec_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_rec_infer"
                ocr = Ocr(img_path, det_model_dir, cls_model_dir, rec_model_dir)
                ocr_result = ocr.identify()
                ocr_list = []
                for line1 in ocr_result:
                    if line1[1][0].find("LRU:") != -1 or line1[1][0].find("RU:") != -1 or line1[1][0].find(
                            "LRU：") != -1 or \
                            line1[1][0].find("RU：") != -1 or \
                            line1[1][0].find("LRU;") != -1 or line1[1][0].find("RU;") != -1 or line1[1][0].find(
                        "LRU；") != -1 or line1[1][0].find("RU；") != -1 or \
                            line1[1][0].find("LRUS") != -1 or line1[1][0].find("LRUs") != -1:  # 找 LRU
                        # ocr_list.append(line1)
                        dis = line1[0][3][1] - line1[0][0][1]
                        # print('dis=', dis)
                        for line2 in ocr_result:
                            if line1[0][0][1] + dis + int(dis / 4) <= line2[0][0][1] <= line1[0][0][
                                1] + 2 * dis + dis / 3 and line2[0][0][1] - line1[0][3][1] >= 5 and line2[0][0][0] - \
                                    line1[0][0][0] <= 100 \
                                    and line2[1][0].find("NEXT PAGE") == -1:
                                ocr_list.append(line2[1][0])

                # print(ocr_list)
                # new_img.res_cms=ocr_list
                # new_img.save()

                CMS_list.append({"id": i, "res": ocr_list})

            res_all = {"res_all": CMS_list}
            print(res_all)
            return JsonResponse(res_all, json_dumps_params={"ensure_ascii": False})
        else:
            return HttpResponse('上传失败')


# maintenance messages 2
# fault report path    4
# fault report         5
# 排故提示               8
def rte_data(no, col):
    book = xlrd.open_workbook('statics\\file\\data.xls')
    sheet = book.sheet_by_name('Sheet1')
    res = {}
    for i in no:
        tmp = sheet.row_values(i)[col].split('\n')
        item = []
        for j in tmp:
            j = j.replace("\r", "")
            j = j.replace(' ', "")
            if j != "":
                item.append(j)
        res[i] = item
    return res


def CMS_find(cms_list):
    for i in range(0, len(cms_list)):
        cms_list[i] = cms_list[i].replace(' ', '')
        cms_list[i] = cms_list[i].upper()
    A=set()
    for item in cms_list:
        if item in cms_dataset.keys():
            A = A | set(cms_dataset[item])  # 倒排索引结果取并集
    A = list(A)
    print(A)
    res = rte_data(A, 2)
    print(res)
    hit = []
    for i in A:
        if set(res[i]) <= set(cms_list):
            hit.append(i)
    print(hit)
    frp = rte_data(hit, 4)
    print(frp)
    flag = 0
    for i in hit:
        if len(frp[i]) != 0 and frp[i][0] != '/' and frp[i][0] != '未记录':
            flag = 1
            break
    if flag == 0:  # fault report path 为空，返回排故提示
        ans = {}
        tmp = []
        fault_info = rte_data(hit, 8)
        for i in hit:
            tmp.extend(fault_info[i])
        ans["status"] = 0  # 直接返回排故提示
        ans["res"] = tmp
        print(ans)
        return ans
    else:  # 返回 fault report path
        ans = {}
        tmp = []
        for i in hit:
            tmp.extend(frp[i])
        ans["status"] = 1  # 返回fault report path
        ans["res"] = tmp
        print(ans)
        return ans


def CMS_confirm(request):
    if request.method == "POST":
        cms = request.POST.get('data')
        cms_list = []
        for i in range(0, len(cms["res_all"])):
            cms_list.extend(cms["res_all"][i]["res"])
        ans = CMS_find(cms_list)
        return JsonResponse(ans, json_dumps_params={"ensure_ascii": False})
    else:
        return HttpResponse('上传失败')


def cal_miss(tmp0):
    miss = []  # 插入缺失值
    if (len(tmp0) >= 3):
        delta0_list = [tmp0[1][0] - tmp0[0][0], tmp0[2][0] - tmp0[1][0], tmp0[-1][0] - tmp0[-2][0],
                       tmp0[-2][0] - tmp0[-3][0]]
        delta0_list.sort()
        delta0 = (delta0_list[1] + delta0_list[2]) / 2
    else:
        delta0 = 16
    n_delta = delta0
    for i in range(0, len(tmp0) - 1):
        if tmp0[i + 1][0] - tmp0[i][0] >= n_delta + n_delta - 3:
            miss.append(i + 1)
        else:
            n_delta = (tmp0[i + 1][0] - tmp0[i][0] + n_delta) / 2
    for i in range(1, len(miss)):
        miss[i] += i
    for i in range(0, len(miss)):
        tmp0.insert(miss[i], [0, "???"])
    return tmp0


def FR(request):
    FR_list = []
    if request.method == "POST":
        imageSrc = request.FILES.getlist('image')
        if imageSrc:
            for k in range(0, len(imageSrc)):
                image = imageSrc[k]
                # new_img = Image(
                #     name=image.name,
                #     image=image,
                #     res=""
                # )
                # new_img.name_cms=image.name
                # new_img.image_cms=image
                # new_img.save()
                with open("static/image/FR/" + image.name, 'wb') as f:
                    for c in image.chunks():
                        f.write(c)
                img_path = "static/image/FR/" + image.name
                print(img_path)
                edge_detection(img_path)

                det_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_det_infer"
                cls_model_dir = "PaddleOCR/inference/ch_ppocr_mobile_v2.0_cls_infer"
                rec_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_rec_infer"
                ocr = Ocr(img_path, det_model_dir, cls_model_dir, rec_model_dir)
                ocr_result = ocr.identify()

                # for line in ocr_result:
                #     print(line)
                # print(len(ocr_result))
                # print('\n')
                result = []
                # 找表头
                tmp = []
                x = 20
                for i in range(0, len(ocr_result)):
                    if ("MONITORNAME" in ocr_result[i][1][0] or "MONITORNANE" in ocr_result[i][1][
                        0] or "MONITOR NAME" in
                            ocr_result[i][1][0] or "NONITOR NANE" in ocr_result[i][1][0] or "MONITOR NANE" in
                            ocr_result[i][1][0]):
                        tmp.append((ocr_result[i][0][0], ocr_result[i][0][1], ocr_result[i][1][0]))  # 找 monitor name
                        x = ocr_result[i][0][0][0]

                        if "ACE" in ocr_result[i - 1][1][0] or "FCM" in ocr_result[i - 1][1][0] or "1A" in \
                                ocr_result[i - 1][1][0] or "1B" in ocr_result[i - 1][1][0]:
                            tmp.append(((ocr_result[i - 1][0][0], ocr_result[i - 1][0][1], ocr_result[i - 1][1][0])))
                        if "ACE" in ocr_result[i - 2][1][0] or "FCM" in ocr_result[i - 2][1][0] or "1A" in \
                                ocr_result[i - 2][1][0] or "1B" in ocr_result[i - 2][1][0]:
                            tmp.append(((ocr_result[i - 2][0][0], ocr_result[i - 2][0][1], ocr_result[i - 2][1][0])))
                        if "ACE" in ocr_result[i + 1][1][0] or "FCM" in ocr_result[i + 1][1][0] or "1A" in \
                                ocr_result[i + 1][1][0] or "1B" in ocr_result[i + 1][1][0]:
                            tmp.append(((ocr_result[i + 1][0][0], ocr_result[i + 1][0][1], ocr_result[i + 1][1][0])))
                        if "ACE" in ocr_result[i + 2][1][0] or "FCM" in ocr_result[i + 2][1][0] or "1A" in \
                                ocr_result[i + 2][1][0] or "1B" in ocr_result[i + 2][1][0]:
                            tmp.append(((ocr_result[i + 2][0][0], ocr_result[i + 2][0][1], ocr_result[i + 2][1][0])))
                tmp.sort()
                title = []
                tmp_ = []
                for i in tmp:
                    title.append(i)
                for i in tmp:
                    # print(i)
                    tmp_.append(i[2])
                result.append(tmp_)
                # print(tmp)
                # print(tmp_)

                if (len(title) == 3):
                    dis0 = title[0][0][0]
                    dis1m = title[1][0][0]
                    dis1M = title[1][1][0]
                    dis2m = title[2][0][0]
                    dis2M = title[2][1][0]
                    tmp0 = []
                    tmp1 = []
                    tmp2 = []
                    for line in ocr_result:
                        if (dis0 - 15) <= line[0][0][0] <= (dis0 + 15) and line[1][0].find("RETURN") == -1 and line[1][
                            0] != \
                                tmp[0][2]:  # 不为 monitor name 且不为 return
                            str = []
                            str.append((line[0][0][1], line[1][0]))
                            for line1 in ocr_result:
                                if line[0][0][1] - 5 <= line1[0][0][1] <= line[0][0][1] + 5 and line1 != line and len(
                                        line1[1][0]) != 1:
                                    str.append((line1[0][0][1], line1[1][0]))
                            str.sort()
                            ss = ""
                            for i in str:
                                ss += i[1]
                            tmp0.append((str[0][0], ss))

                    for line in ocr_result:
                        if (dis1m - 15) <= line[0][0][0] <= dis1M and len(line[1][0]) == 1 and line[0][0][1] > \
                                title[1][0][
                                    1]:  # 不为title
                            tmp1.append((line[0][0][1], line[1][0]))
                    for line in ocr_result:
                        if dis2m - 15 <= line[0][0][0] <= dis2M and len(line[1][0]) == 1 and line[0][0][1] > \
                                title[2][0][
                                    1]:  # 不为title
                            tmp2.append((line[0][0][1], line[1][0]))
                    # print(tmp0)
                    # print(len(tmp0))
                    # print(tmp1)
                    # print(len(tmp1))
                    # print(tmp2)
                    # print(len(tmp2))
                    if (len(tmp0) == len(tmp1) == len(tmp2)):
                        tmp0.sort()
                        tmp1.sort()
                        tmp2.sort()
                        for i in range(0, len(tmp0)):
                            tmp = []
                            tmp.append(tmp0[i][1])
                            tmp.append(tmp1[i][1])
                            tmp.append(tmp2[i][1])
                            result.append(tmp)
                        # for i in range(0, len(result)):
                        #     print(result[i])
                    else:
                        tmp0.sort()
                        tmp1.sort()
                        tmp2.sort()
                        tmp0 = cal_miss(tmp0)
                        tmp1 = cal_miss(tmp1)
                        tmp2 = cal_miss(tmp2)
                        # print(len(tmp0), len(tmp1), len(tmp2))
                        for i in range(0, min(len(tmp0), len(tmp1), len(tmp2))):
                            tmp = []
                            tmp.append(tmp0[i][1])
                            tmp.append(tmp1[i][1])
                            tmp.append(tmp2[i][1])
                            result.append(tmp)
                        # for i in range(0, len(result)):
                        #     print(result[i])

                if (len(title) == 2):
                    dis0 = title[0][0][0]
                    dis1m = title[1][0][0]
                    dis1M = title[1][1][0]
                    tmp0 = []
                    tmp1 = []
                    for line in ocr_result:
                        if (dis0 - 15) <= line[0][0][0] <= (dis0 + 15) and line[1][0].find("RETURN") == -1 and line[1][
                            0] != \
                                tmp[0][
                                    2]:  # 不为 monitor name 且不为 return
                            str = []
                            str.append((line[0][0][1], line[1][0]))
                            for line1 in ocr_result:
                                if line[0][0][1] - 5 <= line1[0][0][1] <= line[0][0][1] + 5 and line1 != line and len(
                                        line1[1][0]) != 1:
                                    str.append((line1[0][0][1], line1[1][0]))
                            str.sort()
                            ss = ""
                            for i in str:
                                ss += i[1]
                            tmp0.append((str[0][0], ss))
                    for line in ocr_result:
                        if (dis1m - 15) <= line[0][0][0] <= dis1M and len(line[1][0]) == 1 and line[0][0][1] > \
                                title[1][0][
                                    1]:
                            tmp1.append((line[0][0][1], line[1][0]))
                    if (len(tmp0) == len(tmp1)):
                        tmp0.sort()
                        tmp1.sort()

                        for i in range(0, len(tmp0)):
                            tmp = []
                            tmp.append(tmp0[i][1])
                            tmp.append(tmp1[i][1])

                            result.append(tmp)
                        # for i in range(0, len(result)):
                        #     print(result[i])
                    else:
                        tmp0.sort()
                        tmp1.sort()
                        tmp0 = cal_miss(tmp0)
                        tmp1 = cal_miss(tmp1)
                        # print(len(tmp0), len(tmp1))
                        for i in range(0, min(len(tmp0), len(tmp1))):
                            tmp = []
                            tmp.append(tmp0[i][1])
                            tmp.append(tmp1[i][1])
                            result.append(tmp)
                        # for i in range(0, len(result)):
                        #     print(result[i])

                FR_list.append({"id": k, "res": result})
                res_all = {"res_all": FR_list}
                return JsonResponse(res_all, json_dumps_params={"ensure_ascii": False})
            else:
                return HttpResponse('上传失败')
