s='''# MarkovedNaming
![](https://count.himiku.com/@MarkovedNaming)\\
Generates non-existent english word to name your project, product, or company etc. using Markov Chain.\\
Some times, it may generate a word that already exists but not included in datas.txt, but most of the time it will generate a new word.
## Daily Generated Names
- '''
import sys
sys.path.append('.')
print(sys.path)
import markov
gen=markov.model()
with open("datas.txt",encoding='utf-8') as f:
    gen.train(f.readlines())
s+='- '.join([gen.run()+'\n' for i in range(100)])
print(s)
with open("./README.md","w",encoding="utf-8") as f:
    f.write(s)
