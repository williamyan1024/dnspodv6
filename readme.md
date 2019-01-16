# dnspod ipv6 ddns
dnspod 的 IPV6的解析脚本

## 使用

编辑 *.py 文件里的 login_token 和 domains 相关配置

dnspodv6.py 为持续运行,每30秒更新一次

dnspodv6_corntab.py 适用于添加crontab调用


## 如何获取 domain_id
```
curl -X POST https://dnsapi.cn/Domain.List \
     -d 'login_token=xxxxx,xxxxxxxxx& \
     format=json'
```
## 如何获取 record_id
```
curl -X POST https://dnsapi.cn/Record.List \
     -d 'login_token=xxxxx,xxxxxxxxx& \
         format=json& \
         domain_id=上面获取的 domain_id& \
         sub_domain=需要获取id的子域名& \
         record_type=AAAA& \
         offset=0& \
         length=3'
```

