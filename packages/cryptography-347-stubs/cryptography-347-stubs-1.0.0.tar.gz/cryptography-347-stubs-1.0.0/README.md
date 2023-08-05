# cryptography-347-stubs

Backported type stubs for Python's [cryptography] package.

The unreleased `main` branch of cryptography has dozens of improvements to the
inline type hints. This package backports those improvements and re-exports
them as stubs, so you can stay on the latest stable release of `cryptography`
while still getting proper type hints.

The source from which these stubs were exported is available at
<https://github.com/benesch/cryptography/tree/347-stubs>.

## Usage

```
# requirements.txt
cryptography==3.4.7
cryptography-347-stubs==1.0.0
```

[cryptography]: https://github.com/pyca/cryptography.git
