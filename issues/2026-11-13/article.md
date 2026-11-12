---
title: Gemini新增执行模型，NVIDIA宣布管理层交接
author: Juju Radar
summary: Hydrogen把规划与执行分工推到产品层；NVIDIA进入管理交接；Anvil用更强模型压力测试安全防线，另补充Gemini Decisions的判断接口。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-13/
sourceNote: 本期窗口为北京时间2026年11月12日07:00至13日07:00。Hydrogen官方元数据为12日18:00 UTC；NVIDIA与Anvil只核实公告日期，小时边界不确定。Decisions原文11日18:00 UTC，单列超窗补充。七天去重；官方实验未独立复现。HF13日日期页不可用，AI HOT失败，已补查一手入口与前两日论文列表。
editorialStatus: reviewed
---

# Gemini新增执行模型，NVIDIA宣布管理层交接

<!-- reading-stats -->约 2,100 字 · 阅读约 8 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 13 日

## 本期导读

Google新推出的Hydrogen，开始把“复杂任务由谁想、重复工作由谁做”落实为产品功能：同一编程会话可以自动切换模型。NVIDIA则宣布了影响算力产业的重要人事交接。安全研究方面，Anthropic用内部强模型重新测试人工红队没有攻破的防线。

另补充一条11月11日的消息：Gemini Decisions把分类、路由和评分从文本生成中抽出来，直接返回选项概率。

## ⚙️ Gemini新增Hydrogen，让模型按任务分工
<!-- source-id: gemini-hydrogen -->
基础模型 / Agent编程 · 9/10 · 建议深挖

Google于11月12日发布 **Gemini 4 Hydrogen**，定位是更快地完成日常编程与多步骤任务。它由Carbon适配而来，API价格为每百万输入token 1.5美元、输出7.5美元，支持四档思考强度。

更值得看的是Antigravity新增的 **Orchestrator**：在同一会话内动态切换Carbon、Hydrogen等模型，让复杂判断和高频执行分开承担。Google报告，在Terminal-Bench 4.0上，这种组合接近Carbon的任务成功率，同时平均少消耗24%的配额、快19%。这里的配额不是直接测得的美元成本，结果也来自官方测试。

这种分工对代码任务很具体：先确定修改方案，再并行改文件、跑测试、检查结果。便宜或快速的执行模型能承接更多工作，但如果频繁丢失上下文、选错模型或反复返工，节省就会被吃掉。评估时应记录整项任务的完成率、总费用和耗时，而不只比较输出速度。

还有一个容易看错的规格：模型卡写的是**输入输出共用百万token窗口**，同步输出默认最多64K，最高百万输出需要后台长解码。它并不表示普通请求可以同时输入百万token再输出百万token。

来源：[官方发布](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/) · [模型卡](https://storage.googleapis.com/deepmind-media/Model-Cards/Gemini-4-Hydrogen-Model-Card.pdf)

## 🏢 NVIDIA宣布管理层交接
<!-- source-id: nvidia-transition -->
公司战略 / 算力产业 · 9/10 · 持续观察

NVIDIA于11月12日公告，黄仁勋辞去总裁、CEO及董事职务；现任CFO **Colette Kress兼任临时CEO**，董事会启动正式继任者遴选。Harvey C. Jones出任董事长。SEC文件进一步说明，董事会接受辞职和作出任命的日期为11月11日。

对AI行业而言，后续需要核对的是客户承诺和产品路线图如何执行。董事会表示预计业务、客户承诺和路线图不会中断；这是交接期间的承诺，还需要实际交付来验证。公司仍计划于11月17日发布财报，这将是观察交接安排的下一个公开节点。

管理层变化会增加协调与执行的不确定性，但不能据此推断GPU马上短缺或某条产品路线已经改变。更有用的跟踪对象是供货节奏、客户项目和正式继任安排，而非把人事新闻直接换算成技术结论。

来源：[NVIDIA公告](https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-CEO-Transition/default.aspx) · [SEC 8-K文件](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000082/nvda-20261111.htm)

## 🛡️ Anvil把更强模型用于测试安全防线
<!-- source-id: anthropic-anvil -->
安全研究 / 自动红队 · 8.5/10 · 建议深挖

Anthropic于11月12日公布自动红队系统 **Anvil**。它让多个独立调查会话反复测试目标模型与防护分类器，寻找部署前需要修补的弱点。研究覆盖生物安全、网络安全和防止隐藏推理被提取的防护。

其中一项实际用途，是把发现的失败案例用于改进反蒸馏分类器：作者报告，相关静态评估中未被拦截的攻击比例从31.5%降至0.4%。这说明自动测试能够提供迭代信号；不能把它扩展为所有安全问题都已解决，文中的生物和网络分类器也未采用同样的闭环训练。

比较人工红队时必须保留一个条件：Anvil使用关闭了自身防护的内部模型，还能看到更细的分类器反馈。外部测试者没有这些条件。因此，“超过人工”首先说明内部压力测试发现弱点的能力提高，不代表普通用户已经拥有同等攻击工具。

这项研究提醒开发者，测试对手也要升级。较弱模型或有限人工测试未发现问题，并不足以证明防线能抵御下一代更强的自动化测试。

来源：[Anthropic研究原文](https://safeguards.anthropic.com/2026/automated-red-teaming/)

## 🔎 补充：Gemini把小判断做成专用接口
<!-- source-id: gemini-decisions -->
Agent工具 / 多模态判断 · 8/10 · 建议深挖

Google在**11月11日**发布Gemini Decisions API。它不逐token生成回答，而是让Gemini Decision 1在一次前向计算中，为预设选项打分。文本、图片、音频、视频和PDF可以共用一份输入，问题可以混合是非判断、多选和分档评分。

这适合工具选择、内容相关性筛选等频繁出现的小判断：共同输入只计费一次，各问题另加自己的指令与选项token；价格为每百万输入token 0.1美元，不收输出token费用。普通生成模型用来解释复杂问题，判定模型负责把材料送到合适的下一步。

官方给出的150—250毫秒端到端延迟，对应最多16K上下文等测试条件，不能直接外推到256K输入和1000个问题同时跑满。返回的置信度也不是事实已经核实的证明：选项漏掉“未知”或“拒绝执行”，模型可能只是更快地选了一个不合适的答案。接入时要一起设计候选集合、低置信度回退和人工复核规则。

来源：[Google官方说明](https://blog.google/innovation-and-ai/technology/developers-tools/gemini-decisions-api/)

## 推荐阅读

先读Hydrogen的编排方式，再看Decisions的输入与计费规则：两者分别在减少昂贵执行和重复判断。把它们组合进工作流后，最值得测的不是一次调用有多快，而是整项任务少了多少等待、又增加了多少返工。

安全相关团队可优先读Anvil的对照条件。自动化能力提高后，防护测试也需要更强的对手；一次测试通过，不能长期替代持续更新的评估。

## 原始资料

点击文末“阅读原文”，查看本期全部来源与模型卡。

*Juju Radar · AI辅助研究与编辑，内容待作者审核。*
