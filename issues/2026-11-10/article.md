---
title: Claude Fable 5.2降价提速，机器人从失败中学习
author: Juju Radar
summary: Fable 5.2基础API价格下降20%；GR00T 2用少量示范微调，美团MR0保留失败与纠正轨迹；另看Google TPU系统、权重编辑复查和马来西亚算力协议。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-10/
sourceNote: 检索窗口为北京时间11月9日07:00至11月10日07:00。六条当前进展，无补看；GR00T公告有9日14:00:01UTC时间，其余仅日期或arXiv9日原始公告组，小时边界不确定。MR0在5日提交、WSP在6日提交，9日首次公开，未将HF推荐日当首发。所有实验与性能数字均来自作者，未独立复现。HF10日接口失败、8日空，AI HOT HTTPError，已补查九领域一手入口并记录缺口。小绿书暂停，微信只保存待审草稿。
editorialStatus: reviewed
---

# Claude Fable 5.2降价提速，机器人从失败中学习

<!-- reading-stats -->约 3,400 字 · 阅读约 12 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 10 日

## 本期导读

Anthropic发布Fable 5.2：基础API降价20%，生成提速，电子设计也有了实际组装的原型。机器人这边，两种降低采集成本的做法值得一起看：GR00T 2把新任务压到少量示范后微调，美团MR0则留下失败过程，让纠正数据说明该避开什么。

还有三条不同方向的进展：Google围绕现有TPU重组系统；新论文复查直接编辑权重的收益与失败；软银、Grab和PETROS签署马来西亚AI基础设施开发协议。

## 🧠 Fable 5.2降价，电路设计走到实物验证

<!-- source-id: claude-fable-mythos-52 -->

基础模型 / 多模态 · 9.5/10 · 建议深挖

[Claude Fable 5.2与Mythos 5.2](https://www.anthropic.com/claude-fable-and-mythos-5-2)基于同一个底层模型。Fable加入网络安全和生物安全限制，面向一般用户；Mythos仍通过专项计划向经过审核的组织开放。[API说明](https://platform.claude.com/docs/en/release-notes/overview)确认支持100万token上下文、最多12.8万token输出，并默认启用自适应思考。

基础输入、输出价格分别为每百万token **8美元和40美元**，相比5.1的10美元、50美元下降20%。Anthropic称，常规生成速度最高提高30%；另有最高2.5倍生成速度的快模式，价格也升到16美元、80美元。这里的倍数指token生成，完整任务还要等待工具、环境和验证，不能直接按同一倍数折算交付时间。

更具体的变化来自[电子设计测试](https://www.anthropic.com/research/claude-electronics-design)。Diode工程师按模型输出组装了扬声器电话、语音控制中枢和虚拟宠物三个原型，电路无需电气修正即可工作，模型同时提供固件、零件与外壳设计。样机仍由人装配与测试，也没有因此完成认证或量产可靠性验证。不过，这已经让输出质量多了一种检查办法：看电路能否实际运行，而不只看设计文字是否合理。

[系统卡](https://www.anthropic.com/document/claude-fable-5-2-mythos-5-2-system-card)还交代了一项有意保留的限制：训练时，部分加速器内核优化和大模型架构研究能力被限制在接近Opus 5.5的水平，其他编程、硬件与传统机器学习任务并未一并限制。开发团队因此需要按自己的工作负载选模型，通用代码成绩不能代替AI研发子任务的实测。

## 🦾 GR00T 2：五次示范之后，还要做一次微调

<!-- source-id: groot2-fewshot -->

机器人 / 世界动作模型 · 9/10 · 建议深挖

NVIDIA在CoRL期间公布[GR00T 2](https://research.nvidia.com/labs/gear/gr00t-2)。它把未来视频和机器人动作放进同一个去噪模型：预测接下来会看到什么，同时生成应该怎样动。预训练结合人类第一视角视频、手持操作设备采集的数据和多种机器人的遥操作数据，让不同身体能共享一部分操作经验。

[白皮书](https://research.nvidia.com/labs/gear/gr00t-2/assets/gr00t2_whitepaper.pdf)的关键实验是Dexter双臂机器人上的50项任务。这些任务没有出现在该机器人的训练数据里，但可能已在人类或其他机器人数据中出现。直接部署时，平均试验成功率为40%；用每项任务一次示范做LoRA微调后为71%，五次示范后为95%。作者报告，适配微调可在单张RTX 5090上约30分钟完成。**“给五次示范”包含参数更新，不是把五段视频放进上下文就立即学会。**

另一组容易混淆的数字是“完成过40项任务”和“40%成功率”。前者指50项里有40项至少成功一次，后者才是所有试验的平均表现。五示范结果也来自这套任务与测试条件，不能直接套到任意工厂动作上。它的价值在于，新机器人可以先继承大规模预训练，再用少量本机示范校准，而不必逐项从零采集。

[同批公告](https://blogs.nvidia.com/blog/robotics-simulation-advancements-corl/)还介绍了Isaac Lab 3.0与人类视频数据入口。本轮已核实项目页和报告，尚未确认GR00T 2权重已可公开下载；现有官方主仓仍展示N1.7。对开发者而言，下一步是核对实际可用的模型版本、目标动作空间和适配工具。

## 🔧 美团MR0把失败现场留在训练里

<!-- source-id: meituan-mr0 -->

机器人 / 交互纠错 · 8.5/10 · 建议深挖

[Meituan-Robotics-0（MR0）](https://arxiv.org/abs/2611.08577)把视觉语言样本与12种机器人身体的轨迹结合训练，再将离散动作表示迁移到连续动作模型。15,060小时机器人数据包括开放真实数据、许可数据和模拟数据，不能全部理解成新公开的真实遥操作数据。[官方仓库](https://github.com/Meituan-Robotics/Meituan-Robotics-0/tree/opensource)提供训练配置、评估接口和策略服务入口。

更值得看的是[Rollback纠错方法](https://arxiv.org/html/2611.08577v1)。机器人失败后，操作员选中失败前的记录点，将机器人返回那里，再示范正确的后续操作。系统同时保存被替换的失败动作和人工纠正动作。CFG-DAgger据此学习正例、负例与无条件分支，执行时让动作朝成功方向偏移，并避开失败方向；它不需要额外学习一个价值函数。

网线插接实验给出了同条件比较：使用同一批650条遥操作与Rollback轨迹，每种策略测试30次，CFG-DAgger成功率为70%，RECAP为60%。论文里的90%是抓取、交接、插入等里程碑构成的进度分，不能写成插接成功率。样本仍小，但这个比较说明了为何要保存失败：纠正不只告诉模型“怎样做”，也告诉它“刚才哪条路走不通”。

MR0还让高层规划根据事件更新记忆，在进度或可行性变化时重新决策，底层持续生成动作。演示显示任务可在中断后恢复，但这部分尚没有统一成功率支撑。它与GR00T 2形成两种互补做法：少量示范帮助迁移，针对失败的纠正帮助补齐接触操作中的薄弱步骤。

## ⚙️ Google用现有TPU重新配置推理系统

<!-- source-id: tpu8tx-8imax -->

芯片算力 / 推理系统 · 9/10 · 持续观察

Google公布[TPU 8tx与TPU 8iMax](https://cloud.google.com/blog/topics/ai-infrastructure/tpu-8tx-and-tpu-8i-max)。它们采用现有第八代芯片，新增的是系统配置。8iMax把两颗8i放进同一封装，计算、SRAM和HBM带宽约为单颗的两倍；这不等于HBM容量也翻倍。8tx则把8t与定制第五代AMD EPYC主机、Boardfly互联结合，兼顾低延迟推理和训练、微调、强化学习任务。

配套的[TPU Sync](https://cloud.google.com/blog/topics/ai-infrastructure/introducing-tpu-sync-fast-kv-cache-and-weight-transfer-on-tpu)与[Agent Compute](https://cloud.google.com/blog/topics/ai-infrastructure/agent-compute-engine-deep-dive)处理另一类成本：权重、注意力缓存和会话状态怎样在显存、主存与存储之间移动，闲置Agent如何挂起并恢复。长任务往往花时间等待工具或用户，若始终把它的状态留在最昂贵的显存里，芯片算得再快，也可能服务不了更多会话。

这次值得关注的指标因此包括并发会话成本、恢复延迟和实际服务稳定性。双芯片封装的峰值、某项互联优化的延迟收益，都不能直接当作所有请求的两倍加速；目前也没有本轮独立测量的价格与服务表现。

## 🧩 权重编辑复查：小修复有效，通用方法还不稳定

<!-- source-id: wsp-capability-scope -->

开源论文 / 权重编辑 · 8.5/10 · 建议深挖

直接让大模型修改另一个模型的权重，究竟能走多远？[这篇新研究](https://arxiv.org/abs/2611.09382)把GPT-6 Astra接入持续运行的Python与GPU工具，对Qwen3.5的0.8B和9B模型进行16次搜索，覆盖七类任务。过程不用梯度，但允许查看张量、修改参数、调用开发评测；每次搜索有50次成功的工具请求预算，因此仍有搜索和验证成本。

最好的0.8B数学修改只改变了1,023个实际存储的BF16参数，集中在一个MLP下投影列。在论文的留出评测协议下，MATH-500从8.35%升到37.80%，增加29.45个百分点。作者用控制实验支持一种解释：部分修改减少了反复自我怀疑与循环，帮助模型更顺畅地使用已有解题能力。这仍是对特定模型行为的解释，不能据此认定找到了通用“数学神经元”。

失败结果同样关键。16次搜索里有6次最终保留原模型；9B数学搜索在开发集上涨29.69个百分点，留出集却下降0.35个百分点。三次0.8B数学搜索的留出收益也明显不同。修改更多参数并不保证收益更大，跨任务迁移更不均匀。论文附录称开发与留出题目经过文本规范化去重，本轮没有独立审计原始数据。

这些结果支持把权重编辑当作诊断特定行为故障后的修复工具，却不足以说明它能稳定替代训练。[项目仓库](https://github.com/WSP-Scope/WSP-Scope-Project)当前根目录仅有报告PDF，本轮也未复现修改。后续最有价值的证据，是不同编辑模型、目标模型和任务上都能重复出现的留出收益。

## 🌏 马来西亚算力协议，资本跟着客户里程碑投入

<!-- source-id: softbank-grab-malaysia -->

公司战略 / 算力建设 · 8/10 · 持续观察

[软银、Grab与PETROS签署联合开发协议](https://group.softbank/en/news/press/20261109_0)，计划在沙捞越及马来半岛建设AI基础设施。拟投入的初始种子资金合计18.5亿美元：软银10亿、Grab7.5亿、PETROS1亿；长期目标为5GW以上算力容量。

公告明确，资金按项目开发、客户合同等里程碑分阶段部署，并受必要交割条件约束，还要寻找其他投资者与大型云客户。5GW是长期目标，初始资金也不是整个目标容量的全额预算。跟踪这个项目时，客户合同、阶段交割和实际投运，比把目标容量直接计入供应更能说明进度。

## 今日主线

模型能力要进入实际系统，还要跨过几道具体工序：电路需要组装测量，机器人需要本机校准和失败纠正，长任务服务需要安排闲置状态。今天几条技术进展分别减少了这些工序的代价。权重编辑的正反结果则提醒我们，局部修复究竟能释放多少已有能力，要靠留出任务和重复搜索回答。

推荐先读Fable发布与电子设计实例，再对照GR00T 2的50任务图表和MR0的Rollback实验；对权重编辑感兴趣，可以从新论文的失败搜索与开发集、留出集差异读起。TPU与马来西亚协议分别适合跟踪服务成本和算力建设进度。

## 原始资料

点击文末“阅读原文”，查看本期全部原始来源、研究报告、论文与代码入口。

补充资料包括[GR00T人类视频数据](https://huggingface.co/datasets/nvidia/PhysicalAI-Human-1M-100K)、[Isaac Lab 3.0版本说明](https://github.com/isaac-sim/IsaacLab/releases/tag/v3.0.0)、[MR0项目页](https://meituan-robotics.github.io/Meituan-Robotics-0/)与[模型入口](https://huggingface.co/MeituanRobotics/Meituan-Robotics-0)、[AMD主机配置公告](https://newsroom.amd.com/news/amd-epyc-expands-leadership-foundation-ai/)，以及[权重编辑论文全文](https://arxiv.org/html/2611.09382v1)和[研究项目页](https://wsp-scope.github.io/)。

Juju Radar · AI辅助研究与编辑，内容待审核。
