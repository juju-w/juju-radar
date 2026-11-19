---
title: Anthropic登陆纳斯达克，Jeveration单次前向生成图像
author: Juju Radar
summary: Anthropic开启公开交易，正式招股书披露产业配售。Jeveration一次生成图像，Olala公开小模型权重，BiCAT改写双臂动作编码，TabBioMed比较生物医药表格模型，欧委会披露十月网络事件。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-20/
sourceNote: 检索窗口为北京时间11月19日07:00至20日07:00。三项预印本按19日arXiv公告选取，提交时间单列。Olala区分17日预告与19日工件，欧委会按披露日期。七天去重，六条入选，无补看。AI HOT与HF截止日API访问受阻，已直接巡检官网、论文和工件。性能数据为作者报告，未独立复现。
editorialStatus: reviewed
---

# Anthropic登陆纳斯达克，Jeveration单次前向生成图像

<!-- reading-stats -->约 2,300 字 · 阅读约 8 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 20 日

## 本期导读

Anthropic 在纳斯达克开始交易。正式招股书还披露，几家云和芯片公司将按 IPO 发行价参与一笔附条件的私募配售。拆开看，公开发行、老股转让和产业配售对应不同的资金流向。

技术上，Jeveration 用一次前向计算协调整张图。BiCAT 在双臂各自并行预测的基础上，保留两臂之间的一步依赖。两项研究都在缩短反馈时间，但对生成顺序的处理不同。

## 🏛️ Anthropic开始交易，公开发售之外还有产业配售
<!-- source-id: anthropic-listing -->

**公司战略 / 资本市场 · 9.5/10 · 建议深挖**

纳斯达克确认，Anthropic 以 ANT 为代码开始交易，首笔成交价为每股 111.50 美元。此次 IPO 发行价是 83 美元，公开发售 9.8 亿股，按发行价合计 813.4 亿美元。其中约 9.56 亿股由公司发售，对应约 793.8 亿美元毛额。其余是老股东出售的股份，所得归出售股东。公司毛额还需扣除承销折扣和发行费用。

正式招股书另外披露，Google、NVIDIA 等七家公司协议以发行价认购合计 260 亿美元的无投票权股份，交割附有条件。这给 Anthropic 提供了两条不同的资金来源，一条面向公开市场，另一条来自与算力和供应链有关的企业。发行公告预计公开发售于 11 月 20 日交割。跟踪公司未来可用于训练和扩张的资金，需要看新股实际交割与配售进度。首笔成交价影响市场估值，公司的发行收入仍按 83 美元计算。

[纳斯达克确认](https://www.nasdaq.com/newsroom/anthropic-marks-ipo-at-nasdaq) · [发行人公告](https://www.anthropic.com/news/anthropic-prices-initial-public-offering) · [SEC 定价文件](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074937/anthropicpbc-fwppricing.htm) · [正式招股书](https://www.sec.gov/Archives/edgar/data/2130357/000162828026074944/anthropicpbc-424b4.htm)

## 🎨 Jeveration让整张图共用一次随机抽样
<!-- source-id: jeveration -->

**视觉生成 / 开源论文 · 8.5/10 · 建议深挖**

Jeveration 把 Jev 一类模型的并行预测方式用到图像生成。它冻结视觉语言底座，用训练后的模块一次预测整张图的离散编码，再解码成像素。困难在于，同一句提示可以对应很多合理的画面。各位置独立抽样，可能各自选中不同的构图，最后拼不成一张协调的图。

作者因此给所有位置同一个随机状态，并先学习可能的图像编码分布，再训练生成模块利用这份共享信息。论文报告，单张 H200 生成 512×512 图像耗时 77.8 毫秒，GenEval 为 0.74。同一检查点还可做图生图和密集预测，例如深度图估计。约 122 倍提速来自与论文所用 Janus-Pro-7B 的对照。要判断它适不适合交互式设计，还要看更高分辨率、复杂布局和实际服务时延。

[论文与消融实验](https://arxiv.org/abs/2611.24738)

## 🧠 Olala mini公开权重，36层里7层保留注意力缓存
<!-- source-id: olala-open -->

**基础模型 / 推理效率 · 8/10 · 建议深挖**

OVHcloud 11 月 17 日预告 Olala mini，19 日公开模型工件与技术报告。模型约有 70 亿总参数，每个 token 激活约 10 亿。它在欧洲公共超算上训练，权重采用 Apache 2.0 许可。

架构里，29 层 Mamba-3 以递推状态保留信息，另有 7 层注意力保留键值缓存。混合专家每步只激活部分参数，主要影响计算量。减少注意力层则改变对话变长时的缓存需求。部署时可以分别测加载权重占用多少资源、上下文每增长一段会增加多少显存。注意力层数给出了结构线索，实际用量还取决于实现和量化方式。

[模型与权重](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B) · [厂商预告](https://corporate.ovhcloud.com/en-ie/newsroom/news/ovh-olala-mini/) · [技术报告](https://huggingface.co/OVHaiLLM/Olala-v1.0-mini-7A1B/blob/main/Olala-v1.0-mini.pdf) · [代码目录](https://github.com/orgs/OVHai-LLM/repositories)

## 🤖 BiCAT把两只机械臂的配合写进动作编码
<!-- source-id: bicat -->

**机器人 / 开源论文 · 8/10 · 建议深挖**

双臂机器人常要一只手固定物体，另一只手完成操作。BiCAT 给两条手臂保留各自的动作序列，让它们共享同一套动作表示，并在编码时交换信息。模型先并行预测第一只手的一组动作，再根据结果并行预测第二只手。这样只增加一个预测步骤，就能让后者看到前者准备怎么动。

作者在 RoboTwin 2.0 的 10 项模拟任务上报告，平均成功率比比较组中最强的动作编码器高 17.6 个百分点。他们还在三种机器人上验证了六项实机任务。论文的 40.5 毫秒来自动作块推理，在单张 H200、批量为 1 的条件下测得。部署要把相机采集、通信和关节执行也纳入延迟测量。

[论文](https://arxiv.org/abs/2611.23499) · [项目演示](https://magiclab-nus.github.io/BiCAT/) · [代码仓库](https://github.com/MAGICLAB-NUS/BiCAT)

## 🔬 TabBioMed把跑不完的评估也纳入表格模型比较
<!-- source-id: tabbiomed -->

**AI for Science / 生物医药 · 7.5/10 · 建议深挖**

TabBioMed 整理了 94 个公开生物医药表格数据集，对照 23 种模型实现。表格基础模型在整体比较中表现较强，但在较大、高维数据集上也更常遇到超时和内存不足。作者同时报告了只看完整案例的结果，以及对缺失结果做填补的分析。适用于全部数据集的主比较包含 21 种模型。

这会改变实际选型。团队通常有固定的时间和显存预算。如果一次评估跑不完，平均榜单分数再高也无法解决交付问题。梯度提升树和调优后的多层感知机在这些约束下仍有竞争力。该基准来自公开回顾性数据，无法据此判断临床应用效果。

[论文](https://arxiv.org/abs/2611.23779) · [代码与评测说明](https://github.com/AI-sandbox/TabBioMed) · [数据集](https://huggingface.co/datasets/TabBioMed/TabBioMed)

## 🛡️ 欧委会披露10月网络事件涉及AI工具
<!-- source-id: ec-cyber-disclosure -->

**真实事故 / 安全治理 · 8/10 · 持续观察**

欧委会在 11 月 19 日记者会上确认，10 月发现的一次网络事件涉及 AI 工具。10 月 22 日检测到异常，26 日经初查确认。欧委会出于防范暂时下线若干应用，披露时多数已经恢复，并称正与欧盟机构网络安全应急团队及欧洲数据保护监管机构保持联系。

发言人表示，调查尚未发现影响欧委会员工整体的数据泄露证据。攻击归因、AI 在各环节所起的作用和完整影响范围仍在调查。服务恢复让业务能继续运行，数据影响则是另一条需要后续证据的问题。

[欧委会记者会](https://audiovisual.ec.europa.eu/en/media/video/I-298222) · [美联社采访](https://apnews.com/article/79705095e8141cd650196dbff1cf3c70)

## 今日主线

Jeveration 把构图所需的共同信息放进共享随机状态，让各位置可以同时预测。BiCAT 则保留两步顺序，因为第二只手需要知道第一只手准备怎么动。速度优化要先搞清输出依赖什么。能提前共享的信息可以减少等待，必须由前一步产生的信息仍值得保留顺序。

## 推荐阅读

先读 Jeveration 的共享状态消融，再看 BiCAT 分组预测的延迟与成功率对照。关注算力产业的读者可从 Anthropic 招股书的配售条款与 Olala 的模型结构读起。

## 原始资料

点击文末“阅读原文”，查看本期全部来源、论文、代码与项目链接。

*Juju Radar · AI辅助整理，供研究与阅读参考。*
