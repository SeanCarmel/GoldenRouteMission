# GoldenRouteMission
הוראות להרצת השרת:
1.	ודאו שיש את כל הקבצים הנדרשים בתיקייה server:
•	app.py
•	requirements.txt

2.	פתחו טרמינל (view\tool windows\terminal), בצעו בו את הפקודות הבאות בסדר הבא:

cd server

python3 -m venv env

pip3 install -U pip virtualenv

virtualenv --system-site-packages -p python3 ./venv

venv\Scripts\activate

pip install -r requirements.txt

flask run --port=5001 --debug

הוראות להרצת הלקוח:
1.	ודאו שיש את הקבצים הנדרשים בתיקייה client:
•	Index.html
•	package.json
•	vite.config.js
•	תיקיית src שבה:
•	App.vue
•	main.js
•	תיקיית components בתוך תיקיית src שבה:
•	calculator.vue
•	תיקיית router בתוך תיקיית src שבה:
•	index.js

2.	פתחו טרמינל חדש (Ctrl+Shift+T), בצעו בו את הפקודות הבאות בסדר הבא:

cd client

npm install

npm run dev

