<a href='https://github.com/Junwu0615/Parsing-Media-From-JVID'><img alt='GitHub Views' src='https://views.whatilearened.today/views/github/Junwu0615/Parsing-Media-From-JVID.svg'> 
<a href='https://github.com/Junwu0615/Parsing-Media-From-JVID'><img alt='GitHub Clones' src='https://img.shields.io/badge/dynamic/json?color=success&label=Clone&query=count_total&url=https://gist.githubusercontent.com/Junwu0615/95457ff8b4eae84b4e855461cdc34ab4/raw/Parsing-Media-From-JVID_clone.json&logo=github'> </br>
[![](https://img.shields.io/badge/Project-Web_Crawler-blue.svg?style=plastic)](https://github.com/Junwu0615/Parsing-Media-From-JVID) 
[![](https://img.shields.io/badge/Project-Parsing_Media-blue.svg?style=plastic)](https://github.com/Junwu0615/Parsing-Media-From-JVID) 
[![](https://img.shields.io/badge/Language-Python_3.12.0-blue.svg?style=plastic)](https://www.python.org/) </br>
[![](https://img.shields.io/badge/Package-BeautifulSoup_4.12.2-green.svg?style=plastic)](https://pypi.org/project/beautifulsoup4/) 
[![](https://img.shields.io/badge/Package-Requests_2.31.0-green.svg?style=plastic)](https://pypi.org/project/requests/) 
[![](https://img.shields.io/badge/Package-pycryptodome_3.21.0-green.svg?style=plastic)](https://pypi.org/project/pandas/) 
[![](https://img.shields.io/badge/Package-ArgumentParser_1.2.1-green.svg?style=plastic)](https://pypi.org/project/argumentparser/) 

## STEP.1　CLONE
```python
git clone https://github.com/Junwu0615/Parsing-Media-From-JVID.git
```

## STEP.2　INSTALL PACKAGES
```python
pip install -r requirements.txt
```

## STEP.3　RUN
```python
python Entry.py -h
```

## STEP.4　HELP

- `-h` Help : Show this help message and exit.
- `-t` Type : Give a want todo type | ex: image / mp4 `default: image`
- `-u` URL : Give a url of JVID | ex: 'https://www.jvid.com/v/[PAGE_ID]' `default: ''`
- `-p` Path : Give a save path | ex: './media/' `default: media`

## STEP.5　EXAMPLE

### I　執行前須注意事項
- 環境可能需要安裝 [FFmpeg](https://www.ffmpeg.org/download.html) 解包套件，請參考頁尾文章
- 現階段非同步的下載作業有`卡死問題`，因此選擇 `一般執行 [2]` 就好

  - ![00.jpg](/sample/00.jpg) 
  
- 將 package `permissions_.txt` -> `permissions.txt` 修改內容。
  ```python
  authorization,[Fill In Your Authorization]
  cookie,[Fill In Your Cookie]
  ```
  
### II-A.　抓取網站影像 (.jpg)
```python
python Entry.py -t img -u https://www.jvid.com/v/**PAGE_ID**
```

### II-B.　抓取網站串流影片 (.m3u8)
```python
python Entry.py -t mp4 -u https://www.jvid.com/v/**PAGE_ID**
```

## 參考來源
- [FFmpeg Windows 安裝教學](https://vocus.cc/article/64701a2cfd897800014daed0)
- [解碼 TS 串流媒體方式](https://cloud.tencent.com/developer/article/2258872)