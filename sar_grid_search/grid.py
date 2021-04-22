from Trade_project.sar_grid_search.main.grid_search import f_klines_to_csv, grid_search

time_frame = ['30MINUTE', '1HOUR', '4HOUR']
for i in time_frame:
    csv_data = f_klines_to_csv('ONEUSDT', i)
    print(i)
    grid_search(csv_data)
