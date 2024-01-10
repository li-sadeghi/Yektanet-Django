from enum import Enum
default_credit = 0
one_click_cost = 1
thousand_view_cost = 1

CLICK = 'Click'
VIEW = 'View'
TYPE_CHOICES = [
    (CLICK, 'Click'),
    (VIEW, 'View'),
]

CLICK_TRANSACTION_TOPIC = 'click-transaction'
VIEW_TRANSACTION_TOPIC = 'view-transaction'
FINANCIAL_REPORT_TRANSACTION_TOPIC = 'financial-transaction'
