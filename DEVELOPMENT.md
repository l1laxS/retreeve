# Development Notes

This document tracks open development tasks, ideas for improvement, and clarifications about the design.

---

## ✅ Confirmed Design

- Handlers are **classes** that act both as recognizers and parsed object constructors.
  - `handler(line)` creates an instance **only if the line matches**.
  - The returned object is added to the `ParseTree`.
  - It must support `.feed(line)` for incremental parsing.
- `FallbackHandler(line)` creates a wrapped object when no other handler applies.
- `move_current_up()` in `HandlerTree` is currently unused and can be removed.
- `move_up_to()` in `ParseTree` is fine as-is — clear and effective.

---

## 🛠️ TODOs

### 1. Improve Handler Interface Clarity

- Define a base class (or document convention) for handlers:
  - Must be callable via constructor `handler(line)`
  - Must implement `.feed(line)`
  - Should raise if the line doesn't match, or return `None` to indicate no match

### 2. Set `parent` Links in `HandlerTree`

- Ensure all nodes in the `HandlerTree` have `.parent` set during initialization.
- This supports upward traversal (already assumed in `move_current_up()` and other places).

```python
# During tree init
for root in self.roots:
    root.parent = None
    self._link_parents(root)
```

### 3. Add Optional Debug Logging

- Log:
	- Which handler matches
	- When .feed() succeeds
	- When fallback is triggered
- Optional debug=True flag in Parser

### 4. Add Extensibility Hooks

- Add support for on_enter() / on_exit() on handlers:
	- Called when a node is entered or exited during parsing
- Consider pre-processing hooks (e.g., trim whitespace, ignore comments)
- Add error collection or line-tracking for invalid inputs
