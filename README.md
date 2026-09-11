# Juju Radar

每日 AI 动态、论文和开源项目，附中文解读与原始链接。

**网站：[www.asteronline.cn/juju-radar](https://www.asteronline.cn/juju-radar/)**

- [每日精选 RSS](https://www.asteronline.cn/juju-radar/feed.xml)
- [论文 RSS](https://www.asteronline.cn/juju-radar/papers.xml)
- [Zotero 文献导出](https://www.asteronline.cn/juju-radar/papers.ris)

## 内容

`issues/` 只保存审核后的公开文章、引用来源及论文笔记。论文首次公开日期与收录日期分开记录；原始材料已阅读不等于独立复现。

`site/` 是不依赖第三方 Python 包的静态网站生成器。模板、数据、RSS 和 RIS 从同一份资料生成。

```sh
python3 site/scripts/package.py
```

需要 Python 3.11+、Git。产物写入 `site/dist/` 和 `release/`，不提交生成文件。生成的页面使用 `/juju-radar/` 路径前缀。

## 更新与部署

本地整理 → 内容审核 → 导出公开文件 → 敏感信息扫描 → 提交 → GitHub Actions 检查/构建 → GitHub Release → 网站服务器拉取。

PR 只运行检查。主分支更新且检查通过后，Actions 使用临时 GITHUB_TOKEN 发布静态包。服务器通过 GitHub 官方 Release Asset API 定期读取公开附件，无须配置 GitHub 或云平台密钥，也不依赖第三方下载代理。拉取器核对提交、文件清单和哈希，拒绝路径穿越、符号链接和非静态文件；不执行下载的代码。每次覆盖前保留上一版文件，首页最后替换。

服务器安装方式（路径由部署者自行指定）：

```sh
python3 ops/pull-release.py --repo juju-w/juju-radar --root /srv/juju-radar --state /var/lib/juju-radar-updater
```

拉取器由管理员单独安装，仓库更新不会自动替换服务器上的拉取程序。建议以仅能写入网站目录的独立用户运行，每五分钟检查一次。网络或校验失败时继续服务现有页面。

## 内容更正

欢迎通过 Issues 或 PR 指出错误并附原始来源。仓库与网站内容由 AI 辅助整理。

## 音乐播放器

播放器代码位于 `site/assets/music/`，随网站发布。音频、封面及曲目清单独立部署到网站根目录的 `music-v1/`，不进入 Git 或 GitHub Release；缺少曲目清单时网站保留正常阅读页面。播放器使用同源阅读框架，站内跳转时保持播放，首次访问尝试自动播放，受浏览器策略限制时显示播放按钮。

媒体清单 `music-v1/playlist.json` 为数组，每项包含 `title`、`artist`、`album`、`track`、`duration`、`url`、`cover`。默认专辑为 `Misty for Direct Cutting`。音乐按需加载，服务器应支持音频 Range 请求。更新器仅覆盖发布清单内的文件，不删除独立媒体目录。

液态玻璃效果使用 [deepika-builds/liquid-glass](https://github.com/deepika-builds/liquid-glass)，MIT 许可已保留在脚本中；Chromium 使用 SVG 折射，其他浏览器使用模糊回退。

## 特别版与深度解读

重大报告与专题分析单独发布到“深度解读”，并在收录当天的精选列表显示一个特别版入口。同日每日精选保持独立，两篇各有固定地址及 RSS 条目。

特别版目录使用 `issues/YYYY-MM-DD-topic/`；公开元数据包含 `date`、`issue_id`、`kind: special`、`section`、带时区的 `published_at` 和来源。目录标识决定链接，日期用于往期分组；不能用特别版覆盖同日目录。经核验的报告可以用 `item_type: report` 收入文献库，相关期次指回特别版。所有内容仍经公开文件白名单、敏感信息扫描与构建检查后发布。

## 双语导读

`site/reading-guides.json` 保存本站撰写的英文摘要与对应中文，构建到 `guides/`。专题文章和原始资料页自动添加入口；导读提供语言切换、分享及官方 PDF 页码导航，不增加一条重复的每日精选或 RSS 条目。

目前导读是原创摘要，不是报告原文或全文翻译。第三方报告全文、完整译文及图表不随网站发布；版权声明不能代替转载和翻译授权。报告全文请通过页面所附的官方链接阅读。
