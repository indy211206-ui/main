def valid_parentheses(x):
    while "()" in x:
        x = x.replace("()", "")
    return x == ""
