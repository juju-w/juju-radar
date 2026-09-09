# Juju Radar

每日 AI 动态、论文和开源项目，附中文解读与原始链接。

**网站：[happy.asteronline.cn/juju-radar](https://happy.asteronline.cn/juju-radar/)**

- [每日精选 RSS](https://happy.asteronline.cn/juju-radar/feed.xml)
- [论文 RSS](https://happy.asteronline.cn/juju-radar/papers.xml)
- [Zotero 文献导出](https://happy.asteronline.cn/juju-radar/papers.ris)

## 内容

`issues/` 只保存审核后的公开文章、引用来源及论文笔记。论文首次公开日期与收录日期分开记录；原始材料已阅读不等于独立复现。

`site/` 是不依赖第三方 Python 包的静态网站生成器。模板、数据、RSS 和 RIS 从同一份资料生成。

```sh
python3 site/scripts/package.py
```

需要 Python 3.11+、Git。产物写入 `site/dist/` 和 `release/`，不提交生成文件。生成的页面使用 `/juju-radar/` 路径前缀。

## 更新与部署

本地整理 → 内容审核 → 导出公开文件 → 敏感信息扫描 → 提交 → GitHub Actions 检查/构建 → GitHub Release → 网站服务器拉取。

PR 只运行检查。主分支更新且检查通过后，Actions 使用临时 GITHUB_TOKEN 发布静态包。服务器定期读取公开 Release，无须配置 GitHub 或云平台密钥。拉取器核对提交、文件清单和哈希，拒绝路径穿越、符号链接和非静态文件；不执行下载的代码。每次覆盖前保留上一版文件，首页最后替换。

服务器安装方式（路径由部署者自行指定）：

```sh
python3 ops/pull-release.py --repo juju-w/juju-radar --root /srv/juju-radar --state /var/lib/juju-radar-updater
```

拉取器由管理员单独安装，仓库更新不会自动替换服务器上的拉取程序。建议以仅能写入网站目录的独立用户运行，每五分钟检查一次。网络或校验失败时继续服务现有页面。

## 内容更正

欢迎通过 Issues 或 PR 指出错误并附原始来源。仓库与网站内容由 AI 辅助整理。
