"""rosary - a Sphinx directive for praying and teaching the Rosary.

All twenty mysteries are built in, in four sets of five (Joyful, Luminous,
Sorrowful, Glorious).  Each mystery has its own icon, its fruit and ten
scripture references, one for each Hail Mary of the decade.

    .. rosary::                     all four sets, opening on today's set

    .. rosary:: today               only the set prayed today

    .. rosary:: sorrowful           one set of five mysteries

    .. rosary:: glorious
        :mystery: 3                 one mystery (Pentecost)

Options
    Options that match a menu in the reader's Options panel (icons, nav-icons,
    layout, pictures, virtues, under, verses, read, extra-prayers, fatima) set this page's starting
    choice.  When one is left out, the site's starting choice from conf.py is
    used; those are built in (see setup() at the end of this file) and are
    shown in [brackets] below.  A reader's own choices, saved in their
    browser, take over on later visits.

    :title:          heading above the block
    :mystery:        1-5, show only that mystery of the named set (without
                     the opening and closing prayers)
    :open:           set to open first when all four are shown (default: today)
    :bible-version:  BibleGateway version code for the reference links
                     (default NRSVCE); "none" for plain text references
    :prayers:        show the words of the prayers on each bead from the start
    :no-beads:       leave out the beads, buttons and opening and closing
                     prayers (reference lists only)
    :no-captions:    references only, without the short summary of each passage
    :no-scripture:   leave out the verse text under each reference
    :no-audio:       leave out the read-aloud buttons and options
    :icons:          picture style: classic, stained, gold, photo (the first
                     picture folder) or photo-<key> for another folder in
                     rosary_image_sets, e.g. photo-sg  [photo-sg]
    :images:         folder of pictures for this rosary, instead of the site's
                     rosary_images folder (default /_static/rosary-images,
                     which holds the traditional paintings); "none" to turn
                     pictures off.  Pictures are named joyful-1.png ...
                     glorious-5.png, opening and closing (.png, .jpg, .jpeg,
                     .webp, .gif or .svg); any that are missing use the drawn
                     icon.  A page with :images: starts on them unless
                     :icons: says otherwise.  Optional full/joyful-1.jpg ...
                     are the whole paintings, shown when a picture is
                     clicked.  A credits.txt in the folder (lines such as
                     "joyful-1: Fra Angelico, The Annunciation", or
                     "opening: ...") adds a caption under each title
    :no-picker:      leave out the Pictures, Mystery picker, Layout,
                     Scripture verses and Opening & closing menus
    :extra-prayers:  the opening and closing prayers: off, on (Sign of the
                     Cross, Creed, Our Father, three Hail Marys, Glory Be;
                     Hail Holy Queen, versicle, Rosary Prayer, Sign of the
                     Cross) or full (also the Prayer to St Michael and the
                     Memorare)  [on]
    :fatima:         yes or no: the Fatima prayer (O my Jesus) after the
                     Glory Be at the end of each decade  [yes]
    :hide-title:     hide the page's main heading (it still names the page in
                     the menu and the browser tab)
    :nav-icons:      style of the small pictures in the mystery picker: same
                     (as the main pictures), classic, stained, gold, photo or
                     photo-<key>  [classic]
    :layout:         auto (picks desktop, ipad or iphone from the width of
                     the screen), desktop (a large picture on the left, with
                     the details in a column beside it), ipad (a
                     tablet-sized picture on the left, with the title, beads
                     and the ten steps beside it) or iphone (the picture on
                     top, with smaller buttons and the details below)  [auto]
    :pictures:       yes or no: show the main picture of each mystery  [yes]
    :virtues:        yes or no: show each mystery's virtue (fruit) under its
                     name in the mystery picker  [yes]
    :verses:         where the scripture is shown: all (under each step),
                     current (only the step being prayed, in the panel at
                     the top) or none  [current]
    :under:          what is shown under the beads: steps (the ten scripture
                     steps), meditation (a short meditation on the mystery
                     and a prayer), offering (an offering of the decade in
                     the manner of St Louis de Montfort), virtue (a
                     meditation on the mystery's fruit), intention (who and
                     what the decade is offered for), classic (a classic
                     meditation from The Rosary, 1915; rosary_classic.py) or
                     modern (a modern reflection with a question); the
                     others are in rosary_meditations.py  [steps]
    :read:           what Listen / Pray aloud read for each Hail Mary: step
                     (the one-line summary), both (summary then scripture)
                     or scripture  [step]

The page is fully readable (and prints) without JavaScript: _static/rosary.js
adds the tabs, the mystery picker, the clickable beads, the Options panel,
full screen and read-aloud.
"""

import html
import json
import os
import shutil
from pathlib import Path
from urllib.parse import quote_plus

from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.util import logging
from sphinx.util.docutils import SphinxDirective

from .rosary_data import CLOSING, DAY_NAMES, OPENING, ORDINALS, PRAYERS, SET_ORDER, SETS
from .rosary_icons import extra_icon, icon
from .rosary_classic import CLASSIC, SOURCE as CLASSIC_SOURCE
from .rosary_meditations import INTENTIONS, MEDITATIONS, MODERN, OFFERINGS, VIRTUES
from .rosary_scripture import TEXT, TRANSLATION, TRANSLATION_SHORT

logger = logging.getLogger(__name__)

SET_ALIASES = {
    'joyful': 'joyful', 'joy': 'joyful',
    'luminous': 'luminous', 'light': 'luminous',
    'sorrowful': 'sorrowful', 'sorrow': 'sorrowful',
    'glorious': 'glorious', 'glory': 'glorious',
}


def mystery_option(argument):
    value = directives.positive_int(argument)
    if not 1 <= value <= 5:
        raise ValueError('expected a mystery number from 1 to 5')
    return value


def set_option(argument):
    key = SET_ALIASES.get((argument or '').strip().lower())
    if key is None:
        raise ValueError('expected joyful, luminous, sorrowful or glorious')
    return key


ICON_STYLES = ('classic', 'stained', 'gold', 'photo')
IMAGE_EXTS = ('.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif')


def _esc(text):
    return html.escape(text, quote=True)


def days_text(days):
    names = [DAY_NAMES[d] for d in days]
    return names[0] if len(names) == 1 else ' and '.join(names)


UNDER = ('steps', 'meditation', 'virtue', 'intention', 'offering', 'classic', 'modern')   # under the beads
LAYOUTS = ('auto', 'desktop', 'ipad', 'iphone')
# layouts from earlier versions, mapped to the nearest new one
OLD_LAYOUTS = {'phone': 'ipad', 'large': 'ipad', 'side': 'desktop', 'compact': 'iphone'}


def _layout(value):
    """A layout name: auto, desktop, ipad or iphone (older names are mapped)."""
    value = (value or '').strip().lower()
    value = OLD_LAYOUTS.get(value, value)
    return value if value in LAYOUTS else 'auto'


class RosaryDirective(SphinxDirective):
    has_content = False
    optional_arguments = 1
    final_argument_whitespace = False

    option_spec = {
        'title': directives.unchanged,
        'mystery': mystery_option,
        'open': set_option,
        'bible-version': directives.unchanged,
        'prayers': directives.flag,
        'no-beads': directives.flag,
        'no-captions': directives.flag,
        'no-scripture': directives.flag,
        'no-audio': directives.flag,
        'icons': directives.unchanged,
        'images': directives.unchanged_required,
        'no-picker': directives.flag,
        'layout': lambda a: _layout(directives.choice(a, LAYOUTS + tuple(OLD_LAYOUTS))),
        'pictures': lambda a: directives.choice(a, ('yes', 'no')),
        'virtues': lambda a: directives.choice(a, ('yes', 'no')),
        'verses': lambda a: directives.choice(a, ('all', 'current', 'none')),
        'read': lambda a: directives.choice(a, ('step', 'both', 'scripture')),
        'nav-icons': directives.unchanged,
        'hide-title': directives.flag,
        'extra-prayers': lambda a: directives.choice(a, ('off', 'on', 'full')),
        'fatima': lambda a: directives.choice(a, ('yes', 'no')),
        'under': lambda a: directives.choice(a, UNDER),
    }

    def _warn(self, message, *args):
        logger.warning('rosary: ' + message, *args, location=self.get_location())

    # ------------------------------------------------------------ pieces

    def _ref_html(self, ref, caption, version, captions, scripture):
        if version:
            url = ('https://www.biblegateway.com/passage/?search=%s&version=%s'
                   % (quote_plus(ref), quote_plus(version)))
            ref_html = ('<a class="rosary-ref" href="%s" target="_blank" '
                        'rel="noopener">%s</a>' % (_esc(url), _esc(ref)))
        else:
            ref_html = '<span class="rosary-ref">%s</span>' % _esc(ref)
        cap = ('<span class="rosary-cap">%s</span>' % _esc(caption)) if captions else ''
        alt_ref, text = TEXT.get(ref, ('', ''))
        verse = ''
        if scripture and text:
            note = (' <span class="rosary-verse-src">(%s %s)</span>' % (TRANSLATION_SHORT, _esc(alt_ref))
                    if alt_ref else '')
            verse = '<span class="rosary-verse">%s%s</span>' % (_esc(text), note)
        return '<li data-ref="%s" data-cap="%s" data-text="%s">%s%s%s</li>' % (
            _esc(ref), _esc(caption), _esc(text), ref_html, cap, verse)

    def _mystery_html(self, key, index, version, captions, scripture, beads, active):
        data = SETS[key]
        m = data['mysteries'][index]
        ordinal = '%s %s Mystery' % (ORDINALS[index], data['name'])
        refs = ''.join(self._ref_html(r, c, version, captions, scripture) for r, c in m['refs'])
        meditation = self._under_html(key, index)
        decade = ('<div class="rosary-decade" aria-label="Beads of the decade"></div>'
                  '<div class="rosary-controls"></div>'
                  '<div class="rosary-now" aria-live="polite"></div>') if beads else ''
        return (
            '<article class="rosary-mystery%s" data-index="%d">'
            '<div class="rosary-head">'
            '<div class="rosary-icon%s">%s</div>'
            '<div><p class="rosary-num">%s</p>'
            '<h4 class="rosary-mystery-title">%s</h4>'
            '<p class="rosary-fruit">Fruit of the mystery: <strong>%s</strong></p>%s</div>'
            '</div>%s'
            '<div class="rosary-under-wrap"><ol class="rosary-refs">%s</ol>%s</div>'
            '</article>' % (
                ' rosary-active' if active else '', index,
                ' rosary-has-photo' if self._photo(key, index) else '',
                icon(key, index, _esc(m['title'])) + self._photo_html(key, index, m['title']),
                _esc(ordinal), _esc(m['title']), _esc(m['fruit']),
                self._credit_html(key, index), decade, refs, meditation))

    def _under_html(self, key, index):
        """The alternatives to the ten steps: a meditation, a Montfort-style offering,
        a classic (1915) meditation and a modern reflection.  CSS shows the one chosen
        under "Under the beads"; rosary.js reads the parts marked rosary-say aloud."""
        def box(kind, label, inner):
            return ('<div class="rosary-under-box rosary-%s"><p class="rosary-meditation-label">%s</p>%s</div>'
                    % (kind, label, inner))
        med_text, med_prayer = MEDITATIONS[key][index]
        med_inner = ('<p class="rosary-meditation-text rosary-say">%s</p>'
                     '<p class="rosary-meditation-prayer rosary-say">%s</p>' % (_esc(med_text), _esc(med_prayer)))
        out = box('meditation', 'Meditation', med_inner)
        out += box('offering', 'Offering of the decade',
                   '<p class="rosary-offering-text rosary-say">%s</p>' % _esc(OFFERINGS[key][index]))
        if key in CLASSIC:
            title, paras, invocation = CLASSIC[key][index]
            out += box('classic', 'Classic meditation (1915)',
                       '<p class="rosary-classic-title rosary-say">%s</p>%s'
                       '<p class="rosary-meditation-prayer rosary-say">%s</p>'
                       '<p class="rosary-classic-source">%s</p>' % (
                           _esc(title),
                           ''.join('<p class="rosary-meditation-text rosary-say">%s</p>' % _esc(p) for p in paras),
                           _esc(invocation), _esc(CLASSIC_SOURCE)))
        else:
            out += box('classic', 'Classic meditation',
                       '<p class="rosary-classic-note">The 1915 book of classic meditations was written before '
                       'the Luminous Mysteries were added in 2002, so this mystery\u2019s meditation is shown '
                       'instead.</p>' + med_inner)
        v_text, v_prayer = VIRTUES[key][index]
        out += box('virtue', 'The virtue: %s' % _esc(SETS[key]['mysteries'][index]['fruit']),
                   '<p class="rosary-meditation-text rosary-say">%s</p>'
                   '<p class="rosary-meditation-prayer rosary-say">%s</p>' % (_esc(v_text), _esc(v_prayer)))
        i_line, i_text, i_prayer = INTENTIONS[key][index]
        out += box('intention', 'Intention for this decade',
                   '<p class="rosary-intention-line rosary-say">%s</p>'
                   '<p class="rosary-meditation-text rosary-say">%s</p>'
                   '<p class="rosary-meditation-prayer rosary-say">%s</p>' % (
                       _esc(i_line), _esc(i_text), _esc(i_prayer)))
        text, question = MODERN[key][index]
        out += box('modern', 'Reflection',
                   '<p class="rosary-meditation-text rosary-modern-text rosary-say">%s</p>'
                   '<p class="rosary-modern-question"><strong>To think about:</strong> '
                   '<span class="rosary-say">%s</span></p>' % (_esc(text), _esc(question)))
        return out

    def _set_html(self, key, version, captions, scripture, beads, only=None, hidden=False):
        data = SETS[key]
        indices = [only - 1] if only else range(5)
        nav = ''
        if not only:
            nav = '<div class="rosary-nav" role="group" aria-label="Choose a mystery">%s</div>' % ''.join(
                '<button type="button" class="rosary-nav-btn%s" data-index="%d"%s>%s<span>%d. %s</span>'
                '<small class="rosary-nav-fruit">%s</small></button>' % (
                    ' rosary-has-photo' if self._photo(key, i) else '',
                    i, ' aria-current="true"' if i == 0 else '',
                    icon(key, i, '') + self._photo_html(key, i, ''), i + 1,
                    _esc(data['mysteries'][i]['title'].replace('The ', '', 1)),
                    _esc(data['mysteries'][i]['fruit']))
                for i in range(5))
            if beads:
                extra_btn = ('<button type="button" class="rosary-nav-btn rosary-extra%s" data-index="%d">'
                             '%s<span>%s</span></button>')
                nav = nav.replace('aria-label="Choose a mystery">',
                                  'aria-label="Choose a mystery">' + extra_btn % (
                                      ' rosary-has-photo' if self._photo('opening', 0) else '', -1,
                                      extra_icon('opening', '') + self._photo_html('opening', 0, ''),
                                      'Opening prayers'), 1)
                nav = nav[:-len('</div>')] + extra_btn % (
                    ' rosary-has-photo' if self._photo('closing', 0) else '', 5,
                    extra_icon('closing', '') + self._photo_html('closing', 0, ''),
                    'Closing prayers') + '</div>'
        body = ''.join(self._mystery_html(key, i, version, captions, scripture, beads, i == indices[0])
                       for i in indices)
        if beads and not only:
            body = self._prayers_card('opening', -1) + body + self._prayers_card('closing', 5)
        heading = ('<h3 class="rosary-set-title">The %s Mysteries'
                   '<span class="rosary-days">prayed on %s</span></h3>'
                   % (data['name'], days_text(data['days'])))
        return (
            '<section class="rosary-set rosary-set--%s%s" data-set="%s" data-days="%s"%s>'
            '%s%s<div class="rosary-mysteries">%s</div></section>' % (
                key, ' rosary-single' if only else '', key,
                ','.join(str(d) for d in data['days']),
                ' data-hidden="1"' if hidden else '',
                heading, nav, body))

    def _prayers_card(self, kind, index):
        """The opening or closing prayers, as a card with its own beads."""
        plan = OPENING if kind == 'opening' else CLOSING
        title = 'The Opening Prayers' if kind == 'opening' else 'The Closing Prayers'
        sub = ('Before the first mystery' if kind == 'opening' else 'After the fifth mystery')
        items = []
        for label, name, intent, keys, style, full_only in plan:
            texts = [PRAYERS[k][1] for k in keys]
            shown = ''.join('<span class="rosary-prayer-text">%s%s</span>' % (
                ('<em>%s.</em> ' % _esc(PRAYERS[k][0])) if len(keys) > 1 else '', _esc(PRAYERS[k][1]))
                for k in keys)
            items.append(
                '<li class="rosary-prayer-item%s" data-label="%s" data-style="%s" data-name="%s" '
                'data-intent="%s" data-text="%s"><strong class="rosary-prayer-name">%s</strong>%s%s</li>' % (
                    ' rosary-extra-full' if full_only else '', _esc(label), style, _esc(name),
                    _esc(intent), _esc(' '.join(texts)), _esc(name),
                    (' <span class="rosary-cap">%s</span>' % _esc(intent)) if intent else '', shown))
        return (
            '<article class="rosary-mystery rosary-prayers-card rosary-extra" data-index="%d" data-kind="%s">'
            '<div class="rosary-head">'
            '<div class="rosary-icon%s">%s</div>'
            '<div><p class="rosary-num">%s</p>'
            '<h4 class="rosary-mystery-title">%s</h4>%s</div>'
            '</div>'
            '<div class="rosary-decade" aria-label="Beads"></div>'
            '<div class="rosary-controls"></div>'
            '<div class="rosary-now" aria-live="polite"></div>'
            '<ol class="rosary-refs rosary-prayer-list">%s</ol>'
            '</article>' % (index, kind, ' rosary-has-photo' if self._photo(kind, 0) else '',
                            extra_icon(kind, _esc(title)) + self._photo_html(kind, 0, title),
                            _esc(sub), _esc(title), self._credit_html(kind, 0), ''.join(items)))

    # ------------------------------------------------------------ pictures

    def _picture_folders(self):
        """[(key, label, folder, explicit)] - the folders to look for pictures in."""
        if 'images' in self.options:
            folder = (self.options.get('images') or '').strip()
            if not folder or folder.lower() == 'none':
                return []
            return [('photo', 'Pictures', folder, True)]
        sets = self.config.rosary_image_sets
        if sets is None:
            sets = [('photo', 'Traditional paintings', self.config.rosary_images),
                    ('sg', 'Stained glass windows', '/_static/rosary-images-sg'),
                    ('cubism', 'Cubism', '/_static/rosary-images-cubism'),
                    ('modaus', 'Modern Australian', '/_static/rosary-images-mod-aus'),
                    ('trad', 'Renaissance style', '/_static/rosary-images-trad')]
        out = []
        for entry in sets:
            key, label, folder = entry[0], entry[1], entry[2]
            if folder:
                out.append((str(key), str(label), str(folder), False))
        return out

    def _scan_folder(self, key, label, folder, explicit):
        """One picture folder -> dict with its pictures, whole pictures and credits."""
        rel, abs_path = self.env.relfn2path(folder)
        if not os.path.isdir(abs_path):
            if explicit:
                self._warn('the :images: folder "%s" was not found.', folder)
            return None
        found_set = {'key': key, 'label': label, 'photos': {}, 'full': {}, 'credits': {},
                     'style': 'photo' if key == 'photo' else 'photo-' + key}
        depth = self.env.docname.count('/')
        images = self.env.rosary_images.setdefault(self.env.docname, set())
        credits_file = os.path.join(abs_path, 'credits.txt')
        if os.path.isfile(credits_file):
            self.env.note_dependency(credits_file)
            with open(credits_file, encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    name, sep, text = line.partition(':')
                    if not sep:
                        name, sep, text = line.partition('=')
                    name = name.strip().lower()
                    if name in ('opening', 'closing'):
                        found_set['credits'][(name, 0)] = text.strip()
                    for skey in SET_ORDER:
                        for i in range(5):
                            if name == '%s-%d' % (skey, i + 1):
                                found_set['credits'][(skey, i)] = text.strip()
        missing = []
        wanted = [(skey, i, '%s-%d' % (skey, i + 1)) for skey in SET_ORDER for i in range(5)]
        wanted += [('opening', 0, 'opening'), ('closing', 0, 'closing')]
        for skey, i, stem in wanted:
            if True:
                found = None
                for ext in IMAGE_EXTS + tuple(e.upper() for e in IMAGE_EXTS):
                    name = stem + ext
                    if os.path.isfile(os.path.join(abs_path, name)):
                        found = name
                        break
                if not found:
                    if skey in SETS:
                        missing.append(stem)
                    continue
                src_rel = (Path(rel) / found).as_posix()
                images.add(src_rel)
                self.env.note_dependency(os.path.join(abs_path, found))
                found_set['photos'][(skey, i)] = '../' * depth + src_rel
                # the whole picture, shown when it is clicked
                for ext in IMAGE_EXTS:
                    full = os.path.join(abs_path, 'full', stem + ext)
                    if os.path.isfile(full):
                        full_rel = (Path(rel) / 'full' / os.path.basename(full)).as_posix()
                        images.add(full_rel)
                        found_set['full'][(skey, i)] = '../' * depth + full_rel
                        break
        if not found_set['photos']:
            if explicit:
                self._warn('no pictures named joyful-1.png ... glorious-5.png were '
                           'found in "%s".', folder)
            return None
        if missing:
            logger.info('rosary: %s has no picture for %s - the drawn icon is used.',
                        folder, ', '.join(missing), location=self.get_location())
        return found_set

    def _find_photos(self):
        """Every picture folder that has pictures, first one first."""
        self.photosets = []
        for key, label, folder, explicit in self._picture_folders():
            found = self._scan_folder(key, label, folder, explicit)
            if found:
                self.photosets.append(found)
        self.photos = self.photosets[0]['photos'] if self.photosets else {}

    def _photo(self, key, index):
        """True when the first (default) picture folder has this mystery."""
        return self.photos.get((key, index))

    def _credit_html(self, key, index):
        out = []
        for n, ps in enumerate(self.photosets):
            text = ps['credits'].get((key, index)) if (key, index) in ps['photos'] else None
            if text:
                out.append('<p class="rosary-photo-credit%s" data-photoset="%s">%s</p>' % (
                    ' rosary-photo-on' if n == 0 else '', _esc(ps['style']), _esc(text)))
        return ''.join(out)

    def _photo_html(self, key, index, alt):
        out = []
        for n, ps in enumerate(self.photosets):
            url = ps['photos'].get((key, index))
            if not url:
                continue
            full = ps['full'].get((key, index))
            credit = ps['credits'].get((key, index), '')
            extra = (' data-full="%s" data-credit="%s" title="Click to see the whole picture"'
                     % (_esc(full), _esc(credit))) if full else ''
            out.append('<img class="rosary-photo%s" data-photoset="%s" src="%s" alt="%s" loading="lazy"%s>' % (
                ' rosary-photo-on' if n == 0 else '', _esc(ps['style']), _esc(url), _esc(alt), extra))
        return ''.join(out)

    # ------------------------------------------------------------ run

    def run(self):
        if not hasattr(self.env, 'rosary_images'):
            self.env.rosary_images = {}
        self._find_photos()
        mode = 'all'
        set_key = None
        if self.arguments:
            word = self.arguments[0].strip().lower()
            if word in ('all', ''):
                mode = 'all'
            elif word == 'today':
                mode = 'today'
            elif word in SET_ALIASES:
                mode = 'set'
                set_key = SET_ALIASES[word]
            else:
                self._warn('"%s" is not a set of mysteries (use joyful, luminous, '
                           'sorrowful, glorious, today or all); all four sets are '
                           'shown.', self.arguments[0])

        only = self.options.get('mystery')
        if only and mode != 'set':
            self._warn(':mystery: needs a set, e.g. ".. rosary:: joyful" - ignored.')
            only = None

        version = self.options.get('bible-version', 'NRSVCE').strip()
        if version.lower() in ('none', 'off', 'no', ''):
            version = ''
        captions = 'no-captions' not in self.options
        beads = 'no-beads' not in self.options
        scripture = 'no-scripture' not in self.options

        if mode == 'set':
            keys = [set_key]
        else:
            keys = list(SET_ORDER)

        sets = ''.join(self._set_html(k, version, captions, scripture, beads, only) for k in keys)

        tabs = ''
        if mode == 'all':
            tabs = '<div class="rosary-tabs" role="tablist">%s</div>' % ''.join(
                '<button type="button" class="rosary-tab rosary-set--%s" role="tab" '
                'data-set="%s" aria-selected="false">%s<span class="rosary-tab-word">Mysteries</span>'
                '<small>%s</small></button>' % (
                    k, k, SETS[k]['name'], days_text(SETS[k]['days']))
                for k in keys)

        config = {
            'mode': mode,
            'open': self.options.get('open', ''),
            'prayers': 'prayers' in self.options,
            'beads': beads,
            'audio': beads and 'no-audio' not in self.options,
            'picker': 'no-picker' not in self.options,
            'photos': bool(self.photosets),
            'photosets': [[ps['style'], ps['label']] for ps in self.photosets],
            'read': self.options.get('read') or self.config.rosary_default_read,
            'extra': self.options.get('extra-prayers') or self.config.rosary_default_extra_prayers,
            'fatima': (self.options['fatima'] == 'yes') if 'fatima' in self.options
                      else bool(self.config.rosary_default_fatima),
            'readTitles': bool(self.config.rosary_default_read_titles),
            'hideTitle': 'hide-title' in self.options,
        }
        photo_styles = [ps['style'] for ps in self.photosets]
        style = (self.options.get('icons') or '').strip().lower()
        if not style:
            # site default (conf.py rosary_default_icons); quietly classic if missing
            style = 'photo' if self.photos and 'images' in self.options else (
                self.config.rosary_default_icons or 'classic').strip().lower()
            if style.startswith('photo') and style not in photo_styles and style != 'photo':
                style = 'classic'
        if style.startswith('photo') and style not in photo_styles:
            if photo_styles and style == 'photo':
                style = photo_styles[0]
            else:
                self._warn(':icons: %s has no pictures (picture styles here: %s) - classic '
                           'icons are used.', style, ', '.join(photo_styles) or 'none')
                style = 'classic'
        elif not style.startswith('photo') and style not in ICON_STYLES:
            self._warn(':icons: must be one of %s - classic icons are used.',
                       ', '.join(ICON_STYLES[:-1] + tuple(photo_styles)))
            style = 'classic'
        data_icons, photoset = (('photo', style) if style.startswith('photo') else
                                (style, photo_styles[0] if photo_styles else ''))

        # the mystery picker can have its own picture style
        nav_style = (self.options.get('nav-icons') or self.config.rosary_default_nav_icons
                     or 'same').strip().lower()
        if nav_style != 'same' and not (nav_style in ICON_STYLES[:-1] or nav_style in photo_styles):
            if 'nav-icons' in self.options:
                self._warn(':nav-icons: %s is not a picture style here - the picker matches the '
                           'main pictures.', nav_style)
            nav_style = 'same'
        config['navIcons'] = nav_style
        if nav_style == 'same':
            nav_icons, nav_photoset = data_icons, photoset
        elif nav_style.startswith('photo'):
            nav_icons, nav_photoset = 'photo', nav_style
        else:
            nav_icons, nav_photoset = nav_style, photoset
        sets = sets.replace('<div class="rosary-mysteries">',
                            '<div class="rosary-mysteries" data-icons="%s" data-photoset="%s">'
                            % (data_icons, photoset))
        sets = sets.replace('<div class="rosary-nav" ',
                            '<div class="rosary-nav" data-icons="%s" data-photoset="%s" '
                            % (nav_icons, nav_photoset))
        title = self.options.get('title', '').strip()
        title_html = '<p class="rosary-title">%s</p>' % _esc(title) if title else ''
        prayers_attr = (' data-prayers="%s"' % _esc(json.dumps(PRAYERS))) if beads else ''

        credit = ('<p class="rosary-credit">Scripture: %s (public domain).</p>' % TRANSLATION
                  if scripture or config['audio'] else '')
        layout = self.options.get('layout') or _layout(self.config.rosary_default_layout)
        if 'pictures' in self.options:
            pictures = self.options['pictures'] == 'yes'
        else:
            pictures = bool(self.config.rosary_default_pictures)
        if 'virtues' in self.options:
            virtues = self.options['virtues'] == 'yes'
        else:
            virtues = bool(self.config.rosary_default_virtues)
        html_output = (
            '<div class="rosary-block" data-icons="%s" data-photoset="%s" data-layout-choice="%s" '
            'data-layout="%s" data-pictures="%s" data-virtues="%s" data-under="%s" data-verses="%s" data-extra="%s" data-config="%s"%s>%s%s%s%s</div>'
            % (data_icons, photoset, layout,
               # without JavaScript, "auto" shows the iPad layout (it adapts to narrow screens)
               'ipad' if layout == 'auto' else layout, 'on' if pictures else 'off',
               'on' if virtues else 'off',
               self.options.get('under') or (self.config.rosary_default_under
                                             if self.config.rosary_default_under in UNDER else 'steps'),
               self.options.get('verses') or self.config.rosary_default_verses, config['extra'],
               _esc(json.dumps(config)),
               prayers_attr, title_html, tabs, sets, credit))
        return [nodes.raw('', html_output, format='html')]


def _purge(app, env, docname):
    getattr(env, 'rosary_images', {}).pop(docname, None)


def _merge(app, env, docnames, other):
    if not hasattr(env, 'rosary_images'):
        env.rosary_images = {}
    for docname, images in getattr(other, 'rosary_images', {}).items():
        if docname in docnames:
            env.rosary_images[docname] = images


def _copy_images(app, exception):
    """Copy the :images: pictures to the same place in the HTML output."""
    if exception or app.builder.format != 'html':
        return
    wanted = set()
    for images in getattr(app.env, 'rosary_images', {}).values():
        wanted.update(images)
    for rel in wanted:
        src = Path(app.srcdir) / rel
        dst = Path(app.outdir) / rel
        if src.is_file() and (not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime):
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def _web_app_tags(app, exception):
    """Let phones save the site to the Home Screen as a full-screen app.

    Adds the tags to the <head> of every built page after the build, so it
    works whatever the theme does with Sphinx's metatags.
    """
    if exception or not app.config.rosary_web_app or app.builder.format != 'html':
        return
    title = html.escape(app.config.rosary_web_app_title or app.config.project or 'Rosary', quote=True)
    outdir = Path(app.outdir)
    for page in outdir.rglob('*.html'):
        try:
            text = page.read_text(encoding='utf-8')
        except (OSError, UnicodeDecodeError):
            continue
        if 'apple-mobile-web-app-capable' in text or '</head>' not in text:
            continue
        up = os.path.relpath(outdir / '_static', page.parent).replace(os.sep, '/')
        tags = (
            '<meta name="apple-mobile-web-app-capable" content="yes">\n'
            '<meta name="mobile-web-app-capable" content="yes">\n'
            '<meta name="apple-mobile-web-app-status-bar-style" content="default">\n'
            '<meta name="apple-mobile-web-app-title" content="%s">\n'
            '<meta name="theme-color" content="#02024e">\n'
            '<link rel="apple-touch-icon" href="%s/rosary-touch-icon.png">\n'
            '<link rel="manifest" href="%s/rosary-manifest.json">\n' % (title, up, up))
        page.write_text(text.replace('</head>', tags + '</head>', 1), encoding='utf-8')


def setup(app):
    app.add_directive('rosary', RosaryDirective)
    # Home Screen app support (full screen on iPhone, no Safari bars)
    app.add_config_value('rosary_web_app', True, 'html')
    app.add_config_value('rosary_web_app_title', '', 'html')
    app.connect('build-finished', _web_app_tags)
    # folder of traditional paintings offered on every rosary ("" to turn off)
    app.add_config_value('rosary_images', '/_static/rosary-images', 'env')
    # every picture folder offered in the Pictures menu: [(key, label, folder), ...]
    # None = Traditional paintings (rosary_images), Stained glass windows
    # (/_static/rosary-images-sg), Cubism (/_static/rosary-images-cubism),
    # Modern Australian (/_static/rosary-images-mod-aus) and Renaissance style
    # (/_static/rosary-images-trad); the Pictures menu
    # lists them last-first, above the drawn styles; folders that are missing or empty are skipped
    app.add_config_value('rosary_image_sets', None, 'env')
    # site-wide starting choices; a page's directive options and each reader's
    # own menu choices take over from these
    app.add_config_value('rosary_default_icons', 'photo-sg', 'env')      # classic, stained, gold, photo, photo-sg, photo-cubism, photo-modaus, photo-trad
    app.add_config_value('rosary_default_nav_icons', 'classic', 'env')   # same, classic, stained, gold, photo...
    app.add_config_value('rosary_default_layout', 'auto', 'env')         # auto, desktop, ipad, iphone
    app.add_config_value('rosary_default_pictures', True, 'env')         # False to start with the pictures hidden
    app.add_config_value('rosary_default_virtues', True, 'env')          # False to hide the virtues in the picker
    app.add_config_value('rosary_default_under', 'steps', 'env')         # steps, meditation, virtue, intention, offering, classic, modern
    app.add_config_value('rosary_default_verses', 'current', 'env')      # all, current, none
    app.add_config_value('rosary_default_read', 'step', 'env')           # step, both, scripture
    app.add_config_value('rosary_default_extra_prayers', 'on', 'env')    # off, on, full
    app.add_config_value('rosary_default_fatima', True, 'env')           # O my Jesus after each Glory Be
    app.add_config_value('rosary_default_read_titles', False, 'env')     # say each opening/closing prayer's name
    app.connect('env-purge-doc', _purge)
    app.connect('env-merge-info', _merge)
    app.connect('build-finished', _copy_images)

    static_path = Path(__file__).parent / '_static'
    if str(static_path) not in app.config.html_static_path:
        app.config.html_static_path.append(str(static_path))

    app.add_js_file('rosary.js')
    app.add_css_file('rosary.css')
    return {
        'version': '1.0',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
