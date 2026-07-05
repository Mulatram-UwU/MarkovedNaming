import random

class model:
    def __init__(self):
        self.hashset=set()
    def train(self, datas: list[str]):
        # 去除换行符
        datas = [i.replace('\n', '') for i in datas]

        # 构建字符映射：0=开始，1=结束，字符从2开始编号
        ct = 2
        self.forward = {'\n': 1}      # 结束标记用'\n'，但索引为1
        self.backward = {1: '\n'}
        for seq in datas:
            for ch in seq:
                if ch not in self.forward:
                    self.forward[ch] = ct
                    self.backward[ct] = ch
                    ct += 1
            self.hashset.add(seq)

        # 状态空间：所有可能的(前前,前)组合，其中符号不包括结束标记(1)
        # 因此可用的符号索引为 0 和 2..ct-1，共 ct-1 个
        self.V_state = ct - 1          # 包括开始(0)和所有字符
        self.state_num = self.V_state * self.V_state
        self.col_num = ct              # 所有符号作为候选（0不会被选到）

        # 转移计数矩阵：行=状态，列=目标符号
        self.p = [[0] * self.col_num for _ in range(self.state_num)]

        # 训练：统计二阶转移
        for seq_str in datas:
            # 获取字符索引列表
            idx_list = [self.forward[ch] for ch in seq_str]
            # 序列前后补两个开始和一个结束
            seq = [0, 0] + idx_list + [1]
            # 遍历所有转移（t>=2 保证有前两个符号）
            for t in range(2, len(seq)):
                prevprev = seq[t-2]
                prev = seq[t-1]
                target = seq[t]

                # 将原始索引映射到状态空间中的索引（0..V_state-1）
                mapped_pp = 0 if prevprev == 0 else prevprev - 1
                mapped_p  = 0 if prev == 0 else prev - 1
                state_id = mapped_pp * self.V_state + mapped_p

                self.p[state_id][target] += 1

    def run(self):
        # 初始状态：两个开始标记
        prevprev = 0
        prev = 0
        s = ""

        while True:
            # 计算当前状态ID
            mapped_pp = 0 if prevprev == 0 else prevprev - 1
            mapped_p  = 0 if prev == 0 else prev - 1
            state_id = mapped_pp * self.V_state + mapped_p

            weights = self.p[state_id]

            # 如果该状态从未出现，则直接结束（或可改为随机字符）
            if sum(weights) == 0:
                target = 1   # 结束
            else:
                target = random.choices(range(self.col_num), weights=weights)[0]

            if target == 1:   # 遇到结束标记
                break

            # 输出字符
            s += self.backward[target]

            # 更新状态：滑动窗口
            prevprev, prev = prev, target
        if s in self.hashset:
            return self.run()
        self.hashset.add(s)
        return s