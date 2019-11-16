# Sample Data Generators and Validators

## Links

- [Online JSON Schema Validator](https://www.jsonschemavalidator.net/)

## Idea

Main aim is to prepare instruments which help to generate data like them came from a real Android/UAV device.
Also, there are classes to check the schema validity of producing samples.

### Main things

- There are JSON Schemas which reflects structure of expected JSON object (located in folder **schemas**)
- There are two types of datasets representing right and wrong payload (located in folder **payloads**)
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
