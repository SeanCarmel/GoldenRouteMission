# GoldenRouteMission
Instructions for running the server:
1. Make sure all the required files are in the server folder:
• app.py
• requirements.txt

2. Open a terminal (in PyCharm: view\tool windows\terminal), execute the following commands in the following order:

cd server

python3 -m venv env

pip3 install -U pip virtualenv

virtualenv --system-site-packages -p python3 ./venv

venv\Scripts\activate

pip install -r requirements.txt

flask run --port=5001 --debug

Instructions for running the client:
1. Make sure there all the required files are in the client folder:
•	Index.html
•	package.json
•	vite.config.js
•	src folder with:
  •	App.vue
  •	main.js
  •	components folder (inside src folder) with:
    •	calculator.vue
  •	router folder (inside src folder) with:
    •	index.js

2. Open a new terminal (Ctrl+Shift+T), execute the following commands in the following order:

cd client

npm install

npm run dev

