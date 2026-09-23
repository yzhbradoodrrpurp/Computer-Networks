# 协议分层 (Protocol Layer)

## 为什么需要分层

网络系统非常复杂，里面有：

- 主机和路由器；
- 铜线、光纤、无线等链路；
- 操作系统和网络硬件；
- 应用程序；
- 大量不同协议。

为了控制复杂度，网络采用 **layering（分层）**：把完整通信任务拆成几个层次，每层负责一种功能：

1. 通过自己的内部操作提供某种服务；
2. 依赖下一层提供的服务；
3. 向上一层隐藏内部实现细节。

## 网络协议栈 (Internet protocol stack)

Internet 协议栈从上到下分为五层：

| 层          | 主要任务                     | 常见协议或技术           |
| ----------- | ---------------------------- | ------------------------ |
| Application | 支持具体网络应用             | HTTP、SMTP、FTP、DNS     |
| Transport   | 在两个进程之间传输数据       | TCP、UDP                 |
| Network     | 将数据报从源主机送到目的主机 | IP、路由协议             |
| Link        | 在相邻网络节点之间传输数据   | Ethernet、Wi-Fi、PPP     |
| Physical    | 在介质上传输一个个 bit       | 电信号、光信号、无线电波 |

## ISO/OSI referenced model

OSI 参考模型有七层：

```markdown
Application
**Presentation**
**Session**
Transport
Network
Link
Physical
```

相比之下，Internet 五层模型没有单独列出：

- **Presentation layer（表示层）**：数据格式转换、压缩、加密等；
- **Session layer（会话层）**：建立和维护会话、同步、检查点和恢复。

Internet 模型并不是完全没有这些功能，而是通常让应用层或应用所使用的库实现。例如：

- TLS 实现加密和身份验证；
- JSON、JPEG、UTF-8 规定数据表示；
- 应用自己处理会话恢复。

