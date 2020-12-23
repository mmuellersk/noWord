### <a name="manual"></a> Resource block

Loads an external data from yaml, json, plist or xml files. Can load
either one file containing one list or several files in a specified folder.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      |  resource                |  
| alias     |  key of the resource<br/> this key is used to access the resource in other blocks     |
| filename  |  load single file (yaml, json, plist or xml)<br/> filename shall specify path to data file relative to source file  |
| folder    |  loads all files in this folder (yaml, json, plist or xml)<br/> folder shall specify path to data files relative to source file         |
| recursive |  only for folder key: loads files in folder recursively             | False |
| content   |  load data directly from text in source file        |
| sort      |  sorts data by specified column (max 3 fields for sorting)              |
| filter    |  applies filter to loaded data            |
| autonumber    |  adds number to each entry in resources data           | False |
| global    |  loads resource as global resource           | False |


Example:
```YAML
- type     : resource
  alias    : data01
  filename : ../../data.yaml

```

Back to [Documentation](../../../doc/block_types.md#data)
