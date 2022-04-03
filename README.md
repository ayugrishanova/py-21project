# py-21project
## Сравнение лексики различных СМИ по нескольним акторам
### План действий:
* Составляем 3 корпуса со статьями про каждого актора
* Работа с каждой статьей корпуса:
    * Предварительная обработка текста: 
         * удаление знаков пунктуации, лишних пробелов, табов и тп
         * токенизация
         * удаление стоп-слов
         * лемматизация с помощью модулей
    * Создание словаря частотности слов
    * Визуализация популярности слов в виде облака
    * Анализ биграмм и обращений к актору
* Определение окраски статей:
    * Скачивание заведомо гневных & заведомо доброжелательных статей/твитов 
    * Подсчет встречаемости слов => составление списка слов-маркеров эмоциональной окраски (_молодец_ заведомо доброе, _дурак_ заведомо злое)
    * Поиск слов-маркеров в статьях => определение окраски статей
* Определение тематики статей:
    * Анализ html-страниц статей: в какой раздел сайта редакторы отнесли статью?
        * для статей, где не указан раздел, следовать алгоритму определения окраски статей
* Доработка программы до user-friendly состояния
