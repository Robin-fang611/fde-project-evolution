# 对账异常检测 Demo

## 场景

一家小型贸易公司每周需要把订单表和收款表做人工对账。当前问题是：客户名称不完全一致、金额有小误差、收款日期可能晚于订单日期，财务需要逐行检查。

这个 demo 展示一个最小闭环：

```text
订单 CSV + 收款 CSV -> 对账脚本 -> 异常清单 CSV + 摘要 Markdown
```

## 如何运行

```powershell
python run.py
Get-Content output\anomalies.md
```

## 输入文件

- `sample_data/orders.csv`：模拟订单数据
- `sample_data/payments.csv`：模拟收款数据

所有数据均为模拟数据，仅供学习。

## 输出文件

- `output/anomalies.csv`：异常明细
- `output/anomalies.md`：异常摘要

## 异常类型

- `missing_payment`：有订单无收款
- `unknown_payment`：有收款无对应订单
- `amount_mismatch`：金额接近但不一致
- `date_before_order`：收款日期早于订单日期，需要人工确认

## 现实使用注意

这个 demo 不直接判断“谁错了”，只输出需要人工复核的异常。真实业务中还需要补充合同号、发票号、收款账户、业务员等字段。
