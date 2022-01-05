import requests
import os
from lxml import etree
print("downloading with requests")
noaa_url = 'https://www.ncei.noaa.gov/data/ocean-near-surface-atmospheric-properties/access/'
# 定义请求头部信息
headers = {'User-Agent': 'M'}
# 发送请求
resp= requests.get(noaa_url,headers=headers)
noaa_resp_text = resp.text
# 根据返回的text创建etree对象才能使用xpath分析
noaa_etree_element = etree.HTML(noaa_resp_text)
noaa_url_xpath = noaa_etree_element.xpath('//*/table/tr/td/a')
# for i in noaa_url_xpath:
#     print(i.xpath('@href'))
    
for noaa in noaa_url_xpath[2:]:
    file = noaa.xpath('@href')[0]
    noaa_nc_url = noaa_url + noaa.xpath('@href')[0]
    #     print(noaa_nc_url)
    # 定义请求头部信息
    headers = {'User-Agent': 'M'}
    # 发送请求
    resp= requests.get(noaa_nc_url,headers=headers)
    noaa_nc_resp_text = resp.text
    # 根据返回的text创建etree对象才能使用xpath分析
    noaa_nc_etree_element = etree.HTML(noaa_nc_resp_text)
    noaa_nc_url_xpath = noaa_nc_etree_element.xpath('//*/table/tr/td/a')
    # for i in tar_gz_url_xpath:
    #     print(i.xpath('@href'))
    for noaa_nc in noaa_nc_url_xpath[1:]:
        # 打印要下载的文件名
        # print(tar_gz.xpath('@href')[0])
        requests_url = noaa_nc_url + noaa_nc.xpath('@href')[0]
        file_name = noaa_nc.xpath('@href')[0]
        # 打印拼接以后的下载链接
        # print(requests_url)
        # 通过下载链接创建对象r
        r = requests.get(requests_url)
        # 如果当前文件夹没有目录则创建该目录
        if file not in [x for x in os.listdir('.') if os.path.isdir(x)]:
            try:
                os.mkdir(file)
            except:
                print('创建文件夹失败')
        # 如果在目录tar_gz下已经有文件了则不重复下载,否则下载
        if file_name in [x for x in os.listdir(file)]:
            print('%s文件已下载'%(file_name))
        else:
            # 通过拼接的下载url下载文件,下载文件存储在目录下
            with open(f'file/{file_name}', "wb") as code:
                code.write(r.content)
                print('下载文件%s成功'%(file_name))