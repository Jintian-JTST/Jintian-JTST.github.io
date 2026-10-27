"""Build editable, self-contained concept covers from vectors and curated photos.

Uses only Python's standard library. Original photographs and result plots are
never rewritten. These illustrations are presentation artwork, not result plots.
"""
from pathlib import Path
import base64
import html
import math

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets/projects/covers"
OUT.mkdir(parents=True, exist_ok=True)


def photo(relative):
    path = ROOT / relative
    mime = "image/jpeg" if path.suffix == ".jpg" else "image/png"
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def line(points, **attrs):
    attrs = " ".join(f'{key.replace("_", "-")}="{value}"' for key, value in attrs.items())
    return '<polyline points="' + " ".join(f"{x:.2f},{y:.2f}" for x, y in points) + f'" {attrs}/>'


def cover(filename, title, code, art, defs="", accent="#8ce7df"):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000" viewBox="0 0 1600 1000" role="img" aria-labelledby="title desc">
<title id="title">{html.escape(title)}</title>
<desc id="desc">Concept illustration for a project cover. Photographs, where included, are curated original project media. This is not a scientific result plot or an application screenshot.</desc>
<defs>
 <radialGradient id="bg"><stop stop-color="#1b3033"/><stop offset=".65" stop-color="#101a20"/><stop offset="1" stop-color="#0c1116"/></radialGradient>
 <linearGradient id="silver" x2=".8" y2="1"><stop stop-color="#e7f2ef"/><stop offset=".48" stop-color="#7faaa7"/><stop offset=".54" stop-color="#d5f3e9"/><stop offset="1" stop-color="#456b70"/></linearGradient>
 <linearGradient id="fade"><stop stop-color="{accent}" stop-opacity="0"/><stop offset=".35" stop-color="{accent}"/><stop offset="1" stop-color="{accent}" stop-opacity=".2"/></linearGradient>
 <pattern id="grid" width="80" height="80" patternUnits="userSpaceOnUse"><path d="M80 0H0V80" fill="none" stroke="#a7d4cf" stroke-opacity=".055" stroke-width="1"/></pattern>
 <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="13"/></filter>
 {defs}
</defs>
<rect width="1600" height="1000" fill="url(#bg)"/>
<rect x="0" y="0" width="1600" height="1000" fill="url(#grid)"/>
<ellipse cx="800" cy="550" rx="580" ry="290" fill="none" stroke="{accent}" stroke-opacity=".06" transform="rotate(-18 800 550)"/>
<path d="M64 112V64h48M1488 64h48v48M64 888v48h48M1488 936h48v-48" fill="none" stroke="{accent}" stroke-width="1" stroke-opacity=".35"/>
<g font-family="Consolas,monospace" font-size="16" letter-spacing="3" fill="{accent}"><text x="100" y="112">{code}</text><text x="100" y="910" opacity=".6" font-size="12">CONCEPT ILLUSTRATION</text></g>
<path d="M100 860H1500" stroke="{accent}" stroke-opacity=".12"/>
{art}
</svg>'''
    svg = "\n".join(row.rstrip() for row in svg.splitlines()) + "\n"
    (OUT / filename).write_text(svg, encoding="utf-8")
    print(filename, len(svg.encode("utf-8")))


# The wave and field geometry are deliberately uncalibrated decorative motifs.
waves = ""
for offset, opacity in [(-75, ".14"), (0, ".95"), (75, ".14")]:
    points = [(90 + i * 5.3, 500 + offset + 200 * math.exp(-i / 130) * math.sin(i / 8.5)) for i in range(205)]
    waves += line(points, fill="none", stroke="url(#fade)", stroke_width="2.5", opacity=opacity)
field = ""
for angle in range(0, 360, 60):
    field += f'<g transform="rotate({angle} 1160 500)"><ellipse cx="1240" cy="500" rx="180" ry="85" fill="none" stroke="#94cbc6" stroke-opacity=".4"/><ellipse cx="1240" cy="500" rx="130" ry="55" fill="none" stroke="#94cbc6" stroke-opacity=".2"/><circle cx="1355" cy="500" r="9" fill="#8ce7df"/><circle cx="1355" cy="500" r="20" fill="none" stroke="#8ce7df" stroke-opacity=".2"/></g>'
cover("muon-g2.svg", "Decay waveform and six-coil field concept", "01 / FIELD + TIME", f'<path d="M90 500H1490" stroke="#8ce7df" stroke-opacity=".1"/>{waves}{field}<circle cx="1160" cy="500" r="33" fill="#8ce7df" opacity=".15"/><circle cx="1160" cy="500" r="7" fill="#d4f3eb"/>')

fingers = [[(420, 765), (300, 645), (225, 525), (160, 450), (140, 355)], [(420, 765), (350, 550), (310, 380), (300, 260), (290, 170)], [(420, 765), (440, 520), (430, 330), (430, 210), (430, 110)], [(420, 765), (520, 550), (540, 380), (560, 260), (575, 190)], [(420, 765), (580, 590), (650, 470), (700, 400), (740, 370)]]
hand = ""
for finger in fingers:
    hand += line(finger, fill="none", stroke="#a8e4d7", stroke_width="3", stroke_linecap="round", stroke_linejoin="round")
    for x, y in finger:
        hand += f'<circle cx="{x}" cy="{y}" r="6" fill="#102328" stroke="#9ee5d8" stroke-width="2"/>'
hand += line([finger[1] for finger in fingers], fill="none", stroke="#8ce7df", stroke_opacity=".3")
glove = photo("assets/projects/second-touch-reality/hero-haptic-glove.jpg")
photo_art = f'<g transform="rotate(-5 1140 475)"><rect x="790" y="230" width="690" height="460" rx="15" fill="#192329" stroke="#8ce7df" stroke-opacity=".25"/><image href="{glove}" x="805" y="245" width="660" height="372" preserveAspectRatio="xMidYMid slice" clip-path="url(#gloveClip)"/><text x="825" y="660" fill="#a5bdbb" font-family="Consolas,monospace" font-size="14" letter-spacing="2">TEAM PROTOTYPE / ORIGINAL PHOTO</text></g>'
cover("second-touch.svg", "Hand tracking and the team haptic glove", "02 / HUMAN + MACHINE", hand + photo_art, '<clipPath id="gloveClip"><rect x="805" y="245" width="660" height="372" rx="8"/></clipPath>')

logo = photo("assets/projects/one-tap-reality/hero-logo.png")
album = f'''<g transform="rotate(11 925 510)"><rect x="660" y="235" width="510" height="570" rx="12" fill="#203338" stroke="#76968f" stroke-opacity=".3"/></g>
<g transform="rotate(-9 880 495)"><rect x="600" y="185" width="510" height="610" rx="12" fill="#d4c6ac"/><rect x="620" y="205" width="470" height="570" rx="4" fill="#eee5d5"/>
<image href="{logo}" x="760" y="225" width="190" height="190"/>
<rect x="655" y="425" width="400" height="255" fill="#a5bcb0"/>
<circle cx="950" cy="480" r="30" fill="#e9d8b6"/>
<path d="M655 680V585l92-85 96 120 69-61 143 121" fill="#516f70"/><path d="m655 680 145-115 120 115" fill="#244c52"/>
<path d="M655 717h225m-225 20h135" stroke="#9e927f" stroke-width="4"/></g>
<path d="M120 610c150-235 300 240 455-50S730 340 800 340" stroke="#c3af90" stroke-width="2" stroke-dasharray="5 10" fill="none"/>
<g fill="#172428" stroke="#dfc5a1" stroke-width="2"><circle cx="120" cy="610" r="9"/><circle cx="370" cy="620" r="9"/><circle cx="570" cy="560" r="9"/></g>
<path d="m1250 350 80 130-80 130-80-130z" fill="none" stroke="#c7ba9f" stroke-opacity=".3"/>
<path d="M1250 400v160m-32-130v100m64-100v100" stroke="#d6c7ad" stroke-opacity=".6" stroke-width="2"/>'''
cover("one-tap.svg", "Travel album and route concept", "03 / PLACES + MEMORIES", album, accent="#d8c3a2")

apparatus = photo("assets/projects/compound-pendulum/hero-apparatus-in-water.jpg")
pendulum = f'''<path d="M150 240h620m-310-30v555" stroke="#abc1b4" stroke-opacity=".2" stroke-dasharray="3 9"/>
<path d="M460 240 655 740" stroke="url(#silver)" stroke-width="17" stroke-linecap="round"/>
<circle cx="460" cy="240" r="16" fill="#172b2c" stroke="#aecabd" stroke-width="3"/>
<g transform="rotate(-21 625 665)"><rect x="580" y="560" width="90" height="200" rx="16" fill="url(#silver)"/><circle cx="625" cy="715" r="13" fill="#1b3035"/></g>
<path d="M460 370a130 130 0 0 0 47-9" fill="none" stroke="#d3d5ad" stroke-width="2"/>
<path d="M250 685q150 50 300 0t300 0M250 710q150 50 300 0t300 0" fill="none" stroke="#8ce7df" stroke-opacity=".17"/>
<rect x="970" y="180" width="400" height="610" rx="10" fill="#172126" stroke="#abc1b4" stroke-opacity=".25"/>
<image href="{apparatus}" x="987" y="195" width="366" height="580" preserveAspectRatio="xMidYMid meet"/>
<path d="M1420 245v475m-10-475h20m-20 475h20" stroke="#b7d5c1" stroke-opacity=".3"/>'''
cover("pendulum.svg", "Pendulum geometry and original experimental apparatus", "04 / MOTION + MEDIUM", pendulum, accent="#b7d5c1")

orbits = ""
for angle in [-25, 30, 80]:
    orbits += f'<ellipse cx="800" cy="500" rx="505" ry="150" fill="none" stroke="#a4c7e5" stroke-width="1.5" stroke-opacity=".35" transform="rotate({angle} 800 500)"/>'
space = f'''<path d="M250 725 1310 440M800 150v660M410 300l780 435" fill="none" stroke="#96b4cf" stroke-opacity=".25"/>
<circle cx="800" cy="500" r="180" fill="url(#sphere)"/>
<ellipse cx="800" cy="500" rx="180" ry="63" fill="none" stroke="#b1dcdb" stroke-opacity=".2"/>
<ellipse cx="800" cy="500" rx="68" ry="180" fill="none" stroke="#b1dcdb" stroke-opacity=".2"/>
{orbits}<circle cx="1258" cy="331" r="13" fill="#cbe7e4"/><circle cx="1258" cy="331" r="36" fill="#8ce7df" opacity=".15"/>
<path d="m460 650 80-20-15 80m605-390 70-15-15 70" fill="none" stroke="#b9d9e3" stroke-width="2"/>
<g fill="#95b3c4" font-family="Consolas,monospace" font-size="22"><text x="1325" y="446">x</text><text x="805" y="135">z</text><text x="1205" y="758">y</text></g>'''
cover("visualisation.svg", "Spatial coordinates and orbital geometry", "05 / SPACE + MATHEMATICS", space, '<radialGradient id="sphere" cx=".3" cy=".2"><stop stop-color="#c2dedc"/><stop offset=".35" stop-color="#729fa9"/><stop offset="1" stop-color="#17353f"/></radialGradient>', accent="#a4c7e5")

tokens = ""
for index, y in enumerate([285, 405, 525, 645]):
    tokens += f'<rect x="140" y="{y}" width="90" height="65" rx="9" fill="#1d3941" stroke="#7ba5b4" stroke-opacity=".5"/><path d="M165 {y+25}h40m-40 15h25" stroke="#91c5d1" stroke-opacity=".4" stroke-width="3"/><path d="M250 {y+32}C430 {y+32} 370 500 555 500" fill="none" stroke="#8cb5cf" stroke-opacity=".4"/>'
layers = ""
for index in [3, 2, 1, 0]:
    x, y = 570 + index * 75, 235 - index * 14
    layers += f'<rect x="{x}" y="{y}" width="390" height="530" rx="17" fill="#11202c" fill-opacity=".9" stroke="#9ab9d2" stroke-opacity="{.7-index*.14}"/>'
matrix = ""
for row in range(5):
    for col in range(5):
        opacity = .15 + ((row * 7 + col * 3) % 8) / 11
        matrix += f'<rect x="{625+col*54}" y="{350+row*54}" width="37" height="37" rx="5" fill="#8fc1db" opacity="{opacity:.2f}"/>'
outputs = '<path d="M1190 500h165" stroke="#a0c1d9" stroke-opacity=".5"/><path d="m1345 490 10 10-10 10" fill="none" stroke="#a0c1d9"/>'
for y in [395, 495, 595]:
    outputs += f'<rect x="1390" y="{y}" width="75" height="40" rx="6" fill="#294251" stroke="#91b4cf" stroke-opacity=".4"/>'
cover("transformer.svg", "Tokens, attention matrix and decoder layers", "06 / TOKENS + ATTENTION", tokens + layers + matrix + outputs + '<path d="M625 300h280m-280 365h280" stroke="#a3d3e4" stroke-opacity=".3"/>', accent="#a8bfdc")

# A compatible cover for the separately maintained Oxford Physics library.
book = '''<g transform="rotate(-9 800 500)">
<path d="M360 270q220-55 440 45 220-100 440-45v460q-220-55-440 45-220-100-440-45z" fill="#162c34" stroke="#9ec5cd" stroke-opacity=".45" stroke-width="2"/>
<path d="M800 315v460" fill="none" stroke="#b8d9d8" stroke-opacity=".5"/>
<path d="M400 305q185-30 360 40m-360 45q185-30 360 40m-360 45q185-30 200 0m-200 160q185-30 360 40m-360 45q185-30 290 20" fill="none" stroke="#a5c3c7" stroke-opacity=".24" stroke-width="3"/>
<path d="M870 600V390m0 210h275m-255-80c60-190 100 110 155-30s85 40 115-40" fill="none" stroke="#9dd2cc" stroke-opacity=".6" stroke-width="2"/>
<circle cx="1060" cy="380" r="44" fill="none" stroke="#b6ced7" stroke-opacity=".35"/>
<path d="M400 765q185-30 360 40m80 0q175-70 360-40" fill="none" stroke="#b6ced7" stroke-opacity=".22" stroke-width="2"/>
</g><circle cx="330" cy="390" r="90" fill="none" stroke="#a5c3c7" stroke-opacity=".1"/>
<path d="M1310 350v340m-12-340h24m-24 340h24" stroke="#a5c3c7" stroke-opacity=".3"/>'''
cover("oxford-physics.svg", "Open physics notebook and diagrams", "07 / NOTES + EXPLORATION", book, accent="#b6ced7")

(OUT / "README.md").write_text('''# Project concept covers

Seven SVG presentation illustrations, generated by `python scripts/build-covers.py`.
Each uses editable vector geometry. SecondTouchReality and Compound Pendulum
embed the original curated project photograph; OneTapReality embeds its original
team logo. The original raster assets remain unchanged.

The waveforms, field lines, album, orbits and attention patterns are decorative
concept illustrations, not scientific result plots or application screenshots.
Original evidence is linked separately on each project page.
''', encoding="utf-8")
