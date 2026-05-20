<div align="center">
<h1>Проект по сложностям</h1>
</div>

<div align="right">
<normall>Бирюков Илья, 2 курс Б05-424</normall>
</div>

## Проект:
* `project.pdf` - теоретическая часть проекта (пункты `a` и `b`)
* `./algo` - директория с алгоритмом и тестами
  * `alogrithm.py` - реализация алгоритма **EFFICIENT**
  * `tests.py` - тестирование алгоритма
    * `./tests` - данные для тестирования, взятые [отсюда](https://users.cecs.anu.edu.au/~bdm/data/graphs.html)
  * `analysis.pdf` - выводы о работе алгоритма на основе тестов (`tests_output.md`)    

## Запуск тестирования:
<font size=3, color=red>**Дисклеймер**</font>

Тесты могут долго запускаться, поэтому можете менять их количества в `./algo/tests.py`

###  Запуск тестов
1. Перейдите в папку `./algo`
2. Установите необходимые зависимости
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```
3. Запустите тесты
```bash
python3 tests.py
```
