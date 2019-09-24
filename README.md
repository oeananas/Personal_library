# Personal_library
Library project on Django

opportunities:
* add, edit and review authors
* add, edit and review books, current author books, current bookshelf books
* add, edit and review bookshelves
* change book's bookshelf or/and number on bookshelf

# Installation
```bash
pip3 install -r requirements.txt
cd library_project
./manage.py makemigrations library
./manage.py migrate
```
# Usage
```bash
./manage.py runserver
```
# Tests
```bash
py.test
```