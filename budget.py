class Category:
  def __init__(self, name):
    self.ledger = []
    self.name = name

  def __str__(self):
    ret = "*************" + self.name + "*************\n"
    for i in self.ledger:
      out_desc = i["description"][:23]
      out_val = "{:.2f}".format(i["amount"])
      ret += out_desc
      ret += " " * (30 - len(out_desc) - len(out_val))
      ret += out_val
      ret += "\n"

    out_total = "{:.2f}".format(self.get_balance())
    ret += "Total: " + out_total
      
    return ret

  def deposit(self, amount, description=""):
    amount = float(amount)
    if not description:
      description = ""
    self.ledger.append({
      "amount": amount,
      "description": description
    })

  def withdraw(self, amount, description=""):
    amount = float(amount)
    if(self.check_funds(amount)):
      if not description:
        description = ""
      self.ledger.append({
        "amount": -amount,
        "description": description
      })
      return True
    else:
      return False

  def transfer(self, amount, other_category):
    res = self.withdraw(amount, "Transfer to " + other_category.name)
    if res:
      other_category.deposit(amount, "Transfer from " + self.name)
      return True 
    else:
      return False

  def check_funds(self, amount):
    return self.get_balance() >= amount

  def get_balance(self):
    sum = 0
    for a in self.ledger:
      sum += a["amount"]
    return sum





def create_spend_chart(categories):
  ret = "Percentage spent by category\n"
  for i in range(100, -10, -10):
    # labels on y axis
    label_length = len(str(i))
    ret += " " * (3 - label_length)
    ret += str(i) + "| "

    # bars (values)
    for category in categories:
      percentage = get_percentage(categories, category)
      if percentage < i:
        ret += "   "
      else:
        ret += "o  "
    ret += "\n"

  # bottom dashed line (-------)
  ret += "    -"
  ret += "---" * len(categories)
  ret += "\n"

  # labels on x axis
  
  longest_name_len = get_longest_name_len(categories)
  for i in range(0, longest_name_len):
    ret += "     "
    for category in categories:
      char = category.name[i:i+1]
      if(len(char) < 1):
        char = " "
      ret += char + "  "
    if i < longest_name_len - 1: # no newline at the end
        ret += "\n"

  return ret

def get_longest_name_len(categories):
  ret = 0
  for category in categories:
    length = len(category.name)
    if(length > ret):
      ret = length
  return ret

def get_percentage(categories, category):
  total = calculate_total_spendings(categories)
  spendings = calculate_spendings(category)
  return spendings / total * 100


def calculate_total_spendings(categories):
  ret = 0
  for category in categories:
    ret += calculate_spendings(category)
  return ret

def calculate_spendings(category):
  ret = 0
  for i in category.ledger:
    if(i["amount"] < 0):
      ret += i["amount"]
  return ret