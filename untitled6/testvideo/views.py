# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.shortcuts import render

# Create your views here.
from django.templatetags.static import register

from django.utils.safestring import mark_safe

from testvideo import models


@register.simple_tag
def action_all(current_url, index):
    """
    获取当前url，video-1-1-2.html
    :param current_url:
    :param item:
    :return:
    """
    url_part_list = current_url.split('-')
    if index == 3:
        if url_part_list[index] == "0.html":
            temp = "<a href='%s' class='active'>全部</a>"
        else:
            temp = "<a href='%s'>全部</a>"

        url_part_list[index] = "0.html"
    else:
        if url_part_list[index] == "0":
            temp = "<a href='%s' class='active'>全部</a>"
        else:
            temp = "<a href='%s'>全部</a>"

        url_part_list[index] = "0"

    href = '-'.join(url_part_list)

    temp = temp % (href,)
    return mark_safe(temp)


@register.simple_tag
def action(current_url, item, index):
    # videos-0-0-1.html
    # item: id name
    # video-   2   -0-0.html
    url_part_list = current_url.split('-')

    if index == 3:
        if str(item['id']) == url_part_list[3].split('.')[0]:  # 如果当前标签被选中
            temp = "<a href='%s' class='active'>%s</a>"
        else:
            temp = "<a href='%s'>%s</a>"

        url_part_list[index] = str(item['id']) + '.html'  # 拼接对应位置的部分url

    else:
        if str(item['id']) == url_part_list[index]:
            temp = "<a href='%s' class='active'>%s</a>"
        else:
            temp = "<a href='%s'>%s</a>"

        url_part_list[index] = str(item['id'])

    ur_str = '-'.join(url_part_list)  # 拼接整体url
    temp = temp % (ur_str, item['name'])  # 生成对应的a标签
    return mark_safe(temp)  # 返回安全的html


def video(request,*args,**kwargs):
    print(kwargs)
    # 当前请求的路径
    request_path = request.path
    # 从数据库获取视频时的filter条件字典
    q = {}
    # 状态为审核通过的
    q['status'] = 1
    # 获取url中的视频分类id
    class_id = int(kwargs.get('classification_id'))
    # 从数据库中获取所有的视频方向（包括视频方向的id和name）
    direction_list = models.Direction.objects.all().values('id','name')

    # 如果视频方向是0
    if kwargs.get('direction_id') == '0':
        # 方向选择全部
        # 方向id=0，即获取所有的视频分类（包括视频分类的id和name）
        class_list = models.Classification.objects.all().values('id', 'name')
        # 如果视频分类id也为0，即全部分类，那就什么都不用做，因为已经全取出来了
        if kwargs.get('classification_id') == '0':
            pass
        else:
            # 如果视频分类不是全部，过滤条件为视频分类id在[url中的视频分类id]
            q['classification_id__in'] = [class_id,]

    else:
        print('方向不为0')
        # 方向选择某一个方向，
        # 如果分类是0
        if kwargs.get('classification_id') == '0':
            print('分类为0')
            # 获取已选择的视频方向
            obj = models.Direction.objects.get(id=int(kwargs.get('direction_id')))
            # 获取该方向的所有视频分类
            class_list = obj.classification.all().values('id', 'name')
            # 获取所有视频分类对应的视频分类id
            id_list = list(map(lambda x: x['id'], class_list))
            # 过滤条件为视频分类id in [该方向下的所有视频分类id]
            q['classification_id__in'] = id_list
        else:
            # 方向不为0，分类也不为0
            obj = models.Direction.objects.get(id=int(kwargs.get('direction_id')))
            class_list = obj.classification.all().values('id', 'name')
            id_list = list(map(lambda x:x['id'], class_list))
            # 过滤条件为视频分类id in [已经选择的视频分类id]
            q['classification_id__in'] = [class_id,]
            print('分类不为0')
            # 当前分类如果在获取的所有分类中，则方向下的所有相关分类显示
            # 当前分类如果不在获取的所有分类中，
            if int(kwargs.get('classification_id')) in id_list:
                pass
            else:
                print('不再,获取指定方向下的所有分类：选中的回到全部')
                url_part_list = request_path.split('-')
                url_part_list[2] = '0'
                request_path = '-'.join(url_part_list)
    # 视频等级id
    level_id = int(kwargs.get('level_id'))
    if level_id == 0:
        pass
    else:
        # 过滤条件增加视频等级
        q['level'] = level_id

    # 取出相对应的视频
    video_list = models.Video.objects.filter(**q).values('title','summary', 'img', 'href')
    # 把视频等级转化为单个标签是字典格式，整体是列表格式
    ret = map(lambda x:{"id": x[0], 'name': x[1]}, models.Video.level_choice)
    level_list = list(ret)
    return render(request, 'video.html', {'direction_list': direction_list,
                                          'class_list': class_list,
                                          'level_list': level_list,
                                          'current_url': request_path,
                                          "video_list": video_list})