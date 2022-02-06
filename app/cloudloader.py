from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import imageio


class CloudLoader:
    def __init__(self, data_path):
        self._df = pd.read_csv(data_path)
        print("Load Data %d lines." % (self._df.size))

    @property
    def df(self):
        return self._df


def generate_cloud(df, max_words=200):
    frequencies = {}
    for word, count in df.head(max_words).values:
        frequencies[word] = float(count)
    mask = imageio.imread('./word_count/mask.png')

    wc = WordCloud(
        font_path="./word_count/OPPOSansH.ttf",
        max_words=max_words,
        background_color='white',
        mask=mask,
        scale=3,
        max_font_size=180,
        width=2000,
        height=1200,
    )
    word_cloud = wc.generate_from_frequencies(frequencies)
    word_cloud.to_file("wordcloud2.jpg")
    plt.imshow(word_cloud)
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    cl = CloudLoader('./word_count/word_frequency_male.csv')
    generate_cloud(cl.df)
