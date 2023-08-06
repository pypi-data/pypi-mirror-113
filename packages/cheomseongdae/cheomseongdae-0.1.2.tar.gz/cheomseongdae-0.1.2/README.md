# 첨성대 (cheomseongdae)
Let's express the operating principles of Apache Spark interestingly and visually. I hope the process is more fun than the result.

# User Guide
- [https://cheomseongdae.github.io](https://cheomseongdae.github.io)
- [https://pypi.org/project/cheomseongdae](https://pypi.org/project/cheomseongdae)
```
pip install cheomseongdae
```

```
>>> cheomseongdae-ping
pong

>>> cheomseongdae-ping 10
ppppppppppong
```

# Developer Guide
## dockstring
- [https://cheomseongdae.github.io/docs.html](https://cheomseongdae.github.io/docs.html)

## build
```
python3 -m build
```

## install
- local
```
pip install cheomseongdae -I --no-index --find-links ./dist/
```

- git
```
pip install git+https://github.com/cheomseongdae/cheomseongdae.github.io.git
```

## deploy -> pypi
```
python3 -m twine upload --repository pypi dist/*
```

## deploy -> docs
```
mkodcs gh-deploy
```
