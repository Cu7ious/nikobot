import re


PHONES = []
PHONES_SET = {}

CATS = [
    ["Людина з інвалідністю", {"инвалид", "інвалід"}],
    ["Переселенці", {"переселенці", "впо"}],
    ["Багатодітна родина", {"многодетная", "багатодітна"}],
    ["Родини, що втратили годувальника",
     {"втратили годувальника"}],
    ["Один годувальник", {"один годувальник"}],
    ["Мати-одиначка", {"мама-одиночка", "мати-одиначка"}],
    ["Літні люди (75+)", {"літні люди (75+)"}],
    ["Пенсіонер", {"пенсіонер", "пенсионер"}]
]

ru = ["янв", "фев", "мар", "апр", "мая", "июн",
      "июл", "авг", "сен", "окт", "ноя", "дек"]
ua = ["січ", "лют", "бер", "квіт", "трав", "черв",
      "лип", "серп", "вер", "жов", "лист", "груд"]
_ua = ["січ", "лют", "бер", "кві", "тра", "чер",
       "лип", "сер", "вер", "жов", "лис", "гру"]


def find_order_number(t):
    no = r'#️⃣?№? ?\d* *?\n'
    result = re.search(no, t)
    if result:
        r = result.group()
        r = r.replace('#️⃣', '')
        r = r.replace('№', '')
        return int(r)
    return None


def find_categories(t):
    if len(t) > 0:
        categories = []
        for cat in CATS:
            for word in cat[1]:
                if t.lower().__contains__(word):
                    categories.append(cat[0])
                    break
        return categories
    return []


def is_selfpick(t):
    """"""
    keywords = ["самовивіз", "самовывоз"]
    for word in keywords:
        if t.lower().__contains__(word):
            return True

    return False


def find_phone(t):
    phone = r'(\+?\d{12})|\d{10}'
    result = re.search(phone, t)

    """
    +380971525053
       0971525053
    """
    if result:
        r = result.group()
        if len(r) > 10:
            r = r[2:]
        return int(r)
    return None


def find_address(t):
    """
    Patterns:
        [See comments below]

        [Won't match]
            1-я Госпитальная, 18
            6 слободская, 5а, кв.19
    """

    """
        Too generic, so words like match as well, which is wrong.
        But too cool to be simply forgotten

        📫 вул. Лазурна, 50А
        📫 ул. Вільна, 58
        📫 ул. Велика Морська, 58
        вул. Фаліївська, 40
        пров. Зоряний, 13
        пер. Рейдовый 9А
        вулиця Металургів, 15
        ул. Московська 50 квартира 13
        Очаковская 15
        Заречная, 54
        Московська 55 квартира 12
        Озерна 1 А кв 17
        Крылова, 38 б, кв.3
        6 слободская, 5а, кв.19
        Варваровка улица Партизанская дом 41
        Мастерская, 60/3, кв. 2
        вул. Героїв України, 18 кв. 36
        Миколаїв, Курортна 19, 24
    """
    addr = r'\n(📫{1} ?)?([а-яїієґ]+)?,? ?(((в?ул.?)|(пров.?)|(пер.?)|(вулиця)|(улица)) ?)?(\d{1,2})? ?[а-яїієґ]+( ?[а-яїієґ]+)?,? ?\d{1,4}(\/\d{1,2})? ?[абвгд]?(,? ?(квартира|кв.?)? ?\d{1,4})?'
    result = re.search(addr, t, flags=re.IGNORECASE)

    """
        📫 вул. Лазурна, 50А
        📫 ул. Вільна, 58
        📫 ул. Велика Морська, 58
        вул. Фаліївська, 40
        пров. Зоряний, 13
        пер. Рейдовый 9А
        пр. Мира 9а
        Пр.Богоявленський  26-А
        вулиця Металургів, 15
        ул. Московська 50 квартира 13
        Варваровка улица Партизанская дом 41
        вул. Героїв України, 18 кв. 36
        ул. Арх. Старова, 6б кв65
    """
    # without the first word
    addr = r'\n(📫{1} ?)?,? ?(((в?ул.?)|(пров.?)|(пер.?)|(пр.?)|(вулиця)|(улица)) ?)(\d{1,3})? ?[а-яїієґ]+\.?( ?[а-яїієґ]+)?,? {1,}?\d{1,3}(\/\d{1,2})?( |-)?[абвгд]?(,? ?(квартира|кв.?)? ?\d{1,3})?'
    result = re.search(addr, t, flags=re.IGNORECASE)

    if not result:
        """
            вулиця Металургів, 15
            Очаковская 15
            Заречная, 54
            Московська 55 квартира 12
            Озерна 1 А кв 17
            Крылова, 38 б, кв.3
            Мастерская, 60/3, кв. 2
            Миколаїв, Курортна 19, 24
            Потемкинська, 129в
        """
        # 143 chars
        addr = r'\n(📫{1} ?)?([а-яїієґ]+)?,? ?((\d{1,2}\bw)?(-[а|я])?) ?[а-яїієґ]+( ?[а-яїієґ]+)?,? ?\d{1,3}(\/\d{1,2})? ?[абвгд]?(,? ?(квартира|кв.?)? ?\d{1,3})?'
        result = re.search(addr, t, flags=re.IGNORECASE)

    if result:
        return result.group().replace("📫", "").lstrip()
    return None


def parse_year(t):
    """
    returns:
        str<YYYY> || False
    """
    y = r'\d{4}'
    y = re.search(y, t)
    if not y:
        return False
    y = y.group()
    if not y:
        return False

    return y


def parse_dob(t):
    """
    returns:
        str<DD Mon YYYY> || None
    """
    if not t:
        return None
    year = parse_year(t)
    if not year:
        return None

    t = t.split(year)

    for item in t:
        if not item:
            continue
        t = item
        break

    if t.__contains__('.'):
        # numeric
        t = t.strip().strip('.').split('.')

        if len(t) != 2:
            t = t[0].split(' ')

        day = int(t[0])
        mon = int(t[1])
        return f'{day} {ua[mon - 1]} {year}'
    else:
        # num + word || year only
        valid = set(t)
        if not valid.pop():
            # year only
            return f'{year}'

        num = r'\d{1,2}'
        num = re.search(num, t)
        if num:
            num = num.group()
        else:
            return None

        delim = len(num)
        day = int(t[:delim].strip())
        mon = t[delim:].strip()[:3]

        if mon in _ua:
            return f'{day} {ua[_ua.index(mon)]} {year}'
        if mon in ru:
            return f'{day} {ua[ru.index(mon)]} {year}'

    return None


def find_dob(t):
    """
    Patterns:
        <UA occurances>
         17 липня 1941
         01лютого1947
         26 серпня1958
         22листопада 1930

        <RU occurances>
         17 мая 1941
         01февраля1947
         26 августа1958
         22ноября 1930

        <DD.MM.YYYY>
         01.09.1970

        <YYYY.DD.MM>
         1985.13.04

        <D.MM.YYYY>
         1.09.1970

        <YYYY.DD.MM>
         1985.13.04

        <YYYY>
         1970
    Returns:
        None or [1936, 01.09.1970, ...]
    """
    # 01.09.1970 <DD.MM.YYYY>
    dob = r'(0[1-9]|[12][0-9]|3[01])[- \..](0[1-9]|1[012])[- \..](19|20)\d\d'
    result = re.search(dob, t)

    if not result:
        # 1.09.1970 <D.MM.YYYY>
        dob = r'([1-9]|[12][0-9]|3[01])[- \..](0[1-9]|1[012])[- \..](19|20)\d\d'
        result = re.search(dob, t)

    if not result:
        # 1985.13.04 <YYYY.DD.MM>
        dob = r'(19|20)\d\d\.(0[1-9]|[12][0-9]|3[01]).(0[1-9]|1[012])'
        result = re.search(dob, t)

    if not result:
        # RU text date <DD M YYYY> or <DDMYYYY>
        """ 17 мая 1941
            01февраля1947
            26 августа1958
            22ноября 1930
        """
        dob = r'(0?[1-9]|[12][0-9]|3[01]) ?(янв(?:аря)?|фев(?:раля)?|мар(?:та)?|апр(?:еля)?|мая|июн(?:я)?|июл(?:я)?|авг(?:уста)?|сен(?:тября)?|окт(?:ября)?|ноя(?:бря)?|дек(?:абря)?) ?(19|20)\d\d'
        result = re.search(dob, t)

    if not result:
        # UA text date <DD MM YYYY> or <DDMMYYYY>
        """ 17 липня 1941
            01лютого1947
            26 серпня1958
            22листопада 1930
        """
        dob = r'(0?[1-9]|[12][0-9]|3[01]) ?(січ(:?ня)?|лют(?:ого)?|бер(?:езня)?|квіт(?:ня)?|трав(?:ня)?|черв(?:ня)?|лип(?:ня)?|серп(?:ня)?|вер(?:есня)?|жовт(?:ня)?|груд(?:ня)?|лист(?:опада)?) ?(19|20)\d\d'
        result = re.search(dob, t)

    if not result:
        # 1970 <YYYY>
        dob = r'(19|20)\d\d'
        result = re.search(dob, t)

    if result:
        return result.group()
    return None


def find_pib(text):
    """
        ПІБ

        В'юн В'ячеслав Дем'янович
        Урова Олена Михайлівна
        ГЛУХИХ АННА АЛЕКСЕЕВНА
        Заяц А.О
    """
    text = str(text)
    text = text.replace('Ё', 'Е')
    text = text.replace('ё', 'е')
    text = re.sub(r'\s+', ' ', text)  # removes double spaces
    name = None

    # ЇІЄҐ' їієґ'
    pattern = r"((\b[А-ЯЇІЄҐ][^А-ЯЇІЄҐ\s\.\,][а-яїієґ']*)(\s+)([А-ЯЇІЄҐ][а-яїієґ']*)(\.+\s*|\s+)([А-ЯЇІЄҐ][а-яїієґ']*))"

    name = re.findall(pattern, text)
    if name:
        PIB = name[0][0].replace('.', ' ')
        PIB = re.sub(r'\s+', ' ', PIB).split(' ')
        if len(PIB) >= 3:
            return PIB[0], PIB[1], PIB[2]
        elif len(PIB) == 2:
            return PIB[0], PIB[1], None
        elif len(PIB) == 1:
            return PIB[0], None, None
    else:
        return None, None, None


collection = []


def parse_msg_for_record(data):
    if data:
        record = {}

        date = data["date"]
        # f'{date:%Y-%m-%d}T{date:%H:%M:%S}+00:00'
        fmtdate = f'{date:%Y-%m-%d}T{date:%H:%M:%S}+00:00'

        record["Date"] = fmtdate
        record["OrderNumber"] = find_order_number(data["text"])
        record["PIB"] = find_pib(data["text"])
        record["Bday"] = parse_dob(find_dob(data["text"]))
        record["Phone"] = find_phone(data["text"])
        record["Address"] = find_address(data["text"])
        record["Categories"] = find_categories(data["text"])
        record["SelfPickup"] = is_selfpick(data["text"])
        record["RawMessage"] = data["text"]
        # print(record)

        return record
