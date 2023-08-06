import requests
import time
from random import randint
from YXKJapi import UpAndDown

# 上传单个文件(fileType:文件类型，siteType:卫星类型，algorithm:算法，path:本地待上传文件绝对路径)-->请求的url
def uploadFile(fileType, siteType, algorithm, path):
    mainURL = "http://172.25.17.120:8080/api/v1/upload/"
    urlParam = f"{fileType}/{siteType}/{algorithm}/"
    files = {
        "file": open(path, "rb"),
        "Content-Disposition": "form-data",
    }
    r = requests.post(mainURL+urlParam, files=files)

    return mainURL + urlParam

# 上传多个文件(fileType:文件类型，siteType:卫星类型，algorithm:算法，li:本地待上传文件绝对路径列表)-->请求的url
def uploadAll(fileType, siteType, algorithm,li):
    urlParam = f"{fileType}/{siteType}/{algorithm}/"
    for path in li:
        uploadFile(fileType, siteType, algorithm, path)

# 发送待下载文件列表(fileList:文件绝对路径列表)-->待下载zip文件文件名
def sendList(fileList):
    url = "http://172.25.17.120:8080/api/v1/downloads/"
    res = time.time()
    zipName = str(res) + ".zip"
    filesDict = dict()
    filesDict["fileList"] = fileList
    filesDict["fileName"] = zipName
    filesDict["Content-Type"] = "application/x-www-form-urlencoded"
    r = requests.post(url, data=filesDict)
    return zipName

# 构建多jpg文件绝对路径列表(fileType:文件类型，siteType:卫星类型，algorithm:算法，fileNameList:文件名列表)-->绝对路径列表
def buildPath(fileType, siteType, algorithm,fileNameList):
    fileAbsList = list()
    for fileName in fileNameList:
         fileAbsList.append(f"F:\\QNAP\\{fileType}\\{siteType}\\{algorithm}\\{fileName}")
    return fileAbsList

# 下载文件(fileType:文件类型，siteType:卫星类型，algorithm:算法，fileName:待下载文件名，savePath:指定本地保存路径)-->请求的url
def donwloadFile(fileType, siteType, algorithm, fileName, savePath):
    mainURL = "http://172.25.17.120:8080/api/v1/download/"
    urlParam = f"{fileType}/{siteType}/{algorithm}/{fileName}"
    r = requests.get(mainURL+urlParam)
    f = open(savePath+urlParam.split("/")[-1], "wb")
    f.write(r.content)
    return mainURL + urlParam

# 获取下载文件对应的url(fileType:文件类型，siteType:卫星类型，algorithm:算法，fileName:待下载文件名)-->请求url
def donwloadFilepath( fileType, siteType, algorithm, fileName):  # 卫星类型、算法、文件名
    mainURL = "http://172.25.17.120:8080/api/v1/download/"
    urlParam = f"{fileType}/{siteType}/{algorithm}/{fileName}"
    url = mainURL + urlParam
    return url

# 仅通过文件名下载文件(fileName:需要下载的文件名，savePath:保存路径)
def downloadByName(fileName,savePath):
    mainURL = "http://172.25.17.120:8080/api/v1/download/"
    r = requests.get(mainURL+fileName)
    f = open(savePath+fileName, "wb")
    f.write(r.content)
    f.close()
    return mainURL+fileName


# if __name__ == "__main__":
#     # uploadFile("shp","GF2","算法1",r"E:\素材\壁纸精选\1.shp")
#     # donwloadFile('GF1','算法1','GF1_WFV1_E86.3_N31.3_20210523_L1A0005667743.zip',"E:/")
#     # temp = sendList(['F:\\QNAP\\img\\GF1\\warter_extraction\\GF1_WFV1_E86.3_N31.3_20210523_L1A0005667743.jpg',
#     #          'F:\\QNAP\\img\\GF1\\warter_extraction\\GF1_WFV2_E85.7_N32.6_20210503_L1A0005629324.jpg'])
#     # print(f"文件名：{temp}")
#     downloadByName("145006.zip","E:\\test\\")
