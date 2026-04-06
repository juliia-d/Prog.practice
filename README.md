# BlockProcessor з SQL сховищем (Лабораторні 2–6)

У лабораторних роботах 2-6 реалізується система, яка читає вхідні дані про блоки та голоси з CSV або консолі, зберігає їх у SQLite, а потім обробляє чергу подій та будує правильний консенсусний ланцюжок блоків. Ланцюжок будується за правилом: блок додається тільки тоді, коли його номер view збігається з поточною довжиною ланцюжка і за цей блок вже є голос. Уся система має перевірку вхідних даних через Pydantic, працює через чергу подій у базі даних і може працювати постійно, обробляючи нові події в міру їх надходження.

## Схема потоку даних

```mermaid
flowchart TD
    subgraph Джерела даних
        CSV[CSV файл]
        Console[Консольний ввід]
    end

    CSV -->|load_csv| Updater
    Console -->|команди| Updater

    subgraph Updater
        direction LR
        U1[Читання рядків] --> U2[Вставка в BLOCKS/VOTES]
        U2 --> U3[INSERT INTO event_stream]
    end

    Updater --> DB[(SQLite БД)]
    Updater --> ES[(event_stream)]

    subgraph BlockProcessor [Періодичний процесор]
        direction TB
        BP1[SELECT FROM event_stream WHERE processed=0] --> BP2{Для кожної події}
        BP2 -->|тип block| BP3[Завантажити блок з BLOCKS]
        BP2 -->|тип vote| BP4[Завантажити голос з VOTES]
        BP3 --> BP5[Створити об'єкт Block]
        BP4 --> BP6[Створити об'єкт Vote]
        BP5 --> CB[ChainBuilder]
        BP6 --> CB
        CB --> BP7[UPDATE event_stream SET processed=1]
    end

    ES --> BlockProcessor
    DB --> BlockProcessor

    CB --> Chain[Готовий ланцюжок блоків]

    style DB fill:#f9f,stroke:#333,stroke-width:2px
    style ES fill:#bbf,stroke:#333,stroke-width:2px
    style CB fill:#bfb,stroke:#333,stroke-width:2px
