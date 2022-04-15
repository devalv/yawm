"""RandomGenerator with 1000 russian adjectives.

Adjectives source: https://gist.github.com/oboshto/07372c13b905a8789183ecb76f77eadb"""

from typing import FrozenSet

from coolname import RandomGenerator

adjectives: FrozenSet[str] = frozenset(
    {
        "Заброшенный",
        "Способный",
        "Абсолютный",
        "Академический",
        "Приемлемый",
        "Признанный",
        "Точный",
        "Кислый",
        "Акробатический",
        "Авантюрный",
        "Младенческий",
        "Плохой",
        "Мешковатый",
        "Токсичный",
        "Добрый",
        "Голый",
        "Бесплодный",
        "Основной",
        "Прекрасный",
        "Запоздалый",
        "Любимый",
        "Откровенный",
        "Собачий",
        "Беззаботный",
        "Осторожный",
        "Небрежный",
        "Кавернозный",
        "Очаровательный",
        "Сырой",
        "Опасный",
        "Щеголеватый",
        "Дерзкий",
        "Дорогой",
        "Ослепительный",
        "Смертельный",
        "Оглушительный",
        "Каждый",
        "Нетерпеливый",
        "Серьезный",
        "Восторженный",
        "Съедобный",
        "Образованный",
        "Сказочный",
        "Слабый",
        "Верный",
        "Известный",
        "Расплывчатый",
        "Гигантский",
        "Газообразный",
        "Щедрый",
        "Нежный",
        "Подлинный",
        "Волосатый",
        "Красивый",
        "Удобный",
        "Счастливый",
        "Жесткий",
        "Неприятный",
        "Ледяной",
        "Идеальный",
        "Идеалистический",
        "Идентичный",
        "Идиотский",
        "Праздный",
        "Невежественный",
        "Больной",
        "Незаконный",
        "Измученный",
        "Зазубренный",
        "Забитый",
        "Калейдоскопический",
        "Увлеченный",
        "Долговязый",
        "Большой",
        "Последний",
        "Прочный",
        "Законный",
        "Сумасшедший",
        "Великолепный",
        "Величественный",
        "Главный",
        "Мужской",
        "Чудесный",
        "Наивный",
        "Узкий",
        "Противный",
        "Естественный",
        "Непослушный",
        "Послушный",
        "Тучный",
        "Продолговатый",
        "Очевидный",
        "Случайный",
        "Маслянистый",
        "Вкусный",
        "Бледный",
        "Ничтожный",
        "Иссушенный",
        "Частичный",
        "Страстный",
        "Мирный",
        "Острый",
        "Ароматный",
        "Причудливый",
        "Квалифицированный",
        "Сияющий",
        "Оборванный",
        "Стремительный",
        "Редкий",
        "Недавний",
        "Безрассудный",
        "Прямоугольный",
        "Печальный",
        "Соленый",
        "Здравомыслящий",
        "Саркастический",
        "Сардонический",
        "Довольный",
        "Чешуйчатый",
        "Дефицитный",
        "Испуганный",
        "Душистый",
        "Научный",
        "Презрительный",
        "Колючий",
        "Тощий",
        "Второй",
        "Вторичный",
        "Подержанный",
        "Эгоистичный",
        "Самоуверенный",
        "Сентиментальный",
        "Болтливый",
        "Высокий",
        "Осязаемый",
        "Потрепанный",
        "Натянутый",
        "Утомительный",
        "Изобилующий",
        "Уродливый",
        "Окончательный",
        "Неудобный",
        "Необычный",
        "Заниженный",
        "Непревзойденный",
        "Вакантный",
        "Тщеславный",
        "Действительный",
        "Воинственный",
        "Теплый",
        "Сердечный",
        "Искривленный",
        "Расточительный",
        "Бдительный",
        "Заболоченный",
        "Водянистый",
        "Волнистый",
        "Глупый",
        "Ложный",
        "Активный",
        "Актуальный",
        "Замечательный",
        "Обожаемый",
        "Продвинутый",
        "Любящий",
        "Отягчающий",
        "Полезный",
        "Лучший",
        "Заколдованный",
        "Биоразлагаемый",
        "Укушенный",
        "Горький",
        "Черный",
        "Веселый",
        "Пухлый",
        "Круговой",
        "Классический",
        "Чистый",
        "Умный",
        "Порядочный",
        "Решающий",
        "Глубокий",
        "Беззащитный",
        "Оборонительный",
        "Неполноценный",
        "Определенный",
        "Восхитительный",
        "Эластичный",
        "Приподнятый",
        "Пожилой",
        "Электрический",
        "Элегантный",
        "Элементарный",
        "Эллиптический",
        "Смущенный",
        "Быстрый",
        "Фатальный",
        "Отеческий",
        "Благоприятный",
        "Страшный",
        "Бесстрашный",
        "Кошачий",
        "Женский",
        "Непостоянный",
        "Одаренный",
        "Давая",
        "Гламурный",
        "Вопиющий",
        "Сверкающий",
        "Радостный",
        "Вредный",
        "Безобидный",
        "Гармоничный",
        "Суровый",
        "Поспешный",
        "Ненавистный",
        "Преследующий",
        "Злополучный",
        "Неграмотный",
        "Прославленный",
        "Воображаемый",
        "Образный",
        "Безупречный",
        "Нематериальный",
        "Немедленный",
        "Необъятный",
        "Пылкий",
        "Ревнивый",
        "Нервный",
        "Ленивый",
        "Ведущий",
        "Лиственный",
        "Худой",
        "Массивный",
        "Зрелый",
        "Скудный",
        "Мучнистый",
        "Жалкий",
        "Мясистый",
        "Медицинский",
        "Посредственный",
        "Морской",
        "Аккуратный",
        "Нуждающийся",
        "Странный",
        "Официальный",
        "Старый",
        "Периодический",
        "Задорный",
        "Личный",
        "Надоедливый",
        "Пессимистичный",
        "Мелочный",
        "Фальшивый",
        "Физический",
        "Розовый",
        "Простой",
        "Сварливый",
        "Ежеквартальный",
        "Настоящий",
        "Реалистичный",
        "Разумный",
        "Красный",
        "Отражающий",
        "Царственный",
        "Регулярный",
        "Отдельный",
        "Безмятежный",
        "Призрачный",
        "Тенистый",
        "Мелкий",
        "Постыдный",
        "Бесстыдный",
        "Мерцающий",
        "Блестящий",
        "Шокирующий",
        "Дрянной",
        "Короткая",
        "Эффектный",
        "Пронзительный",
        "Застенчивый",
        "Тихий",
        "Шелковистый",
        "Соблазнительный",
        "Напряженный",
        "Прохладный",
        "Ужасный",
        "Потрясающий",
        "Вспыльчивый",
        "Неровный",
        "Незаконченный",
        "Непригодный",
        "Развернутый",
        "Несчастный",
        "Нездоровый",
        "Неважный",
        "Уникальный",
        "Ценный",
        "Банальный",
        "Переменная",
        "Обширный",
        "Бархатистый",
        "Богатый",
        "Усталый",
        "Перепончатый",
        "Крошечный",
        "Плакучий",
        "Весомый",
        "Желтый",
        "Усердный",
        "Агрессивный",
        "Проворный",
        "Взволнованный",
        "Мучительный",
        "Приятный",
        "Приоткрытый",
        "Встревоженный",
        "Тревожный",
        "Отчужденный",
        "Альтруистический",
        "Мягкий",
        "Пустой",
        "Мрачный",
        "Слепой",
        "Блаженный",
        "Синий",
        "Неуклюжий",
        "Загроможденный",
        "Грубый",
        "Холодный",
        "Красочный",
        "Бесцветный",
        "Колоссальный",
        "Общий",
        "Сострадательный",
        "Компетентный",
        "Полный",
        "Бредовый",
        "Требовательный",
        "Плотный",
        "Стоматологический",
        "Надежный",
        "Зависимый",
        "Описательный",
        "Подробный",
        "Решительный",
        "Посвященный",
        "Другой",
        "Украшенный",
        "Выдающийся",
        "Эмоциональный",
        "Очарованный",
        "Энергичный",
        "Просвещенный",
        "Огромный",
        "Грязный",
        "Законченный",
        "Первый",
        "Шелушащийся",
        "Яркий",
        "Кричащий",
        "Плоский",
        "Испорченный",
        "Славный",
        "Глянцевый",
        "Угрюмый",
        "Золотой",
        "Добродушный",
        "Изящный",
        "Здоровый",
        "Душевный",
        "Небесный",
        "Тяжелый",
        "Здоровенный",
        "Беспомощный",
        "Беспристрастный",
        "Несовершенный",
        "Невозмутимый",
        "Невежливый",
        "Важный",
        "Непрактичный",
        "Впечатлительный",
        "Впечатляющий",
        "Невероятный",
        "Совместный",
        "Весёлый",
        "Добросердечный",
        "Симпатичный",
        "Хромая",
        "Линейный",
        "Выложенный",
        "Кроткий",
        "Мелодичный",
        "Памятный",
        "Угрожающий",
        "Металлический",
        "Незначительный",
        "Отрицательный",
        "Соседний",
        "Новый",
        "Старомодный",
        "Оптимальный",
        "Оптимистичный",
        "Жалобный",
        "Игривый",
        "Плюшевый",
        "Уравновешенный",
        "Полированный",
        "Вежливый",
        "Политический",
        "Тошнотворный",
        "Ворчливый",
        "Раскаявшийся",
        "Удаленный",
        "Раскаивающийся",
        "Уважительный",
        "Ответственный",
        "Серебряный",
        "Аналогичный",
        "Упрощенный",
        "Грешный",
        "Шипящий",
        "Скелетный",
        "Сонный",
        "Тонкий",
        "Слизистый",
        "Скользкий",
        "Медленный",
        "Маленький",
        "Дымный",
        "Самодовольный",
        "Резкий",
        "Подлый",
        "Любопытный",
        "Толстый",
        "Жаждущий",
        "Тщательный",
        "Заботливая",
        "Изношенный",
        "Объединенный",
        "Неопрятный",
        "Несчастливый",
        "Неестественный",
        "Нереальный",
        "Почитаемый",
        "Мстительный",
        "Проверяемый",
        "Порочный",
        "Ухоженный",
        "Состоятельный",
        "Поношенный",
        "Мокрый",
        "Который",
        "Желтоватый",
        "Удивительный",
        "Честолюбивый",
        "Обильный",
        "Забавный",
        "Древний",
        "Ангельский",
        "Сердитый",
        "Анимированный",
        "Годовой",
        "Античный",
        "Смелый",
        "Костлявый",
        "Скучный",
        "Властный",
        "Бодрый",
        "Сложный",
        "Обеспокоенный",
        "Сознательный",
        "Внимательный",
        "Постоянный",
        "Обычный",
        "Приготовленный",
        "Цифровой",
        "Прилежный",
        "Тусклый",
        "Недалекий",
        "Непосредственный",
        "Катастрофический",
        "Дискретный",
        "Изуродованный",
        "Отвратительный",
        "Нелояльный",
        "Завистливый",
        "Равный",
        "Экваториальный",
        "Существенный",
        "Уважаемый",
        "Этический",
        "Эйфорический",
        "Хлипкий",
        "Легкомысленный",
        "Цветочный",
        "Пушистый",
        "Сосредоточенный",
        "Сильный",
        "Раздвоенный",
        "Формальный",
        "Покинутый",
        "Милостивый",
        "Великий",
        "Грандиозный",
        "Гранулированный",
        "Серый",
        "Отличный",
        "Жадный",
        "Зеленый",
        "Скрытый",
        "Хриплый",
        "Полый",
        "Домашний",
        "Нечистый",
        "Врожденный",
        "Несравненный",
        "Несовместимый",
        "Неполный",
        "Несущественный",
        "Несмываемый",
        "Неопытный",
        "Инфантильный",
        "Ликующий",
        "Узловатый",
        "Оживленный",
        "Одинокий",
        "Длинная",
        "Молочный",
        "Бессмысленный",
        "Мятный",
        "Скупой",
        "Заблудший",
        "Туманный",
        "Смешанный",
        "Следующий",
        "Хороший",
        "Шустрый",
        "Оранжевый",
        "Органический",
        "Злобный",
        "Бедный",
        "Популярный",
        "Дородный",
        "Шикарный",
        "Положительный",
        "Питьевой",
        "Мощный",
        "Бессильный",
        "Практичный",
        "Драгоценный",
        "Престижный",
        "Отталкивающий",
        "Вращающийся",
        "Окольцованный",
        "Спелый",
        "Общительный",
        "Твердый",
        "Жидкий",
        "Испанский",
        "Конкретный",
        "Захватывающий",
        "Сферический",
        "Пряный",
        "Пятнистый",
        "Бережливый",
        "Громовой",
        "Своевременный",
        "Тонированный",
        "Порванный",
        "Незрелый",
        "Бескорыстный",
        "Неприглядный",
        "Неустойчивый",
        "Невоспетый",
        "Несвоевременный",
        "Непроверенный",
        "Победоносный",
        "Злодейский",
        "Белый",
        "Злой",
        "Широкий",
        "Шаткий",
        "Дикий",
        "Желающий",
        "Увядший",
        "Ветреный",
        "Молодой",
        "Опасающийся",
        "Подходящий",
        "Арктический",
        "Засушливый",
        "Артистический",
        "Храбрый",
        "Хрупкий",
        "Краткий",
        "Бойкий",
        "Сломанный",
        "Коричневый",
        "Согласованный",
        "Дорогостоящий",
        "Учтивый",
        "Лукавый",
        "Сливочный",
        "Творческий",
        "Хрустящий",
        "Замаскированный",
        "Нечестный",
        "Далекий",
        "Отчетливый",
        "Искаженный",
        "Одурманенный",
        "Унылый",
        "Вечнозеленый",
        "Вечный",
        "Возвышенный",
        "Возбудимый",
        "Образцовый",
        "Удачливый",
        "Хилый",
        "Потертый",
        "Свободный",
        "Французский",
        "Частый",
        "Свежий",
        "Дружелюбный",
        "Пугающий",
        "Седой",
        "Валовой",
        "Заземленный",
        "Честный",
        "Почетный",
        "Заслуженный",
        "Обнадеживающий",
        "Гостеприимный",
        "Низший",
        "Бесконечный",
        "Неофициальный",
        "Невиновный",
        "Небезопасный",
        "Коварный",
        "Настойчивый",
        "Поучительный",
        "Рассудительный",
        "Сочный",
        "Знающий",
        "Долгосрочный",
        "Однобокий",
        "Громкий",
        "Милый",
        "Современный",
        "Скромный",
        "Влажный",
        "Чудовищный",
        "Монументальный",
        "Моральный",
        "Униженный",
        "Шумный",
        "Нормальный",
        "Примечательный",
        "Исходящий",
        "Диковинный",
        "Отдаленный",
        "Предыдущий",
        "Первичный",
        "Первозданный",
        "Частный",
        "Вероятный",
        "Продуктивный",
        "Прибыльный",
        "Сообразительный",
        "Жареный",
        "Крепкий",
        "Гнилой",
        "Круглый",
        "Скрипучий",
        "Стабильный",
        "Стойкий",
        "Окрашенный",
        "Несвежий",
        "Крахмалистый",
        "Звездный",
        "Крутой",
        "Липкий",
        "Стимулирующий",
        "Бурный",
        "Строгий",
        "Поразительный",
        "Полосатый",
        "Оглушающий",
        "Обученный",
        "Травматический",
        "Заветный",
        "Треугольный",
        "Хитрый",
        "Неиспользованный",
        "Нежеланный",
        "Громоздкий",
        "Неписаный",
        "Жестокий",
        "Виртуальный",
        "Добродетельный",
        "Видимый",
        "Крылатый",
        "Жилистый",
        "Мудрый",
        "Остроумный",
        "Деревянный",
        "Многословный",
        "Мирской",
        "Привлекательный",
        "Уполномоченный",
        "Автоматический",
        "Средний",
        "Осведомленный",
        "Игристый",
        "Бугристый",
        "Жизнерадостный",
        "Обременительный",
        "Занятый",
        "Критический",
        "Кривой",
        "Переполненный",
        "Культурный",
        "Кудрявый",
        "Цилиндрический",
        "Двойной",
        "Драматический",
        "Обвисший",
        "Сухой",
        "Тупой",
        "Возбужденный",
        "Дорогая",
        "Опытный",
        "Посторонний",
        "Секретный",
        "Вьющийся",
        "Морозный",
        "Замороженный",
        "Плодотворный",
        "Функциональный",
        "Смешной",
        "Суетливый",
        "Нечеткий",
        "Растущий",
        "Легковерный",
        "Унизительный",
        "Обидный",
        "Преднамеренный",
        "Внутренний",
        "Международный",
        "Бронированный",
        "Безответственный",
        "Раздражающий",
        "Зудящий",
        "Младший",
        "Малолетний",
        "Чокнутый",
        "Кошерный",
        "Низкий",
        "Лояльный",
        "Светящийся",
        "Комковатый",
        "Роскошный",
        "Горный",
        "Мутный",
        "Приглушенный",
        "Разноцветный",
        "Обыденный",
        "Затхлый",
        "Таинственный",
        "Ядовитый",
        "Онемевший",
        "Питательный",
        "Возмутительный",
        "Переваренный",
        "Просроченный",
        "Обрадованный",
        "Правильный",
        "Гордый",
        "Расчетливый",
        "Пунктуальный",
        "Фиолетовый",
        "Напористый",
        "Озадачивающий",
        "Донкихотский",
        "Насмешливый",
        "Королевский",
        "Резиновый",
        "Румяный",
        "Сельский",
        "Ржавый",
        "Изумительный",
        "Стильный",
        "Покоренный",
        "Покорный",
        "Сладкий",
        "Солнечный",
        "Поверхностный",
        "Высший",
        "Поддерживающий",
        "Устойчивый",
        "Стройный",
        "Потный",
        "Душный",
        "Доверчивый",
        "Правдивый",
        "Городской",
        "Используемый",
        "Бесполезный",
        "Использованный",
        "Живой",
        "Объемный",
        "Наихудший",
        "Стоящий",
        "Достойный",
        "Гневный",
        "Лазурный",
        "Бежевый",
        "Васильковый",
        "Голубой",
        "Темный",
        "Индийский",
        "Световой",
        "Салатовый",
        "Пурпурный",
        "Бордовый",
        "Оливковый",
        "Непрозрачный",
        "Персиковый",
        "Серебряный",
        "Бирюзовый",
        "Прозрачный",
    }
)


custom_name = RandomGenerator(
    {"all": {"number_of_words": 1, "type": "words", "words": list(adjectives)}}
)

random_name = custom_name.generate