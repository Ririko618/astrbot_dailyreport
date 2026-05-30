# 日报插件 (astrbot_dailyreport)

✨ 基于 AstrBot 的可定制化日报插件 ✨

每日自动汇总最新资讯，生成精美的日报图片。支持自定义名称、角色形象、主题颜色，一切皆可配置。

> 💙 作者是锦依卫，因此默认角色为洛天依，默认配色为天依蓝。另保留fork来源的绪山真寻角色，如需其他角色请自行上传配置。

## 📖 介绍

每日汇总以下内容，生成一张精美图片：

- 📺 **今日新番** — Bangumi 番剧日历
- 🔥 **B站热点** — B站热搜词
- 🌍 **60s读懂世界** — 国际新闻简报
- 💻 **IT资讯** — IT之家 RSS
- 🐟 **摸鱼日历** — 节假日倒计时
- 📜 **每日古诗词** — 经典古诗词

## 💿 安装

### 通过 AstrBot 插件市场安装（推荐）

1. 在 AstrBot WebUI 中打开插件市场
2. 搜索 `astrbot_dailyreport` 或 `日报插件`
3. 点击安装

### 手动安装

```bash
cd AstrBot/data/plugins
git clone https://github.com/Ririko618/astrbot_dailyreport
cd astrbot_dailyreport
pip install -r requirements.txt
playwright install chromium
```

## 🆚 与源仓库的区别

本项目 fork 自 [astrbot_plugin_zhenxunribao](https://github.com/luminacry/astrbot_plugin_zhenxunribao)，主要改进：

- **自定义角色**：支持 WebUI 上传或 `res/role/` 文件夹添加新角色，随机选择 PNG 立绘
- **主题配色**：5 套中文命名配色（天依蓝/樱花粉/典雅紫/初音绿/暖阳橙）
- **每日古诗词**：替换原文的今日一言
- **时区配置**：14 个常用时区下拉选择
- **AI 问候**：`/日报` 命令支持 LLM 生成个性化问候

## ⚙️ 配置

在 AstrBot WebUI 的插件配置页面进行配置：

| 配置 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `report_name_cn` | string | `天依日报` | 日报标题 |
| `character` | 下拉选择 | `洛天依` | 日报角色，对应 `res/role/` 下的文件夹 |
| `character_upload` | 文件上传 | `[]` | 导入新角色：上传 1 个 MD 人格文件 + 若干 PNG 图片，MD 文件名即为角色名 |
| `theme` | 下拉选择 | `天依蓝` | 日报配色：天依蓝 / 樱花粉 / 典雅紫 / 初音绿 / 暖阳橙 |
| `timezone` | 下拉选择 | `Asia/Shanghai` | 时区，用于定时推送和问候语判断，共 14 个常用时区 |
| `api_token` | string | `""` | ALAPI Token，用于节假日、每日古诗词、早报 API |
| `max_anime_count` | int | `4` | 今日新番最大数量，建议 4-8 |
| `max_news_count` | int | `5` | 新闻最大数量，建议 5-10 |
| `max_hotword_count` | int | `4` | B站热点最大数量，建议 4-8 |
| `max_holiday_count` | int | `3` | 摸鱼日历最大数量，建议 3-5 |
| `render_dpr` | int | `5` | 渲染清晰度，越大越清晰但更慢，建议 3-6 |
| `enable_scheduled_push` | bool | `false` | 是否启用定时推送 |
| `scheduled_push_time` | string | `"08:00"` | 定时推送时间，HH:MM 格式 |
| `scheduled_push_groups` | list | `[]` | 推送目标群号，如 `["123456789"]` |
| `enable_ai_greeting` | bool | `false` | 启用 AI 生成个性化问候语，`/日报` 和定时推送均生效 |

### 导入 / 更新角色

**新增角色：**
1. 准备一个 `.md` 文件（角色人格描述）和若干 `.png` 图片（角色立绘）
2. 在 WebUI 配置页的「导入新角色」中上传这些文件
3. 保存配置并重启插件
4. 插件会自动将文件归入 `res/role/{角色名}/`，并在角色下拉框中出现新选项
5. 每次生成日报时会从该角色的 PNG 图片中**随机选择一张**

**更新已有角色：**
- 上传**同名 MD 文件**会覆盖旧人格描述
- 上传**新 PNG 图片**会添加到角色图库，不上传同名 PNG 则保留原有立绘

> **MD 文件格式参考** (`res/role/洛天依/洛天依.md`)：
> ```markdown
> # 角色名
> ## 身份
> ...
> ## 性格
> ...
> ## 口吻
> ...
> ```

## 🎁 使用

```
/日报          — 手动生成日报（会先发送问候语再发图片）
/日报群组ID    — 获取当前会话标识，用于定时推送配置
```

## 📋 依赖

- `aiohttp>=3.8.0`
- `jinja2>=3.0.0`
- `playwright>=1.40.0`
- `zhdate>=0.1`

安装后需执行：`playwright install chromium`

## ⚠️ 注意事项

1. **API Token**：节假日、古诗词、早报需要配置 ALAPI Token
2. **Playwright**：首次使用需安装 Chromium 浏览器
3. **角色导入**：必须包含至少一个 `.md` 人格文件，文件名决定角色名

## 📄 许可证

AGPL-3.0

## ❤ 致谢

- [nonebot-plugin-zxreport](https://github.com/HibiKier/nonebot-plugin-zxreport) — 原始项目
- [astrbot_plugin_zhenxunribao](https://github.com/luminacry/astrbot_plugin_zhenxunribao) — AstrBot 移植版本（本项目的 fork 来源）
- [AstrBot](https://github.com/AstrBotDevs/AstrBot) — 机器人框架
- [ALAPI](https://www.alapi.cn/) — API 服务
- [Bangumi](https://bgm.tv/) — 番剧数据
- [bangumi-proxy](https://github.com/Yuri-NagaSaki/bangumi-proxy) — 番剧 API 反代服务
