/* rosary directive: tabs, mystery picker, the decade of beads and read-aloud.
 *
 * The directive writes every set, mystery, reference and verse into the page,
 * so the page reads and prints without this script.  This script only hides /
 * shows parts, drives the beads and reads aloud with the browser's own voice
 * (the Web Speech API - no audio files):
 *
 *   bead 0       Our Father (announce the mystery)
 *   beads 1-10   Hail Marys, each with its scripture passage
 *   bead 11      Glory Be and the O my Jesus prayer
 */
(function () {
    'use strict';

    var SPEECH = ('speechSynthesis' in window) && ('SpeechSynthesisUtterance' in window);
    var STORE_VOICE = 'rosary-voice';
    var STORE_RATE = 'rosary-rate';
    var STORE_ICONS = 'rosary-icons';
    var STORE_LAYOUT = 'rosary-layout';
    var FULLSCREEN = !!(document.documentElement.requestFullscreen);
    // drawn styles; the picture folders (Stained glass windows, Masterpieces
    // windows ...) are added from the directive's config.photosets
    var STYLES = [['classic', 'Classic'], ['stained', 'Stained glass (drawn)'], ['gold', 'Gold icon']];
    // menu order: the picture folders in their config order, then the drawn styles
    function menuStyles(config) {
        return (config.photosets || []).concat(STYLES.slice().reverse());
    }

    function el(tag, cls, text) {
        var node = document.createElement(tag);
        if (cls) node.className = cls;
        if (text !== undefined) node.textContent = text;
        return node;
    }

    /* button labels: parts marked true are words that the iPhone layout hides,
     * so the buttons fit on one line there */
    var LBL = {
        back: [['\u25C0'], [' Back']],
        begin: [['Begin'], [' \u25B6']],
        next: [['Next'], [' \u25B6']],
        finish: [['Finish'], [' \u2714']],
        finishDecade: [['Finish'], [' decade', true], [' \u2714']],
        // the Listen control: 'Listen: [This bead] [Whole decade]', on iPhone '[Bead] [All]'
        listenBead: [['This bead', true], ['Bead', 'short']],
        listenPrayer: [['This prayer', true], ['Prayer', 'short']],
        allDecade: [['Whole decade', true], ['All', 'short']],
        allPrayers: [['All prayers', true], ['All', 'short']],
        stop: [['\u25A0 Stop']],
        full: [['\u26F6'], [' Full screen', true]]
    };
    function setLabel(b, parts) {
        var key = parts.map(function (p) { return p[0] + (p[1] ? '*' : ''); }).join('|');
        if (b.getAttribute('data-lbl') === key) return;
        b.setAttribute('data-lbl', key);
        b.textContent = '';
        parts.forEach(function (p) {
            if (p[1] === 'short') b.appendChild(el('span', 'rosary-btn-short', p[0]));
            else if (p[1]) b.appendChild(el('span', 'rosary-btn-word', p[0]));
            else b.appendChild(document.createTextNode(p[0]));
        });
        b.setAttribute('aria-label', parts.filter(function (p) { return p[1] !== 'short'; })
            .map(function (p) { return p[0]; }).join('').replace(/^\s+|\s+$/g, ''));
    }
    function fullLabel(b) { setLabel(b, LBL.full); }

    // "🔊 Listen: [one] [all]": both audio buttons in one labelled group
    function audioGroup(one, all) {
        var g = el('span', 'rosary-audio-group');
        g.setAttribute('role', 'group');
        g.setAttribute('aria-label', 'Listen');
        var lab = el('span', 'rosary-audio-group-label', '\uD83D\uDD0A');
        lab.appendChild(el('span', 'rosary-btn-word', ' Listen:'));
        g.appendChild(lab);
        g.appendChild(one);
        g.appendChild(all);
        return g;
    }

    function button(cls, text, title) {
        var b = el('button', cls, text);
        b.type = 'button';
        if (title) b.title = title;
        return b;
    }

    function store(key, value) {
        try {
            if (value === undefined) return window.localStorage.getItem(key);
            window.localStorage.setItem(key, value);
        } catch (e) { /* storage unavailable */ }
        return null;
    }

    function todayKey(sets) {
        var day = new Date().getDay();
        for (var i = 0; i < sets.length; i++) {
            var days = (sets[i].getAttribute('data-days') || '').split(',');
            if (days.indexOf(String(day)) !== -1) return sets[i].getAttribute('data-set');
        }
        return sets.length ? sets[0].getAttribute('data-set') : '';
    }

    /* ------------------------------------------------------------ speech */

    var speech = {
        token: 0,
        queue: [],          // keep utterances referenced (Chrome drops onend otherwise)
        voice: null,
        rate: 0.9
    };

    function englishVoices() {
        if (!SPEECH) return [];
        return window.speechSynthesis.getVoices().filter(function (v) {
            return /^en([-_]|$)/i.test(v.lang);
        });
    }

    function bestVoice(voices) {
        var saved = store(STORE_VOICE);
        var i;
        if (saved) for (i = 0; i < voices.length; i++) if (voices[i].name === saved) return voices[i];
        var prefs = [/en[-_]AU/i, /en[-_]GB/i, /en[-_]IE|en[-_]NZ/i, /en/i];
        for (var p = 0; p < prefs.length; p++) {
            var matches = voices.filter(function (v) { return prefs[p].test(v.lang); });
            if (matches.length) {
                // the "Natural" / "Online" / Google voices sound far better
                for (i = 0; i < matches.length; i++) if (/natural|online|google/i.test(matches[i].name)) return matches[i];
                return matches[0];
            }
        }
        return voices[0] || null;
    }

    function cleanForSpeech(text) {
        return text
            .replace(/\b([A-Z])([A-Z]{2,})\b/g, function (m, a, b) { return a + b.toLowerCase(); })  // JESUS -> Jesus
            .replace(/[“”"]/g, '')
            .replace(/\s+/g, ' ')
            .trim();
    }

    function sentences(text) {
        // short chunks: some browsers cut off long utterances
        var parts = cleanForSpeech(text).match(/[^.!?;:]+[.!?;:]*\s*/g) || [];
        var out = [];
        parts.forEach(function (p) {
            p = p.trim();
            if (!p) return;
            if (out.length && out[out.length - 1].length + p.length < 160) out[out.length - 1] += ' ' + p;
            else out.push(p);
        });
        return out;
    }

    function stopSpeech() {
        speech.token++;
        speech.queue = [];
        if (SPEECH) window.speechSynthesis.cancel();
    }

    /* Speak a list of texts in order, then call done() (unless stopped). */
    function speak(texts, done) {
        stopSpeech();
        if (!SPEECH) { if (done) done(); return; }
        var token = speech.token;
        var chunks = [];
        texts.forEach(function (t) { if (t) chunks = chunks.concat(sentences(t)); });
        var i = 0;
        function next() {
            if (token !== speech.token) return;
            if (i >= chunks.length) { if (done) done(); return; }
            var u = new window.SpeechSynthesisUtterance(chunks[i++]);
            if (speech.voice) { u.voice = speech.voice; u.lang = speech.voice.lang; } else { u.lang = 'en-AU'; }
            u.rate = speech.rate;
            u.onend = function () { setTimeout(next, 120); };
            u.onerror = function () { setTimeout(next, 120); };
            speech.queue.push(u);
            window.speechSynthesis.speak(u);
        }
        next();
    }

    window.addEventListener('beforeunload', stopSpeech);

    /* ------------------------------------------------------------ a block */

    function initBlock(block) {
        var config = {};
        try { config = JSON.parse(block.getAttribute('data-config') || '{}'); } catch (e) { config = {}; }
        var prayers = {};
        try { prayers = JSON.parse(block.getAttribute('data-prayers') || '{}'); } catch (e) { prayers = {}; }
        var state = {
            showPrayers: !!config.prayers,
            auto: false,            // praying aloud, bead after bead
            speaking: null,         // mystery element being read
            read: ['step', 'both', 'scripture'].indexOf(config.read) !== -1 ? config.read : 'both',
            fatima: config.fatima !== false,     // O my Jesus after each Glory Be
            readTitles: !!config.readTitles      // announce each opening / closing prayer
        };
        var refreshers = [];
        function refreshAll() { refreshers.forEach(function (f) { f(); }); }

        block.classList.add('rosary-js');
        var sets = Array.prototype.slice.call(block.querySelectorAll('.rosary-set'));
        var today = todayKey(sets);
        var audio = config.audio && SPEECH;

        /* ---------------- picture style: a drawn style, or a picture folder.
         * A folder's style value is "photo" or "photo-<key>": the block gets
         * data-icons="photo" and data-photoset=<that value>. */
        function currentStyle() {
            var icons = block.getAttribute('data-icons') || 'classic';
            return icons === 'photo' ? (block.getAttribute('data-photoset') || 'photo') : icons;
        }
        function showPhotos(holders, set) {
            holders.forEach(function (holder) {
                var any = false;
                holder.querySelectorAll('.rosary-photo').forEach(function (img) {
                    var on = img.getAttribute('data-photoset') === set;
                    img.classList.toggle('rosary-photo-on', on);
                    if (on) any = true;
                });
                holder.classList.toggle('rosary-has-photo', any);
            });
        }
        function applyPhotoset() {
            var icons = block.getAttribute('data-icons') || 'classic';
            var set = block.getAttribute('data-photoset') || '';
            block.querySelectorAll('.rosary-mysteries').forEach(function (m) {
                m.setAttribute('data-icons', icons);
                m.setAttribute('data-photoset', set);
            });
            showPhotos(block.querySelectorAll('.rosary-icon'), set);
            block.querySelectorAll('.rosary-photo-credit').forEach(function (p) {
                p.classList.toggle('rosary-photo-on', p.getAttribute('data-photoset') === set);
            });
            applyNav();
            if (block.rosaryMarkShapes) block.rosaryMarkShapes();
        }
        /* the mystery picker: "same" as the main pictures, or its own style */
        var navChoice = config.navIcons || 'same';
        function applyNav() {
            var value = navChoice === 'same' ? currentStyle() : navChoice;
            var icons = value.indexOf('photo') === 0 ? 'photo' : value;
            var set = value.indexOf('photo') === 0 ? value : (block.getAttribute('data-photoset') || '');
            block.querySelectorAll('.rosary-nav').forEach(function (nav) {
                nav.setAttribute('data-icons', icons);
                nav.setAttribute('data-photoset', set);
                showPhotos(nav.querySelectorAll('.rosary-nav-btn'), set);
            });
        }
        function setStyle(value) {
            if (value.indexOf('photo') === 0) {
                block.setAttribute('data-icons', 'photo');
                block.setAttribute('data-photoset', value);
            } else {
                block.setAttribute('data-icons', value);
            }
            applyPhotoset();
        }
        applyPhotoset();

        function extraOn() {
            var x = block.getAttribute('data-extra');
            return x === 'on' || x === 'full';
        }
        var savedExtra = store('rosary-extra');
        if (['off', 'on', 'full'].indexOf(savedExtra) !== -1 && block.querySelector('.rosary-prayers-card')) {
            block.setAttribute('data-extra', savedExtra);
        }

        /* ---------------- layout: desktop, ipad or iphone; "auto" picks one
         * from the width of the screen.  data-layout-choice holds the
         * reader's choice, data-layout the layout in use. */
        function oldLayout(v) {
            // layouts from earlier versions map to the nearest new one
            var map = { phone: 'ipad', large: 'ipad', side: 'desktop', compact: 'iphone' };
            if (map[v]) return map[v];
            return ['auto', 'desktop', 'ipad', 'iphone'].indexOf(v) !== -1 ? v : null;
        }
        var layoutChoice = oldLayout(block.getAttribute('data-layout-choice')) ||
                           oldLayout(block.getAttribute('data-layout')) || 'auto';
        function applyLayout() {
            var use = layoutChoice;
            if (use === 'auto') {
                var w = window.innerWidth;
                use = w < 700 ? 'iphone' : (w < 1200 ? 'ipad' : 'desktop');
            }
            block.setAttribute('data-layout-choice', layoutChoice);
            if (block.getAttribute('data-layout') !== use) block.setAttribute('data-layout', use);
            document.documentElement.classList.toggle('rosary-layout-iphone', use === 'iphone');
            if (block.rosaryWiden) block.rosaryWiden();
        }
        applyLayout();
        window.addEventListener('resize', function () { if (layoutChoice === 'auto') applyLayout(); });

        /* ---------------- toolbar: picture style, voice and speed */
        var bar = null;

        /* compact top row: set tabs, then Options and Hide menus buttons */
        var topbar = el('div', 'rosary-topbar');
        var tabsEl = block.querySelector('.rosary-tabs');
        var firstSet = block.querySelector('.rosary-set');
        block.insertBefore(topbar, tabsEl || firstSet);
        if (tabsEl) topbar.appendChild(tabsEl);
        topbar.appendChild(el('span', 'rosary-topbar-gap'));
        var optionsBtn = null;
        if (config.picker || audio) {
            bar = el('div', 'rosary-audio-bar');
            block.insertBefore(bar, firstSet);
            optionsBtn = button('rosary-top-btn', '\u2699 Options', 'Pictures, layout and voice');
            optionsBtn.setAttribute('aria-expanded', 'false');
            topbar.appendChild(optionsBtn);
            var setOptions = function (open) {
                bar.hidden = !open;
                optionsBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
                optionsBtn.classList.toggle('rosary-on', open);
            };
            setOptions(store('rosary-options-open') === '1');
            optionsBtn.addEventListener('click', function () {
                var open = bar.hidden;
                setOptions(open);
                store('rosary-options-open', open ? '1' : '0');
            });
        }
        var hideBtn = button('rosary-top-btn', '\u2922 Hide menus', 'Hide the menus to give the picture more room');
        topbar.appendChild(hideBtn);
        var showRow = el('div', 'rosary-show-row');
        var showBtn = button('rosary-show-menus', '\u2630 Menus', 'Show the menus again');
        showRow.appendChild(showBtn);
        block.insertBefore(showRow, topbar);
        // previous / next mystery, for moving quickly on a phone (iPhone layout)
        function quickButtons() {
            var q = el('span', 'rosary-quick');
            var back = button('rosary-top-btn rosary-quick-btn', '\u2039', 'Previous mystery');
            var fwd = button('rosary-top-btn rosary-quick-btn', '\u203A', 'Next mystery');
            back.setAttribute('aria-label', 'Previous mystery');
            fwd.setAttribute('aria-label', 'Next mystery');
            back.addEventListener('click', function () { stepMystery(-1); });
            fwd.addEventListener('click', function () { stepMystery(1); });
            q.appendChild(back);
            q.appendChild(fwd);
            return q;
        }
        if (config.beads) {
            topbar.insertBefore(quickButtons(), topbar.querySelector('.rosary-topbar-gap').nextSibling);
            showRow.appendChild(quickButtons());
        }
        // Hide menus also hides the page title and the site's header bar
        var setMenus = function (hidden) {
            block.classList.toggle('rosary-menus-hidden', hidden);
            document.documentElement.classList.toggle('rosary-page-focus', hidden);
            store('rosary-menus-hidden', hidden ? '1' : '0');
            if (block.rosaryWiden) block.rosaryWiden();
        };
        if (store('rosary-menus-hidden') === '1') {
            block.classList.add('rosary-menus-hidden');
            document.documentElement.classList.add('rosary-page-focus');
        }
        if (config.hideTitle) document.documentElement.classList.add('rosary-hide-title');
        hideBtn.addEventListener('click', function () { setMenus(true); });
        showBtn.addEventListener('click', function () { setMenus(false); });
        if (config.picker) {
            var picLabel = el('label', 'rosary-audio-field', 'Pictures ');
            var picSelect = el('select', 'rosary-select');
            menuStyles(config).forEach(function (st) {
                var o = el('option', '', st[1]);
                o.value = st[0];
                picSelect.appendChild(o);
            });
            var savedStyle = store(STORE_ICONS);
            if (savedStyle && picSelect.querySelector('option[value="' + savedStyle + '"]')) {
                setStyle(savedStyle);
            }
            picSelect.value = currentStyle();
            picSelect.addEventListener('change', function () {
                setStyle(picSelect.value);
                store(STORE_ICONS, picSelect.value);
            });
            picLabel.appendChild(picSelect);
            bar.appendChild(picLabel);

            var navLabel = el('label', 'rosary-audio-field', 'Mystery picker ');
            var navSelect = el('select', 'rosary-select');
            [['same', 'Same as pictures']].concat(menuStyles(config)).forEach(function (st) {
                var o = el('option', '', st[1]);
                o.value = st[0];
                navSelect.appendChild(o);
            });
            var savedNav = store('rosary-nav-icons');
            if (savedNav && navSelect.querySelector('option[value="' + savedNav + '"]')) navChoice = savedNav;
            if (!navSelect.querySelector('option[value="' + navChoice + '"]')) navChoice = 'same';
            navSelect.value = navChoice;
            applyNav();
            navSelect.addEventListener('change', function () {
                navChoice = navSelect.value;
                store('rosary-nav-icons', navChoice);
                applyNav();
            });
            navLabel.appendChild(navSelect);
            bar.appendChild(navLabel);

            var layLabel = el('label', 'rosary-audio-field', 'Layout ');
            var laySelect = el('select', 'rosary-select');
            [['auto', 'Automatic (fits the screen)'], ['desktop', 'Desktop'], ['ipad', 'iPad'],
             ['iphone', 'iPhone']].forEach(function (l) {
                var o = el('option', '', l[1]);
                o.value = l[0];
                laySelect.appendChild(o);
            });
            var savedLayout = oldLayout(store(STORE_LAYOUT));
            if (savedLayout) { layoutChoice = savedLayout; applyLayout(); }
            laySelect.value = layoutChoice;
            laySelect.addEventListener('change', function () {
                layoutChoice = laySelect.value;
                store(STORE_LAYOUT, layoutChoice);
                applyLayout();
            });
            layLabel.appendChild(laySelect);
            bar.appendChild(layLabel);

            /* the main pictures can be hidden, in every layout */
            var spLabel = el('label', 'rosary-audio-field rosary-prayers-field');
            spLabel.title = 'Untick to hide the main picture of each mystery and give the text more room';
            var spBox = el('input');
            spBox.type = 'checkbox';
            var savedPics = store('rosary-pictures');
            if (savedPics === '1' || savedPics === '0') block.setAttribute('data-pictures', savedPics === '1' ? 'on' : 'off');
            spBox.checked = block.getAttribute('data-pictures') !== 'off';
            spLabel.appendChild(spBox);
            spLabel.appendChild(document.createTextNode(' Show pictures'));
            bar.appendChild(spLabel);
            spBox.addEventListener('change', function () {
                block.setAttribute('data-pictures', spBox.checked ? 'on' : 'off');
                store('rosary-pictures', spBox.checked ? '1' : '0');
                if (block.rosaryWiden) block.rosaryWiden();
            });

            /* each mystery's virtue under its name in the mystery picker */
            var viLabel = null;
            if (block.querySelector('.rosary-nav-fruit')) {
                viLabel = el('label', 'rosary-audio-field rosary-prayers-field');
                viLabel.title = 'Show each mystery\u2019s virtue (the fruit of the mystery) under its name in the mystery picker';
                var viBox = el('input');
                viBox.type = 'checkbox';
                var savedVirtues = store('rosary-virtues');
                if (savedVirtues === '1' || savedVirtues === '0') block.setAttribute('data-virtues', savedVirtues === '1' ? 'on' : 'off');
                viBox.checked = block.getAttribute('data-virtues') !== 'off';
                viLabel.appendChild(viBox);
                viLabel.appendChild(document.createTextNode(' Show virtues'));
                bar.appendChild(viLabel);
                viBox.addEventListener('change', function () {
                    block.setAttribute('data-virtues', viBox.checked ? 'on' : 'off');
                    store('rosary-virtues', viBox.checked ? '1' : '0');
                });
            }

            /* scripture under the steps: all, the current step only, or none */
            if (block.querySelector('.rosary-verse')) {
                var verLabel = el('label', 'rosary-audio-field', 'Scripture verses ');
                var verSelect = el('select', 'rosary-select');
                [['all', 'All, under each step'], ['current', 'Current step, in the panel'], ['none', 'Hidden']].forEach(function (v) {
                    var o = el('option', '', v[1]);
                    o.value = v[0];
                    verSelect.appendChild(o);
                });
                var savedVerses = store('rosary-verses');
                if (['all', 'current', 'none'].indexOf(savedVerses) !== -1) block.setAttribute('data-verses', savedVerses);
                verSelect.value = block.getAttribute('data-verses') || 'all';
                verSelect.addEventListener('change', function () {
                    block.setAttribute('data-verses', verSelect.value);
                    store('rosary-verses', verSelect.value);
                });
                verLabel.appendChild(verSelect);
                bar.appendChild(verLabel);
            }

            /* under the beads: the ten steps, or a meditation on the mystery */
            if (block.querySelector('.rosary-meditation')) {
                var undLabel = el('label', 'rosary-audio-field', 'Under the beads ');
                var undSelect = el('select', 'rosary-select');
                [['steps', 'The ten steps'], ['meditation', 'A meditation'],
                 ['virtue', 'A meditation on the virtue'], ['intention', 'An intention'],
                 ['offering', 'A Montfort-style offering'], ['classic', 'A classic meditation (1915)'],
                 ['modern', 'A modern reflection']].forEach(function (v) {
                    var o = el('option', '', v[1]);
                    o.value = v[0];
                    undSelect.appendChild(o);
                });
                var savedUnder = store('rosary-under');
                var UNDER = ['steps', 'meditation', 'virtue', 'intention', 'offering', 'classic', 'modern'];
                if (UNDER.indexOf(savedUnder) !== -1) block.setAttribute('data-under', savedUnder);
                undSelect.value = UNDER.indexOf(block.getAttribute('data-under')) !== -1
                    ? block.getAttribute('data-under') : 'steps';
                undSelect.addEventListener('change', function () { setUnder(undSelect.value); });
                undLabel.appendChild(undSelect);
                bar.appendChild(undLabel);
            }

            /* the opening and closing prayers of the rosary */
            if (block.querySelector('.rosary-prayers-card')) {
                var exLabel = el('label', 'rosary-audio-field', 'Opening & closing ');
                var exSelect = el('select', 'rosary-select');
                [['off', 'Off'], ['on', 'On'], ['full', 'On, with St Michael and Memorare']].forEach(function (v) {
                    var o = el('option', '', v[1]);
                    o.value = v[0];
                    exSelect.appendChild(o);
                });
                exSelect.value = block.getAttribute('data-extra') || 'off';
                exSelect.addEventListener('change', function () {
                    var wasOn = extraOn();
                    block.setAttribute('data-extra', exSelect.value);
                    store('rosary-extra', exSelect.value);
                    stopAuto();
                    sets.forEach(function (set) {
                        if (!set.rosaryShowMystery) return;
                        var act = set.querySelector('.rosary-mystery.rosary-active');
                        if (!extraOn() && act && act.classList.contains('rosary-extra')) set.rosaryShowMystery(0);
                        else if (extraOn() && !wasOn && !set.querySelector('.rosary-bead.rosary-here')) set.rosaryShowMystery(-1);
                    });
                    refreshAll();
                });
                exLabel.appendChild(exSelect);
                bar.appendChild(exLabel);
            }
        }

        /* Show the prayers: one checkbox for the whole rosary, in the Options panel */
        var savedPrayers = store('rosary-prayers');
        if (savedPrayers === '1' || savedPrayers === '0') state.showPrayers = savedPrayers === '1';
        var prayersBox = null;
        if (bar && config.beads) {
            var prLabel = el('label', 'rosary-audio-field rosary-prayers-field');
            prayersBox = el('input');
            prayersBox.type = 'checkbox';
            prayersBox.checked = state.showPrayers;
            prLabel.appendChild(prayersBox);
            prLabel.appendChild(document.createTextNode(' Show the prayers'));
            bar.appendChild(prLabel);
            prayersBox.addEventListener('change', function () {
                state.showPrayers = prayersBox.checked;
                store('rosary-prayers', state.showPrayers ? '1' : '0');
                refreshAll();
            });

            var savedFatima = store('rosary-fatima');
            if (savedFatima === '1' || savedFatima === '0') state.fatima = savedFatima === '1';
            var faLabel = el('label', 'rosary-audio-field rosary-prayers-field');
            faLabel.title = 'O my Jesus, after the Glory Be at the end of each decade';
            var fatimaBox = el('input');
            fatimaBox.type = 'checkbox';
            fatimaBox.checked = state.fatima;
            faLabel.appendChild(fatimaBox);
            faLabel.appendChild(document.createTextNode(' Fatima prayer'));
            bar.appendChild(faLabel);
            fatimaBox.addEventListener('change', function () {
                state.fatima = fatimaBox.checked;
                store('rosary-fatima', state.fatima ? '1' : '0');
                refreshAll();
            });
        }

        /* the layouts and full screen show the whole painting, not the crop */
        function updatePhotos() {
            var big = true;
            block.querySelectorAll('.rosary-mystery .rosary-icon .rosary-photo[data-full]').forEach(function (img) {
                if (!img.getAttribute('data-crop')) img.setAttribute('data-crop', img.getAttribute('src'));
                var want = big ? img.getAttribute('data-full') : img.getAttribute('data-crop');
                if (img.getAttribute('src') !== want) img.setAttribute('src', want);
            });
        }
        updatePhotos();
        block.rosaryUpdatePhotos = updatePhotos;

        /* wide (landscape) pictures: marked so the iPad layout can frame them to
         * their own shape instead of the tall phone-shaped frame */
        function markShape(img) {
            var mark = function () {
                var icon = img.closest('.rosary-icon');
                if (!icon || !img.naturalWidth || !img.classList.contains('rosary-photo-on')) return;
                icon.classList.toggle('rosary-wide', img.naturalWidth > img.naturalHeight * 1.1);
            };
            if (img.complete && img.naturalWidth) mark(); else img.addEventListener('load', mark, { once: true });
        }
        function markShapes() {
            block.querySelectorAll('.rosary-mystery .rosary-icon.rosary-wide').forEach(function (i) {
                i.classList.remove('rosary-wide');
            });
            block.querySelectorAll('.rosary-mystery .rosary-icon .rosary-photo.rosary-photo-on').forEach(markShape);
        }
        markShapes();
        block.rosaryMarkShapes = markShapes;

        /* desktop: widen the block into empty space right of the page's
         * column, so the picture can be as large as the screen allows */
        function widen() {
            block.style.removeProperty('--rosary-widen');
            block.removeAttribute('data-widen');
            if (block.getAttribute('data-layout') !== 'desktop' || window.innerWidth < 1100) return;
            var r = block.getBoundingClientRect();
            var spare = window.innerWidth - r.right - 24;
            // leave room for a table-of-contents sidebar if the page has one
            var toc = document.querySelector('.sy-rside, .toc-drawer, aside.toc, .bd-sidebar-secondary');
            var tocUsed = toc && (toc.innerText || '').replace(/\s+/g, '').length > 3;
            if (tocUsed && toc.getBoundingClientRect().width > 0 && toc.getBoundingClientRect().left > r.left) {
                spare = Math.min(spare, toc.getBoundingClientRect().left - r.right - 16);
            }
            if (spare > 40) {
                block.style.setProperty('--rosary-widen', Math.round(Math.min(spare, 900)) + 'px');
                block.setAttribute('data-widen', '');
            }
        }
        widen();
        window.addEventListener('resize', widen);
        block.rosaryWiden = widen;
        if (audio) {
            bar.appendChild(el('span', 'rosary-audio-icon', '🔊'));
            var voiceLabel = el('label', 'rosary-audio-field', 'Voice ');
            var voiceSelect = el('select', 'rosary-select');
            voiceLabel.appendChild(voiceSelect);
            var readLabel = el('label', 'rosary-audio-field', 'Read aloud ');
            var readSelect = el('select', 'rosary-select');
            [['step', 'Step only'], ['both', 'Step and scripture'], ['scripture', 'Scripture only']].forEach(function (r) {
                var o = el('option', '', r[1]);
                o.value = r[0];
                readSelect.appendChild(o);
            });
            var savedRead = store('rosary-read');
            if (['step', 'both', 'scripture'].indexOf(savedRead) !== -1) state.read = savedRead;
            readSelect.value = state.read;
            readSelect.addEventListener('change', function () {
                state.read = readSelect.value;
                store('rosary-read', state.read);
            });
            readLabel.appendChild(readSelect);

            // announce the opening and closing prayers by name before reading them
            var titlesLabel = null;
            if (block.querySelector('.rosary-prayers-card')) {
                var savedTitles = store('rosary-read-titles');
                if (savedTitles === '1' || savedTitles === '0') state.readTitles = savedTitles === '1';
                titlesLabel = el('label', 'rosary-audio-field rosary-prayers-field');
                titlesLabel.title = 'Say the name of each opening and closing prayer (and its intention) before reading it';
                var titlesBox = el('input');
                titlesBox.type = 'checkbox';
                titlesBox.checked = state.readTitles;
                titlesLabel.appendChild(titlesBox);
                titlesLabel.appendChild(document.createTextNode(' Read prayer names'));
                titlesBox.addEventListener('change', function () {
                    state.readTitles = titlesBox.checked;
                    store('rosary-read-titles', state.readTitles ? '1' : '0');
                });
            }
            var rateLabel = el('label', 'rosary-audio-field', 'Speed ');
            var rateSelect = el('select', 'rosary-select');
            [['0.75', 'Slow'], ['0.9', 'Calm'], ['1', 'Normal'], ['1.15', 'Quick']].forEach(function (r) {
                var o = el('option', '', r[1]);
                o.value = r[0];
                rateSelect.appendChild(o);
            });
            speech.rate = parseFloat(store(STORE_RATE) || '0.9') || 0.9;
            rateSelect.value = String(speech.rate);
            if (!rateSelect.value) rateSelect.value = '0.9';
            rateLabel.appendChild(rateSelect);
            bar.appendChild(voiceLabel);
            bar.appendChild(readLabel);
            if (titlesLabel) bar.appendChild(titlesLabel);
            bar.appendChild(rateLabel);

            var fillVoices = function () {
                var voices = englishVoices();
                if (!voices.length) return;
                var chosen = speech.voice && voices.indexOf(speech.voice) !== -1 ? speech.voice : bestVoice(voices);
                speech.voice = chosen;
                voiceSelect.textContent = '';
                voices.forEach(function (v) {
                    var o = el('option', '', v.name.replace(/^Microsoft /, '').replace(/ - English.*$/, '') + ' (' + v.lang + ')');
                    o.value = v.name;
                    if (v === chosen) o.selected = true;
                    voiceSelect.appendChild(o);
                });
            };
            fillVoices();
            if (window.speechSynthesis.addEventListener) window.speechSynthesis.addEventListener('voiceschanged', fillVoices);
            voiceSelect.addEventListener('change', function () {
                var voices = englishVoices();
                for (var i = 0; i < voices.length; i++) if (voices[i].name === voiceSelect.value) speech.voice = voices[i];
                store(STORE_VOICE, voiceSelect.value);
                document.querySelectorAll('.rosary-block .rosary-select[data-kind="voice"]').forEach(function (s) {
                    if (s !== voiceSelect) s.value = voiceSelect.value;
                });
            });
            voiceSelect.setAttribute('data-kind', 'voice');
            rateSelect.addEventListener('change', function () {
                speech.rate = parseFloat(rateSelect.value) || 0.9;
                store(STORE_RATE, rateSelect.value);
            });
        }

        /* ---------------- quick switch above the steps: Steps, Meditation, Virtue,
         * Intention, Offering, Classic, Modern (the same choice as "Under the beads") */
        function setUnder(v) {
            block.setAttribute('data-under', v);
            store('rosary-under', v);
            if (undSelect) undSelect.value = v;
            refreshAll();
        }
        block.querySelectorAll('.rosary-mystery:not(.rosary-prayers-card) .rosary-under-wrap').forEach(function (wrap) {
            if (!wrap.querySelector('.rosary-under-box')) return;
            var row = el('div', 'rosary-under-switch');
            row.setAttribute('role', 'group');
            row.setAttribute('aria-label', 'Show under the beads');
            [['steps', 'Steps', 'The ten scripture steps'], ['meditation', 'Meditation', 'A meditation'],
             ['virtue', 'Virtue', 'A meditation on the virtue'], ['intention', 'Intention', 'An intention'],
             ['offering', 'Offering', 'A Montfort-style offering'], ['classic', 'Classic', 'A classic meditation (1915)'],
             ['modern', 'Modern', 'A modern reflection']].forEach(function (c) {
                var b = button('rosary-under-chip', c[1], c[2]);
                b.setAttribute('data-v', c[0]);
                b.addEventListener('click', function () { setUnder(c[0]); });
                row.appendChild(b);
            });
            wrap.insertBefore(row, wrap.firstChild);
        });

        /* ---------------- tidy the Options panel into labelled groups */
        if (bar) {
            var oldIcon = bar.querySelector('.rosary-audio-icon');
            if (oldIcon) oldIcon.remove();
            bar.classList.add('rosary-opt-panel');
            var groups = el('div', 'rosary-opt-groups');
            var addGroup = function (title, items) {
                items = items.filter(function (x) { return x && x.parentNode === bar; });
                if (!items.length) return;
                var g = el('fieldset', 'rosary-opt-group');
                g.appendChild(el('legend', '', title));
                var selects = el('div', 'rosary-opt-selects');
                var checks = el('div', 'rosary-opt-checks');
                items.forEach(function (lab) {
                    (lab.querySelector('input[type="checkbox"]') ? checks : selects).appendChild(lab);
                });
                if (selects.children.length) g.appendChild(selects);
                if (checks.children.length) g.appendChild(checks);
                groups.appendChild(g);
            };
            addGroup('🖼 Pictures', [picLabel, navLabel, layLabel, spLabel, viLabel]);
            addGroup('✝ Prayers', [exLabel, undLabel, verLabel, prLabel, faLabel]);
            addGroup('🔊 Reading aloud', [voiceLabel, readLabel, rateLabel, titlesLabel]);
            // anything not placed above stays, in a final group
            var rest = Array.prototype.slice.call(bar.children);
            if (rest.length) addGroup('Other', rest);
            bar.appendChild(groups);

            var foot = el('div', 'rosary-opt-foot');
            var resetBtn = button('rosary-opt-btn', '↺ Reset to starting choices',
                'Forget the choices saved in this browser and go back to the site’s starting choices');
            var doneBtn = button('rosary-opt-btn rosary-opt-done', '✓ Done', 'Close the options');
            resetBtn.addEventListener('click', function () {
                try {
                    var keys = [];
                    for (var i = 0; i < window.localStorage.length; i++) {
                        var k = window.localStorage.key(i);
                        if (k && k.indexOf('rosary-') === 0) keys.push(k);
                    }
                    keys.forEach(function (k) { window.localStorage.removeItem(k); });
                } catch (e) { /* storage unavailable */ }
                if (window.speechSynthesis) window.speechSynthesis.cancel();
                document.documentElement.classList.remove('rosary-page-focus');
                window.location.reload();
            });
            doneBtn.addEventListener('click', function () {
                setOptions(false);
                store('rosary-options-open', '0');
                if (optionsBtn) optionsBtn.focus();
            });
            foot.appendChild(resetBtn);
            foot.appendChild(doneBtn);
            bar.appendChild(foot);
        }

        /* ---------------- sets: tabs, or today's set only */
        var tabs = Array.prototype.slice.call(block.querySelectorAll('.rosary-tab'));

        function showSet(key) {
            sets.forEach(function (s) {
                var on = s.getAttribute('data-set') === key;
                s.classList.toggle('rosary-tabhidden', !on);
                s.style.display = on ? '' : 'none';
            });
            tabs.forEach(function (t) {
                t.setAttribute('aria-selected', t.getAttribute('data-set') === key ? 'true' : 'false');
            });
        }

        if (config.mode === 'all') {
            tabs.forEach(function (t) {
                var small = t.querySelector('small');
                if (small) t.title = 'Prayed on ' + small.textContent;
                if (t.getAttribute('data-set') === today) {
                    t.insertBefore(el('span', 'rosary-today-badge', 'Today'), t.querySelector('small'));
                    t.classList.add('rosary-tab-today');
                }
                t.addEventListener('click', function () {
                    stopAuto();
                    showSet(t.getAttribute('data-set'));
                });
            });
            showSet(config.open || today);
        } else if (config.mode === 'today') {
            sets.forEach(function (s) {
                if (s.getAttribute('data-set') !== today) {
                    s.classList.add('rosary-hidden');
                    s.style.display = 'none';
                }
            });
        }

        /* the previous or next mystery (or opening / closing prayers); past the
         * end of a set it carries on into the next set */
        function stepMystery(d) {
            var visible = sets.filter(function (s) { return s.style.display !== 'none'; });
            var set = visible[0];
            if (!set || !set.rosaryShowMystery) return;
            var cards = Array.prototype.slice.call(set.querySelectorAll('.rosary-mystery')).filter(function (m) {
                return !m.classList.contains('rosary-extra') || extraOn();
            });
            var act = set.querySelector('.rosary-mystery.rosary-active');
            var i = cards.indexOf(act) + d;
            stopAuto();
            if (i < 0 || i >= cards.length) {
                if (config.mode !== 'all' || !tabs.length) {
                    i = (i + cards.length) % cards.length;
                } else {
                    var keys = tabs.map(function (t) { return t.getAttribute('data-set'); });
                    var k = (keys.indexOf(set.getAttribute('data-set')) + d + keys.length) % keys.length;
                    showSet(keys[k]);
                    set = sets.filter(function (s) { return s.getAttribute('data-set') === keys[k]; })[0];
                    cards = Array.prototype.slice.call(set.querySelectorAll('.rosary-mystery')).filter(function (m) {
                        return !m.classList.contains('rosary-extra') || extraOn();
                    });
                    i = d > 0 ? 0 : cards.length - 1;
                }
            }
            set.rosaryShowMystery(Number(cards[i].getAttribute('data-index')));
            var r = set.getBoundingClientRect();
            if (r.top < 0) set.scrollIntoView({ block: 'start' });
        }

        function stopAuto() {
            state.auto = false;
            state.speaking = null;
            stopSpeech();
            refreshAll();
        }

        /* ---------------- each set: mystery picker */
        sets.forEach(function (set) {
            if (config.beads) addPresentControls(set);
            var mysteries = Array.prototype.slice.call(set.querySelectorAll('.rosary-mystery'));
            var navButtons = Array.prototype.slice.call(set.querySelectorAll('.rosary-nav-btn'));

            function showMystery(index) {
                mysteries.forEach(function (m) {
                    m.classList.toggle('rosary-active', Number(m.getAttribute('data-index')) === index);
                });
                navButtons.forEach(function (b) {
                    if (Number(b.getAttribute('data-index')) === index) b.setAttribute('aria-current', 'true');
                    else b.removeAttribute('aria-current');
                });
            }
            navButtons.forEach(function (b) {
                b.addEventListener('click', function () {
                    stopAuto();
                    showMystery(Number(b.getAttribute('data-index')));
                });
            });

            // cards that are switched on: the opening and closing prayers only with
            // the Opening & closing option
            function enabled(m) { return !m.classList.contains('rosary-extra') || extraOn(); }
            mysteries.forEach(function (m, mi) {
                if (!config.beads) return;
                var onFinish = function () {
                    // after the last bead: on to the next card of the set
                    if (!navButtons.length) return false;
                    for (var j = mi + 1; j < mysteries.length; j++) {
                        if (!enabled(mysteries[j])) continue;
                        showMystery(Number(mysteries[j].getAttribute('data-index')));
                        mysteries[j].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        mysteries[j].rosaryGo(0);
                        return true;
                    }
                    return false;
                };
                if (m.classList.contains('rosary-prayers-card')) initPrayers(m, onFinish);
                else initDecade(m, onFinish);
            });
            set.rosaryShowMystery = showMystery;
        });
        if (extraOn()) sets.forEach(function (set) { if (set.rosaryShowMystery) set.rosaryShowMystery(-1); });

        /* ---------------- the opening or closing prayers: one bead per prayer */
        function initPrayers(card, onFinish) {
            var LISTEN_ONE = LBL.listenPrayer, LISTEN_ALL = LBL.allPrayers;
            var decade = card.querySelector('.rosary-decade');
            var controls = card.querySelector('.rosary-controls');
            var now = card.querySelector('.rosary-now');
            var items = Array.prototype.slice.call(card.querySelectorAll('.rosary-prayer-list > li'));
            var beads = [];
            var pos = -1;

            function active(i) {
                return !items[i].classList.contains('rosary-extra-full') ||
                       block.getAttribute('data-extra') === 'full';
            }
            function nextIndex(from) { for (var j = from + 1; j < items.length; j++) if (active(j)) return j; return -1; }
            function prevIndex(from) { for (var j = from - 1; j >= 0; j--) if (active(j)) return j; return -1; }

            items.forEach(function (li, i) {
                var st = li.getAttribute('data-style');
                if (i > 0) decade.appendChild(el('span', 'rosary-chain' + (li.classList.contains('rosary-extra-full') ? ' rosary-extra-full' : '')));
                var cls = st === 'large' ? 'rosary-bead--large' : (st === 'glory' || st === 'cross') ? 'rosary-bead--glory' : '';
                var b = button('rosary-bead ' + cls, li.getAttribute('data-label'));
                b.setAttribute('aria-label', li.getAttribute('data-name'));
                if (li.classList.contains('rosary-extra-full')) b.classList.add('rosary-extra-full');
                b.addEventListener('click', function () { go(i, true); });
                beads.push(b);
                decade.appendChild(b);
                li.classList.add('rosary-step');
                li.addEventListener('click', function (e) {
                    if (e.target.closest && e.target.closest('a')) return;
                    go(i, true);
                });
            });

            var prev = button('rosary-btn', '\u25C0 Back');
            var next = button('rosary-btn rosary-btn--primary', 'Begin \u25B6');
            setLabel(prev, LBL.back);
            setLabel(next, LBL.begin);
            controls.appendChild(prev);
            controls.appendChild(next);
            var listen = null, auto = null;
            if (audio) {
                listen = button('rosary-btn rosary-btn--audio', 'This prayer', 'Read this prayer aloud, once');
                auto = button('rosary-btn rosary-btn--audio', 'All prayers',
                              'Pray aloud from here on, moving through the beads by itself');
                setLabel(listen, LBL.listenPrayer);
                setLabel(auto, LBL.allPrayers);
                controls.appendChild(audioGroup(listen, auto));
            }
            var present = button('rosary-btn rosary-btn--present', '\u26F6 Full screen', 'Show this prayer full screen');
            fullLabel(present);
            controls.appendChild(present);
            // the Listen group last, so Back, Next and Full screen share the first row
            var agroup = controls.querySelector('.rosary-audio-group');
            if (agroup) controls.appendChild(agroup);
            present.addEventListener('click', function () {
                var set = card.closest('.rosary-set');
                if (set.classList.contains('rosary-presenting')) { endPresent(set); return; }
                var start = function () {
                    set.classList.add('rosary-presenting');
                    updatePhotos();
                    if (pos < 0) go(0, true);
                };
                if (FULLSCREEN) set.requestFullscreen().then(start).catch(function () { pseudoPresent(set, start); });
                else pseudoPresent(set, start);
            });

            prev.addEventListener('click', function () { var p = prevIndex(pos); if (p !== -1) go(p, true); });
            next.addEventListener('click', function () { advance(true); });
            if (listen) listen.addEventListener('click', function () {
                if (state.speaking === card && !state.auto) { stopAuto(); return; }
                state.auto = false;
                if (pos < 0) go(0, false);
                speakBead(null);
            });
            if (auto) auto.addEventListener('click', function () {
                if (state.auto && state.speaking === card) { stopAuto(); return; }
                state.auto = true;
                if (pos < 0 || nextIndex(pos) === -1) go(0, false);
                else speakBead(autoNext);
            });

            function advance(manual) {
                var n = nextIndex(pos);
                if (n === -1) {
                    if (!onFinish()) {
                        if (manual) go(-1, true);
                        else stopAuto();
                    }
                } else {
                    go(n, manual);
                }
            }
            function autoNext() {
                if (!state.auto) return;
                setTimeout(function () { if (state.auto) advance(false); }, 700);
            }
            function speakBead(done) {
                var li = items[pos];
                if (!li) return;
                state.speaking = card;
                refreshAll();
                // the prayer's name (and intention) only with "Read prayer names"
                var intent = li.getAttribute('data-intent');
                var title = state.readTitles ? li.getAttribute('data-name') + (intent ? ', ' + intent : '') + '.' : '';
                speak([title, li.getAttribute('data-text')], function () {
                    if (!state.auto) { state.speaking = null; refreshAll(); }
                    if (done) done();
                });
            }
            function render() {
                beads.forEach(function (b, i) {
                    b.classList.toggle('rosary-here', i === pos);
                    b.classList.toggle('rosary-done', pos >= 0 && i < pos);
                });
                items.forEach(function (li, i) { li.classList.toggle('rosary-here', i === pos); });
                prev.disabled = prevIndex(pos) === -1;
                setLabel(next, pos < 0 ? LBL.begin : (nextIndex(pos) === -1 ? LBL.finish : LBL.next));
                var speakingHere = state.speaking === card;
                if (listen) {
                    setLabel(listen, speakingHere && !state.auto ? LBL.stop : LISTEN_ONE);
                    listen.classList.toggle('rosary-on', speakingHere && !state.auto);
                }
                if (auto) {
                    setLabel(auto, state.auto && speakingHere ? LBL.stop : LISTEN_ALL);
                    auto.classList.toggle('rosary-on', state.auto && speakingHere);
                }
                now.classList.toggle('rosary-speaking', speakingHere);
                now.textContent = '';
                var li = items[pos];
                if (!li) return;
                var intent = li.getAttribute('data-intent');
                now.appendChild(el('span', 'rosary-now-label', li.getAttribute('data-name') + (intent ? ' \u2013 ' + intent : '')));
                li.querySelectorAll('.rosary-prayer-text').forEach(function (t) {
                    now.appendChild(el('p', 'rosary-now-prayer rosary-now-prayer-always', t.textContent));
                });
                // how to make the Sign of the Cross (shown, not read aloud)
                if (li.getAttribute('data-name') === 'The Sign of the Cross') {
                    now.appendChild(el('p', 'rosary-now-hint',
                        'Touch your forehead, your breast, your left shoulder, then your right shoulder.'));
                }
            }
            function go(index, manual) {
                pos = Math.max(-1, Math.min(items.length - 1, index));
                if (pos >= 0 && !active(pos)) pos = nextIndex(pos) === -1 ? prevIndex(pos) : nextIndex(pos);
                if (manual && state.speaking && !state.auto) { state.speaking = null; stopSpeech(); }
                render();
                if (state.auto && pos >= 0) speakBead(autoNext);
                else if (manual && state.speaking === null) refreshAll();
            }
            card.rosaryGo = function (index) { go(index, false); };
            refreshers.push(render);
            render();
        }

        /* ---------------- one decade */
        function initDecade(mystery, onFinish) {
            var LISTEN_ONE = LBL.listenBead, LISTEN_ALL = LBL.allDecade;
            var decade = mystery.querySelector('.rosary-decade');
            var controls = mystery.querySelector('.rosary-controls');
            var now = mystery.querySelector('.rosary-now');
            if (!decade || !controls || !now) return;

            var items = Array.prototype.slice.call(mystery.querySelectorAll('.rosary-refs > li'));
            var title = mystery.querySelector('.rosary-mystery-title').textContent;
            var ordinal = mystery.querySelector('.rosary-num').textContent;
            var fruit = mystery.querySelector('.rosary-fruit strong').textContent;
            var beads = [];
            var pos = -1;

            function addBead(label, cls, aria) {
                var b = button('rosary-bead ' + (cls || ''), label);
                b.setAttribute('aria-label', aria);
                var index = beads.length;
                b.addEventListener('click', function () { go(index, true); });
                beads.push(b);
                decade.appendChild(b);
            }
            addBead('', 'rosary-bead--large', 'Our Father');
            decade.appendChild(el('span', 'rosary-chain'));
            for (var i = 1; i <= 10; i++) {
                addBead(String(i), '', 'Hail Mary ' + i + ': ' + (items[i - 1] ? items[i - 1].getAttribute('data-ref') : ''));
            }
            decade.appendChild(el('span', 'rosary-chain'));
            addBead('Glory Be', 'rosary-bead--glory', 'Glory Be');

            var prev = button('rosary-btn', '◀ Back');
            var next = button('rosary-btn rosary-btn--primary', 'Begin ▶');
            setLabel(prev, LBL.back);
            setLabel(next, LBL.begin);
            controls.appendChild(prev);
            controls.appendChild(next);

            var listen = null, auto = null;
            if (audio) {
                listen = button('rosary-btn rosary-btn--audio', 'This bead', 'Read this bead aloud, once');
                auto = button('rosary-btn rosary-btn--audio', 'Whole decade',
                              'Pray the decade aloud, bead by bead, moving on by itself');
                setLabel(listen, LBL.listenBead);
                setLabel(auto, LBL.allDecade);
                controls.appendChild(audioGroup(listen, auto));
            }

            var present = button('rosary-btn rosary-btn--present', '\u26F6 Full screen',
                                 'Show this mystery full screen (arrow keys or swipes move through the beads)');
            fullLabel(present);
            controls.appendChild(present);
            // the Listen group last, so Back, Next and Full screen share the first row
            var agroup = controls.querySelector('.rosary-audio-group');
            if (agroup) controls.appendChild(agroup);
            present.addEventListener('click', function () {
                var set = mystery.closest('.rosary-set');
                if (set.classList.contains('rosary-presenting')) { endPresent(set); return; }
                var start = function () {
                    set.classList.add('rosary-presenting');
                    updatePhotos();
                    if (pos < 0) go(0, true);
                };
                if (FULLSCREEN) {
                    set.requestFullscreen().then(start).catch(function () { pseudoPresent(set, start); });
                } else {
                    pseudoPresent(set, start);     // iPhone: fill the browser window instead
                }
            });

            var toggle = null;
            if (!prayersBox) {     // no Options panel on this rosary: keep a checkbox here
                var toggleLabel = el('label', 'rosary-toggle');
                toggle = el('input');
                toggle.type = 'checkbox';
                toggle.checked = state.showPrayers;
                toggleLabel.appendChild(toggle);
                toggleLabel.appendChild(document.createTextNode(' Show the prayers'));
                controls.appendChild(toggleLabel);
            }

            prev.addEventListener('click', function () { if (pos > 0) go(pos - 1, true); });
            next.addEventListener('click', function () { advance(true); });
            if (toggle) toggle.addEventListener('change', function () {
                state.showPrayers = toggle.checked;
                store('rosary-prayers', state.showPrayers ? '1' : '0');
                refreshAll();
            });
            if (listen) listen.addEventListener('click', function () {
                if (state.speaking === mystery && !state.auto) { stopAuto(); return; }
                state.auto = false;
                if (pos < 0) go(0, false);
                speakBead(null);
            });
            if (auto) auto.addEventListener('click', function () {
                if (state.auto && state.speaking === mystery) { stopAuto(); return; }
                state.auto = true;
                if (pos < 0 || pos >= 11) go(0, false);   // go() starts the reading
                else speakBead(autoNext);
            });

            function advance(manual) {
                if (pos >= 11) {
                    var moved = onFinish();
                    if (!moved) {
                        if (manual) go(-1, true);
                        else stopAuto();
                    }
                } else {
                    go(pos + 1, manual);
                }
            }

            function autoNext() {
                if (!state.auto) return;
                setTimeout(function () { if (state.auto) advance(false); }, 700);
            }

            /* what is read aloud for the current bead */
            // what is chosen under "Under the beads" instead of the ten steps (a
            // meditation, offering, classic meditation or modern reflection): its
            // parts marked rosary-say are shown and read on the Our Father bead
            function meditation() {
                var under = block.getAttribute('data-under');
                if (!under || under === 'steps') return null;
                var box = mystery.querySelector('.rosary-under-box.rosary-' + under);
                if (!box) return null;
                var parts = Array.prototype.map.call(box.querySelectorAll('.rosary-say'), function (e) {
                    return e.textContent;
                });
                // read aloud without the bracketed references, e.g. "(St. Mark, XIV, 36.)"
                parts.spoken = parts.map(function (t) {
                    return t.replace(/\s*\([^()]*\d[^()]*\)\.?/g, '').replace(/\s+([.,;:!?])/g, '$1');
                });
                return parts.length ? parts : null;
            }

            function beadTexts() {
                var p = state.showPrayers;
                if (pos === 0) {
                    var med = meditation();
                    return [ordinal + '. ' + title + '. The fruit of the mystery: ' + fruit + '.']
                        .concat(med ? med.spoken : [])
                        .concat([p && prayers['our-father'] ? prayers['our-father'][1] : '']);
                }
                if (pos >= 1 && pos <= 10) {
                    var li = items[pos - 1];
                    var cap = li ? li.getAttribute('data-cap') : '';
                    var verse = li ? li.getAttribute('data-text') : '';
                    var read = state.read === 'step' || !verse ? [cap]
                             : state.read === 'scripture' ? [verse] : [cap + '.', verse];
                    return read.concat([p && prayers['hail-mary'] ? prayers['hail-mary'][1] : '']);
                }
                if (pos === 11) {
                    var fatima = state.fatima && prayers.fatima ? prayers.fatima[1] : '';
                    return p ? [prayers['glory-be'] ? prayers['glory-be'][1] : '', fatima]
                             : ['Glory be to the Father, and to the Son, and to the Holy Spirit.', fatima];
                }
                return [];
            }

            function speakBead(done) {
                state.speaking = mystery;
                refreshAll();
                speak(beadTexts(), function () {
                    if (!state.auto) { state.speaking = null; refreshAll(); }
                    if (done) done();
                });
            }

            function prayer(key) {
                var p = prayers[key];
                return p ? el('p', 'rosary-now-prayer', p[1]) : null;
            }

            function render() {
                if (toggle) toggle.checked = state.showPrayers;
                if (prayersBox) prayersBox.checked = state.showPrayers;
                beads.forEach(function (b, i) {
                    b.classList.toggle('rosary-here', i === pos);
                    b.classList.toggle('rosary-done', pos >= 0 && i < pos);
                });
                items.forEach(function (li, i) { li.classList.toggle('rosary-here', i + 1 === pos); });
                prev.disabled = pos <= 0;
                setLabel(next, pos < 0 ? LBL.begin : (pos >= 11 ? LBL.finishDecade : LBL.next));
                var speakingHere = state.speaking === mystery;
                if (listen) {
                    setLabel(listen, speakingHere && !state.auto ? LBL.stop : LISTEN_ONE);
                    listen.classList.toggle('rosary-on', speakingHere && !state.auto);
                }
                if (auto) {
                    setLabel(auto, state.auto && speakingHere ? LBL.stop : LISTEN_ALL);
                    auto.classList.toggle('rosary-on', state.auto && speakingHere);
                }
                now.classList.toggle('rosary-speaking', speakingHere);

                now.textContent = '';
                if (pos < 0) return;
                var label, line, extra = [];
                if (pos === 0) {
                    label = 'Our Father';
                    line = el('div');
                    line.appendChild(el('span', 'rosary-now-ref', ordinal + ': ' + title));
                    line.appendChild(document.createTextNode(' – fruit: ' + fruit));
                    // the meditation, in the panel only in full screen (it is under the beads otherwise)
                    var md = meditation();
                    if (md) md.forEach(function (t) { extra.push(el('p', 'rosary-now-meditation', t)); });
                    if (state.showPrayers) extra.push(prayer('our-father'));
                } else if (pos <= 10) {
                    var li = items[pos - 1];
                    label = 'Hail Mary ' + pos + ' of 10';
                    line = el('div');
                    line.appendChild(el('span', 'rosary-now-ref', li ? li.getAttribute('data-ref') : ''));
                    if (li) line.appendChild(document.createTextNode(' – ' + li.getAttribute('data-cap')));
                    if (li && li.getAttribute('data-text')) extra.push(el('p', 'rosary-now-verse', li.getAttribute('data-text')));
                    if (state.showPrayers) extra.push(prayer('hail-mary'));
                } else {
                    label = 'Glory Be';
                    line = el('div', '', 'End of the ' + ordinal.toLowerCase() + '.');
                    if (state.showPrayers) {
                        extra.push(prayer('glory-be'));
                        if (state.fatima) extra.push(prayer('fatima'));
                    }
                }
                now.appendChild(el('span', 'rosary-now-label', label));
                now.appendChild(line);
                extra.forEach(function (p) { if (p) now.appendChild(p); });
            }

            /* manual: the reader clicked; while praying aloud, carry on from there */
            function go(index, manual) {
                pos = Math.max(-1, Math.min(11, index));
                if (manual && state.speaking && !state.auto) { state.speaking = null; stopSpeech(); }
                render();
                if (state.auto && pos >= 0) {
                    speakBead(autoNext);
                } else if (manual && state.speaking === null) {
                    refreshAll();
                }
            }
            mystery.rosaryGo = function (index) { go(index, false); };
            // click a step in the list to go to its bead
            items.forEach(function (li, i) {
                li.classList.add('rosary-step');
                li.addEventListener('click', function (e) {
                    if (e.target.closest && e.target.closest('a')) return;
                    go(i + 1, true);
                });
            });
            refreshers.push(render);
            render();
        }
    }

    /* ------------------------------------------------------------ whole painting */

    function showPainting(img) {
        var overlay = el('div', 'rosary-lightbox');
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-label', img.alt || 'Painting');
        var big = el('img');
        big.src = img.getAttribute('data-full');
        big.alt = img.alt;
        var cap = el('p', 'rosary-lightbox-caption', img.getAttribute('data-credit') || img.alt);
        var close = button('rosary-lightbox-close', '\u2715', 'Close');
        overlay.appendChild(close);
        overlay.appendChild(big);
        overlay.appendChild(cap);
        function shut() {
            document.removeEventListener('keydown', onKey);
            overlay.remove();
            img.focus && img.focus();
        }
        function onKey(e) { if (e.key === 'Escape') shut(); }
        overlay.addEventListener('click', function (e) { if (e.target !== big) shut(); });
        document.addEventListener('keydown', onKey);
        document.body.appendChild(overlay);
        close.focus();
    }

    document.addEventListener('click', function (e) {
        if (presentingSet()) return;
        var img = e.target.closest && e.target.closest('.rosary-icon .rosary-photo[data-full]');
        if (img) showPainting(img);
    });

    /* Full screen -------------------------------------------------------
     * Real full screen where the browser allows it; otherwise (iPhone Safari)
     * the set fills the browser window. An Exit button, Esc, the arrow keys
     * and left/right swipes work in both. */
    function stopPresent(set) {
        set.classList.remove('rosary-presenting', 'rosary-pseudo-fs');
        document.documentElement.classList.remove('rosary-noscroll');
        var block = set.closest('.rosary-block');
        if (block && block.rosaryUpdatePhotos) block.rosaryUpdatePhotos();
    }
    function endPresent(set) {
        if (document.fullscreenElement) document.exitFullscreen();
        else stopPresent(set);
    }
    function pseudoPresent(set, start) {
        set.classList.add('rosary-pseudo-fs');
        document.documentElement.classList.add('rosary-noscroll');
        start();
        set.scrollTop = 0;
    }
    function presentingSet() {
        var fs = document.fullscreenElement;
        if (fs && fs.classList.contains('rosary-presenting')) return fs;
        return document.querySelector('.rosary-set.rosary-pseudo-fs.rosary-presenting');
    }
    function step(set, forward) {
        var m = set.querySelector('.rosary-mystery.rosary-active');
        if (!m) return;
        if (forward) {
            m.querySelector('.rosary-btn--primary').click();
        } else {
            var back = m.querySelector('.rosary-controls .rosary-btn:not(.rosary-btn--primary)');
            if (back && !back.disabled) back.click();
        }
    }
    // an Exit button inside each set, shown only while presenting, and swipes
    function addPresentControls(set) {
        {
            var exit = button('rosary-exit-present', '\u2715 Exit', 'Leave full screen');
            exit.addEventListener('click', function () { endPresent(set); });
            set.insertBefore(exit, set.firstChild);
            // swipe left = next bead, swipe right = back
            var x0 = null, y0 = null;
            set.addEventListener('touchstart', function (e) {
                if (!set.classList.contains('rosary-presenting') || e.touches.length !== 1) return;
                x0 = e.touches[0].clientX; y0 = e.touches[0].clientY;
            }, { passive: true });
            set.addEventListener('touchend', function (e) {
                if (x0 === null) return;
                var dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
                x0 = null;
                if (Math.abs(dx) > 60 && Math.abs(dx) > 2 * Math.abs(dy)) step(set, dx < 0);
            }, { passive: true });
        }
    }
    document.addEventListener('fullscreenchange', function () {
        if (document.fullscreenElement) return;
        document.querySelectorAll('.rosary-presenting:not(.rosary-pseudo-fs)').forEach(stopPresent);
    });
    document.addEventListener('keydown', function (e) {
        var set = presentingSet();
        if (!set) return;
        if (e.key === 'Escape' && set.classList.contains('rosary-pseudo-fs')) { stopPresent(set); return; }
        if (e.target.closest && e.target.closest('select, input')) return;
        var nextKeys = ['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'];
        var prevKeys = ['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'];
        if (nextKeys.indexOf(e.key) !== -1) {
            e.preventDefault();
            step(set, true);
        } else if (prevKeys.indexOf(e.key) !== -1) {
            e.preventDefault();
            step(set, false);
        }
    });

    function init() {
        var blocks = document.querySelectorAll('.rosary-block');
        for (var i = 0; i < blocks.length; i++) {
            if (!blocks[i].classList.contains('rosary-js')) initBlock(blocks[i]);
        }
    }

    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
    else init();
})();
