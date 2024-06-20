from durable.lang import ruleset, when_all, m, post, get_host
import pandas as pd

# Define a ruleset for comparison rules
with ruleset('comparison_rules'):
    # Define a rule for checking if the row count of two dataframes is equal
    @when_all(m.rule == 'equal_row_count')
    def equal_rows(c):
        """
        Checks if the row count of the source and target dataframes is equal.

        If the row count is not equal, prints a validation failure message and sets the result to False.
        If the row count is equal, prints a validation success message and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if len(source) != len(target):
            print(f"Validation failed: Row count does not match (source: {len(source)}, target: {len(target)})")
            c.s.source_size = len(source)
            c.s.target_size = len(target)
            c.s.result = False
        else:
            print(f"Validation succeeded: Row count matches (source: {len(source)}, target: {len(target)})")
            c.s.source_size = len(source)
            c.s.target_size = len(target)
            c.s.result = True
        c.update(c.s)

    # Define a rule for checking if the rows of two dataframes match
    @when_all(m.rule == 'rows_match')
    def rows_match(c):
        """
        Checks if the rows of the source and target dataframes match.

        If the rows do not match, prints a message and sets the result to False.
        If the rows match, prints a message and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)

        if source.equals(target):
            print(f"Rows match between both source and target")
            c.s.source_size = len(source)
            c.s.target_size = len(target)
            c.s.result = True
        else:
            print(f"Rows do not match between both source and target")
            all = pd.concat([source, target])
            unique = all.drop_duplicates(subset=None, keep=False)
            c.s.source_size = abs(int(len(source) - len(unique)/2))
            c.s.target_size = len(target)
            c.s.result = False
        c.update

    # Define a rule for checking if a dataframe has any null values
    @when_all(m.rule == 'not_null')
    def not_null(c):
        """
        Checks if the target dataframe has any null values.

        If the dataframe has null values, prints a message and returns False.
        If the dataframe does not have null values, prints a message and returns True.

        Parameters:
        c (Context): The context object, which contains the target dataframe.
        """
        target = pd.DataFrame(c.m.target)
        if target.notnull().all().all():
            print(f"No Nulls")
            c.s.target_size = len(target)
            c.s.result = True
        else:
            print(f"Empty Values")
            c.s.target_size = len(target[target.isnull().any(axis=1)])
            c.s.result = False
        c.update