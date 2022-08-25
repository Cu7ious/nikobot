// # Category
// # 575 records, results must match as close as possible
addresses = {
  "None": 0,

  "вул.": 189,
  "ул.": 2,
  "\nул.": 41,

  "вулиця": 2,
  "улица": 1,

  "Провулок": 9,
  "Переулок": 8,

  "пров.": 5,
  "пер.": 2,

  "Варваровка": 2,
  "Варварівка": 1,

  "Проспект": 28,
  "пр.": 13,

  "Площа": 1,
  "Очаковская": 6,
  "Московська": 1,
  "Озерна": 14,
  "Крылова": 8,
  "Казарского": 2,
  "Заречная": 1,

  "[n] слободская": 0,
  "\n📫": 0,
}

raw_addresses = 0;
i = 0;
for (k in addresses) {
  i = i + addresses[k];
  raw_addresses++;
}

recs = 575;
in_addresses = 575 - i;

addresses_accuracy = 100 - in_addresses / recs * 100;

console.log('Всього "сирих" адрес:', raw_addresses);
console.log('Категоризація можлива для відсотку заявок:', Number(addresses_accuracy.toFixed(2)), '%');
