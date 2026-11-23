---
title: GLM-5.4让28层跑两遍，MemOnce按需重建缓存
author: Juju Radar
summary: 智谱重复使用28层提升计算深度。MemOnce把历史状态移出显存，按需重建缓存。另读防穿墙视频研究、OpenCode桌面版、Helios整柜和黎曼证明的内核复核。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-24/
sourceNote: 检索窗口为北京时间11月23日07:00至24日07:00。GLM-5.4官网仅列日期，窗口内有公开记录。两篇论文按arXiv的23日公告批次纳入，较早的代码和权重发布时间另记。无补看。
editorialStatus: reviewed
---

# GLM-5.4让28层跑两遍，MemOnce按需重建缓存

<!-- reading-stats -->约 2,600 字 · 阅读约 9 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 24 日

## 本期导读

智谱发布 GLM-5.4，把同一组 28 层用两遍，并让第二轮沿用第一轮的部分缓存。MemOnce 从另一端节省显存，把长历史压缩后移出显卡，等新问题到来再取回。另有一项视频研究尝试让世界模型在画出穿墙之前修正动作。OpenCode、微软 Azure 和黎曼猜想的复核也更新了具体进展。

## 🔁 GLM-5.4 让同一组 28 层运行两遍
<!-- source-id: glm54-loop -->

**基础模型 / 多模态 · 9/10 · 建议深挖**

智谱在已经预训练的 GLM-5 基座上继续训练，让同一组 28 层用同一套权重运行两遍。第二遍接过第一遍产生的中间状态继续计算。两轮各自有门控，动态控制每个词元的新状态写回多少。智谱报告，第一轮大体形成上下文，第二轮再进一步修正结果。

如果给每一轮各存一份完整的注意力键值缓存（KV），长上下文会给显存带来额外压力。GLM-5.4 的第二轮沿用第一轮选出的稀疏注意力位置和相应的远处键值，只在当前位置附近留一份自己算出的键值。这样的设计保留了第二轮对近期内容的修正，也让它继续参考整段上下文中的相关位置。

智谱在同架构的 300 亿参数模型上做了同参数量对照，循环版总训练计算量多约一成，部分数学、科学推理和长上下文结果更好。这个对照的结论适用于该实验，旗舰版服务的实际延迟仍取决于请求和负载。GLM-5.4 已进入 Coding Plan、ZCode 和 Z.ai Chat，通用 API 和权重在官方公告里仍列为后续计划。

[智谱技术公告](https://z.ai/blog/glm-5.4) · [ZCode 接入说明](https://zcode.z.ai/en/docs/qa)

## 🧠 MemOnce 把长上下文缓存改为按需重建
<!-- source-id: memonce-memory -->

**开源论文 / 推理效率 · 8.5/10 · 建议深挖**

常规 Transformer 往往要给多层注意力都保存长历史。MemOnce 把历史压成末层的一小部分向量，放进可以卸载到 CPU 内存或固态硬盘的记忆池。新输入到来时，模型先检索一次相关历史，再把取回的向量投影成各层要用的注意力键值。各层可以共用一份检索结果，同时保留各自的键值表示。

论文表 14 的百万词元实验使用 Qwen3.5-4B 适配版。作者报告，GPU 上的活跃缓存为 25 MB，另有 640 MB 历史池在 GPU 外。原基线的活跃缓存为 32.05 GB。两者预填充用时分别为 41.36 秒和 286.86 秒。这里比较的是处理输入和准备缓存的阶段，模型权重本身还要占空间，单卡放不下的基线也使用了多卡。

这套设计使长历史的常驻显存和历史总量分开。代价是每次要找到正确的片段再恢复它。作者尚未系统验证长程编程和多步工具使用，早期代码和适配权重可用于检验这两类工作负载。

[MemOnce 论文](https://arxiv.org/abs/2611.27973) · [项目页](https://clare-nie.github.io/MemOnce/) · [代码](https://github.com/Clare-Nie/MemOnce) · [适配权重](https://huggingface.co/ClareNie/MemOnce)

## 🎬 NoPeWorld 读取扩散模型的中间状态来拦下穿墙
<!-- source-id: nopeworld-collision -->

**视觉视频 / 世界模型 · 8.5/10 · 建议深挖**

让视频世界模型朝砖墙走，有些模型会画出墙，然后把镜头送到墙后。香港理工大学团队发现，视频扩散模型在生成过程中的中间状态已经带有碰撞信息。NoPeWorld 保持生成器权重不动，另训练一个小预测头，读取这些状态并判断候选动作会不会穿透障碍。发生冲突时，它尽量保留原来的移动意图，例如改成沿墙滑动或停下。

论文以虚幻引擎场景的几何作为参照。在闭环生成的碰撞模式中，六个开源生成器的平均违规率从 74% 降到 16%。完全停下也能减少穿墙，代价是牺牲移动意图，因此论文同时评估动作保留。这个结果覆盖特定的障碍穿透测试，仍存在误拦正常动作的情形。项目此前已公开预测头和评测数据，这次新增公开的是给出完整方法与实验的论文。

[NoPeWorld 论文](https://arxiv.org/abs/2611.27963) · [项目页](https://nopeworld.github.io/) · [实现](https://github.com/yuhangdai427/NoPeWorld) · [预测头权重](https://huggingface.co/PeterDAI/NoPeWorld) · [NoPeBench 数据](https://huggingface.co/datasets/PeterDAI/NoPeBench)

## 🖥️ OpenCode 桌面版把浏览器会话与自动任务接到一起
<!-- source-id: opencode-browser -->

**Agent / Coding · 8/10 · 建议深挖**

OpenCode v2.4.0 增加了桌面内置浏览器。浏览器能够导入已有登录状态与历史，也会跨重启保留标签页。在同一个应用里，用户能让代理读页面、改代码，再打开登录后的测试页面检查结果。对需要反复排查界面的任务，节省的是重新打开页面和恢复测试状态的时间。

新版也提供按定时、周期或应用事件触发的自动任务。浏览器会话一旦可以跨任务复用，原来跟着某个测试账号留下的状态也可能被后续工作接着用。用于团队开发时，浏览器配置适合与工作区权限一起检查，具体可访问的页面取决于配置和账号。

[GitHub 发行记录](https://github.com/anomalyco/opencode/releases/tag/v2.4.0) · [OpenCode 更新日志](https://opencode.ai/changelog/v2.4.0)

## 🧩 Azure 在实验室验证 AMD Helios 整柜推理
<!-- source-id: helios-azure-lab -->

**芯片算力 / 推理设施 · 8/10 · 持续观察**

AMD 披露，微软在一座 Azure 研究实验室给首柜 Helios 通电，并开始运行早期负载。这个机柜把 MI455X 加速器、EPYC 处理器、Pensando 网络和 ROCm 软件接在一起。进入工作负载验证后，微软要检查这套组合能否跑好实际模型，范围包括单卡之外的通信和软件栈。

此前双方已公布部署计划。此次新增披露的是交付后的实验室进度。AMD 说 Azure 计划规模部署，尚未给出客户可购买的地区、上架日期、规模或实测成本。

[AMD 验证进度](https://newsroom.amd.com/news/microsoft-running-workload-validation-amd-helios-rackscale-solution/) · [Helios 整柜资料](https://newsroom.amd.com/press-kits/press-kit-helios-rackscale-solution/)

## 🔢 黎曼证明的完整导出通过 Lean 官方两种内核复核
<!-- source-id: riemann-lean-kernel -->

**AI for Science / 数学 · 8/10 · 持续观察**

前一期的隔离重建复现了同一份证明导出。MIT 数学家 Andrew Sutherland 的新记录显示，Lean 官方默认内核和更严格的 paranoid 模式都直接读完这份完整导出，并通过核验。在单线程上两次分别约用 9 小时和 10 小时，峰值内存约为 82.6 GiB 和 98.8 GiB。

这两次复核使用原版 Lean 二进制，只调节了内存分配器全堆回收的频率，核验逻辑相同。另一条 Comparator v4.33 流程也通过，使用的是已有构建产物。同一报告仍把另一条用默认设置运行的 Comparator 流程列为进行中。新增的是完整导出通过两种官方内核的记录，数学命题仍是原先的范围。

[MIT 核验报告](https://math.mit.edu/~drew/grh/) · [默认内核日志](https://math.mit.edu/~drew/grh/lean-default-kernel-tuned.log) · [严格模式日志](https://math.mit.edu/~drew/grh/lean-paranoid-kernel-tuned.log) · [Comparator 日志](https://math.mit.edu/~drew/grh/comparator-v4.33.0.log)

## 今日主线

GLM-5.4 和 MemOnce 都要让后续计算继续用到较早的上下文。GLM-5.4 在相邻两轮之间直接复用远处键值，只补上近处的更新。MemOnce 把长历史存到显存外，新问题到来后选择少量历史，再把它恢复成可供注意力读取的形式。评估这两类系统时，常驻显存、历史存储和每次查询的耗时要一起看。单独一个缓存压缩数字，很难说明应用能省下多少算力。

## 推荐阅读

想理解长上下文的成本，先看智谱技术公告中的混合缓存设计，再看 MemOnce 表 14 如何拆分活跃缓存和外置历史。关注视频交互可靠性的读者，可以从 NoPeWorld 的闭环几何测试看它怎样兼顾避障与原本的移动方向。

## 原始资料

点击文末“阅读原文”，查看本期全部来源、论文和项目链接。

*Juju Radar · AI 辅助整理，供研究与阅读参考。*
