# 实验2 DNS服务器配置与DNS协议分析

易治行，2023141220023，计算机科学与技术，102班。实验日期2026-10-20。

## 提交文件

- PDF：output/pdf/2023141220023_易治行_实验2_报告.pdf
- Word：2023141220023_易治行_实验2_报告.docx
- 工程：2023141220023_易治行_实验2.pkt
- 正式原始抓包：evidence/final/2023141220023_易治行_实验2_DNS.pcapng
- 完整包：2023141220023_易治行_实验2_提交材料.zip

报告按原四川大学模板制作，17页，10道分析题，12张实际截图。原模板未修改；课时和教师评议保留空白。

## A 仿真结果

Cisco Packet Tracer 9.0.1.0858，1台PC-PT、2台Server-PT、1台Switch-PT，三条直通铜缆。设备按学号命名。
PC 192.168.1.155/24，HOST 192.168.1.200/24，DNS初始192.168.1.199/24。
A：www.yizhixing.com →192.168.1.200；CNAME：www1.2023141220023.com →www.yizhixing.com。
初始三个ping均4发4收。DNS改.198、PC保留旧解析器.199后，IP ping成功，主域名和别名均找不到主机。修正PC解析器为.198后三项均4发4收。
最终工程保存为DNS服务器.198、PC解析器.198的恢复配置。刚连线的预热ping曾1次超时，另存pt-ip-warmup.jpg，正式重测为4发4收。
Simulation真实响应经内置脚本接口读取：主域名1条A；别名1条CNAME加1条A，均TTL86400秒。FrameInstance是仿真内部索引，不能与Wireshark帧号混用。
临时lab2.js已从工程删除，辅助代码保留于scripts，最终工程无需自动执行辅助脚本。

## B 正式捕获

macOS26.5.1、en0、客户端10.135.128.230。Wireshark dumpcap4.6.9捕获，TShark4.6.9解析，Wireshark4.4.14截图。正式文件51个分组、7164字节。所有真实帧号均对应final目录的正式文件。截图的英文名final-dns.pcapng副本与原文件SHA256相同。

|用途|查询/响应帧|事务ID|DNS端点|
|---|---|---|---|
|百度首次ping|5/6|0x12c7|223.5.5.5|
|川大首次ping|25/26|0xf1c5|223.5.5.5|
|百度A|36/37|0x9d7c|202.115.39.9|
|百度CNAME|38/39|0x4552|202.115.39.9|
|川大A|40/41|0x0ce6|202.115.39.9|
|川大CNAME|50/51|0x3a1c|202.115.39.9|

百度首次和重复ping均3发3收；川大解析到202.115.47.167，但两次均3发0收。解析结果与ICMP连通性分开分析。重复ping未产生新的目标DNS查询，支持本机缓存复用；缓存枚举返回Unable to get details from the cache node，不编造缓存表。
第51帧为NOERROR、Answer=0并带SOA，表示没有CNAME数据，不是NXDOMAIN。第41帧附加区域的名称服务器A地址不计作目标答案。
系统配置显示校园DNS，但ping实际报文端点为223.5.5.5；四次nslookup显式指定同一校园解析器202.115.39.9。

## 证据与复核

命令、起止时间、返回码与输出在evidence/final/real-actions.json及同目录txt；报文全文和结构化分析在evidence/final-analysis/；实际截图为evidence/pt-*.jpg、ws-*.jpg。
首轮过滤漏掉ping实际端点、全部接口补抓缺查询，两轮仅保留作排障记录，不用于报告帧号，提交包仅包含最终正式抓包。
复跑抓包使用scripts/capture-final-dns.sh（需本人sudo），解析使用EX2_FINAL=1配合scripts/analyze-real-dns.py。已取得证据，无需重新抓包；如复跑先另存原文件。脚本不改系统DNS设置。
辅助pt-setup.js、pt-configure.js仅供空白工程按序复现，最终工程已完成配置，不需重跑。Word生成脚本为scripts/build-report.py。
evidence/submission-sha256.json记录提交包成员的SHA256，打包后逐项核验；同时检查DOCX/ZIP完整性及PDF全部页面。
