# 接入网络 (access network)

有以下几种方式将主机 (end system) 接入边缘路由器 (edge router)：

- DSL (Digital Subscriber Line)：电话线接入
- Cable Network：有线电视网络接入
- Ethernet：以太网接入
- Wireless access networks: 无线接入网络

> 边缘路由器 (edge router)：端系统的数据离开本地接入网络、进入 ISP 或其他网络时经过的第一个路由器。

在比较接入网络时重点关注以下两个指标：

- **Bandwidth**：传输速率是多少，bits per second？
- **Shared or dedicated**：线路由多人共享，还是一户独享？

### DSL

DSL 使用家庭现有的铜质电话线接入互联网：

```
电脑 → DSL modem → 电话线 → DSLAM → ISP
```

同一根电话线使用不同频率同时传输：

- 语音进入电话网络；
- 数据进入 ISP 和互联网。

Bandwith:

- < 2.5 Mbps upstream transmission rate (typically < 1 Mbps)

- < 24 Mbps downstream transmission rate (typically < 10 Mbps)

Shared or dedicated:

- 家庭到电话局 DSLAM 的这段线路通常是 **dedicated（专用）**的，即每户有自己的电话线。

> **Downstream transmission**：数据从互联网或 ISP 传到用户，也就是通常说的**下载**。
>
> **Upstream transmission**：数据从用户传到互联网或 ISP，也就是通常说的**上传**。

![dsl](/Users/yzhbradoodrrpurp/Desktop/Computer Networks/notes/resources/dsl.png)

### Cable Network

Cable network 利用原有的有线电视网络上网，一般称为 **HFC** (Hybrid Fiber Coax，混合光纤同轴电缆)：

```
家庭 → cable modem → 同轴电缆/光纤 → CMTS → ISP
```

电视和上网数据通过不同频段传输，这叫 **FDM（Frequency Division Multiplexing，频分复用）**。

Bandwith：

- up to 30Mbps downstream transmission rate
- 2Mbps upstream transmission rate

Shared or dedicated:

- homes share access network to cable headend

Cable 与 DSL 的关键区别是：

| DSL                                | Cable                          |
| ---------------------------------- | ------------------------------ |
| 家庭到电话局的线路一般独享         | 多户家庭共享一段电缆           |
| 邻居的使用通常不直接占用你的接入线 | 邻居大量下载时可能争用共享带宽 |
| 使用电话线                         | 使用有线电视电缆和光纤         |

![cable](/Users/yzhbradoodrrpurp/Desktop/Computer Networks/notes/resources/cable.png)

### Ethernet

公司和大学通常使用 **Ethernet（以太网）**：

```
电脑 → Ethernet switch → 机构路由器 → ISP
                       └→ 校内服务器
```

- 终端通常先连接到以太网交换机
- 多台交换机再连接到机构路由器
- 机构路由器通过专线或其他链路连接 ISP
- 学校或企业也可能在内部部署邮件、Web 等服务器

Bandwith:

- 10 Mbps, 100Mbps, 1Gbps, 10Gbps transmission rates

![ethernet](/Users/yzhbradoodrrpurp/Desktop/Computer Networks/notes/resources/ethernet.png)

### Wireless access networks

端系统通过无线信号连接到基站或接入点 (access point)，再由它接入路由器。

有两种 wireless access networks 方式：

1. **Wireless LAN（无线局域网）**

   也就是 Wi-Fi，覆盖家庭、办公室或教学楼等较小范围：

   ```
   手机 → Wi-Fi AP → 路由器 → Internet
   ```

2. **Wide-area wireless access（广域无线接入）**

   也就是运营商的蜂窝网络，例如 3G、4G、LTE、现代的 5G：

   ```
   手机 → 蜂窝基站 → 运营商网络 → Internet
   ```

无线介质通常是共享的，多台设备会竞争有限的无线信道资源。

# 主机数据传输

应用产生一条消息后，主机会把消息分割成较小的 **packets（分组/数据包）**，然后逐个送入接入链路。

如果：

- 数据包长度为 \(L\) bits；
- 链路传输速率为 \(R\) bits/s；

那么，把整个数据包“推入”链路所需的时间是：
$$
d_{\text{trans}}=\frac{L}{R}
$$


例如，一个数据包为 1 Mb，链路速率为 10 Mbps：
$$
d_{\text{trans}}=\frac{1\text{ Mb}}{10\text{ Mbps}}=0.1\text{ s}
$$


这里算的是 **transmission delay（传输时延）**，也就是把所有 bit 放进链路所需的时间，并不是数据在物理线路上传播到目的地的时间。

### 数据传输介质

数据依靠物理介质传播，物理介质分成两类：

| 类型               | 含义                   | 例子                        |
| ------------------ | ---------------------- | --------------------------- |
| **Guided media**   | 信号沿着固体介质传播   | 双绞线、同轴电缆、光纤      |
| **Unguided media** | 信号在空气或空间中传播 | Wi-Fi、蜂窝网络、微波、卫星 |

具体包括：

- **Twisted pair（双绞线）**：常见网线，由成对铜线组成；
- **Coaxial cable（同轴电缆）**：常用于有线电视和 Cable 接入；
- **Fiber optic cable（光纤）**：使用光脉冲传输，速度高、距离远、抗电磁干扰；
- **Radio（无线电）**：无需实体线缆，但会受到遮挡、反射和干扰；
- **Satellite（卫星）**：覆盖范围大，但尤其是地球同步卫星，传播时延较高。

