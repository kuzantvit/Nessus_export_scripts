#$headers.Add("content-type", "application/json")
add-type @"
    using System.Net;
    using System.Security.Cryptography.X509Certificates;
    public class TrustAllCertsPolicy : ICertificatePolicy {
        public bool CheckValidationResult(
            ServicePoint srvPoint, X509Certificate certificate,
            WebRequest request, int certificateProblem) {
            return true;
        }
    }
"@

[System.Net.ServicePointManager]::CertificatePolicy = New-Object TrustAllCertsPolicy
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$accesskey = 'placeholder'
$secretkey = 'placeholder'
$name_array = @()
function Get_scan_report {
	param (
		$string_id, $nameid
	)
$headers = @{}
#$headers.Add("Accept", "application/json")
#$headers.Add("Content-Type", "application/json")
$headers.Add("X-ApiKeys", "accessKey=$accesskey; secretKey=$secretkey")
#$headers.Add
Write-Output $string_id
$URL = $string_id
$body = @{'format'='html';'chapters'='vuln_by_plugin'}
try{
$response_file = Invoke-RestMethod -Uri $URL -Method POST -Headers $headers -Body $body
}
catch{
Write-Output "Ran into an issue: $PSItem"
}
Start-Sleep -s 79
$response_file_id = $response_file.file
$headers_d = @{}
#$headers.Add("Accept", "application/json")
#$headers.Add("Content-Type", "application/json")
$headers_d.Add("X-ApiKeys", "accessKey=$accesskey; secretKey=$secretkey")
#$headers.Add
$URL_d = $string_id + "/" + "$response_file_id" + "/download"
#$body = @{'format'='html'}
if ( $nameid -like '*/*')
{
$nameid = $nameid -replace "/", "_"
}
elseif ( $nameid -like '*\*')
{
$nameid = $nameid -replace "\\", "_"
}
Write-Output $nameid
$file_save = "Y:\Nessus\script_reports\report_" + "$nameid" + "_.html"
try{
$response_report = Invoke-RestMethod -Uri $URL_d -Method GET -Headers $headers_d | out-file $file_save
}
catch{
Write-Output "Ran into an issue: $PSItem"
}
}


$headers = @{} 
$headers.Add("X-ApiKeys", "accessKey=$accesskey; secretKey=$secretkey")
$URL = 'https://nessus_ip:8834/scans'
$response = Invoke-RestMethod -Uri $URL -Method GET -Headers $headers 
#ForEach ($var in $response.scans) { Write-Output $var.name}
$scans =@{}
ForEach ($var in $response.scans) {
$id_scan = $var.id
$nameid = $var.name
$scans.Add("$nameid", "https://nessus_ip:8834/scans/$id_scan/export")  #$scans.Values
$name_array += $nameid
}

ForEach ($item in $name_array) { Get_scan_report $scans.$item $item}
