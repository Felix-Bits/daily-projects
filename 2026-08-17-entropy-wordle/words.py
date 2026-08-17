"""A pure-stdlib word list of common 5-letter English words, used as both
the answer pool and the guess pool for the entropy-driven Wordle solver."""

WORDS = """
aback abide above abuse actor adapt admit adult agent agree ahead alarm
album alert alien alike alive allow alone along alter among angel anger
angle angry apart apple apply arena argue arise armor aside asset avoid
awake award aware badly baker based basic basis beach beard beast began
begin being below bench birth black blade blame blank blast blend bless
blind block blood board boast boost booth bound brain brand brave bread
break breed brick bride brief bring broad broke brown brush build built
burst cabin cable camel canal candy canoe cargo carry carve catch cause
chain chair chalk charm chart chase cheap check cheek cheer chess chest
chief child chill chimp choir chose civic claim class clean clear clerk
click cliff climb cling clock close cloth cloud clown coach coast could
count court cover craft crane crash crawl crazy cream creek crest crime
crisp cross crowd crown crude cruel crush curly curve cycle daily dance
dealt death debut decay delay delta dense depth diary dirty donor doubt
dozen draft drain drama drank drawn dread dream dress dried drift drill
drink drive drove drown drunk dying eager eagle early earth eight elbow
elder elect elite email embed empty enemy enjoy enter entry equal equip
error essay event every exact exile exist extra fable faced faith false
fancy fatal fault favor feast fence ferry fetch fever fiber field fifth
fifty fight final first fixed flame flash fleet flesh float flock flood
floor flour fluid flush focal focus folly force forge forth forty forum
found frame frank fraud fresh front frost frown fruit fully funny gauge
ghost giant given glass glory glove going grace grade grain grand grant
grape graph grasp grass grave gravy great greed green greet grief grill
grind groan groom gross group grove grown guard guess guest guide habit
happy harsh heart heavy hedge hello hence night ideal image imply index
inner input issue ivory joint judge juice jumbo known label labor laser
later laugh layer learn lease least leave legal level lever light limit
linen liver lobby local logic loose lower loyal lucky lunar lunch lying
magic major maker march match maybe mayor meant medal media metal meter
might minor minus mixed model moist molar moral motor mount mouse mouth
moved movie music naive nasty naval nerve never newly nicer noble noise
north notch novel nurse nylon occur ocean offer often olive onset opera
orbit order organ other ought ounce outer owner oxide panel panic paper
party patch pause peace peach pearl phase phone photo piano piece pilot
pitch pizza place plain plane plant plate point poker polar porch pound
power press price pride prime print prior prize proof proud prove pulse
punch pupil puppy purse queen query quick quiet quilt quote radar radio
raise rally ranch range rapid ratio reach react ready realm rebel refer
relax reply rider ridge rifle right rigid rival river roast robin robot
rocky rogue roman rough round route rowdy royal rugby ruler rural sadly
saint salad sauce scale scare scarf scene scent scope score scout scrap
screw seize sense serve seven shade shaft shake shall shame shape share
shark sharp shave shelf shell shift shine shiny shirt shock shoot shore
short shout shown sight silly since sixth sixty skill skirt skull slate
sleep slice slide slope small smart smell smile smoke snack solar solid
solve sonic sorry sound south space spare spark speak speed spell spend
spent spice spike spine split spoke sport spray squad staff stage stain
stake stamp stand stare start state steak steal steam steel steep steer
stern stick stiff still sting stock stone stood stool story stove strap
straw stray strip stuck study stuff style sugar suite super sweet swept
swift swing sword table taken taste teach tempo tenth terms thank theme
thick thief thing think third those throw thumb tiger tight timer tired
title toast today token topic torch total touch tough tower toxic trace
track trade trail train trait trash treat trend trial tribe trick tried
troop truck truly trunk trust truth tumor tunes twice twist ultra uncle
under union unity until upper upset urban usage usual vague valid value
valve vapor vault venue verse video virus visit vital vivid vocal voice
waste watch water weary weigh weird whale wheat wheel where which while
white whole whose widen wider width witty woman world worry worse worst
worth would wound woven wrist write wrong yield young youth zebra
""".split()

assert all(len(w) == 5 and w.isalpha() for w in WORDS)
