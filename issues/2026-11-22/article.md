---
title: Transformers统一缓存接口，黎曼证明核验扩展到约数和
author: Juju Radar
summary: Transformers 5.24 统一注意力与递推模型的生成缓存接口，并支持 Inkling 2 Mini 等新架构。黎曼猜想的独立核验新增 Robin 与 Lagarias 两条约数和不等式。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-22/
sourceNote: 检索窗口为北京时间11月21日07:00至22日07:00。两条为窗口内实质更新。Inkling权重发布早于窗口，作为Transformers新集成的背景。黎曼猜想条目为MIT核验页11月21日12:55 UTC新增约数和结论。无补看。AI HOT接口失败，HF截止日接口不可用，已直接查验官网、论文列表与版本记录。
editorialStatus: reviewed
---

# Transformers统一缓存接口，黎曼证明核验扩展到约数和

<!-- reading-stats -->约 1,300 字 · 阅读约 5 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 22 日

## 本期导读

Transformers 发布 5.24，给注意力模型和递推模型用上了同一个缓存接口，并正式支持会反复运行中间层的 Inkling 2 Mini。黎曼猜想的独立核验也有进展。研究者用同一份 Lean 证明，推导出两条可以直接用整数约数和表述的不等式。

## ⚙️ Transformers更新缓存接口，正式支持循环层模型
<!-- source-id: transformers-524 -->

**开源工具 / 推理框架 · 8.5/10 · 建议深挖**

普通注意力模型在生成时缓存历史词元的键和值，递推模型则保存每步更新后的状态。以前 Transformers 分别叫它们 `past_key_values` 和 `cache_params`，混合架构的调用代码得兼顾两种名称。5.24 在模型前向、生成和相应输出中统一用 `cache`。旧名称暂时仍兼容，外部自定义缓存或依赖旧多模态输出类的代码需要核对迁移项。

这次也正式加入了 Inkling 2 Mini 和 NVIDIA Dory 等模型。以 Inkling 2 Mini 为例，网络实际有 24 层，其中间 12 层沿同一组权重运行三次。因此权重只需存一份，每个词元仍要多做两遍这部分计算。模型卡给出的低比特检查点大小约为 20 GB，Transformers 发行说明称其低比特层会在加载时反量化。部署前需要分别测下载体积、实际峰值内存与生成速度。权重在本期之前已公开，窗口内新增的是框架正式发包和这组架构支持。

[Transformers 发行说明](https://github.com/huggingface/transformers/releases/tag/v5.24.0) · [PyPI 版本](https://pypi.org/project/transformers/5.24.0/) · [循环架构文档](https://huggingface.co/docs/transformers/v5.24.0/en/model_doc/inkling2_loop) · [Inkling 2 Mini 模型卡](https://thinkingmachines.ai/model-card/inkling-2-mini/)

## 🔢 黎曼证明的独立核验新增两条约数和不等式
<!-- source-id: riemann-divisor-check -->

**AI for Science / 数学 · 8.5/10 · 建议深挖**

昨天的特别版讲了 Claude 怎样参与构造这份证明。11 月 21 日的更新落在另一端。MIT 数学家 Andrew Sutherland 把同一份 Lean 证明接到独立维护的 Robin1984 项目，得到 Robin 和 Lagarias 两条约数和不等式。约数和就是把所有正约数加起来，例如 6 的正约数是 1、2、3、6，合计 12。Robin 判据给每个大于 5040 的整数规定了一个随整数变化的上限，Lagarias 判据则用调和数为所有正整数写出另一条上限。

这两条判据与经典黎曼猜想等价，早已为人所知。此次新公开的是一条从原证明接到这两条整数命题的完整形式化推导。核验者准备了只依赖 Mathlib 的目标文件，单独写下两条约数和不等式，再检查导出的联合证明。报告显示，独立内核 con-leche 和 nanoda 接受了联合证明，con-leche 也核对了目标，公理记录仅列 Lean 的三条标准公理。联合导出的另一套完整 Comparator 流程当时仍在运行，克雷数学研究所的题目页仍标为未解决。

[核验更新](https://math.mit.edu/~drew/grh/) · [不等式目标文件](https://math.mit.edu/~drew/grh/ArithChallenge.lean) · [公理记录](https://math.mit.edu/~drew/grh/arith-audit.log) · [nanoda 日志](https://math.mit.edu/~drew/grh/arith-nanoda.log) · [Lagarias 原论文](https://arxiv.org/abs/math/0008177) · [克雷数学研究所](https://www.claymath.org/millennium/Riemann-Hypothesis/)

## 今日主线

开源框架和形式化数学都要把已有成果接到可复用的入口上。对生成框架，统一的缓存对象让同一段代码可以接入不同模型。对证明，已知等价性让核验者可以改用约数和这种直接可读的目标。可复用的接口把后续工作变得明确。工程师能按真实后端测内存和速度，数论读者能看清楚这条证明对整数给出了什么保证。

## 推荐阅读

先看 Transformers 发行说明里的旧接口兼容与反量化，再对着 Sutherland 的目标文件读两条约数和不等式。

## 原始资料

点击文末“阅读原文”，查看本期全部来源、论文和项目链接。

*Juju Radar · AI辅助整理，供研究与阅读参考。*
