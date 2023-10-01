virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
touch records.py
echo -e 'txt = [""]\nmx = [""]\n\ndkim1 = [""]\ndkim2 = [""]\ndkim3 = [""]\n\ndmarc = [""]' >> records.py