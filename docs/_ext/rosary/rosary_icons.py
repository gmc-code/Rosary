"""Iconography for the twenty mysteries, drawn as small inline SVGs.

Every icon uses a 100 x 100 viewBox and these classes, which rosary.css
colours from the set's colour so each set has its own palette:

    ri-line   outline strokes (set colour)
    ri-fill   solid shapes in the set colour
    ri-soft   pale tint of the set colour
    ri-gold   gold (light, halos, stars, crowns)
    ri-white  white (hosts, linen, the dove)
    ri-dark   dark shapes (the empty tomb, the darkened sun)
    ri-wine   deep red (wine, blood, fire)
    ri-green  leaves
"""

import math


# ---------------------------------------------------------------- helpers

def _f(value):
    return ('%.1f' % value).rstrip('0').rstrip('.')


def star(cx, cy, r_out, r_in, points=5, cls='ri-gold', rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append('%s,%s' % (_f(cx + r * math.cos(a)), _f(cy + r * math.sin(a))))
    return '<polygon class="%s" points="%s"/>' % (cls, ' '.join(pts))


def rays(cx, cy, r1, r2, count, start=0, end=360, cls='ri-gold-line'):
    out = []
    span = end - start
    full = abs(span - 360) < 1e-6
    for i in range(count):
        frac = i / count if full else (i / (count - 1) if count > 1 else 0.5)
        a = math.radians(start + span * frac)
        out.append('<line class="%s" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (
            cls, _f(cx + r1 * math.cos(a)), _f(cy + r1 * math.sin(a)),
            _f(cx + r2 * math.cos(a)), _f(cy + r2 * math.sin(a))))
    return ''.join(out)


def dove(cx, cy, s=1.0):
    """The Holy Spirit as a dove, wings spread, descending (head down)."""
    return (
        '<g transform="translate(%s %s) scale(%s)">'
        '<path class="ri-white ri-outline" d="M-2,-2 C-8,-12 -20,-16 -27,-12 '
        'C-22,-11 -18,-8 -16,-5 C-20,-5 -23,-3 -24,0 C-16,-2 -9,0 -3,4 Z"/>'
        '<path class="ri-white ri-outline" d="M2,-2 C8,-12 20,-16 27,-12 '
        'C22,-11 18,-8 16,-5 C20,-5 23,-3 24,0 C16,-2 9,0 3,4 Z"/>'
        '<path class="ri-white ri-outline" d="M-3,-6 L0,-15 L3,-6 Z"/>'
        '<ellipse class="ri-white ri-outline" cx="0" cy="1" rx="4.5" ry="8"/>'
        '<circle class="ri-white ri-outline" cx="0" cy="11" r="3.6"/>'
        '</g>' % (_f(cx), _f(cy), s))


def halo(cx, cy, r):
    return '<circle class="ri-gold-ring" cx="%s" cy="%s" r="%s"/>' % (cx, cy, r)


def chalice(cx, top, s=1.0, wine=False):
    cup = 'ri-wine' if wine else 'ri-gold'
    return (
        '<g transform="translate(%s %s) scale(%s)">'
        '<path class="%s ri-outline" d="M-16,0 L16,0 C16,15 9,23 0,23 C-9,23 -16,15 -16,0 Z"/>'
        '<rect class="ri-gold ri-outline" x="-2.5" y="23" width="5" height="12"/>'
        '<ellipse class="ri-gold ri-outline" cx="0" cy="29" rx="5" ry="3"/>'
        '<path class="ri-gold ri-outline" d="M-14,44 C-11,36 11,36 14,44 Z"/>'
        '</g>' % (_f(cx), _f(top), s, cup))


def cloud(cx, cy, s=1.0, cls='ri-white'):
    return (
        '<g transform="translate(%s %s) scale(%s)" class="%s ri-outline">'
        '<path d="M-22,6 C-28,6 -28,-3 -21,-3 C-21,-11 -10,-13 -6,-7 '
        'C-3,-15 10,-15 11,-6 C17,-10 25,-5 22,1 C28,2 27,6 22,6 Z"/>'
        '</g>' % (_f(cx), _f(cy), s, cls))


def flame(cx, base, h=22, cls='ri-wine'):
    w = h * 0.36
    return ('<path class="%s ri-outline" d="M%s,%s C%s,%s %s,%s %s,%s '
            'C%s,%s %s,%s %s,%s Z"/>' % (
                cls, _f(cx), _f(base),
                _f(cx - w), _f(base - h * 0.35), _f(cx - w * 0.4), _f(base - h * 0.7), _f(cx), _f(base - h),
                _f(cx + w * 0.4), _f(base - h * 0.7), _f(cx + w), _f(base - h * 0.35), _f(cx), _f(base)))


def cross(cx, top, h, w, t=5, cls='ri-fill', rotate=0):
    arm_y = top + h * 0.28
    return (
        '<g transform="rotate(%s %s %s)" class="%s ri-outline">'
        '<rect x="%s" y="%s" width="%s" height="%s"/>'
        '<rect x="%s" y="%s" width="%s" height="%s"/>'
        '</g>' % (rotate, _f(cx), _f(top + h / 2), cls,
                  _f(cx - t / 2), _f(top), t, h,
                  _f(cx - w / 2), _f(arm_y - t / 2), w, t))


def bird(cx, cy, flip=False, cls='ri-white'):
    """A small turtledove, side on, facing right (or left when flipped)."""
    sx = -1 if flip else 1
    return (
        '<g transform="translate(%s %s) scale(%s 1)">'
        '<path class="%s ri-outline" d="M-16,2 C-12,-7 0,-10 7,-7 C9,-12 15,-13 18,-9 '
        'L23,-7 L18,-5 C17,3 9,9 -2,9 L-18,10 L-14,5 Z"/>'
        '<path class="ri-soft ri-outline" d="M-6,0 C-2,-6 6,-6 9,-2 C5,4 -2,5 -6,0 Z"/>'
        '<circle class="ri-dark" cx="15" cy="-9" r="1.3"/>'
        '</g>' % (_f(cx), _f(cy), sx, cls))


def figure(cx, top, s=1.0, robe='ri-fill', mantle_halo=True):
    """A simple robed figure seen from the front, head at the top."""
    parts = ['<g transform="translate(%s %s) scale(%s)">' % (_f(cx), _f(top), s)]
    if mantle_halo:
        parts.append(halo(0, 8, 11))
    parts.append('<circle class="ri-soft ri-outline" cx="0" cy="8" r="7"/>')
    parts.append('<path class="%s ri-outline" d="M-8,16 C-14,30 -16,46 -15,58 '
                 'L15,58 C16,46 14,30 8,16 C4,20 -4,20 -8,16 Z"/>' % robe)
    parts.append('</g>')
    return ''.join(parts)


def _sector(r1, r2, a0, a1, cls):
    """An annular sector (one pane of a rose window) centred on (50, 50)."""
    def pt(r, a):
        a = math.radians(a)
        return _f(50 + r * math.cos(a)), _f(50 + r * math.sin(a))
    x1, y1 = pt(r1, a0)
    x2, y2 = pt(r2, a0)
    x3, y3 = pt(r2, a1)
    x4, y4 = pt(r1, a1)
    big = 1 if (a1 - a0) > 180 else 0
    if r1 == 0:
        return ('<path class="%s" d="M50,50 L%s,%s A%s,%s 0 %d 1 %s,%s Z"/>'
                % (cls, x2, y2, r2, r2, big, x3, y3))
    return ('<path class="%s" d="M%s,%s L%s,%s A%s,%s 0 %d 1 %s,%s L%s,%s A%s,%s 0 %d 0 %s,%s Z"/>'
            % (cls, x1, y1, x2, y2, r2, r2, big, x3, y3, x4, y4, r1, r1, big, x1, y1))


def _rose_window():
    """Background panes for the stained-glass style (hidden in other styles)."""
    parts = ['<g class="ri-glass-bg">']
    parts.append('<circle class="ri-pane-a" cx="50" cy="50" r="17"/>')
    for i in range(8):
        parts.append(_sector(17, 34, i * 45 - 90, (i + 1) * 45 - 90, ('ri-pane-b', 'ri-pane-c')[i % 2]))
    for i in range(12):
        parts.append(_sector(34, 75, i * 30 - 75, (i + 1) * 30 - 75, ('ri-pane-c', 'ri-pane-a', 'ri-pane-b')[i % 3]))
    parts.append('</g>')
    return ''.join(parts)


ROSE_WINDOW = _rose_window()


def svg(body, label):
    return ('<svg class="rosary-svg" viewBox="0 0 100 100" role="img" '
            'aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s%s</svg>'
            % (label, ROSE_WINDOW, body))


# ---------------------------------------------------------------- joyful

def annunciation():
    lily = (
        '<path class="ri-green-line" d="M50,96 L50,52"/>'
        '<path class="ri-green ri-outline" d="M50,84 C40,80 34,72 34,64 C42,68 48,74 50,84 Z"/>'
        '<path class="ri-green ri-outline" d="M50,76 C60,72 66,64 66,56 C58,60 52,66 50,76 Z"/>'
    )
    blooms = ''
    for x, y, r in ((50, 52, 0), (40, 62, -30), (60, 62, 30)):
        blooms += (
            '<g transform="rotate(%s %s %s)">'
            '<path class="ri-white ri-outline" d="M%s,%s C%s,%s %s,%s %s,%s '
            'C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s C%s,%s %s,%s %s,%s Z"/>'
            '</g>' % (r, x, y,
                      x, y, x - 7, y - 3, x - 10, y - 12, x - 7, y - 17,
                      x - 4, y - 11, x - 2, y - 15, x, y - 19,
                      x + 2, y - 15, x + 4, y - 11, x + 7, y - 17,
                      x + 10, y - 12, x + 7, y - 3, x, y))
    return rays(50, 16, 8, 42, 7, 60, 120) + dove(50, 16, 0.9) + lily + blooms


def visitation():
    return (
        '<path class="ri-soft" d="M0,92 C25,82 75,82 100,92 L100,100 L0,100 Z"/>'
        + figure(36, 22, 1.0, 'ri-fill')
        + figure(64, 22, 1.0, 'ri-soft-strong')
        + '<path class="ri-wine ri-outline" d="M50,16 C46,10 40,14 44,19 L50,25 '
          'L56,19 C60,14 54,10 50,16 Z"/>'
    )


def nativity():
    return (
        rays(50, 16, 9, 18, 8)
        + star(50, 16, 9, 3.5, 4, 'ri-gold') + star(50, 16, 6, 2.5, 4, 'ri-gold', -45)
        + '<line class="ri-gold-dash" x1="50" y1="27" x2="50" y2="48"/>'
        + '<line class="ri-line" x1="24" y1="60" x2="40" y2="92"/>'
          '<line class="ri-line" x1="40" y1="60" x2="24" y2="92"/>'
          '<line class="ri-line" x1="60" y1="60" x2="76" y2="92"/>'
          '<line class="ri-line" x1="76" y1="60" x2="60" y2="92"/>'
        + '<path class="ri-gold ri-outline" d="M22,60 L78,60 L70,76 L30,76 Z"/>'
        + '<path class="ri-gold-line" d="M24,60 l3,-5 l3,5 l3,-5 l3,5 M64,60 l3,-5 l3,5 l3,-5 l3,5"/>'
        + halo(37, 54, 8)
        + '<ellipse class="ri-white ri-outline" cx="52" cy="56" rx="14" ry="6"/>'
        + '<circle class="ri-soft ri-outline" cx="37" cy="54" r="5"/>'
        + '<path class="ri-line-thin" d="M44,53 L48,59 M50,52 L54,60 M56,52 L60,59"/>'
    )


def presentation():
    return (
        rays(50, 30, 10, 20, 9, 200, 340)
        + bird(30, 46) + bird(70, 46, flip=True)
        + '<path class="ri-gold ri-outline" d="M20,64 L80,64 C78,84 66,92 50,92 C34,92 22,84 20,64 Z"/>'
        + '<path class="ri-line-thin" d="M24,72 L76,72 M28,80 L72,80 M36,64 L40,91 M50,64 L50,92 M64,64 L60,91"/>'
        + '<path class="ri-line" d="M24,64 C30,52 70,52 76,64" fill="none"/>'
    )


def finding():
    cols = ''.join('<rect class="ri-soft ri-outline" x="%d" y="40" width="7" height="30"/>' % x
                   for x in (22, 36, 57, 71))
    return (
        '<path class="ri-fill ri-outline" d="M16,36 L50,14 L84,36 Z"/>'
        + '<circle class="ri-gold" cx="50" cy="28" r="4"/>'
        + '<rect class="ri-fill ri-outline" x="16" y="35" width="68" height="6"/>'
        + cols
        + '<rect class="ri-fill ri-outline" x="12" y="70" width="76" height="5"/>'
          '<rect class="ri-fill ri-outline" x="8" y="75" width="84" height="5"/>'
        + '<rect class="ri-white ri-outline" x="30" y="81" width="40" height="13"/>'
          '<rect class="ri-gold ri-outline" x="26" y="79" width="6" height="17" rx="3"/>'
          '<rect class="ri-gold ri-outline" x="68" y="79" width="6" height="17" rx="3"/>'
          '<path class="ri-line-thin" d="M35,85 L65,85 M35,89 L60,89"/>'
    )


# ---------------------------------------------------------------- luminous

def baptism():
    ribs = rays(50, 58, 4, 24, 7, 200, 340, 'ri-line-thin')
    return (
        rays(50, 14, 8, 22, 5, 50, 130)
        + dove(50, 14, 0.7)
        + '<path class="ri-gold ri-outline" d="M28,56 C30,34 70,34 72,56 C62,62 38,62 28,56 Z"/>'
        + ribs
        + '<path class="ri-gold ri-outline" d="M45,59 L55,59 L53,64 L47,64 Z"/>'
        + ''.join('<path class="ri-water ri-outline" d="M%s,%s c-3,4 -3,7 0,7 c3,0 3,-3 0,-7 Z"/>'
                  % (x, y) for x, y in ((44, 66), (50, 70), (56, 66)))
        + '<path class="ri-water-line" d="M8,84 q8,-6 16,0 t16,0 t16,0 t16,0 t16,0 t16,0"/>'
          '<path class="ri-water-line" d="M8,93 q8,-6 16,0 t16,0 t16,0 t16,0 t16,0 t16,0"/>'
    )


def _jar(x, wine):
    fill = 'ri-wine' if wine else 'ri-soft'
    return (
        '<path class="ri-soft ri-outline" d="M%s,50 C%s,58 %s,82 %s,88 L%s,88 '
        'C%s,82 %s,58 %s,50 Z"/>' % (x - 7, x - 14, x - 13, x - 8, x + 8, x + 13, x + 14, x + 7)
        + '<rect class="ri-fill ri-outline" x="%s" y="44" width="16" height="6" rx="2"/>' % (x - 8)
        + ('<path class="%s" d="M%s,60 C%s,66 %s,82 %s,86 L%s,86 C%s,82 %s,66 %s,60 Z"/>'
           % (fill, x - 11, x - 13, x - 12, x - 7, x + 7, x + 12, x + 13, x + 11)
           if wine else '')
    )


def cana():
    return (
        '<circle class="ri-gold-ring" cx="44" cy="22" r="10"/>'
        '<circle class="ri-gold-ring" cx="56" cy="22" r="10"/>'
        + _jar(24, False) + _jar(50, True) + _jar(76, False)
        + star(50, 38, 4, 1.5, 4)
    )


def proclamation():
    return (
        rays(50, 34, 16, 28, 9, 190, 350)
        + '<path class="ri-gold ri-outline" d="M32,44 L32,24 L41,34 L50,18 L59,34 L68,24 L68,44 Z"/>'
        + '<circle class="ri-wine" cx="50" cy="37" r="3"/>'
        + '<path class="ri-white ri-outline" d="M50,58 C40,52 24,52 14,56 L14,86 C24,82 40,82 50,88 Z"/>'
          '<path class="ri-white ri-outline" d="M50,58 C60,52 76,52 86,56 L86,86 C76,82 60,82 50,88 Z"/>'
        + '<path class="ri-line-thin" d="M20,63 C28,61 38,61 45,64 M20,70 C28,68 38,68 45,71 '
          'M20,77 C28,75 38,75 45,78 M55,64 C62,61 72,61 80,63 M55,71 C62,68 72,68 80,70 '
          'M55,78 C62,75 72,75 80,77"/>'
    )


def transfiguration():
    return (
        rays(48, 28, 13, 30, 16)
        + '<circle class="ri-gold" cx="48" cy="28" r="11"/>'
        + '<path class="ri-fill ri-outline" d="M4,92 L40,40 L52,54 L62,44 L96,92 Z"/>'
        + '<path class="ri-white" d="M40,40 L33,50 L38,48 L42,52 L46,46 Z"/>'
        + cloud(24, 40, 0.9) + cloud(76, 46, 0.8)
    )


def eucharist():
    return (
        rays(50, 24, 14, 26, 16)
        + '<circle class="ri-white ri-outline" cx="50" cy="24" r="12"/>'
        + '<path class="ri-line-thin" d="M50,17 L50,31 M43,24 L57,24"/>'
        + chalice(50, 44, 1.0)
        + '<path class="ri-green-line" d="M18,90 C20,76 22,64 26,54"/>'
        + ''.join('<ellipse class="ri-gold ri-outline" cx="%s" cy="%s" rx="2.4" ry="4.5" '
                  'transform="rotate(%s %s %s)"/>' % (x, y, r, x, y)
                  for x, y, r in ((24, 60, -20), (28, 64, 30), (21, 68, -20), (25, 72, 30), (19, 76, -15)))
        + ''.join('<circle class="ri-wine ri-outline" cx="%s" cy="%s" r="3.3"/>' % (x, y)
                  for x, y in ((76, 62), (82, 62), (79, 67), (73, 67), (85, 67), (76, 72), (82, 72), (79, 77)))
        + '<path class="ri-green-line" d="M79,58 C79,54 82,52 85,52"/>'
    )


# ---------------------------------------------------------------- sorrowful

def agony():
    leaves = ''.join(
        '<ellipse class="ri-green ri-outline" cx="%s" cy="%s" rx="5" ry="2.2" transform="rotate(%s %s %s)"/>'
        % (x, y, r, x, y) for x, y, r in ((72, 40, -30), (78, 48, 20), (70, 52, -40), (80, 58, 30), (74, 64, -20)))
    return (
        '<path class="ri-gold" transform="translate(4 8)" d="M24,12 A12,12 0 1 0 34,30 A9,9 0 1 1 24,12 Z"/>'
        + star(46, 18, 3, 1.2) + star(58, 26, 2.5, 1)
        + '<path class="ri-soft ri-outline" d="M10,94 C10,80 20,70 36,70 C46,66 62,66 70,72 C84,72 92,82 92,94 Z"/>'
        + chalice(46, 36, 0.85, wine=True)
        + '<path class="ri-green-line" d="M66,72 C70,60 74,46 74,34"/>' + leaves
    )


def scourging():
    rope = ''.join('<path class="ri-wine-line" d="M38,%s C46,%s 54,%s 62,%s"/>' % (y, y - 4, y - 4, y - 8)
                   for y in (48, 56, 64))
    return (
        '<rect class="ri-soft ri-outline" x="40" y="22" width="20" height="62"/>'
        + '<path class="ri-line-thin" d="M45,24 L45,82 M50,24 L50,82 M55,24 L55,82"/>'
        + '<rect class="ri-fill ri-outline" x="32" y="14" width="36" height="8" rx="2"/>'
          '<rect class="ri-fill ri-outline" x="36" y="10" width="28" height="5"/>'
          '<rect class="ri-fill ri-outline" x="34" y="84" width="32" height="5"/>'
          '<rect class="ri-fill ri-outline" x="30" y="89" width="40" height="6"/>'
        + rope
        + '<path class="ri-wine-line" d="M62,56 C70,60 74,70 70,80 C68,86 74,90 80,88"/>'
    )


def crowning():
    thorns = ''
    for i in range(16):
        a = math.radians(i * 22.5 + 8)
        x = 50 + 30 * math.cos(a)
        y = 54 + 13 * math.sin(a)
        dx, dy = 6 * math.cos(a + 0.6), 6 * math.sin(a + 0.6)
        thorns += '<line class="ri-line" x1="%s" y1="%s" x2="%s" y2="%s"/>' % (
            _f(x), _f(y), _f(x + dx), _f(y + dy))
    return (
        '<line class="ri-gold-line" x1="18" y1="14" x2="82" y2="90"/>'
        '<path class="ri-gold" d="M16,10 C20,6 24,10 22,16 Z"/>'
        + '<path class="ri-line" d="M20,54 C24,36 76,36 80,54 C76,72 24,72 20,54 Z" fill="none"/>'
          '<path class="ri-line" d="M20,56 C26,40 74,42 80,52 C78,70 26,70 20,56 Z" fill="none"/>'
          '<path class="ri-line" d="M22,50 C30,70 72,70 80,58" fill="none"/>'
        + thorns
        + ''.join('<path class="ri-wine" d="M%s,%s c-2,3 -2,5 0,5 c2,0 2,-2 0,-5 Z"/>' % (x, y)
                  for x, y in ((34, 74), (52, 78), (68, 73)))
    )


def carrying():
    return (
        '<path class="ri-soft" d="M0,96 C30,92 60,74 100,52 L100,100 L0,100 Z"/>'
        + '<path class="ri-line-dash" d="M6,92 C34,86 62,70 96,52"/>'
        + cross(52, 16, 64, 40, 7, 'ri-fill', -28)
        + ''.join('<ellipse class="ri-line-fill" cx="%s" cy="%s" rx="2.2" ry="3.6" transform="rotate(60 %s %s)"/>'
                  % (x, y, x, y) for x, y in ((16, 88), (24, 84), (32, 82)))
    )


def crucifixion():
    return (
        '<circle class="ri-dark" cx="74" cy="24" r="8"/>'
        '<circle class="ri-gold-ring" cx="74" cy="24" r="10"/>'
        + '<path class="ri-soft ri-outline" d="M0,96 C16,80 34,70 50,70 C66,70 84,80 100,96 Z"/>'
        + cross(22, 46, 34, 20, 4, 'ri-fill')
        + cross(78, 46, 34, 20, 4, 'ri-fill')
        + cross(50, 12, 62, 36, 6, 'ri-fill')
        + '<rect class="ri-white ri-outline" x="42" y="13" width="16" height="7"/>'
        + '<text class="ri-text" x="50" y="18.6" text-anchor="middle">INRI</text>'
    )


# ---------------------------------------------------------------- glorious

def resurrection():
    return (
        rays(52, 52, 26, 48, 13, 190, 350)
        + '<path class="ri-soft ri-outline" d="M6,92 C6,62 24,44 50,44 C76,44 94,62 94,92 Z"/>'
        + '<path class="ri-dark ri-outline" d="M36,92 L36,72 C36,62 44,58 50,58 C56,58 64,62 64,72 L64,92 Z"/>'
        + '<path class="ri-white" d="M42,90 C44,84 52,82 58,86 L58,90 Z"/>'
        + '<circle class="ri-fill ri-outline" cx="80" cy="80" r="14"/>'
        + '<path class="ri-line-thin" d="M72,72 C78,76 82,84 80,92"/>'
        + '<path class="ri-green-line" d="M18,92 C18,84 20,80 22,76 M26,92 C25,86 28,82 30,80"/>'
    )


def ascension():
    return (
        cloud(32, 26, 0.85) + cloud(68, 24, 0.85) + cloud(50, 32, 1.0)
        + rays(50, 96, 22, 58, 9, 230, 310)
        + '<path class="ri-soft ri-outline" d="M0,96 C20,82 34,76 50,76 C66,76 80,82 100,96 Z"/>'
        + '<path class="ri-fill" d="M40,86 C38,80 44,76 46,82 C47,86 46,90 43,90 C41,90 41,88 40,86 Z"/>'
          '<path class="ri-fill" d="M60,86 C62,80 56,76 54,82 C53,86 54,90 57,90 C59,90 59,88 60,86 Z"/>'
    )


def pentecost():
    return (
        rays(50, 22, 12, 48, 9, 30, 150)
        + dove(50, 22, 1.0)
        + ''.join(flame(x, 88 - (4 if x == 50 else 0), 26 if x == 50 else 22,
                        'ri-wine' if i % 2 == 0 else 'ri-gold')
                  for i, x in enumerate((18, 34, 50, 66, 82)))
        + ''.join(flame(x, 86, 11, 'ri-gold') for x in (18, 50, 82))
    )


def assumption():
    return (
        rays(50, 40, 22, 46, 15, 180, 360)
        + figure(50, 10, 1.05, 'ri-fill')
        + '<path class="ri-gold ri-outline" d="M26,74 C34,86 66,86 74,74 C66,80 34,80 26,74 Z"/>'
        + cloud(22, 88, 1.0) + cloud(78, 88, 1.0) + cloud(50, 92, 1.2)
    )


def coronation():
    stars = ''.join(star(50 + 38 * math.cos(math.radians(i * 30 - 90)),
                         52 + 38 * math.sin(math.radians(i * 30 - 90)), 5, 2)
                    for i in range(12))
    return (
        stars
        + '<path class="ri-gold ri-outline" d="M26,66 L22,36 L36,50 L50,28 L64,50 L78,36 L74,66 Z"/>'
        + '<rect class="ri-gold ri-outline" x="25" y="64" width="50" height="9" rx="2"/>'
        + '<circle class="ri-wine" cx="50" cy="68.5" r="3"/>'
          '<circle class="ri-fill" cx="38" cy="68.5" r="2.4"/><circle class="ri-fill" cx="62" cy="68.5" r="2.4"/>'
        + '<circle class="ri-white ri-outline" cx="22" cy="35" r="3"/>'
          '<circle class="ri-white ri-outline" cx="50" cy="27" r="3"/>'
          '<circle class="ri-white ri-outline" cx="78" cy="35" r="3"/>'
    )


ICONS = {
    'joyful': (annunciation, visitation, nativity, presentation, finding),
    'luminous': (baptism, cana, proclamation, transfiguration, eucharist),
    'sorrowful': (agony, scourging, crowning, carrying, crucifixion),
    'glorious': (resurrection, ascension, pentecost, assumption, coronation),
}


def icon(set_key, index, label):
    """SVG markup for mystery ``index`` (0-4) of ``set_key``."""
    return svg(ICONS[set_key][index](), label)
