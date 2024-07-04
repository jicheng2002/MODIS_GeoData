import os
import requests

# 你的txt文件路径
txt_file_path = r'D:\A-Projects\Urban Green Space\json\LAADS_query.2024-06-21T12_12_urls.txt'

# 下载文件的目标文件夹
download_dir = r'D:\A-Projects\Urban Green Space\HDF'

# Bearer Token
bearer_token = 'eyJ0eXAiOiJKV1QiLCJvcmlnaW4iOiJFYXJ0aGRhdGEgTG9naW4iLCJzaWciOiJlZGxqd3RwdWJrZXlfb3BzIiwiYWxnIjoiUlMyNTYifQ.eyJ0eXBlIjoiVXNlciIsInVpZCI6InBhcnJqaTIwMDIiLCJleHAiOjE3MjQxNTM2MzQsImlhdCI6MTcxODk2OTYzNCwiaXNzIjoiRWFydGhkYXRhIExvZ2luIn0.6eJVdNn65E0r36HAN-L0sE1gf2KO1aKePYUfDkV70FO4XCj82aesni0CmDp_Ak9DOrYR7eIxoddfeHgCwjtyCX4kkEPphn7auTRRhHU-P2EcQbINDY0mRczFDM0Rr077h150OUy0WUkNo3PLvGAuey6ZwSCdEPYAIpC6zNUYq5jxq4x1UYNMjB5XYPJrs7Qi6YnaA3-uKRYNnlIIOAO61D3efdBSuS2D1QVhprv09O3aDuPkMPwEjXOD1vXmuqrP_z0OqG3oq6ugwDAOPBY8V5FRjDDUU-GSM-Gz52cOcINWvcPMeKZ3M-zMG4Ysy7eHKlWqfMz2-zffA_w6S3aGoQ'  # 替换为你的Bearer Token

# 确保目标下载文件夹存在
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

# 读取txt文件中的所有URLs
with open(txt_file_path, 'r') as file:
    urls = [line.strip() for line in file if line.strip()]

# 下载每个URL指向的文件
for url in urls:
    try:
        print(f"Downloading {url}...")
        headers = {
            "Authorization": f"Bearer {bearer_token}"
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        file_name = os.path.join(download_dir, url.split('/')[-1])
        with open(file_name, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {url} to {file_name}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
