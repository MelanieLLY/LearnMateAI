# Manual debug scripts

Ad-hoc scripts used while developing quiz generation. They hit the real database and LLM API, so
they are kept out of `tests/` and are never collected by pytest.

Run them from `server/` so that `src` is importable:

```bash
python -m scripts.debug_generation
python -m scripts.debug_router
python -m scripts.scratch_api_test
python -m scripts.scratch_serialize
```
