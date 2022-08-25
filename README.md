# A bot that automates the search for applications
## Бот що автоматизує пошук заявок


> Commands:
```ini
start - Знайомство
save_order - Створити заявку
find_by_phone - Шукати за номером телефону
find_by_name - Шукати за ім'ям
find_by_dob - Шукати за датою народження
find_by_address - Шукати за адресою
help - Докладний перелік можливостей
```

#### TODO:
- [ ] Implement `save_order` task
- [ ] Check that user belongs to NikoVoluneers
- [ ] Add search by name chunks, e.g. Захарче Володим Алекс
- [ ] Implement `CANCEL` command
- [ ] Improve search by address
- [ ] Parser fails on Names with ' sign in Ukrainian, e.g. В'юн В'ячеслав Дем'янович FIXME
7. PROFIT!!!111

#### Notes and thoughts
Search by address is far from ideal based on data we have.
So it is most realistic to search by street names with $regex.
That will generate many results (20 +)
    
1. Create mechanism for this < Вулиця + 16 + кв 5 >
    1. Searches within prev results

```
        result = search (Вулиця):
            # narrows the scope by adding house number
            search (16):
                # narrows the scope by adding house number
                search (кв 5):
                    ...
                    # exact result
```
    2. OR Add InlineKeyboard to create choosable address cards
        a) Update to latest version:
               `pip install python-telegram-bot==v20.0a2`
        b) Revrite the WHOLE APP accordingly :(
"""

 <!--
docker cp parsed_results.json mongodb:/tmp/parsed_results.json
docker exec mongodb mongoimport -d nikovolunteers -c orders --file /tmp/parsed_results.json --jsonArray

docker ps -a
docker exec -it mongodb bash

db.orders.find({"Phone": 680659203}).pretty()
db.orders.find({"Date": {$in: [/2022-08-03/]}}).count()

db.orders.find({"Cathegories": {$in : ["Пенсіонер"]}}).count()
db.orders.find({"PIB": {$in: ["Михеевич"]}}).pretty()
db.orders.find({"PIB": {$all: ["Владимир", "Васильевич"]}}).pretty()

db.orders.find({"Bday": {$in: [/5 лют 1987/]}}).count()
db.orders.find({"Bday": {$in: [/^5 лют/]}}).count()
db.orders.find({"Bday": {$in: [/^1942/]}}).count()
db.orders.find({"Bday": {$in: [/1942/]}}).count()

db.orders.find({"Address": {$in: [/Партизанской/]}}).count()
-->
