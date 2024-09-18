import csv
import re
import os

def search_log(filePath):

# Initialize variables to track the block of interest
    block_started = False
    date_time = []
    rwy = []
    # Read the log data from the text file
    with open(filePath, 'r') as file:
        for line in file:
            if re.search(fr'\bcreateSequenceMessage\b', line) and block_started == False:
                block_started = True
            if block_started is True:
                if re.search(fr'\bcreateSequenceMessage\b', line):
                    date_time = re.search(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3}', line)
                    date_time = date_time.group(0) 
                    print(date_time)
                if re.search(fr'\bRunway\b', line):
                    rwy = re.search(r'Runway:(.*)', line)
                    rwy = rwy.group(1)
                    print(rwy)
                if re.search(r'\-Id', line):
                    if re.search(r'\bCAT:D', line):
                        lineSplit = line.split()
                        id = lineSplit[0]
                        id = id.split(':')
                        id = id[1]
                        cs = lineSplit[1]
                        cs = cs.split(':')
                        cs = cs[1]
                        cat = lineSplit[2]
                        cat = cat.split(':')
                        cat = cat[1]
                        wtc = lineSplit[3]
                        wtc = wtc.split(':')
                        wtc = wtc[1]
                        tobt = lineSplit[4]
                        tobt = re.search(r'\d{2}:\d{2}:\d{2}', tobt)
                        tobt = tobt.group(0)
                        tsat = lineSplit[5]
                        tsat = re.search(r'\d{2}:\d{2}:\d{2}', tsat)
                        tsat = tsat.group(0)
                        taxi = lineSplit[6]
                        taxi = taxi.split(':')
                        taxi = taxi[1]
                        ttot = lineSplit[7]
                        ttot =re.search(r'\d{2}:\d{2}:\d{2}', ttot)
                        ttot = ttot.group(0)
                        eta = ''
                        sta = ''
                        try:
                            remark = lineSplit[8] + lineSplit[9]
                        except:
                            remark = ''
                        store_result(date_time, rwy, id, cs, cat, wtc, tobt, tsat, taxi, ttot, eta, sta, remark)
                    else:
                        lineSplit = line.split()
                        id = lineSplit[0]
                        id = id.split(':')
                        id = id[1]
                        cs = lineSplit[1]
                        cs = cs.split(':')
                        cs = cs[1]
                        cat = lineSplit[2]
                        cat = cat.split(':')
                        cat = cat[1]
                        eta = lineSplit[3]
                        eta = re.search(r'\d{2}:\d{2}:\d{2}', eta)
                        eta = eta.group(0)
                        sta = lineSplit[4]
                        sta = re.search(r'\d{2}:\d{2}:\d{2}', sta)
                        sta = sta.group(0)
                        wtc = ''
                        tobt = ''
                        tsat = ''
                        taxi = ''
                        ttot = ''
                        store_result(date_time, rwy, id, cs, cat, wtc, tobt, tsat, taxi, ttot, eta, sta, remark)
            if re.search(fr'  o', line):
                block_started=False 
        
def file_sort(cur_dir):

    files = os.listdir(cur_dir)
    file_time = [(file, os.path.getmtime(os.path.join(cur_dir, file))) for file in files]
    sort = sorted(file_time, key=lambda x: x[1], reverse=False)
    sorted_file = [file[0] for file in sort]    
    return sorted_file

def store_result(date_time, rwy, id, cs, cat, wtc, tobt, tsat, taxi, ttot, eta, sta, remark):
    data = [date_time, rwy, id, cs, cat, wtc, tobt, tsat, taxi, ttot, eta, sta, remark]
    # Specify the CSV file path
    date = date_time.split()
    date = date[0]
    csv_file_path = f'{date}_DMAN_sequence.csv'
    # Check if the file exists
    is_new_file = not os.path.isfile(csv_file_path)

    # Write the data to the CSV file
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        if is_new_file:
            header = ["Timestamp", "Runway", "Sequence", "Callsign", "Category", "WTC", "TOBT", "TSAT", "TTOT", "ETA", "STA", "Remark"]
            print(header)
            csv_writer.writerow(header)

        csv_writer.writerow(data)

        print(f"{data}")
# print(os.getcwd()+'/LOG')
log_path = os.getcwd() +'/DMAN/LOG/'
print(log_path)
print(os.listdir(log_path))
sorted_files = file_sort(log_path)
for log in sorted_files:
    print(log)
    search_log(log_path + log)

