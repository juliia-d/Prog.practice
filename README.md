# BlockProcessor з SQL сховищем 
У лабораторних роботах 2-6 реалізується система, яка читає вхідні дані про блоки та голоси з CSV або консолі, зберігає їх у SQLite, а потім обробляє чергу подій та будує правильний консенсусний ланцюжок блоків. Ланцюжок будується за правилом: блок додається тільки тоді, коли його номер view збігається з поточною довжиною ланцюжка і за цей блок вже є голос. Уся система має перевірку вхідних даних через Pydantic, працює через чергу подій у базі даних і може працювати постійно, обробляючи нові події в міру їх надходження.

## Загальна архітектура
```mermaid
flowchart TD
    CSV[CSV файл] -->|load_csv| Updater
    Console[Консольний ввід] -->|команди| Updater

    subgraph Updater [Оновлювач]
        U1[Читання рядків] --> U2[Вставка в BLOCKS/VOTES]
        U2 --> U3[INSERT INTO event_stream]
    end

    Updater --> DB[(SQLite БД)]
    Updater --> ES[(event_stream)]

    ES --> Processor[Періодичний процесор]
    DB --> Processor

    Processor --> P1[SELECT FROM event_stream WHERE processed=0]
    P1 --> P2[Для кожної події]
    P2 --> P3{Тип події}
    P3 -->|block| P4[Завантажити блок з BLOCKS]
    P3 -->|vote| P5[Завантажити голос з VOTES]
    P4 --> P6[Створити об'єкт Block]
    P5 --> P7[Створити об'єкт Vote]
    P6 --> CB[ChainBuilder]
    P7 --> CB
    CB --> P8[UPDATE event_stream SET processed=1]
    P8 --> Chain[Готовий ланцюжок блоків]

    style DB fill:#f9f,stroke:#333,stroke-width:2px
    style ES fill:#bbf,stroke:#333,stroke-width:2px
    style CB fill:#bfb,stroke:#333,stroke-width:2px
