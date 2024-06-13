from durable.lang import *
import pandas as pd

with ruleset('comparison_rules'):
    @when_all(m.rule == 'equal_row_count')
    def equal_rows(c):
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if len(source) != len(target):
            print(f"Validation failed: Row count does not match (source: {len(source)}, target: {len(target)})")
        else:
            print(f"Validation succeeded: Row count matches (source: {len(source)}, target: {len(target)})")
    @when_all(m.rule == 'rows_match')
    def rows_match(c):
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if source.equals(target):
            print(f"Rows match between both source and target")
            return True
        else:
            print(f"Rows do not match between both source and target")
            return False