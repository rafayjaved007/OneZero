Clone the project

Create and activate 'virtual environment' according to your OS

Install requirements using following command
'pip install -r requirements.txt'

Go to the following directory
'one_zero_system'

Run the project using following command
'python manage.py runserver'


Api Call
http://localhost:8000/core/products/?offset=0
It will will return you first '100' products. To get next products, set 'offset=100' and so on
