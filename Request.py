# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 09:41:11 2019

@author: Alejandro
"""

import json
import requests

headers = {"Authorization": "Bearer " + ACCESS_TOKEN}
para = {
        "title": "image_url.jpg",
        "parents": [{"id": "root"}, {"id": "### folder ID ###"}]
}
files = {
        "data": ("metadata", json.dumps(para), "application/json; charset=UTF-8"),
        "file": requests.get("image_url").content
}
response = requests.post("https://www.googleapis.com/upload/drive/v2/files?uploadType=multipart", headers=headers, files=files)

    return response