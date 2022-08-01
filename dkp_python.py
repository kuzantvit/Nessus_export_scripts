import requests
import json
import time
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
response = requests.request("GET", url, headers=headers, verify=False)
print(response.text)
data = response.json()
scans_ids = []
scans_names = []
for i in range(len(data['scans')):
    scans_ids.append(data['scans'][i]['id'])
    if ('\\' or '/') in data['scans'][i]['name']:
        scan_name_ = data['scans'][i]['name'].replace('\\', "_").replace("/","_")
    else:
        scan_name_ = data['scans'][i]['name']
    scans_names.append(scan_name_)
j = 0
for i in scans_ids:
    url_export_request = "https://localhost:8834/scans/"+ str(i) +"/export"
    response_export = requests.request("POST", url_export_request, json=payload, headers=headers, verify=False)
    if "[404]" in response_export:
        continue
    time.sleep(40)
    
    file_id_json= response_export.json()
    file_id = file_id_json['file']
    url_export_download = "https://localhost:8834/scans/"+ str(i) +"/export/" + str(file_id) + "/download"
    response_download =  requests.request("GET", url_export_download, headers=headers, verify=False)
    
    
    file_name = "export_reports/"+ str(scans_names[j])
    file = open(str(file_name), "w")  
    file.write(response_download.text)
    file.close()
    time.sleep(1)
    j += 1




