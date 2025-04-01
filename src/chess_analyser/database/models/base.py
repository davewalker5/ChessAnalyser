"""
Declare module-level variables used by the chess analysis model. The following module-level variables are defined:

+----------+-----------------------------------------------------------------------------+
| **Name** | **Comments**                                                                |
+----------+-----------------------------------------------------------------------------+
| Base     | SQLAlchemy declarative base class for the other classes in the model        |
+----------+-----------------------------------------------------------------------------+
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
