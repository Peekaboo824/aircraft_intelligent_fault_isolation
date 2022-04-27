import xlrd
book = xlrd.open_workbook('..\\api\\static\\file\\data.xls')
sheet = book.sheet_by_name('Sheet1')

cms_list=[]
print(sheet.nrows)
for i in range(1, sheet.nrows):
    tmp=sheet.row_values(i)[2].split('\n')
    for i in tmp:
        i=i.replace("\r","")
        i=i.replace(' ',"")
        if i!="":
            cms_list.append(i)
cms_set=set(cms_list)
cms_dataset={}
for i in cms_set:
    cms_dataset[i]=[]
for key in cms_dataset.keys():
    for i in range(1, sheet.nrows):
        tmp=sheet.row_values(i)[2].split('\n')
        for j in range(0,len(tmp)):
            tmp[j]=tmp[j].replace("\r","")
            tmp[j] = tmp[j].replace(' ', "")
        if key in tmp:
            cms_dataset[key].append(i)

for key,value in cms_dataset.items():
    print(key)
    print(value)
print(cms_dataset)
print(len(cms_dataset))
print(cms_dataset['P-ACE3-2UPRUDPCUEHSVLVDTINTERFACEFAULT'])

# cms_dataset = {'PACE1：P-ACE1-2FSECU2INTERFACEFAULT': [66], 'FSECU2：NOFSECUDATATODCU': [37],
#                'FSECU2：NOFSECUOUTPUTTODCU': [43, 45, 46, 47], 'HS-ACE2FAULT': [54, 55],
#                'FCM2BL-DCBUSINTERFACEFAULT': [107], 'P-ACE1：P-ACE1-2FAULT': [66],
#                'P-ACE3-2FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 89, 120, 121],
#                'APM1NIC1INTERFACEFAULT': [51, 52], 'HCLE:HCLEPARTITION2FAILURE': [37],
#                'P-ACE1-2FCBATTBUSINTERFACEFAULT': [111],
#                'P-ACE1-2PACU1INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
#                'P-ACE2-1R-DCESSBUSINTERFACEFAULT': [112], 'PACE2：P-ACE2-2FSECU1INTERFACEFAULT': [68, 69],
#                'ADC2：NOOUTPUT': [6], 'P-ACE1-1FAULT': [53, 55, 77, 78, 79, 81, 82, 83, 86, 87, 108, 109],
#                'HSACE1FAULT': [96, 97], 'IRS1：NOOUTPUT': [11],
#                'P-ACE4-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90], 'P-ACE1-1R-DCBUSINTERFACEFAULT': [109],
#                'P-ACE6-1R-DCBUSINTERFACEFAULT': [130], 'FCM2：CANBUS2AFAULT': [55], 'HYD2SOVFAIL': [37],
#                'FCM1BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
#                               104, 105],
#                'P-ACE6-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
#                'P-ACE3-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89], 'NIC1：ASCBPRIMARYBUSFAULT': [48, 49],
#                'LPS:OXYPRSW/WRGFAULT': [37], 'P-ACE2-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87],
#                'P-ACE1：P-ACE1-1FAULT': [65], 'FCM2BP-ACU2INTERFACEFAULT': [15, 16],
#                'P-ACE5-1L-DCBUSINTERFACEFAULT': [126],
#                'GIOM1A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 46, 47, 51, 52, 78, 86, 87, 96],
#                'P-ACE4-1FAULT': [53, 55, 72, 77, 78, 81, 82, 83, 86, 87, 90, 122, 123],
#                'GIOM1A-ADC-6INTERFACEFAULT': [52],
#                'P-ACE2-2FAULT': [54, 56, 77, 78, 81, 82, 83, 85, 86, 87, 115, 116],
#                'P-ACE5-2FAULT': [53, 55, 74, 77, 78, 81, 82, 83, 86, 87, 92, 127, 128], 'FCM2：CANBUS2BFAULT': [56],
#                'P-ACE6-2FSECU2INTERFACEFAULT': [76], 'P-ACE6-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94],
#                'FCM1BR-DCBUSINTERFACEFAULT': [105], 'FCM2AR-DCESSBUSINTERFACEFAULT': [106],
#                'P-ACE4-1FCBATTBUSINTERFACEFAULT': [123],
#                'P-ACE3-2R-DCESSBUSINTERFACEFAULT': [120], 'GIOM1L-AHC-4INTERFACEFAULT': [9, 10, 11, 51],
#                'NIC1：ASCBSECONDARYBUSFAULT': [48, 49], 'FCM1：CANBUS1BFAULT': [54], 'HS-ACE1FAULT': [53, 56],
#                'FCM1APACU1INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87], 'IRS2：NOOUTPUT': [14],
#                'P-ACE5-1FSECU2INTERFACEFAULT': [73], 'P-ACE5-2FSECU2INTERFACEFAULT': [74],
#                'APUSOV:APUCONTROLRELAY/WRGFAULT': [36, 37],
#                'FSECU2：SLATBIOC6INPUTNOTPRESENT': [42, 44], 'P-ACE4-1FSECU2INTERFACEFAULT': [72],
#                'PACE3：P-ACE3-1FAULT': [70],
#                'HSACE2/WRG[STICKSHAKER]FAULT': [98, 99, 100], 'ADC1:NOOUTPUT': [3],
#                'GIOM1B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 52],
#                'PACE2：P-ACE2-1FSECU1INTERFACEFAULT': [67],
#                'FCM2BFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
#                'GSCM:GSCMFAULT': [37],
#                'P-ACE3-2L-DCBUSINTERFACEFAULT': [121],
#                'FCM2ABCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
#                'LEFTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52],
#                'P-ACE3-1FAULT': [53, 55, 77, 78, 81, 82, 83, 86, 87, 88, 117, 119],
#                'GSCMFAULT': [15, 16, 29, 36, 51, 52], 'HCLE：HCLEPARTITION1FAILURE': [36],
#                'P-ACE5-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92],
#                'GIOM2B-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 38, 40, 46, 47, 51, 52],
#                'P-ACE5-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91],
#                'P-ACE5-2L-DCESSBUSINTERFACEFAULT': [128],
#                'GIOM2R-AHC-4INTERFACEFAULT': [12, 13, 14, 48, 52], 'FCM2BPACU2INTERFACEFAULT': [30, 36, 37, 51],
#                'P-ACE3-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88], 'HSACE2FAULT': [98, 99, 100],
#                'P-ACE4-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 90], 'APM1FAULT': [52],
#                'PACE3：P-ACE3-2FSECU1INTERFACEFAULT': [71], 'FSECU1：NOFSECUOUTPUTTODCU': [42, 44, 47],
#                'HYD1：SYSTEM1PRESSURETRANSDUCER': [33], 'FUELLEFTPUMP1：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [37],
#                'P-ACE6-1FSECU2INTERFACEFAULT': [75], 'LENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [36],
#                'OILLEVEL/TEMPSENSOR:LENGOILTEMPSENSOROUTOFRANGE': [36, 37], 'HYD2：SYSTEM2PRESSURETRANSDUCER': [34],
#                'P-ACE1-1PACU1INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87],
#                'P-ACE3-1L-DCESSBUSINTERFACEFAULT': [117],
#                'P-ACE5-1FSECU1INTERFACEFAULT': [73],
#                'FCM1AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 53, 54, 59, 60, 61, 62, 77, 78, 81, 82, 83, 86, 87,
#                               104, 105],
#                'P-ACE6-2FAULT': [54, 56, 76, 77, 78, 81, 82, 83, 86, 87, 94, 132], 'NIC1FAULT': [51, 52],
#                'FCM2APACU1INTERFACEFAULT': [30, 36, 37, 51],
#                'P-ACE6-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 93],
#                'ROLLCONTROLDU：ROLLDISCOUNITFAIL': [36],
#                '/': [7, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 39, 50, 57, 58, 63, 64, 95, 101, 113, 118, 125],
#                'RIGHTGSPCUFAULT': [15, 16, 29, 36, 37, 51, 52], 'FCM2AP-ACU1INTERFACEFAULT': [15, 16],
#                'FCM1BP-ACU2INTERFACEFAULT': [15, 16],
#                'PACE3：P-ACE3-1FSECU1INTERFACEFAULT': [70], 'P-ACE6-1FSECU1INTERFACEFAULT': [75],
#                'FCM1AP-ACU1INTERFACEFAULT': [15, 16],
#                'P-ACE6-2FSECU1INTERFACEFAULT': [76], 'HSACE1/WRG[STICKSHAKER]FAULT': [96, 97],
#                'PACE1：P-ACE1-1FSECU1INTERFACEFAULT': [65],
#                'NICAPM2：APM2FAULT': [51], 'FSECU1：SLATBIOC6INPUTNOTPRESENT': [43, 45, 46],
#                'P-ACE1-1PACU2INTERFACEFAULT': [77, 78, 79, 81, 82, 83, 86, 87],
#                'P-ACE2-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87],
#                'GIOM2R-DCU-9INTERFACEFAULT': [16, 29, 30, 36, 37, 51, 52],
#                'FCM1ABCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
#                'TW:TAWSFAULTREPORTED': [46], 'PACE2：P-ACE2-2FSECU2INTERFACEFAULT': [68, 69],
#                'GIOM2R-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51, 52], 'P-ACE6-2FCBATTBUSINTERFACEFAULT': [132],
#                'P-ACE6-2PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 94], 'RENGSOV:ENGLEFTSOV/WRG/DCUFAULT': [37],
#                'P-ACE2-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 85, 86, 87], 'P-ACE4-1FEECU1INTERFACEFAULT': [72],
#                'FCM1AL-DCESSBUSINTERFACEFAULT': [104], 'P-ACE1-1L-DCESSBUSINTERFACEFAULT': [108],
#                'GIOM1L-ADC-6INTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 51],
#                'FUELRIGHTPUMP1：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [36],
#                'PACE1：P-ACE1-1FSECU2INTERFACEFAULT': [65], 'PACE2：P-ACE2-1FSECU2INTERFACEFAULT': [67],
#                'P-ACE3-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 88], 'PACE3：P-ACE3-2FAULT': [71],
#                'PITCHCONTROLDU：PITCHDISCOUNITFAIL': [37], 'DCPUMP:DCFUELSTARTPUMP/PRSW/WRG/DCPUMPRLYFAULT': [36],
#                'DCU2：NOOUTPUT': [37], 'APM2NIC2INTERFACEFAULT': [51, 52],
#                'P-ACE1-2PACU2INTERFACEFAULT': [77, 78, 80, 81, 82, 83, 86, 87],
#                'PACE1：P-ACE1-2FSECU1INTERFACEFAULT': [66],
#                'P-ACE5-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 92],
#                'PACE3：P-ACE3-2FSECU2INTERFACEFAULT': [71],
#                'P-ACE5-1PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 91],
#                'FCM1BBCU2INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 52, 59, 60, 61, 62],
#                'P-ACE4-1R-DCESSBUSINTERFACEFAULT': [122],
#                'P-ACE5-1FAULT': [54, 56, 73, 77, 78, 81, 82, 83, 86, 87, 91, 124, 126],
#                'GIOM1L-DCU-9INTERFACEFAULT': [15, 29, 30, 36, 37, 51, 52, 77, 78, 81, 82, 83, 86, 87],
#                'FCM1：CANBUS1AFAULT': [53], 'GIOM2A-IOC-3DINTERFACEFAULT': [1, 2, 3, 4, 5, 6, 8, 41, 51, 78, 86, 87, 96],
#                'P-ACE5-2R-DCBUSINTERFACEFAULT': [127], 'P-ACE1-2R-DCESSBUSINTERFACEFAULT': [110],
#                'HYD2：HYD2SOVFAIL': [36], 'P-ACE2-2L-DCESSBUSINTERFACEFAULT': [115],
#                'P-ACE5-1R-DCESSBUSINTERFACEFAULT': [124], 'P-ACE2：P-ACE2-1FAULT': [67],
#                'P-ACE2-1PACU2INTERFACEFAULT': [77, 78, 81, 82, 83, 84, 86, 87],
#                'PACE3：P-ACE3-1FSECU2INTERFACEFAULT': [70], 'GIOM1L-DCUINTERFACEFAULT': [16],
#                'P-ACE3-2PACU1INTERFACEFAULT': [77, 78, 81, 82, 83, 86, 87, 89], 'APM2FAULT': [52],
#                'GIOM2R-DCUINTERFACEFAULT': [15], 'DCU1：NOOUTPUT': [36],
#                'P-ACE2-1FAULT': [53, 54, 55, 56, 77, 78, 81, 82, 83, 84, 86, 87, 112, 114],
#                'FUELXFEEDSOV:XFEEDSOV/WRG/DCUFAULT': [37], 'P-ACE2-1L-DCBUSINTERFACEFAULT': [114],
#                'P-ACE6-1FAULT': [54, 56, 75, 77, 78, 81, 82, 83, 86, 87, 93, 129, 130],
#                'P-ACE1-2FAULT': [54, 56, 77, 78, 80, 81, 82, 83, 86, 87, 110, 111], 'FSECU1：NOFSECUDATATODCU': [36],
#                'GIOM1FAULT': [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 15, 16, 30, 36, 37, 38, 40, 41, 47, 51, 52, 77, 78, 81,
#                               82, 83, 86, 87, 96], 'P-ACE6-2R-DCESSBUSINTERFACEFAULT': [131],
#                'P-ACE2：P-ACE2-2FAULT': [68, 69],
#                'GIOM2FAULT': [1, 2, 3, 4, 5, 6, 8, 12, 13, 14, 15, 16, 30, 36, 37, 38, 40, 41, 47, 48, 51, 52, 78, 86,
#                               87, 96], 'HYD1：HYD1SOVFAIL': [36], 'FUELLEFTPUMP2：FUELLEFTPUMP2/PRSW/WRG/RLYFAULT': [36],
#                'P-ACE6-1L-DCESSBUSINTERFACEFAULT': [129], 'NICAPM1：APM1FAULT': [51],
#                'FCM2AFAULT': [15, 16, 30, 31, 32, 36, 37, 51, 52, 55, 56, 59, 60, 61, 62, 106, 107],
#                'FCM1BPACU2INTERFACEFAULT': [30, 36, 37, 52, 77, 78, 81, 82, 83, 86, 87],
#                'P-ACE5-2FSECU1INTERFACEFAULT': [74], 'HYD3：SYSTEM3PRESSURETRANSDUCER': [35, 36],
#                'P-ACE2-2FCBATTBUSINTERFACEFAULT': [116],
#                'FCM2BBCU1INTERFACEFAULT': [15, 16, 31, 32, 36, 37, 51, 59, 60, 61, 62],
#                'FUELRIGHTPUMP2：FUELRIGHTPUMP1/PRSW/WRG/RLYFAULT': [37], 'P-ACE3-1FCBATTBUSINTERFACEFAULT': [119],
#                'ADC2：NOR-ADC-6BUSOUTPUT': [4]}
#
# def check_mm(ll):
#     for i in range(0, len(ll)):
#         ll[i] = ll[i].replace(' ', '')
#         ll[i] = ll[i].upper()
#     A = set(cms_dataset[ll[0]])
#     for item in ll:
#         # print(set(cms_dataset[item]))
#         A = A & set(cms_dataset[item])
#     print(A)
#
#     return A
#
# test = ['GIOM1 FAULT', 'GIOM2 FAULT', 'GIOM1 A-IOC-3D INTERFACE FAULT', 'GIOM1 B-IOC-3D INTERFACE FAULT',
#         'GIOM1 L-ADC-6 INTERFACE FAULT', 'GIOM2 A-IOC-3D INTERFACE FAULT', 'GIOM2 B-IOC-3D INTERFACE FAULT',
#         'GIOM2 R-ADC-6 INTERFACE FAULT',
#         'ADC2：NOR-ADC-6BUSOUTPUT','P-ACE3-1FCBATTBUSINTERFACEFAULT']
# check_mm(test)