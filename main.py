import collections
from janome.tokenizer import Tokenizer
import csv

path = 'text.txt'
# path = 'botchan.txt'


class Blog(object):
    def __init__(self, text):
        self.pos_num = 0
        self.pos_counts = {}

    def get_pos_rates(self):
        pos_rates = {}
        for pos, count in self.pos_counts.items():
            pos_rates[pos] = count / self.pos_num
        return pos_rates


def get_text():
    with open(path) as f:
        text = f.read()
    return text


def create_blogs(text):
    blog = Blog(text)

    # 形態素解析
    pos_list = []
    for token in Tokenizer().tokenize(text):
        pos = token.part_of_speech.split(',')[0]
        base_pos = ('名詞', '助詞', '動詞', '助動詞', '副詞', '形容詞', '連体詞', '接頭詞', '接続詞', '感動詞')
        if pos in base_pos:
            pos_list.append(pos)
    blog.pos_num = len(pos_list)

    # 品詞 (pos) カウント
    blog.pos_counts = collections.Counter(pos_list)
    blog.pos_counts = dict(sorted(blog.pos_counts.items(), key=lambda x: -x[1]))
    return blog


def show_result(blog):
    print(get_text())
    print()
    print('総単語数 :', blog.pos_num)
    for pos, count in blog.pos_counts.items():
        pct = (count / blog.pos_num) * 100
        print('{}: {} ( {}% )'.format(pos, count, round(pct, 1)))


def export_csv(blog):
    with open('results.csv', 'w') as f:
        base_pos = ['名詞', '助詞', '動詞', '助動詞', '副詞', '形容詞', '連体詞', '接頭詞', '接続詞', '感動詞']
        header = ['id'] + base_pos
        writer = csv.DictWriter(f, header)

        pos_rates = blog.get_pos_rates()
        pos_rates['id'] = 'botchan'
        writer.writeheader()
        writer.writerow(pos_rates)


def main():
    text = get_text()
    blog = create_blogs(text)
    show_result(blog)
    # export_csv(blog)


if __name__ == '__main__':
    main()
