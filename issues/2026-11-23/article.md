---
title: OpenRouter调整零留存路由，黎曼证明复现同一份导出
author: Juju Radar
summary: OpenRouter移除125个端点的零数据留存资格。黎曼证明在另一台机器隔离重建后，导出逐字节一致。KoboldCpp新版本接入本地语音转写与字幕对齐。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-23/
sourceNote: 检索窗口为北京时间11月22日07:00至23日07:00。OpenRouter原公告仅刊日期，有窗口内公开记录旁证。黎曼条目采用MIT核验页新快照和con-ron日志。KoboldCpp按GitHub发行时间。无补看。
editorialStatus: reviewed
---

# OpenRouter调整零留存路由，黎曼证明复现同一份导出

<!-- reading-stats -->约 1,600 字 · 阅读约 6 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 23 日

## 本期导读

OpenRouter 在一轮推理服务调查后，取消了 125 个端点的零留存资格。黎曼猜想的 Lean 证明换了一台机器重建，得到与原版逐字节一致的证明导出。KoboldCpp 则把语音转写和逐词时间对齐接进同一套本地工具。

## 🔒 OpenRouter 移除 125 个推理端点的零留存资格
<!-- source-id: openrouter-zdr-audit -->

**真实事故 / 推理数据 · 9/10 · 建议深挖**

OpenRouter 在 11 月 22 日披露，调查后将三家推理服务商从平台下架，并取消了 125 个端点的零数据留存（ZDR）资格。其中一部分端点是出于预防被移除。平台称，研究人员的发现涉及具体推理服务商，未发现 OpenRouter 自身系统被入侵的证据。OpenRouter 表示已通知可能受影响的客户，并开始核验请求和响应是否被转发给第三方。

Novita 的公告解释了实际处理链怎么发生变化。该公司确认，一条原本只为特定客户设置的路由被更广泛地使用，部分 MiniMax 请求转发到了 MiniMax 官方 API。Novita 称，5 月 28 日至 11 月 11 日经它处理的相关请求内容可能被第三方访问或留存，既包括直连，也包括经 OpenRouter 路由的请求。此轮集中公告还链接了 Together 的测试样本泄露和 Phala 的初步报告，两起事件各有自己的影响范围。

零留存设置会改变请求可以走哪些端点。严格选用 ZDR 的应用会少一批候选路由，直到相关端点通过复核。对处理客户文件、内部代码或会议记录的团队，同一个模型名下有哪些实际处理方、请求能否被继续转发，比只查平台是否勾选了 ZDR 更能说明数据经过哪里。

[OpenRouter 公告](https://openrouter.ai/blog/announcements/data-processing-incidents-on-inference-providers/) · [Novita 隐私通知](https://novita.ai/blog/minimax-requests-privacy-notice/) · [Together 事件说明](https://www.together.ai/blog/security-event-prompt-leakage-for-requests-in-june-and-july-of-2026) · [Phala 初步报告](https://phala.com/posts/phala-november-preliminary-incident-report) · [零留存路由规则](https://openrouter.ai/docs/guides/features/zdr)

## 🔢 黎曼猜想的 Lean 证明经隔离重建复现同一份导出
<!-- source-id: riemann-rebuild-export -->

**AI for Science / 数学 · 8.5/10 · 建议深挖**

MIT 数学家 Andrew Sutherland 更新了核验记录。他在另一台机器上用只读源码、断网的沙箱重新构建原作者公开的 Lean 工程。按照日志，约 61.6 GB 的证明导出与最初版本字节数相同，SHA-256 摘要也一致。验证者因此可以确认，两种构建环境交给证明检查器的是同一份数据。17 万余个单独的编译文件中仍有一个因构建结果不确定而出现字节差异，差异没有传到最后的证明导出。

还有一项新增核验检查的是证明到底回答了什么。con-ron 是 con-leche 的 Rust 移植版。它用分别准备的目标文件做比对，通过了五个主命题，也通过了前一期提到的两条约数和命题。新日志补强了复现与目标核对，证明的命题范围仍与此前一致。Sutherland 的报告还标明，完整的 Comparator 流程与 Lean 官方内核直接重放导出的任务仍在运行。

[MIT 核验报告](https://math.mit.edu/~drew/grh/) · [隔离重建日志](https://math.mit.edu/~drew/grh/sandbox-timeline.txt) · [五条主命题比对](https://math.mit.edu/~drew/grh/con-ron-compare.log) · [约数和命题比对](https://math.mit.edu/~drew/grh/arith-con-ron-compare.log)

## 🎙️ KoboldCpp 接入本地语音转写和逐词对齐
<!-- source-id: koboldcpp-local-align -->

**语音 / 开源工具 · 7.5/10 · 持续观察**

KoboldCpp v1.125.1 把 Qwen3ASR、SenseVoice 两类语音识别接进本地运行时，也新增 MMS 和 Qwen3 的强制对齐模型。转写先将录音变成文字，对齐再用文字在原音中定位对应的时间片段。两步接起来，访谈或课程录音就能生成带词级时间戳的文本，读者可从字幕直接跳回对应的原音。

这次交付的价值在于把识别和精确定位接成一条可在本地运行的流程。发行说明没有公布噪声和混合语言下的对齐误差。多人重叠讲话、有漏词或不同语言混说的录音，仍需抽查转写和时间戳。

[KoboldCpp 发行说明](https://github.com/LostRuins/koboldcpp/releases/tag/v1.125.1) · [转写模型目录](https://huggingface.co/koboldcpp/whisper/tree/main/audiocpp-asr) · [对齐模型目录](https://huggingface.co/koboldcpp/whisper/tree/main/audiocpp-aligner)

## 今日主线

当结果要交给别人复用，核验往往需要追溯到中间环节。推理请求要能追到实际服务端点，数学结论要能追到可复现的证明导出，字幕要能追到原录音的位置。这些记录给后续复查提供了具体的落点。

## 推荐阅读

处理敏感数据的团队可先看 OpenRouter 公告和 Novita 披露的请求范围。关注黎曼猜想的读者可以对照 MIT 的重建日志与目标比对日志，看两者分别核查了什么。

## 原始资料

点击文末“阅读原文”，查看本期全部来源和项目链接。

*Juju Radar · AI 辅助整理，供研究与阅读参考。*
