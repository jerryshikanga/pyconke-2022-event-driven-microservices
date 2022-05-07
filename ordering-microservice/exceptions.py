class UserNotFoundError(Exception):
    pass


class InactiveUserError(Exception):
    pass


class ProductNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass
