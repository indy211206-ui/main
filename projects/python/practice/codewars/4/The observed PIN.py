def get_pins(o):
    pn = {
        '1': ['1', '2', '4'],
        '2': ['1', '2', '3', '5'],
        '3': ['2', '3', '6'],
        '4': ['1', '4', '5', '7'],
        '5': ['2', '4', '5', '6', '8'],
        '6': ['3', '5', '6', '9'],
        '7': ['4', '7', '8'],
        '8': ['5', '7', '8', '9', '0'],
        '9': ['6', '8', '9'],
        '0': ['8', '0']
    }
    results = ['']
    for i in o:
        current_options = pn[i]
        new_results = []
        for pin in results:
            for d in current_options:
                new_results.append(pin + d)
        results = new_results
    return results
print(get_pins('8'))
