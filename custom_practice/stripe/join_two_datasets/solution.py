from typing import List, Sequence


def join_data_set(
    field_name: str,
    customer_file: Sequence[str],
    processor_file: Sequence[str],
    skip_unmatched: bool,
) -> List[str]:
    """Join customer rows with matching processor rows and return CSV lines.

    ``skip_unmatched=True`` behaves like an inner join. Otherwise, unmatched
    customer rows are kept with an empty processor portion, like a left join.
    """

    customer_header = customer_file[0].split(",")
    processor_header = processor_file[0].split(",")

    # Resolve column positions once instead of searching the headers per row.
    customer_join_index = customer_header.index(field_name)
    processor_join_index = processor_header.index(field_name)
    customer_order_index = customer_header.index("order")
    processor_order_index = processor_header.index("order")

    # A list per key preserves every processor match and its original order.
    # This supports a one-to-many join rather than keeping only one match.
    processors_by_key = {}
    for line in processor_file[1:]:
        row = line.split(",")
        key = row[processor_join_index]
        processors_by_key.setdefault(key, []).append(row)

    joined_rows = []
    empty_processor = [""] * len(processor_header)

    # Expand each customer into one output row per matching processor row.
    for line in customer_file[1:]:
        customer_row = line.split(",")
        customer_order = int(customer_row[customer_order_index])
        matches = processors_by_key.get(customer_row[customer_join_index])

        if matches:
            for processor_row in matches:
                processor_order = int(processor_row[processor_order_index])
                joined_rows.append(
                    (customer_order, False, processor_order, customer_row + processor_row)
                )
        elif not skip_unmatched:
            # The True flag makes an unmatched row sort after matched rows that
            # have the same customer order because False sorts before True.
            joined_rows.append(
                (customer_order, True, 0, customer_row + empty_processor)
            )

    # Sort by customer order, unmatched flag, then processor order. Python's
    # stable sort preserves customer/processor source order when all keys tie.
    joined_rows.sort(key=lambda row: row[:3])

    # Rebuild the header and expanded rows in the required CSV-string format.
    result = [",".join(customer_header + processor_header)]
    result.extend(",".join(row[3]) for row in joined_rows)
    return result
