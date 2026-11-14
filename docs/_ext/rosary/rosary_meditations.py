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
