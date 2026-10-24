#!/usr/bin/env python3
"""Render and validate the standalone privacy/support website (Python 3.9+)."""
import argparse
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlencode, urlsplit

ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {'index.html', 'privacy.html', 'privacy-en.html',
                'support.html', 'support-en.html', 'styles.css'}
GITHUB_PRIVACY = 'https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement'


def public_details(config):
    result = {key: config.get(key, '').strip() if isinstance(config.get(key), str) else '' for key in
              ('developerName', 'supportEmail', 'privacyPolicyURL', 'supportURL')}
    if not re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+", result['supportEmail']):
        result['supportEmail'] = ''
    for key in ('privacyPolicyURL', 'supportURL'):
        try:
            value = result[key]
            url = urlsplit(value)
            if (url.scheme != 'https' or not url.hostname or url.username or url.password
                    or url.query or url.fragment or any(c.isspace() for c in value)):
                result[key] = ''
        except ValueError:
            result[key] = ''
    return result


def publication_errors(content, deployment, repository=None):
    details = public_details(content['configuration'])
    errors = ['Missing/invalid public detail: ' + key for key, value in details.items() if not value]
    owner = deployment.get('githubOwner', '')
    repo = deployment.get('repositoryName', '')
    if not re.fullmatch(r'[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?', owner):
        errors.append('Missing/invalid githubOwner in deployment.json')
    if not re.fullmatch(r'[A-Za-z0-9_][A-Za-z0-9_.-]{0,99}', repo):
        errors.append('Missing/invalid repositoryName in deployment.json')
    if owner and repo:
        base = 'https://' + owner.lower() + '.github.io'
        if repo.lower() != owner.lower() + '.github.io':
            base += '/' + repo
        for key, page in [('privacyPolicyURL', 'privacy.html'), ('supportURL', 'support.html')]:
            if details[key] and details[key] != base + '/' + page:
                errors.append(key + ' must equal ' + base + '/' + page)
        if repository and repository.lower() != (owner + '/' + repo).lower():
            errors.append('Workflow repository does not match deployment.json')
    return errors


def render(content):
    e = html.escape
    details = public_details(content['configuration'])
    incomplete = not all(details.values())
    output = {}
    for language in ('zh-Hant', 'en'):
        english = language == 'en'
        suffix = '-en' if english else ''
        t = content['translations'][language]
        for topic in ('privacy', 'support'):
            doc = t[topic]
            title = e(doc['title'])
            privacy = 'Privacy' if english else '隱私政策'
            support = 'Support' if english else '使用說明與支援'
            sections = ''.join('<section id="{}"><h2>{}</h2>{}</section>\n'.format(
                e(s['id'], quote=True), e(s['title']),
                ''.join('<p>{}</p>'.format(e(p)) for p in s['paragraphs'])) for s in doc['sections'])
            toc = ''.join('<li><a href="#{}">{}</a></li>'.format(e(s['id'], quote=True), e(s['title'])) for s in doc['sections'])
            developer = '<p>{}: {}</p>'.format('Developer' if english else '開發者', e(details['developerName'])) if details['developerName'] else ''
            contact = ''
            if details['supportEmail']:
                href = 'mailto:' + details['supportEmail'] + '?' + urlencode({'subject': 'Violin Trainer Support'})
                contact = '<section id="email"><h2>{}</h2><p><a href="{}">{}</a></p></section>'.format(
                    'Contact developer' if english else '聯絡開發者', e(href, quote=True), e(details['supportEmail']))
            draft = ''
            if incomplete:
                draft = '<aside class="draft" role="note">{}</aside>'.format(
                    'Draft: developer name, contact details and public URLs are not yet complete.' if english
                    else '頁面草稿：開發者名稱、聯絡資訊與公開網址尚未補齊。')
            hosting = ''
            if topic == 'privacy':
                hosting = '<section id="website-hosting"><h2>{}</h2><p>{} <a href="{}">{}</a></p></section>'.format(
                    'Website hosting' if english else '網站託管',
                    'When this website is published on GitHub Pages, GitHub logs visitors’ IP addresses for security purposes. See the' if english
                    else '本網站發布於 GitHub Pages 後，GitHub 會基於安全目的記錄訪客的 IP 位址。相關處理方式請參閱',
                    GITHUB_PRIVACY, 'GitHub Privacy Statement.' if english else 'GitHub 隱私聲明。')
                toc += '<li><a href="#website-hosting">{}</a></li>'.format('Website hosting' if english else '網站託管')
            other_page = topic + ('.html' if english else '-en.html')
            output[topic + suffix + '.html'] = f'''<!doctype html>
<html lang="{language}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  {'<meta name="robots" content="noindex">' if incomplete else ''}
  <meta name="description" content="Violin Trainer {title}">
  <title>{title} · Violin Trainer</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <a class="skip-link" href="#main">{'Skip to content' if english else '跳至主要內容'}</a>
  <header class="site-header">
    <div class="header-inner">
      <span class="brand">Violin Trainer</span>
      <nav aria-label="{'Navigation' if english else '主要導覽'}">
        <a href="privacy{suffix}.html"{' aria-current="page"' if topic == 'privacy' else ''}>{privacy}</a>
        <a href="support{suffix}.html"{' aria-current="page"' if topic == 'support' else ''}>{support}</a>
        <a class="language" href="{other_page}" lang="{'zh-Hant' if english else 'en'}">{'繁體中文' if english else 'English'}</a>
      </nav>
    </div>
  </header>
  <main id="main" class="wrap" tabindex="-1">
    <div class="hero">
      <p class="eyebrow">VIOLIN TRAINER</p>
      <h1>{title}</h1>
      <div class="meta"><p>{'Updated:' if english else '更新日期：'} {e(content['updatedAt'])}</p>{developer}</div>
      <p class="intro">{e(doc['introduction'])}</p>
      <p>{e(t['advertisingStatus']['website'])}</p>
      {draft}
    </div>
    <div class="layout">
      <aside class="contents" aria-label="{'Contents' if english else '內容導覽'}">
        <h2>{'Contents' if english else '內容導覽'}</h2><ol>{toc}</ol>
      </aside>
      <article aria-label="{title}">{sections}{hosting}{contact}</article>
    </div>
  </main>
  <footer class="wrap"><span>Violin Trainer</span><a href="privacy{suffix}.html">{privacy}</a><a href="support{suffix}.html">{support}</a></footer>
</body>
</html>
'''
    output['index.html'] = '''<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0; url=privacy.html">
<meta name="robots" content="noindex"><title>Violin Trainer 隱私政策</title></head>
<body><p><a href="privacy.html">隱私政策</a> · <a href="privacy-en.html" lang="en">Privacy policy</a></p></body></html>
'''
    return {name: '\n'.join(line.rstrip() for line in value.splitlines()) + '\n' for name, value in output.items()}


class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.forbidden = [], [], []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('script', 'iframe', 'form', 'object', 'embed', 'audio', 'video') or any(key.startswith('on') for key in attrs):
            self.forbidden.append(tag)
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append((tag, attrs[key]))


def check_site(root, content):
    public = root / 'public'
    errors = []
    if public.is_symlink() or not public.is_dir():
        return ['Public artifact must be a real directory inside the website package']
    actual = {p.relative_to(public).as_posix() for p in public.rglob('*') if p.is_file() or p.is_symlink()}
    if actual != PUBLIC_FILES:
        errors.append('Public file allowlist mismatch: ' + repr(sorted(actual ^ PUBLIC_FILES)))
    documents = {}
    for name, expected in render(content).items():
        path = public / name
        if not path.is_file() or path.is_symlink():
            errors.append('Missing/non-regular page: ' + name)
            continue
        text = path.read_text(encoding='utf-8')
        if text != expected:
            errors.append('Outdated generated page: ' + name)
        doc = Document(); doc.feed(text)
        documents[name] = doc
        if len(doc.ids) != len(set(doc.ids)) or doc.forbidden:
            errors.append('Duplicate IDs or active/embedded content: ' + name)
    for path in public.rglob('*'):
        if path.is_symlink() or (path.is_file() and path.stat().st_nlink != 1):
            errors.append('Public artifact cannot contain links: ' + str(path.relative_to(public)))
    for name, doc in documents.items():
        for tag, href in doc.links:
            url = urlsplit(href)
            if url.scheme:
                if tag != 'a' or not (href == GITHUB_PRIVACY or href.startswith('mailto:')):
                    errors.append('Unexpected external resource: ' + href)
                continue
            target = unquote(url.path) or name
            if url.netloc or target not in PUBLIC_FILES or not (public / target).is_file():
                errors.append('Broken/non-relative link in ' + name + ': ' + href)
            elif url.fragment and (target not in documents or unquote(url.fragment) not in documents[target].ids):
                errors.append('Broken fragment in ' + name + ': ' + href)
    css = public / 'styles.css'
    if css.is_file() and re.search(r'@import|url\s*\(', css.read_text(encoding='utf-8'), re.I):
        errors.append('CSS must not load additional resources')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Regenerate HTML from content.json')
    parser.add_argument('--check', action='store_true', help='Read-only validation (default)')
    parser.add_argument('--require-public-details', action='store_true', help='Require deployment identity and public contacts/URLs')
    parser.add_argument('--repository', help='Expected GitHub owner/repository, used in Actions')
    args = parser.parse_args()
    if args.write and args.check:
        parser.error('--write and --check are mutually exclusive')
    content = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
    deployment = json.loads((ROOT / 'deployment.json').read_text(encoding='utf-8'))
    if args.write:
        (ROOT / 'public').mkdir(exist_ok=True)
        for name, text in render(content).items():
            (ROOT / 'public' / name).write_text(text, encoding='utf-8')
    errors = check_site(ROOT, content)
    if errors:
        print('\n'.join(errors)); return 1
    missing = publication_errors(content, deployment, args.repository)
    if args.require_public_details and missing:
        print('Publication blocked:\n' + '\n'.join(missing)); return 2
    print('6 public files verified; bilingual content, relative links and artifact allowlist passed.')
    print('Publication details incomplete (local draft).' if missing else 'Publication details complete; no deployment performed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
