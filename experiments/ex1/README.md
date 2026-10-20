# 实验1 Web服务器搭建与HTTP协议分析

姓名：易治行；学号：2023141220023；班级：102班。

## 报告与材料

- `实验1报告_易治行_2023141220023.docx`：完整实验报告，含14道必答题、8幅本机实际截图、配置说明、排障、资料来源及小结。
- `site/index.html`：自建首页。
- `apache/httpd.conf`：本次实际启用的独立配置。
- `evidence/wireshark-browser.pcapng`：Wireshark自带dumpcap正式捕获，39个分组。
- `evidence/final-http-details.txt`、`final-http.json`、`final-http-summary.tsv`：正式抓包的TShark解析。
- `evidence/final-actions.json`、`final-actions-cli.txt`、`final-second-visit-cache.txt`：浏览器实际执行记录及第二次导航计时。
- `evidence/01-apache-browser.png`至`08-apache-config.png`：报告使用的截图。

## 已运行的 Apache

- 版本：macOS自带 `/usr/sbin/httpd`，Apache 2.4.66。
- 网站根目录：本目录下 `site/`；默认首页：`index.html`。
- 监听：`127.0.0.1:8080`；访问：http://127.0.0.1:8080/ 。
- 管理：`bash scripts/server.sh start|stop|restart|check|status`。
- 当前账户运行，不修改系统Apache配置；只监听本机。
- 响应正文已与 `site/index.html` 逐字节核对一致。

## 正式抓包结果

日期：2026-10-19，Asia/Shanghai。
使用全新的临时Chromium会话；通过 `--no-proxy-server` 仅为本实验会话直连，未修改系统代理。
正式捕获使用Wireshark dumpcap 4.6.9，接口en0，捕获过滤器 `host gaia.cs.umass.edu and tcp port 80`。Wireshark 4.4.14用于稳定显示截图，TShark 4.6.9用于解析。

| 操作 | 本地时间 | 请求帧 | 响应帧 | 实际结果 |
| --- | --- | --- | --- | --- |
| 访问file1 | 22:11:04.990开始 | 5 | 9 | 200 OK，正文128字节 |
| 首次访问file2 | 22:11:05.822开始 | 11 | 13 | 200 OK，正文371字节 |
| 再次打开同一file2 URL | 22:11:06.150开始 | 无新目标HTTP请求 | 无新目标HTTP响应 | transferSize=0，encodedBodySize=371 |
| 补充普通刷新file2 | 22:11:06.459开始 | 25 | 28 | 两个条件首部，304 Not Modified，无正文 |

上表时间为浏览器操作开始时间，具体报文时间以pcapng为准。
第二次访问和补充刷新是两个不同操作；不能把刷新的304写成第二次普通访问的结果。
客户端 `10.132.215.185:62842`，服务器 `128.119.245.12:80`。`tcp.stream == 0` 中还包含第21帧favicon GET及第23帧301响应，可与页面GET共同证明连接复用。

Wireshark显示过滤器：

- 基本请求响应：`frame.number in {5,9}`
- 缓存实验：`frame.number in {11,13,25,28}`
- 连接复用：`tcp.stream == 0 && http`

## 预实验记录

`browser-http.pcap`、`http-analysis.pcapng`、`http-analysis.pcap`、`http-details.txt`等不带final前缀的旧抓包解析，以及 `preflight/` 中截图，为使用tcpdump完成的预实验。它们的客户端端口和帧号不同，未用于最终报告，也未放入提交材料压缩包。
`browser-http.pcap`扩展名为pcap，但文件实际格式是pcapng，来自macOS tcpdump默认格式。

## 重现与生成

- `scripts/capture-wireshark.sh`：管理员运行的120秒定向捕获脚本；使用 `-g` 使输出文件的组可读。若文件已存在则拒绝覆盖。
- `scripts/capture-http.sh`：预实验tcpdump捕获脚本。
- `scripts/browser-final.config.json`：独立浏览器启动配置。
- `scripts/analyze_capture.py`：解析本次正式捕获并验证状态、正文长度、缓存观察及连接复用，生成 `report-data.json`。
- `scripts/build_report.py`：由真实解析数据生成报告；依赖python-docx。

报告生成和渲染使用Codex bundled Python及LibreOffice。渲染时显式使用bundled `Resources/fontconfig/fonts.conf`，否则中文字体可能缺失。最终DOCX已逐页检查。

## 官方资料

- Apache DocumentRoot：https://httpd.apache.org/docs/2.4/mod/core.html#documentroot
- Apache DirectoryIndex：https://httpd.apache.org/docs/2.4/mod/mod_dir.html#directoryindex
- HTTP语义与条件请求：https://httpwg.org/specs/rfc9110.html
- HTTP缓存：https://httpwg.org/specs/rfc9111.html
- Wireshark用户指南：https://www.wireshark.org/docs/wsug_html_chunked/

具体字段、IP、端口和状态码以本次正式捕获为准。
