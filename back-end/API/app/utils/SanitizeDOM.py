import bleach

def sanitize_html(value):
    return bleach.clean(
        value, 
        tags=['p', 'strong', 'em', 'u', 'h1', 'h2', 'h3', 'ul', 'ol', 'li', 'a', 'blockquote'],
        attributes={'a': ['href', 'target']},
        strip=True
    )