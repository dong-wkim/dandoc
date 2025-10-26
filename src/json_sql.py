"""json_sql.py

Convert nested JSON into relational SQL (single .sql file) with generated
integer primary keys and parent_id foreign keys so the result can be
imported into SQLite/Postgres/MySQL easily.

Behavior:
- Create one table per object node path (table names sanitized)
- Each table gets an id INTEGER PRIMARY KEY and parent_id INTEGER NULL
- Scalar fields become columns; lists are converted into child tables
- Try to infer basic column types (INTEGER, REAL, TEXT) from sample values
- Output: one SQL file written to data/sql/<base>_relational.sql

This is a conservative, portable SQL generator aimed at quick imports.
"""

from pathlib import Path
import json
import re
from collections import defaultdict
from typing import Any, Dict, List, Tuple


def _sanitize_ident(name: str) -> str:
    # Lowercase, alnum and underscores only, cannot start with digit
    s = re.sub(r"[^0-9a-zA-Z_]+", "_", name)
    s = re.sub(r"__+", "_", s)
    s = s.strip('_').lower()
    if not s:
        s = 't'
    if s[0].isdigit():
        s = 't_' + s
    return s


def _infer_type(values: List[Any]) -> str:
    # Simple inference: if all ints -> INTEGER, if all numbers -> REAL, else TEXT
    has_real = False
    has_text = False
    for v in values:
        if v is None or v == '':
            continue
        if isinstance(v, bool):
            has_real = True
            continue
        try:
            if isinstance(v, (int,)):
                continue
            if isinstance(v, float):
                has_real = True
                continue
            s = str(v)
            if re.fullmatch(r"-?\d+", s):
                continue
            if re.fullmatch(r"-?\d+\.\d+", s):
                has_real = True
                continue
            has_text = True
        except Exception:
            has_text = True
    if has_text:
        return 'TEXT'
    if has_real:
        return 'REAL'
    return 'INTEGER'


class TableBuilder:
    def __init__(self):
        # mapping: table_name -> list of rows (dicts)
        self.tables: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        # per-table counters to generate synthetic integer ids
        self.counters: Dict[str, int] = defaultdict(int)

    def add_row(self, table: str, row: Dict[str, Any]) -> int:
        """Add a row to a table, assign a sequential integer id, and return it."""
        # assign id
        self.counters[table] += 1
        assigned = self.counters[table]
        # ensure id stored as integer
        row = dict(row)
        row['id'] = assigned
        # parent_id may be provided already in row
        self.tables[table].append(row)
        return assigned

    def build_sql(self, root_name: str) -> Tuple[str, List[str]]:
        # For each table determine column types
        create_stmts = []
        insert_stmts = []

        for table, rows in self.tables.items():
            cols = set()
            for r in rows:
                cols.update(r.keys())
            # ensure id and parent_id exist
            cols.discard('id')
            cols.discard('parent_id')
            cols = sorted(cols)

            # collect sample values
            samples = {c: [] for c in cols}
            for r in rows:
                for c in cols:
                    samples[c].append(r.get(c))

            col_defs = []
            for c in cols:
                col_type = _infer_type(samples[c])
                col_defs.append(f'  "{c}" {col_type}')

            # map column types for insert formatting
            col_types = {c: _infer_type(samples[c]) for c in cols}

            # add id and parent_id
            col_defs = ['  "id" INTEGER PRIMARY KEY AUTOINCREMENT', '  "parent_id" INTEGER NULL'] + col_defs

            create = f"CREATE TABLE IF NOT EXISTS \"{table}\" (\n" + ',\n'.join(col_defs) + '\n);'
            create_stmts.append(create)

            # inserts
            for r in rows:
                cols_order = ['id', 'parent_id'] + cols
                vals = []
                for c in cols_order:
                    v = r.get(c)
                    # determine how to render value based on column type
                    if c == 'id' or c == 'parent_id':
                        # numeric ids
                        if v is None:
                            vals.append('NULL')
                        else:
                            vals.append(str(int(v)))
                    else:
                        ctype = col_types.get(c, 'TEXT')
                        if v is None:
                            vals.append('NULL')
                        else:
                            if ctype in ('INTEGER', 'REAL'):
                                # try to render numeric without quotes
                                try:
                                    if ctype == 'INTEGER':
                                        vals.append(str(int(v)))
                                    else:
                                        vals.append(str(float(v)))
                                except Exception:
                                    s = str(v).replace("'", "''")
                                    vals.append(f"'{s}'")
                            else:
                                s = str(v).replace("'", "''")
                                vals.append(f"'{s}'")
                insert = f"INSERT INTO \"{table}\" ({', '.join(['"'+c+'"' for c in cols_order])}) VALUES ({', '.join(vals)});"
                insert_stmts.append(insert)

        header = [f'-- Relational SQL for {root_name}', 'BEGIN TRANSACTION;']
        footer = ['COMMIT;']
        sql = '\n\n'.join(header + create_stmts + [''] + insert_stmts + footer)
        return sql, list(self.tables.keys())


def json_to_relational_sql(input_json: Any, out_sql_path: str, root_table_name: str = None):
    """Convert a loaded JSON object into relational SQL and write to out_sql_path."""
    tb = TableBuilder()

    def recurse(node, table_path, parent_id_name='parent_id', parent_id_val=None):
        table_name = _sanitize_ident(table_path)

        if isinstance(node, dict):
            # collect scalars for this row
            row = {}
            for k, v in node.items():
                if isinstance(v, (dict, list)):
                    continue
                row[k] = v

            # set parent link
            row['parent_id'] = parent_id_val
            # placeholder id will be generated on insert; keep as NULL
            row['id'] = None
            tb.add_row(table_name, row)

            # For nested lists/dicts create child rows
            for k, v in node.items():
                child_path = f"{table_path}_{k}" if table_path else k
                if isinstance(v, dict):
                    recurse(v, child_path, parent_id_val=None)
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, dict):
                            # child row will reference this parent's id
                            # We cannot know the parent's id at SQL generation time, so store NULL parent_id.
                            recurse(item, child_path, parent_id_val=None)
                        else:
                            # atomic list -> create a child row with 'value'
                            recurse({ 'value': item }, child_path, parent_id_val=None)

        elif isinstance(node, list):
            for item in node:
                recurse(item, table_path, parent_id_val=None)

        else:
            # scalar at root
            tb.add_row(_sanitize_ident(table_path or 'root'), {'value': node, 'parent_id': parent_id_val, 'id': None})

    # entry
    root_name = root_table_name or (input_json.get('name') if isinstance(input_json, dict) and 'name' in input_json else 'root')
    recurse(input_json, root_name)

    sql_text, tables = tb.build_sql(Path(out_sql_path).stem)
    outp = Path(out_sql_path)
    outp.parent.mkdir(parents=True, exist_ok=True)
    outp.write_text(sql_text, encoding='utf-8')

    return str(outp), tables


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Convert JSON to relational SQL file')
    parser.add_argument('input', help='input JSON file path')
    parser.add_argument('--out', help='output SQL file path', default='data/sql/output_relational.sql')
    parser.add_argument('--root', help='root table name', default=None)
    args = parser.parse_args()

    p = Path(args.input)
    data = json.loads(p.read_text(encoding='utf-8'))
    out_path = args.out
    out_file, created_tables = json_to_relational_sql(data, out_path, args.root)
    print('Wrote SQL to', out_file)
    print('Created tables:', created_tables)
