# FDE Project Evolution

面向中国中小企业真实业务流程的 FDE 工具包，帮助把混乱的表格、聊天记录、系统导出和人工流程，转成可验证、可试点、可复用的 AI/数字化小闭环。

这个项目是 **skill-first**：主产品是 `SKILL.md` 和配套方法论文档，样例和模板只是帮助理解、验证和传播这个 skill。

- **核心用法**：Codex/Claude Code 读取 `SKILL.md` 后，按 FDE 方法论做项目诊断、场景筛选、工具选型、ROI 测量和经验沉淀。
- **辅助样例**：`examples/` 里的脚本用于展示 skill 期望的样例质量和输出标准，不是独立数据处理产品。

## 快速开始

```powershell
cd outputs\fde-project-evolution\examples\reconciliation
python run.py
Get-Content output\anomalies.md
```

运行后会得到一个辅助样例：

- `output/anomalies.csv`：对账异常明细
- `output/anomalies.md`：给财务或项目负责人看的异常摘要

> 当前样例使用 CSV，目的是保持零依赖和可读性。后续可在模板层补充 `.xlsx` 版本。

## 适合谁

- 想学习 FDE 实战方法的人
- 给本地企业做 AI/数字化落地的顾问或创业者
- 中小企业内部的运营、信息化、数字化负责人
- 想让 Codex/Claude Code 围绕项目持续沉淀经验的人

## 不适合谁

- 需要完整 ERP/CRM 替换方案的团队
- 想看全自动 AI agent 自主决策 demo 的用户
- 没有业务样本、没有责任人、只想泛泛“做数字化”的项目

## 目录结构

```text
.
├── SKILL.md
├── agents/
├── examples/
│   └── reconciliation/
├── references/
├── scripts/
└── templates/
```

## 核心方法

- 先看业务，再看技术
- 先做小闭环，再做大系统
- 先量基线，再谈 ROI
- 先人机协同，再考虑自动化升级
- 先给已填写样例，再给空白模板

## 当前状态

Pre-alpha：

- 已有完整 Codex skill
- 已有方法论文档和案例拆解
- 已有 1 个支撑 skill 的零依赖可运行样例
- 已有基础模板文件

下一步优先补的是能反哺 skill 的材料：

- `examples/customer-grading/`
- `examples/daily-report/`
- `.xlsx` 模板版本
- 更多已填写样例

## 致谢

本项目由 [Codex](https://github.com/anthropics/claude-code) 辅助创建，包括方法论迭代、案例调研、Demo 开发和文档撰写。

## License

MIT
