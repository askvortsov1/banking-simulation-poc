kill -9 $(lsof -i:5000 -t)
export FLASK_DB_FILE=test.db
cd src
flask db upgrade
flask run &
cd .. && sleep 5 && py.test --pdb
rm -f src/test.db
