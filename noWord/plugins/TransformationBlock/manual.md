### <a name="manual"></a> Transformation block

Transforms one or multiple resources to new a resource using the specified transformation algorithm.

Default transformation are defined in the following file:
[DefaultTransformation](../../../noWord/common/DefaultTransformation.py)

Custom transformation can be injected in sub project as decoartions.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      | transformation                |        |
| input     | If this parameter is a string one resource is use as input for the transformation function. If this parameter is  list, all specified resources will be used for the transformation function.   |        |
| output    |  Name of the produced output resources.     |        |
| transformation    |  The name (string) or a list of the transformation function(s). A list of default transformations is implemented in the DefaultTransformation.py. If a list of transfromation is given, these transformation are exeuted subsequently using the outout of the previous transformation as input. Derived projects can add custom transformations.   |
| params    |  A dictionary of parameters for the transformation function. The function shall use these parameters in its implementation. In case of multiple transformations, the params shall contain a list of dictionaries, one for each transformation. The order and number of this list shall match exactly the list of transformations.      |  |

Example:
```YAML
- type   : transformation
  input  : consumer_data
  output : consumer_short
  transformation: distinctFirstToken
  params:
    key      : Url
    seperator: '/'


- type     : transformation
  input    : memo_data
  output   : memo_data_10
  transformation :  slice
  params:
    start: 0
    end  : 10

- type           : transformation
  input          : delays_verif_id_check/orders
  output         : delays_verif_id_check_sort_20_number
  transformation :
    - sort
    - slice
    - autonumber
  params         :
    - key     : 'sub_waiting_sec'
      reverse : True
    - start : 0
      end   : 20
    - ''
```

Available transfomration shall be declared in the docInfo.yaml file of
each project.

Example:
```YAML
transformations:
  - distinctFirstToken
  - slice

```

Back to [Documentation](../../../README.md#block_data)
