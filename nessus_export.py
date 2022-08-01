import requests
import json
import time
import csv
url = "https://localhost:8834/scans"
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-ApiKeys":"accessKey=placeholder; secretKey=placeholder"
}
payload = {
    "format": "html",
    "chapters": "vuln_by_plugin"
}
payload_by_host = {
    "format": "html",
    "chapters": "vuln_by_host"
}

payload_by_csv ={"format":"csv"}

response = requests.request("GET", url, headers=headers, verify=False)
#print(response.text)
data = response.json()
scans_ids = []
scans_names = []
for i in range(len(data['scans'])):
    scans_ids.append(data['scans'][i]['id'])
    if '\\' in data['scans'][i]['name'] or "/" in data['scans'][i]['name']:
        scan_name_ = data['scans'][i]['name'].replace('\\', "_").replace("/","_")
    else:
        scan_name_ = data['scans'][i]['name']
    scans_names.append(scan_name_)

j = 0
for i in scans_ids:
    print(scans_names[j])
    url_export_request = "https://localhost:8834/scans/"+ str(i) +"/export"
    response_export = requests.request("POST", url_export_request, json=payload, headers=headers, verify=False)
    if "The requested file was not" in response_export.text:
        continue
    time.sleep(26)    
    file_id_json= response_export.json()
    file_id = file_id_json['file']
    url_export_download = "https://localhost:8834/scans/"+ str(i) +"/export/" + str(file_id) + "/download"
    response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    if "Report is still being generated" in response_download.text[5:60]:
       time.sleep(39)
       response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    else:
       pass
    file_name = "export_reports_by_plugin/"+ str(scans_names[j]) + ".html"
    file = open(str(file_name), "w")  
    file.write(response_download.text)
    file.close()
    time.sleep(2)
    j += 1

k = 0
for i in scans_ids:
    print(scans_names[k])
    url_export_request = "https://localhost:8834/scans/"+ str(i) +"/export"
    response_export = requests.request("POST", url_export_request, json=payload_by_host, headers=headers, verify=False)
    if "The requested file was not" in response_export.text:
        continue
    time.sleep(26)    
    file_id_json= response_export.json()
    file_id = file_id_json['file']
    url_export_download = "https://localhost:8834/scans/"+ str(i) +"/export/" + str(file_id) + "/download"
    response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    if "Report is still being generated" in response_download.text[5:60]:
       print("!!!!!!!!!!!!\n!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!")
       time.sleep(95)
       response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    else:
       pass
    file_name = "export_reports_by_host/"+ str(scans_names[k]) + ".html"
    file = open(str(file_name), "w")  
    file.write(response_download.text)
    file.close()
    time.sleep(2)
    k += 1

t=0
for i in scans_ids:
    print(scans_names[t])
    url_export_request = "https://localhost:8834/scans/"+ str(i) +"/export"
    response_export = requests.request("POST", url_export_request, json=payload_by_csv, headers=headers, verify=False)
    if "The requested file was not" in response_export.text:
        continue
    time.sleep(19)    
    file_id_json= response_export.json()
    file_id = file_id_json['file']
    url_export_download = "https://localhost:8834/scans/"+ str(i) +"/export/" + str(file_id) + "/download"
    response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    if "Report is still being generated" in response_download.text[5:60]:
       print("!!!!!!!!!!!!\n!!!!!!!!!!!!!!\n!!!!!!!!!!!!!!!!")
       time.sleep(25)
       response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    else:
       pass
    file_name = "export_reports_by_csv/"+ str(scans_names[t]) + "_temp.csv"
    file = open(str(file_name), "w")  
    file.write(response_download.text)
    file.close()
    time.sleep(1)
    input_file = file_name
    output_file = "export_reports_by_csv/"+ str(scans_names[t]) + ".csv"
    cols_to_remove = [8, 9, 10, 11, 12] # Column indexes to be removed (starts at 0)

    cols_to_remove = sorted(cols_to_remove, reverse=True) # Reverse so we remove from the end first
    row_count = 0 # Current amount of rows processed

    with open(input_file, "r") as source:
        reader = csv.reader(source)
        with open(output_file, "w", newline='') as result:
            writer = csv.writer(result)
            for row in reader:
              row_count += 1
              if "000" in str(row_count):
                print('\r{0}\n'.format(row_count), end='') # Print rows processed
              for col_index in cols_to_remove:
                del row[col_index]
              writer.writerow(row)
    os.remove(file_name)
    time.sleep(1)











