import os
import datetime
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_title():
    prompt = "Generate a concise, attention-grabbing SEO title for a car modification article (6–12 words)."
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert automotive writer."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=32,
        temperature=0.7
    )
    return resp.choices[0].message["content"].strip()

def generate_article(title):
    prompt = (
        f"Write an 800-word SEO-friendly article titled '{title}'. "
        "Include: intro, 3–4 subheadings, a conclusion, and natural keyword usage. "
        "Focus on automotive modifications and performance upgrades."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert automotive journalist."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000,
        temperature=0.7
    )

    return resp.choices[0].message["content"].strip()

def save_article_html(title, content):
    filename = title.lower().replace(" ", "_") + ".html"
    filepath = os.path.join("articles", filename)

    date = datetime.date.today().strftime("%b %d, %Y")

    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <title>{title}</title>
        <link rel="stylesheet" href="../style.css">
    </head>
    <body>
        <article>
            <h2>{title}</h2>
            <em>{date}</em>
            <p>{content}</p>
        </article>
    </body>
    </html>
    """

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    return filename

def main():
    title = generate_title()
    content = generate_article(title)
    save_article_html(title, content)

if __name__ == "__main__":
    main()
