# FDE 项目最终审查与完整升级方案

2026-06-01

---

## 一、项目资产全景图

### 当前已存在 ✓

| 文件 | 行数 | 质量 | 状态 |
|---|---|---|---|
| `SKILL.md` | 258 | 方法论完整，引用清晰 | ✅ 已迭代到第三版 |
| `china-sme-fde.md` | 165 | 洞察真实，有操作指导 | ✅ 核心资产 |
| `practicality-validation.md` | 169 | 评分表+双高双低+已填写示例 | ✅ 核心资产 |
| `evolution-loop.md` | 149 | 六步循环+记忆模板 | ✅ 可用 |
| `open-source-productization.md` | 171 | Star 标准+发布阶段+增长抓手 | ✅ 可用 |
| `automation-prompt.md` | 48 | 可用的自动化提示词模板 | ✅ 可用 |
| `known-cases-analysis.md` | ~300 | 8 个案例拆解，有数据有模式 | ✅ 新增，质量好 |
| `case-patterns-for-sme.md` | ~200 | 7 个可复用模式 | ✅ 新增，质量好 |
| `fde-optimization-roadmap.md` | ~250 | 四层优化+优先级 | ✅ 新增但需更新 |
| `tool-selection-guide.md` | 58 | 决策树+规模梯度+工具判断 | ✅ 可用 |
| `role-output-templates.md` | 131 | 四角色输出模板 | ✅ 可用 |
| `roi-measurement.md` | 72 | ROI公式+指标表+结论规则 | ✅ 可用 |
| `scan_project_notes.py` | 250 | 零依赖，功能完整 | ✅ 唯一可运行资产 |
| `agents/openai.yaml` | 5 | Agent 配置 | ✅ 可用 |

**共：1 个 Skill 定义 + 12 份方法论文档 + 1 个脚本 + 1 个配置文件 = 约 2100 行**

### 被引用但不存在 ❌

SKILL.md 第 257 行引用的资源全部落在 `references/` 目录下，目前实际上都在，没有缺失引用。

### 不存在且未被引用，但开源必需的 ❌

| 缺失项 | 重要程度 |
|---|---|
| `README.md` | 🔴 致命——没有仓库首页，Star 数为 0 |
| `LICENSE` | 🔴 致命——不开源协议没人敢用 |
| `examples/` 目录及样例数据 | 🔴 致命——与"30分钟第一次收获"直接矛盾 |
| `templates/` 目录（可填写的空白文件） | 🟡 严重——模板都在 md 里嵌入，不独立可用 |
| `CONTRIBUTING.md` | 🟡 严重——没有贡献入口 |
| 可运行 Demo 脚本 | 🔴 致命——当前唯一脚本是扫描器，不是业务工具 |
| `tests/` 目录 | 🟢 次要——有代码才有测试需求 |

---

## 二、诚实评估

### 这不是一个开源软件项目

当前项目是一个 **Codex Skill 的完整工作流定义 + 配套方法论手册**。它的运行环境是 Claude Code/Codex，它的核心价值是教 AI 如何做 FDE。

**类比**：这就像一个写得非常好的游戏攻略本，但不是一个游戏。攻略本有价值，但不会有人在 GitHub 上 Star 一份攻略本——除非攻略本里有可玩的 Demo。

### 它的真正价值在哪

1. **方法论体系完整**：场景评分 → 工具选型 → 基线测量 → A/B 验证 → 角色化输出 → 经验沉淀，六个环节环环相扣，逻辑自洽
2. **中国民企洞察深刻**："土办法"视角、老板语言翻译、工具选型梯度，这些是真正在中小企业现场跑过才能总结出来的
3. **安全边界清晰**：数据脱敏、人机协同分级、不跳步原则，避免了 AI 落地最常见的坑
4. **案例对照有价值**：8 个从百亿到微型企业的拆解，覆盖制造/零售/贸易/快消，能帮助新 FDE 判断项目处在什么阶段

### 它的根本局限

**这个项目是一个"规范"，不是"产品"。**

一个规范的受众是"执行这个规范的人"（FDE）。一个产品的受众是"需要解决这个问题的人"（中小企业老板/运营负责人）。

当前项目对 FDE 很有用，但对"想看看 AI 怎么帮中小企业"的路人完全不可用。这就是 Star 上不去的根本原因。

---

## 三、重新定位

### 当前定位

> 一个 Codex Skill，帮助 AI 扮演面向中国中小民企的 FDE

### 建议的新定位

> 一个**双模式**项目：
>
> **模式 A（Skill 模式）**：Codex/Claude Code 用户加载此 Skill 后，AI 能按方法论执行 FDE 工作流
>
> **模式 B（独立工具模式）**：不装 Codex 的人 clone 项目后，能跑 3 个零依赖 Python 脚本，用模拟数据体验"混乱 Excel → 可读报告"的完整流程

**这两种模式共享同样的方法论文档、模板和案例。区别是执行者：模式 A 是 AI，模式 B 是人不靠 AI 先手动跑一遍。**

### 为什么这个定位更好

- 模式 A 保持现有 Skill 的核心功能，不丢弃
- 模式 B 解决了"30 分钟第一次收获"问题——任何人 clone 后 `python examples/reconciliation/run.py` 就能看到效果
- 两个模式互相引流：从模式 B 入门的用户会想"如果接入 AI 是不是更强"，自然进入模式 A

---

## 四、最终升级方案

### 总览：三根柱子 + 一个地基

```
┌─────────────────────────────────────────────┐
│              FDE Toolkit                     │
├─────────────────┬─────────────────┬─────────┤
│  方法论（已有）   │  数据样例（新建） │  工具脚本 │
│  12份参考文档    │  3个场景 × 样例   │  3个 demo │
│  质量：✅ 80%    │  数据 + 模拟输入   │  零依赖   │
├─────────────────┴─────────────────┴─────────┤
│              地基：仓库工程化                 │
│   README / LICENSE / CONTRIBUTING / 目录重整  │
└─────────────────────────────────────────────┘
```

### 柱子一：数据样例（examples/）

**目标**：让没读过任何文档的人，打开文件夹就能看到"这是什么"。

**设计原则**：
- 每个样例自包含：一个独立文件夹，含 README + 数据 + 脚本
- 数据全部虚构，标注"模拟数据，仅供学习"
- 数据格式贴近真实中小企业的混乱程度（但不至于不可读）
- 每个样例展示一个完整流程：输入 → 处理 → 输出

**三个样例场景**：

#### Example 1：对账异常检测 (`examples/reconciliation/`)

```
场景：一家小型贸易公司，财务每周手工比对订单表和收款表
数据：
  - orders.xlsx（50条模拟订单，含日期/客户/产品/金额/订单号）
  - payments.xlsx（40条模拟收款，含日期/客户/金额/收款方式）
  - 刻意制造 8 处不一致：金额差 1 分钱、客户名简繁体/错别字、日期顺序颠倒、重复收款
脚本：run.py
  - 读两个表，按客户名+金额模糊匹配
  - 输出 anomalies.xlsx，分 4 类异常：
    1. 有订单无收款
    2. 有收款无订单
    3. 金额不匹配
    4. 金额匹配但日期异常
  - 人工可快速复核，不直接标记"错误"
README：写清这是什么场景、怎么跑、输出每列的含义、实际对账注意事项
```

#### Example 2：客户分级与流失预警 (`examples/customer-grading/`)

```
场景：一家建材批发商，客户分散在 Excel 和微信里，复购靠老板记性
数据：
  - customers.xlsx（60条模拟客户，含最近购买日期/累计采购额/质量问题次数/所在城市）
  - 包含明显可分级模式：少量大客户 + 大量中小客户 + 几个快流失的老客户
脚本：run.py
  - 读客户表，按 RFM 简化模型打分
  - 分 4 级：VIP / 稳定 / 风险 / 流失
  - 输出 graded_customers.xlsx，含评分 + 分级 + 建议触达动作
README：解释 RFM 对老板的意义，写清每个分级的定义和跟进建议
```

#### Example 3：老板经营日报 (`examples/daily-report/`)

```
场景：老板每天想知道销售、回款、库存、逾期、异常，现在靠打电话问
数据：
  - sales.xlsx（昨日销售数据）
  - receivables.xlsx（回款记录）
  - overdue.xlsx（逾期订单）
脚本：run.py
  - 读三个表，汇总关键数字
  - 标出异常（单日销售额暴跌、单笔回款异常大、逾期超 30 天）
  - 输出 daily-report.md，格式为：
    # 经营日报 2026-06-01
    ## 核心数字（4 行）
    ## 异常预警（如有）
    ## 待决策（如有）
README：解释为什么日报要控制在 1 页，每类指标对应的业务含义
```

**技术要求**：
- Python 3.8+，零第三方库（只用 openpyxl + csv + json + pathlib）
- 每个脚本一个 `run()` 函数，能直接 `python run.py`
- 输入读取 `sample_data/` 下的文件，输出写入 `output/`
- 有简单的输入校验（文件不存在时给出提示）
- 不做过度抽象，每个脚本约 100-200 行

### 柱子二：独立模板文件（templates/）

**目标**：让用户能直接下载一个 Excel/Word 文件开始填，不用从 Markdown 里复制。

当前状态：所有模板嵌入在 `.md` 文件中。**这导致了"看着有模板，用的时候复制不了"。**

| 模板 | 格式 | 来源 |
|---|---|---|
| 场景评分表（空表） | `.xlsx` | practicality-validation.md |
| 场景评分表（已填写示例） | `.xlsx` | practicality-validation.md |
| 场景池 | `.xlsx` | practicality-validation.md |
| A/B 测试报告 | `.md` 或 `.docx` | practicality-validation.md |
| 项目画像 | `.md` | evolution-loop.md |
| 流程简报 | `.md` | china-sme-fde.md |
| 访谈提纲 | `.md` | china-sme-fde.md |
| 企业负责人版报告 | `.md` | role-output-templates.md |
| 部门负责人版报告 | `.md` | role-output-templates.md |
| 一线操作员版说明 | `.md` | role-output-templates.md |
| ROI 测算表 | `.xlsx` | roi-measurement.md |

**动作**：
1. 每个模板创建一个独立文件
2. Excel 格式的提供 `.xlsx` + 已完成示例 `.xlsx`
3. Markdown 格式的提供 `.md` + 已完成示例 `.md`
4. 文件名清晰：`template-scenario-scoring.xlsx` / `example-scenario-scoring.xlsx`

### 柱子三：仓库工程化

这是地基，没有这个，上面两根柱子立不起来。

#### README.md

```
结构：
1. 一句话定位（40 字以内）
2. 这是什么（2 段，不超过 150 字）
3. 30 秒快速开始（3 条命令）
   git clone ...
   cd fde-toolkit/examples/reconciliation
   python run.py
4. 你会得到什么（截图或输出示例）
5. 目录结构
6. 适合谁（4 类用户）
7. 不适合谁（3 类）
8. 来自真实案例的模式（简短，链接到文档）
9. Star 历史（空，为以后准备）
10. License
```

#### LICENSE

建议 MIT —— 对工具类项目最友好，允许商用，不强制开源衍生作品。

#### CONTRIBUTING.md

```
1. 三种贡献方式：提场景 / 提供样例数据 / 提代码
2. 场景贡献模板
3. 样例数据要求（虚构但逼真、脱敏、标注"模拟数据"）
4. 代码风格要求（零依赖优先、中文注释允许）
5. PR 流程
```

#### .gitignore

```
__pycache__/
*.pyc
.DS_Store
output/
```

#### 最终目录结构

```
fde-toolkit/
├── README.md
├── LICENSE                          (MIT)
├── CONTRIBUTING.md
├── .gitignore
│
├── examples/                         ← 柱子一
│   ├── reconciliation/
│   │   ├── README.md
│   │   ├── sample_data/
│   │   │   ├── orders.xlsx
│   │   │   └── payments.xlsx
│   │   ├── run.py
│   │   └── output/                   (.gitignore)
│   │       └── anomalies.xlsx
│   ├── customer-grading/
│   │   ├── README.md
│   │   ├── sample_data/
│   │   │   └── customers.xlsx
│   │   ├── run.py
│   │   └── output/
│   └── daily-report/
│       ├── README.md
│       ├── sample_data/
│       │   ├── sales.xlsx
│       │   ├── receivables.xlsx
│       │   └── overdue.xlsx
│       ├── run.py
│       └── output/
│
├── templates/                        ← 柱子二
│   ├── template-scenario-scoring.xlsx
│   ├── example-scenario-scoring.xlsx
│   ├── template-ab-test-report.md
│   ├── example-ab-test-report.md
│   ├── template-project-profile.md
│   ├── template-process-brief.md
│   ├── template-interview-checklist.md
│   ├── template-roi-calculator.xlsx
│   ├── template-boss-report.md
│   ├── template-manager-report.md
│   └── template-operator-guide.md
│
├── references/                       ← 方法论（已有）
│   ├── china-sme-fde.md
│   ├── practicality-validation.md
│   ├── evolution-loop.md
│   ├── open-source-productization.md
│   ├── known-cases-analysis.md
│   ├── case-patterns-for-sme.md
│   ├── tool-selection-guide.md
│   ├── role-output-templates.md
│   ├── roi-measurement.md
│   └── automation-prompt.md
│
├── skill/                            ← Codex Skill（已有）
│   ├── SKILL.md
│   └── agents/
│       └── openai.yaml
│
├── scripts/
│   └── scan_project_notes.py        ← 已有
│
└── tests/                            ← 未来
    └── .gitkeep
```

---

## 五、执行计划

### 阶段一：地基 + 最小可发布（第 1-2 周）

**目标**：项目可以从零开始被理解和使用

| # | 动作 | 产物 | 工作量 |
|---|---|---|---|
| 1 | 写 README.md | `README.md` | 1h |
| 2 | 加 LICENSE (MIT) | `LICENSE` | 10min |
| 3 | 写 .gitignore | `.gitignore` | 5min |
| 4 | 创建 examples/reconciliation/ 完整样例 | 数据 + 脚本 + README | 3h |
| 5 | 创建 templates/ 目录，放 3 个最重要模板 | xlsx + md 各 3 个 | 2h |
| 6 | 删除 fde-optimization-roadmap.md（已被本文件替代） | - | 1min |
| 7 | 更新 SKILL.md 资源列表，对齐实际文件 | 更新引用 | 30min |

**此时可以发布 Pre-alpha**。别人 clone 下来能跑一个 Demo。

### 阶段二：丰富样例 + 贡献入口（第 3-4 周）

| # | 动作 | 产物 | 工作量 |
|---|---|---|---|
| 8 | 创建 examples/customer-grading/ | 数据 + 脚本 + README | 3h |
| 9 | 创建 examples/daily-report/ | 数据 + 脚本 + README | 2h |
| 10 | 补全 templates/ 剩余模板 | 6 个文件 | 2h |
| 11 | 写 CONTRIBUTING.md | `CONTRIBUTING.md` | 1h |
| 12 | 手动测试：在另一台电脑 clone 后跑通 3 个 Demo | 验证 | 1h |

**此时可以发布 Alpha**。3 个场景可跑，模板可填，贡献有入口。

### 阶段三：公开发布（第 5-6 周）

| # | 动作 | 产物 |
|---|---|---|
| 13 | 中文社区发帖（即刻/V2EX/掘金/知乎） | 传播 |
| 14 | 录 3 分钟演示视频 | README 嵌入 |
| 15 | 准备 Issue 模板（场景贡献 / Bug 报告） | `.github/ISSUE_TEMPLATE/` |
| 16 | 根据反馈修一轮 | 迭代 |

---

## 六、不做的事

1. **不做 Web 界面**。保持 CLI + Excel，这是中小企业最熟悉的形态。Web 界面需要运维，中小企业没有运维能力。
2. **不做 SaaS**。SaaS 的获客成本、留存、付费转化是这个项目无法承受的。保持工具定位。
3. **不接入真实微信/钉钉/飞书 API**。涉及 App 审核、企业资质、隐私合规，单人开发者无法承担。
4. **不做 AI Agent 自主决策**。项目定位是"人机协同"，L4 以上的自动化留给客户自己配置。
5. **不写测试**（暂缓）。三个 Demo 脚本用人工验证即可。等贡献者增多、代码行数过 2000 再补测试。

---

## 七、Star 数重新估算

基于新定位（双模式：Skill + 独立工具）和完整执行计划：

| 里程碑 | Star 预估 | 条件 |
|---|---|---|
| Pre-alpha（1 个 Demo + README + 模板） | 30-60 | 有东西可跑，但样例少 |
| Alpha（3 个 Demo + 全部模板 + CONTRIBUTING） | 100-200 | 30 分钟收获路径完整 |
| 公开发布 + 社区传播 | 200-500 | 取决于传播效果 |
| 持续运营（案例积累 + 社区贡献） | 400-800 | 6-12 个月后 |
| 1000 star | **有可能，不确定** | 需要：①3+ 个外部贡献的真实案例 ②一篇爆款中文传播文章 ③品类先发优势持续放大 |

**关键变量**：
- 有没有人在社区提交脱敏案例 → 案例数决定了"这东西是不是真的有用"
- 中文 SME AI 落地工具这个品类目前是真空 → 能否抢占"品类 = 项目名"的心智
- 执行质量 → 三个 Demo 的数据是否够逼真、让人一看就想到自己公司的乱账

---

## 八、与上一版优化方案的区别

| 维度 | 上一版 (fde-optimization-roadmap.md) | 本版 |
|---|---|---|
| 定位 | 纯 Skill 优化 | 双模式：Skill + 独立工具 |
| Demo 数量 | 4 个建议 | 锁定 3 个最佳切口 |
| 仓库结构 | 概念性描述 | 完整目录树 |
| 模板 | 提到但没规划 | 11 个独立文件清单 |
| 执行 | 四层，没有时间线 | 三阶段，每阶段有产物和工时 |
| Star 预期 | 10-700 过于乐观的范围 | 按里程碑分层，上限调低 |
| 发布策略 | 没有 | Pre-alpha → Alpha → 公开发布 |

---

## 九、如果你只做三件事

如果时间有限，按顺序只做这三个：

1. **README.md + 一个可运行 Demo**：让项目从"不能跑"变成"能跑"
2. **LICENSE (MIT)**：让项目从"不能合法使用"变成"可以"
3. **独立 Excel 模板（场景评分 + ROI 测算）**：让最核心的两个框架可独立使用

这三件事做完，项目就有资格被称为"开源项目"了。预计工作量：6-8 小时。
