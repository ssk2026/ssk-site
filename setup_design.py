import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

templates_dir = os.path.join(BASE_DIR, "templates")
static_dir = os.path.join(BASE_DIR, "static")
css_dir = os.path.join(static_dir, "css")

os.makedirs(templates_dir, exist_ok=True)
os.makedirs(css_dir, exist_ok=True)

# ----------------------------
# base.html
# ----------------------------
base_html = """{% load static %}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}SSK 연구단{% endblock %}</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>

<header class="header">
    <div class="container">
        <div class="logo">Dongguk University SSK</div>
        <nav>
            <ul class="menu">
                <li><a href="/">홈</a></li>
                <li><a href="/about/">연구단 소개</a></li>
                <li><a href="/people/">연구진 소개</a></li>
                <li><a href="/outputs/">연구실적</a></li>
                <li><a href="/events/">행사</a></li>
                <li><a href="/contact/">문의</a></li>
            </ul>
        </nav>
    </div>
</header>

<section class="hero">
    <div class="hero-text">
        <h1>SSK Research Group</h1>
        <p>Advancing Social Science Knowledge</p>
    </div>
</section>

<main class="container">
    {% block content %}{% endblock %}
</main>

<footer class="footer">
    © 2026 Dongguk University SSK Research Group
</footer>

</body>
</html>
"""

# ----------------------------
# home.html
# ----------------------------
home_html = """{% extends 'base.html' %}
{% block title %}홈 | SSK{% endblock %}

{% block content %}
<div class="card-grid">
    <div class="card">
        <h3>연구단 소개</h3>
        <p>연구단 개요와 연구 목표</p>
    </div>
    <div class="card">
        <h3>연구진</h3>
        <p>참여 연구진 소개</p>
    </div>
    <div class="card">
        <h3>연구실적</h3>
        <p>논문 및 연구 성과</p>
    </div>
</div>
{% endblock %}
"""

# ----------------------------
# CSS
# ----------------------------
css_content = """
body {
    margin: 0;
    font-family: 'Segoe UI', sans-serif;
    background: #f9f9f9;
    color: #222;
}

.container {
    width: 1200px;
    margin: 0 auto;
}

.header {
    background: white;
    border-bottom: 1px solid #ddd;
    padding: 20px 0;
}

.logo {
    font-size: 22px;
    font-weight: bold;
}

.menu {
    list-style: none;
    display: flex;
    gap: 30px;
    padding: 0;
}

.menu a {
    text-decoration: none;
    color: #333;
    font-weight: 500;
}

.menu a:hover {
    color: #b22222;
}

.hero {
    height: 300px;
    background: linear-gradient(to right, #000000aa, #000000aa),
                url('https://images.unsplash.com/photo-1524995997946-a1c2e315a42f');
    background-size: cover;
    background-position: center;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.hero h1 {
    font-size: 42px;
    margin-bottom: 10px;
}

.card-grid {
    display: flex;
    gap: 30px;
    margin: 60px 0;
}

.card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    flex: 1;
    box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}

.footer {
    text-align: center;
    padding: 30px;
    background: #111;
    color: white;
}
"""

with open(os.path.join(templates_dir, "base.html"), "w", encoding="utf-8") as f:
    f.write(base_html)

with open(os.path.join(templates_dir, "home.html"), "w", encoding="utf-8") as f:
    f.write(home_html)

with open(os.path.join(css_dir, "style.css"), "w", encoding="utf-8") as f:
    f.write(css_content)

print("✅ 디자인 세팅 완료!")
