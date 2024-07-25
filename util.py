def update_position(position, transaction):
    key = f"{transaction['exchange_id']}:{transaction['ticker_symbol']}"
    if key in position.keys():
        if transaction["side"] == "BUY":
            position[key]["long"][f"{transaction['matched_price']}"] = transaction["transaction_id"]
        else:
            position[key]["short"][f"{transaction['matched_price']}"] = transaction["transaction_id"]
        
    else:
        position[key] = {"long": {}, "short": {}}
        if transaction["side"] == "BUY":
            position[key]["long"] = {transaction["matched_price"] : transaction["transaction_id"]}
        else:
            position[key]["short"] = {transaction["matched_price"]: transaction["transaction_id"]}

    return position