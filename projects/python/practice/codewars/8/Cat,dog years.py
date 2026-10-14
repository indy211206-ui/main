def human_years_cat_years_dog_years(human_years):
    cat = 15
    dog = 15
    if human_years > 1:
        cat += 9
        dog += 9
    if human_years > 2:
        cat += (human_years - 1) * 4
        dog += (human_years - 1) * 5
    return [human_years, cat, dog]
