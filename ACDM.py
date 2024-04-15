#!/usr/bin/env python
# coding: utf-8
# Revision 1.0.5
# In[16]:


import re
import csv
import os


# In[28]:


def search_log_file_single(log_file_path, word1, word2):
    
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            if re.search(r'\bEVENT  : ClientManager::sendFplMessage client -clientMAHB- sessionId -\b', line):
                client_id_match = re.search(r'sessionId -(.*?)-', line)
                client_id = client_id_match.group(1)
                               
                    
                    
            # Using regular expression to check if both words are present in the line
            if re.search(fr'\b{word1}\b', line) and re.search(fr'\b{word2}\b', line):
                # Use regular expressions to extract required information
                date_time_match = re.search(r'\[(.*?)\]', line)
                session_id_match = re.search(r'sessionId -(.*?)-', line) 
                dep_rwy_match = re.search(r'DRW="(.*?)"', line)
                dep_seq_match = re.search (r'DSN="(.*?)"', line)
                eobt_match = re.search (r'EOBT="(.*?)"', line)
                cs_match = re.search (r'IDT="(.*?)"', line)
                pkb_match = re.search (r'PKB="(.*?)"', line)
                tobt_match = re.search (r'TOBT="(.*?)"', line)
                tsat_match = re.search (r'TSAT="(.*?)"', line)
                ttot_match = re.search (r'TTOT="(.*?)"', line)
                session_id = session_id_match.group(1)
                tobt_rx = ''
                asat = ''
                if client_id == session_id:


                

                    if date_time_match and session_id_match and dep_rwy_match and dep_seq_match and eobt_match and cs_match and pkb_match and tobt_match and tsat_match and ttot_match:
                        date_time = date_time_match.group(1)
                        date_time = date_time.split('.')[0]
      
                        drw = dep_rwy_match.group(1)
                        dsn = dep_seq_match.group(1)
                        eobt = eobt_match.group(1)
                        idt = cs_match.group(1)
                        pkb = pkb_match.group(1)
                        tobt = tobt_match.group(1)
                        tsat = tsat_match.group(1)
                        ttot = ttot_match.group(1)

                         

                        if eobt != '':
                            eobt1 = eobt[:8]
                            eobt2 = eobt[8:]
                            eobt = f'{eobt1} {eobt2}'
                            #eobt = eobt+'UTC'

                        if tobt != '':
                            tobt1 = tobt[:8]
                            tobt2 = tobt[8:]
                            tobt = f'{tobt1} {tobt2}'                        
                            #tobt = tobt+'UTC'

                        if tsat != '':
                            tsat1 = tsat[:8]
                            tsat2 = tsat[8:]
                            tsat = f'{tsat1} {tsat2}'                        
                            #tsat = tsat+'UTC'

                        if ttot != '':
                            ttot1 = ttot[:8]
                            ttot2 = ttot[8:]
                            ttot = f'{ttot1} {ttot2}'                         
                           # ttot = ttot+'UTC'
                        store_result(date_time, idt, dsn, eobt, tobt_rx, tobt, tsat, ttot, drw, pkb, asat)
                else:
                    print('Client Not Found')  
                    
            if re.search(fr'\bEVENT\b', line) and re.search(fr'\bFPLAODB\b', line) and re.search(fr'\b{word1}\b', line) and re.search(fr'\bTOBT\b', line):
                date_time_match = re.search(r'\[(.*?)\]', line)
                cs_match = re.search (r'IDT="(.*?)"', line)
                tobt_rx_match = re.search(r'TOBT="(.*?)"', line)
#                if date_time_match and cs_match and tobt_rx_match:
                date_time = date_time_match.group(1)
                date_time = date_time.split('.')[0]
                idt = cs_match.group(1)
                tobt_rx = tobt_rx_match.group(1)
                drw = ''
                dsn = ''
                eobt = ''
                pkb = ''
                tobt = ''
                tsat = ''
                ttot = ''
                asat = ''
                if tobt_rx != '':
                    tobt_rx1 = tobt_rx[:8]
                    tobt_rx2 = tobt_rx[8:]
                    tobt_rx = f'{tobt_rx1} {tobt_rx2}'
                        
                store_result(date_time, idt, dsn, eobt, tobt_rx, tobt, tsat, ttot, drw, pkb, asat)


            if re.search(fr'\bEVENT\b', line) and re.search(fr'\bFPLAODB\b', line) and re.search(fr'\b{word1}\b', line) and re.search(fr'\bRSC\b', line) and re.search(fr'\bAOBT\b', line):
                date_time_match = re.search(r'\[(.*?)\]', line)
                cs_match = re.search (r'IDT="(.*?)"', line)
                asat_rx_match = re.search(r'RSC="(.*?)"', line)
#                if date_time_match and cs_match and tobt_rx_match:
                date_time = date_time_match.group(1)
                date_time = date_time.split('.')[0]
                idt = cs_match.group(1)
                asat = asat_rx_match.group(1)
                tobt_rx = ''
                drw = ''
                dsn = ''
                eobt = ''
                pkb = ''
                tobt = ''
                tsat = ''
                ttot = ''
                if asat != '':
                    asat1 = asat[:8]
                    asat2 = asat[8:]
                    asat = f'{asat1} {asat2}'
                        
                store_result(date_time, idt, dsn, eobt, tobt_rx, tobt, tsat, ttot, drw, pkb, asat)

def store_result(date_time, idt, dsn, eobt, tobt_rx, tobt, tsat, ttot, drw, pkb, asat):
# Create a list with the extracted information
    data = [date_time, idt, dsn, eobt, tobt_rx, tobt, tsat, ttot, drw, pkb, asat]



    # Specify the CSV file path
    callsign = idt.split()
    callsign = callsign[0]
    #try: 
    #    date = eobt.split()
    #    date = date[0]
    #except:
    #    date = date
    csv_file_path = f'{callsign}_data.csv'
    #csv_file_path = f'{callsign}_{date}.csv'
    # Check if the file exists
    is_new_file = not os.path.isfile(csv_file_path)

    # Write the data to the CSV file
    with open(csv_file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)

        if is_new_file:
            header = ["Timestamp", "IDT", "DSN", "EOBT", "TOBT RX", "TOBT", "TSAT", "TTOT", "DRW", "PKB", "ASAT"]
            print(header)
            csv_writer.writerow(header)

        csv_writer.writerow(data)

        print(f"{data}")
        
def file_sort(cur_dir):

    files = os.listdir(cur_dir)
    file_time = [(file, os.path.getmtime(os.path.join(cur_dir, file))) for file in files]
    sort = sorted(file_time, key=lambda x: x[1], reverse=False)
    sorted_file = [file[0] for file in sort]    
    return sorted_file

                       
# In[32]:

log_path = os.getcwd() + '\\IOP\\'
sorted_files = file_sort(log_path)
word1 = input('Insert Callsign:')
word2 = 'FPLDREC'

# In[35]:



for log in sorted_files:
    print(log)
    search_log_file_single(log_path + log, word1, word2)



# In[ ]:


#time.sleep(5)
os.system("pause")

