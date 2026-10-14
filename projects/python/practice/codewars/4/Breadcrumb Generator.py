IGNORE = {
    "the", "of", "in", "from", "by",
    "with", "and", "or", "for",
    "to", "at", "a"
}
def format_name(name):
    name = name.split('.')[0]

    if len(name) > 30:
        return "".join(
            word[0].upper()
            for word in name.split('-')
            if word not in IGNORE
        )

    return name.replace('-', ' ').upper()
def generate_bc(url, separator):
    url = url.replace("http://", "").replace("https://", "")
    if url.startswith("www."):
        url = url[4:]
    url = url.split('?')[0]
    url = url.split('#')[0]
    parts = url.split('/')
    parts = parts[1:]
    parts = [x for x in parts if x]
    if parts and parts[-1].startswith("index."):
        parts.pop()
    if not parts:
        return '<span class="active">HOME</span>'
    result = ['<a href="/">HOME</a>']
    path = "/"
    for part in parts[:-1]:
        path += part + "/"
        result.append(
            f'<a href="{path}">{format_name(part)}</a>'
        )
    result.append(
        f'<span class="active">{format_name(parts[-1])}</span>'
    )
    return separator.join(result)
