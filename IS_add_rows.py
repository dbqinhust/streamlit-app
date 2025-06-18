def apply_rules(df, rules):
    for new_index, rule in rules.items():
        formula = rule["formula"]

        # Build a Python expression string that accesses df.loc[...] for each index
        expr = ' '.join(
            f"df.loc['{tok.strip()}', 'col3']" if tok.strip() not in ['+', '-', '*', '/'] else tok
            for tok in formula.replace('-', ' - ').replace('+', ' + ').split()
        )

        # Safely evaluate the expression
        try:
            col3_value = eval(expr)
        except KeyError as e:
            raise ValueError(f"Missing index in DataFrame: {e}") from None

        # Add the new row
        df.loc[new_index] = {
            'col1': rule.get('col1'),  # Optional field
            'col2': rule.get('col2'),
            'col3': col3_value
        }

    return df.sort_index()
