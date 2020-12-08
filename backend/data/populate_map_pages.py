import csv
# Input CSV - map_Square_page; lowest_map_square; highest_map_square; top_right_lat; top_right_long; is_irregular
# Output CSV - map_square; top_right_lat; top_right_long

# Map Pages: (5 x 4)
# change in longitude: 0.01361302273 (width of map page)
# change in latitutde: 0.011179 (height of map page)
mp_delta_long = 0.01361302273
mp_delta_lat = 0.011179

# Map Squares:
# change in longitude: 0.00340325568 (width of map square)
# change in latitude: 0.0022358 (height of map square)
ms_delta_long = 0.00340325568
ms_delta_lat = 0.0022358

with open('Map_Page_Input.csv') as input:
    reader = csv.reader(input, delimiter=' ')
    output = open('Map_Page_Output.csv', 'w')
    with output:
        writer = csv.writer(output, delimiter=' ')
        writer.writerow(["map_square,top_right_lat,top_right_long"]) # Adds title columns
        for row in reader:
            row = row[0].split(',')  # Splits the row into an array of entries
            if row[-1] != 'FALSE':  # Skips the irregularly shaped map square pages + header
                continue

            # Pulls top right coordinate of map page
            top_right_lat = float(row[3])
            top_right_long = float(row[4])

            current_ms = int(row[1]) # Defines the current map square
            # Splits the map page into a 5 x 4 grid and assigns coordinates of map square by
            # referring to the changes in latitude and longitude within the grid


            # map pages are 5x4 row x col.
            # since we start at top right corner coordinate,
            # subtract incrementally larger values of y*ms_delta_lat (up to down)
            # subtract incrementally smaller values of x*ms_dela_long (left to right)
            for y in range(0, 5):
                current_ms_lat = top_right_lat - (y * ms_delta_lat)
                for x in range(3,-1, -1):
                    current_ms_long = top_right_long - (x * ms_delta_long)
                    current_ms_row = '{map_square},{tr_lat},{tr_lng}'.format(map_square = current_ms, tr_lat = current_ms_lat, tr_lng = current_ms_long)
                    current_ms += 1
                    writer.writerow([current_ms_row])
