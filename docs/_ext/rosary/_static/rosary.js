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
    // drawn styles; the picture folders (Traditional paintings, Stained glass
    // windows ...) are added from the directive's config.photosets
    var STYLES = [['classic', 'Classic'], ['stained', 'Stained glass (drawn)'], ['gold', 'Gold icon']];

    function el(tag, cls, text) {
        var node = document.createElement(tag);
        if (cls) node.className = cls;
        if (text !== undefined) node.textContent = text;
        return node;
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
            read: ['step', 'both', 'scripture'].indexOf(config.read) !== -1 ? config.read : 'both'
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
        var showBtn = button('rosary-show-menus', '\u2630 Menus', 'Show the menus again');
        block.insertBefore(showBtn, topbar);
        var setMenus = function (hidden) {
            block.classList.toggle('rosary-menus-hidden', hidden);
            store('rosary-menus-hidden', hidden ? '1' : '0');
        };
        if (store('rosary-menus-hidden') === '1') block.classList.add('rosary-menus-hidden');
        hideBtn.addEventListener('click', function () { setMenus(true); });
        showBtn.addEventListener('click', function () { setMenus(false); });
        if (config.picker) {
            var picLabel = el('label', 'rosary-audio-field', 'Pictures ');
            var picSelect = el('select', 'rosary-select');
            STYLES.concat(config.photosets || []).forEach(function (st) {
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
            [['same', 'Same as pictures']].concat(STYLES, config.photosets || []).forEach(function (st) {
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
            [['phone', 'Phone-size picture'], ['compact', 'Compact'], ['side', 'Large picture beside details'],
             ['large', 'Large picture above details']].forEach(function (l) {
                var o = el('option', '', l[1]);
                o.value = l[0];
                laySelect.appendChild(o);
            });
            var savedLayout = store(STORE_LAYOUT);
            if (['phone', 'compact', 'side', 'large'].indexOf(savedLayout) !== -1) block.setAttribute('data-layout', savedLayout);
            laySelect.value = block.getAttribute('data-layout') || 'phone';
            laySelect.addEventListener('change', function () {
                block.setAttribute('data-layout', laySelect.value);
                store(STORE_LAYOUT, laySelect.value);
                updatePhotos();
                if (block.rosaryWiden) block.rosaryWiden();
            });
            layLabel.appendChild(laySelect);
            bar.appendChild(layLabel);

            /* scripture under the steps: all, the current step only, or none */
            if (block.querySelector('.rosary-verse')) {
                var verLabel = el('label', 'rosary-audio-field', 'Verses ');
                var verSelect = el('select', 'rosary-select');
                [['all', 'All'], ['current', 'Current step only'], ['none', 'Hidden']].forEach(function (v) {
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
        }

        /* large layout and Present mode show the whole painting, not the crop */
        function updatePhotos() {
            var big = block.getAttribute('data-layout') !== 'compact' ||
                      !!block.querySelector('.rosary-presenting');
            block.querySelectorAll('.rosary-mystery .rosary-icon .rosary-photo[data-full]').forEach(function (img) {
                if (!img.getAttribute('data-crop')) img.setAttribute('data-crop', img.getAttribute('src'));
                var want = big ? img.getAttribute('data-full') : img.getAttribute('data-crop');
                if (img.getAttribute('src') !== want) img.setAttribute('src', want);
            });
        }
        updatePhotos();
        block.rosaryUpdatePhotos = updatePhotos;

        /* side-by-side: widen the block into empty space right of the page's
         * column, so the picture can be as large as the screen allows */
        function widen() {
            block.style.removeProperty('--rosary-widen');
            block.removeAttribute('data-widen');
            if (block.getAttribute('data-layout') !== 'side' || window.innerWidth < 1100) return;
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

        function stopAuto() {
            state.auto = false;
            state.speaking = null;
            stopSpeech();
            refreshAll();
        }

        /* ---------------- each set: mystery picker */
        sets.forEach(function (set) {
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

            mysteries.forEach(function (m, mi) {
                if (config.beads) initDecade(m, function () {
                    // after the Glory Be: on to the next mystery of the set
                    if (mi + 1 < mysteries.length && navButtons.length) {
                        showMystery(Number(mysteries[mi + 1].getAttribute('data-index')));
                        mysteries[mi + 1].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                        mysteries[mi + 1].rosaryGo(0);
                        return true;
                    }
                    return false;
                });
            });
        });

        /* ---------------- one decade */
        function initDecade(mystery, onFinish) {
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
            controls.appendChild(prev);
            controls.appendChild(next);

            var listen = null, auto = null;
            if (audio) {
                listen = button('rosary-btn rosary-btn--audio', '🔊 Listen', 'Read this bead aloud');
                auto = button('rosary-btn rosary-btn--audio', '▶ Pray aloud', 'Read the whole decade aloud, bead by bead');
                controls.appendChild(listen);
                controls.appendChild(auto);
            }

            if (FULLSCREEN) {
                var present = button('rosary-btn rosary-btn--present', '\u26F6 Present',
                                     'Show this mystery full screen (arrow keys move through the beads, Esc to finish)');
                controls.appendChild(present);
                present.addEventListener('click', function () {
                    var set = mystery.closest('.rosary-set');
                    if (document.fullscreenElement) { document.exitFullscreen(); return; }
                    set.requestFullscreen().then(function () {
                        set.classList.add('rosary-presenting');
                        updatePhotos();
                        if (pos < 0) go(0, true);
                    }).catch(function () { /* refused */ });
                });
            }

            var toggleLabel = el('label', 'rosary-toggle');
            var toggle = el('input');
            toggle.type = 'checkbox';
            toggle.checked = state.showPrayers;
            toggleLabel.appendChild(toggle);
            toggleLabel.appendChild(document.createTextNode(' Show the prayers'));
            controls.appendChild(toggleLabel);

            prev.addEventListener('click', function () { if (pos > 0) go(pos - 1, true); });
            next.addEventListener('click', function () { advance(true); });
            toggle.addEventListener('change', function () {
                state.showPrayers = toggle.checked;
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
            function beadTexts() {
                var p = state.showPrayers;
                if (pos === 0) {
                    return [ordinal + '. ' + title + '. The fruit of the mystery: ' + fruit + '.',
                            p && prayers['our-father'] ? prayers['our-father'][1] : ''];
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
                    return p ? [prayers['glory-be'] ? prayers['glory-be'][1] : '', prayers.fatima ? prayers.fatima[1] : '']
                             : ['Glory be to the Father, and to the Son, and to the Holy Spirit.'];
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
                toggle.checked = state.showPrayers;
                beads.forEach(function (b, i) {
                    b.classList.toggle('rosary-here', i === pos);
                    b.classList.toggle('rosary-done', pos >= 0 && i < pos);
                });
                items.forEach(function (li, i) { li.classList.toggle('rosary-here', i + 1 === pos); });
                prev.disabled = pos <= 0;
                next.textContent = pos < 0 ? 'Begin ▶' : (pos >= 11 ? 'Finish decade ✔' : 'Next ▶');
                var speakingHere = state.speaking === mystery;
                if (listen) {
                    listen.textContent = speakingHere && !state.auto ? '■ Stop' : '🔊 Listen';
                    listen.classList.toggle('rosary-on', speakingHere && !state.auto);
                }
                if (auto) {
                    auto.textContent = state.auto && speakingHere ? '■ Stop' : '▶ Pray aloud';
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
                    if (state.showPrayers) { extra.push(prayer('glory-be')); extra.push(prayer('fatima')); }
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
        if (document.fullscreenElement) return;
        var img = e.target.closest && e.target.closest('.rosary-icon .rosary-photo[data-full]');
        if (img) showPainting(img);
    });

    /* Present mode: leaving full screen, and keys to move through the beads */
    document.addEventListener('fullscreenchange', function () {
        if (document.fullscreenElement) return;
        document.querySelectorAll('.rosary-presenting').forEach(function (set) {
            set.classList.remove('rosary-presenting');
            var block = set.closest('.rosary-block');
            if (block && block.rosaryUpdatePhotos) block.rosaryUpdatePhotos();
        });
    });
    document.addEventListener('keydown', function (e) {
        var set = document.fullscreenElement;
        if (!set || !set.classList.contains('rosary-presenting')) return;
        if (e.target.closest && e.target.closest('select, input')) return;
        var m = set.querySelector('.rosary-mystery.rosary-active');
        if (!m) return;
        var nextKeys = ['ArrowRight', 'ArrowDown', 'PageDown', ' ', 'Enter'];
        var prevKeys = ['ArrowLeft', 'ArrowUp', 'PageUp', 'Backspace'];
        if (nextKeys.indexOf(e.key) !== -1) {
            e.preventDefault();
            m.querySelector('.rosary-btn--primary').click();
        } else if (prevKeys.indexOf(e.key) !== -1) {
            e.preventDefault();
            var back = m.querySelector('.rosary-controls .rosary-btn:not(.rosary-btn--primary)');
            if (back && !back.disabled) back.click();
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
