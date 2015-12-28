# Vulnerable_scan

A Vulnerability Scanning Tools.

根据匹配规则进行弱点扫描。可自行添加匹配规则。


##Usage
```
Usage: [target] or -f [target_file]

Options:
  -h, --help      show this help message and exit
  -f TARGET_FILE  The files path
  -t THREAD_NUM   Number of threads. default = 20
  -o OUTPUT_FILE  Output file name.
  -r RULES        Choice the rule.
```
-r 默认为All。多个类型之间用逗号隔开。

一对多[一个域名对应多种扫描类型] scan.py www.baidu.com -r phpinfo,htaccess

多对一[多个域名对应一种扫描类型] scan.py -f url.txt -r phpinfo

多对多[多个域名对应多种扫描类型] scan.py -f url.txt -r phpinfo,htaccess

###database.json
根据格式可自行添加

id: 编号顺序

type: 漏洞类型

path: 文件路径

text: 验证规则


