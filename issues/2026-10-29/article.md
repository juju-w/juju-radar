---
title: Gemini 4 Carbon公布，Copilot开始编排多模型
author: Juju Radar
summary: Carbon把重点放在持续工程和网络安全；Copilot Fusion按任务组织模型协作。另看MiniCPM-OCR的独立判别器、NVIDIA可控转写、Google Cloud采用数据，以及有限单群分类形式化补看。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-10-29/
sourceNote: 检索窗口为北京时间10月28日07:00至29日07:00。Carbon、GitHub及NVIDIA博客有28日精确发布时间；Alphabet的8-K接收时间为28日20:01:33UTC，并核对CEO本人链接的正式讲话。MiniCPM公告显示28日，小时级边界未独立确认，模型创建、文件更新与正式宣布分列。Axiom工作26日宣布、公开仓库27日创建，为本期唯一超窗补看，不计当日新进展。Cathedral原始报道为26日，不因28日转述重报。HF29日列表失败，已补查九领域原始入口；论文初筛与全文阅读范围分别记录。重要度为编辑判断，模型与经营数字保留披露主体；未独立复现性能或编译CFSG证明。
editorialStatus: reviewed
---

# Gemini 4 Carbon公布，Copilot开始编排多模型

<!-- reading-stats -->约 3,200 字 · 阅读约 11 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 10 月 29 日

## 本期导读

Google公布Gemini 4 Carbon，强调长时间工程任务与网络安全；GitHub则把模型选择、升级和互评做成Copilot的一部分，并通过Microsoft Foundry向外部提供运行Agent的基础设施。

另外四条分别关注文档、语音、采用规模与数学：MiniCPM-OCR配了独立的区域判别器，NVIDIA让同一录音按不同文字约定输出，Google披露Cloud与模型调用增长，Axiom则把一项巨大的人类证明转成可供机器检查的工程。

## 🛡️ Gemini 4 Carbon瞄准持续工程与网络安全

<!-- source-id: gemini-carbon -->

前沿模型 / 网络安全 · 9.5/10 · 建议深读

[Google公布Gemini 4 Carbon](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-carbon/)，距Argon约两周。公司称，Carbon在内部能够连续运行数天，追查大型代码库和底层系统里的复杂问题；当前先向部分安全防御者开放，再逐步扩展到可信伙伴，尚未普遍进入消费者和开发者产品。

这次值得分开看的是漏洞发现、风险验证与修复。Google报告Carbon在[SEC-bench Pro](https://github.com/SEC-bench/SEC-bench-Pro)达到88.2%，在修补任务CWE-bench达到71.0%。发现可疑代码、证明问题可触发、交付根因修复，是三个不同环节；模型若能把它们持续做完，对安全团队的价值会高于多找到几个可疑点。

这些网络安全结果是在未启用护栏时评测的。它们不能直接等同于实际开放版本的表现，内部“运行数天”也没有配套公开的任务成功率。官方披露了训练与运行时防御的改进，但未给出新的架构细节；现阶段更适合关注完整任务交付和失败记录，而非把单个榜单成绩当成部署结论。

## 🧩 Copilot Fusion把模型选择变成运行时决策

<!-- source-id: copilot-orchestration -->

Agent / 编程基础设施 · 8.5/10 · 建议深读

[GitHub Copilot Fusion正式可用](https://github.blog/changelog/2026-10-28-route-and-orchestrate-models-with-github-copilot-fusion)。用户选择任务所需的投入档位后，系统可以让一个模型直接完成，也可以先用高效模型起草，再通过质量检查决定是否升级；另一条路径是让第二个模型审阅，由原模型修改。

这比把多个模型固定串起来更有意义：额外调用发生在需要升级或复核的地方。GitHub自报，Fusion Max在一项Coding Agent评测中接近Claude Code搭配Opus 5.5 Max的成绩，平均API费用约为一半。不过，实际账单仍按所调用模型各自的价格累加，不能据此承诺每个项目都省一半。

配套变化发生在模型周围。[Microsoft将同一Copilot运行框架通过Foundry提供](https://blogs.microsoft.com/blog/2026/10/28/introducing-the-microsoft-copilot-harness-unlocking-the-potential-of-truly-multi-model-agentic-work/)，管理Agent循环、上下文、工具和沙箱；[GitHub Agentic Workflows](https://github.blog/changelog/2026-10-28-github-agentic-workflows-generally-available)则把Markdown描述编译成Actions工作流，复用既有运行器与策略。日常排障、维护文档和测试因此更容易成为后台持续任务。

另一个容易被夸大的词是“自我改进”。[Copilot Automations的新功能](https://github.blog/changelog/2026-10-28-copilot-automations-now-learn-from-outcomes-and-self-improve)会参考标签被改回、建议被接受、PR被合并等反馈，提出提示词修改供人审阅；它不是自动重训模型权重。

## 📄 MiniCPM-OCR把解析与正确性判别分开

<!-- source-id: minicpm-ocr -->

视觉 / 文档理解 · 8/10 · 建议深读

[MiniCPM-OCR](https://github.com/OpenBMB/MiniCPM-OCR)同时发布了[1.3B文档解析模型](https://huggingface.co/openbmb/MiniCPM-OCR-1.0)和[2B的OCR Jev判别模型](https://huggingface.co/openbmb/MiniCPM-OCR-Jev)。后者按文本、公式或表格区域检查候选：输入原始裁剪图、OCR文字，以及把候选文字重新渲染成的图片，输出0到1的质量分数。

[模型说明](https://github.com/OpenBMB/MiniCPM-OCR/blob/b33b474136088dc43a2341e94590c804ec0c16a5/docs/minicpm_ocr_jev_en.md)给出了具体做法：保留Qwen3.5-2B的视觉编码器和语言骨干，把语言输出头替换成二分类头。它直接比较视觉证据与候选内容，不必先生成一段“我有多大把握”的解释。这样可以从多个解析器的候选中选择，也可以把低分区域交给人工复核。

团队报告JevOCRBench上的AUROC为93.6，表示区分正确与错误候选的能力，不是“93.6%的结果可以免审”。跨解析器实验只用了200个样本；上线阈值仍要用实际文档校准。候选还必须来自同一裁剪范围，所有候选都错时，判别器也不会凭空补出正确内容。

两个模型的权重文件均已可访问，项目标注Apache 2.0。[吞吐复现说明](https://github.com/OpenBMB/MiniCPM-OCR/blob/b33b474136088dc43a2341e94590c804ec0c16a5/docs/benchmark_reproduction_en.md)也坦承，完整版本、计时边界与部分比较日志仍待补齐，暂不把加速宣传推广到任意文档流水线。

## 🎙️ NVIDIA让转写方式成为明确的训练目标

<!-- source-id: nemotron-transcribe -->

语音 / 开放模型与数据 · 8/10 · 建议深读

[Nemotron 3.5 Transcribe](https://huggingface.co/blog/nvidia/nemotron-transcribe-granary)可以根据指令保留口头重复、整理成书面形式、使用领域术语，或标注谁说了哪句话。同一句录音里的“二十五欧元”，写成文字还是“€25”，取决于用途；传统转写指标经常把这些约定差异也算成错误。

[技术报告](https://research.nvidia.com/labs/nemotron/files/NVIDIA-Nemotron-3.5-Transcribe-Technical-Report.pdf)的架构把声学编码器与说话人识别分支并行运行，将“谁在何时说话”的线索加入声学表征，再交给语言模型按指令输出。配套Granary v2为同一录音准备不同转写目标，把格式选择落实到训练样本里。

领域适配也有较清楚的检验。[医疗转写案例](https://github.com/NVIDIA-NeMo/Speech/blob/main/examples/speechlm2/finetuning/docs/medical-asr-synthetic-data.md)按说话人留出测试集，团队报告微调后词错误率从22.44%降到12.17%；一般英语测试却略有退步。它说明专业术语和书写约定可以训练，但应同时检查新说话人与通用能力，不能只看参与调参的数据。

[模型权重](https://huggingface.co/nvidia/NVIDIA-Nemotron-3.5-Transcribe-30B-A4B)已经开放，整体约34B参数、激活约4.3B，属于离线录音模型。内部按30秒分块不代表实时流式；中文远场会议和中英混说仍是限制。官方NIM的最高吞吐还包含尚未全部进入开放实现的优化，不能拿它直接估算本地部署速度。

## ☁️ Google Cloud增长翻倍，要分清三种采用信号

<!-- source-id: alphabet-cloud -->

公司战略 / 云与算力 · 8.5/10 · 持续观察

[Alphabet的Q3正式讲话](https://blog.google/company-news/inside-google/message-ceo/alphabet-earnings-q3-2026/)称，Google Cloud收入同比增长103%；自有模型API每分钟处理近320亿词元，较上季增长40%。Pichai同时强调，TPU系统在不同客户中都有强需求，公司仍在增加供应能力。

这三项数字和表述对应不同生意：云基础设施与解决方案、模型调用、以及TPU系统交付。它们说明Google的AI投入正在通过多条渠道被采用，也意味着不能把Cloud的整体增长直接当成Gemini API收入增长。

调用量还不能回答利润问题。公开讲话没有把这些词元按付费与免费、任务类型或单位利润拆开；“年化收入规模”也不等于已经实现的全年收入。后续更有解释力的变化，是不同交付方式如何影响收入结构与新增产能需求。

## 🔎 补看：Axiom把有限单群分类证明转成Lean

<!-- source-id: axiom-cfsg -->

AI for Science / 形式化数学 · 8.5/10 · 建议深读

10月26日，[Axiom宣布完成有限单群分类的Lean形式化](https://axiommath.ai/research/the-enormous-theorem-formalized/)。这项分类列出了有限群可以分解出的基本“构件”，是已有的人类数学成果。Axiom称，数学家与工程师组织数十个Agent，在24天里完成了约4,310万行代码的项目。

更值得看的是它如何处理证明集成。团队先建立依赖图，把大目标拆成能连接的定理；早期有些片段带着额外、尚未证明的假设，表面完成却接不到最终结论，只能删改重做。规模变大后，复查速度成了瓶颈，工程团队用共享编译缓存和独立检查的计算证书减少重复工作。

[公开仓库](https://github.com/AxiomMath/CFSG)声称，最终证明不含Lean中暂时跳过证明的“sorry”，仅使用三个标准公理。这个声明仍有两层检查：机器验证形式推导，人类核对最终命题和定义是否表达了原来的分类。本文没有运行整个项目的编译，也未独立审计其数学规格。它的重要性在于把巨大证明变成可追踪的依赖与可复用的库，代码行数本身不是质量证明。

## 今日主线

今天几项系统的共同变化，是把额外工作放到了模型调用周围：Fusion决定何时升级和互评，OCR判别器决定哪些区域需要复核，语音模型把书写约定变成训练目标，形式化工程则不断检查证明片段能否连接。它们分别减少不同的成本：昂贵调用、人工检查、格式返工，以及重复编译。

因此，比较Agent系统不能只看核心模型的榜单或单次价格。更具体的问题是：什么情况会触发下一次调用，错误在哪一步被发现，人工最终要检查多少内容。Carbon延长任务跨度之后，这些问题也会变得更重要。

## 推荐阅读

关注前沿能力，先读Carbon的发布范围与评测条件；关注日常开发，读Copilot Fusion的三种协作方式。文档和语音应用可分别看OCR判别器及Nemotron技术报告。数学读者再从CFSG的最终命题、依赖图和构建说明进入完整项目。

点击文末“阅读原文”查看全部来源、模型仓库和研究材料。

Juju Radar · AI辅助研究与整理
