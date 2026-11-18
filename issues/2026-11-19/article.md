---
title: Gemini 4 Neon发布，Genie 4开放实时改写场景
author: Juju Radar
summary: Gemini 4 Neon上线，Genie 4开放交互世界。FastFrames拆解视频延迟，TCP4D为机器人录像补动作，星辰4披露昇腾训练工程，SciWorkBench比较科研智能体的执行框架。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-19/
sourceNote: 检索窗口为北京时间11月18日07:00至19日07:00。两条产品消息核对官方发布时间，四篇论文17日提交、18日列入arXiv公告，公告小时边界未确认。六条精选，七天去重，无补看。AI HOT与HF截止日数据访问受阻，已补查官方入口、论文及工件。性能数据为来源报告，未独立复现。
editorialStatus: reviewed
---

# Gemini 4 Neon发布，Genie 4开放实时改写场景

<!-- reading-stats -->约 2,500 字 · 阅读约 9 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 19 日

## 本期导读

Google 发布新的快推理模型 Gemini 4 Neon，并将能在探索时修改场景的 Genie 4 开放给符合条件的 Ultra 用户。Apple 的 FastFrames 发现缓存更新和像素呈现也是视频跟不上操作的主要原因。

机器人研究尝试把没有动作日志的旧录像变成训练数据。星辰 4 新报告披露大规模昇腾训练细节。SciWorkBench 则发现，同一个模型换一套执行框架，科研任务的分数可能升，也可能降。

## 🧠 Gemini 4 Neon发布，补上快推理与复杂任务之间的一档
<!-- source-id: gemini-neon -->

**基础模型 / 多模态 · 9/10 · 建议深挖**

Google 发布 Gemini 4 Neon，开始在 Gemini API、企业平台、Antigravity 和 Gemini 应用推送。模型支持 100 万 token 上下文和四档推理强度。API 每百万 token 的标价为输入 3 美元、缓存输入 0.15 美元、输出 15 美元。对需要读大量文件、又要做多步分析的任务，这一档提供了新的成本选择。

发布文还给出一组比榜单名次更实用的对照。同一 Neon 在 SWE-sweep 上使用 mini-SWE 框架得 12.8%，换到 Google Antigravity 得 39.0%。差值来自整套执行配置，无法从这组结果分离某项工具的贡献。团队评估升级时，可以先把代码库、工具和验收标准固定下来，再比较完成同一任务的费用和返工量。否则，模型与框架同时更换，收益来自哪里很难判断。

[Google 发布说明](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)

## 🎮 Genie 4开放，探索途中可以改写场景
<!-- source-id: genie-4-rollout -->

**视觉视频 / 世界模型 · 8/10 · 建议深挖**

Google 在 10 月公布 Genie 4，这次通过 Project Genie 向符合条件的 Google AI Ultra 用户开放。人在场景里移动时，可以用文字改变天气、加入角色或改变故事走向，环境音和对白也会随生成过程变化。新画廊允许发布、探索和改编已有场景。

它把修改放进一次连续体验里。过去要比较暴雨与晴天的场景，可能要分别准备两段素材，现在可以在探索中切换条件，再观察同一空间接下来怎样变化。开放公告里的最长三分钟、全景图作为起始场景和多世界串联属于 Genie 3 的更新。Genie 4 的演示主要说明交互能力，长期空间一致性和物理规律仍需要单独测量。

[本次开放公告](https://blog.google/innovation-and-ai/models-and-research/google-deepmind/genie-4-now-available-project-genie/) · [10月技术预告](https://deepmind.google/blog/genie-4-a-new-generation-of-world-simulation/) · [模型卡](https://deepmind.google/models/model-cards/genie-4/)

## 🎬 FastFrames把视频反馈的等待压到几十毫秒
<!-- source-id: fastframes -->

**视觉视频 / 推理效率 · 8.5/10 · 建议深挖**

Apple 团队把延迟定义为一次新操作到第一张受该操作影响的画面出现。连续播出的帧数可以很高，但如果模型每次成批生成，观众按下方向键仍可能要等到下一批才能看到变化。论文因此把缓存更新、扩散采样和转成像素的时间都算进一次响应。

研究者发现，在所测基线里，像素解码与缓存更新合计占端到端延迟的一半以上。FastFrames 用针对现有模型特征训练的轻量解码器生成像素，再用小网络修正缓存，省下较重的处理步骤。在 480p 测试中，1.3B 版在单张 B200 上为 36 毫秒，14B 版在八张 B200 上为 45 毫秒。论文还报告提高到 720p 会明显增加延迟。比较交互模型时，画质、硬件和反馈延迟需要放进同一组指标。

[论文](https://arxiv.org/abs/2611.23226) · [项目演示](https://apple-aiml-research.github.io/ml-fastframes/) · [实现代码](https://github.com/apple-aiml-research/ml-fastframes) · [小模型权重](https://huggingface.co/apple/FastFrames-S) · [大模型权重](https://huggingface.co/apple/FastFrames-L)

## 🤖 TCP4D给机器人旧录像补上动作标签
<!-- source-id: tcp4d -->

**机器人 / 开源论文 · 8/10 · 建议深挖**

操作录像能看到抓取过程，却常常缺少同步的机械臂状态。TCP4D 从单目视频和初始二维查询出发，恢复带尺度的工具末端位置、朝向与夹爪状态。同一个时空表示还可以接收指令和后续观测，预测接下来要执行的动作轨迹。

这种表示统一描述工具的位置和朝向，可以适配关节结构不同的机械臂。研究者可以用它把录像里的轨迹重新映射到另一种机器人，并构造对应的观测。论文报告在 DROID 和 RoboLab 上的绝对轨迹误差分别为 7.60 和 16.07 毫米。随机化布局的表现仍有限，夹爪覆盖也较窄。对抓取可以容忍的误差，到了插接就可能决定成败。

[论文](https://arxiv.org/abs/2611.23143) · [项目与演示](https://livioni.github.io/TCP4D/) · [实现代码](https://github.com/Livioni/TCP4D) · [模型集合](https://huggingface.co/collections/HarrisonPENG/tcp-4d-models)

## ⚙️ 星辰 4 新报告披露 8192 张昇腾卡如何协同
<!-- source-id: xing4-report -->

**芯片算力推理 / 开源论文 · 8/10 · 建议深挖**

中国电信团队的新报告介绍了用 8192 张昇腾 910C 预训练 285B 参数模型的工程方案。29B 总参数、4B 激活的公开版本已在 9 月发布。这次新增的是更大规模训练的设计和测量。

报告把高速互联域内和较慢的域间通信分别调度，将部分梯度通信放到反向计算期间。对长上下文还要处理负载不均的问题，例如因果注意力中，序列靠后的片段通常要读更多历史内容。把轻、重片段分配给同一计算单元，可以减少整个集群等待最慢分片的时间。报告中的吞吐改善有各自的对照配置，评价其他集群仍要看实际互联和任务分布。

[技术报告](https://arxiv.org/abs/2611.22115) · [29B 项目](https://github.com/XingChen-AGI/Xing4.0-29B-A4B) · [公开权重](https://huggingface.co/XingChen-AGI/Xing4.0-29B-A4B) · [分布式框架](https://github.com/mindspore-ai/hyper-parallel)

## 🔬 SciWorkBench发现科研智能体对执行框架很敏感
<!-- source-id: sciworkbench -->

**AI for Science / Agent评测 · 8/10 · 建议深挖**

SciWorkBench 的 98 项任务覆盖了科研分析的不同阶段，包括检查输入、执行分析，以及解释证据能支持什么结论。作者评测了 13 种模型和执行框架组合，最高平均分是 57.38，由 GPT-5.6 Sol 与 Codex 组合取得。这个数字来自评分规则，代表平均得分。

框架差异没有统一方向。GLM-5.3-Flash 从 Codex 换成 Claude Code 后提高 14.12 分，Gemini 3.5 Flash 同样切换则降低 15.47 分。研究指出，智能体经常知道基本方法，却无法把它落实到具体数据，或在遇到异常时没有回头检查。实验重复次数有限，评分也有待独立检验。做内部评测时，可以留存数据质检、分析依据和结论三个阶段的输出，找到真正需要研究者返工的一步。

[论文与评测设计](https://arxiv.org/abs/2611.22490)

## 今日主线

Neon 和 SciWorkBench 都显示，执行框架会改变同一个模型完成任务的结果。FastFrames 则测到缓存更新和像素解码在部分视频生成系统中占了超过一半的响应时间。决定下一步怎么优化之前，先定义何时算交付，再找出哪个步骤最慢、最容易出错。

## 推荐阅读

先看 Neon 的框架对照和 SciWorkBench 表 3，再读 FastFrames 的延迟拆解。机器人方向可看 TCP4D 的跨平台增强及随机布局结果，训练基础设施方向可以从星辰 4 的集群拓扑与序列分配读起。

## 原始资料

点击文末“阅读原文”，查看本期全部来源、论文、代码与项目链接。

*Juju Radar · AI辅助整理，供研究与阅读参考。*
