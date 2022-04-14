from django.db import models

# Create your models here.
class FI(models.Model):  # 故障隔离数据库
    no = models.IntegerField(verbose_name=u'序号')
    EICAS = models.TextField(verbose_name=u'EICAS（告警信息，只要出现与飞控相关的告警即进行下一步）')
    MaintenanceMassages = models.TextField(verbose_name=u'Maintenance massages（维修信息，“与”的关系）')
    MaintenanceMode = models.TextField(verbose_name=u'Maintenance mode（维护位维修信息，“与”的关系）')
    FaultReportPath = models.TextField(verbose_name=u'Fault Report Path（路径）')
    FaultReport = models.TextField(verbose_name=u'Fault Report（触发的监控器为1，“与”的关系）')
    diagram = models.TextField(verbose_name=u'简图页')
    diagnosis = models.TextField(verbose_name=u'诊断页参数')
    tips = models.TextField(verbose_name=u'排故提示')
    def __str__(self):
        return str(self.no)
