## 2024-05-15 - Optimizing CSV Tail Reads
**Learning:** In backend operations (like Odoo service), reading the end of a large CSV file by converting the entire reader to a list (`list(reader)`) causes significant memory overhead and slowness for large files, creating an O(n) memory allocation.
**Action:** Always use `collections.deque(reader, maxlen=limit)` when only the last N rows of a large dataset/CSV are needed to maintain O(1) memory usage relative to file size.
