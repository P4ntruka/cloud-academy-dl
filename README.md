# CloudAcademy Downloader
This python script was built to download videos and subtitles from cloudacademy.com only for personal offline purpose and self-study.

## Disclaimer

This tool is meant to be used only if your CloudAcademy account supports
lecture downloads.

## Installation instructions
This script requires Python 3 and a CloudAcademy account.
Tested on Linux, Mac and Windows platform.\
First clone this repository in any directory and then run the requirements.txt
```
$ git clone https://github.com/P4ntruka/cloud-academy-dl.git
Cloning into 'cloud-academy-dl'...

$ cd cloud-academy-dl
$ pip install -r requirements.txt
```

## Usage Instructions
```sh
cloud-academy-dl.py <url course> --cookie=file.txt 
```
The URL must be the full qualifier from the course, when you see all video list in the left side of the video player.  
__`Windows platform user: URL must be in double quotes`__  
__`Linux/Mac platform user: URL must be in single or double quotes`__  

The **--cookie** argument must be a text file with your cookies, for that, you must loggin on cloud academy and then make right click to inspect the website.
In the **Network tab** mark the **XHR** option and look for a request with **'config'** name in the left side of requests, select all **request header**, copy and save it into a text file.

![cookie example](https://user-images.githubusercontent.com/36051334/85949355-42dd9300-b924-11ea-98e9-6f332f197f0d.jpeg)
  
**Mandatory: The Request Header must have the 'authorization' and 'cookie' fields in your text file:**  

__`"You only need generate the request header file once then can be used multiple time to download until your session expired from server."`__

```
:authority: cloudacademy.com
:method: GET
:path: /api/v3/reports/categories/course/
:scheme: https
accept: application/json
accept-encoding: gzip, deflate, br
accept-language: *
authorization: Bearer eyJ..........
cookie: _gcl_au=123abc....
referer: https://cloudacademy.com/
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36
```
# Optional arguments
```
The optional command line arguments for the script are:

--help              Prints out the list of command line arguments.
--res=<resolution>  The required video resolution. Allowed values are 360,
                    720, and 1080. The default value for this argument is
                    1080.
--out=<output_dir>  The directory where the videos are saved. If this command
                    line argument is not specified, then they will be saved in
                    current directory under courses/.
```


# Downloading videos & new features

If error appear while download, you can run again the script to check your downloaded files and if they're not corrupted.\
If any file is corrupted, the script will start downloading again from that point.

![corrupted_file](https://user-images.githubusercontent.com/36051334/85954604-ac6e9900-b946-11ea-8130-fb7a4c693615.png)

__`Icons only available on Mac(oh-my-zsh)`__