import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent/"12-tools"))
from tools import calculate

tests=[("2+2",calculate("2+2"),4),("6*7",calculate("6*7"),42)]
results=[{"test":a,"actual":b,"expected":c,"passed":b==c} for a,b,c in tests]
score=sum(x["passed"] for x in results)/len(results)
out={"score":score,"passed":sum(x["passed"] for x in results),"total":len(results),"tests":results}
Path(__file__).parent.joinpath("results.json").write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
