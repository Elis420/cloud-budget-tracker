
class Category:

    def __init__(self, category=None):
        self.ledger = []
        self.balance = 0
        self.category = category

    def __str__(self):
        header = f"{self.category:*^30}"
        output = header
        total =  f'{self.balance:.2f}'

        for i in self.ledger:
            limited_desc = (i["description"])[0:23]
            amount = i["amount"]
            mod_amount = (str(f"{amount:.2f}"))[0:7]
            number_of_spaces = (30 - len(limited_desc) - len(mod_amount))
            spaces = " "*number_of_spaces
            output += f'\n{limited_desc}{spaces}{mod_amount}'

        
        output += f'\nTotal: {total}'


        return output


    def deposit(self, amount, description = ""):
        self.ledger.append({'amount': amount, 'description': description})
        self.balance += amount



    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            self.balance -= amount
            return True
        else:
            return False
        

    def transfer(self, amount, where):
        destination = where.category
        origin = self.category
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': f'Transfer to {destination}'})
            where.ledger.append({'amount': amount, 'description': f'Transfer from {origin}'})
            self.balance -= amount
            where.balance += amount
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount <= self.balance:
            return True
        else:
            return False 

    def get_balance(self):
        return self.balance
    
    def to_dict(self):
        return {
            "category": self.category,
            "balance": self.balance,
            "ledger": self.ledger,  # list of {"amount": float, "description": str}
        }

    @classmethod
    def from_dict(cls, data: dict):
        c = cls(category=data["category"])
        c.balance = data.get("balance", 0)
        c.ledger = list(data.get("ledger", []))
        return c


def create_spend_chart(categories):
    """
    Build an ASCII chart like:

    Percentage spent by category
    100|          
     90|          
     80|          
     70|          
     60| o        
     50| o        
     40| o        
     30| o  o     
     20| o  o     
     10| o  o     
      0| o  o     
         ----------
          F  E
          o  n
          o  t
          d  e
             r
             t
             a
             i
             n
             m
             e
             n
             t
    """
    # 1. How much was spent (negative amounts) in each category?
    spent_per_cat = []
    names = []
    for c in categories:
        names.append(c.category)
        spent = 0
        for entry in c.ledger:
            amt = entry["amount"]
            if amt < 0:
                spent += -amt
        spent_per_cat.append(spent)

    total_spent = sum(spent_per_cat)
    if total_spent == 0:
        return "Percentage spent by category\n\n(no spending recorded yet)"

    # 2. Convert to percentages, rounded DOWN to the nearest 10
    percents = [
        int((spent / total_spent * 100) // 10 * 10) for spent in spent_per_cat
    ]

    # 3. Build chart rows from 100 down to 0
    lines = ["Percentage spent by category"]
    for level in range(100, -1, -10):
        line = f"{level:>3}| "
        for p in percents:
            line += "o  " if p >= level else "   "
        lines.append(line)

    # 4. Add the horizontal line
    lines.append("    " + "-" * (len(categories) * 3 + 1))

    # 5. Add the category names vertically
    max_len = max(len(name) for name in names) if names else 0
    for i in range(max_len):
        line = "     "
        for name in names:
            if i < len(name):
                line += name[i] + "  "
            else:
                line += "   "
        lines.append(line.rstrip())

    return "\n".join(lines)





