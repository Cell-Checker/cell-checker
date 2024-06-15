from durable.lang import ruleset, when_all, m, post, get_host
import pandas as pd

with ruleset('comparison_rules'):
    @when_all(m.rule == 'equal_row_count')
    def equal_rows(c):
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if len(source) != len(target):
            print(f"Validation failed: Row count does not match (source: {len(source)}, target: {len(target)})")
            c.s.result = False
        else:
            print(f"Validation succeeded: Row count matches (source: {len(source)}, target: {len(target)})")
            c.s.result = True
        c.update(c.s)
    @when_all(m.rule == 'rows_match')
    def rows_match(c):
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if source.equals(target):
            print(f"Rows match between both source and target")
            c.m.result = True
        else:
            print(f"Rows do not match between both source and target")
            c.m.result = False
        c.s.update
    @when_all(m.rule == 'not_null')
    def not_null(c):
        target = pd.DataFrame(c.m.terget)
        if target.notnull:
            print(f"No Nulls")
            return True
        else:
            print(f"Empty Values")
            return False