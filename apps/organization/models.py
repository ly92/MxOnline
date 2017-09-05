from django.db import models
from datetime import datetime

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name="城市名")
    desc = models.CharField(max_length=200, verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="姓名")
    desc = models.TextField(verbose_name="描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击次数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数量")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name="封面图片", max_length=100)
    address = models.CharField(max_length=150, verbose_name="地址")
    city = models.ForeignKey(CityDict, verbose_name="城市")

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name="姓名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数量")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name