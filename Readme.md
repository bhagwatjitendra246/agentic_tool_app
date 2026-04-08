**Setup**

conda create -n "venv" python=3.12.7

conda activate venv

git clone https://github.com/bhagwatjitendra246/agentic_tool_app.git

cd agentic_tool_app

pip install -r requirements.txt

**Run**
python app/main.py --query "Add 1 and 1, then multiply with 10, then subtract 0.5 from it, and add 4"
