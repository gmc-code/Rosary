"""The twenty mysteries of the Rosary.

Each mystery has a title, a fruit (the grace traditionally prayed for) and ten
scripture references, one for each Hail Mary of the decade.  The short caption
beside each reference is a plain summary of the passage, not a quotation.

References use the chapter and verse numbering of the NRSV / NRSV-CE (the
default Bible on BibleGateway links).  A few books (Micah 5, Psalms) are
numbered one verse differently in some Catholic editions such as the NABRE.
"""

ORDINALS = ('First', 'Second', 'Third', 'Fourth', 'Fifth')

DAY_NAMES = ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday',
             'Friday', 'Saturday')

# order shown on the tabs: the order of the four sets in the life of Christ
SET_ORDER = ('joyful', 'luminous', 'sorrowful', 'glorious')

SETS = {
    'joyful': {
        'name': 'Joyful',
        'days': (1, 6),     # Monday, Saturday (0 = Sunday)
        'mysteries': [
            {
                'title': 'The Annunciation',
                'fruit': 'Humility',
                'refs': [
                    ('Isaiah 7:14', 'The Lord himself will give a sign: a young woman will bear a son, Emmanuel'),
                    ('Luke 1:26-27', 'The angel Gabriel is sent to a virgin named Mary in Nazareth'),
                    ('Luke 1:28', 'Gabriel greets Mary as full of grace: the Lord is with her'),
                    ('Luke 1:29-30', 'Mary is troubled, but the angel tells her not to be afraid'),
                    ('Luke 1:31', 'She will conceive and bear a son and name him Jesus'),
                    ('Luke 1:32-33', 'He will be called Son of the Most High and his kingdom will never end'),
                    ('Luke 1:34-35', 'Mary asks how; the Holy Spirit will come upon her'),
                    ('Luke 1:36-37', 'Elizabeth has conceived; nothing is impossible with God'),
                    ('Luke 1:38', 'Mary answers: here am I, the servant of the Lord'),
                    ('John 1:14', 'The Word became flesh and lived among us'),
                ],
            },
            {
                'title': 'The Visitation',
                'fruit': 'Love of neighbour',
                'refs': [
                    ('Luke 1:39-40', 'Mary sets out in haste to the hill country to visit Elizabeth'),
                    ('Luke 1:41', 'The child leaps in Elizabeth\'s womb and she is filled with the Holy Spirit'),
                    ('Luke 1:42', 'Elizabeth calls Mary blessed among women, and blessed is the fruit of her womb'),
                    ('Luke 1:43', 'Why has the mother of my Lord come to me?'),
                    ('Luke 1:44', 'The child in her womb leapt for joy at Mary\'s greeting'),
                    ('Luke 1:45', 'Blessed is she who believed the Lord\'s promise'),
                    ('Luke 1:46-48', 'Mary\'s song: her soul proclaims the greatness of the Lord'),
                    ('Luke 1:49-50', 'The Mighty One has done great things; his mercy lasts for ever'),
                    ('Luke 1:51-53', 'He scatters the proud, lifts up the lowly and fills the hungry'),
                    ('Luke 1:56', 'Mary stays with Elizabeth about three months'),
                ],
            },
            {
                'title': 'The Nativity',
                'fruit': 'Poverty of spirit',
                'refs': [
                    ('Micah 5:2', 'From little Bethlehem will come a ruler for Israel'),
                    ('Luke 2:1-3', 'Emperor Augustus orders a census of the whole world'),
                    ('Luke 2:4-5', 'Joseph goes with Mary to Bethlehem, the city of David'),
                    ('Luke 2:6-7', 'Mary gives birth and lays her son in a manger: no room at the inn'),
                    ('Luke 2:8-9', 'An angel appears to shepherds keeping watch at night'),
                    ('Luke 2:10-11', 'Good news of great joy: a Saviour is born, the Messiah, the Lord'),
                    ('Luke 2:12', 'The sign: a child wrapped in bands of cloth, lying in a manger'),
                    ('Luke 2:13-14', 'The heavenly host sings: glory to God and peace on earth'),
                    ('Luke 2:15-16', 'The shepherds hurry and find Mary, Joseph and the child'),
                    ('Matthew 2:10-11', 'The magi see the star, worship the child and offer gold, frankincense and myrrh'),
                ],
            },
            {
                'title': 'The Presentation in the Temple',
                'fruit': 'Obedience',
                'refs': [
                    ('Luke 2:22', 'Mary and Joseph bring Jesus to Jerusalem to present him to the Lord'),
                    ('Luke 2:23', 'Every firstborn male is to be consecrated to the Lord'),
                    ('Luke 2:24', 'They offer a pair of turtledoves or two young pigeons'),
                    ('Luke 2:25', 'Simeon, righteous and devout, waits for the consolation of Israel'),
                    ('Luke 2:26-27', 'The Spirit had promised Simeon he would see the Messiah'),
                    ('Luke 2:28-30', 'Simeon takes the child in his arms: now let your servant go in peace'),
                    ('Luke 2:31-32', 'A light for revelation to the Gentiles and glory for Israel'),
                    ('Luke 2:34', 'This child is destined for the falling and rising of many'),
                    ('Luke 2:35', 'A sword will pierce Mary\'s own soul too'),
                    ('Luke 2:36-38', 'The prophet Anna praises God and speaks about the child'),
                ],
            },
            {
                'title': 'The Finding of Jesus in the Temple',
                'fruit': 'Joy in finding Jesus',
                'refs': [
                    ('Luke 2:41-42', 'Each year the family goes to Jerusalem for Passover; Jesus is twelve'),
                    ('Luke 2:43', 'The boy Jesus stays behind without his parents knowing'),
                    ('Luke 2:44-45', 'They search among relatives, then return to Jerusalem'),
                    ('Luke 2:46', 'After three days they find him in the temple among the teachers'),
                    ('Luke 2:47', 'All who hear him are amazed at his understanding'),
                    ('Luke 2:48', 'Mary says: your father and I have been searching for you in great anxiety'),
                    ('Luke 2:49', 'Did you not know I must be in my Father\'s house?'),
                    ('Luke 2:50', 'They do not understand what he says to them'),
                    ('Luke 2:51', 'He goes home obedient to them; Mary treasures all these things'),
                    ('Luke 2:52', 'Jesus grows in wisdom and in years, and in favour with God and people'),
                ],
            },
        ],
    },
    'luminous': {
        'name': 'Luminous',
        'days': (4,),       # Thursday
        'mysteries': [
            {
                'title': 'The Baptism of Jesus in the Jordan',
                'fruit': 'Openness to the Holy Spirit',
                'refs': [
                    ('Matthew 3:1-2', 'John the Baptist preaches in the wilderness: repent'),
                    ('Matthew 3:5-6', 'People from all Judea are baptised by John in the Jordan'),
                    ('Mark 1:7', 'One more powerful than John is coming after him'),
                    ('Matthew 3:11', 'He will baptise with the Holy Spirit and fire'),
                    ('John 1:29', 'John sees Jesus coming: here is the Lamb of God'),
                    ('Matthew 3:13-14', 'Jesus comes to be baptised; John feels unworthy'),
                    ('Matthew 3:15', 'Jesus says it is right to fulfil all righteousness'),
                    ('Matthew 3:16', 'The heavens open and the Spirit descends like a dove'),
                    ('Matthew 3:17', 'A voice from heaven: this is my Son, the Beloved'),
                    ('John 1:32-34', 'John testifies that Jesus is the Son of God'),
                ],
            },
            {
                'title': 'The Wedding at Cana',
                'fruit': 'To Jesus through Mary',
                'refs': [
                    ('John 2:1-2', 'There is a wedding at Cana; Mary, Jesus and his disciples are there'),
                    ('John 2:3', 'The wine runs out and Mary tells Jesus: they have no wine'),
                    ('John 2:4', 'Jesus answers that his hour has not yet come'),
                    ('John 2:5', 'Mary tells the servants: do whatever he tells you'),
                    ('John 2:6', 'Six stone water jars stand there for purification'),
                    ('John 2:7', 'Jesus says fill the jars with water; they fill them to the brim'),
                    ('John 2:8', 'Draw some out and take it to the chief steward'),
                    ('John 2:9', 'The steward tastes the water that has become wine'),
                    ('John 2:10', 'You have kept the good wine until now'),
                    ('John 2:11', 'The first of his signs: his disciples believe in him'),
                ],
            },
            {
                'title': 'The Proclamation of the Kingdom',
                'fruit': 'Repentance and trust in God',
                'refs': [
                    ('Mark 1:14-15', 'The kingdom of God has come near: repent and believe the good news'),
                    ('Luke 4:18-19', 'The Spirit of the Lord sends Jesus to bring good news to the poor'),
                    ('Matthew 5:3', 'Blessed are the poor in spirit: theirs is the kingdom of heaven'),
                    ('Matthew 5:7-9', 'Blessed are the merciful, the pure in heart and the peacemakers'),
                    ('Matthew 5:14-16', 'You are the light of the world: let your light shine'),
                    ('Matthew 6:9-10', 'Jesus teaches the Our Father: your kingdom come'),
                    ('Matthew 6:33', 'Strive first for the kingdom of God'),
                    ('Mark 2:5', 'Jesus tells the paralysed man: your sins are forgiven'),
                    ('Luke 7:47-48', 'Her many sins are forgiven, for she has shown great love'),
                    ('Matthew 10:7-8', 'Jesus sends the twelve to proclaim the kingdom and heal'),
                ],
            },
            {
                'title': 'The Transfiguration',
                'fruit': 'Desire for holiness',
                'refs': [
                    ('Matthew 17:1', 'Jesus takes Peter, James and John up a high mountain'),
                    ('Luke 9:28-29', 'While he is praying, the appearance of his face changes'),
                    ('Matthew 17:2', 'His face shines like the sun; his clothes become dazzling white'),
                    ('Matthew 17:3', 'Moses and Elijah appear, talking with him'),
                    ('Luke 9:30-31', 'They speak of his departure, which he will accomplish in Jerusalem'),
                    ('Matthew 17:4', 'Peter says: Lord, it is good for us to be here'),
                    ('Matthew 17:5', 'A bright cloud and a voice: this is my Son, listen to him'),
                    ('Matthew 17:6-7', 'The disciples fall down in fear; Jesus touches them: do not be afraid'),
                    ('Matthew 17:8', 'Looking up, they see no one but Jesus himself alone'),
                    ('2 Peter 1:16-18', 'Peter recalls being an eyewitness of his majesty on the holy mountain'),
                ],
            },
            {
                'title': 'The Institution of the Eucharist',
                'fruit': 'Adoration',
                'refs': [
                    ('John 13:1', 'Having loved his own, Jesus loves them to the end'),
                    ('Luke 22:14-15', 'Jesus has eagerly desired to eat this Passover with them'),
                    ('John 13:14-15', 'He washes their feet and gives them an example'),
                    ('Matthew 26:26', 'He takes bread, blesses and breaks it: this is my body'),
                    ('Luke 22:19', 'Do this in remembrance of me'),
                    ('Matthew 26:27-28', 'The cup of his blood of the covenant, poured out for forgiveness'),
                    ('John 6:35', 'I am the bread of life'),
                    ('John 6:51', 'I am the living bread that came down from heaven'),
                    ('John 6:54-56', 'Whoever eats my flesh and drinks my blood abides in me'),
                    ('1 Corinthians 11:26', 'We proclaim the Lord\'s death until he comes'),
                ],
            },
        ],
    },
    'sorrowful': {
        'name': 'Sorrowful',
        'days': (2, 5),     # Tuesday, Friday
        'mysteries': [
            {
                'title': 'The Agony in the Garden',
                'fruit': 'Sorrow for sin',
                'refs': [
                    ('Matthew 26:36', 'Jesus goes with his disciples to Gethsemane to pray'),
                    ('Matthew 26:37-38', 'His soul is deeply grieved; he asks them to stay awake with him'),
                    ('Matthew 26:39', 'Let this cup pass from me; yet not what I want, but what you want'),
                    ('Luke 22:43', 'An angel from heaven appears and gives him strength'),
                    ('Luke 22:44', 'In his anguish his sweat becomes like great drops of blood'),
                    ('Matthew 26:40-41', 'Could you not stay awake one hour? The spirit is willing, the flesh weak'),
                    ('Matthew 26:42', 'He prays again: your will be done'),
                    ('Matthew 26:45-46', 'The hour is at hand: get up, let us be going'),
                    ('Matthew 26:47-49', 'Judas arrives with a crowd and betrays him with a kiss'),
                    ('Matthew 26:56', 'All the disciples desert him and flee'),
                ],
            },
            {
                'title': 'The Scourging at the Pillar',
                'fruit': 'Purity',
                'refs': [
                    ('Mark 15:1', 'Jesus is bound and handed over to Pilate'),
                    ('John 18:33', 'Pilate asks him: are you the King of the Jews?'),
                    ('John 18:36', 'My kingdom is not from this world'),
                    ('John 18:37-38', 'Jesus came to testify to the truth; Pilate asks what truth is'),
                    ('Matthew 27:15-17', 'Pilate offers to release Barabbas or Jesus'),
                    ('Matthew 27:22-23', 'The crowd shouts: let him be crucified'),
                    ('Mark 15:15', 'To satisfy the crowd, Pilate has Jesus flogged'),
                    ('Isaiah 50:6', 'The servant gives his back to those who strike him'),
                    ('Isaiah 53:5', 'He was wounded for our sins; by his bruises we are healed'),
                    ('Isaiah 53:7', 'Like a lamb led to the slaughter, he does not open his mouth'),
                ],
            },
            {
                'title': 'The Crowning with Thorns',
                'fruit': 'Courage',
                'refs': [
                    ('Matthew 27:27', 'The soldiers gather the whole cohort around Jesus'),
                    ('Matthew 27:28', 'They strip him and put a scarlet robe on him'),
                    ('Matthew 27:29', 'They twist a crown of thorns, put a reed in his hand and mock him as king'),
                    ('Matthew 27:30', 'They spit on him and strike him on the head'),
                    ('John 19:4-5', 'Pilate brings him out wearing the crown: here is the man'),
                    ('John 19:6', 'The chief priests shout: crucify him'),
                    ('John 19:10-11', 'Pilate would have no power unless it were given from above'),
                    ('John 19:14-15', 'Here is your King; they answer that they have no king but Caesar'),
                    ('Matthew 27:24', 'Pilate washes his hands before the crowd'),
                    ('Matthew 27:26', 'He hands Jesus over to be crucified'),
                ],
            },
            {
                'title': 'The Carrying of the Cross',
                'fruit': 'Patience',
                'refs': [
                    ('John 19:16-17', 'Carrying the cross by himself, Jesus goes out to the Place of the Skull'),
                    ('Isaiah 53:4', 'Surely he has borne our infirmities and carried our diseases'),
                    ('Mark 15:21', 'Simon of Cyrene is made to carry the cross'),
                    ('Luke 23:27', 'A great crowd follows, including women mourning for him'),
                    ('Luke 23:28', 'Daughters of Jerusalem, do not weep for me'),
                    ('Luke 23:31', 'If they do this when the wood is green, what will happen when it is dry?'),
                    ('Luke 23:32', 'Two criminals are led away to be put to death with him'),
                    ('Matthew 16:24', 'Whoever wants to follow me must take up their cross'),
                    ('1 Peter 2:21', 'Christ suffered for you, leaving an example to follow in his steps'),
                    ('Hebrews 12:2', 'For the joy set before him he endured the cross'),
                ],
            },
            {
                'title': 'The Crucifixion and Death of Jesus',
                'fruit': 'Perseverance',
                'refs': [
                    ('Luke 23:33', 'At the Skull they crucify Jesus between two criminals'),
                    ('Luke 23:34', 'Father, forgive them, for they do not know what they are doing'),
                    ('Luke 23:42-43', 'Today you will be with me in Paradise'),
                    ('John 19:25', 'Standing near the cross is his mother'),
                    ('John 19:26-27', 'Woman, here is your son; here is your mother'),
                    ('Mark 15:33', 'Darkness comes over the whole land until three in the afternoon'),
                    ('Mark 15:34', 'My God, my God, why have you forsaken me?'),
                    ('John 19:28-30', 'I am thirsty ... It is finished'),
                    ('Luke 23:46', 'Father, into your hands I commend my spirit'),
                    ('Mark 15:39', 'The centurion says: truly this man was God\'s Son'),
                ],
            },
        ],
    },
    'glorious': {
        'name': 'Glorious',
        'days': (0, 3),     # Sunday, Wednesday
        'mysteries': [
            {
                'title': 'The Resurrection',
                'fruit': 'Faith',
                'refs': [
                    ('Mark 16:1-2', 'At sunrise the women bring spices to the tomb'),
                    ('Mark 16:3-4', 'They wonder who will roll away the stone; it is already rolled back'),
                    ('Matthew 28:5-6', 'The angel says: do not be afraid; he is not here, he has been raised'),
                    ('Luke 24:5-6', 'Why do you look for the living among the dead?'),
                    ('John 20:6-8', 'Peter and the other disciple see the linen wrappings and believe'),
                    ('John 20:15-16', 'Jesus calls Mary Magdalene by name and she knows him'),
                    ('Luke 24:30-31', 'At Emmaus he is known to them in the breaking of the bread'),
                    ('John 20:27-28', 'Thomas touches his wounds: my Lord and my God'),
                    ('John 20:29', 'Blessed are those who have not seen and yet have come to believe'),
                    ('1 Corinthians 15:20', 'Christ has been raised, the first fruits of those who have died'),
                ],
            },
            {
                'title': 'The Ascension',
                'fruit': 'Hope',
                'refs': [
                    ('John 14:2-3', 'I go to prepare a place for you'),
                    ('Matthew 28:18', 'All authority in heaven and on earth has been given to me'),
                    ('Matthew 28:19', 'Go and make disciples of all nations, baptising them'),
                    ('Matthew 28:20', 'I am with you always, to the end of the age'),
                    ('Mark 16:15-16', 'Proclaim the good news to the whole creation'),
                    ('Acts 1:8', 'You will receive power and be my witnesses to the ends of the earth'),
                    ('Luke 24:50-51', 'He blesses them and is carried up into heaven'),
                    ('Acts 1:9', 'He is lifted up and a cloud takes him out of their sight'),
                    ('Acts 1:10-11', 'Two men in white ask why they stand looking up towards heaven'),
                    ('Luke 24:52-53', 'They return to Jerusalem with great joy, blessing God'),
                ],
            },
            {
                'title': 'The Descent of the Holy Spirit',
                'fruit': 'Love of God',
                'refs': [
                    ('John 14:16-17', 'The Father will give another Advocate, the Spirit of truth'),
                    ('John 14:26', 'The Holy Spirit will teach you everything'),
                    ('Acts 1:14', 'They devote themselves to prayer, together with Mary the mother of Jesus'),
                    ('Acts 2:1', 'On the day of Pentecost they are all together in one place'),
                    ('Acts 2:2', 'A sound like the rush of a violent wind fills the house'),
                    ('Acts 2:3', 'Divided tongues, as of fire, rest on each of them'),
                    ('Acts 2:4', 'All are filled with the Holy Spirit and speak in other languages'),
                    ('Acts 2:5-6', 'People from every nation each hear them in their own language'),
                    ('Acts 2:38', 'Repent and be baptised, and receive the gift of the Holy Spirit'),
                    ('Acts 2:41', 'About three thousand people are baptised that day'),
                ],
            },
            {
                'title': 'The Assumption of Mary',
                'fruit': 'Grace of a happy death',
                'refs': [
                    ('Genesis 3:15', 'God puts enmity between the serpent and the woman'),
                    ('Psalm 16:10', 'You do not let your faithful one see the Pit'),
                    ('Psalm 132:8', 'Rise up, O Lord, to your resting place, you and the ark of your might'),
                    ('Song of Solomon 2:10-11', 'Arise, my love, and come away; the winter is past'),
                    ('Luke 1:48', 'From now on all generations will call me blessed'),
                    ('Luke 1:49', 'The Mighty One has done great things for me'),
                    ('1 Corinthians 15:20-22', 'In Christ all will be made alive'),
                    ('1 Corinthians 15:23', 'Each in their own order: Christ, then those who belong to him'),
                    ('1 Corinthians 15:54-55', 'Death has been swallowed up in victory'),
                    ('Revelation 11:19', 'God\'s temple in heaven opens and the ark of his covenant is seen'),
                ],
            },
            {
                'title': 'The Coronation of Mary',
                'fruit': 'Trust in Mary\'s intercession',
                'refs': [
                    ('1 Kings 2:19', 'King Solomon has a throne brought for his mother at his right hand'),
                    ('Psalm 45:9', 'At your right hand stands the queen in gold of Ophir'),
                    ('Judith 13:18', 'Blessed are you by the Most High God above all women on earth'),
                    ('Judith 15:9', 'You are the glory of Jerusalem and the great boast of Israel'),
                    ('Revelation 12:1', 'A woman clothed with the sun, with a crown of twelve stars'),
                    ('2 Timothy 4:7-8', 'The crown of righteousness is reserved for those who keep the faith'),
                    ('James 1:12', 'Those who endure will receive the crown of life'),
                    ('1 Peter 5:4', 'You will win the crown of glory that never fades away'),
                    ('Revelation 2:10', 'Be faithful until death and I will give you the crown of life'),
                    ('Revelation 22:5', 'The servants of God will reign for ever and ever'),
                ],
            },
        ],
    },
}

# The traditional prayers of a decade (public domain wording).
PRAYERS = {
    'our-father': ('Our Father',
                   'Our Father, who art in heaven, hallowed be thy name; thy '
                   'kingdom come; thy will be done on earth as it is in heaven. '
                   'Give us this day our daily bread; and forgive us our '
                   'trespasses, as we forgive those who trespass against us; '
                   'and lead us not into temptation, but deliver us from evil. '
                   'Amen.'),
    'hail-mary': ('Hail Mary',
                  'Hail Mary, full of grace, the Lord is with thee; blessed art '
                  'thou among women, and blessed is the fruit of thy womb, '
                  'Jesus. Holy Mary, Mother of God, pray for us sinners, now '
                  'and at the hour of our death. Amen.'),
    'glory-be': ('Glory Be',
                 'Glory be to the Father, and to the Son, and to the Holy '
                 'Spirit. As it was in the beginning, is now, and ever shall '
                 'be, world without end. Amen.'),
    'fatima': ('O my Jesus',
               'O my Jesus, forgive us our sins, save us from the fires of '
               'hell, lead all souls to heaven, especially those in most need '
               'of thy mercy.'),
}


def _check():
    assert tuple(SETS) and set(SETS) == set(SET_ORDER)
    for key, data in SETS.items():
        assert len(data['mysteries']) == 5, key
        for m in data['mysteries']:
            assert len(m['refs']) == 10, (key, m['title'])


_check()
