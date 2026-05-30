# Changelog

## 1.0.0 - 2026-05-30

### Added
- 日报名称、角色、主题色均支持 WebUI 下拉配置，不再硬编码
- 角色系统：`res/role/{角色名}/` 文件夹结构，启动自动扫描，写入选项
- WebUI 文件上传导入角色：上传 MD 人格文件 + PNG 图片，自动归入角色文件夹
- 5 套主题配色：天依蓝（默认）、pink、purple、初音绿、orange，一键切换
- 每日古诗词模块，替换原有今日一言（API：`v3.alapi.cn/api/shici`）
- 番剧 API 备用地址 `bgmapi.anibt.net`，主地址不可用时自动切换
- `/日报` 命令支持 AI 问候语（需开启 `enable_ai_greeting`）
- 角色图片随机选择：每天从角色 PNG 中随机选一张

### Changed
- 插件注册名改为 `astrbot_dailyreport`，版本重置为 1.0.0
- 模板重构：CSS 变量去颜色化，布局优化，去除英文副标题和页脚版权
- 番剧封面仅使用 `images.common`，HTTP 自动升级 HTTPS
- 番剧卡片改用 flexbox 均匀分布，图片加载改为等待全部完成
- 摸鱼日历与 B 站热点面板高度自适应，以较高者为准
- 角色图片宽度 120px 等比缩放，头部三元素垂直居中
- 兜底番剧图片改为自包含 SVG data URI，不再依赖本地文件

### Removed
- 英文日报名称 `report_name_en` 配置项
- 页脚版权文案及对应 CSS
- 今日一言模块，替换为每日古诗词

### Fixed
- 番剧 API 返回 HTTP 图片导致 Playwright 无法加载的问题
- 上传角色文件路径解析错误导致导入失败的问题
- 同步开发目录与运行时目录不一致导致配置不生效的问题
