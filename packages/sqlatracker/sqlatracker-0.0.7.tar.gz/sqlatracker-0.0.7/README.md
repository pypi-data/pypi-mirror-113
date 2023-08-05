# sqlatracker
#### Inspired by django-field-history

![GitHub](https://img.shields.io/github/license/Ed-XCF/sqlatracker)
[![Build Status](https://travis-ci.org/Ed-XCF/sqlatracker.svg?branch=main)](https://travis-ci.org/Ed-XCF/sqlatracker)
[![codecov](https://codecov.io/gh/Ed-XCF/sqlatracker/branch/master/graph/badge.svg?token=J3HnAigB4J)](undefined)
![PyPI](https://img.shields.io/pypi/v/sqlatracker)

### Example
```python
from sqlalchemy import BigInteger, Column
from sqlalchemy.ext.declarative import as_declarative
from sqlatracker.field_tracker import FieldTracker


@as_declarative()
class Base:
    id = Column(BigInteger, primary_key=True, autoincrement=True)


class Example(Base):
    example_field_1 = Column(BigInteger)
    example_field_2 = Column(BigInteger)


FieldTracker.listen_for(
    Example.example_field_1,
    Example.example_field_2,
)
```

### Integrate with your metadata for alembic

```python
from sqlatracker.field_tracker import FieldTracker
from sqlatracker.utils import merge_metadata

target_metadata = merge_metadata(your_metadata, FieldTracker.metadata)
```
