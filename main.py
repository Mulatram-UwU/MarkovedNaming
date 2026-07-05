import markov
gen=markov.model()
with open("datas.txt",encoding='utf-8') as f:
    gen.train(f.readlines())
for i in range(100):
    print(gen.run())