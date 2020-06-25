#CloudAcademy Downloader
This python script was built to download videos from Cloud Academy only for personal offline purpose and self-study.

This project was inspired on this repo: https://github.com/josefeg/cloudacademy-dl

## Disclaimer

This tool is meant to be used only if your CloudAcademy account supports
lecture downloads.

## Installation instructions
This script requires Python 3 and a CloudAcademy account.
Tested against Linux, MacOS and Windows OS. 
First clone this repository in any directory and then run the requirements.txt
```
pip install -r requirements.txt
```

## Usage Instructions
```sh
cloud-academy-dl.py <url course> --cookie=file.txt 
```
The **<url course>** must be the full qualifier URL from the course, when you see all video list in the left side of player.
the **--cookie** argument must be a text file with your cookies, for that, you must loggin on cloud academy and then make right click to inspect the website.
In the Network tab look for any request to 'cloudacademy.com' and GET method, copy all **Request Header** and save it into a text file, e.g:

```
:authority: cloudacademy.com
:method: GET
:path: /api/v3/reports/categories/course/
:scheme: https
accept: application/json
accept-encoding: gzip, deflate, br
accept-language: *
authorization: Bearer eyJ
cookie: _gcl_au=
referer: https://cloudacademy.com/
sec-fetch-dest: empty
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36
```
#optional arguments
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


#Referential image of the script

[![Capture.png](https://i.postimg.cc/1RVTZ9hc/cloud-academy-dl.png)](https://postimg.cc/ThGQVvPp)
