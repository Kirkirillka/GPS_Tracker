# Sample Data Generators and Validators

## Links

- [Online JSON Schema Validator](https://www.jsonschemavalidator.net/)

## Idea

Main aim is to prepare instruments which help to generate data like them came from a real Android/UAV device.
Also, there are classes to check the schema validity of producing samples.

### Main things

- There is JSON Schema which represent a bare empty message with no payload - [valid_schema.json](valid_schema.json)
- There are two datasets representing valid samples ([correct_data.json](correct_data.json)) and invalid samples ([wrong_data.json](wrong_data.json))
- For sample generation, there is a special method of generating dictionaries from a dictionary mapping

So, let's suppose, we have the following mapping:

```python
        {
            "field1": function_to_generate1,
            "field2": function_to_generate2,
            "nested.field1": func3,
            "more.deep.field": func4
        }
```

This mapping trasform any key into a field for generating sample. The value for the field will be returned by
the corresponding value by key.

Nested fields can be represented by dots:

```python
field = "level.second.third.key"

mapped = {"level":
            {"second":
                {"third":
                    {
                        "key":somefunc
                    }
                }
            }
        }
        
accessed_field = mapped["level"]["second"]["third"]["key"]

```
