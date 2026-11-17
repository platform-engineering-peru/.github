"""Check the profile's GitHub HTML contract and self-contained brand assets."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
from base64 import b64decode
import hashlib
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'profile/assets'
class Profile(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs, self.links, self.images = [], [], 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        assert tag in {'p','a','picture','source','img','br','h3','strong','code','sub','details','summary'}, tag
        assert not any(k == 'style' or k.startswith('on') for k in attrs), attrs
        if tag == 'a':
            self.links.append(attrs['href'])
            assert attrs['href'].startswith(('https://', 'mailto:'))
        if tag == 'img':
            self.images += 1
            assert 'alt' in attrs
        for key in ('src', 'srcset'):
            if key in attrs:
                value = attrs[key]
                assert value.startswith('https://raw.githubusercontent.com/platform-engineering-peru/.github/')
                file = ASSETS / urlparse(value).path.rsplit('/',1)[-1]
                assert file.is_file(), file
                self.refs.append(file)

profile = Profile()
profile.feed((ROOT/'profile/README.md').read_text())
assert profile.images == 7
assert len(set(profile.refs)) == 9
assert len(profile.links) >= 15
for file in set(profile.refs):
    svg = ET.parse(file).getroot()
    assert svg.attrib.get('viewBox')
    assert svg.find('{http://www.w3.org/2000/svg}title') is not None
    assert file.stat().st_size < 2_000_000
    for el in svg.iter():
        assert el.tag.rsplit('}',1)[-1] not in ('script','foreignObject','animate','animateTransform')
        href = el.attrib.get('href')
        if href:
            assert href.startswith('data:image/')
            raw=b64decode(href.split(',',1)[1])
            originals = [(ASSETS/n).read_bytes() for n in ('official-mark.png','ukuku.webp')]
            assert raw in originals, 'Embedded brand artwork was modified'
print(f'Validated {profile.images} image components, {len(set(profile.refs))} SVG assets, and {len(profile.links)} links.')
print('No scripts, inline CSS, remote SVG resources, or altered brand artwork.')
