import random
import jieba

class MarkovChainGenerator:
    def __init__(self):
        self.transition_dict = {}
        self.start_words = []

    def train(self, text):
        # 对文本进行分词
        words = list(jieba.cut(text))
        
        # 如果词数太少，直接返回
        if len(words) < 2:
            return
        
        # 第一个词作为可能的开头
        self.start_words.append(words[0])
        
        for i in range(len(words) - 1):
            current_word = words[i]
            next_word = words[i + 1]
            if current_word not in self.transition_dict:
                self.transition_dict[current_word] = []
            self.transition_dict[current_word].append(next_word)

    def generate_sentence(self, length=20):
        # 随机选择一个开始的词
        current_word = random.choice(self.start_words)
        sentence = [current_word]
        
        for _ in range(length - 1):
            # 如果不存在 transition 或下一词库为空，则重新开始
            if current_word not in self.transition_dict or len(self.transition_dict[current_word]) == 0:
                current_word = random.choice(self.start_words)
                sentence.append(current_word)
            else:
                next_word = random.choice(self.transition_dict[current_word])
                sentence.append(next_word)
                current_word = next_word
        
        return "".join(sentence)

if __name__ == "__main__":
    # 初始化
    generator = MarkovChainGenerator()
    
    # 读入语料库
    with open("xhs_corpus.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                generator.train(line)

    # 生成一条模拟小红书文案
    print(generator.generate_sentence(30))
