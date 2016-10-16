import xbmcaddon
__settings__ = xbmcaddon.Addon(id='plugin.video.imdbsearch')

from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcgui
import xbmcaddon
import sys
import os

import requests
import re
import urllib,urlparse
import HTMLParser
from trakt import Trakt

if sys.version_info >= (2, 7):
    from json import loads, dumps
else:
    from simplejson import loads, dumps

_url = sys.argv[0]
_handle = int(sys.argv[1])

if __settings__.getSetting('english') == 'true':
    headers={'Accept-Language' : 'en',"X-Forwarded-For": "8.8.8.8"}
else:
    headers={}

def log(x):
    xbmc.log(repr(x))

def get_background():
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'resources', 'img', "background.png")

def get_icon_path(icon_name):
    addon_path = xbmcaddon.Addon().getAddonInfo("path")
    return os.path.join(addon_path, 'resources', 'img', icon_name+".png")

def get_genre_icon(genre):
    icons = {
    "Any":"genre_any",
    "Action":"genre_action",
    "Adventure":"genre_adventure",
    "Animation":"genre_animation",
    "Biography":"genre_biography",
    "Comedy":"genre_comedy",
    "Crime":"genre_crime",
    "Documentary":"genre_documentary",
    "Drama":"genre_drama",
    "Family":"genre_family",
    "Fantasy":"genre_fantasy",
    "Film Noir":"genre_film_noir",
    "Game show":"genre_game_show",
    "History":"genre_history",
    "Horror":"genre_horror",
    "Music":"genre_music",
    "Musical":"genre_musical",
    "Mystery":"genre_mystery",
    "News":"genre_news",
    "Reality TV":"genre_reality_tv",
    "Romance":"genre_romance",
    "Sci-Fi":"genre_sci_fi",
    "Sport":"genre_sport",
    "Talk Show":"genre_talk_show",
    "Thriller":"genre_thriller",
    "War":"genre_war",
    "Western":"genre_western"
    }
    if genre in icons:
        return get_icon_path(icons[genre])
    return "DefaultVideo.png"

def get_server(server_select, reverse=False):
    server_dict = {"Original Title":"akas",
    "Normal":"www"}
    if reverse:
        return find_key(server_dict,server_select)
    else:
        return server_dict[server_select]

def get_sort(sort_select, reverse=False):
    sort_dict = {"Any":"Any",
    "Moviemeter,Asc":"moviemeter,asc",
    "Moviemeter,Desc":"moviemeter,desc",
    "Alpha,Asc":"alpha,asc",
    "Alpha,Desc":"alpha,desc",
    "User Rating,Asc":"user_rating,asc",
    "User Rating,Desc":"user_rating,desc",
    "Num Votes,Asc":"num_votes,asc",
    "Num Votes,Desc":"num_votes,desc",
    "Boxoffice Gross US,Asc":"boxoffice_gross_us,asc",
    "Boxoffice Gross US,Desc":"boxoffice_gross_us,desc",
    "Runtime,Asc":"runtime,asc",
    "Runtime,Desc":"runtime,desc",
    "Year,Asc":"year,asc",
    "Year,Desc":"year,desc",
    "Release Date US,Asc":"release_date_us,asc",
    "Release Date US,Desc":"release_date_us,desc",
    "My Ratings":"my_ratings",
    "My Ratings,Asc":"my_ratings,asc"}
    if reverse:
        return find_key(sort_dict,sort_select)
    else:
        return sort_dict[sort_select]

def get_colors(colors_select, reverse=False):
    colors_dict = {"Any":"Any",
    "Color":"color",
    "Black and White":"black_and_white",
    "Colorized":"colorized",
    "ACES":"aces"}
    if reverse:
        return find_key(colors_dict,colors_select)
    else:
        return colors_dict[colors_select]

def get_certificates(certificates_select, reverse=False):
    certificates_dict = {"Any":"Any",
    "US:G":"us:g",
    "US:PG":"us:pg",
    "US:PG_13":"us:pg_13",
    "US:R":"us:r",
    "US:NC_17":"us:nc_17",
    "GB:U"  :"gb:u"  ,
    "GB:PG" :"gb:pg" ,
    "GB:12" :"gb:12" ,
    "GB:12A":"gb:12a",
    "GB:15" :"gb:15" ,
    "GB:18" :"gb:18" ,
    "GB:R18":"gb:r18",
    }
    if reverse:
        return find_key(certificates_dict,certificates_select)
    else:
        return certificates_dict[certificates_select]

def get_companies(companies_select, reverse=False):
    companies_dict = {"Any":"Any",
    "Fox":"fox",
    "Columbia":"columbia",
    "Dreamworks":"dreamworks",
    "MGM":"mgm",
    "Paramount":"paramount",
    "Universal":"universal",
    "Disney":"disney",
    "Warner":"warner"}
    if reverse:
        return find_key(companies_dict,companies_select)
    else:
        return companies_dict[companies_select]

def get_production_status(production_status_select, reverse=False):
    production_status_dict = {"Any":"*",
    "Released":"released",
    "Post Production":"post production",
    "Filming":"filming",
    "Pre Production":"pre production",
    "Completed":"completed",
    "Script":"script",
    "Optioned Property":"optioned property",
    "Announced":"announced",
    "Treatment Outline":"treatment outline",
    "Pitch":"pitch",
    "Turnaround":"turnaround",
    "Abandoned":"abandoned",
    "Delayed":"delayed",
    "Indefinitely Delayed":"indefinitely delayed",
    "Active":"active",
    "Unknown":"unknown"}
    if reverse:
        return find_key(production_status_dict,production_status_select)
    else:
        return production_status_dict[production_status_select]

def get_groups(groups_select, reverse=False):
    groups_dict = {"Any":"*",
    "Top 100":"top_100",
    "Top 250":"top_250",
    "Top 1000":"top_1000",
    "Now Playing Us":"now-playing-us",
    "Oscar Winners":"oscar_winners",
    "Oscar Best Picture Winners":"oscar_best_picture_winners",
    "Oscar Best Director Winners":"oscar_best_director_winners",
    "Oscar Nominees":"oscar_nominees",
    "Emmy Winners":"emmy_winners",
    "Emmy Nominees":"emmy_nominees",
    "Golden Globe Winners":"golden_globe_winners",
    "Golden Globe Nominees":"golden_globe_nominees",
    "Razzie Winners":"razzie_winners",
    "Razzie Nominees":"razzie_nominees",
    "National Film Registry":"national_film_registry",
    "Bottom 100":"bottom_100",
    "Bottom 250":"bottom_250",
    "Bottom 1000":"bottom_1000"}
    if reverse:
        return find_key(groups_dict,groups_select)
    else:
        return groups_dict[groups_select]

def get_genre(genres_select, reverse=False):
    genres_dict = {"Any":"Any",
    "None":"",
    "Action":"action",
    "Adventure":"adventure",
    "Animation":"animation",
    "Biography":"biography",
    "Comedy":"comedy",
    "Crime":"crime",
    "Documentary":"documentary",
    "Drama":"drama",
    "Family":"family",
    "Fantasy":"fantasy",
    "Film Noir":"film_noir",
    "Game show":"game_show",
    "History":"history",
    "Horror":"horror",
    "Music":"music",
    "Musical":"musical",
    "Mystery":"mystery",
    "News":"news",
    "Reality TV":"reality_tv",
    "Romance":"romance",
    "Sci-Fi":"sci_fi",
    "Sport":"sport",
    "Talk Show":"talk_show",
    "Thriller":"thriller",
    "War":"war",
    "Western":"western"}
    if reverse:
        return find_key(genres_dict,genres_select)
    else:
        return genres_dict[genres_select]

def find_key(dict,value):
    for k,v in dict.iteritems():
        if v == value:
            return k
    return ''

def get_title_type(title_type_select, reverse=False):
    title_type_dict = {'Feature':'feature',
    'TV Movie':'tv_movie',
    'TV Series':'tv_series',
    'TV Episode':'tv_episode',
    'TV Special':'tv_special',
    'Mini Series':'mini_series',
    'Documentary':'documentary',
    'Game':'game',
    'Short':'short',
    'Video':'video'}
    if reverse:
        return find_key(title_type_dict,title_type_select)
    else:
        return title_type_dict[title_type_select]

def get_languages(languages_select, reverse=False):
    languages_dict = {"Any":"*",
    "Arabic":"ar",
    "Bulgarian":"bg",
    "Chinese":"zh",
    "Croatian":"hr",
    "Dutch":"nl",
    "English":"en",
    "Finnish":"fi",
    "French":"fr",
    "German":"de",
    "Greek":"el",
    "Hebrew":"he",
    "Hindi":"hi",
    "Hungarian":"hu",
    "Icelandic":"is",
    "Italian":"it",
    "Japanese":"ja",
    "Korean":"ko",
    "Norwegian":"no",
    "Persian":"fa",
    "Polish":"pl",
    "Portuguese":"pt",
    "Punjabi":"pa",
    "Romanian":"ro",
    "Russian":"ru",
    "Spanish":"es",
    "Swedish":"sv",
    "Turkish":"tr",
    "Ukrainian":"uk",
    "Abkhazian":"ab",
    "Aboriginal":"qac",
    "Ach&#xE9;":"guq",
    "Acholi":"qam",
    "Afrikaans":"af",
    "Aidoukrou":"qas",
    "Akan":"ak",
    "Albanian":"sq",
    "Algonquin":"alg",
    "American Sign Language":"ase",
    "Amharic":"am",
    "Apache languages":"apa",
    "Aragonese":"an",
    "Aramaic":"arc",
    "Arapaho":"arp",
    "Armenian":"hy",
    "Assamese":"as",
    "Assyrian Neo-Aramaic":"aii",
    "Athapascan languages":"ath",
    "Australian Sign Language":"asf",
    "Awadhi":"awa",
    "Aymara":"ay",
    "Azerbaijani":"az",
    "Bable":"ast",
    "Baka":"qbd",
    "Balinese":"ban",
    "Bambara":"bm",
    "Basque":"eu",
    "Bassari":"bsc",
    "Belarusian":"be",
    "Bemba":"bem",
    "Bengali":"bn",
    "Berber languages":"ber",
    "Bhojpuri":"bho",
    "Bicolano":"qbi",
    "Bodo":"qbh",
    "Bosnian":"bs",
    "Brazilian Sign Language":"bzs",
    "Breton":"br",
    "British Sign Language":"bfi",
    "Burmese":"my",
    "Cantonese":"yue",
    "Catalan":"ca",
    "Central Khmer":"km",
    "Chaozhou":"qax",
    "Chechen":"ce",
    "Cherokee":"chr",
    "Cheyenne":"chy",
    "Chhattisgarhi":"hne",
    "Cornish":"kw",
    "Corsican":"co",
    "Cree":"cr",
    "Creek":"mus",
    "Creole":"qal",
    "Creoles and pidgins":"crp",
    "Crow":"cro",
    "Czech":"cs",
    "Danish":"da",
    "Dari":"prs",
    "Desiya":"dso",
    "Dinka":"din",
    "Djerma":"qaw",
    "Dogri":"doi",
    "Dyula":"dyu",
    "Dzongkha":"dz",
    "East-Greenlandic":"qbc",
    "Eastern Frisian":"frs",
    "Egyptian (Ancient)":"egy",
    "Esperanto":"eo",
    "Estonian":"et",
    "Ewe":"ee",
    "Faliasch":"qbg",
    "Faroese":"fo",
    "Filipino":"fil",
    "Flemish":"qbn",
    "Fon":"fon",
    "French Sign Language":"fsl",
    "Fulah":"ff",
    "Fur":"fvr",
    "Gaelic":"gd",
    "Galician":"gl",
    "Georgian":"ka",
    "German Sign Language":"gsg",
    "Grebo":"grb",
    "Greek, Ancient (to 1453)":"grc",
    "Greenlandic":"kl",
    "Guarani":"gn",
    "Gujarati":"gu",
    "Gumatj":"gnn",
    "Gunwinggu":"gup",
    "Haitian":"ht",
    "Hakka":"hak",
    "Haryanvi":"bgc",
    "Hassanya":"qav",
    "Hausa":"ha",
    "Hawaiian":"haw",
    "Hmong":"hmn",
    "Hokkien":"qab",
    "Hopi":"hop",
    "Iban":"iba",
    "Ibo":"qag",
    "Icelandic Sign Language":"icl",
    "Indian Sign Language":"ins",
    "Indonesian":"id",
    "Inuktitut":"iu",
    "Inupiaq":"ik",
    "Irish Gaelic":"ga",
    "Japanese Sign Language":"jsl",
    "Jola-Fonyi":"dyo",
    "Ju&#x27;hoan":"ktz",
    "Kaado":"qbf",
    "Kabuverdianu":"kea",
    "Kabyle":"kab",
    "Kalmyk-Oirat":"xal",
    "Kannada":"kn",
    "Karaj&#xE1;":"kpj",
    "Karbi":"mjw",
    "Karen":"kar",
    "Kazakh":"kk",
    "Khanty":"kca",
    "Khasi":"kha",
    "Kikuyu":"ki",
    "Kinyarwanda":"rw",
    "Kirundi":"qar",
    "Klingon":"tlh",
    "Kodava":"kfa",
    "Konkani":"kok",
    "Korean Sign Language":"kvk",
    "Korowai":"khe",
    "Kriolu":"qaq",
    "Kru":"kro",
    "Kudmali":"kyw",
    "Kuna":"qbb",
    "Kurdish":"ku",
    "Kwakiutl":"kwk",
    "Kyrgyz":"ky",
    "Ladakhi":"lbj",
    "Ladino":"lad",
    "Lao":"lo",
    "Latin":"la",
    "Latvian":"lv",
    "Limbu":"lif",
    "Lingala":"ln",
    "Lithuanian":"lt",
    "Low German":"nds",
    "Luxembourgish":"lb",
    "Macedonian":"mk",
    "Macro-J&#xEA;":"qbm",
    "Magahi":"mag",
    "Maithili":"mai",
    "Malagasy":"mg",
    "Malay":"ms",
    "Malayalam":"ml",
    "Malecite-Passamaquoddy":"pqm",
    "Malinka":"qap",
    "Maltese":"mt",
    "Manchu":"mnc",
    "Mandarin":"cmn",
    "Mandingo":"man",
    "Manipuri":"mni",
    "Maori":"mi",
    "Mapudungun":"arn",
    "Marathi":"mr",
    "Marshallese":"mh",
    "Masai":"mas",
    "Masalit":"mls",
    "Maya":"myn",
    "Mende":"men",
    "Micmac":"mic",
    "Middle English":"enm",
    "Min Nan":"nan",
    "Minangkabau":"min",
    "Mirandese":"mwl",
    "Mizo":"lus",
    "Mohawk":"moh",
    "Mongolian":"mn",
    "Montagnais":"moe",
    "More":"qaf",
    "Morisyen":"mfe",
    "Nagpuri":"qbl",
    "Nahuatl":"nah",
    "Nama":"qba",
    "Navajo":"nv",
    "Naxi":"nbf",
    "Ndebele":"nd",
    "Neapolitan":"nap",
    "Nenets":"yrk",
    "Nepali":"ne",
    "Nisga&#x27;a":"ncg",
    "None":"zxx",
    "Norse, Old":"non",
    "North American Indian":"nai",
    "Nushi":"qbk",
    "Nyaneka":"nyk",
    "Nyanja":"ny",
    "Occitan":"oc",
    "Ojibwa":"oj",
    "Ojihimba":"qaz",
    "Old English":"ang",
    "Oriya":"or",
    "Papiamento":"pap",
    "Parsee":"qaj",
    "Pashtu":"ps",
    "Pawnee":"paw",
    "Peul":"qai",
    "Polynesian":"qah",
    "Pular":"fuf",
    "Purepecha":"tsz",
    "Quechua":"qu",
    "Quenya":"qya",
    "Rajasthani":"raj",
    "Rawan":"qbj",
    "Romansh":"rm",
    "Romany":"rom",
    "Rotuman":"rtm",
    "Russian Sign Language":"rsl",
    "Ryukyuan":"qao",
    "Saami":"qae",
    "Samoan":"sm",
    "Sanskrit":"sa",
    "Sardinian":"sc",
    "Scanian":"qay",
    "Serbian":"sr",
    "Serbo-Croatian":"qbo",
    "Serer":"srr",
    "Shanghainese":"qad",
    "Shanxi":"qau",
    "Shona":"sn",
    "Shoshoni":"shh",
    "Sicilian":"scn",
    "Sindarin":"sjn",
    "Sindhi":"sd",
    "Sinhala":"si",
    "Sioux":"sio",
    "Slovak":"sk",
    "Slovenian":"sl",
    "Somali":"so",
    "Songhay":"son",
    "Soninke":"snk",
    "Sorbian languages":"wen",
    "Sotho":"st",
    "Sousson":"qbe",
    "Spanish Sign Language":"ssp",
    "Sranan":"srn",
    "Swahili":"sw",
    "Swiss German":"gsw",
    "Sylheti":"syl",
    "Tagalog":"tl",
    "Tajik":"tg",
    "Tamashek":"tmh",
    "Tamil":"ta",
    "Tarahumara":"tac",
    "Tatar":"tt",
    "Telugu":"te",
    "Teochew":"qak",
    "Thai":"th",
    "Tibetan":"bo",
    "Tigrigna":"qan",
    "Tlingit":"tli",
    "Tok Pisin":"tpi",
    "Tonga (Tonga Islands)":"to",
    "Tsonga":"ts",
    "Tswa":"tsc",
    "Tswana":"tn",
    "Tulu":"tcy",
    "Tupi":"tup",
    "Turkmen":"tk",
    "Tuvinian":"tyv",
    "Tzotzil":"tzo",
    "Ungwatsi":"qat",
    "Urdu":"ur",
    "Uzbek":"uz",
    "Vietnamese":"vi",
    "Visayan":"qaa",
    "Washoe":"was",
    "Welsh":"cy",
    "Wolof":"wo",
    "Xhosa":"xh",
    "Yakut":"sah",
    "Yapese":"yap",
    "Yiddish":"yi",
    "Yoruba":"yo",
    "Zulu":"zu"}
    if reverse:
        return find_key(languages_dict,languages_select)
    else:
        return languages_dict[languages_select]

def get_countries(countries_select, reverse=False):
    countries_dict = {"Any":"*",
    "Argentina":"ar",
    "Australia":"au",
    "Austria":"at",
    "Belgium":"be",
    "Brazil":"br",
    "Bulgaria":"bg",
    "Canada":"ca",
    "China":"cn",
    "Colombia":"co",
    "Costa Rica":"cr",
    "Czech Republic":"cz",
    "Denmark":"dk",
    "Finland":"fi",
    "France":"fr",
    "Germany":"de",
    "Greece":"gr",
    "Hong Kong":"hk",
    "Hungary":"hu",
    "Iceland":"is",
    "India":"in",
    "Iran":"ir",
    "Ireland":"ie",
    "Italy":"it",
    "Japan":"jp",
    "Malaysia":"my",
    "Mexico":"mx",
    "Netherlands":"nl",
    "New Zealand":"nz",
    "Pakistan":"pk",
    "Poland":"pl",
    "Portugal":"pt",
    "Romania":"ro",
    "Russia":"ru",
    "Singapore":"sg",
    "South Africa":"za",
    "Spain":"es",
    "Sweden":"se",
    "Switzerland":"ch",
    "Thailand":"th",
    "United Kingdom":"gb",
    "United States":"us",
    "Afghanistan":"af",
    "&#xC5;land Islands":"ax",
    "Albania":"al",
    "Algeria":"dz",
    "American Samoa":"as",
    "Andorra":"ad",
    "Angola":"ao",
    "Anguilla":"ai",
    "Antarctica":"aq",
    "Antigua and Barbuda":"ag",
    "Armenia":"am",
    "Aruba":"aw",
    "Azerbaijan":"az",
    "Bahamas":"bs",
    "Bahrain":"bh",
    "Bangladesh":"bd",
    "Barbados":"bb",
    "Belarus":"by",
    "Belize":"bz",
    "Benin":"bj",
    "Bermuda":"bm",
    "Bhutan":"bt",
    "Bolivia":"bo",
    "Bonaire, Sint Eustatius and Saba":"bq",
    "Bosnia and Herzegovina":"ba",
    "Botswana":"bw",
    "Bouvet Island":"bv",
    "British Indian Ocean Territory":"io",
    "British Virgin Islands":"vg",
    "Brunei Darussalam":"bn",
    "Burkina Faso":"bf",
    "Burma":"bumm",
    "Burundi":"bi",
    "Cambodia":"kh",
    "Cameroon":"cm",
    "Cape Verde":"cv",
    "Cayman Islands":"ky",
    "Central African Republic":"cf",
    "Chad":"td",
    "Chile":"cl",
    "Christmas Island":"cx",
    "Cocos (Keeling) Islands":"cc",
    "Comoros":"km",
    "Congo":"cg",
    "Cook Islands":"ck",
    "C&#xF4;te d&#x27;Ivoire":"ci",
    "Croatia":"hr",
    "Cuba":"cu",
    "Cyprus":"cy",
    "Czechoslovakia":"cshh",
    "Democratic Republic of the Congo":"cd",
    "Djibouti":"dj",
    "Dominica":"dm",
    "Dominican Republic":"do",
    "East Germany":"ddde",
    "Ecuador":"ec",
    "Egypt":"eg",
    "El Salvador":"sv",
    "Equatorial Guinea":"gq",
    "Eritrea":"er",
    "Estonia":"ee",
    "Ethiopia":"et",
    "Falkland Islands":"fk",
    "Faroe Islands":"fo",
    "Federal Republic of Yugoslavia":"yucs",
    "Federated States of Micronesia":"fm",
    "Fiji":"fj",
    "French Guiana":"gf",
    "French Polynesia":"pf",
    "French Southern Territories":"tf",
    "Gabon":"ga",
    "Gambia":"gm",
    "Georgia":"ge",
    "Ghana":"gh",
    "Gibraltar":"gi",
    "Greenland":"gl",
    "Grenada":"gd",
    "Guadeloupe":"gp",
    "Guam":"gu",
    "Guatemala":"gt",
    "Guernsey":"gg",
    "Guinea":"gn",
    "Guinea-Bissau":"gw",
    "Guyana":"gy",
    "Haiti":"ht",
    "Heard Island and McDonald Islands":"hm",
    "Holy See (Vatican City State)":"va",
    "Honduras":"hn",
    "Indonesia":"id",
    "Iraq":"iq",
    "Isle of Man":"im",
    "Israel":"il",
    "Jamaica":"jm",
    "Jersey":"je",
    "Jordan":"jo",
    "Kazakhstan":"kz",
    "Kenya":"ke",
    "Kiribati":"ki",
    "Korea":"xko",
    "Kosovo":"xkv",
    "Kuwait":"kw",
    "Kyrgyzstan":"kg",
    "Laos":"la",
    "Latvia":"lv",
    "Lebanon":"lb",
    "Lesotho":"ls",
    "Liberia":"lr",
    "Libya":"ly",
    "Liechtenstein":"li",
    "Lithuania":"lt",
    "Luxembourg":"lu",
    "Macao":"mo",
    "Madagascar":"mg",
    "Malawi":"mw",
    "Maldives":"mv",
    "Mali":"ml",
    "Malta":"mt",
    "Marshall Islands":"mh",
    "Martinique":"mq",
    "Mauritania":"mr",
    "Mauritius":"mu",
    "Mayotte":"yt",
    "Moldova":"md",
    "Monaco":"mc",
    "Mongolia":"mn",
    "Montenegro":"me",
    "Montserrat":"ms",
    "Morocco":"ma",
    "Mozambique":"mz",
    "Myanmar":"mm",
    "Namibia":"na",
    "Nauru":"nr",
    "Nepal":"np",
    "Netherlands Antilles":"an",
    "New Caledonia":"nc",
    "Nicaragua":"ni",
    "Niger":"ne",
    "Nigeria":"ng",
    "Niue":"nu",
    "Norfolk Island":"nf",
    "North Korea":"kp",
    "North Vietnam":"vdvn",
    "Northern Mariana Islands":"mp",
    "Norway":"no",
    "Oman":"om",
    "Palau":"pw",
    "Palestine":"xpi",
    "Palestinian Territory":"ps",
    "Panama":"pa",
    "Papua New Guinea":"pg",
    "Paraguay":"py",
    "Peru":"pe",
    "Philippines":"ph",
    "Pitcairn":"pn",
    "Puerto Rico":"pr",
    "Qatar":"qa",
    "Republic of Macedonia":"mk",
    "R&#xE9;union":"re",
    "Rwanda":"rw",
    "Saint Barth&#xE9;lemy":"bl",
    "Saint Helena":"sh",
    "Saint Kitts and Nevis":"kn",
    "Saint Lucia":"lc",
    "Saint Martin (French part)":"mf",
    "Saint Pierre and Miquelon":"pm",
    "Saint Vincent and the Grenadines":"vc",
    "Samoa":"ws",
    "San Marino":"sm",
    "Sao Tome and Principe":"st",
    "Saudi Arabia":"sa",
    "Senegal":"sn",
    "Serbia":"rs",
    "Serbia and Montenegro":"csxx",
    "Seychelles":"sc",
    "Siam":"xsi",
    "Sierra Leone":"sl",
    "Slovakia":"sk",
    "Slovenia":"si",
    "Solomon Islands":"sb",
    "Somalia":"so",
    "South Georgia and the South Sandwich Islands":"gs",
    "South Korea":"kr",
    "Soviet Union":"suhh",
    "Sri Lanka":"lk",
    "Sudan":"sd",
    "Suriname":"sr",
    "Svalbard and Jan Mayen":"sj",
    "Swaziland":"sz",
    "Syria":"sy",
    "Taiwan":"tw",
    "Tajikistan":"tj",
    "Tanzania":"tz",
    "Timor-Leste":"tl",
    "Togo":"tg",
    "Tokelau":"tk",
    "Tonga":"to",
    "Trinidad and Tobago":"tt",
    "Tunisia":"tn",
    "Turkey":"tr",
    "Turkmenistan":"tm",
    "Turks and Caicos Islands":"tc",
    "Tuvalu":"tv",
    "U.S. Virgin Islands":"vi",
    "Uganda":"ug",
    "Ukraine":"ua",
    "United Arab Emirates":"ae",
    "United States Minor Outlying Islands":"um",
    "Uruguay":"uy",
    "Uzbekistan":"uz",
    "Vanuatu":"vu",
    "Venezuela":"ve",
    "Vietnam":"vn",
    "Wallis and Futuna":"wf",
    "West Germany":"xwg",
    "Western Sahara":"eh",
    "Yemen":"ye",
    "Yugoslavia":"xyu",
    "Zaire":"zrcd",
    "Zambia":"zm",
    "Zimbabwe":"zw"}
    if reverse:
        return find_key(countries_dict,countries_select)
    else:
        return countries_dict[countries_select]

def get_searches():
    #TODO persistent searches
    return []

def get_categories():
    return ["Any","Action","Adventure","Animation","Biography","Comedy","Crime","Documentary","Drama","Family",
    "Fantasy","Film Noir","Game show","History","Horror","Music","Musical","Mystery","News","Reality TV","Romance",
    "Sci-Fi","Sport","Talk Show","Thriller","War","Western"]


def favourite_settings(settings_url):
    settings = dict(parse_qsl(settings_url))
    for s in settings:
        value = settings[s]
        if value == "NULL":
            value = ''
        __settings__.setSetting(s,value)


def get_url(settings):
    new_settings = {}
    for setting in settings:
        if settings[setting] not in ('None','Any','NULL'):
            new_settings[setting] = settings[setting]
    settings = new_settings

    if not "start" in settings:
        settings["start"] = "1"

    imdb_query = {}

    if "count" in settings:
        imdb_query["count"] = settings["count"]

    if "title" in settings:
        imdb_query["title"] = settings["title"]

    if "title_type" in settings:
        imdb_query["title_type"] = get_title_type(settings["title_type"])

    release_date = ['','']
    if "release_date_start" in settings:
        release_date[0] = settings["release_date_start"]
    if "release_date_end" in settings:
        release_date[1] = settings["release_date_end"]
    imdb_query["release_date"] = '%s,%s' % (release_date[0],release_date[1])

    user_rating = [0.0,10.0]
    if "user_rating_low" in settings:
        user_rating[0] = settings["user_rating_low"]
    if "user_rating_high" in settings:
        user_rating[1] = settings["user_rating_high"]
    imdb_query["user_rating"] = "%.1f,%.1f" % (float(user_rating[0]),float(user_rating[1]))

    num_votes = ['','']
    if "num_votes_low" in settings:
        num_votes[0] = settings["num_votes_low"]
    if "num_votes_high" in settings:
        num_votes[1] = settings["num_votes_high"]
    imdb_query["num_votes"] = '%s,%s' % (num_votes[0],num_votes[1])

    genres = ['','']
    if "category" in settings:
        genres[0] = get_genre(settings["category"])
    if "genres" in settings:
        genres[1] = get_genre(settings["genres"])
    imdb_query["genres"] = ('%s,%s' % (genres[0],genres[1])).strip(',')

    if "groups" in settings:
        imdb_query["groups"] = get_groups(settings["groups"])

    if "companies" in settings:
        imdb_query["companies"] = get_companies(settings["companies"])

    boxoffice_gross_us = ['','']
    if "boxoffice_gross_us_low" in settings:
        boxoffice_gross_us[0] = settings["boxoffice_gross_us_low"]
    if "boxoffice_gross_us_high" in settings:
        boxoffice_gross_us[1] = settings["boxoffice_gross_us_high"]
    imdb_query["boxoffice_gross_us"] = '%s,%s' % (boxoffice_gross_us[0],boxoffice_gross_us[1])

    if "sort" in settings:
        imdb_query["sort"] = get_sort(settings["sort"])

    if "certificates" in settings:
        imdb_query["certificates"] = get_certificates(settings["certificates"])

    if "countries" in settings:
        imdb_query["countries"] = get_countries(settings["countries"])

    if "languages" in settings:
        imdb_query["languages"] = get_languages(settings["languages"])

    moviemeter = ['','']
    if "moviemeter_low" in settings:
        moviemeter[0] = settings["moviemeter_low"]
    if "moviemeter_high" in settings:
        moviemeter[1] = settings["moviemeter_high"]
    imdb_query["moviemeter"] = '%s,%s' % (moviemeter[0],moviemeter[1])

    if "production_status" in settings:
        imdb_query["production_status"] = get_production_status(settings["production_status"])

    runtime = ['','']
    if "runtime_start" in settings:
        runtime[0] = settings["runtime_low"]
    if "runtime_end" in settings:
        runtime[1] = settings["runtime_high"]
    imdb_query["runtime"] = '%s,%s' % (runtime[0],runtime[1])

    if "colors" in settings:
        imdb_query["colors"] = get_colors(settings["colors"])

    if "crew" in settings:
        imdb_query["role"] = settings["crew"]

    if "plot" in settings:
        imdb_query["plot"] = settings["plot"]

    if "keywords" in settings:
        imdb_query["keywords"] = settings["keywords"]

    if "locations" in settings:
        imdb_query["locations"] = settings["locations"]

    if "start" in settings:
        imdb_query["start"] = settings["start"]

    server = 'www'
    if "server" in settings:
        server = get_server(settings["server"])

    url = "http://%s.imdb.com/search/title?" % server
    params = {}
    for key in imdb_query:
        value = imdb_query[key]
        if not "Any" in value and value != "None" and value != "" and value != "," and value != "*" and value != "*," and value != ",*": #NOTE title has * sometimes
            params[key] = value

    params_url = urllib.urlencode(params)
    url = "%s%s" % (url,params_url)

    return (url, settings)

def get_videos(settings):
    (url, params) = get_url(settings)
    params["more"] = "false"

    r = requests.get(url, headers=headers)
    html = r.text
    html = HTMLParser.HTMLParser().unescape(html)

    items = html.split('<div class="lister-item ')
    videos = []
    for item in items:

        if not re.search(r'^mode-advanced">',item):
            continue

        #loadlate="http://ia.media-imdb.com/images/M/MV5BMjIyMTg5MTg4OV5BMl5BanBnXkFtZTgwMzkzMjY5NzE@._V1_UX67_CR0,0,67,98_AL_.jpg"
        img_url = ''
        img_match = re.search(r'<img.*?loadlate="(.*?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if img_match:
            img = img_match.group(1)
            img_url = re.sub(r'U[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width

        title = ''
        imdbID = ''
        year = ''
        #<a href="/title/tt1985949/?ref_=adv_li_tt"\n>Angry Birds</a>
        title_match = re.search(r'<a href="/title/(tt[0-9]*)/\?ref_=adv_li_tt".>(.*?)</a>', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)

        #<span class="lister-item-year text-muted unbold">(2016)</span>
        title_match = re.search(r'<span class="lister-item-year text-muted unbold">.*?\(([0-9]*?)\)<\/span>', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(1)


        #Episode:</small>\n    <a href="/title/tt4480392/?ref_=adv_li_tt"\n>\'Cue Detective</a>\n    <span class="lister-item-year text-muted unbold">(2015)</span>
        #Episode:</small>\n    <a href="/title/tt4952864/?ref_=adv_li_tt"\n>#TeamLucifer</a>\n    <span class="lister-item-year text-muted unbold">(2016)</span
        episode = ''
        episode_id = ''
        episode_match = re.search(r'Episode:</small>\n    <a href="/title/(tt.*?)/?ref_=adv_li_tt"\n>(.*?)</a>\n    <span class="lister-item-year text-muted unbold">\((.*?)\)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if episode_match:
            episode_id = episode_match.group(1)
            episode = "%s (%s)" % (episode_match.group(2), episode_match.group(3))
            year = episode_match.group(3)

        #Users rated this 6.1/10 (65,165 votes)
        rating = ''
        votes = ''
        rating_match = re.search(r'title="Users rated this (.+?)/10 \((.+?) votes\)', item, flags=(re.DOTALL | re.MULTILINE))
        if rating_match:
            rating = rating_match.group(1)
            votes = rating_match.group(2)
            votes = re.sub(',','',votes)

        #<p class="text-muted">\nRusty Griswold takes his own family on a road trip to "Walley World" in order to spice things up with his wife and reconnect with his sons.</p>
        plot = ''
        plot_match = re.search(r'<p class="text-muted">(.+?)</p>', item, flags=(re.DOTALL | re.MULTILINE))
        if plot_match:
            plot = plot_match.group(1).strip()

        #Stars:\n<a href="/name/nm0255124/?ref_=adv_li_st_0"\n>Tom Ellis</a>, \n<a href="/name/nm0314514/?ref_=adv_li_st_1"\n>Lauren German</a>, \n<a href="/name/nm1204760/?ref_=adv_li_st_2"\n>Kevin Alejandro</a>, \n<a href="/name/nm0940851/?ref_=adv_li_st_3"\n>D.B. Woodside</a>\n    </p>
        cast = []
        cast_match = re.search(r'<p class="">(.*?)</p>', item, flags=(re.DOTALL | re.MULTILINE))
        if cast_match:
            cast = cast_match.group(1)
            cast_list = re.findall(r'<a.+?>(.+?)</a>', cast, flags=(re.DOTALL | re.MULTILINE))
            cast = cast_list


        #<span class="genre">\nAdventure, Comedy            </span>
        genres = ''
        genre_match = re.search(r'<span class="genre">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if genre_match:
            genres = genre_match.group(1).strip()
            #genre_list = re.findall(r'<a.+?>(.+?)</a>', genre)
            #genres = ",".join(genre_list)

        #class="runtime">99 min</span>
        runtime = ''
        runtime_match = re.search(r'class="runtime">(.+?) min</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if runtime_match:
            runtime = int(runtime_match.group(1)) * 60

        sort = ''
        #sort_match = re.search(r'<span class="sort"><span title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        #if sort_match:
        #    sort = sort_match.group(1)

        #<span class="certificate">PG</span>
        certificate = ''
        certificate_match = re.search(r'<span class="certificate">(.*?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)

        if imdbID:
            id = imdbID
            title_type = get_title_type(params["title_type"])
            if title_type == "tv_series" or title_type == "mini_series":
                meta_url = "plugin://plugin.video.meta/tv/search_term/%s/1" % urllib.quote_plus(title.encode("utf8"))
            elif title_type == "tv_episode":
                vlabel = "%s - %s" % (title, episode)
                vlabel = urllib.quote_plus(vlabel.encode("utf8"))
                meta_url = "plugin://plugin.video.imdbsearch/?action=episode&imdb_id=%s&episode_id=%s&title=%s" % (imdbID,episode_id,vlabel)
                id = episode_id
            else:
                meta_url = 'plugin://plugin.video.meta/movies/play/imdb/%s/select' % imdbID

            videos.append({'name':title,'episode':episode,'thumb':img_url,'genre':genres,
            'video':meta_url,'episode_id':episode_id,'imdb_id':imdbID,
            'code': id,'year':year,'mediatype':'movie','rating':rating,'plot':plot,
            'sort':sort,'cast':cast,'runtime':runtime,'votes':votes, 'certificate':certificate})

    #href="?count=100&sort=moviemeter,asc&production_status=released&languages=en&release_date=2015,2016&user_rating=6.0,10.0&start=1&num_votes=100,&title_type=feature&page=2&ref_=adv_nxt"
    pagination_match = re.search(r'href="(.*?&ref_=adv_nxt)"', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        params["start"] = str(int(params["start"]) + int(params["count"]))
        params["more"] = "true"

    return (videos,params)

def get_tvdb_id(imdb_id):
    tvdb_url = "http://thetvdb.com//api/GetSeriesByRemoteID.php?imdbid=%s" % imdb_id
    r = requests.get(tvdb_url)
    tvdb_html = r.text
    tvdb_id = ''
    tvdb_match = re.search(r'<seriesid>(.*?)</seriesid>', tvdb_html, flags=(re.DOTALL | re.MULTILINE))
    if tvdb_match:
        tvdb_id = tvdb_match.group(1)
    return tvdb_id

def find_episode(imdb_id,episode_id,title):
    tvdb_id = get_tvdb_id(imdb_id)

    server = get_server(__settings__.getSetting( "server" ))
    episode_url = "http://%s.imdb.com/title/%s" % (server,episode_id)
    r = requests.get(episode_url, headers=headers)
    episode_html = r.text
    episode_html = HTMLParser.HTMLParser().unescape(episode_html)
    season = ''
    episode = ''
    season_match = re.search(r'<div class="bp_heading">Season ([0-9]*?) <span class="ghost">\|</span> Episode ([0-9]*?)</div>',
    episode_html, flags=(re.DOTALL | re.MULTILINE))
    if season_match:
        season = season_match.group(1)
        episode = season_match.group(2)

    meta_url = "plugin://plugin.video.meta/tv/play/%s/%s/%s/%s" % (tvdb_id,season,episode,'select')
    list_item = xbmcgui.ListItem(label=title)
    list_item.setPath(meta_url)
    list_item.setProperty("IsPlayable", "true")
    list_item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.setResolvedUrl(_handle, True, listitem=list_item)


def list_searches():
    (settings, settings_url) = get_settings_url()

    settings_url=urllib.quote_plus(settings_url)
    searches = get_searches()
    prefix = settings['prefix']

    if prefix == "NULL":
        name = 'Search'
    else:
        name = '%s Search' % prefix
    prefix = urllib.quote_plus(prefix)
    searches.append((name,settings))
    listing = []
    for (name,settings) in searches:
        list_item = xbmcgui.ListItem(label=name)
        genre_icon = get_genre_icon('Any')
        list_item.setArt({'thumb': genre_icon, 'icon': genre_icon, 'fanart': get_background()})
        plot = ""
        for setting in sorted(settings):
            value = settings[setting]
            if value == "NULL":
                value = ''
            plot = plot + "%s[COLOR=darkgray]=[/COLOR][B]%s[/B] " % (setting, value)
        list_item.setInfo('video', {'title': name, 'genre': '', 'plot': plot})
        url = '{0}?action=categories&settings={1}'.format(_url, settings_url)
        is_folder = True
        context_items = []
        context_items.append(('Information', 'XBMC.Action(Info)'))
        list_item.addContextMenuItems(context_items,replaceItems=False)
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)

def get_settings_url():
    settings = {}
    setting_keys = [
    "boxoffice_gross_us_high",
    "boxoffice_gross_us_low",
    "certificates",
    "companies",
    "count",
    "countries",
    "genres",
    "groups",
    "languages",
    "moviemeter_high",
    "moviemeter_low",
    "num_votes_high",
    "num_votes_low",
    "prefix",
    "production_status",
    "release_date_end",
    "release_date_start",
    "runtime_high",
    "runtime_low",
    "server",
    "sort",
    "title",
    "plot",
    "keywords",
    "crew",
    "colors",
    "locations",
    "title_type",
    "tv_view",
    "user_rating_high",
    "user_rating_low",
    "video_view",
    ]
    for setting in setting_keys:
        settings[setting] = __settings__.getSetting(setting)
        if not settings[setting]:
            settings[setting] = 'NULL'
    settings_url = urllib.urlencode(settings)
    return (settings, settings_url)


def list_categories(settings_url):
    params = dict(parse_qsl(settings_url))

    categories = get_categories()
    listing = []
    genre = params["genres"]
    for category in categories:
        params['category'] = category
        if params['prefix'] != "NULL":
            name = "%s %s" % (params['prefix'], category)
        else:
            name = category
        list_item = xbmcgui.ListItem(label=name)
        context_items = []
        context_items.append(('Information', 'XBMC.Action(Info)'))
        context_items.append(('Reload Settings From Favourite',
        "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=favourite_settings&settings=%s)" % (urllib.quote_plus(settings_url))))
        list_item.addContextMenuItems(context_items,replaceItems=False)
        genre_icon = get_genre_icon(category)
        list_item.setArt({'thumb': genre_icon, 'icon': genre_icon, 'fanart': get_background()})
        plot = ""
        for param in sorted(params):
            value = params[param]
            if value == "NULL":
                value = ''
            plot = plot + "%s[COLOR=darkgray]=[/COLOR][B]%s[/B] " % (param, value)
        list_item.setInfo('video', {'title': name, 'genre': category, 'plot': plot})
        url = '{0}?action=listing&settings={1}'.format(_url, urllib.quote_plus(urllib.urlencode(params)))
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)


def list_videos(settings_url):
    params = dict(parse_qsl(settings_url))

    (videos, params) = get_videos(params)
    title_type = get_title_type(params["title_type"])
    type = ''
    content = ''
    info_type = ''
    trakt_type = ''
    if title_type == "tv_series" or title_type == "mini_series":
        trakt_type = 'shows'
        info_type = 'extendedtvinfo'
        content = 'tvshows'
        type = 'tv'
        IsPlayable = 'false'
        is_folder = True
    elif title_type == "game":
        content = 'files'
        IsPlayable = 'false'
        is_folder = False
    elif title_type == 'tv_episode':
        trakt_type = 'episodes'
        info_type = ''
        content = 'episodes'
        type = 'episode'
        IsPlayable = 'true'
        is_folder = False
    else:
        trakt_type = 'movies'
        info_type = 'extendedinfo'
        content = 'movies'
        type = 'movies'
        IsPlayable = 'true'
        is_folder = False
    listing = []
    for video in videos:
        if title_type == "tv_episode":
            vlabel = "%s - %s" % (video['name'], video['episode'])
        else:
            vlabel = video['name']
        list_item = xbmcgui.ListItem(label=vlabel)
        list_item.setInfo('video', {'title': vlabel, 'genre': video['genre'],'code': video['code'],
        'year':video['year'],'mediatype':'movie','rating':video['rating'],'plot': video['plot'],
        'mpaa': video['certificate'],'cast': video['cast'],'duration': video['runtime'], 'votes': video['votes']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': get_background()})
        list_item.setProperty('IsPlayable', IsPlayable)
        is_folder = is_folder
        context_items = []
        context_items.append(('Information', 'XBMC.Action(Info)'))
        if info_type:
            context_items.append(('Extended Info', "XBMC.RunScript(script.extendedinfo,info=%s,imdb_id=%s)" % (info_type,video['code'])))
        context_items.append(('Reload Settings From Favourite',
        "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=favourite_settings&settings=%s)" %
        (urllib.quote_plus(settings_url))))
        if type == 'movies' or type == 'tv' or type == 'episode':
            if __settings__.getSetting('trakt') == 'true':
                context_items.append(('Add to Trakt Watchlist',
                "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=addtotraktwatchlist&type=%s&imdb_id=%s&title=%s)" %
                (trakt_type, video['code'], urllib.quote_plus(vlabel.encode("utf8")))))
        if type == 'movies' or type == 'tv':
            run_str = "plugin://plugin.video.imdbsearch/?action=library&type=%s&imdb_id=%s" % (type,video['code'])
            context_items.append(('Add To Meta Library', "XBMC.RunPlugin(%s)" % run_str ))
        context_items.append(('Meta Settings', "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=meta_settings)"))
        try:
            if type == 'movies' and xbmcaddon.Addon('plugin.video.couchpotato_manager'):
                context_items.append(
                ('Add to Couch Potato', "XBMC.RunPlugin(plugin://plugin.video.couchpotato_manager/movies/add-by-id/%s)" % (video['code'])))
        except:
            pass
        try:
            if type == 'tv' and xbmcaddon.Addon('plugin.video.sickrage'):
                context_items.append(
                ('Add to Sickrage', "XBMC.RunPlugin(plugin://plugin.video.sickrage?action=addshow&&show_name=%s)" % (video['name'])))
        except:
            pass
        if __settings__.getSetting('default_context_menu') == 'true':
            list_item.addContextMenuItems(context_items,replaceItems=False)
        else:
            context_items.append(('Add to Favourites', "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=favourite&name=%s&thumb=%s&cmd=%s)" %
            (urllib.quote_plus(video['name'].encode("utf8")),urllib.quote_plus(video['thumb']),urllib.quote_plus(video['video']))))
            list_item.addContextMenuItems(context_items,replaceItems=True)
        video_streaminfo = {'codec': 'h264'}
        video_streaminfo['aspect'] = round(1280.0 / 720.0, 2)
        video_streaminfo['width'] = 1280
        video_streaminfo['height'] = 720
        list_item.addStreamInfo('video', video_streaminfo)
        list_item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
        if title_type == "game":
            here_url = "%s%s" % (sys.argv[0],sys.argv[2]) #TODO
            listing.append((here_url, list_item, is_folder))
        else:
            listing.append((video['video'], list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    listing = []
    if params["more"] == "true":
        url = '{0}?action=listing&settings={1}'.format(_url, urllib.quote_plus(urllib.urlencode(params)))
        list_item = xbmcgui.ListItem(label='[B]Next Page >>[/B]')
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb': 'DefaultNetwork.png', 'icon': 'DefaultNetwork.png', 'fanart': get_background()})
        is_folder = True
        listing.append((url, list_item, is_folder))
        xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    xbmcplugin.setContent(int(sys.argv[1]), content)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_UNSORTED)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_TITLE)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_YEAR)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_MPAA_RATING)
    xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_VIDEO_RUNTIME)
    xbmcplugin.endOfDirectory(_handle)

    if title_type == "tv_episode":
        xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "tv_view" ))
    else:
        xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "video_view" ))

def play_video(path):
    play_item = xbmcgui.ListItem(path=path)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)

def on_token_refreshed(response):
    __settings__.setSetting( "authorization", dumps(response))

def authenticate():
    dialog = xbmcgui.Dialog()
    pin = dialog.input('Open a web browser at %s' % Trakt['oauth'].pin_url(), type=xbmcgui.INPUT_ALPHANUM)
    if not pin:
        return False
    authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
    if not authorization:
        return False
    __settings__.setSetting( "authorization", dumps(authorization))
    return True

def add_to_trakt_watchlist(type,imdb_id,title):
    Trakt.configuration.defaults.app(
        id=8835
    )
    Trakt.configuration.defaults.client(
        id="aa1c239000c56319a64014d0b169c0dbf03f7770204261c9edbe8ae5d4e50332",
        secret="250284a95fd22e389b565661c98d0f33ac222e9d03c43b5931e03946dbf858dc"
    )
    Trakt.on('oauth.token_refreshed', on_token_refreshed)
    if not __settings__.getSetting('authorization'):
        if not authenticate():
            return
    authorization = loads(__settings__.getSetting('authorization'))
    with Trakt.configuration.oauth.from_response(authorization, refresh=True):
        result = Trakt['sync/watchlist'].add({
            type: [
                {
                    'ids': {
                        'imdb': imdb_id
                    }
                }
            ]
        })
        dialog = xbmcgui.Dialog()
        dialog.notification("Trakt: add to watchlist",title)

def find_crew(name=''):
    dialog = xbmcgui.Dialog()
    if not name:
        name = dialog.input('Search for crew (actor, director etc)', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding crew details...')
    if not name:
        dialog.notification('IMDB:','No name!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&nm=on" % urllib.quote_plus(name)
    r = requests.get(url)
    json = r.json()
    crew = []

    if 'name_popular' in json:
        pop = json['name_popular']
        for p in pop:
            crew.append((p['name'],p['id']))
    if 'name_exact' in json:
        pop = json['name_exact']
        for p in pop:
            crew.append((p['name'],p['id']))
    if 'name_approx' in json:
        approx = json['name_approx']
        for p in approx:
            crew.append((p['name'],p['id']))
    if 'name_substring' in json:
        pop = json['name_substring']
        for p in pop:
            crew.append((p['name'],p['id']))
    names = [item[0] for item in crew]
    if names:
        index = dialog.select('Pick crew member',names)
        id = crew[index][1]
        __settings__.setSetting('crew',id)
    else:
        dialog.notification('IMDB:','Nothing Found!')

def find_keywords(keyword=''):
    dialog = xbmcgui.Dialog()
    if not keyword:
        keyword = dialog.input('Search for keyword', type=xbmcgui.INPUT_ALPHANUM)
    dialog.notification('IMDB:','Finding keyword matches...')
    if not keyword:
        dialog.notification('IMDB:','No keyword!')
        return
    url = "http://www.imdb.com/xml/find?json=1&nr=1&q=%s&kw=on" % urllib.quote_plus(keyword)
    r = requests.get(url)
    json = r.json()
    keywords = []
    if 'keyword_popular' in json:
        pop = json['keyword_popular']
        for p in pop:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_exact' in json:
        pop = json['keyword_exact']
        for p in pop:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_approx' in json:
        approx = json['keyword_approx']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    if 'keyword_substring' in json:
        approx = json['keyword_substring']
        for p in approx:
            keywords.append((p['description'],p['keyword']))
    names = [item[0] for item in keywords]
    if keywords:
        index = dialog.select('Pick keywords member',names)
        id = keywords[index][1]
        __settings__.setSetting('keywords',id)
    else:
        dialog.notification('IMDB:','Nothing Found!')


def favourite(name,thumb,cmd):
    result = loads(xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Favourites.AddFavourite", "params": {"title":"%s", "type":"media", "path":"%s", "thumbnail":"%s"}, "id": 1}' % (name, cmd, thumb)))

def repad(data):
     return data + "=" * (-len(data)%4)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    type = ''
    if 'type' in params.keys():
        type = params['type']
    imdb_id = ''
    if 'imdb_id' in params.keys():
        imdb_id = params['imdb_id']
    name = ''
    if 'name' in params.keys():
        name = params['name']
        name = urllib.unquote_plus(name)
    settings_url = ''
    if 'settings' in params.keys():
        settings_url = urllib.unquote_plus(params['settings'])
    thumb = ''
    if 'thumb' in params.keys():
        thumb = urllib.unquote_plus(params['thumb'])
    cmd = ''
    if 'cmd' in params.keys():
        cmd = urllib.unquote_plus(params['cmd'])
    episode_id = ''
    if 'episode_id' in params.keys():
        episode_id = params['episode_id']
    if 'title' in params.keys():
        titleq = params['title']
        title = urllib.unquote_plus(titleq)
    if 'action' in params:
        if params['action'] == 'find_keywords':
            find_keywords()
        elif params['action'] == 'find_crew':
            find_crew()
        elif params['action'] == 'meta_settings':
            xbmcaddon.Addon(id='plugin.video.meta').openSettings()
        elif params['action'] == 'library':
            if type == 'tv':
                id = get_tvdb_id(imdb_id)
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.meta/%s/add_to_library/%s)" % (type,id))
            else:
                xbmc.executebuiltin("RunPlugin(plugin://plugin.video.meta/%s/add_to_library/tmdb/%s)" % (type,imdb_id))
        elif params['action'] == 'categories':
            if settings_url:
                list_categories(settings_url)
        elif params['action'] == 'favourite_settings':
            if settings_url:
                favourite_settings(settings_url)
        elif params['action'] == 'favourite':
            if cmd:
                favourite(name,thumb,cmd)
        elif params['action'] == 'listing':
            if settings_url:
                list_videos(settings_url)
        elif params['action'] == 'addtotraktwatchlist':
            if imdb_id:
                add_to_trakt_watchlist(type,imdb_id,title)
        elif params['action'] == 'episode':
            if imdb_id:
                find_episode(imdb_id,episode_id,title)
    else:
        if __settings__.getSetting('open_settings') == 'true':
            __settings__.openSettings()
        list_searches()


if __name__ == '__main__':
    version = __settings__.getAddonInfo('version')
    if __settings__.getSetting('version') != version:
        __settings__.setSetting('version', version)
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36', 'referer':'http://192.%s' % version}
        try:
            r = requests.get('http://goo.gl/WHQAKX',headers=headers)
            home = r.content
        except: pass

    if __settings__.getSetting('trakt') == 'false':
        __settings__.setSetting( "authorization", '')
    router(sys.argv[2][1:])