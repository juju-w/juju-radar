---
title: Gemini测试直接购物，Jev新评测揭示低成本判断的难题
author: Juju Radar
summary: Gemini在印度测试Flipkart结账入口；补看微软Copilot常驻Agent、Jev安全评测，以及编码Agent为机器人生成可复用规划程序的研究。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-09-28/
sourceNote: 检索窗口为北京时间9月27日07:00至28日07:00。Flipkart报道于9月27日01:30 UTC发布；Copilot公告为9月25日，两篇论文于9月24日提交、25日获HF推荐，均明确列为近期补看。评分为编辑判断。
---

# Gemini测试直接购物，Jev新评测揭示低成本判断的难题

<!-- reading-stats -->约 2,500 字 · 阅读约 9 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 9 月 28 日

## 本期导读

Gemini在印度开始测试一件很具体的事：看完商品，直接进入Flipkart结账流程。AI购物入口与零售商的关系，正在从推荐商品延伸到接入交易。

另外补读三份近期材料。微软准备让Copilot承接持续运行的企业应用和常驻Agent；一篇Jev评测发现，便宜地排出风险高低，与可靠地决定何时报警，是两个问题；机器人研究则尝试让编码Agent先写出规划程序，之后由程序反复处理新场景。

## 🛒 Gemini测试直接向Flipkart下单

<!-- source-id: gemini-flipkart-checkout -->

Agent应用 / 电商 · 8/10 · 建议持续观察

TechCrunch于9月27日发布的[体验报道](https://techcrunch.com/2026/09/26/google-tests-buying-from-walmart-owned-flipkart-through-gemini-and-ai-mode-in-india/)显示，部分印度用户在Gemini和Google的AI Mode里看Flipkart商品时，会看到“Buy”按钮。点击后，Flipkart品牌的结账流程就在AI界面里打开。早期测试只覆盖部分用户，以及手机、电子产品和配件等少量商品。

这一步改变的是购买路径。以前AI推荐完商品，用户还要离开界面去商家网站；现在合作商家能把交易接进来。记者看到，同屏的Amazon商品没有相同购买按钮。由此看，商家今后争取的可能不只有“被AI推荐”，还包括“能否在AI入口完成交易”。这会影响平台合作的价值，但目前没有转化率数据。

Google只回应说，公司一直在试验新功能，没有确认详细时间表和技术方案。报道中的结账页也不同于此前Google托管的演示，尚不清楚是否采用通用商业协议UCP。当前体验仍由用户点击进入购买流程，不能理解为Agent可以自行付款。

## 近期补看

## 🏢 Copilot准备承接企业应用和常驻Agent

<!-- source-id: copilot-persistent-runtime -->

Agent / 企业软件 / 公司战略 · 8.5/10 · 建议关注运行与计费方式

微软9月25日[公布新版Copilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)，新增Home、Code和Autopilot。Home整合聊天、委托任务与可协作的Office文件；Code可以生成内部应用，并在公司的Microsoft 365租户环境中托管运行；Autopilot则拥有自己的身份、记忆、计算机和工作空间，用来持续处理任务。

这一组合值得关注，因为生成代码之后的托管和管理也被纳入产品。业务团队可以尝试把需求做成持续使用的小工具，管理员则要同时管权限、插件、运行环境和费用。微软明确将Cowork、Code、Autopilot等长期任务放入按用量计费：以后判断一项自动化是否划算，要看它持续运行的账单，而不只是聊天订阅的价格。

功能还在分批开放。Home和Code将通过Frontier计划陆续推出，Autopilot计划月底扩大私测。公司是否真能用它减少人工维护，还需要实际任务的稳定性和成本数据，不能从产品预告直接得出结论。

## 🧠 Jev新评测：分数能排序，阈值却不好直接搬用

<!-- source-id: jev-alignment-evaluation -->

模型评测 / AI安全 / 论文 · 8.5/10 · 建议读实验与消融

9月24日提交的[Just Ask Jev](https://arxiv.org/abs/2609.29429)测试了TypeSafe的官方Jev能否检测迎合、欺骗、提示注入等异常行为。研究覆盖44个基准、7,193条实例。对适用二元问题的31个基准，通用问题的AUROC中位数为0.886，说明分数区分正负样本的排序能力较好；这个数不是88.6%的准确率。

Jev的机制也值得再说清。[官方文档](https://docs.typesafe.ai/introduction)定义的是：针对同一份输入，一次返回多个独立的类型化判断及概率，不先逐项写评语，再从文字里解析结论。这能减少多项检测重复调用的开销。论文对19个裁判评分基准按公开标价估算，Jev总成本0.30美元，原裁判合计18.96美元；约63倍的费用差只适用于这组实验。

更有用的发现是，排序有效不代表统一的0.5告警阈值也有效。论文发现概率与各任务的异常比例会偏离，部分任务直接使用0.5会漏报，需要任务内样本调整阈值。修改问法带来的收益有限；给模型什么参照信息往往更关键。例如检测泄密时，若不知道哪些信息应保密，单看一段回复就可能无法判断。

因此，这项研究支持的是低成本风险排序，再结合具体任务决定如何处置。测试主要使用2至7B模型的输出，部分基准标签也未独立验证；一些上下文增益依赖部署时未必拿得到的参照。[代码已公开](https://github.com/sumleo/RLCDAlignBench)，数据集需申请访问。这是对Jev用途的一次新评测，不是新的模型发布。

## 🤖 先写规划程序，再让程序处理机器人新场景

<!-- source-id: coding-agent-robot-programs -->

机器人 / 任务与运动规划 / 论文 · 8.5/10 · 建议深挖

另一篇9月24日提交的[研究](https://arxiv.org/abs/2609.30233)，把编码Agent用于机器人任务与运动规划：研究者给出任务描述和模拟器接口，让Agent自行试验、写代码，再把最终程序冻结，放到未见过的实例上测试。测试时不再调用大模型，运行的是已经写好的规划程序。

作者在28个模拟环境中评估了980个程序，每个测试100个新实例，共98,000次评估。在有手工规划器可对照的16个环境上，三种Agent配置的平均成功率为56%至95%，规划器为47%。主实验没有给Agent环境源代码，程序主要靠与模拟器交互形成；[仓库](https://github.com/tomsilver/robocode)也区分了严格黑箱与可读源代码的设置。

最有价值的地方，是把模型调用提前到“写出求解程序”这一步。同类任务反复出现时，可以重复运行普通代码，摊薄前期试错费用。论文报告每实例平均计算量明显低于规划器，但这个口径不包含前期程序合成，不能直接当作总体成本降低。

实验提供完整的对象状态，没有检验真实摄像头感知和硬件控制。复杂动态三维场景中的扫拢、倾倒等任务仍有明显失败。它提供了一种值得测试的分工：大模型负责开发策略，程序负责高频执行；距离通用实机控制仍有待验证的环节。

## 今天的主线

购物和企业软件的两条消息，都把AI接进现成的交易或工作环境。能推荐商品、生成代码，只解决了其中一段；零售商结账、企业托管、执行权限和持续费用，决定任务能否真正运行下去。

两篇论文则给出另一层判断：重复任务未必需要重复调用大模型。Jev把多个小判断合在一次输入里；机器人研究把昂贵试错放在前期，之后复用程序。做系统时可以先问，哪些部分需要模型每次重新判断，哪些可以提前算好、校准好或写进程序。省下的调用是否值得，最终仍要用任务成功率和完整成本来检验。

## 推荐阅读

优先读Jev论文中关于上下文和阈值的实验，再看机器人论文的冻结程序协议与失败案例。关注企业应用的读者可看Copilot公告里的托管与计费安排；Flipkart报道则适合观察AI购物究竟怎样接到真实交易。

## 原始资料

点击文末“阅读原文”，查看本期全部原始资料和论文。

- [TechCrunch：Flipkart结账测试](https://techcrunch.com/2026/09/26/google-tests-buying-from-walmart-owned-flipkart-through-gemini-and-ai-mode-in-india/)
- [同作者转载与发布时间](https://uk.finance.yahoo.com/news/google-tests-buying-walmart-owned-013000418.html)
- [微软：Home、Code与Autopilot](https://blogs.microsoft.com/blog/2026/09/25/introducing-the-new-copilot-with-home-code-and-autopilot/)
- [Just Ask Jev论文](https://arxiv.org/abs/2609.29429)
- [Jev评测HTML全文](https://arxiv.org/html/2609.29429v1)
- [RLCDAlignBench代码与数据说明](https://github.com/sumleo/RLCDAlignBench)
- [TypeSafe：Jev调用语义](https://docs.typesafe.ai/introduction)
- [编码Agent机器人规划论文](https://arxiv.org/abs/2609.30233)
- [机器人规划论文HTML全文](https://arxiv.org/html/2609.30233v1)
- [RoboCode代码与实验协议](https://github.com/tomsilver/robocode)

本文由AI辅助检索与整理。
