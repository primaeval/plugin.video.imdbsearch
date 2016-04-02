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

def get_server(server_select):
    server_dict = {"Original Title":"akas",
    "Normal":"www"}
    return server_dict[server_select]

def get_sort(sort_select):
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
    return sort_dict[sort_select]

def get_certificate(certificate_select):
    certificate_dict = {"Any":"Any",
    "US:G":"us:g",
    "US:PG":"us:pg",
    "US:PG_13":"us:pg_13",
    "US:R":"us:r",
    "US:NC_17":"us:nc_17"}
    return certificate_dict[certificate_select]

def get_company(companies_select):
    companies_dict = {"Any":"Any",
    "Fox":"fox",
    "Columbia":"columbia",
    "Dreamworks":"dreamworks",
    "MGM":"mgm",
    "Paramount":"paramount",
    "Universal":"universal",
    "Disney":"disney",
    "Warner":"warner"}
    return companies_dict[companies_select]

def get_production_status(production_status_select):
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
    return production_status_dict[production_status_select]

def get_group(groups_select):
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
    return groups_dict[groups_select]

def get_genre(genres_select):
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
    return genres_dict[genres_select]

def get_title_type(title_type_select):
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
    return title_type_dict[title_type_select]

def get_languages(languages_select):
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
    return languages_dict[languages_select]

def get_countries(countries_select):
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
    return countries_dict[countries_select]

def get_categories():
    return ["Any","Action","Adventure","Animation","Biography","Comedy","Crime","Documentary","Drama","Family",
    "Fantasy","Film Noir","Game show","History","Horror","Music","Musical","Mystery","News","Reality TV","Romance",
    "Sci-Fi","Sport","Talk Show","Thriller","War","Western"]

def get_url(category,start):
    imdb_query = [
    ("count", __settings__.getSetting( "count" )),
    ("title", __settings__.getSetting( "title" )),
    ("title_type", get_title_type(__settings__.getSetting( "title_type" ))),
    ("release_date", "%s,%s" % (__settings__.getSetting( "release_date_start" ),__settings__.getSetting( "release_date_end" ))),
    ("user_rating", "%.1f,%.1f" % (float(__settings__.getSetting( "user_rating_low" )),float(__settings__.getSetting( "user_rating_high" )))),
    ("num_votes", "%s,%s" % (__settings__.getSetting( "num_votes_low" ),__settings__.getSetting( "num_votes_high" ))),
    ("genres", "%s,%s" % (get_genre(category),get_genre(__settings__.getSetting( "genres" )))),   
    ("groups", "%s" % (get_group(__settings__.getSetting( "groups" )))),  
    ("companies", get_company(__settings__.getSetting( "companies" ))),
    ("boxoffice_gross_us", "%s,%s" % (__settings__.getSetting( "boxoffice_gross_us_low" ),__settings__.getSetting( "boxoffice_gross_us_high" ))),
    ("sort", get_sort(__settings__.getSetting( "sort" ))),
    ("certificates", get_certificate(__settings__.getSetting( "certificates" ))),
    ("countries", get_countries(__settings__.getSetting( "countries" ))),
    ("languages", get_languages(__settings__.getSetting( "languages" ))),
    ("moviemeter", "%s,%s" % (__settings__.getSetting( "moviemeter_low" ),__settings__.getSetting( "moviemeter_high" ))),
    ("production_status", get_production_status(__settings__.getSetting( "production_status" ))),
    ("runtime", "%s,%s" % (__settings__.getSetting( "runtime_low" ),__settings__.getSetting( "runtime_high" ))),
    ("sort", get_sort(__settings__.getSetting( "sort" ))),
    ("start", start),
    ]
    server = get_server(__settings__.getSetting( "server" ))
    url = "http://%s.imdb.com/search/title?" % server
    params = {}
    for (field, value) in imdb_query:
        if not "Any" in value and value != "None" and value != "" and value != "," and value != "*" and value != "*," and value != ",*": #NOTE title has * sometimes
            params[field] = value
    params_url = urllib.urlencode(params)
    url = "%s%s" % (url,params_url)
    return (url,params)

def get_videos(url):
    r = requests.get(url)
    html = r.text
    html = HTMLParser.HTMLParser().unescape(html)
    
    items = html.split('<tr class="')
    videos = []
    for item in items:
        
        if not re.search(r'^.*?detailed"',item):
            continue
        
        img_url = ''
        img_match = re.search(r'<img src="(.*?)"', item)
        if img_match:
            img = img_match.group(1)
            img_url = re.sub(r'S[XY].*_.jpg','SX344_.jpg',img) #NOTE 344 is Confluence List View width

        title = ''
        imdbID = ''
        year = ''
        title_match = re.search(r'<td class="title">.*?<a href="/title/(.+?)/">(.*?)</a>', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            imdbID = title_match.group(1)
            title = title_match.group(2)

        title_match = re.search(r'<a href="/title/(.+?)/" title="(.+?) \((.+?)\)"', item, flags=(re.DOTALL | re.MULTILINE))
        if title_match:
            year = title_match.group(3)

        episode = ''
        episode_id = ''
        episode_match = re.search(r'<span class="episode">Episode: <a href="/title/(.+?)/">(.+?)</a>(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if episode_match:
            episode_id = episode_match.group(1)
            episode = "%s%s" % (episode_match.group(2), episode_match.group(3))
            year = episode_match.group(3).strip('() ')
            
        rating = ''
        votes = ''
        rating_match = re.search(r'title="Users rated this (.+?)/10 \((.+?) votes\)', item, flags=(re.DOTALL | re.MULTILINE))
        if rating_match:
            rating = rating_match.group(1)
            votes = rating_match.group(2)
            votes = re.sub(',','',votes)
            
        plot = ''
        plot_match = re.search(r'<span class="outline">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if plot_match:
            plot = plot_match.group(1)
            
        cast = []
        cast_match = re.search(r'<span class="credit">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if cast_match:
            cast = cast_match.group(1)
            cast_list = re.findall(r'<a.+?>(.+?)</a>', cast)
            cast = cast_list
                
        genres = ''
        genre_match = re.search(r'<span class="genre">(.+?)</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if genre_match:
            genre = genre_match.group(1)
            genre_list = re.findall(r'<a.+?>(.+?)</a>', genre)
            genres = ",".join(genre_list)
                
        runtime = ''
        runtime_match = re.search(r'<span class="runtime">(.+?) mins\.</span>', item, flags=(re.DOTALL | re.MULTILINE))
        if runtime_match:
            runtime = int(runtime_match.group(1)) * 60
                
        sort = ''
        sort_match = re.search(r'<span class="sort"><span title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if sort_match:
            sort = sort_match.group(1)

        certificate = ''
        certificate_match = re.search(r'<span class="certificate">.*?title="(.+?)"', item, flags=(re.DOTALL | re.MULTILINE))
        if certificate_match:
            certificate = certificate_match.group(1)
            
        if imdbID:
            id = imdbID
            title_type = get_title_type(__settings__.getSetting( "title_type" ))
            if title_type == "tv_series" or title_type == "mini_series": 
                meta_url = "plugin://plugin.video.meta/tv/search_term/%s/1" % re.sub(' ','+',title)
            elif title_type == "tv_episode":
                vlabel = "%s - %s" % (title, episode)
                vlabel = urllib.quote_plus(vlabel.encode("utf8"))
                meta_url = "plugin://plugin.video.imdbsearch/?action=episode&imdb_id=%s&episode_id=%s&title=%s" % (imdbID,episode_id,vlabel)
                id = episode_id
            else:
                meta_url = 'plugin://plugin.video.meta/movies/play/imdb/%s/default' % imdbID

            videos.append({'name':title,'episode':episode,'thumb':img_url,'genre':genres,
            'video':meta_url,'episode_id':episode_id,'imdb_id':imdbID,
            'code': id,'year':year,'mediatype':'movie','rating':rating,'plot':plot,
            'sort':sort,'cast':cast,'runtime':runtime,'votes':votes, 'certificate':certificate})
            
    next_url = ''
    pagination_match = re.search(r'<span class="pagination">.*<a href="(.+?)">Next', html, flags=(re.DOTALL | re.MULTILINE))
    if pagination_match:
        server = get_server(__settings__.getSetting( "server" ))
        next_url = "http://%s.imdb.com%s" % (server,pagination_match.group(1))
        
    return (videos,next_url)
    
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
    r = requests.get(episode_url)
    episode_html = r.text
    episode_html = HTMLParser.HTMLParser().unescape(episode_html)
    season = ''
    episode = ''
    season_match = re.search(r'<div class="bp_heading">Season ([0-9]*?) <span class="ghost">\|</span> Episode ([0-9]*?)</div>', 
    episode_html, flags=(re.DOTALL | re.MULTILINE))
    if season_match:
        season = season_match.group(1)
        episode = season_match.group(2)
        
    meta_url = "plugin://plugin.video.meta/tv/play/%s/%s/%s/%s" % (tvdb_id,season,episode,'default')
    list_item = xbmcgui.ListItem(label=title)
    list_item.setPath(meta_url)
    list_item.setProperty("IsPlayable", "true")
    list_item.setInfo(type='Video', infoLabels={'Title': title})
    xbmcplugin.setResolvedUrl(_handle, True, listitem=list_item)
    

def list_categories():
    categories = get_categories()
    listing = []
    for category in categories:
        prefix = __settings__.getSetting( "prefix" )
        cat = re.sub('_',' ',category)
        if prefix:
            name = "%s %s" % (prefix, re.sub('_',' ',cat))
        else:
            name = cat
        list_item = xbmcgui.ListItem(label=name)
        genre_icon = get_genre_icon(category)
        list_item.setArt({'thumb': genre_icon, 'icon': genre_icon})
        (url,params) = get_url(category,'')
        imdb_url=urllib.quote_plus(url)
        plot = ""
        params['server'] = get_server(__settings__.getSetting( "server" ))
        for param in sorted(params):
            plot = plot + "%s[COLOR=darkgray]=[/COLOR][B]%s[/B] " % (param, params[param])
        list_item.setInfo('video', {'title': name, 'genre': category, 'plot': plot})
        url = '{0}?action=listing&category={1}&imdb={2}'.format(_url, category,imdb_url)
        is_folder = True
        listing.append((url, list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    xbmcplugin.setContent(int(sys.argv[1]), 'episodes')
    xbmcplugin.endOfDirectory(_handle)
    xbmc.executebuiltin("Container.SetViewMode(%s)" % __settings__.getSetting( "index_view" ))


def list_videos(imdb_url):
    (videos,next_url) = get_videos(imdb_url)
    title_type = get_title_type(__settings__.getSetting( "title_type" ))
    type = ''
    content = ''
    info_type = ''
    if title_type == "tv_series" or title_type == "mini_series": 
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
        info_type = ''
        content = 'episodes'
        IsPlayable = 'true'
        is_folder = False
    else:
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
        list_item.setInfo('video', {'title': vlabel, 'genre': video['genre'],'code': video['code'], 'tagline': video['code'],
        'year':video['year'],'mediatype':'movie','rating':video['rating'],'plot': video['plot'],
        'mpaa': video['certificate'],'cast': video['cast'],'duration': video['runtime'], 'votes': video['votes']})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb']})
        list_item.setProperty('IsPlayable', IsPlayable)
        is_folder = is_folder
        context_items = []
        if type == 'movies' or type == 'tv':
            run_str = "plugin://plugin.video.imdbsearch/?action=library&type=%s&imdb_id=%s" % (type,video['code'])
            context_items.append(('Add To Meta Library', "XBMC.RunPlugin(%s)" % run_str ))
        context_items.append(('Information', 'XBMC.Action(Info)'))
        if info_type:
            context_items.append(('Extended Info', "XBMC.RunScript(script.extendedinfo,info=%s,imdb_id=%s)" % (info_type,video['code'])))
        context_items.append(('Meta Settings', "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=meta_settings)"))
        if type == 'movies':
            context_items.append(('Add to Trakt Watchlist', "XBMC.RunPlugin(plugin://plugin.video.imdbsearch/?action=addtotraktwatchlist&imdb_id=%s)" % video['code']))
        list_item.addContextMenuItems(context_items,replaceItems=True)
        video_streaminfo = {'codec': 'h264'}
        video_streaminfo['aspect'] = round(1280.0 / 720.0, 2)
        video_streaminfo['width'] = 1280
        video_streaminfo['height'] = 720
        list_item.addStreamInfo('video', video_streaminfo)
        list_item.addStreamInfo('audio', {'codec': 'aac', 'language': 'en', 'channels': 2})
        if title_type == "game": 
            here_url = "%s%s" % (sys.argv[0],sys.argv[2])
            listing.append((here_url, list_item, is_folder))
        else:
            listing.append((video['video'], list_item, is_folder))
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))

    listing = []
    if next_url:
        url = '{0}?action=listing&imdb={1}'.format(_url, urllib.quote_plus(next_url))
        list_item = xbmcgui.ListItem(label='[B]Next Page >>[/B]')
        list_item.setProperty('IsPlayable', 'true')
        list_item.setArt({'thumb': 'DefaultNetwork.png', 'icon': 'DefaultNetwork.png'})
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
        pin = dialog.input('Navigate to %s' % Trakt['oauth'].pin_url(), type=xbmcgui.INPUT_ALPHANUM)
        if not pin:
            return False
        authorization = Trakt['oauth'].token_exchange(pin, 'urn:ietf:wg:oauth:2.0:oob')
        if not authorization:
            return False
        __settings__.setSetting( "authorization", dumps(authorization))
        return True

def add_to_trakt_watchlist(imdb_id):
    Trakt.configuration.defaults.app(
        id=999
    )
    Trakt.configuration.defaults.client(
        id="d4161a7a106424551add171e5470112e4afdaf2438e6ef2fe0548edc75924868",
        secret="b5fcd7cb5d9bb963784d11bbf8535bc0d25d46225016191eb48e50792d2155c0"
    )
    Trakt.on('oauth.token_refreshed', on_token_refreshed)
    authorization = loads(__settings__.getSetting('authorization'))
    if not authorization:
        if not authenticate():
            return
    authorization = loads(__settings__.getSetting('authorization'))
    with Trakt.configuration.oauth.from_response(authorization, refresh=True):
        result = Trakt['sync/watchlist'].add({
            'movies': [
                {
                    'ids': {
                        'imdb': imdb_id
                    }
                }
            ]
        })
        dialog = xbmcgui.Dialog()
        dialog.notification("Trakt","added %s to watchlist" % imdb_id)
    
    
def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'meta_settings':
            xbmcaddon.Addon(id='plugin.video.meta').openSettings()        
        elif params['action'] == 'library':
            if 'type' in params.keys():
                type = params['type']
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
            id = imdb_id
            if type == 'tv':
                id = get_tvdb_id(imdb_id)
            xbmc.executebuiltin("RunPlugin(plugin://plugin.video.meta/%s/add_to_library/%s)" % (type,id))
        elif params['action'] == 'listing':
            if 'imdb' in params.keys():
                imdb = params['imdb']
                list_videos(urllib.unquote_plus(imdb))
        elif params['action'] == 'addtotraktwatchlist':
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
                add_to_trakt_watchlist(imdb_id)
        elif params['action'] == 'episode':
            if 'imdb_id' in params.keys():
                imdb_id = params['imdb_id']
            if 'episode_id' in params.keys():
                episode_id = params['episode_id']
            if 'title' in params.keys():
                title = params['title']
                title = urllib.unquote_plus(title)
                find_episode(imdb_id,episode_id,title)
        elif params['action'] == 'play':
            play_video(params['video'])
    else:
        list_categories()


if __name__ == '__main__':
    router(sys.argv[2][1:])