# Серверный модуль приложения "StudentNotes"
<ul>
  <li><b>Исполнитель:</b> Ларин А.В.</li>
  <li><b>Группа:</b> М8О-203М-20</li>
  <li><b>Научный руководитель:</b> Ухов П.А.</li>
</ul>
Выполнено в рамках выпускной квалификационной работы на тему <b>«Микросервисное приложение "Ежедневник студента"»</b>.

### Структура проекта

Весь основной код сосредоточен [в данном модуле](https://github.com/justalgit/StudentNotes-Server/tree/master/main) (за исключением файла контроллера с URL-адресами: его можно найти [здесь](https://github.com/justalgit/StudentNotes-Server/blob/master/StudentNotesServer/urls.py)).

Директория [views](https://github.com/justalgit/StudentNotes-Server/tree/master/main/views) содержит код представлений - функций, обрабатывающих запросы.

Классы JSON-сериализаторов расположены [здесь](https://github.com/justalgit/StudentNotes-Server/blob/master/main/serializers.py).

Классы, описывающие сущности базы данных, представлены в [файле models.py](https://github.com/justalgit/StudentNotes-Server/blob/master/main/models.py).

[Файл с утилитами](https://github.com/justalgit/StudentNotes-Server/blob/master/main/utils/raw_query_utils.py) содержит функции с raw-SQL запросами.
