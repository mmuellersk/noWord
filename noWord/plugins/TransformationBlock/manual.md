### <a name="manual"></a> Transformation block

Transforms one or up to 3 resources to new resources using the specified transformation algorithm.

Default transformation are defined in the following file:
[DefaultTransformation](../../../noWord/common/DefaultTransformation.py)

Custom transformation can be injected in sub project as decoartions.


| Key       |      Description      | Default |
|:----------|:--------------------- |:-------------- |
| type      | transformation                |        |
| input     | If this parameter is a string one resource is use as input for the transformation function. If this parameter is  list, all specified resources will be used for the transformation function.   |        |
| output    |  Name of the produced output resources.     |        |
| transformation    |  Name of the transformation function. A list of default transformations is implemented in the DefaultTransformation.py. Derived projects can add custom transformations.   |
| params    |  A dictionary of parameters for the transformation function. The function shall use these parameters in its implementation.       |  |

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
