#!/usr/bin/env python3
"""对账异常检测 demo。

只使用 Python 标准库，读取 sample_data 下的 CSV，输出异常清单。
"""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SAMPLE_DIR = ROOT / "sample_data"
OUTPUT_DIR = ROOT / "output"


@dataclass
class Order:
    order_id: str
    order_date: date
    customer: str
    amount: float


@dataclass
class Payment:
    payment_id: str
    payment_date: date
    customer: str
    amount: float


def normalize_customer(name: str) -> str:
    text = re.sub(r"[\s（）()【】\[\]·.,，。]", "", name.strip().lower())
    for suffix in ("有限公司", "有限责任公司", "公司", "商贸", "贸易"):
        text = text.replace(suffix, "")
    return text


def parse_date(value: str) -> date:
    return date.fromisoformat(value.strip())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"找不到输入文件: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def load_orders() -> list[Order]:
    rows = read_csv(SAMPLE_DIR / "orders.csv")
    return [
        Order(
            order_id=row["order_id"],
            order_date=parse_date(row["order_date"]),
            customer=row["customer"],
            amount=float(row["amount"]),
        )
        for row in rows
    ]


def load_payments() -> list[Payment]:
    rows = read_csv(SAMPLE_DIR / "payments.csv")
    return [
        Payment(
            payment_id=row["payment_id"],
            payment_date=parse_date(row["payment_date"]),
            customer=row["customer"],
            amount=float(row["amount"]),
        )
        for row in rows
    ]


def customer_score(left: str, right: str) -> int:
    left_norm = normalize_customer(left)
    right_norm = normalize_customer(right)
    if left_norm == right_norm:
        return 100
    if left_norm in right_norm or right_norm in left_norm:
        return 80
    shared = set(left_norm) & set(right_norm)
    base = max(len(set(left_norm) | set(right_norm)), 1)
    return int(len(shared) / base * 100)


def find_best_payment(order: Order, payments: list[Payment], used_ids: set[str]) -> tuple[Payment | None, int]:
    candidates: list[tuple[int, Payment]] = []
    for payment in payments:
        if payment.payment_id in used_ids:
            continue
        amount_gap = abs(order.amount - payment.amount)
        if amount_gap > max(100, order.amount * 0.05):
            continue
        score = customer_score(order.customer, payment.customer)
        if score >= 60:
            if amount_gap <= 0.01:
                score += 20
            elif amount_gap <= 100:
                score += 10
            candidates.append((score, payment))
    if not candidates:
        return None, 0
    candidates.sort(key=lambda item: item[0], reverse=True)
    return candidates[0][1], candidates[0][0]


def build_anomalies(orders: list[Order], payments: list[Payment]) -> list[dict[str, str]]:
    anomalies: list[dict[str, str]] = []
    used_payment_ids: set[str] = set()

    for order in orders:
        payment, score = find_best_payment(order, payments, used_payment_ids)
        if payment is None:
            anomalies.append(
                {
                    "type": "missing_payment",
                    "order_id": order.order_id,
                    "payment_id": "",
                    "customer": order.customer,
                    "order_amount": f"{order.amount:.2f}",
                    "payment_amount": "",
                    "reason": "有订单但未找到匹配收款",
                    "review_hint": "检查是否未回款、客户名差异过大、或收款记录缺失",
                }
            )
            continue

        used_payment_ids.add(payment.payment_id)
        amount_gap = round(payment.amount - order.amount, 2)
        if abs(amount_gap) > 0.01:
            anomalies.append(
                {
                    "type": "amount_mismatch",
                    "order_id": order.order_id,
                    "payment_id": payment.payment_id,
                    "customer": order.customer,
                    "order_amount": f"{order.amount:.2f}",
                    "payment_amount": f"{payment.amount:.2f}",
                    "reason": f"金额不一致，差额 {amount_gap:.2f}，匹配分 {score}",
                    "review_hint": "检查是否少收、多收、拆分收款或录入错误",
                }
            )
        if payment.payment_date < order.order_date:
            anomalies.append(
                {
                    "type": "date_before_order",
                    "order_id": order.order_id,
                    "payment_id": payment.payment_id,
                    "customer": order.customer,
                    "order_amount": f"{order.amount:.2f}",
                    "payment_amount": f"{payment.amount:.2f}",
                    "reason": "收款日期早于订单日期",
                    "review_hint": "检查是否预收款、日期录错或匹配错订单",
                }
            )

    for payment in payments:
        if payment.payment_id in used_payment_ids:
            continue
        anomalies.append(
            {
                "type": "unknown_payment",
                "order_id": "",
                "payment_id": payment.payment_id,
                "customer": payment.customer,
                "order_amount": "",
                "payment_amount": f"{payment.amount:.2f}",
                "reason": "有收款但未找到匹配订单",
                "review_hint": "检查是否预收款、客户名差异、或订单未录入",
            }
        )

    return anomalies


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = ["type", "order_id", "payment_id", "customer", "order_amount", "payment_amount", "reason", "review_hint"]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, anomalies: list[dict[str, str]]) -> None:
    counts: dict[str, int] = {}
    for item in anomalies:
        counts[item["type"]] = counts.get(item["type"], 0) + 1

    lines = [
        "# 对账异常摘要",
        "",
        "数据说明：本 demo 使用模拟数据，仅供学习。",
        "",
        "## 核心数字",
        "",
        f"- 异常总数：{len(anomalies)}",
    ]
    for anomaly_type, count in sorted(counts.items()):
        lines.append(f"- {anomaly_type}: {count}")

    lines.extend(["", "## 需要优先复核的异常", ""])
    for item in anomalies[:10]:
        lines.append(
            f"- `{item['type']}` | 订单 `{item['order_id'] or '-'}` | 收款 `{item['payment_id'] or '-'}` | "
            f"{item['customer']} | {item['reason']} | 建议：{item['review_hint']}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    orders = load_orders()
    payments = load_payments()
    anomalies = build_anomalies(orders, payments)
    write_csv(OUTPUT_DIR / "anomalies.csv", anomalies)
    write_markdown(OUTPUT_DIR / "anomalies.md", anomalies)
    print(f"完成：发现 {len(anomalies)} 条需复核异常。输出目录: {OUTPUT_DIR}")


if __name__ == "__main__":
    run()
