# TODO

- [ ] Inspect CSV structure and decide which fields to keep per association
- [ ] Design indexing strategy to load association rows as context chunks
- [ ] Update `src/impl/indexer.py` to ingest CSV rows instead of generic documents
- [ ] Update `src/impl/datastore.py` to embed association records (concatenated fields)
- [ ] Review `src/impl/response_generator.py` prompt for association-specific answers
- [ ] Adapt evaluator (or create new one) to validate association answers once dataset exists
- [ ] Document new workflow in `README.md`
