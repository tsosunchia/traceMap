import datetime
import os

import folium
from geo import geoInterface


def draw(locationsRawList, output_path, file_name):
    """
    绘制gps轨迹图
    :param locationsRawList: list, 需要绘制轨迹的经纬度信息，格式为[[lat0, lon0, msg0], [lat1, lon1, msg1], ...] (纬度,经度,信息)
    :param output_path: str, 轨迹图保存路径
    :param file_name: str, 轨迹图保存文件名
    :return: None
    """
    locationsList = [[i[0], i[1]] for i in locationsRawList]
    msgList = [i[2] for i in locationsRawList]

    m = folium.Map(locationsList[int(len(locationsList) / 2)], attr='default', zoom_start=4)  # 中心区域的确定

    folium.PolyLine(  # polyline方法为将坐标用实线形式连接起来
        locationsList,  # 将坐标点连接起来
        weight=4,  # 线的大小为4
        color='red',  # 线的颜色为红色
        opacity=0.8,  # 线的透明度
    ).add_to(m)  # 将这条线添加到刚才的区域m内

    # 起始点，结束点
    folium.Marker(locationsList[0], popup=f'<b>Starting Point, {msgList[0]}</b>').add_to(m)
    folium.Marker(locationsList[-1], popup=f'<b>End Point, {msgList[-1]}</b>').add_to(m)

    # 其他点
    for i in range(1, len(locationsList) - 1):
        folium.Marker(locationsList[i], popup=f'<b>Point {i}, {msgList[i]}</b>').add_to(m)

    m.save(os.path.join(output_path, file_name))  # 将结果以HTML形式保存到指定路径


def process(rawData) -> str:
    """
    处理原始数据，获取HTML文件路径
    :param rawData: dict, 原始数据
    :return: str, HTML文件路径
    """
    coordinatesList = geoInterface(rawData)
    filename = str(int(datetime.datetime.now().timestamp())) + '.html'
    draw(coordinatesList, './html', filename)
    return filename
