# Welcome to the DAS Python package

The [Royal Netherlands Institute for Sea Research](https://www.nioz.nl) has its data management system to help scientists archive and access their data. This tool is called: **Data Archive System (DAS)** and this package is its Python client.

To install this package use the following command:

```powershell
    $ pip install daspython
```


# Contents

1. [Authentication](#authentication)
1. [Attributes](#attributes)
    * [AttributeService](#attributeservice)
      * [Get](#get-attribute)
1. [Entries](#entries)
    * [EntryService](#entryservice)
      * [Get All](#get-all-entries)
      * [Get](#get-entry)
      * [Get Entry By Code](#get-entry-by-code)      
      * [Get Entries Level](#get-entries-level)
      * [Create Entry](#create-entry)
      * [Update Entry](#update-entry)
      * [Delete Entry](#delete-entry)
1. [Searches](#searches)
    * [SearchService](#searchservice)
      * [Search Entries](#search-entries)

For more examples please take a look at our [automated test scripts](https://git.nioz.nl/ict-projects/das-python/-/tree/master/tests)

# Authentication

Use this class to authenticate and keep your token that will be needed to use with all other service classes.

##### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
from daspython.auth.authenticate import DasAuth

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    
```

</p>
</details>

# Attributes

The entry group used on DAS are called attributes. Each department has its way to organize; classify and define the relations between their entries.
For example the [MMB](https://www.nioz.nl/en/about/mmb) department uses the following attributes: MMB Fractions and MMB Samples.

## AttributeService

Class that has all methods needed to handle attributes.

### Get Attribute

This method is used to get an attribute based on the parameter: GetAttributeRequest.

You need to inform either one field: 

    - id
    - name or 
    - alias

##### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.attributes.attributeservice import AttributeService, GetAttributeRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

attribute_service = AttributeService(auth)    

request = GetAttributeRequest()
request.id = 55
response = attribute_service.get(request)
print(json.dumps(response, sort_keys=True, indent=4))
```

</p>
</details>

##### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
    "__abp": true,
    "error": null,
    "result": {   
        "alias": "cores",
        "deleterUserId": null,
        "description": null,
        "id": 55,
        "indexName": "das_dev.cores-20201016-071620",
        "isDeleted": false,
        "isExcelOperationsEnabled": true,
        "isShowEnvGraph": true,
        "name": "Core",
        "tableName": "Cores",
        "tenantId": 1
    },
    "success": true,
    "targetUrl": null,
    "unAuthorizedRequest": false
}
```

</p>
</details>

# Entries

An entry most of the time belongs to an attribute and is a set of data. If we could compare an entry is like a row in a table, each row has its columns/ values and entries has its fields and values.

## EntryService

Class that has all methods needed to handle entries.


### Get All

Gets all entries based on the parameter info sent to this method.

##### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService, GetAllEntriesRequest, GetEntryRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

service = EntryService(auth)    

request = GetAllEntriesRequest()
request.attributeid = 55
response = service.get_all(request)
print(json.dumps(response, sort_keys=True, indent=4))
```

</p>
</details>

##### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
    "__abp": true,
    "error": null,
    "result": {
        "items": [
            {
                "entries": [
                    {
                        "acronym": null,
                        "amountofchildren": 1,
                        "amountofparents": 1,
                        "code": "zb.b.3h",
                        "creationtime": "2019-06-24T14:52:04.093",      
                        "creatoruserid": 110,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 5.0,
                        "displayname": "-01-#01",
                        "enddepthincm": null,
                        "event": "a92ac8dd-2940-428b-a242-cec9ace3917a",
                        "id": "ed89706c-40e6-4ec5-b07b-b5dee56297be",   
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": "2021-07-08T07:03:20",  
                        "lastmodifieruserid": 47,
                        "lengthincm": 0.0,
                        "number": 1.0,
                        "numberalias": null,
                        "order": 224,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": null,
                        "storagelocation": null,
                        "storagelocationname": null,
                        "tenantid": 1,
                        "trackingnumber": 224
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.v1",
                        "creationtime": "2021-05-28T13:12:32.6376855",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-01GC#01",
                        "enddepthincm": null,
                        "event": "1aea4d98-6ff3-4a4d-abb9-2c5c4423fc18",
                        "id": "cbeef9d4-7877-4350-8983-2e58661afe77",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 810,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 810
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.2nb",
                        "creationtime": "2021-05-28T13:23:34.07475",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-02BC#01",
                        "enddepthincm": null,
                        "event": "86d96c12-3e2c-473a-a88a-ce4ee4b4a39f",
                        "id": "8479b20a-250a-4ee3-b8bf-d3ef06ef56e7",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 1477,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "19b87c8a-300c-4b9a-873c-5425bbd39f08",
                        "storagelocationname": "Unknown",
                        "tenantid": 1,
                        "trackingnumber": 1477
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.jzc",
                        "creationtime": "2021-05-28T13:48:04.9521265",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-02GC#01",
                        "enddepthincm": null,
                        "event": "61c60754-4e18-430c-a5ca-b5791969e5b9",
                        "id": "a5001d23-e1b2-4b87-8275-b8879b513622",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 2911,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 2911
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.5nb",
                        "creationtime": "2021-05-28T13:23:37.0279446",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-03BC#01",
                        "enddepthincm": null,
                        "event": "d7ff910b-7786-414a-b520-794d56ab8eca",
                        "id": "8e7ecb3a-2901-42ca-96ec-b5b5f8feefb1",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 1480,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 1480
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.6nb",
                        "creationtime": "2021-05-28T13:23:37.9967312",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-03BC#01",
                        "enddepthincm": null,
                        "event": "d80d55ae-00b6-465e-afcb-418076f584f5",
                        "id": "09c5fed3-6915-4a35-ad39-f8ab245db033",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 1481,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 1481
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.hzc",
                        "creationtime": "2021-05-28T13:48:04.0614839",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-03GC#01",
                        "enddepthincm": null,
                        "event": "fbe7cb1d-47a8-4c21-af7b-10b9258b2f97",
                        "id": "dbba315a-661b-4bcf-8597-93284d4af3a0",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 2910,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 2910
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.pzc",
                        "creationtime": "2021-05-28T13:48:09.8711384",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-04BC#01",
                        "enddepthincm": null,
                        "event": "fd835206-2437-4277-b6eb-c47928653550",
                        "id": "1ba2f566-78f5-4066-9d51-52766955e255",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 2916,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 2916
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.kzc",
                        "creationtime": "2021-05-28T13:48:05.8740167",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-04GC#01",
                        "enddepthincm": null,
                        "event": "6612d917-ce6a-41c5-9acb-b587dac0781c",
                        "id": "b99e5c6a-8310-4278-94f8-32eab1ee35cf",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 2912,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 2912
                    },
                    {
                        "acronym": null,
                        "amountofchildren": 3,
                        "amountofparents": 3,
                        "code": "zb.b.7nb",
                        "creationtime": "2021-05-28T13:23:38.98185",
                        "creatoruserid": 208,
                        "deleteruserid": null,
                        "deletiontime": null,
                        "description": null,
                        "diameterincm": 0.0,
                        "displayname": "64HA003-05BC#01",
                        "enddepthincm": null,
                        "event": "32597973-00bb-49df-a0b4-98459fe65918",
                        "id": "2714d540-71ed-4e27-b053-d5fa5282a68b",
                        "isdeleted": false,
                        "islocked": false,
                        "lastmodificationtime": null,
                        "lastmodifieruserid": null,
                        "lengthincm": null,
                        "number": 1.0,
                        "numberalias": "1",
                        "order": 1482,
                        "qtydigitalobjects": 0,
                        "startdepthincm": null,
                        "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                        "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                        "storagelocationname": "OCS-A00-KC3",
                        "tenantid": 1,
                        "trackingnumber": 1482
                    }
                ],
                "entryFields": [
                    {
                        "column": "qtydigitalobjects",
                        "copyFromParent": false,
                        "customData": null,
                        "description": null,
                        "displayName": "# Dig. Obj.",
                        "displayType": 4,
                        "id": "10518b51-a22c-4c02-80e8-00883b144b9d",
                        "inputType": 19,
                        "isClearedOnReuse": true,
                        "isMandatory": false,
                        "isPrintable": true,
                        "isReadOnly": false,
                        "isSearchable": true,
                        "isSortable": true,
                        "tenantId": 1,
                        "x": 1,
                        "y": 80
                    },
                    {
                        "column": "displayname",
                        "copyFromParent": false,
                        "customData": "{ \"readonly\": true,\"generatedFrom\":[\"event\",\"#\",\"number|{0:00}\"]}",
                        "description": "Name is created from: 'Event'#'Number'.",
                        "displayName": "Name",
                        "displayType": 4,
                        "id": "5ab98427-8bd8-4293-a97a-091f16456c6e",
                        "inputType": 1,
                        "isClearedOnReuse": false,
                        "isMandatory": false,
                        "isPrintable": true,
                        "isReadOnly": true,
                        "isSearchable": true,
                        "isSortable": true,
                        "tenantId": 1,
                        "x": 1,
                        "y": 10
                    },
                    {
                        "column": "creationtime",
                        "copyFromParent": false,
                        "customData": null,
                        "description": null,
                        "displayName": "Date created",
                        "displayType": 4,
                        "id": "0e3c1140-e7cf-4919-91cc-57ebaf2468c8",
                        "inputType": 3,
                        "isClearedOnReuse": false,
                        "isMandatory": false,
                        "isPrintable": false,
                        "isReadOnly": true,
                        "isSearchable": false,
                        "isSortable": false,
                        "tenantId": 1,
                        "x": 1,
                        "y": 90
                    },
                    {
                        "column": "code",
                        "copyFromParent": false,
                        "customData": null,
                        "description": null,
                        "displayName": "Code",
                        "displayType": 4,
                        "id": "062cc0a2-382c-45a8-8682-696a1883dfe5",
                        "inputType": 1,
                        "isClearedOnReuse": false,
                        "isMandatory": false,
                        "isPrintable": true,
                        "isReadOnly": true,
                        "isSearchable": true,
                        "isSortable": true,
                        "tenantId": 1,
                        "x": 1,
                        "y": 0
                    },
                    {
                        "column": "storagelocationname",
                        "copyFromParent": false,
                        "customData": null,
                        "description": null,
                        "displayName": "Storage Location",
                        "displayType": 4,
                        "id": "0b552995-73ce-484f-ba96-c2250f98e403",
                        "inputType": 1,
                        "isClearedOnReuse": false,
                        "isMandatory": false,
                        "isPrintable": false,
                        "isReadOnly": false,
                        "isSearchable": true,
                        "isSortable": false,
                        "tenantId": 1,
                        "x": 1,
                        "y": 85
                    },
                    {
                        "column": "startdepthincm",
                        "copyFromParent": false,
                        "customData": null,
                        "description": "Relative to sediment surface",
                        "displayName": "Start Depth in cm",
                        "displayType": 4,
                        "id": "60238d4e-ea68-440f-8d30-cddb9bbff12b",
                        "inputType": 10,
                        "isClearedOnReuse": true,
                        "isMandatory": false,
                        "isPrintable": true,
                        "isReadOnly": false,
                        "isSearchable": true,
                        "isSortable": true,
                        "tenantId": 1,
                        "x": 1,
                        "y": 40
                    },
                    {
                        "column": "enddepthincm",
                        "copyFromParent": false,
                        "customData": null,
                        "description": "Relative to sediment surface",
                        "displayName": "End Depth in cm",
                        "displayType": 4,
                        "id": "42711007-7533-4a81-a1cd-f106c433636e",
                        "inputType": 10,
                        "isClearedOnReuse": true,
                        "isMandatory": false,
                        "isPrintable": true,
                        "isReadOnly": false,
                        "isSearchable": true,
                        "isSortable": true,
                        "tenantId": 1,
                        "x": 1,
                        "y": 50
                    }
                ],
                "entryForm": null,
                "entryMenuInfo": {
                    "attributeAlias": "cores",
                    "attributeId": 55,
                    "description": "",
                    "id": "4caf71e3-8d17-4095-83d0-26d72008cd60",
                    "name": "Cores"
                }
            }
        ],
        "totalCount": 4607
    },
    "success": true,
    "targetUrl": null,
    "unAuthorizedRequest": false
}
```

</p>
</details>

### Get

Gets a single entry info.

##### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService, GetEntryRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

service = EntryService(auth)    

request = GetEntryRequest()
request.attributeid = 55
request.id = 'a5001d23-e1b2-4b87-8275-b8879b513622'
response = service.get(request)
print(json.dumps(response, sort_keys=True, indent=4))
```

</p>
</details>

##### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
    "__abp": true,
    "error": null,
    "result": {
        "entry": {
            "6": "[]",
            "acronym": null,
            "amountofchildren": 3,
            "amountofparents": 3,
            "attributeid": 55,
            "code": "zb.b.jzc",
            "creationtime": "2021-05-28T13:48:04.9521265",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "description": null,
            "diameterincm": 0.0,
            "displayname": "64HA003-02GC#01",
            "enddepthincm": null,
            "event": "61c60754-4e18-430c-a5ca-b5791969e5b9",
            "id": "a5001d23-e1b2-4b87-8275-b8879b513622",
            "isdeleted": false,
            "islocked": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "lengthincm": null,
            "number": 1.0,
            "numberalias": "1",
            "order": 2911,
            "qtydigitalobjects": 0,
            "startdepthincm": null,
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "tenantid": 1,
            "trackingnumber": 2911
        }
    },
    "success": true,
    "targetUrl": null,
    "unAuthorizedRequest": false
}
```

</p>
</details>

### Get Entry By Code

Gets an entry by its code.

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

service = EntryService(auth)    
service = EntryService(self._get_token())
response = service.get_entry_by_code('4.b.wcb')
print(json.dumps(response, sort_keys=True, indent=4))
```

</p>
</details>

##### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
  "result": {
    "entry": {
      "6": "[]",
      "id": "a10fb352-659f-4f9d-8ef6-7f37a5e160b3",
      "displayname": "64HA003-05GC",
      "order": 1174,
      "trackingnumber": 1174,
      "tenantid": 1,
      "description": null,
      "code": "4.b.wcb",
      "amountofchildren": 2,
      "amountofparents": 2,
      "acronym": null,
      "islocked": false,
      "creationtime": "2021-05-27T15:37:04.8651748",
      "creatoruserid": 208,
      "deleteruserid": null,
      "deletiontime": null,
      "isdeleted": false,
      "lastmodificationtime": null,
      "lastmodifieruserid": null,
      "startdate": null,
      "starttime": null,
      "contactperson": "info CoreBase",
      "enddate": null,
      "endtime": null,
      "device": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
      "deviceid": null,
      "samplingresolution": null,
      "recoverystation": null,
      "storagelocation": null,
      "qtydigitalobjects": 0,
      "airtemperature": null,
      "windforce": null,
      "precipitation": null,
      "lightcondition": null,
      "cloudcover": null,
      "winddirection": null,
      "latitude": null,
      "longitude": null,
      "castnumber": null,
      "station": "183d5e05-1153-4e8f-a17b-4d3e2a247039"
    }
  },
  "targetUrl": null,
  "success": true,
  "error": null,
  "unAuthorizedRequest": false,
  "__abp": true
}
Response headers
```

</p>
</details>

### Get Entries Level

Gets all entries based on the given paramenter, but also includes either the children/ parents of each entry returned. You can also specify how deep are the levels of relations. For example:

    Let's say that we have the following relations:

    Cruise --> Vessel --> Station

    The cruise is a parent of a Vessel that is an grandparent of a Station here we have 3 levels deep.

##### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService, GetEntryRelationsRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

service = EntryService(auth)    

request = GetEntryRelationsRequest()
request.attributeid = 55
request.deeplevel = 3
request.relationtype = 1
response = service.get_entries_level(request)
print(json.dumps(response, sort_keys=True, indent=4))
```

</p>
</details>

##### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
  "result": {
    "totalCount": 4607,
    "items": [
      {
        "entries": [
          {
            "id": "ed89706c-40e6-4ec5-b07b-b5dee56297be",
            "displayname": "-01-#01",
            "order": 224,
            "trackingnumber": 224,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.3h",
            "amountofchildren": 1,
            "amountofparents": 1,
            "acronym": null,
            "islocked": false,
            "creationtime": "2019-06-24T14:52:04.093",
            "creatoruserid": 110,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": "2021-07-08T07:03:20",
            "lastmodifieruserid": 47,
            "number": 1,
            "lengthincm": 0,
            "diameterincm": 5,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": null,
            "event": "a92ac8dd-2940-428b-a242-cec9ace3917a",
            "qtydigitalobjects": 0,
            "numberalias": null,
            "state": null,
            "storagelocationname": null,
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "a92ac8dd-2940-428b-a242-cec9ace3917a",
                    "displayname": "TataSteel-01NN-",
                    "order": 74,
                    "trackingnumber": 74,
                    "tenantid": 1,
                    "description": "Staal kern; Tata Steel PT_BF5",
                    "code": "4.b.kc",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2019-06-20T15:09:39.28",
                    "creatoruserid": 110,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": "2020-09-11T16:30:20.2243882",
                    "lastmodifieruserid": 47,
                    "startdate": "2019-06-20T15:02:32",
                    "starttime": "15:02:32",
                    "contactperson": "Piet Van Gaever",
                    "enddate": "2019-06-28T00:00:00",
                    "endtime": "00:00:00",
                    "device": "f50d85ad-29e6-4450-ae47-acf9301b3d88",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": "",
                    "station": "ed31ac2b-fe09-4ef0-99ed-204335843a1c",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "ed31ac2b-fe09-4ef0-99ed-204335843a1c",
                            "displayname": "TataSteel-01",
                            "order": 73,
                            "trackingnumber": 73,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.jc",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2019-06-20T15:01:54.953",
                            "creatoruserid": 110,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": 0,
                            "longitude": 1,
                            "waterdepth": 0,
                            "timeofarrival": "2019-06-21T15:00:12",
                            "timeofdeparture": "2019-06-20T15:00:12",
                            "identifier": 1,
                            "geographicalname": "Tata Steel",
                            "hourofdeparture": "15:00:12",
                            "hourofarrival": "15:00:12",
                            "cruise": null,
                            "alias": null,
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "f50d85ad-29e6-4450-ae47-acf9301b3d88",
                            "displayname": "None",
                            "order": 9,
                            "trackingnumber": 9,
                            "description": null,
                            "code": "5.b.l",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "NN",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "cbeef9d4-7877-4350-8983-2e58661afe77",
            "displayname": "64HA003-01GC#01",
            "order": 810,
            "trackingnumber": 810,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.v1",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:12:32.6376855",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "1aea4d98-6ff3-4a4d-abb9-2c5c4423fc18",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "1aea4d98-6ff3-4a4d-abb9-2c5c4423fc18",
                    "displayname": "64HA003-01GC",
                    "order": 1194,
                    "trackingnumber": 1194,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.hdb",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:37:40.9338132",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "547f4bfb-b9f2-47e0-bf27-1146bf3383fb",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "547f4bfb-b9f2-47e0-bf27-1146bf3383fb",
                            "displayname": "64HA003-01",
                            "order": 565,
                            "trackingnumber": 565,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.fu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:05.8849032",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.91,
                            "longitude": 106.17,
                            "waterdepth": 26,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 1,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "01",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                            "displayname": "Gravity corer",
                            "order": 6,
                            "trackingnumber": 6,
                            "description": null,
                            "code": "5.b.h",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "GC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "8479b20a-250a-4ee3-b8bf-d3ef06ef56e7",
            "displayname": "64HA003-02BC#01",
            "order": 1477,
            "trackingnumber": 1477,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.2nb",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:23:34.07475",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "19b87c8a-300c-4b9a-873c-5425bbd39f08",
            "event": "86d96c12-3e2c-473a-a88a-ce4ee4b4a39f",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "Unknown",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "86d96c12-3e2c-473a-a88a-ce4ee4b4a39f",
                    "displayname": "64HA003-02BC",
                    "order": 785,
                    "trackingnumber": 785,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.30",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:25:19.2968684",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "fb9603fa-4d21-49db-bd97-01432f418be5",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "72458585-6be1-4c89-9c38-3de82d2b33ca",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "72458585-6be1-4c89-9c38-3de82d2b33ca",
                            "displayname": "64HA003-02",
                            "order": 566,
                            "trackingnumber": 566,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.gu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:07.2773279",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.92,
                            "longitude": 106.17,
                            "waterdepth": 14.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 2,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "02",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "fb9603fa-4d21-49db-bd97-01432f418be5",
                            "displayname": "Box corer",
                            "order": 4,
                            "trackingnumber": 4,
                            "description": "",
                            "code": "5.b.f",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "BC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "19b87c8a-300c-4b9a-873c-5425bbd39f08",
                    "attributeid": 77,
                    "displayname": "Unknown",
                    "order": 10,
                    "trackingnumber": 10,
                    "description": null,
                    "code": "nc.b.m",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "a5001d23-e1b2-4b87-8275-b8879b513622",
            "displayname": "64HA003-02GC#01",
            "order": 2911,
            "trackingnumber": 2911,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.jzc",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:48:04.9521265",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "61c60754-4e18-430c-a5ca-b5791969e5b9",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "61c60754-4e18-430c-a5ca-b5791969e5b9",
                    "displayname": "64HA003-02GC",
                    "order": 1171,
                    "trackingnumber": 1171,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.tcb",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:36:59.3047467",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "72458585-6be1-4c89-9c38-3de82d2b33ca",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "72458585-6be1-4c89-9c38-3de82d2b33ca",
                            "displayname": "64HA003-02",
                            "order": 566,
                            "trackingnumber": 566,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.gu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:07.2773279",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.92,
                            "longitude": 106.17,
                            "waterdepth": 14.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 2,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "02",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                            "displayname": "Gravity corer",
                            "order": 6,
                            "trackingnumber": 6,
                            "description": null,
                            "code": "5.b.h",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "GC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "8e7ecb3a-2901-42ca-96ec-b5b5f8feefb1",
            "displayname": "64HA003-03BC#01",
            "order": 1480,
            "trackingnumber": 1480,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.5nb",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:23:37.0279446",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "d7ff910b-7786-414a-b520-794d56ab8eca",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "d7ff910b-7786-414a-b520-794d56ab8eca",
                    "displayname": "64HA003-03BC",
                    "order": 786,
                    "trackingnumber": 786,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.40",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:25:20.9843944",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "fb9603fa-4d21-49db-bd97-01432f418be5",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                            "displayname": "64HA003-03",
                            "order": 567,
                            "trackingnumber": 567,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.hu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:08.6523768",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.92,
                            "longitude": 106.18,
                            "waterdepth": 20.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 3,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "03",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "fb9603fa-4d21-49db-bd97-01432f418be5",
                            "displayname": "Box corer",
                            "order": 4,
                            "trackingnumber": 4,
                            "description": "",
                            "code": "5.b.f",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "BC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "09c5fed3-6915-4a35-ad39-f8ab245db033",
            "displayname": "64HA003-03BC#01",
            "order": 1481,
            "trackingnumber": 1481,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.6nb",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:23:37.9967312",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "d80d55ae-00b6-465e-afcb-418076f584f5",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "d80d55ae-00b6-465e-afcb-418076f584f5",
                    "displayname": "64HA003-03BC",
                    "order": 787,
                    "trackingnumber": 787,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.50",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:25:22.828167",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "fb9603fa-4d21-49db-bd97-01432f418be5",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                            "displayname": "64HA003-03",
                            "order": 567,
                            "trackingnumber": 567,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.hu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:08.6523768",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.92,
                            "longitude": 106.18,
                            "waterdepth": 20.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 3,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "03",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "fb9603fa-4d21-49db-bd97-01432f418be5",
                            "displayname": "Box corer",
                            "order": 4,
                            "trackingnumber": 4,
                            "description": "",
                            "code": "5.b.f",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "BC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "dbba315a-661b-4bcf-8597-93284d4af3a0",
            "displayname": "64HA003-03GC#01",
            "order": 2910,
            "trackingnumber": 2910,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.hzc",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:48:04.0614839",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "fbe7cb1d-47a8-4c21-af7b-10b9258b2f97",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "fbe7cb1d-47a8-4c21-af7b-10b9258b2f97",
                    "displayname": "64HA003-03GC",
                    "order": 1172,
                    "trackingnumber": 1172,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.ucb",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:37:01.2117412",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "2b3499c2-3498-46b1-9ed2-345bed6ef2c2",
                            "displayname": "64HA003-03",
                            "order": 567,
                            "trackingnumber": 567,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.hu",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:08.6523768",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.92,
                            "longitude": 106.18,
                            "waterdepth": 20.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 3,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "03",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                            "displayname": "Gravity corer",
                            "order": 6,
                            "trackingnumber": 6,
                            "description": null,
                            "code": "5.b.h",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "GC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "1ba2f566-78f5-4066-9d51-52766955e255",
            "displayname": "64HA003-04BC#01",
            "order": 2916,
            "trackingnumber": 2916,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.pzc",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:48:09.8711384",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "fd835206-2437-4277-b6eb-c47928653550",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "fd835206-2437-4277-b6eb-c47928653550",
                    "displayname": "64HA003-04BC",
                    "order": 788,
                    "trackingnumber": 788,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.60",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:25:24.6719464",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "fb9603fa-4d21-49db-bd97-01432f418be5",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "32acc9b3-0eea-4b5e-bb02-9cd827788c1d",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "32acc9b3-0eea-4b5e-bb02-9cd827788c1d",
                            "displayname": "64HA003-04",
                            "order": 568,
                            "trackingnumber": 568,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.ju",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:10.1055479",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.93,
                            "longitude": 106.18,
                            "waterdepth": 12,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 4,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "04",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "fb9603fa-4d21-49db-bd97-01432f418be5",
                            "displayname": "Box corer",
                            "order": 4,
                            "trackingnumber": 4,
                            "description": "",
                            "code": "5.b.f",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "BC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "b99e5c6a-8310-4278-94f8-32eab1ee35cf",
            "displayname": "64HA003-04GC#01",
            "order": 2912,
            "trackingnumber": 2912,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.kzc",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:48:05.8740167",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "6612d917-ce6a-41c5-9acb-b587dac0781c",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "6612d917-ce6a-41c5-9acb-b587dac0781c",
                    "displayname": "64HA003-04GC",
                    "order": 1173,
                    "trackingnumber": 1173,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.vcb",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:37:03.3060233",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "32acc9b3-0eea-4b5e-bb02-9cd827788c1d",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "32acc9b3-0eea-4b5e-bb02-9cd827788c1d",
                            "displayname": "64HA003-04",
                            "order": 568,
                            "trackingnumber": 568,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.ju",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:10.1055479",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.93,
                            "longitude": 106.18,
                            "waterdepth": 12,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 4,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "04",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "bf143258-cf0f-40aa-90c6-21d118d3fb08",
                            "displayname": "Gravity corer",
                            "order": 6,
                            "trackingnumber": 6,
                            "description": null,
                            "code": "5.b.h",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "GC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          },
          {
            "id": "2714d540-71ed-4e27-b053-d5fa5282a68b",
            "displayname": "64HA003-05BC#01",
            "order": 1482,
            "trackingnumber": 1482,
            "tenantid": 1,
            "description": null,
            "code": "zb.b.7nb",
            "amountofchildren": 3,
            "amountofparents": 3,
            "acronym": null,
            "islocked": false,
            "creationtime": "2021-05-28T13:23:38.98185",
            "creatoruserid": 208,
            "deleteruserid": null,
            "deletiontime": null,
            "isdeleted": false,
            "lastmodificationtime": null,
            "lastmodifieruserid": null,
            "number": 1,
            "lengthincm": null,
            "diameterincm": 0,
            "startdepthincm": null,
            "enddepthincm": null,
            "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
            "event": "32597973-00bb-49df-a0b4-98459fe65918",
            "qtydigitalobjects": 0,
            "numberalias": "1",
            "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
            "storagelocationname": "OCS-A00-KC3",
            "parents": [
              {
                "attribute": "Event",
                "entries": [
                  {
                    "6": "[]",
                    "id": "32597973-00bb-49df-a0b4-98459fe65918",
                    "displayname": "64HA003-05BC",
                    "order": 789,
                    "trackingnumber": 789,
                    "tenantid": 1,
                    "description": null,
                    "code": "4.b.70",
                    "amountofchildren": 2,
                    "amountofparents": 2,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-05-27T15:25:26.2256798",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "startdate": null,
                    "starttime": null,
                    "contactperson": "info CoreBase",
                    "enddate": null,
                    "endtime": null,
                    "device": "fb9603fa-4d21-49db-bd97-01432f418be5",
                    "deviceid": null,
                    "samplingresolution": null,
                    "recoverystation": null,
                    "storagelocation": null,
                    "qtydigitalobjects": 0,
                    "airtemperature": null,
                    "windforce": null,
                    "precipitation": null,
                    "lightcondition": null,
                    "cloudcover": null,
                    "winddirection": null,
                    "latitude": null,
                    "longitude": null,
                    "castnumber": null,
                    "station": "183d5e05-1153-4e8f-a17b-4d3e2a247039",
                    "attributeid": 27,
                    "parents": [
                      {
                        "attribute": "Station",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "183d5e05-1153-4e8f-a17b-4d3e2a247039",
                            "displayname": "64HA003-05",
                            "order": 569,
                            "trackingnumber": 569,
                            "tenantid": 1,
                            "description": null,
                            "code": "1.b.ku",
                            "amountofchildren": 1,
                            "amountofparents": 1,
                            "acronym": null,
                            "islocked": false,
                            "creationtime": "2021-05-20T16:44:11.5743544",
                            "creatoruserid": 208,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "latitude": -5.96,
                            "longitude": 106.18,
                            "waterdepth": 7.5,
                            "timeofarrival": null,
                            "timeofdeparture": null,
                            "identifier": 5,
                            "geographicalname": null,
                            "hourofdeparture": null,
                            "hourofarrival": null,
                            "cruise": "933929c4-c1f3-4f45-8dab-df4ce979681d",
                            "alias": "05",
                            "attributeid": 24,
                            "parents": []
                          }
                        ],
                        "level": 2
                      },
                      {
                        "attribute": "Device",
                        "entries": [
                          {
                            "6": "[]",
                            "id": "fb9603fa-4d21-49db-bd97-01432f418be5",
                            "displayname": "Box corer",
                            "order": 4,
                            "trackingnumber": 4,
                            "description": "",
                            "code": "5.b.f",
                            "amountofchildren": 0,
                            "amountofparents": 0,
                            "acronym": "BC",
                            "islocked": false,
                            "creationtime": "2020-09-18T09:13:31.313",
                            "creatoruserid": null,
                            "deleteruserid": null,
                            "deletiontime": null,
                            "isdeleted": false,
                            "lastmodificationtime": null,
                            "lastmodifieruserid": null,
                            "tenantid": 1,
                            "attributeid": 28,
                            "parents": []
                          }
                        ],
                        "level": 2
                      }
                    ]
                  }
                ],
                "level": 1
              },
              {
                "attribute": "Storage Location",
                "entries": [
                  {
                    "id": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "attributeid": 77,
                    "displayname": "OCS-A00-KC3",
                    "order": 5,
                    "trackingnumber": 5,
                    "description": null,
                    "code": "nc.b.g",
                    "amountofchildren": null,
                    "amountofparents": null,
                    "acronym": null,
                    "islocked": false,
                    "creationtime": "2021-07-06T11:05:03.5166667",
                    "creatoruserid": null,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "isdeleted": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "tenantid": 1,
                    "parents": []
                  }
                ],
                "level": 1
              }
            ]
          }
        ]
      }
    ]
  },
  "targetUrl": null,
  "success": true,
  "error": null,
  "unAuthorizedRequest": false,
  "__abp": true
}
```  

</p>
</details>

### Create Entry

Creates a new entry.

In orde to create a new entry you must inform it's attribute identifier:

```
request.entry = {
  'attributeid': 55
  ...
}
```

Do not inform the propery 'displayname' for auto-generated names.

Note that the `event` field has its identifier and not its name.

<details><summary><b>Click for more</b></summary>
<p>

```python
from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService, InsertRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')
auth.authenticate()

service = EntryService(auth)
request = InsertRequest()
request.entry = {
  'attributeid': 55,
  'event': 'e9a68051-b47a-4a93-b14a-63c2e0f49d26',
  'number': 1,
  'diameterincm': 100
}
response = service.create(request)
```
</p>
</details>

### Update Entry

Updates an entry.

In orde to update an entry you must inform it's attribute identifier and it's identifier:

```
request.entry = {
  'attributeid': 55,
  'id': 'd28cc83e-e4a2-43d3-aa60-acd61d3dbf9c'
  ...
}
```
Do not inform the propery 'displayname' for auto-generated names.

Inform only the fields that you would like to update.

<details><summary><b>Click for more</b></summary>
<p>

```python

from daspython.auth.authenticate import DasAuth
from daspython.services.entries.entryservice import EntryService, UpdateRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')
auth.authenticate()

service = EntryService(auth)

request = UpdateRequest()
request.entry = {
    'id': 'f41788d3-ebe2-4209-97eb-f5fb9058a68f',
    'diameterincm': 10,
    'attributeid': 55
}

response = service.update(request)        
```
</p>
</details>

### Delete Entry

Deletes an entry.

You just need to provide two arguments:

  * EntryId and entry's attribute id.

<details><summary><b>Click for more</b></summary>
<p>

```python

from daspython.auth.authenticate import DasAuth
from daspython.services.searches.searchservice import SearchEntriesRequest, SearchService
from daspython.services.entries.entryservice import EntryService, UpdateRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')
auth.authenticate()

service = EntryService(auth)               
response = service.delete_entry('d28cc83e-e4a2-43d3-aa60-acd61d3dbf9c', 55)
    
```
</p>
</details>

# Searches

The searches module will give a tool to find any type of entry on DAS.

## SearchService

Class that has all methods needed to search entries.


### Search Entries

Returns a list of entries based on the given parameter values.

#### Usage

<details><summary><b>Click for more</b></summary>
<p>

```python
import json
from daspython.auth.authenticate import DasAuth
from daspython.services.searches.searchservice import SearchService, SearchEntriesRequest

auth = DasAuth('DAS url', 'Your user name', 'Your password')

if (auth.authenticate()):
    print('You are connected ...')    

service = SearchService(auth)    

request = SearchEntriesRequest()
request.attributeid = 55
request.maxresultcount = 3
request.querystring='displayname(64*)'
response = service.search_entries(request)
print(json.dumps(response, sort_keys=True, indent=4))
```
</p>
</details>

#### Expected result

<details><summary><b>Click for more</b></summary>
<p>

```json
{
    "__abp": true,
    "error": null,
    "result": {
        "items": [
            {
                "entry": {
                    "acronym": null,
                    "amountofchildren": 3,
                    "amountofparents": 3,
                    "code": "zb.b.v1",
                    "creationtime": "2021-05-28T13:12:32.6376855",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "description": null,
                    "diameterincm": 0.0,
                    "displayname": "64HA003-01GC#01",
                    "enddepthincm": null,
                    "event": "1aea4d98-6ff3-4a4d-abb9-2c5c4423fc18",
                    "id": "cbeef9d4-7877-4350-8983-2e58661afe77",
                    "isdeleted": false,
                    "islocked": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "lengthincm": null,
                    "number": 1.0,
                    "numberalias": "1",
                    "order": 810,
                    "qtydigitalobjects": 0,
                    "startdepthincm": null,
                    "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                    "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "storagelocationname": "OCS-A00-KC3",
                    "tenantid": 1,
                    "trackingnumber": 810
                }
            },
            {
                "entry": {
                    "acronym": null,
                    "amountofchildren": 3,
                    "amountofparents": 3,
                    "code": "zb.b.2nb",
                    "creationtime": "2021-05-28T13:23:34.07475",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "description": null,
                    "diameterincm": 0.0,
                    "displayname": "64HA003-02BC#01",
                    "enddepthincm": null,
                    "event": "86d96c12-3e2c-473a-a88a-ce4ee4b4a39f",
                    "id": "8479b20a-250a-4ee3-b8bf-d3ef06ef56e7",
                    "isdeleted": false,
                    "islocked": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "lengthincm": null,
                    "number": 1.0,
                    "numberalias": "1",
                    "order": 1477,
                    "qtydigitalobjects": 0,
                    "startdepthincm": null,
                    "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                    "storagelocation": "19b87c8a-300c-4b9a-873c-5425bbd39f08",
                    "storagelocationname": "Unknown",
                    "tenantid": 1,
                    "trackingnumber": 1477
                }
            },
            {
                "entry": {
                    "acronym": null,
                    "amountofchildren": 3,
                    "amountofparents": 3,
                    "code": "zb.b.jzc",
                    "creationtime": "2021-05-28T13:48:04.9521265",
                    "creatoruserid": 208,
                    "deleteruserid": null,
                    "deletiontime": null,
                    "description": null,
                    "diameterincm": 0.0,
                    "displayname": "64HA003-02GC#01",
                    "enddepthincm": null,
                    "event": "61c60754-4e18-430c-a5ca-b5791969e5b9",
                    "id": "a5001d23-e1b2-4b87-8275-b8879b513622",
                    "isdeleted": false,
                    "islocked": false,
                    "lastmodificationtime": null,
                    "lastmodifieruserid": null,
                    "lengthincm": null,
                    "number": 1.0,
                    "numberalias": "1",
                    "order": 2911,
                    "qtydigitalobjects": 0,
                    "startdepthincm": null,
                    "state": "1cf9f0ec-ff90-4b8a-86f4-a4f89cb249b8",
                    "storagelocation": "230bfae0-d04e-4a39-9c13-8c162446a9fc",
                    "storagelocationname": "OCS-A00-KC3",
                    "tenantid": 1,
                    "trackingnumber": 2911
                }
            }
        ],
        "totalCount": 4295
    },
    "success": true,
    "targetUrl": null,
    "unAuthorizedRequest": false
}
```
</p>
</details>