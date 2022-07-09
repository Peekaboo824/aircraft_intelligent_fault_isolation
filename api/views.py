import json
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
from edge_detection.detect import run

cms_dataset = {'GSCMFAULT': [15, 16, 29, 36, 51, 52], 'PITCHCONTROLDU：PITCHDISCOUNITFAIL': [37],
               'PACE1：P-ACE1-1FSECU2INTERFACEFAULT': [65], 'P-ACE5-2FSECU2INTERFACEFAULT': [74],
               'GIOM2FAULT': [1, 2, 3, 4, 5, 6, 8, 12, 13, 14, 15, 16, 30, 36, 37, 38, 40, 41, 47, 48, 51, 52, 78, 86,
                              87, 96],
               'FCM1AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
                              104, 105], 'P-ACE5-1L-DCBUSINTERFACEFAULT': [126], 'APM1NIC1INTERFACEFAULT': [51, 52],
               'P-ACE5-2R-DCBUSINTERFACEFAULT': [127], 'P-ACE4-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90],
               'FCM1AP-ACU1INTERFACEFAULT': [15, 16], 'P-ACE5-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92],
               'GIOM1L-DCU-9INTERFACEFAULT': [15, 29, 30, 36, 37, 51, 52, 77, 78, 81, 82, 83, 86, 87],
               'LPS:OXYPRSW/WRGFAULT': [37], 'GIOM2R-DCUINTERFACEFAULT': [15], 'P-ACE1：P-ACE1-2FAULT': [66],
               'FCM2ABCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
               'P-ACE5-2DIRECTMODESWITCHINTERFACEFAULT': [138],
               'P-ACE2-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87], 'IRS1：NOOUTPUT': [11],
               'P-ACE6-2FAULT': [54, 56, 76, 77, 78, 81, 82, 83, 86, 87, 94, 132, 133, 134, 136, 140],
               'PACE2：P-ACE2-1FSECU2INTERFACEFAULT': [67],
               'FCM2BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
               'P-ACE2-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87],
               'FCM1APACU1INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87],
               'HSACE1/WRG[STICKSHAKER]FAULT': [96, 97],
               'FCM2AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
               'FCM1BR-DCBUSINTERFACEFAULT': [105], 'PACE3：P-ACE3-1FSECU2INTERFACEFAULT': [70], 'DCU2：NOOUTPUT': [37],
               'P-ACE3-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88],
               'FCM2BPACU2INTERFACEFAULT': [30, 36, 37, 51],
               'P-ACE1-1PACU1INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87], 'APM2FAULT': [52],
               'P-ACE1-1FAULT': [53, 55, 77, 78, 79, 81, 82, 83, 86, 87, 108, 109],
               'FCM2BP-ACU2INTERFACEFAULT': [15, 16], 'HCLE:HCLEPARTITION2FAILURE': [37],
               'P-ACE3-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89],
               'HSACE2/WRG[STICKSHAKER]FAULT': [98, 99, 100], 'P-ACE1：P-ACE1-1FAULT': [65],
               'P-ACE4-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90],
               'P-ACE6-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
               'GIOM2B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 46, 47, 51, 52],
               'P-ACE5-2FSECU1INTERFACEFAULT': [74], 'LEFTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52],
               'HSACE1FAULT': [96, 97], 'P-ACE1-2PACU1INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
               'P-ACE5-1R-DCESSBUSINTERFACEFAULT': [124], 'GIOM2R-DCU-9INTERFACEFAULT': [16, 29, 30, 36, 37, 51, 52],
               'PACE3：P-ACE3-2FSECU2INTERFACEFAULT': [71], 'FCM1AL-DCESSBUSINTERFACEFAULT': [104],
               'FCM1BP-ACU2INTERFACEFAULT': [15, 16], 'NIC1：ASCBSECONDARYBUSFAULT': [48, 49],
               'GIOM1L-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51], 'FSECU1：NOFSECUOUTPUTTODCU': [42, 44, 47],
               'P-ACE5-2FAULT': [53, 55, 74, 77, 78, 81, 82, 83, 86, 87, 92, 127, 128, 135, 136],
               'IBSUPPLYPRESSURELOW': [140, 141, 142], 'FUELRIGHTPUMP2：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [37],
               'P-ACE3-2UPRUDPCUEHSVLVDTINTERFACEFAULT': [139], 'P-ACE5-2L-DCESSBUSINTERFACEFAULT': [128],
               'P-ACE4-1FEECU1INTERFACEFAULT': [72], 'P-ACE6-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
               'PACE3：P-ACE3-2FSECU1INTERFACEFAULT': [71], 'FUELRIGHTPUMP1：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [36],
               'FSECU1：NOFSECUDATATODCU': [36], 'P-ACE2-1L-DCBUSINTERFACEFAULT': [114],
               'FCM2AP-ACU1INTERFACEFAULT': [15, 16], 'P-ACE3-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88],
               'P-ACE4-1FCBATTBUSINTERFACEFAULT': [123], 'ROLLCONTROLDU：ROLLDISCOUNITFAIL': [36],
               'GIOM2R-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51, 52], 'NICAPM1：APM1FAULT': [51],
               'P-ACE5-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91], 'P-ACE6-1R-DCBUSINTERFACEFAULT': [130],
               'FCM2BL-DCBUSINTERFACEFAULT': [107], 'P-ACE1-1L-DCESSBUSINTERFACEFAULT': [108],
               'FSECU1：SLATBIOC6INPUTNOTPRESENT': [43, 45, 46], 'NIC1：ASCBPRIMARYBUSFAULT': [48, 49],
               'PACE1：P-ACE1-2FSECU1INTERFACEFAULT': [66], 'FUELLEFTPUMP1：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [37],
               'P-ACE6-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94], 'HCLE：HCLEPARTITION1FAILURE': [36],
               'HYD2：HYD2SOVFAIL': [36], 'PACE3：P-ACE3-1FAULT': [70], 'P-ACE6-1FSECU2INTERFACEFAULT': [75],
               'HYD1：HYD1SOVFAIL': [36], 'P-ACE1-2PACU2INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
               'FCM2：CANBUS2BFAULT': [56], 'P-ACE6-1FAULT': [54, 56, 75, 77, 78, 81, 82, 83, 86, 87, 93, 129, 130],
               'PACE3：P-ACE3-1FSECU1INTERFACEFAULT': [70], 'P-ACE4-1FSECU2INTERFACEFAULT': [72],
               'NICAPM2：APM2FAULT': [51], 'FCM1BPACU2INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87],
               'FSECU2：NOFSECUOUTPUTTODCU': [43, 45, 46, 47],
               'GIOM1B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 52],
               'RENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [37], 'P-ACE3-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89],
               'FCM2AR-DCESSBUSINTERFACEFAULT': [106], 'PACE2：P-ACE2-1FSECU1INTERFACEFAULT': [67],
               'P-ACE6-1FSECU1INTERFACEFAULT': [75], 'ADC1:NOOUTPUT': [3], 'FUELXFEEDSOV:XFEEDSOV/WRG/DCUFAULT': [37],
               'APUSOV:APUCONTROLRELAY/WRGFAULT': [36, 37],
               'P-ACE2-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87],
               'P-ACE5-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91], 'P-ACE1-1R-DCBUSINTERFACEFAULT': [109],
               'GIOM1L-DCUINTERFACEFAULT': [16], 'GSCM:GSCMFAULT': [37],
               '/': [7, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 39, 50, 57, 58, 63, 64, 95, 101, 113, 118, 125],
               'P-ACE1-1PACU2INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87],
               'P-ACE3-1L-DCESSBUSINTERFACEFAULT': [117], 'FCM2APACU1INTERFACEFAULT': [30, 36, 37, 51],
               'GIOM1A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 46, 47, 51, 52, 78, 86, 87, 96],
               'P-ACE2-2FCBATTBUSINTERFACEFAULT': [116], 'P-ACE3-2R-DCESSBUSINTERFACEFAULT': [120],
               'FUELLEFTPUMP2：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [36], 'HYD3：SYSTEM3PRESSURETRANSDUCER': [35, 36],
               'RUDDERMIDPCUFAULT': [135, 136, 137], 'HYD2：SYSTEM2PRESSURETRANSDUCER': [34],
               'P-ACE3-1FCBATTBUSINTERFACEFAULT': [119], 'HS-ACE2FAULT': [54, 55],
               'P-ACE1-2FAULT': [54, 56, 77, 78, 80, 81, 82, 83, 86, 87, 110, 111],
               'FCM1BBCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
               'GIOM1A-ADC-6INTERFACEFAULT': [52], 'FCM2：CANBUS2AFAULT': [55],
               'P-ACE2-2L-DCESSBUSINTERFACEFAULT': [115],
               'P-ACE4-1FAULT': [53, 55, 72, 77, 78, 81, 82, 83, 86, 87, 90, 122, 123],
               'RIGHTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52], 'P-ACE2：P-ACE2-1FAULT': [67],
               'ADC2：NOR-ADC-6BUSOUTPUT': [4], 'P-ACE6-2R-DCESSBUSINTERFACEFAULT': [131],
               'NOTTR-TX-1BUSOUTPUT': [133, 136], 'PACE1：P-ACE1-2FSECU2INTERFACEFAULT': [66],
               'P-ACE2：P-ACE2-2FAULT': [68, 69],
               'FCM2BBCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
               'P-ACE6-2FSECU2INTERFACEFAULT': [76], 'P-ACE6-2FSECU1INTERFACEFAULT': [76],
               'P-ACE3-2L-DCBUSINTERFACEFAULT': [121], 'WRONGRELAYOUTPUT': [133, 134, 136, 141],
               'P-ACE5-1FAULT': [54, 56, 73, 77, 78, 81, 82, 83, 86, 87, 91, 124, 126],
               'P-ACE2-2FAULT': [54, 56, 77, 78, 81, 82, 83, 85, 86, 87, 115, 116],
               'P-ACE6-1L-DCESSBUSINTERFACEFAULT': [129], 'NIC1FAULT': [51, 52], 'HYD1：SYSTEM1PRESSURETRANSDUCER': [33],
               'PACE2：P-ACE2-2FSECU2INTERFACEFAULT': [68, 69], 'P-ACE4-1R-DCESSBUSINTERFACEFAULT': [122],
               'DCU1：NOOUTPUT': [36], 'TW:TAWSFAULTREPORTED': [46], 'P-ACE5-1FSECU2INTERFACEFAULT': [73],
               'P-ACE6-2FCBATTBUSINTERFACEFAULT': [132], 'OILLEVEL/TEMPSENSOR:LENGOILTEMPSENSOROUTOFRANGE': [36, 37],
               'FSECU2：NOFSECUDATATODCU': [37], 'LENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [36],
               'FCM1BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
                              104, 105], 'P-ACE6-2MIDRUDPCUEXCINTERFACEFAULT': [135, 136, 137],
               'DCPUMP:DCFUELSTARTPUMP/PRSW/WRG/DCPUMPRLYFAULT': [36], 'APM2NIC2INTERFACEFAULT': [51, 52],
               'P-ACE2-1FAULT': [53, 54, 55, 56, 77, 78, 81, 82, 83, 84, 86, 87, 112, 114],
               'P-ACE1-2FCBATTBUSINTERFACEFAULT': [111], 'GIOM2R-AHC-4INTERFACEFAULT': [12, 13, 14, 48, 52],
               'ADC2：NOOUTPUT': [6], 'P-ACE5-1FSECU1INTERFACEFAULT': [73], 'APM1FAULT': [52],
               'P-ACE5-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92], 'HYD2SOVFAIL': [37],
               'HSACE2FAULT': [98, 99, 100], 'FCM1：CANBUS1BFAULT': [54],
               'GIOM2A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 51, 78, 86, 87, 96],
               'P-ACE3-1FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 88, 117, 119],
               'FSECU2：SLATBIOC6INPUTNOTPRESENT': [42, 44], 'P-ACE2-1R-DCESSBUSINTERFACEFAULT': [112],
               'P-ACE3-2FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 89, 120, 121],
               'P-ACE6-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94], 'IRS2：NOOUTPUT': [14],
               'FCM1ABCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
               'PACE1：P-ACE1-1FSECU1INTERFACEFAULT': [65], 'FCM1：CANBUS1AFAULT': [53], 'HS-ACE1FAULT': [53, 56],
               'GIOM1L-AHC-4INTERFACEFAULT': [9, 10, 11, 51], 'P-ACE1-2R-DCESSBUSINTERFACEFAULT': [110],
               'PACE2：P-ACE2-2FSECU1INTERFACEFAULT': [68, 69],
               'GIOM1FAULT': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 30, 36, 37, 38, 40, 41, 47, 51, 52, 77, 78, 81,
                              82, 83, 86, 87, 96], 'PACE3：P-ACE3-2FAULT': [71],
               'P-ACE2-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87]}


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
                # edge_detection(img_path)
                run()

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
            if os.path.exists(img_path):
                os.remove(img_path)
            return JsonResponse(res_all, json_dumps_params={"ensure_ascii": False})
        else:
            return HttpResponse('上传失败')


# maintenance messages 2
# fault report path    4
# fault report         5
# 排故提示               8
def rte_data(no, col):
    work_dir = os.path.dirname(os.path.abspath(__file__))
    pth = os.path.join(work_dir, 'data.xls')
    book = xlrd.open_workbook(pth)
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
    A = set()
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
        ans["hit"] = hit
        print(ans)
        return ans


@csrf_exempt
def CMS_confirm(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cms = data.get('res_all')
        print(data)
        print(type(data))
        print(cms)
        print(type(cms))
        cms_list = []
        for i in range(0, len(cms)):
            cms_list.extend(cms[i]["res"])
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
    print(1)
    if request.method == "POST":
        print("POST")
        imageSrc = request.FILES.getlist('image')
        print(imageSrc)
        if imageSrc:
            for k in range(0, len(imageSrc)):
                image = imageSrc[k]
                with open("static/image/FR/" + image.name, 'wb') as f:
                    for c in image.chunks():
                        f.write(c)
                img_path = "static/image/FR/" + image.name
                print(img_path)
                # edge_detection(img_path)
                run(source="static/image/FR")

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
                print(res_all)
                if os.path.exists(img_path):
                    os.remove(img_path)
                return JsonResponse(res_all, json_dumps_params={"ensure_ascii": False})
            else:
                return HttpResponse('上传失败')


def FR_resolove(fr_res):
    res = []
    for item in fr_res:
        tmp=[]

        if len(item['res'][0]) == 2:
            for i in range(1, len(item['res'])):
                tmp.append(item['res'][i][0] + '=' + item['res'][i][1])

            # print(tmp)
            assert "frp" in item.keys(), "frp"
            res.append([tmp, item['frp']])
        elif len(item['res'][0]) == 3:
            for i in range(1, len(item['res'])):
                # print(item['res'][i][0])
                ss1 = item['res'][i][0] + '=' + item['res'][i][1] + "(" + item['res'][0][1] + ")"

                tmp.append(ss1)
                ss2 = item['res'][i][0] + '=' + item['res'][i][2] + "(" + item['res'][0][2] + ")"
                tmp.append(ss2)
            assert "frp" in item.keys(), "frp"
            res.append([tmp, item['frp']])
    return res


def FR_find(fr_list, cms_hit):
    ans=[]
    hit=[]
    for i in range(0, len(fr_list)):
        fr_list[i][1] = fr_list[i][1].replace(' ', "")  # frp
        for j in range(0, len(fr_list[i][0])):
            fr_list[i][0][j] = fr_list[i][0][j].replace(' ', '')  #fr
            fr_list[i][0][j] = fr_list[i][0][j].replace(':', '')
            fr_list[i][0][j] = fr_list[i][0][j].upper()
    # print(fr_list)
    for h in cms_hit:
        FRP = rte_data([h], 4)
        # print(FRP)
        s=""
        if len(FRP[h])>0:
            s = FRP[h][0]
            s = s.split(",")
            # print(s)
        tmp=[]
        for i in range(0, len(fr_list)):
            for j in range(0, len(s)):
                # print(fr_list[i][1])
                if fr_list[i][1] in s[j]:
                    tmp.extend(fr_list[i][0])
        print(h, tmp)
        res=rte_data([h], 5)
        print(h, res)
        if set(res[h])<=set(tmp):
            hit.append(h)

    hit=list(hit)
    print(hit)
    ans=rte_data(hit, 8)
    print(ans)
    return ans



def FR_confirm(request):
    if request.method == "POST":
        print(1)
        data = json.loads(request.body)
        # fr = data.get('res_all')
        print(data)
        print(type(data))
        # print(fr)
        # print(type(fr))
        fr_list = FR_resolove(data["res_all"]["fr_res"])
        print(fr_list)
        ans = FR_find(fr_list, data["res_all"]["hit"])
        return JsonResponse(ans, json_dumps_params={"ensure_ascii": False})
    else:
        return HttpResponse('上传失败')
