---
title: 黎曼猜想短版 Lean 证明通过复核，英伟达开放文档数据
author: Juju Radar
summary: 黎曼猜想的短版 Lean 证明通过独立复核，素数分布的显式误差界也通过机器检查。另读英伟达文档训练数据、Qwen Code 会话恢复、数学猜想发现、机器人仿真与视频编解码。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-27/
sourceNote: 检索窗口为北京时间11月26日07:00至27日07:00。短版Lean代码在UTC 25日公开，本期报道26日核验及误差界进展。三篇预印本按arXiv 26日公告批次，提交日期另记。无补看。
editorialStatus: reviewed
---

# 黎曼猜想短版 Lean 证明通过复核，英伟达开放文档数据

<!-- reading-stats -->约 2,800 字 · 阅读约 10 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 27 日

## 本期导读

黎曼猜想的短版 Lean 证明通过多套检查器，从短版推导出的素数分布误差界也通过机器核验。英伟达公开三套训练文档解析模型的合成数据，Qwen Code 让部分等审批的会话在进程重启后接着跑。另有三篇论文，分别讲怎样让 AI 从算例里找数学猜想、怎样评测从视频写出来的仿真，以及怎样加快流式视频的编码和解码。

## 🧮 黎曼猜想的短版 Lean 证明通过多套检查器
<!-- source-id: riemann-compact-check -->

**AI for Science / 数学 · 9.5/10 · 建议深挖**

Luke Sernau 和同事用 Claude 把 Alpöge 的 Lean 证明改写成两套源码。易读版约 30 万行，紧凑版约 7.6 万行，两版都保留了原来的五条定理。MIT 的 Andrew Sutherland 公布了复核记录。紧凑版在两台机器上独立构建，导出的证明逐字节一致，两次都通过 Lean 的严格比对流程。易读版也在大内存机器上通过。在同一台大内存机器上，检查器 lean4lean 跑易读版用了约 332 GB 内存，跑紧凑版用了约 7 GB。紧凑版的完整导出文件反而更大，实际复核成本要看具体检查器怎样处理展开后的证明。

Sutherland 还核验了由紧凑版推出的 Schoenfeld 误差界。把小于等于 x 的素数幂按其底数的对数加权求和，得到切比雪夫函数 ψ(x)。当 x 至少为 73.2 时，ψ(x) 与 x 的差的绝对值小于 √x(log x)²/(8π)。这是 1976 年已有的条件性结论。这次把它和黎曼猜想的等价关系写入 Lean，再接上短版证明，让这条关于素数分布的具体上界也能沿同一套流程检查。

[MIT 复核记录](https://math.mit.edu/~drew/shortgrh/) · [短版固定提交](https://github.com/lsernau/grh-lean/tree/72fead10) · [误差界形式化](https://github.com/AndrewVSutherland/schoenfeld-rh-lean/tree/0e52d7b1) · [滑铁卢大学 Rubinstein 的复核记录](https://www.math.uwaterloo.ca/~mrubinst/alpoge_claude_grh/)

## 📄 英伟达公开训练文档解析模型的三套数据
<!-- source-id: nemotron-parse-data -->

**视觉视频 / 文档理解 · 9/10 · 建议深挖**

Nemotron 3.5 Parse 能把一页图像中的文字、表格、图表和阅读顺序转成结构化数据。英伟达公开了用于训练的约 998 万张合成图表、100 万张合成表格和 790 万页多语言文字识别样本，并给出微调配方。合成图表附带轴、系列和数值的答案，表格数据保留表头、行列及单元格关系。训练时可以直接查某个数字是否落在正确的系列或列里。

英伟达先用监督微调教模型读文档，再用可验证奖励的强化学习检查结构、数值和输出是否正常结束。在厂商公布的开发检查点对照中，触发重复检测的页面从 126 降至 29，达到 9,000 词元上限的页面从 185 降至 35。收益在于下游少处理一些看起来像表格、实际错位或没生成完的输出。自有文档里的低清扫描、合并单元格和复杂表头，仍要用真实样本验收。

[英伟达训练说明](https://huggingface.co/blog/nvidia/building-on-nemotron-35-parse-open-data-fine-tunin) · [图表数据](https://huggingface.co/datasets/nvidia/Synthetic-Charts-V1) · [表格数据](https://huggingface.co/datasets/nvidia/Synthetic-Tables-V1) · [多语言 OCR 数据](https://huggingface.co/datasets/nvidia/OCR-Synthetic-Multilingual-v2) · [训练配方](https://github.com/NVIDIA-NeMo/Nemotron/blob/main/docs/nemotron/parse/index.md)

## 🛠️ Qwen Code 让等待审批的会话在重启后恢复
<!-- source-id: qwen-code-recovery -->

**Agent / Coding · 8.5/10 · 建议深挖**

Qwen Code v0.28.6 改了托管会话的暂停方式。符合条件的会话等用户审批、回答问题或等后台任务时，可以保存待处理的动作并释放常驻会话。运行器重开后，批准、拒绝和取消还能作用到原来的动作。后台命令的部分输出捕获也移到了独立工作进程，减少运行器重启导致日志丢失的情况。

这关系到一个常见流程。编码智能体生成补丁后，可能要等人批准一次脚本运行。保存聊天记录只能让人知道它问过什么，恢复待审批的动作才能让批准继续生效。官方验收测试覆盖允许、拒绝、取消、超时和控制进程重启。实际适用范围仍取决于会话能否持久化，发布记录未提供生产环境恢复率。

[正式版本记录](https://github.com/QwenLM/qwen-code/releases/tag/v0.28.6) · [暂停与恢复验收测试](https://github.com/QwenLM/qwen-code/pull/18276) · [后台输出捕获改动](https://github.com/QwenLM/qwen-code/pull/17953)

## 🔎 PatternMiner 用小模型提线索，再用反例改写猜想
<!-- source-id: pattern-miner -->

**AI for Science / 数学 · 9/10 · 建议深挖**

华盛顿大学和太平洋西北国家实验室的研究者让语言模型先生成算例，再训练小模型找预测规律。语言模型尝试把规律写成可检验的猜想，交给数学软件找反例。一旦找到反例，就修改条件或补训练集。小模型在这里帮忙决定该查哪里，论文附录另给一般情形的证明。

作者记录了一个关键的人类干预。研究涉及判断一类 Schubert 系数何时为零。智能体不断找到需要保留五、六、七个维度才能识别的例子。研究者把问题改成寻找一套可随维数增长的构造，最终给出固定保留若干维度的投影测试必然会漏判的证明。论文只试了代数组合里的五个问题，直接让大模型解题的对照在工具和研究预算上也有差异。更值得复查的是，哪类反例能促使智能体放弃原有规则。

[论文摘要](https://arxiv.org/abs/2611.33966) · [论文全文与证明附录](https://arxiv.org/pdf/2611.33966) · [代码和实验记录](https://github.com/uw-math-ai/PatternMiner)

## 🤖 Real2SimLab 把从视频写仿真的方法放到同一套评测里
<!-- source-id: real2simlab-platform -->

**机器人 / 仿真评测 · 8.5/10 · 建议深挖**

从录像生成仿真程序，有个实际好处。程序可以重跑，改视角，或者直接导出物体的运动轨迹。问题是不同基准要求的输入、输出和评分方法并不相同。北大等团队推出 Real2SimLab，用统一接口接收代理产出的程序，再独立执行，交给对应的评分器。论文报告接入了 47 种编码智能体与 5 种非智能体方法。

六项既有基准中，有五项沿用原评分器。IRIS 原来只有实拍视频，平台只适配了其中的落球子集，从录像提取轨迹来比较。加入新方法时可以复用评测接口，读分数时仍要分清它衡量的是画面、轨迹还是物理参数。录像里复现一次运动，并不足以确定模型识别了真实摩擦系数或材质。

[论文摘要](https://arxiv.org/abs/2611.34849) · [评测代码](https://github.com/Real2SimHub/Real2SimLab) · [项目与基准说明](https://real2simhub.github.io/)

## 🎬 LiveVAE 用局部窗口同时加快视频编码和解码
<!-- source-id: livevae-streaming -->

**视觉视频 / 视频推理 · 8.5/10 · 建议深挖**

视频生成和编辑都有两道转换。编码器把像素压成扩散模型能处理的表示，解码器再把表示还原为画面。LiveVAE 的作者测到，现有编解码器处理一个图像块时，主要依赖附近的空间区域和相邻时间帧。他们用局部空间窗口和有限的历史帧来做流式处理，再通过蒸馏保留原模型所用的表示空间。这样既能限制要留在显存里的历史，也能让现有扩散模型继续使用这套表示。

在 MiniMax-H3 的短片重建测试中，LiveVAE 的编码速度是原编解码器的 5.2–6.2 倍，解码速度是 3.0–3.3 倍。这些是编解码阶段的数据。论文也记录了细节变糊、人物保真和物理一致性子项落后的情况，代码仓库暂未见配套权重。对流式视频编辑，尤其值得看输入帧的编码时间，因为每次加入参考画面都要付这笔开销。

[论文摘要](https://arxiv.org/abs/2611.34912) · [模型结构与展示](https://livevae.github.io/) · [项目仓库](https://github.com/MeiGen-AI/LiveVAE)

## 今日主线

文档解析、数学猜想和机器人仿真都需要把表面正确的结果交给另一种检查。表格可以核对数字和列的对应关系，猜想可以找一条违反结论的算例，仿真则能从第二个视角重跑。短版 Lean 的复核还说明，验证本身也可能很贵。把可执行的中间结果保存下来，再测一遍需要多少时间和内存，有时和报告最终分数一样重要。

## 推荐阅读

关心黎曼猜想的进展，先看 MIT 记录里的两版核验对照和 Schoenfeld 界。想理解 AI 怎样提出猜想，可接着读 PatternMiner 第 4.1 节。做文档解析或视频部署，分别看英伟达的训练对照与 LiveVAE 论文表 1。

点击文末“阅读原文”，查看本期全部来源、论文和项目链接。

Juju Radar · AI 辅助整理
