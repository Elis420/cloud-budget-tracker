
class Category:

    def __init__(self, category=None):
        self.ledger = []
        self.balance = 0
        self.category = category

    def __str__(self):
        header = f"{self.category:*^30}"
        output = header
        total =  f'{self.balance:.2f}'

        if len(header) < 30: 
            header = f"*{header}" 
        else: 
            None

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
    total_spent = 0
    spendings_list = {}
    perc_list = {}
    output = 'Percentage spent by category'
    hundred = "100| "
    ninety = " 90| "
    eighty = " 80| "
    seventy = " 70| "
    sixty = " 60| "
    fifty = " 50| "
    fourty = " 40| "
    thirty = " 30| "
    twenty = " 20| "
    ten = " 10| "
    zero = "  0| "
    dashes = "-"
    
    list_of_categories = []

    for i in categories:
        list_of_categories.append(i.category)
    longest = len(max(list_of_categories, key=len))

    


    graph = [zero,ten,twenty,thirty,fourty,fifty,sixty,seventy,eighty,ninety,hundred]
    

    for i in categories:
        name = i.category
        spendings_list[name] = 0
        perc_list[name] = 0
        for i in i.ledger:
            amount = i["amount"]
            if amount < 0:
                total_spent += -amount
                spendings_list[name]+=-amount
            else:
                continue


    for i in perc_list:
        perc_list[i] = (spendings_list[i]/total_spent)*100
        perc_list[i] = round(perc_list[i])
        counter = 0
        current = perc_list[i]
        dashes += "---"

        

        for num in range(0,11):
            if counter == 0:
                graph[num] += "o  "
                
            else:
                if current == 0:
                    graph[num] += "   "
                else:
                    if (counter/current) <= 1:
                        graph[num] += "o  "  
                    else:
                        graph[num] += "   "
            counter +=10

    for num in range(10,-1,-1):
        output += f'\n{graph[num]}'

    output += "\n    " + dashes
    


    for num in range(0,longest):
            output+= "\n     "
            for cat in list_of_categories:
                if num >= len(cat):
                    output+="   "
                    continue
                else: 
                    output+=cat[num] + "  "
 
    return output


# Rounding Up percentages
def round(n):

    a = (n//10)*10
    return a



