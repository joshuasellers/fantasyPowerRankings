import metrics


def main():
    df = metrics.get_avg()
    print(df.head())


main()
