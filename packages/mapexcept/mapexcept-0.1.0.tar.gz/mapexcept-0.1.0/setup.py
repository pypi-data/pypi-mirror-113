from setuptools import setup

ld = \
"""
Recommended example usage
-------------------------
```python
import mapexcept

for i in mapexcept(int, ['1', '53', '-42', 'a', '33'])[ValueError]:
  print(i)

# 1
# 53
# -42
# 33
```
"""

setup(
    name='mapexcept',
    packages=["mapexcept"],
    version='0.1.0',
    author='Perzan',
    author_email='PerzanDevelopment@gmail.com',
    description="Exception? Just keep mapping.",
    install_requires=["onetrick~=2.1"],
    long_description=ld,
    long_description_content_type="text/markdown",
)