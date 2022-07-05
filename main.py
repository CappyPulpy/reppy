import upload
import make_csv
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def main():
    make_csv.construct_df().to_csv("books.csv")
    upload.upload_csv()


if __name__ == '__main__':
    main()
