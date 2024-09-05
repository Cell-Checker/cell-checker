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
            c.s.result = False
        else:
            print(f"Validation succeeded: Row count matches (source: {len(source)}, target: {len(target)})")
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
            c.s.result = True
        else:
            print(f"Rows do not match between both source and target")
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
            c.s.result = True
        else:
            print(f"Empty Values")
            c.s.result = False
        c.update

    @when_all(m.rule == 'rows_not_in_target')
    def not_in_target(c):
        """
        This function checks if all rows in the source dataframe are present in the target dataframe.

        It first converts the source and target data into pandas DataFrames. Then, it checks if each row in the source dataframe is in the target dataframe.
        If all rows in the source dataframe are in the target dataframe, it prints "Source In Target" and sets the result to False.
        If there are any rows in the source dataframe that are not in the target dataframe, it prints "Source Not In Target" and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.

        Returns:
        None. The result is stored in the context object.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)
        results = (~source.isin(target).all(axis=1))
        if results.all():
            print(f"Source Not In Target")
            c.s.result = True
        else:
            print(f"Source In Target")
            c.s.result = False
        c.update()

    @when_all(m.rule == 'rows_not_in_source')
    def not_in_source(c):
        """
        This function checks if all rows in the target dataframe are present in the source dataframe.

        It first converts the source and target data into pandas DataFrames. Then, it checks if each row in the target dataframe is in the source dataframe.
        If all rows in the target dataframe are in the source dataframe, it prints "Target Is In Source" and sets the result to False.
        If there are any rows in the target dataframe that are not in the source dataframe, it prints "Target Not In Source" and sets the result to True.

        Parameters:
        c (Context): The context object, which contains the source and target dataframes.

        Returns:
        None. The result is stored in the context object.
        """
        source = pd.DataFrame(c.m.source)
        target = pd.DataFrame(c.m.target)
        results = (~target.isin(source).all(axis=1))
        if results.all():
            print(f"Target Not In Source")
            c.s.result = True
        else:
            print(f"Target Is In Source")
            c.s.result = False
        c.update()
