### <a name="manual"></a> Foreach block

Loads an external data from yaml, json, plist or xml files. Can load
either one file containing one list or several files in a specified folder.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      |  foreach                |  
| resource  |  key of the resource     |
| content   |  list of blocks to be applied for each item in resource,  {{current/_key_}} is replace with field of current item defined by _key_ |
| name      |  defines name for value field resolution     | current |
| keeptogether      |  Renders entire block as one, setting to False allows to render over more than one page (page break handling)     | True |
| keys      |  Fields to be processed     | all |



Example:
```YAML
- type        : foreach
  resource    : data01
  content     :
    - type    : text
      content : >
        {{current/field01}}

```

Back to [Documentation](../../../README.md#block_data)
