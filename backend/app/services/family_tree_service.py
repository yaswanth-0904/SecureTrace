def build_tree(parent_code, records):
    children = []

    for record in records:
        if record.parent_dna == parent_code:
            children.append(
                {
                    "dna_code": record.dna_code,
                    "children": build_tree(
                        record.dna_code,
                        records
                    )
                }
            )

    return children