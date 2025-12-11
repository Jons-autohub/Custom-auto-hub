import os
import datetime
from openai import OpenAI

client = OpenAI()

# API key from GitHub Secrets
openai_api_key = os.getenv("OPENAI_API_KEY")


def generate_title():
    prompt = "Generate a concise, attention-grabbing SEO title for a car modification article (6–12 words)."

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=32,
        temperature=0.7
    )

    return resp.choices[0].message.content.strip()


def generate_article(title):
    prompt = (
        f"Write a 600-word SEO-friendly article about: {title}. "
        "Include an intro, 3 subheadings, and a short conclusion."
    )

    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=800,
        temperature=0.6
    )

    return resp.choices[0].message.content.strip()


def insert_into_index(html_block):
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    updated = html.replace("<!-- AUTO_INSERT_ARTICLE_HERE -->",
                           html_block + "\n<!-- AUTO_INSERT_ARTICLE_HERE -->")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(updated)


def main():
    title = generate_title()
    content = generate_article(title)
    date = datetime.date.today().strftime("%b %d, %Y")

    html_block = f"""
<article>
  <h3>{title}</h3>
  <p><em>{date}</em></p>
  <p>{content}</p>
</article>
"""

    insert_into_index(html_block)


if __name__ == "__main__":
    main()
