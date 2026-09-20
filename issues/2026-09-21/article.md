---
title: ChatGPT 广告 Cookie 被指跨站关联，Step 5 Preview 上线
author: Juju Radar
summary: Step 5 Preview与Qwen-Image-2.1同日上线；一项独立调查追踪ChatGPT广告Cookie的跨站行为。
sourceUrl: https://www.asteronline.cn/juju-radar/2026-09-21/
sourceNote: 检索窗口为北京时间9月20日07:00至21日07:00。Step与Qwen原始页面仅标9月20日，小时级边界未确认；Cookie调查在窗口内发布。评分为编辑判断。HF周末列表为空或暂不可用，论文巡检另用arXiv与项目页补查。
---

# ChatGPT 广告 Cookie 被指跨站关联，Step 5 Preview 上线

<!-- reading-stats -->约 2,100 字 · 阅读约 8 分钟<!-- /reading-stats -->

Juju Radar · 2026 年 9 月 21 日

## 本期导读

今天三条内容都和“边界”有关。Step 5 Preview 想把长任务能力压到更低的调用成本；Qwen-Image-2.1 把生成、编辑和透明图片放进同一套模型；一项独立调查则追问，ChatGPT 的广告测量会不会把站内身份带到第三方网站。

模型能力和开放范围不能只看一句宣传。API 能调用，不等于权重已经开放；权重能下载，也不等于可以自由商用。广告测量组件已经存在，也不等于研究者提出的全部账号关联路径都得到了官方确认。

## 🚀 Step 5 Preview 上线：600B 总参数，每次只激活 27B

基础模型 / Agent · 9.2/10 · 建议深挖

阶跃星辰发布 Step 5 Preview，定位是编程、软件工程、专业知识工作和金融分析。模型采用稀疏混合专家架构，总参数6000亿，每个 token 激活270亿，支持100万 token 上下文和视觉输入。9月20日已经可以通过阶跃平台和 Vercel AI Gateway 调用。

这里最值得看的不是“6000亿”这个总数，而是每次实际动用多少参数。27B 的激活量有助于控制推理成本。Vercel 当前列出的价格是每百万 token 输入1美元、输出2.7美元，缓存读取0.05美元；这说明产品主张很明确：不靠全面领先，而是把较强的长任务能力压到更低价格。

官方成绩也留下了清楚的边界。Step 5 Preview 在 DeepSWE v1.1 得67.7，低于 GPT-6 Astra 的74.1和 Claude Opus 5的74.0；Terminal-Bench v4只有33.3，也低于 Astra的57.9和 Opus 5的52.3。金融评测表现更强，但其中不少是官方自建基准，协议和题目分布仍需外部复核。

目前开放的是预览版服务。官方中文发布称完整权重计划10月15日开放，因此今天还不能把它写成“已经开源”。后续应看三件事：权重是否按期交付、长任务稳定性、以及同等预算下的第三方复测。

## 🎨 Qwen-Image-2.1 开放权重，但商业使用要另谈许可

图像生成 / 开放权重 · 9/10 · 建议深挖

Qwen-Image-2.1 把文生图和指令编辑放进同一模型，视觉生成部分为70亿参数，支持原生2K、最多10张参考图，以及带透明通道的 RGBA 图片。它还提供两个独立的 Qwen3.5-VL 9B 提示词改写模型，分别服务生成和编辑。

这次发布的完成度比单独放一个 checkpoint 更高。Diffusers、ComfyUI、vLLM-Omni、SGLang 和 LightX2V 都在首日给出适配；代码中还说明，多图编辑时可以把文字和条件图的前缀缓存下来，在后续去噪步骤复用。对真正部署模型的人，这些入口比官方展示图更有价值。

“70亿参数”只指视觉生成组件，并不等于整条推理管线只有70亿参数：条件编码器仍使用 Qwen3-VL 8B。官方示例通常跑40步，本期没有独立测试显存、速度和复杂中文排版质量，官方展示也不能替代盲测。

还有一个容易被“开源”二字遮住的细节：权重采用 Qwen Research License，只允许非商业研究或评估。商业使用需要另行取得许可。因此更准确的说法是“开放权重和代码”，而不是不加限定地称为开源模型。

## 🍪 ChatGPT 广告 Cookie 被指可以跨站关联浏览行为

隐私 / 广告基础设施 · 8.8/10 · 持续观察

一名独立研究者在 Android Chrome 上分析 ChatGPT 的广告测量流程，焦点是一枚名为 __obi 的 Cookie。研究者观察到，ChatGPT 会把一个短时同步令牌交给 bzr.openai.com，随后设置有效期一年的 __obi；当第三方网站加载 OpenAI 广告像素时，浏览器会在相关跨站请求中带上它。

OpenAI 自己的 Cookie 政策确实列出了 __obi，把它归为分析 Cookie，有效期一年。OpenAI 的转化测量文档也确认广告主可以安装 Pixel，并用 oppref 和转化事件衡量广告效果。这些官方材料确认了组件存在，但没有直接解释研究者所说的账号关联范围。

这项调查不能被写成“OpenAI 已被证明读取所有人的全部网页”。研究者只在 Android Chrome 上复现，约五次 ChatGPT 会话中一次出现同步令牌；iOS 浏览器会拦截这类第三方 Cookie，桌面 Chrome 没有测试。更关键的是，研究者看到收集端接受了带 Cookie 的事件，但没有直接观察 OpenAI 服务端最后怎样把数据合并到账户。

争议点仍然成立：普通广告平台做跨站转化测量并不新鲜，但聊天产品保存着更敏感的上下文。如果同一个稳定标识同时接触站内身份和站外转化事件，用户需要知道收集范围、保留时间和退出方式。研究者称 OpenAI 支持团队已收下问题，尚未给出针对这套机制的技术说明。

## 今天的主线

今天最值得留意的是“开放”这个词正在被拆得越来越细。Step 5 Preview 已经开放 API，但权重仍是未来承诺；Qwen-Image-2.1 已经提供权重和代码，却使用非商业研究许可。判断一个模型能不能真正进入自己的工作流，需要分别看服务、权重、代码、许可证和部署支持。

另一条线来自广告系统。AI 产品开始接入成熟的转化测量技术后，用户面对的不再只是聊天记录怎样保存，还包括站外行为能否与站内身份发生联系。这里需要的不是一句“和其他广告平台一样”，而是可核查的数据流、退出选项和服务端用途说明。

## 推荐阅读

先读 **Qwen-Image-2.1 的许可证**，它能最快说明“开放权重”和“自由商用”的差别；接着看 **Step 5 Preview 的评测表**，重点比较它没有领先的项目。对隐私问题感兴趣，再读 **__obi 调查的限制部分**，把实测、推断和官方确认分开。

## 原始资料

点击文末“阅读原文”，查看本期全部官方页面、代码和调查材料。

- [阶跃星辰：Step 5 Preview 官方页面](https://www.stepfun.com/step-5-preview)
- [阶跃星辰：开放平台](https://platform.stepfun.com/)
- [Vercel：Step 5 Preview 模型页与价格](https://vercel.com/ai-gateway/models/step-5-preview)
- [阶跃星辰：中文发布](https://mp.weixin.qq.com/s?__biz=MzkyNTYxNzg5Mg%3D%3D&mid=2247488120&idx=1&sn=8ba9ac7f0b36682d6262290677c665da)
- [Qwen：Qwen-Image-2.1 官方博客](https://qwen.ai/blog?id=qwen-image-2.1)
- [Qwen-Image-2.1：代码与使用说明](https://github.com/QwenLM/Qwen-Image-2.1)
- [Qwen-Image-2.1：模型权重](https://huggingface.co/Qwen/Qwen-Image-2.1)
- [Qwen Research License](https://github.com/QwenLM/Qwen-Image-2.1/blob/main/LICENSE)
- [独立调查：ChatGPT 广告收集器与 __obi](https://www.buchodi.com/chatgpt-now-knows-what-you-do-on-other-websites-via-ad-collector)
- [OpenAI Cookie 政策](https://openai.com/en-GB/policies/cookie-policy/)
- [OpenAI 转化测量说明](https://help.openai.com/en/articles/20001409-conversion-measurement)
- [OpenAI Pixel 配置说明](https://github.com/openai/plugins/blob/main/plugins/openai-ads-conversions/skills/openai-ads-conversions-setup/references/measurement-pixel.md)

本文由 AI 辅助检索与整理。模型评测与产品能力来自原始材料，尚未独立复现。
