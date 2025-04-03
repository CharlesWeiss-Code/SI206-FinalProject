from csv_manipulation import *
import folium



def main():
    print("main")
    time_series_dict = get_time_series_dict(read_csv(CSV_PATH), 100)
    print(time_series_dict)



if __name__ == "__main__":
    main()