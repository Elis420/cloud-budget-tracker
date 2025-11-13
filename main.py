# main.py
import os
import sys
import json
from datetime import date
from collections import defaultdict

from s3_io import load_json, save_json
from budget_app import Category, create_spend_chart  # import our budget app code (handles category and creation of chart)

BUCKET = os.environ.get("BUDGET_BUCKET", "elis-budget-tracker-REPLACE")
LEDGER_KEY = os.environ.get("LEDGER_KEY", "data/ledger.json")



def load_categories_from_s3():
    raw = load_json(BUCKET, LEDGER_KEY, default={"categories": []})
    cats = [Category.from_dict(c) for c in raw.get("categories", [])]
    return cats

def save_categories_to_s3(categories):
    payload = {"categories": [c.to_dict() for c in categories]}
    return save_json(BUCKET, LEDGER_KEY, payload)

def ensure_category(categories, name):
    for c in categories:
        if c.category == name:
            return c
    c = Category(name)
    categories.append(c)
    return c

def find_category(categories, name):
    for c in categories:
        if c.category == name:
            return c
    return None

def summarize(categories):
    by_cat_spend = defaultdict(float)
    total_spent = 0.0
    for c in categories:
        for e in c.ledger:
            amt = e["amount"]
            if amt < 0:
                by_cat_spend[c.category] += abs(amt)
                total_spent += abs(amt)
    by_cat_pct = {k: (v / total_spent * 100 if total_spent else 0) for k, v in by_cat_spend.items()}
    return {
        "total_spent": round(total_spent, 2),
        "by_category": {k: round(v, 2) for k, v in by_cat_spend.items()},
        "by_category_pct": {k: round(v, 1) for k, v in by_cat_pct.items()},
    }

def cmd_add(categories, args):
    """
    budget add <Category> <amount> <description...>
    positive amount = deposit, negative = withdraw
    """
    if len(args) < 3:
        print("Usage: budget add <Category> <amount> <description...>")
        sys.exit(1)
    name = args[0]
    amount = float(args[1])
    desc = " ".join(args[2:])
    cat = ensure_category(categories, name)
    if amount >= 0:
        cat.deposit(amount, desc)
    else:
        ok = cat.withdraw(-amount, desc)
        if not ok:
            print("❌ Not enough funds.")
    print(f"✅ Added entry to {name}: {amount} | {desc}")

def cmd_transfer(categories, args):
    """
    budget transfer <From> <To> <amount>
    """
    if len(args) != 3:
        print("Usage: budget transfer <From> <To> <amount>")
        sys.exit(1)
    frm, to, amt = args[0], args[1], float(args[2])
    c_from = ensure_category(categories, frm)
    c_to = ensure_category(categories, to)
    ok = c_from.transfer(amt, c_to)
    print("✅ Transfer complete" if ok else "❌ Transfer failed (insufficient funds)")

def cmd_withdraw(categories, args):

    if len(args) < 3:
        print("Usage: budget withdraw <Category> <amount> <description...>")
        return
    category = args[0]
    amount = float(args[1])
    description = " ".join(args[2:])
    cat = find_category(categories, category)

    if not cat:
        print(f"❌ Category '{category}' not found")
        return

    if cat.withdraw(amount, description):
        print(f"💸 Withdrawn {amount} from {category}: {description}")
    else:
        print("❌ Withdrawal failed (insufficient funds)")


def cmd_show(categories, args):
    """
    budget show           -> print chart
    budget show <Category> -> print ledger for that category
    """
    if not args:
        print(create_spend_chart(categories))
        return
    name = args[0]
    for c in categories:
        if c.category == name:
            print(c)
            return
    print("Category not found.")

def cmd_report(categories, args):
    """
    budget report -> saves summary JSON to s3://.../reports/YYYY-MM-DD.json
    """
    summary = summarize(categories)
    key = f"reports/{date.today().isoformat()}.json"
    uri = save_json(BUCKET, key, summary)
    print("📊 Summary:", json.dumps(summary, indent=2))
    print(f"✅ Saved report: {uri}")

def main():
    if len(sys.argv) < 2:
        print("Commands:")
        print("  budget add <Category> <amount> <description...>")
        print("  budget transfer <From> <To> <amount>")
        print("  budget show [Category]")
        print("  budget report")
        print("  withdraw <Category> <amount> <description>")
        sys.exit(0)

    categories = load_categories_from_s3()

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "add":
        cmd_add(categories, args)
    elif cmd == "transfer":
        cmd_transfer(categories, args)
    elif cmd == "show":
        cmd_show(categories, args)
    elif cmd == "report":
        cmd_report(categories, args)
    elif cmd == "withdraw":
        cmd_withdraw(categories, args)
    else:
        print("Unknown command.")
        sys.exit(1)

    # persist on any mutating command
    if cmd in ("add", "transfer", "withdraw"):
        uri = save_categories_to_s3(categories)
        print(f"☁️  Synced ledger to: {uri}")


if __name__ == "__main__":
    main()

