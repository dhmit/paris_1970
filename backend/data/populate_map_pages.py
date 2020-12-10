"""
populate_map_pages.py

Pulls from an input csv that details each map page's top right coordinates and
the map squares it contains

Creates and overwrites an output csv that details the top right coordinates of each map square

Input CSV fields:
    map_Square_page
    lowest_map_square
    highest_map_square
    top_right_lat
    top_right_long
    is_irregular

Output CSV fields:
    map_square
    top_right_lat
    top_right_long
"""

import csv


# Map Pages: (5 x 4)
# change in longitude: 0.01361302273 (width of map page)
# change in latitude: 0.011179 (height of map page)
mp_delta_long = 0.01361302273
mp_delta_lat = 0.011179

# Map Squares:
# change in longitude: 0.00340325568 (width of map square)
# change in latitude: 0.0022358 (height of map square)
ms_delta_long = 0.00340325568
ms_delta_lat = 0.0022358


def populate_map_pages():
    with open('map_page_input.csv', encoding='utf-8') as map_page_input_csv:
        reader = csv.reader(map_page_input_csv)
        output_rows = []

        for row in reader:
            if row[-1] != 'FALSE':  # Skips the irregularly shaped map square pages + header
                continue

            # Pulls top right coordinate of map page
            top_right_lat = float(row[3])
            top_right_long = float(row[4])

            # Defines the current map square (starting with the lowest map square on the page)
            current_map_square = int(row[1])

            # Splits the map page into a 5 x 4 grid and assigns coordinates of map square by
            # referring to the changes in latitude and longitude within the grid

            # Map pages are 5 x 4 grids
            # Since we start at top right corner coordinate,
            # subtract incrementally larger values of y*ms_delta_lat (up to down), and
            # subtract incrementally smaller values of x*ms_dela_long (left to right)
            for y in range(0, 5):
                current_ms_lat = top_right_lat - (y * ms_delta_lat)
                for x in range(3, -1, -1):
                    current_ms_long = top_right_long - (x * ms_delta_long)
                    current_ms_row = [current_map_square, current_ms_lat, current_ms_long]
                    current_map_square += 1
                    output_rows.append(current_ms_row)

    with open('map_page_output.csv', 'w', encoding='utf-8', newline='\n') as output_csv:
        writer = csv.writer(output_csv)
        writer.writerow(['map_square', 'top_right_lat', 'top_right_long'])  # add header
        for row in output_rows:
            writer.writerow(row)


if __name__ == '__main__':
    print('Producing map page output csv...')
    populate_map_pages()
    print('Done!')
