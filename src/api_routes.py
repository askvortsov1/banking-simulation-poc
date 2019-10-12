import resources


routes = (
    (resources.BankListApi, "/bank/"),
    (resources.BankApi, "/bank/<int:bank_id>/"),

    (resources.BranchListApi, "/bank/<int:bank_id>/branch/"),
    (resources.BranchApi, "/bank/<int:bank_id>/branch/<branch_id>/"),

    (resources.StaffListApi, "/bank/<int:bank_id>/branch/<branch_id>/staff/"),
    (resources.StaffApi, "/bank/<int:bank_id>/branch/<branch_id>/staff/<int:staff_id>/"),

    (resources.AccountConfigListApi, "/bank/<int:bank_id>/account_config/"),
    (resources.AccountConfigApi, "/bank/<int:bank_id>/account_config/<int:account_config_id>/"),

    (resources.AccountListApi, "/bank/<int:bank_id>/account/"),
    (resources.AccountApi, "/bank/<int:bank_id>/account/<int:account_id>/"),

    (resources.TransactionListApi, "/bank/<int:bank_id>/account/<int:account_id>/transaction/"),
    (resources.TransactionApi, "/bank/<int:bank_id>/account/<int:account_id>/transaction/<int:transaction_id>/"),

    (resources.CheckListApi, "/bank/<int:bank_id>/account/<int:account_id>/check/"),
    (resources.CheckApi, "/bank/<int:bank_id>/account/<int:account_id>/check/<int:check_id>/"),

    (resources.UserListApi, "/user/"),
    (resources.UserApi, "/user/<int:user_id>/")
)
