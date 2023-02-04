reps_to_follow = [
    # Use A,B,S to specify what type of transactions to copy. For example you may only want to follow
    # a specific reps selling trends because they sell at just the right time while others seem to buy at
    # just the right time. A = All, B = Buy, S = sell
    # "First_Name | Last_Name | A",  <--- USE THIS FORMAT OR THE BOT WILL NOT FUNCTION CORRECTLY!
    # This is experimental and isn't configured to account for conflicts. It is advised to keep this
    # in mind when building your list. Some reps may buy a stock while another is selling.
    # In this case you would buy and then sell which could just cost a bunch of money in transaction fees.

    "Nancy | Pelosi | a",




]

small_buy = 10 # When your rep buys over $1000
big_buy = 50 # When your rep buys over $5000
