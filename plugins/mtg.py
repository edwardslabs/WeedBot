from lxml import html
import re
import urllib2
import sys

from util import hook


@hook.command
def mtg(inp):
    url = 'http://magiccards.info/query.php?cardname='
    url += urllib2.quote(inp, safe='')
    h = html.parse(url)
    name = h.find('/body/table/tr/td/table/tr/td/h1')
    if name is None:
        return "no cards found"
    card = name.getparent()
    text = card.find('p')

    type = text.text
    global t
    t=text.find('b')
    text = text.find('b').text_content()
    text = re.sub(r'\(.*?\)', '', text) # strip parenthetical explanations
    text = re.sub(r'\.(\S)', r'. \1', text) # fix spacing

    global printing
    printings = card.find('table/tr/td/img').getparent().text_content()
    printings = re.findall(r'\s*(.*?) \((.*?)\)', ' '.join(printings.split()))
    printing_out = ', '.join('%s (%s)' % (set_abbrevs.get(x[0], x[0]),
                                          rarity_abbrevs.get(x[1], x[1]))
                                          for x in printings)

    name.make_links_absolute()
    link = name.find('a').attrib['href']
    name = name.text_content().strip()
    type = type.strip()
    text = ' '.join(text.split())

    return ' | '.join((name, type, text, printing_out, link))


set_abbrevs = {
    '15th Anniversary': '15ANN',
    'APAC Junior Series': 'AJS',
    'Alara Reborn': 'ARB',
    'Alliances': 'AI',
    'Anthologies': 'AT',
    'Antiquities': 'AQ',
    'Apocalypse': 'AP',
    'Arabian Nights': 'AN',
    'Arena League': 'ARENA',
    'Asia Pacific Land Program': 'APAC',
    'Battle Royale': 'BR',
    'Beatdown': 'BD',
    'Betrayers of Kamigawa': 'BOK',
    'Celebration Cards': 'UQC',
    'Champions of Kamigawa': 'CHK',
    'Champs': 'CP',
    'Chronicles': 'CH',
    'Classic Sixth Edition': '6E',
    'Coldsnap': 'CS',
    'Coldsnap Theme Decks': 'CSTD',
    'Conflux': 'CFX',
    'Core Set - Eighth Edition': '8E',
    'Core Set - Ninth Edition': '9E',
    'Darksteel': 'DS',
    'Deckmasters': 'DM',
    'Dissension': 'DI',
    'Dragon Con': 'DRC',
    'Duel Decks: Divine vs. Demonic': 'DVD',
    'Duel Decks: Elves vs. Goblins': 'EVG',
    'Duel Decks: Garruk vs. Liliana': 'GVL',
    'Duel Decks: Jace vs. Chandra': 'JVC',
    'Eighth Edition Box Set': '8EB',
    'European Land Program': 'EURO',
    'Eventide': 'EVE',
    'Exodus': 'EX',
    'Fallen Empires': 'FE',
    'Fifth Dawn': '5DN',
    'Fifth Edition': '5E',
    'Fourth Edition': '4E',
    'Friday Night Magic': 'FNMP',
    'From the Vault: Dragons': 'FVD',
    'From the Vault: Exiled': 'FVE',
    'Future Sight': 'FUT',
    'Gateway': 'GRC',
    'Grand Prix': 'GPX',
    'Guildpact': 'GP',
    'Guru': 'GURU',
    'Happy Holidays': 'HHO',
    'Homelands': 'HL',
    'Ice Age': 'IA',
    'Introductory Two-Player Set': 'ITP',
    'Invasion': 'IN',
    'Judge Gift Program': 'JR',
    'Judgment': 'JU',
    'Junior Series': 'JSR',
    'Legend Membership': 'DCILM',
    'Legends': 'LG',
    'Legions': 'LE',
    'Limited Edition (Alpha)': 'AL',
    'Limited Edition (Beta)': 'BE',
    'Lorwyn': 'LW',
    'MTGO Masters Edition': 'MED',
    'MTGO Masters Edition II': 'ME2',
    'MTGO Masters Edition III': 'ME3',
    'Magic 2010': 'M10',
    'Magic Game Day Cards': 'MGDC',
    'Magic Player Rewards': 'MPRP',
    'Magic Scholarship Series': 'MSS',
    'Magic: The Gathering Launch Parties': 'MLP',
    'Media Inserts': 'MBP',
    'Mercadian Masques': 'MM',
    'Mirage': 'MR',
    'Mirrodin': 'MI',
    'Morningtide': 'MT',
    'Multiverse Gift Box Cards': 'MGBC',
    'Nemesis': 'NE',
    'Ninth Edition Box Set': '9EB',
    'Odyssey': 'OD',
    'Onslaught': 'ON',
    'Planar Chaos': 'PC',
    'Planechase': 'PCH',
    'Planeshift': 'PS',
    'Portal': 'PO',
    'Portal Demogame': 'POT',
    'Portal Second Age': 'PO2',
    'Portal Three Kingdoms': 'P3K',
    'Premium Deck Series: Slivers': 'PDS',
    'Prerelease Events': 'PTC',
    'Pro Tour': 'PRO',
    'Prophecy': 'PR',
    'Ravnica: City of Guilds': 'RAV',
    'Release Events': 'REP',
    'Revised Edition': 'RV',
    'Saviors of Kamigawa': 'SOK',
    'Scourge': 'SC',
    'Seventh Edition': '7E',
    'Shadowmoor': 'SHM',
    'Shards of Alara': 'ALA',
    'Starter': 'ST',
    'Starter 2000 Box Set': 'ST2K',
    'Stronghold': 'SH',
    'Summer of Magic': 'SOM',
    'Super Series': 'SUS',
    'Tempest': 'TP',
    'Tenth Edition': '10E',
    'The Dark': 'DK',
    'Time Spiral': 'TS',
    'Time Spiral Timeshifted': 'TSTS',
    'Torment': 'TR',
    'Two-Headed Giant Tournament': 'THGT',
    'Unglued': 'UG',
    'Unhinged': 'UH',
    'Unhinged Alternate Foils': 'UHAA',
    'Unlimited Edition': 'UN',
    "Urza's Destiny": 'UD',
    "Urza's Legacy": 'UL',
    "Urza's Saga": 'US',
    'Visions': 'VI',
    'Weatherlight': 'WL',
    'Worlds': 'WRL',
    'WotC Online Store': 'WOTC',
    'Zendikar': 'ZEN'}

rarity_abbrevs = {
    'Common': 'C',
    'Uncommon': 'UC',
    'Rare': 'R',
    'Special': 'S',
    'Mythic Rare': 'MR'}
