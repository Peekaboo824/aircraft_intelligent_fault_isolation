# 将excel表格导入到数据库中
import xlrd
import models
book = xlrd.open_workbook('../static/file/data.xls')

# no = models.IntegerField(verbose_name=u'序号')
# EICAS = models.TextField(verbose_name=u'EICAS（告警信息，只要出现与飞控相关的告警即进行下一步）')
# MaintenanceMassages = models.TextField(verbose_name=u'Maintenance massages（维修信息，“与”的关系）')
# MaintenanceMode = models.TextField(verbose_name=u'Maintenance mode（维护位维修信息，“与”的关系）')
# FaultReportPath = models.TextField(verbose_name=u'Fault Report Path（路径）')
# FaultReport = models.TextField(verbose_name=u'Fault Report（触发的监控器为1，“与”的关系）')
# diagram = models.TextField(verbose_name=u'简图页')
# diagnosis = models.TextField(verbose_name=u'诊断页参数')
# tips = models.TextField(verbose_name=u'排故提示')

sheet = book.sheet_by_name('Sheet1')
print(sheet)
value_list=[]
for i in range(1, sheet.nrows):
    value_list.append(models.FI(
        no=int(sheet.row_values(i)[0]),
        EICAS=sheet.row_values(i)[1],
        MaintenanceMassages=sheet.row_values(i)[2],
        MaintenanceMode=sheet.row_values(i)[3],
        FaultReportPath=sheet.row_values(i)[4],
        FaultReport=sheet.row_values(i)[5],
        diagram=sheet.row_values(i)[6],
        diagnosis=sheet.row_values(i)[7],
        tips=sheet.row_values(i)[8]
    ))
    # print(sheet.row_values(i))
models.FI.objects.bulk_create(value_list)