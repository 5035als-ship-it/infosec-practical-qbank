"""src/q_*.txt(지문) + data.json(주제·정답·태그) → index.html"""
import json, re, glob, os, sys
here = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(here, 'data.json'), encoding='utf-8'))
full = {}
for f in sorted(glob.glob(os.path.join(here, 'q_*.txt'))):
    txt = open(f, encoding='utf-8').read()
    for blk in re.split(r'^@@ ', txt, flags=re.M)[1:]:
        qid, body = blk.split('\n', 1)
        full[qid.strip()] = body.strip()
missing = [q['id'] for q in data if q['id'] not in full]
if missing: sys.exit('지문 누락: ' + ', '.join(missing))
for q in data: q['full'] = full[q['id']]
js = 'window.QUESTIONS = ' + json.dumps(data, ensure_ascii=False) + ';'
tpl = open(os.path.join(here, 'template.html'), encoding='utf-8').read()
open(os.path.join(here, '..', 'index.html'), 'w', encoding='utf-8').write(tpl.replace('/*__DATA__*/', js.replace('</', '<\\/')))
print(len(data), 'questions built')
