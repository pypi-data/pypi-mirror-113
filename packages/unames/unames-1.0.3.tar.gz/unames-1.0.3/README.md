# cnames
Generate username from the full name provided

## usage

```python
>>> import unames
>>> u = list()
>>> for i in range(50):
...     u.append(unames.gen_username("Mayank Jha"))
...
>>> print({el for el in u})
{'Mayank.Jha', 'Jha.Mayank', 'itz.Mayank', 'Mayank_Jha', '_.MayankxJha._', 'iam.Mayank', 'May466', 'itz_Mayank', '__Mayank.Jha__', 'May889', 'iam_Mayank', 'May870', 'Mayank._.Jha', 'Mayank.Jha__', 'M4y4nk_Jh4'}
```
