---
title: 蚂蚁灵波让机器人复用地图，KVAE 开放新版视频编码器
author: Juju Radar
summary: LingBot-Map 2.0 把纠偏结果写回空间记忆，LingBot-Navi 用这份记忆规划路线。KVAE 3.0 公开图像和视频权重，小鹏在广州车展部署八台 IRON。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-11-28/
sourceNote: 检索窗口为北京时间11月27日07:00至28日07:00。LingBot按27日正式配套发布核对，部分工件早已可见。KVAE图像与视频权重在27日上传，立体声音频权重更早。无补看。
editorialStatus: reviewed
---

# 蚂蚁灵波让机器人复用地图，KVAE 开放新版视频编码器

<!-- reading-stats -->约 1,600 字 · 阅读约 6 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 11 月 28 日

## 本期导读

蚂蚁灵波给出两组对照：地图发生漂移时，把纠偏写回模型内部能降多少误差，只换地图能给导航带来多少收益。Kandinsky Lab 开放 KVAE 3.0 的图像和视频权重，把压缩后还能保留哪些信息单独拿来测。小鹏则让八台 IRON 在同一个展厅接待观众，并公布香港研发中心。

## 🗺️ LingBot 把地图纠偏写回记忆，导航能接着用
<!-- source-id: lingbot-memory -->

**机器人 / 地图与导航 · 9.5/10 · 建议深挖**

用一个摄像头边走边建图时，前几帧的小误差可能一路累积。同一扇门从两边看，也可能被模型记到两个位置。LingBot-Map 2.0 平时沿着视频逐帧更新。需要纠偏时，模型让上半部分网络重新对照选中的关键帧，再把修正写回自己的缓存。后续帧能直接沿用纠偏后的空间信息。

在作者的 VBR 长轨迹评测中，1.0 版的轨迹误差是 31.12 米，2.0 纯流式版是 17.01 米，加入纠偏后是 4.72 米。三组数字来自同一张对照图。目前配套开放的是纯流式几何基座，4.72 米对应的完整纠偏权重尚未核到公开。

导航模型 LingBot-Navi 把看过的物体和三维位置存进带语义特征的点云。第二次接到找东西的任务，它可以先从已有记忆定位，再让局部控制器用当前画面执行路线。论文固定 Navi 权重，只更换地图模型，两组评测的成功率分别提高 4.15 和 2.35 个百分点。这是模拟评测的增益。真实场地里物体被挪动以后，原有记忆会不会帮倒忙，仍需要用多次到访的任务检验。

[蚂蚁灵波正式公告](https://via.tt.se/pressmeddelande/4660319/robbyant-open-sources-lingbot-map-20-and-lingbot-navi-enabling-long-term-spatial-memory-and-autonomous-navigation-for-robots?lang=en&publisherId=259167) · [地图技术报告](https://github.com/Robbyant/lingbot-map-v2/blob/main/docs/lingbot-map-v2_paper.pdf) · [导航技术报告](https://github.com/Robbyant/lingbot-navi/blob/main/tech_report/Scene-aware%20Navigation%20with%20Spatial%20Memory.pdf) · [纯流式地图项目](https://github.com/Robbyant/lingbot-map-v2) · [导航权重](https://huggingface.co/robbyant/lingbot-navi) · [导航数据集](https://huggingface.co/datasets/robbyant/LingBot-Navi)

## 🎞️ KVAE 3.0 压小视频表示，并保留供生成模型使用的线索
<!-- source-id: kvae-latent -->

**视觉视频 / 多模态编码 · 8.5/10 · 建议深挖**

扩散模型通常在压缩后的表示里生成画面。Kandinsky Lab 的新版视频编码器把横纵方向的压缩率从 16 倍提到 32 倍，时间仍压缩 4 倍，通道从 64 增到 128。空间网格缩到原来的四分之一，通道加倍，同一段视频的表示元素总数约减半。训练时，作者还让压缩后的内容对齐预训练视频模型提取的特征，希望细节被压缩后仍能保留对生成有用的信息。

在团队报告的 MCL-JCV 720p 重建测试中，KVAE-3D-3.0 的感知距离 LPIPS 为 0.161，低于 MiniMax-H3 编码器的 0.176。逐像素误差相关的 PSNR 则是 32.26 dB，低于 H3 的 32.44 dB。这组结果提醒人们，把输入视频还原得多像，和把压缩表示交给扩散模型后能生成得多好，可以分开测。文章里的生成对照还用了不同的分块和通道数，表示变小也无法直接换算为整条流水线的加速。

同批技术说明还介绍了立体声音频编码。它把左右声道一起处理，让压缩表示保留两声道的关系。这部分权重早于本次图像和视频权重发布。

[技术说明与评测](https://huggingface.co/blog/kandinskylab/kvae-3) · [视频权重](https://huggingface.co/kandinskylab/KVAE-3D-3.0) · [项目代码](https://github.com/kandinskylab/kvae) · [权重合集](https://huggingface.co/collections/kandinskylab/kvae-30)

## 🤖 小鹏让八台 IRON 上展台，香港研发中心正式成立
<!-- source-id: xpeng-iron-guangzhou -->

**公司战略 / 具身部署 · 8/10 · 建议深挖**

小鹏公布，广州车展安排八台 IRON 在展台承担迎宾、导览和车辆讲解。公司描述的服务流程包括用语音或应用建任务、低电量补电、充满后回到岗位，以及上报异常。同日宣布成立的香港研发中心位于香港科学园，聚焦机器人与通用智能，并将与深圳、广州的研发团队协作。小鹏把海外部署安排在 2027 年下半年。

展台给出了一个可重复观察的场景。除了看机器人完成一次讲解，还可以看它接下下一项任务前等了多久，补电后能否续跑，遇到人群变化时需不需要接管。小鹏暂未公布连续运行时数、人工接管率或单台运营成本。家庭和商业部署仍有不同的场地与验收要求。

[小鹏车展公告](https://www.xiaopeng.com/news/company_news/5627.html)

## 今日主线

一次走对路或生成一段清晰画面，说明的是单次输出。任务能不能接着做，取决于中间状态留下了什么。地图纠偏要能被下一次规划读到，压缩后的视频表示要留下生成所需的线索。到了展厅，还要知道机器人补完电后能否回到原来的任务。这些环节需要在连续任务里测。

## 推荐阅读

先看 LingBot 两份报告的纯流式与纠偏对照，以及固定 Navi 权重的换图实验。做视频生成可接着看 KVAE 的重建表，再对照下游生成所用的分块方式。

点击文末“阅读原文”，查看本期全部来源、论文和项目链接。

Juju Radar · AI 辅助整理
