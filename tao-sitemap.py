#!/usr/bin/env python3
"""Tự động tạo sitemap.xml và robots.txt từ các file .html trong thư mục gốc."""
import glob, os, subprocess, datetime
SITE = "https://vklens.vn/"
BO_QUA = {"quan-ly.html", "tuyen-dung.html.html"}  # trang nội bộ, không đưa vào sitemap

def ngay(f):
    try:
        t = subprocess.run(["git", "log", "-1", "--format=%cs", "--", f], capture_output=True, text=True).stdout.strip()
        if t: return t
    except Exception: pass
    return datetime.date.fromtimestamp(os.path.getmtime(f)).isoformat()

def uu_tien(f):
    if f == "index.html": return "1.0"
    if f == "kinh-ap-trong.html": return "0.8"
    if f == "chuyen-muc.html": return "0.9"
    if f.startswith("chuyen-muc/"): return "0.8"
    if f.startswith(("kinh-ap-trong-", "nuoc-ngam-", "hop-", "may-rua", "coc-rua", "nhip-", "nho-mat")): return "0.8"
    return "0.6"

files = [f for f in ("index.html", "kinh-ap-trong.html", "khuyen-mai.html", "tuyen-dung.html") if os.path.exists(f)] + ["chuyen-muc.html"] + sorted(glob.glob("chuyen-muc/*.html"))  # chỉ các trang đang dùng; thêm trang mới vào danh sách này khi cần
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for f in files:
    loc = SITE if f == "index.html" else SITE + f
    out.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{ngay(f)}</lastmod>\n    <priority>{uu_tien(f)}</priority>\n  </url>")
out.append("</urlset>")
open("sitemap.xml", "w", encoding="utf-8").write("\n".join(out) + "\n")
open("robots.txt", "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n")
print(len(files), "URL")
