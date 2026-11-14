"""Meditations and offerings for the twenty mysteries.

Shown instead of the ten steps when the reader chooses, under "Under the
beads" in the Options panel:

  "A meditation"                MEDITATIONS: (meditation, prayer), about a
                                hundred words each  (:under: meditation)
  "A Montfort-style offering"   OFFERINGS: one offering of the decade, in the
                                manner of St Louis de Montfort's first method
                                (:under: offering)
  "A modern reflection"         MODERN: (reflection, question), plain
                                everyday English, about seventy words, ending
                                with a question to think about
                                (:under: modern)
  "A meditation on the virtue"  VIRTUES: (meditation, prayer) on the
                                mystery's fruit: what the virtue is, how the
                                mystery shows it, how to practise it
                                (:under: virtue)
  "An intention"                INTENTIONS: (intention, reflection, prayer),
                                the people and needs this decade is offered
                                for (:under: intention)

The classic 1915 meditations are in rosary_classic.py.

Original text written for this site; free to use and edit.
"""

MEDITATIONS = {
    'joyful': [
        # 1. The Annunciation - Humility
        ("The eternal Word, through whom all things were made, waits upon the consent "
         "of a young woman in Nazareth. God, who needs nothing, chooses to ask. Gabriel "
         "greets Mary as full of grace: filled by God before she has done anything, she "
         "is the first fruit of a redemption not yet accomplished. Her answer, “Let it "
         "be done to me according to your word”, undoes Eve’s grasping with a free "
         "and humble yes. In that moment the Word becomes flesh, and heaven and earth are "
         "joined in her womb. Humility is not smallness but truth: receiving everything "
         "as gift.",
         "Mary, teach me to welcome God’s word with your open and undivided heart."),
        # 2. The Visitation - Love of neighbour
        ("Carrying Christ within her, Mary does not stay at home to ponder; she hurries "
         "into the hill country to serve. Wherever she brings him, grace overflows. John "
         "leaps in Elizabeth’s womb, the forerunner recognising the Lord before either "
         "is born, and Elizabeth, filled with the Holy Spirit, blesses the mother and her "
         "child. Mary, the new Ark of the Covenant, answers with the Magnificat, a song of "
         "the God who lifts up the lowly and fills the hungry. Love of neighbour flows "
         "from the presence of Christ: those who receive him are sent, and those they "
         "visit are blessed.",
         "Lord, make me quick to carry you to those who need you."),
        # 3. The Nativity - Poverty of spirit
        ("The Word through whom the universe was made is born in a borrowed shelter and "
         "laid in a manger, the feeding trough of animals: he who is the Bread from heaven "
         "comes to be food for the world. God does not overpower us with glory. He empties "
         "himself and becomes a child who must be held, fed and protected. The first to "
         "come are shepherds, poor and on the edge of society, while angels proclaim peace "
         "to those God favours. Poverty of spirit is the open hand that knows it has "
         "nothing of its own, and so can receive God himself.",
         "Jesus, born poor for my sake, empty me of all that keeps me from receiving you."),
        # 4. The Presentation in the Temple - Obedience
        ("Mary and Joseph bring Jesus to the Temple to fulfil the Law, offering the "
         "sacrifice of the poor, two young birds. The Lawgiver submits to the Law; the "
         "true Temple enters the temple made with hands. Simeon, who has waited a "
         "lifetime, takes the child in his arms and blesses God: here is the light for "
         "the nations and the glory of Israel. Then he turns to Mary and speaks of a sword "
         "that will pierce her soul. Obedience is not mere compliance. It is entrusting "
         "our lives to God’s plan, even when that plan includes the cross.",
         "Father, help me offer my life to you as freely as Mary offered her Son."),
        # 5. The Finding of Jesus in the Temple - Joy in finding Jesus
        ("For three days Mary and Joseph search Jerusalem in anguish, a foreshadowing of "
         "the three days in the tomb. They find Jesus in the Temple, listening, asking "
         "questions and astonishing the teachers. His first recorded words reveal who he "
         "is: he must be in his Father’s house. Mary does not fully understand, yet she "
         "keeps all these things in her heart. Every Christian life has seasons of "
         "searching, when Christ seems lost to us. He is found where the Father’s will "
         "is done, and the joy of finding him is greater for the seeking.",
         "Lord, when I lose sight of you, draw me back to your Father’s house."),
    ],
    'luminous': [
        # 1. The Baptism of Jesus in the Jordan - Openness to the Holy Spirit
        ("The sinless one goes down into the Jordan among sinners, not to be cleansed "
         "but to make the waters cleansing. Taking his place with us, he begins the "
         "journey that will end on the cross. As he rises from the water the heavens are "
         "opened, the Spirit descends like a dove, and the Father’s voice declares him "
         "the beloved Son. Here the Trinity is revealed, and here our own baptism finds "
         "its source: in Christ we too become beloved sons and daughters, anointed by the "
         "same Spirit. To be open to the Spirit is to let God finish in us what baptism "
         "began.",
         "Holy Spirit, renew in me the grace of my baptism."),
        # 2. The Wedding at Cana - To Jesus through Mary
        ("At a village wedding the wine runs out, and Mary notices before anyone else. "
         "She simply tells her Son, “They have no wine,” and then tells the "
         "servants, “Do whatever he tells you.” These words sum up her whole "
         "mission: to bring our needs to Jesus and to point us towards him. He turns the "
         "water meant for purification into abundant, excellent wine, the sign of the "
         "wedding feast at which God takes his people as his bride. Through Mary’s "
         "intercession the first of his signs is given, and his disciples begin to "
         "believe.",
         "Mother of Jesus, bring my needs to your Son, and teach me to do whatever he "
         "tells me."),
        # 3. The Proclamation of the Kingdom - Repentance and trust in God
        ("Jesus comes into Galilee announcing that the time is fulfilled and the Kingdom "
         "of God is near: repent, and believe the Good News. The Kingdom is not first a "
         "place but a person; in Jesus, God’s reign has arrived. He brings good news to "
         "the poor, release to captives and sight to the blind, and he blesses the poor "
         "in spirit, the merciful and the peacemakers. He forgives sins, heals the sick "
         "and eats with sinners. Repentance means turning around, letting go of our own "
         "small kingdoms, and trusting that the Father’s rule is mercy.",
         "Lord Jesus, turn my heart towards you, and teach me to seek your Kingdom above "
         "all."),
        # 4. The Transfiguration - Desire for holiness
        ("On the mountain Jesus is transfigured before Peter, James and John: his face "
         "shines like the sun and his clothes become dazzling white. Moses and Elijah, the "
         "Law and the Prophets, speak with him of the death he will accomplish in "
         "Jerusalem. The glory the disciples glimpse is not borrowed light but his own, "
         "the radiance of the eternal Son, shown to strengthen them before the scandal of "
         "the cross. A cloud overshadows them, and the Father tells them to listen to his "
         "beloved Son. Holiness is this: to listen to Jesus until his light shines "
         "through us.",
         "Father, let me listen to your Son, and be changed into his likeness."),
        # 5. The Institution of the Eucharist - Adoration
        ("On the night he was betrayed, Jesus gathers his disciples for the Passover and, "
         "having loved his own, loves them to the end. He kneels to wash their feet. Then "
         "he takes bread and says, “This is my body,” and gives them the cup of his "
         "blood of the new covenant. What he will offer on the cross the next day he "
         "gives them now, under the signs of bread and wine, and he commands them to do "
         "this in memory of him. In the Eucharist Christ remains with us as sacrifice, "
         "presence and food. Adoration is the only fitting answer to a God who makes "
         "himself so small for love.",
         "Jesus, truly present in the Eucharist, I adore you and I thank you."),
    ],
    'sorrowful': [
        # 1. The Agony in the Garden - Sorrow for sin
        ("In the garden of Gethsemane the new Adam enters the struggle that the first "
         "Adam lost in a garden. Jesus, fully God and fully man, feels the weight of the "
         "sin of the world and the horror of death, and his sweat falls like drops of "
         "blood. He prays that the cup might pass, yet his human will yields completely to "
         "the Father’s: not my will, but yours. His disciples sleep while he keeps "
         "watch. Sorrow for sin begins here, in seeing what our sins cost him, and grows "
         "into the resolve to watch with him rather than sleep.",
         "Lord, give me true sorrow for my sins, and the grace to stay awake with you."),
        # 2. The Scourging at the Pillar - Purity
        ("Before Pilate, Jesus speaks of a kingdom not of this world and of the truth he "
         "came to bear witness to, and Pilate answers, “What is truth?” Truth "
         "itself stands before him, and he has him scourged. The body of the Son of God, "
         "formed in Mary’s womb, is torn to satisfy a crowd. By his wounds we are "
         "healed: the sins we commit in the body and against it are borne in his flesh. "
         "Purity is reverence for the body as a temple of the Holy Spirit, our own and "
         "others’, redeemed at so great a price.",
         "Jesus, scourged for me, make me pure in body, mind and heart."),
        # 3. The Crowning with Thorns - Courage
        ("The soldiers dress Jesus in purple, press a crown of thorns onto his head, put "
         "a reed in his hand and kneel in mockery, hailing him as King of the Jews. "
         "Without knowing it they speak the truth. He is the King, and the thorns, the "
         "sign of the curse on the ground after the Fall, become his crown as he takes "
         "our curse upon himself. He bears contempt in silence, not from weakness but "
         "from a strength that refuses to answer hatred with hatred. Courage is to stand "
         "with Christ when he is mocked, and to bear ridicule without bitterness.",
         "Christ my King, give me courage to stand with you when you are scorned."),
        # 4. The Carrying of the Cross - Patience
        ("Jesus goes out carrying his cross to the Place of the Skull, bearing our "
         "infirmities and carrying our sorrows, as Isaiah foretold. Weakened by the "
         "scourging, he is helped by Simon of Cyrene, who is made to share the load. The "
         "women of Jerusalem weep for him, and even on the way to death he turns to speak "
         "to them. Every step is chosen love. He asks his disciples to take up their "
         "cross daily and follow him. Patience is not resignation but the strength to "
         "keep walking with Christ, carrying what is ours and helping others with theirs.",
         "Jesus, help me carry my cross patiently, and help others carry theirs."),
        # 5. The Crucifixion and Death of Jesus - Perseverance
        ("Lifted up between two criminals, Jesus prays for those who crucify him, "
         "promises paradise to a repentant thief, and gives his mother to the beloved "
         "disciple, and through him to us. Mary stands by the cross, uniting her sorrow "
         "to his offering. Then, having accomplished everything, he gives up his spirit. "
         "The cross is the throne of his love and the altar of the one perfect sacrifice; "
         "from his pierced side flow blood and water, the sacraments of the Church. "
         "Perseverance is faithfulness to the end, sustained by the love that held him "
         "there.",
         "Lord Jesus, by your cross, keep me faithful to you to the end of my life."),
    ],
    'glorious': [
        # 1. The Resurrection - Faith
        ("Early on the first day of the week the women come to the tomb with spices and "
         "find the stone rolled back. The angel asks why they seek the living among the "
         "dead: he is not here, he has risen. Jesus does not simply return to his former "
         "life; he passes through death into glory, the first fruits of a new creation. "
         "His rising confirms all he taught and shows that the Father has accepted his "
         "sacrifice. Death no longer has the last word. Faith is to stake our lives on the "
         "empty tomb and the living Christ.",
         "Risen Lord, strengthen my faith, and raise me with you to new life."),
        # 2. The Ascension - Hope
        ("Forty days after rising, Jesus leads his disciples out, blesses them and is "
         "taken up into heaven. He has not left us; he has gone ahead. Our human nature, "
         "which he took from Mary, now sits at the right hand of the Father, and where "
         "the Head has gone the Body hopes to follow. He promised to prepare a place for "
         "us, sent his Church to make disciples of all nations, and assured us that he is "
         "with us always, to the end of the age. Hope is the confident longing for heaven "
         "that makes us faithful to our mission on earth.",
         "Lord, lift my heart to where you are, and keep me faithful to the work you give "
         "me."),
        # 3. The Descent of the Holy Spirit - Love of God
        ("Gathered in prayer with Mary, the apostles wait as Jesus told them. At Pentecost "
         "a sound like a mighty wind fills the house, and tongues as of fire rest on each "
         "of them. The Holy Spirit, the love of the Father and the Son, is poured into "
         "their hearts, and frightened men become fearless witnesses, speaking so that "
         "every nation hears in its own language. The confusion of Babel is undone, and "
         "the Church is born. The love of God is not first our love for him, but his love "
         "given to us in the Spirit, so that we can love him in return.",
         "Come, Holy Spirit, fill my heart and kindle in me the fire of your love."),
        # 4. The Assumption of Mary - Grace of a happy death
        ("At the end of her earthly life, Mary is taken up body and soul into heavenly "
         "glory. She who was kept free from all sin by a singular grace is not left to the "
         "corruption of the grave; the ark that carried the Lord rises to his resting "
         "place. Her Assumption is the first full share in her Son’s resurrection and "
         "the promise of ours: what God has done for her he wills for all who belong to "
         "Christ. A happy death, like hers, is a passing into the arms of God, and so we "
         "ask her to pray for us now and at the hour of our death.",
         "Mary, taken up into heaven, pray for me now and at the hour of my death."),
        # 5. The Coronation of Mary - Trust in Mary's intercession
        ("Christ, the King of the universe, crowns his mother Queen of heaven and earth. "
         "In Israel the queen was the king’s mother, seated at his right hand to plead "
         "for the people, as Bathsheba sat beside Solomon. Mary’s queenship is one of "
         "service and intercession: the woman clothed with the sun is still the mother "
         "who notices that we have no wine. All her glory comes from her Son and leads "
         "back to him. To trust her intercession is to know that the mother of the King "
         "is our mother too, and that her Son refuses her nothing that is good for us.",
         "Hail, holy Queen, Mother of mercy, pray for us and lead us to Jesus."),
    ],
}


# In the manner of St Louis de Montfort (The Secret of the Rosary): before each
# decade, offer it to Jesus in honour of the mystery and ask, through Mary's
# prayers, for the mystery's fruit.  Written fresh for this site.
_ASK = 'Through this mystery, and through the prayers of your holy Mother, we ask of you '


def _offer(nth, honour, ask):
    return 'We offer you, Lord Jesus, this %s decade in honour of %s. %s%s. Amen.' % (nth, honour, _ASK, ask)


OFFERINGS = {
    'joyful': [
        _offer('first', 'your Incarnation, when at the angel\u2019s greeting you, the eternal Word, '
               'were made flesh in the womb of the Virgin Mary', 'a deep humility of heart'),
        _offer('second', 'the Visitation of your holy Mother to her cousin Elizabeth, when you made '
               'John the Baptist leap for joy before his birth', 'a true love of our neighbour'),
        _offer('third', 'your Nativity in the stable at Bethlehem, where you were born poor and laid '
               'in a manger', 'poverty of spirit and freedom from the things of this world'),
        _offer('fourth', 'your Presentation in the Temple, when Mary and Joseph offered you to the '
               'Father in obedience to the Law', 'a ready obedience to the will of God'),
        _offer('fifth', 'your Finding in the Temple among the teachers, after Mary and Joseph had '
               'searched for you for three days in sorrow', 'the grace to seek you always, and the '
               'joy of finding you'),
    ],
    'luminous': [
        _offer('first', 'your Baptism in the Jordan, when the Holy Spirit came down upon you and the '
               'Father declared you his beloved Son', 'an openness to the Holy Spirit, who was given '
               'to us in our own baptism'),
        _offer('second', 'your first sign at the wedding at Cana, when at your Mother\u2019s word you '
               'changed water into wine', 'the grace to come to you through Mary, and to do whatever '
               'you tell us'),
        _offer('third', 'your proclamation of the Kingdom of God and your call to repentance',
               'true conversion of heart and a childlike trust in our Father'),
        _offer('fourth', 'your Transfiguration on the holy mountain, when your glory shone before '
               'Peter, James and John', 'a deep desire for holiness, and ears to listen to you'),
        _offer('fifth', 'your institution of the Holy Eucharist at the Last Supper, when you gave us '
               'your body and blood', 'a living faith in your presence and a spirit of adoration'),
    ],
    'sorrowful': [
        _offer('first', 'your agony in the Garden of Gethsemane, when you accepted the Father\u2019s '
               'will in anguish and prayer', 'true sorrow for our sins'),
        _offer('second', 'your cruel scourging at the pillar', 'purity of body and soul'),
        _offer('third', 'your crowning with thorns, when you were mocked as a king',
               'courage to stand by you when you are scorned'),
        _offer('fourth', 'your carrying of the cross to Calvary', 'patience in carrying our own '
               'crosses, and kindness in helping others with theirs'),
        _offer('fifth', 'your crucifixion and death on Calvary, with your Mother standing by the '
               'cross', 'perseverance in your grace to the end of our lives'),
    ],
    'glorious': [
        _offer('first', 'your glorious Resurrection from the dead', 'a living faith'),
        _offer('second', 'your Ascension into heaven, where you have gone to prepare a place for us',
               'a firm hope and a longing for heaven'),
        _offer('third', 'the coming of the Holy Spirit upon your apostles and your holy Mother at '
               'Pentecost', 'the fire of the Holy Spirit and a burning love of God'),
        _offer('fourth', 'the Assumption of your holy Mother, body and soul, into heaven',
               'the grace of a happy death'),
        _offer('fifth', 'the crowning of your holy Mother as Queen of heaven and earth',
               'a childlike trust in her motherly care and prayers'),
    ],
}

assert all(len(v) == 5 for v in MEDITATIONS.values()), 'five meditations per set'
assert all(len(v) == 5 for v in OFFERINGS.values()), 'five offerings per set'


# Modern reflections: plain, everyday English, connecting each mystery to
# ordinary life, with a question to think about.  Written fresh for this site.
MODERN = {
    'joyful': [
        ("Mary\u2019s life changed in a single conversation. She had plans, like anyone, and then God "
         "asked for everything. She didn\u2019t have the full picture. She asked an honest question, "
         "\u201cHow can this be?\u201d, and then said yes anyway. Humility isn\u2019t putting yourself down; "
         "it\u2019s being honest about who you are and letting God be bigger than your plans. Most of "
         "God\u2019s invitations don\u2019t come with angels. They come in ordinary moments: a need we "
         "notice, a quiet nudge to do the right thing.",
         "Where might God be asking for my yes today?"),
        ("As soon as Mary hears that her older cousin is pregnant, she sets off on a long, tiring "
         "journey to help. She doesn\u2019t wait to be asked, and she doesn\u2019t make it about herself, "
         "even though her own news is enormous. When they meet, both women are filled with joy. Love "
         "of neighbour often looks like turning up: sending the message, giving the lift, sitting "
         "with someone who\u2019s struggling. Carrying Jesus means taking him to the people around us.",
         "Who needs me to turn up for them this week?"),
        ("God arrives not in a palace but in a shed, born to a young couple far from home with "
         "nowhere to stay. The first visitors are shepherds, people others looked down on. We are "
         "surrounded by messages that we need more: more things, more followers, more success. "
         "Poverty of spirit means knowing that what matters most can\u2019t be bought, and making room "
         "for God and for the people who get left out.",
         "What could I let go of to make more room for what really matters?"),
        ("Mary and Joseph do what faithful families did: they bring their baby to the Temple and give "
         "him to God. An old man, Simeon, who has waited his whole life, recognises Jesus straight "
         "away, and warns Mary that love will cost her. Obedience can sound like just following "
         "rules, but at heart it\u2019s trust: believing God\u2019s way is good even when it\u2019s hard, "
         "and keeping our promises when we\u2019d rather not.",
         "Where is God asking me to trust him and keep going?"),
        ("For three days Mary and Joseph search for their missing twelve-year-old, sick with worry. "
         "When they find him, he is in the Temple, calmly listening and asking questions. Even Mary "
         "doesn\u2019t fully understand. Everyone has times when God feels far away or life doesn\u2019t "
         "make sense. Keep looking. Jesus is found in prayer, in the Church and in honest questions, "
         "and the joy of finding him again is real.",
         "Where do I go looking for Jesus when he feels far away?"),
    ],
    'luminous': [
        ("Jesus lines up at the river with ordinary people who knew they needed a fresh start. He "
         "didn\u2019t need to, but he chose to stand with us. Then the sky opens and the Father says: "
         "this is my beloved Son. At our baptism those words were spoken over us too. Before we "
         "achieve anything, we are loved. Being open to the Holy Spirit means living from that truth "
         "rather than trying to earn it.",
         "What would change if I really believed I am God\u2019s beloved?"),
        ("A wedding is about to turn into an embarrassment: the wine has run out. Mary notices, tells "
         "Jesus, and then tells the servants, \u201cDo whatever he tells you.\u201d Jesus turns water into "
         "the best wine of the night. Mary still notices what we need and points us to her Son. Her "
         "advice is as simple, and as hard, as ever: listen to Jesus, and do what he says.",
         "What is Jesus asking me to do that I\u2019ve been putting off?"),
        ("Jesus\u2019 first message is short: the Kingdom of God is close, so turn around and trust the "
         "good news. He shows what that Kingdom looks like by spending time with outsiders, healing "
         "the sick and forgiving people everyone else had written off. Repentance isn\u2019t about "
         "feeling miserable; it\u2019s about changing direction. God isn\u2019t waiting to catch us out but "
         "to welcome us home.",
         "Where do I need to turn around and start again?"),
        ("Jesus takes three friends up a mountain, and for a moment they see him as he really is, "
         "shining with God\u2019s glory. Peter wants to stay there for ever, but they have to come back "
         "down to ordinary life and, soon, to the cross. We all have mountain-top moments: a retreat, "
         "a beautiful Mass, a time when God felt close. They are given to keep us going in the "
         "valleys. Holiness grows as we listen to Jesus every day.",
         "When have I glimpsed God\u2019s glory, and how can I hold on to it?"),
        ("At his last meal with his friends, Jesus washes their feet like a servant, then gives them "
         "bread and wine: his body and blood. He knows what the next day will bring, and he chooses "
         "to give himself completely. At every Mass that same gift is offered to us. Adoration is "
         "simply noticing how much we are loved and answering with thanks, then going out to serve "
         "as he did.",
         "How can I receive Jesus in the Eucharist with more attention and thanks?"),
    ],
    'sorrowful': [
        ("In the garden Jesus is overwhelmed. He knows what is coming, and he asks his Father if "
         "there is any other way. He doesn\u2019t hide his fear, yet he chooses to trust: not my will, "
         "but yours. Meanwhile his friends fall asleep. Sorrow for sin starts when we see that the "
         "things we do wrong really hurt others and God. And Jesus shows us that we can bring our "
         "fear to God honestly.",
         "What am I afraid of that I need to hand over to God?"),
        ("Jesus is beaten by soldiers while a crowd watches, and he doesn\u2019t hit back. His body, "
         "which God made good, is treated as worthless. We live in a world that often judges bodies, "
         "our own and other people\u2019s, by how they look, or uses people for what they can give. "
         "Purity means seeing every person, including ourselves, as precious and worth respecting, "
         "because Jesus thought we were worth his suffering.",
         "How do I show respect for my own body and for other people?"),
        ("The soldiers make a joke of Jesus: a cloak, a crown of thorns, mock bows. He is humiliated, "
         "laughed at and alone. Many people know what it\u2019s like to be mocked, online or in person. "
         "Jesus stays silent, not because he is weak but because he refuses to answer cruelty with "
         "cruelty. Courage sometimes means standing up for someone who is being picked on, and "
         "sometimes it means not passing on the joke.",
         "When have I laughed along when I should have stood up?"),
        ("Exhausted and bleeding, Jesus carries his cross through the streets. A stranger, Simon, is "
         "pulled out of the crowd to help him. Women weep for him, and he still finds the strength to "
         "speak to them. Everyone carries something heavy: illness, worry, grief, trouble at home. "
         "Patience isn\u2019t pretending things are fine; it\u2019s keeping going one step at a time, "
         "letting others help us, and helping them in turn.",
         "Whose cross could I help to carry right now?"),
        ("On the cross, in terrible pain, Jesus forgives the people killing him, promises paradise to "
         "a criminal who asks for mercy, and makes sure his mother will be cared for. Then he gives "
         "up his life. This is what love looks like when it goes all the way. Perseverance means not "
         "giving up on faith, or on people, when it gets hard, because Jesus never gave up on us.",
         "Who do I need to forgive, or keep loving, even when it\u2019s hard?"),
    ],
    'glorious': [
        ("Early on Sunday morning the women come to the tomb expecting to grieve, and find it empty. "
         "Jesus is alive! Death, failure and sin don\u2019t get the final say. Faith isn\u2019t pretending "
         "everything is fine; it\u2019s trusting that God can bring new life out of the worst "
         "situations, including ours. The same Jesus who rose that morning walks with us now.",
         "Where in my life do I need to trust that God can bring new life?"),
        ("Jesus returns to his Father, but he doesn\u2019t leave his friends empty-handed. He gives them "
         "a mission, to share the good news everywhere, and a promise: \u201cI am with you always.\u201d "
         "It\u2019s easy to stand staring at the sky, or at our screens, and wait for something to "
         "happen. Hope means knowing where we are headed, and getting on with the job in the "
         "meantime.",
         "What part of Jesus\u2019 mission can I carry out this week?"),
        ("The disciples are hiding behind locked doors when the Holy Spirit comes like wind and fire. "
         "Suddenly these frightened people are out in the streets, speaking so that everyone "
         "understands. The same Spirit was given to us in baptism and confirmation. The love of God "
         "isn\u2019t something we have to manufacture; it\u2019s God\u2019s own love poured into our hearts, "
         "ready to overflow.",
         "Where do I need the Holy Spirit\u2019s courage?"),
        ("At the end of her life Mary is taken, body and soul, into heaven, where Jesus has gone "
         "before her. It shows what God has planned for all of us: not just our souls but our whole "
         "selves, made new. Death is real and can be frightening, but for those who belong to Jesus "
         "it is a doorway, not a dead end. That is why we ask Mary to pray for us \u201cat the hour of "
         "our death\u201d.",
         "How does the hope of heaven change the way I live now?"),
        ("Mary is honoured as Queen of heaven and earth, but she is a queen who still acts like a "
         "mother: she notices, cares and prays for her children. Everything she has points back to "
         "Jesus. When we are struggling we can ask her to pray for us, as we would ask a friend, "
         "knowing that she brings our needs to her Son.",
         "What do I want to ask Mary to pray for today?"),
    ],
}

assert all(len(v) == 5 for v in MODERN.values()), 'five modern reflections per set'


# Meditations on the virtue (the fruit of each mystery): what it is, how the
# mystery shows it, and how to practise it.  Written fresh for this site.
VIRTUES = {
    'joyful': [
        ("Humility is the truth about ourselves before God: everything we have is gift. It is not "
         "thinking little of ourselves but thinking of ourselves less, and of God more. Mary shows it "
         "at the Annunciation: greeted as full of grace, she calls herself the Lord\u2019s servant and "
         "makes room for his will. Humility is the ground of every other virtue, because only an open "
         "hand can receive. We practise it by giving thanks, admitting our faults, accepting "
         "correction and letting others go first.",
         "Lord, make me humble of heart, so that I may receive all you wish to give."),
        ("Love of neighbour is charity turned outward: wanting the good of another and acting on it. "
         "Jesus joins it to the love of God as the greatest commandment, and asks us to see him in the "
         "least of our brothers and sisters. At the Visitation Mary goes in haste to serve, without "
         "fuss or reward. Love of neighbour is practical: it notices, serves and forgives, and it "
         "begins with the people nearest to us, at home, at school and at work.",
         "Lord, teach me to love my neighbour as you have loved me."),
        ("Poverty of spirit is the first beatitude: knowing that we depend on God for everything, and "
         "setting our hearts on him rather than on possessions, status or comfort. It frees us to be "
         "generous and content. In the stable at Bethlehem the Son of God chooses to have nothing, so "
         "that we might have him. We grow in it by living simply, sharing what we have, resisting the "
         "urge always to want more, and trusting God with tomorrow.",
         "Jesus, free my heart from every attachment, and be my treasure."),
        ("Obedience comes from a word meaning to listen. It is hearing God\u2019s will and doing it, "
         "freely and with love, through his commandments, the Church, our conscience and those rightly "
         "placed over us. At the Presentation, Mary and Joseph keep the Law, and Jesus, the Lawgiver "
         "himself, submits to it. True obedience is not fear but trust that God\u2019s way leads to "
         "life. We practise it by doing our duties well, keeping our promises, and saying yes to God "
         "in small things.",
         "Father, give me a listening heart, quick to do your will."),
        ("Christian joy is not mere cheerfulness; it is the delight of being with the One we love. It "
         "can live alongside sorrow, because it rests on Christ, not on circumstances. Mary and "
         "Joseph\u2019s anguished search ends in the joy of finding Jesus in his Father\u2019s house. We "
         "too lose him and find him again and again. We seek him in prayer, in the Scriptures and in "
         "the sacraments, above all the Eucharist and Reconciliation, and we share our joy with "
         "others.",
         "Lord Jesus, when I find you, let my joy be full and lasting."),
    ],
    'luminous': [
        ("Openness to the Holy Spirit is the readiness to let God lead: to listen for his promptings "
         "and follow where he guides. The Spirit given in baptism and confirmation brings the gifts of "
         "wisdom, understanding, counsel, fortitude, knowledge, piety and fear of the Lord. At the "
         "Jordan the Spirit rests on Jesus, and from there he is led into his mission. We grow in "
         "openness through silence and prayer, and a willingness to change our plans when God asks.",
         "Come, Holy Spirit; make me attentive to your voice and ready to follow."),
        ("Going to Jesus through Mary means trusting her as a mother who always leads us to her Son. "
         "She never keeps our attention for herself. At Cana she notices the need, brings it to Jesus, "
         "and tells the servants to do whatever he says. Devotion to Mary is real when it makes us "
         "more like Christ. We practise it by praying the Rosary, entrusting our needs to her, and "
         "imitating her faith, purity and readiness to serve.",
         "Mary, my Mother, lead me always to your Son."),
        ("Repentance, or conversion, is turning the whole heart back to God; trust is resting in his "
         "mercy rather than in ourselves. The two belong together: we can only face our sins honestly "
         "when we are sure of being forgiven. Jesus begins his preaching with this call, and shows the "
         "Father\u2019s mercy to sinners. We grow in it by examining our conscience, going to Confession, "
         "making amends, and beginning again each day without discouragement.",
         "Lord, turn my heart to you, and teach me to trust your mercy."),
        ("Holiness is not for a few; it is the call of every baptised person: to share God\u2019s own "
         "life and become more like Christ. The desire for holiness is the longing that keeps us "
         "growing. On the mountain the disciples glimpse the glory to which we are all called. We "
         "nourish this desire by daily prayer and the sacraments, by reading the lives of the saints, "
         "and by doing ordinary things with great love.",
         "Lord, set my heart on fire with longing to be holy."),
        ("Adoration is the first act of the virtue of religion: acknowledging God as God, our Creator "
         "and Saviour, and giving him praise, thanks and love. In the Eucharist Jesus gives himself to "
         "us, truly present, body and blood, soul and divinity, and adoration answers with wonder and "
         "gratitude. We practise it by genuflecting with care, receiving Communion reverently, keeping "
         "silence before God, and spending time with him before the tabernacle.",
         "My Lord and my God, I adore you, present in the Most Holy Sacrament."),
    ],
    'sorrowful': [
        ("Sorrow for sin, or contrition, is grief at having offended God, with the resolve not to sin "
         "again. It is perfect when it comes from love of God, and imperfect when it comes from fear of "
         "sin\u2019s consequences; both lead us back to him. In Gethsemane Jesus feels the weight of "
         "every sin, including ours. True sorrow is not despair but hope, because it turns towards the "
         "Father\u2019s mercy. We practise it in a nightly examination of conscience and in regular "
         "Confession.",
         "Lord, give me true sorrow for my sins and the grace to amend my life."),
        ("Purity, or chastity, is the virtue that orders our love and desires, so that we see others "
         "as persons to be loved, never as objects to be used. It respects the body as a temple of the "
         "Holy Spirit. In the scourging, Christ\u2019s body is torn to heal the wounds of sin, including "
         "sins against purity. We grow in purity by guarding what we look at and watch, choosing good "
         "friends, praying for help, and going to Confession when we fall.",
         "Jesus, give me a pure heart, and help me to see others as you see them."),
        ("Courage, the virtue of fortitude, gives firmness in difficulty and steadiness in doing good, "
         "even in the face of fear, mockery or loss. It is not the absence of fear but the choice to do "
         "what is right anyway. Crowned with thorns and mocked, Jesus endures in silence and dignity. "
         "We practise courage by speaking the truth with kindness, standing up for those who are "
         "picked on, owning our faith, and keeping going when it is hard.",
         "Lord, strengthen me to stand for what is right, whatever the cost."),
        ("Patience is the strength to bear difficulties, delays and other people\u2019s faults without "
         "bitterness or giving up. It is love that waits. Jesus carries the cross step by step, falls "
         "and rises, and accepts help along the way. Patience grows when we accept what we cannot "
         "change, offer our sufferings with his, pause before reacting, and are gentle with others "
         "and with ourselves.",
         "Jesus, teach me to carry my cross patiently, and to be patient with others."),
        ("Perseverance is faithfulness to the end: continuing in grace and goodness through every "
         "trial, until death. It is a gift we ask for daily, because no one perseveres by willpower "
         "alone. On the cross Jesus completes his mission and gives himself to the last. We grow in "
         "perseverance by staying faithful to daily prayer, coming back to God at once when we fall, "
         "and asking Mary to pray for us at the hour of our death.",
         "Lord, keep me faithful to you all the days of my life."),
    ],
    'glorious': [
        ("Faith is the theological virtue by which we believe in God and all that he has revealed, "
         "because he is truth itself. It is both a gift and our free response: trusting God with our "
         "whole lives. The Resurrection is the foundation of our faith; Christ has truly risen. Faith "
         "grows when we pray, read the Scriptures, learn what the Church teaches, ask honest "
         "questions, and act on what we believe.",
         "Lord, I believe; help my unbelief."),
        ("Hope is the theological virtue by which we desire heaven and eternal life as our happiness, "
         "trusting in Christ\u2019s promises and the help of the Holy Spirit, not in our own strength. It "
         "guards us from both despair and presumption. In the Ascension our human nature enters "
         "heaven with Christ, a sign of where we are going. We practise hope by keeping heaven in "
         "view, persevering in difficulty, and bringing hope to others.",
         "Lord, fill me with hope in your promises."),
        ("Charity, the greatest of the theological virtues, is love of God above all things for his "
         "own sake, and love of our neighbour for love of him. It gives life to every other virtue. At "
         "Pentecost the Holy Spirit pours God\u2019s love into the hearts of the apostles. We grow in "
         "the love of God through prayer and worship, by keeping his commandments, and by loving those "
         "around us, for everyone who loves is born of God.",
         "My God, I love you above all things; make my love grow."),
        ("A happy death is dying in God\u2019s friendship, at peace and ready to meet him. It is the "
         "greatest grace of all, because it seals a whole life. Mary, taken up into heaven, shows the "
         "destiny God wills for us. We prepare for a happy death by living each day in grace, going "
         "to Confession often, receiving the Anointing of the Sick when seriously ill, and asking Mary "
         "in every Hail Mary to pray for us at the hour of our death.",
         "Jesus, Mary and Joseph, be with me at the hour of my death."),
        ("Trust in Mary\u2019s intercession is confidence that the Mother of God, crowned in heaven, "
         "prays for us with a mother\u2019s love. Her prayer adds nothing to Christ\u2019s power but shares "
         "in it, and she always leads us to him. As Queen and Mother she still notices what we lack. "
         "We practise this trust by turning to her in every need, praying the Rosary, entrusting "
         "ourselves to her care, and imitating her faith.",
         "Holy Mary, Mother of God, pray for us sinners, now and at the hour of our death."),
    ],
}

# Intentions: who and what each decade is offered for, with a short
# reflection linking the intention to the mystery.  Written fresh for this site.
INTENTIONS = {
    'joyful': [
        ("For expectant mothers, unborn children, and all who are discerning God\u2019s call.",
         "Mary welcomed the Son of God and said yes to her vocation. We pray for mothers awaiting "
         "their children, for the protection of every unborn life, and for young people listening for "
         "what God is asking of them.",
         "Lord, bless every new life, and give us generous hearts to answer your call."),
        ("For families, and for all who care for the elderly, the sick and the lonely.",
         "Mary hurried to help her older cousin. We pray for our families and friendships, for carers, "
         "nurses and volunteers, and for the lonely, that someone will visit them as Mary visited "
         "Elizabeth.",
         "Lord, make us quick to visit and serve those who need us."),
        ("For the poor, the homeless, refugees and all who are far from home.",
         "Jesus was born where there was no room at the inn. We pray for the homeless and the poor, "
         "for refugees and migrants, and for all who have nowhere to belong, and for generous hearts "
         "to welcome them.",
         "Jesus, born poor, open our hearts and our homes to those in need."),
        ("For parents and children, and for the elderly who wait in faith.",
         "Mary and Joseph offered their child to God, and Simeon and Anna had waited a lifetime to see "
         "him. We pray for parents raising their children in faith, for godparents and grandparents, "
         "and for the elderly, that their faithfulness may be honoured.",
         "Lord, bless our families, young and old, and keep them in your love."),
        ("For students and teachers, and for those who have lost their way or their faith.",
         "Jesus was found among the teachers, listening and asking questions. We pray for students "
         "and teachers and our school communities, and for anyone who has drifted from God, that they "
         "will search for Jesus and find him again.",
         "Lord, guide all who learn and teach, and bring the lost back home."),
    ],
    'luminous': [
        ("For the newly baptised, those preparing to enter the Church, and their godparents.",
         "At the Jordan the Father called Jesus his beloved Son. We pray for those being baptised and "
         "confirmed, for adults preparing to join the Church, and for parents and godparents, that "
         "all may live as God\u2019s beloved children.",
         "Holy Spirit, renew in all of us the grace of our baptism."),
        ("For married couples, and for those preparing for marriage.",
         "Jesus worked his first sign at a wedding, at his mother\u2019s request. We pray for husbands "
         "and wives, for couples preparing to marry, for marriages under strain, and for all who are "
         "grieving the loss of a husband or wife.",
         "Lord, bless marriages with your love, and fill whatever is lacking."),
        ("For sinners, for those who proclaim the Gospel, and for peace and justice.",
         "Jesus proclaimed God\u2019s Kingdom, forgave sinners and lifted up the poor. We pray for all who "
         "need conversion, beginning with ourselves, for missionaries, priests and catechists, and for "
         "all who work for peace and justice in our world.",
         "Lord, may your Kingdom come in our hearts and in our world."),
        ("For those who are suffering or discouraged, and for growth in holiness.",
         "Jesus showed his glory to strengthen his friends before the cross. We pray for anyone going "
         "through a dark time, for those struggling with illness, anxiety or depression, and for the "
         "grace to grow in holiness ourselves.",
         "Lord, let your light shine on all who walk in darkness."),
        ("For priests, for vocations, and for reverence for the Eucharist.",
         "At the Last Supper Jesus gave us his body and blood, and the priesthood to make him present. "
         "We pray for our priests, for vocations to the priesthood and religious life, and for those "
         "who no longer come to Mass.",
         "Lord, send labourers into your harvest, and draw all people to your table."),
    ],
    'sorrowful': [
        ("For those who are anxious, afraid or facing hard decisions.",
         "In the garden Jesus faced fear and anguish, and he prayed. We pray for all who are anxious "
         "or afraid, for anyone facing a difficult decision, for those struggling with temptation, and "
         "for those tempted to lose hope.",
         "Lord, give strength and peace to all who are in anguish."),
        ("For victims of violence and abuse, and for an end to cruelty.",
         "Jesus was beaten and treated with contempt. We pray for victims of violence, abuse and "
         "bullying, for the healing of their wounds in body and spirit, and for a change of heart in "
         "those who cause harm.",
         "Jesus, heal the wounded and bring an end to cruelty."),
        ("For all who are mocked, bullied or left out, and for those who lead.",
         "Jesus was mocked as a king. We pray for everyone who is ridiculed, bullied or excluded, "
         "online or in person, and for those in authority, that they will lead with humility and "
         "serve the common good.",
         "Christ our King, protect the humiliated and guide our leaders."),
        ("For the sick, for carers, and for all who carry heavy burdens.",
         "Simon of Cyrene helped Jesus carry his cross. We pray for the sick and those living with "
         "pain or disability, for carers and health workers, and for all weighed down by grief, worry "
         "or hardship.",
         "Jesus, help all who carry heavy crosses, and make us their Simon."),
        ("For the dying, for those who mourn, and for the grace to forgive.",
         "On the cross Jesus forgave his enemies, promised paradise to a thief, and entrusted his "
         "mother to John. We pray for the dying, for all who grieve, for the gift of forgiveness, and "
         "for the souls of the faithful departed.",
         "Lord, have mercy on the dying, comfort those who mourn, and grant eternal rest to the dead."),
    ],
    'glorious': [
        ("For the faithful departed, and for all who need new hope.",
         "Christ is risen, and death does not have the last word. We pray for those who have died, "
         "especially our own family and friends, and for anyone who has lost hope, that the risen "
         "Lord will meet them.",
         "Risen Lord, grant eternal life to the dead and new hope to the living."),
        ("For the mission of the Church, and for persecuted Christians.",
         "Before ascending, Jesus sent his disciples to all the nations. We pray for the Church\u2019s "
         "mission and for missionaries, for Christians who suffer for their faith, and for ourselves, "
         "that we will share our faith with courage and joy.",
         "Lord, make us faithful witnesses to you wherever we go."),
        ("For the Church, for unity among Christians, and for the gifts of the Holy Spirit.",
         "The Holy Spirit came upon the apostles and Mary, and the Church was born. We pray for the "
         "Pope and the bishops, for unity among all Christians, for those being confirmed, and for "
         "the gifts of the Spirit in our own lives.",
         "Come, Holy Spirit, and renew the face of the earth."),
        ("For the elderly and the dying, and for the grace of a holy death.",
         "Mary was taken body and soul into heaven. We pray for the elderly and those near the end of "
         "their lives, for those who care for them, and for the grace of a holy death for ourselves "
         "and those we love.",
         "Holy Mary, pray for us now and at the hour of our death."),
        ("For our own intentions, entrusted to Mary.",
         "Mary, Queen of heaven, is still the mother who notices our needs. In this decade we bring "
         "her our own intentions: the people we love, the worries we carry and the hopes we hold, "
         "knowing she will bring them to her Son.",
         "Mary, Queen and Mother, receive our intentions and present them to Jesus."),
    ],
}

assert all(len(v) == 5 for v in VIRTUES.values()), 'five virtue meditations per set'
assert all(len(v) == 5 for v in INTENTIONS.values()), 'five intentions per set'
