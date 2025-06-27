def calculate_total_due(maintenance_fee: int, due_amt: int = 0, fine: int = 0, miscellaneous: int = 0) -> int:
    """
    Calculates the total due amount for a flat.
    :param maintenance_fee: Monthly maintenance fee (mandatory)
    :param due_amt: Outstanding rent (if any)
    :param fine: Any fines levied
    :param miscellaneous: Any other charges
    :return: Total due as integer
    """
    total = 0
    if maintenance_fee:
        total += maintenance_fee
    if due_amt:
        total += due_amt
    if fine:
        total += fine
    if miscellaneous:
        total += miscellaneous
    return total

