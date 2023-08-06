# pdcompare

Used to compare two pandas DataFrame objects to see how they changed.

```
pip install pdcompare
```
## Requirements
The DataFrames, must have the same index to compare correctly. An error will be thrown if the index data-types do not match, and a warning will be thrown if the index names are differnt.

## STEPS

Initialize and call the ```compare()``` method:
```py
from pdcompare.compare import Compare

compare_object = Compare(df1,df2)
compare_object.compare()
```

To get a dictionary of detailed data call:
```py
compare_object.output()
```