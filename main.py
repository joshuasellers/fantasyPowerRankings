import metrics
import rankandwrite
import sys


def main():
    rankandwrite.give_ranking(sys.argv[1])
    df = metrics.get_avg()
    print(df.head())
    print(metrics.get_request({}).json())


main()
