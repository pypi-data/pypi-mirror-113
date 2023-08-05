# spartan-py

Basic spartan protocol implementation as a python library.

```python
import spartan

res = spartan.get("spartan://mozz.us/echo", "hi")
while True:
	buf = res.read()
	if not buf:
		break
	sys.stdout.buffer.write(buf)
res.close()
```

Try it in the REPL:
```python
>>> import spartan
>>> req = spartan.Request("spartan.mozz.us")
>>> req
>>> <Request spartan.mozz.us:300 / 0>
>>> res = req.send()
>>> res
>>> 2 text/gemini
>>> res.read()
>>> [...]
>>> res.close()
```
