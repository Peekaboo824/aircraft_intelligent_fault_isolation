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

# new_img = Image(
#     name_cms="",
#     image_cms="",
#     res_cms="",
#     name_fr="",
#     image_fr="",
#     res_fr=""
# )
#


def CMS(request):
    CMS_list = []
    if request.method == "POST":
        imageSrc=request.FILES.getlist('image')
        if imageSrc:
            for i in range(0,len(imageSrc)):
                image=imageSrc[i]
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
                img_path = "static/image/CMS/"+image.name
                print(img_path)
                edge_detection(img_path)

                det_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_det_infer"
                cls_model_dir = "PaddleOCR/inference/ch_ppocr_mobile_v2.0_cls_infer"
                rec_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_rec_infer"
                ocr = Ocr(img_path, det_model_dir, cls_model_dir, rec_model_dir)
                ocr_result = ocr.identify()
                ocr_list = []
                for line1 in ocr_result:
                    if line1[1][0].find("LRU:") != -1 or line1[1][0].find("RU:") != -1 or line1[1][0].find("LRU：") != -1 or \
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

                CMS_list.append([i,ocr_list])
                print(CMS_list)
            return HttpResponse(CMS_list)
        else:
            return HttpResponse('上传失败')

def CMS_confirm(request):
    if request.method == "POST":
        cms=request.POST.get('data')
        return HttpResponse(1)
    else:
        return HttpResponse(0)

# def FR(request):
#     if request.method == "POST":
#         image=request.FILES['image']
#         print(image)
#         if image:
#             # new_img = Image(
#             #     name=image.name,
#             #     image=image,
#             #     res=""
#             # )
#             new_img.name_fr = image.name
#             new_img.image_fr = image
#             new_img.save()
#             img_path = "static/image/FR/"+image.name
#             print(img_path)
#             edge_detection(img_path)
#
#             det_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_det_infer"
#             cls_model_dir = "PaddleOCR/inference/ch_ppocr_mobile_v2.0_cls_infer"
#             rec_model_dir = "PaddleOCR/inference/ch_ppocr_server_v2.0_rec_infer"
#             ocr = Ocr(img_path, det_model_dir, cls_model_dir, rec_model_dir)
#             ocr_result = ocr.identify()
#
#             # for line in ocr_result:
#             #     print(line)
#             # print(len(ocr_result))
#             # print('\n')
#             result = []
#             flag=0
#             # 找表头
#             tmp = []
#             x = 20
#             for i in range(0, len(ocr_result)):
#                 if ("MONITORNAME" in ocr_result[i][1][0] or "MONITORNANE" in ocr_result[i][1][0] or "MONITOR NAME" in
#                         ocr_result[i][1][0] or "NONITOR NANE" in ocr_result[i][1][0] or "MONITOR NANE" in
#                         ocr_result[i][1][0]):
#                     tmp.append((ocr_result[i][0][0], ocr_result[i][0][1], ocr_result[i][1][0]))
#                     x = ocr_result[i][0][0][0]
#
#                     if "ACE" in ocr_result[i - 1][1][0] or "FCM" in ocr_result[i - 1][1][0] or "1A" in \
#                             ocr_result[i - 1][1][0] or "1B" in ocr_result[i - 1][1][0]:
#                         tmp.append(((ocr_result[i - 1][0][0], ocr_result[i - 1][0][1], ocr_result[i - 1][1][0])))
#                     if "ACE" in ocr_result[i - 2][1][0] or "FCM" in ocr_result[i - 2][1][0] or "1A" in \
#                             ocr_result[i - 2][1][0] or "1B" in ocr_result[i - 2][1][0]:
#                         tmp.append(((ocr_result[i - 2][0][0], ocr_result[i - 2][0][1], ocr_result[i - 2][1][0])))
#                     if "ACE" in ocr_result[i + 1][1][0] or "FCM" in ocr_result[i + 1][1][0] or "1A" in \
#                             ocr_result[i + 1][1][0] or "1B" in ocr_result[i + 1][1][0]:
#                         tmp.append(((ocr_result[i + 1][0][0], ocr_result[i + 1][0][1], ocr_result[i + 1][1][0])))
#                     if "ACE" in ocr_result[i + 2][1][0] or "FCM" in ocr_result[i + 2][1][0] or "1A" in \
#                             ocr_result[i + 2][1][0] or "1B" in ocr_result[i + 2][1][0]:
#                         tmp.append(((ocr_result[i + 2][0][0], ocr_result[i + 2][0][1], ocr_result[i + 2][1][0])))
#             tmp.sort()
#             title = []
#             tmp_ = []
#             for i in tmp:
#                 title.append(i)
#             for i in tmp:
#                 # print(i)
#                 tmp_.append(i[2])
#             result.append(tmp_)
#             # print(tmp_)
#
#             if (len(title) == 3):
#                 dis0 = title[0][0][0]
#                 dis1m = title[1][0][0]
#                 dis1M = title[1][1][0]
#                 dis2m = title[2][0][0]
#                 dis2M = title[2][1][0]
#                 tmp0 = []
#                 tmp1 = []
#                 tmp2 = []
#                 for line in ocr_result:
#                     if (dis0 - 15) <= line[0][0][0] <= (dis0 + 15) and line[1][0].find("RETURN") == -1 and line[1][0] != \
#                             tmp[0][2]:
#                         tmp0.append((line[0][0][1], line[1][0]))
#
#                 for line in ocr_result:
#                     if (dis1m - 15) <= line[0][0][0] <= dis1M and len(line[1][0]) == 1 and line[0][0][1] > title[1][0][
#                         1]:
#                         tmp1.append((line[0][0][1], line[1][0]))
#                 for line in ocr_result:
#                     if dis2m - 15 <= line[0][0][0] <= dis2M and len(line[1][0]) == 1 and line[0][0][1] > title[2][0][1]:
#                         tmp2.append((line[0][0][1], line[1][0]))
#                 # print(tmp0)
#                 # print(tmp1)
#                 # print(tmp2)
#                 if (len(tmp0) == len(tmp1) == len(tmp2)):
#                     # flag=1
#                     tmp0.sort()
#                     tmp1.sort()
#                     tmp2.sort()
#
#                     for i in range(0, len(tmp0)):
#                         tmp = []
#                         tmp.append(tmp0[i][1])
#                         tmp.append(tmp1[i][1])
#                         tmp.append(tmp2[i][1])
#                         result.append(tmp)
#                     # for i in range(0, len(result)):
#                     #     print(result[i])
#                 # else:
#                 #     print("wrong")
#                 #     return
#
#             if (len(title) == 2):
#                 dis0 = title[0][0][0]
#                 dis1m = title[1][0][0]
#                 dis1M = title[1][1][0]
#                 tmp0 = []
#                 tmp1 = []
#                 for line in ocr_result:
#                     if (dis0 - 15) <= line[0][0][0] <= (dis0 + 15) and line[1][0].find("RETURN") == -1 and line[1][0] != \
#                             tmp[0][2]:
#                         tmp0.append((line[0][0][1], line[1][0]))
#                 for line in ocr_result:
#                     if (dis1m - 15) <= line[0][0][0] <= dis1M and len(line[1][0]) == 1 and line[0][0][1] > title[1][0][
#                         1]:
#                         tmp1.append((line[0][0][1], line[1][0]))
#                 if (len(tmp0) == len(tmp1)):
#                     # flag=1
#                     tmp0.sort()
#                     tmp1.sort()
#
#                     for i in range(0, len(tmp0)):
#                         tmp = []
#                         tmp.append(tmp0[i][1])
#                         tmp.append(tmp1[i][1])
#
#                         result.append(tmp)
#                     # for i in range(0, len(result)):
#                     #     print(result[i])
#                 # else:
#                 #     print("wrong")
#                 #     return
#             for i in result:
#                 print(i)
#             new_img.res_fr=result
#             new_img.save()
#             return redirect('test',img=new_img)
#         else:
#             return HttpResponse('上传失败')