import os
import re
import glob


BANNED_WORDS = [
    '仿佛', '犹如', '宛若', '如同', '一丝', '一抹', '些许', '几分', '隐约',
    '深吸一口气', '缓缓', '不禁', '微微', '轻轻', '淡淡',
    '眼中闪过', '嘴角勾起', '眉头微皱', '眉眼低垂', '瞳孔微缩',
    '心中一动', '心头一震', '心下了然', '心中暗道', '心底泛起', '不由得',
    '不容置疑', '不容置喙', '不易察觉', '显而易见', '毫无疑问', '不可否认',
    '坚定', '闪烁着光芒', '狡黠', '深邃', '凛冽', '冰冷',
    '不由自主', '情不自禁', '自然而然',
    '突然', '好像', '瞬间',
    '瓦解', '无名火', '往我心上捅刀子',
    '烦躁', '心烦意乱',
    '仿佛……一般', '犹如……一般', '宛若……一般', '仿佛能……一般',
    '眼中闪过一丝', '嘴角勾起一抹',
    '心中涌起一股', '心中涌起',
    '他不知道的是',
    '终于明白', '这才意识到',
    '他感到', '她感到', '他意识到', '她意识到',
    '他明白', '她明白', '他知道', '她知道',
    '这一刻', '这就是', '原来',
    '，带着', '带着一丝', '带着……',
    '声音不大，却带着',
    '不是……而是', '不是，而是',
    '梨花带雨', '如沐春风',
]


def count_chars_without_newlines(text):
    return len(text.replace('\n', '').replace('\r', ''))


def count_banned_word_hits(text, banned_words):
    total_hits = 0
    hits_detail = {}
    for word in sorted(banned_words, key=len, reverse=True):
        count = text.count(word)
        if count > 0:
            hits_detail[word] = count
            total_hits += count
    return total_hits, hits_detail


def classify_density(density):
    if density <= 5:
        return '轻度'
    elif density <= 15:
        return '中度'
    else:
        return '重度'


def main():
    banned_file = '/workspace/skills/story-deslop/references/banned-words.md'
    md_dir = '/workspace/林若男烽烟衡阳觅归人/正文'

    banned_words = set(BANNED_WORDS)
    print(f"共提取中文禁用词: {len(banned_words)} 个")
    print("禁用词列表（按字数排序）:")
    for w in sorted(banned_words, key=lambda x: (-len(x), x)):
        print(f"  [{w}]", end='')
    print("\n")

    md_files = sorted(glob.glob(os.path.join(md_dir, '*.md')))[:10]

    total_chars_all = 0
    total_hits_all = 0

    print("-" * 95)
    print(f"{'文件名':<38} {'字符数':>10} {'命中次数':>10} {'密度(次/千字)':>14} {'等级':>6}")
    print("-" * 95)

    top_hits_total = {}

    for md_file in md_files:
        filename = os.path.basename(md_file)
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()

        char_count = count_chars_without_newlines(content)
        hits, detail = count_banned_word_hits(content, banned_words)
        density = (hits * 1000 / char_count) if char_count > 0 else 0
        level = classify_density(density)

        total_chars_all += char_count
        total_hits_all += hits

        for w, c in detail.items():
            top_hits_total[w] = top_hits_total.get(w, 0) + c

        print(f"{filename:<38} {char_count:>10,} {hits:>10,} {density:>14.2f} {level:>6}")

    print("-" * 95)
    total_density = (total_hits_all * 1000 / total_chars_all) if total_chars_all > 0 else 0
    total_level = classify_density(total_density)
    print(f"{'合计':<38} {total_chars_all:>10,} {total_hits_all:>10,} {total_density:>14.2f} {total_level:>6}")
    print("-" * 95)

    print(f"\n密度等级参考: 轻度≤5, 中度6-15, 重度>15")

    print(f"\nTop 20 高频命中禁用词:")
    sorted_hits = sorted(top_hits_total.items(), key=lambda x: -x[1])[:20]
    for i, (w, c) in enumerate(sorted_hits, 1):
        print(f"  {i:>2}. [{w}]: {c} 次")


if __name__ == '__main__':
    main()
