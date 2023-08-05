#$Id$

class Transaction: 
    """This class is used to create object for transaction."""
    def __init__(self):
        """Initialize parameters for transactions object."""
        self.transaction_id = ''
        self.debit_or_credit = ''
        self.date = ''
        self.customer_id = ''
        self.payee = ''
        self.reference_number = '' 
        self.transaction_type = ''
        self.amount = ''
        self.status = ''
        self.date_formatted = ''
        self.transaction_type_formatted = ''
        self.amount_formatted = ''
        self.customer_name = ''
        self.from_account_id = ''
        self.from_account_name  =  ''
        self.to_account_id = ''
        self.to_account_name = ''
        self.currency_id = ''
        self.currency_code = ''
        self.payment_mode = ''
        self.exchange_rate = 0.0
        self.reference_number = ''
        self.description = ''
        self.imported_transaction_id = ''
        self.associated_transactions = []
        self.categorized_transaction_id = ''
        self.transaction_date = ''
        self.account_id = ''
        self.entry_number = ''
        self.offset_account_name = ''
        self.reconcile_status = ''
        self.debit_amount = 0.0
        self.credit_amount = 0.0
        self.source = ''
        self.imported_transactions = []
        self.status_formatted = ''

    def set_imported_transaction_id(self, imported_transaction_id):
        """Set imported transaction id.

        Args:
            imported_transaction_id(str): Imported transaction id.

        """
        self.imported_transaction_id = imported_transaction_id

    def get_imported_transaction_id(self):
        """Get imported transaction id.

        Returns:
            str: Imported transaction id.

        """
        return self.imported_transaction_id

    def set_transaction_id(self, transaction_id): 
        """Set transaction id.

        Args: 
            transaction_id(str): Transaction_id.

        """
        self.transaction_id = transaction_id

    def get_transaction_id(self):
        """Get transaction id.

        Returns: 
            str: Transaction id.

        """
        return self.transaction_id

    def set_debit_or_credit(self, debit_or_credit):
        """Set whether debit or credit.

        Args:
            debit_or_credit(str): Debit or credit.

        """
        self.debit_or_credit = debit_or_credit

    def get_debit_or_credit(self):
        """Get whether debit or credit.

        Returns: 
            str: Debit or credit.

        """
        return self.debit_or_credit

    def set_date(self, date):
        """Set date.

        Args:
            date(str): Date.

        """
        self.date = date

    def get_date(self):
        """Get date.

        Returns:
            str: Date.

        """
        return self.date

    def set_customer_id(self, customer_id):
        """Set customer id.

        Args:
            customer_id(self): Customer id.

        """
        self.customer_id = customer_id

    def get_customer_id(self):
        """Get customer id.

        Returns:
            str: Customer id.

        """
        return self.customer_id

    def set_payee(self, payee):
        """Set payee.

        Args:
            payee(str): Payee.

        """
        self.payee = payee

    def get_payee(self):
        """Get payee.

        Returns:
            str: Payee.

        """
        return self.payee

    def set_reference_number(self, reference_number):
        """Set reference number.

        Args:
            reference_number(str): Reference number.

        """
        self.reference_number = reference_number

    def get_reference_number(self):
        """Get reference number.

        Returns:
            str: Reference number.

        """
        return self.reference_number

    def set_transaction_type(self, transaction_type):
        """Set transaction type.

        Args:
            transaction_type(str): Transaction type.

        """
        self.transaction_type = transaction_type

    def get_transaction_type(self):
        """Get transaction type.

        Returns: 
            str: Transaction type.

        """
        return self.transaction_type

    def set_amount(self, amount):
        """Set amount.

        Args:
            amount(float): Amount.

        """
        self.amount = amount

    def get_amount(self):
        """Get amount.

        Returns:
            float: Amount.

        """
        return self.amount

    def set_status(self, status):
        """Set status.

        Args:
            status(str): Status.

        """
        self.status = status

    def get_status(self):
        """Get status.

        Returns:
            str: Status.

        """
        return self.status

    def set_date_formatted(self, date_formatted): 
        """Set date formatted.

        Args:
            date_formatted(str): Date formatted.

        """
        self.date_formatted = date_formatted

    def get_date_formatted(self):
        """Get date formatted.

        Returns:
            str: Date formatted.
       
        """

    def set_transaction_type_formatted(self, transaction_type_formatted):
        """Set transaction type formatted.

        Args:
            transaction_type_formatted(str): Transaction type formatted.

        """
        self.transaction_type_formatted = transaction_type_formatted

    def get_transaction_type_formatted(self):
        """Get transaction type formatted.

        Returns:
            str: Transaction type formatted.

        """
        return self.transaction_type_formatted

    def set_amount_formatted(self, amount_formatted):
        """Set amount formatted.

        Args:
            amount_formatted(str): Amount formatted.

        """
        self.amount_formatted = amount_formatted

    def get_amount_formatted(self):
        """Get amount formatted.

        Returns: 
            str: Amount formatted.

        """
        return self.amount_formatted

    def set_customer_name(self, customer_name): 
        """Set customer name.

        Args:
            customer_name(str): Customer name.
 
        """
        self.customer_name = customer_name
 
    def get_customer_name(self):
        """Get customer name.

        Returns:
            str: Customer name.
 
        """
        return self.customer_name

    def set_from_account_id(self, from_account_id):
       """Set from account id.

       Args:
           from_account_id(str): From account id.

       """
       self.from_account_id = from_account_id

    def get_from_account_id(self):
        """Get from account id.

        Returns:
            str: From account id.

        """
        return self.from_account_id

    def set_from_account_name(self, from_account_name): 
        """Set from account name.

        Args:
            from_account_name(str): From account name.

        """
        self.from_account_name = from_account_name

    def get_from_account_name(self):
        """Get from account name.

        Returns:
            str: From account name.

        """
        return self.from_account_name

    def set_to_account_id(self, to_account_id):
        """Set to account id.

        Args:
            to_account_id(str): To account id.

        """
        self.to_account_id = to_account_id    

    def get_to_account_id(self):
        """Get to account id.

        Returns:
            str: To account id.

        """
        return self.to_account_id
   
    def set_to_account_name(self, to_account_name): 
        """Set to account name.

        Args:
            to_account_name(str): To account name.

        """
        self.to_account_name = to_account_name

    def get_to_account_name(self):
        """Get to account name.
 
        Returns:
            str: To account name.

        """
        return self.to_account_name


  
    def set_currency_id(self, currency_id): 
        """Set currency id.

        Args:
            currency_id(str): Currency id.

        """
        self.currecny_id = currency_id

    def get_currency_id(self):
        """Get currency id.

        Returns: 
            str: Currecny id.

        """
        return self.currency_id

    def set_currency_code(self, currency_code):
        """Set currecny code.

        Args:
            currency_code(str): Currecny code.

        """
        self.currecy_code = currency_code

    def get_currency_code(self):
        """Get currecny code.

        Returns:
            str: Currecny code.

        """
        return self.currecny_code

    def set_payment_mode(self, payment_mode):
        """Set payment mode.

        Args:
            payment_mode(str): Payment mode.

        """
        self.payment_mode = payment_mode

    def get_payment_mode(self):
        """Get payment mode.

        Returns:
            str: Payment mode.

        """
        return self.payment_mode
  
    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate.

        Args:
            exchaneg_rate(float): Exchange rate.

        """
        self.exchange_rate = exchange_rate

    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchange rate.

        """
        return self.exchange_rate
  
    def set_description(self, description):
        """Set description.

        Args:
            description(str): Description.

        """
        self.description = description
 
    def get_description(self):
        """Get description.

        Returns:
            str: Description.

        """
        return self.description

    def set_currency_id(self, currency_id):
        """Set currency id.

        Args: 
            currency_id(str): Currency id.

        """
        self.currecny_id = currency_id

    def get_currency_id(self): 
        """Get currecny id.
 
        Returns:
            str: Currency id.

        """
        return self.currency_id
   
    def set_currency_code(self, currency_code):
        """Set currency code.

        Args:
            currency_code(str): Currency code.

        """
        self.currency_code = currency_code

    def get_currecny_code(self):
        """Get currecny code.

        Returns: 
            str: Currency code.

        """
        return self.currency_code

    def set_payment_mode(self, payment_mode):
        """Set payment mode.

        Args:
            payment_mode(str): Payment mode.

        """
        self.payment_mode = payment_mode

    def get_payment_mode(self):
        """Get payment mode.

        Returns:
            str: Payment mode.

        """
        return self.payment_mode

    def set_exchange_rate(self, exchange_rate):
        """Set exchange rate.

        Args:
            exchange_rate(float): Exchange rate.

        """
        self.exchange_rate = exchange_rate
    
    def get_exchange_rate(self):
        """Get exchange rate.

        Returns:
            float: Exchange rate.

        """
        return self.exchange_rate

    def set_associated_transactions(self, transactions):
        """Set associated transacctions.

        Args:
            transactions(instance): Transaction object.

        """
        self.associated_transactions.append(transactions)

    def get_associated_transactions(self):
        """Get associated transactions.

        Returns:
            list of instance: List of transactions object.

        """
        return self.associated_transactions

    def set_categorized_transaction_id(self, categorized_transaction_id):
        """Set categorized transaction id.

        Args:
            categorized_transaction_id(str): Categorized transaction id.

        """
        self.categorized_transaction_id = categorized_transaction_id

    def get_categorized_transaction_id(self):
        """Get categorized transaction id.

        Returns:
            str: Categorized transaction id.

        """
        return self.categorized_transaction_id

    def set_transaction_date(self, transaction_date):
        """Set transaction date.

        Args:
            transaction_date(str): Transaction date.

        """
        self.transaction_date = transaction_date

    def get_transaction_date(self):
        """Get transaction date.

        Returns:
            str: Transaction date.

        """
        return self.transaction_date

    def set_account_id(self, account_id):
        """Set account id.

        Args:
            account_id(str): Account id.

        """
        self.account_id = account_id

    def get_account_id(self):
        """Get account id.

        Returns:
            str: Account id.

        """
        return self.account_id

    def set_entry_number(self, entry_number):
        """Set entry number.

        Args:
            entry_number(str): Entry number.

        """
        self.entry_number = entry_number

    def get_entry_number(self):
        """Get entry number.

        Returns:
            str: Entry number.

        """
        return self.entry_number

    def set_offset_account_name(self, offset_account_name):
        """Set offset account name.

        Args: 
            offset_account_name(str): Offset account name.

        """
        self.offset_account_name = offset_account_name

    def get_offset_account_name(self):
        """Get offset_account_name.

        Returns:
            str: Offset account name.

        """
        return self.offset_account_name

    def set_reconcile_status(self, reconcile_status):
        """Set reconcile status.

        Args:
            reconcile_status(str): Reconcile status.

        """
        self.reconcile_status = reconcile_status

    def get_reconcile_status(self):
        """Get reconcile status.

        Returns:
            str:  Reconcile status.

        """
        return self.reconcile_status

    def set_debit_amount(self, debit_amount):
        """Set debit amount.

        Args:
            debit_amount(float): Debit amount.

        """
        self.debit_amount = debit_amount

    def get_debit_amount(self): 
        """Get debit amount.

        Returns:
            float: Debit amount.

        """
        return self.debit_amount

    def set_credit_amount(self, credit_amount):
        """Set ccredit amount.

        Args:
            credit_amount(flaot): Credit amount.

        """
        self.credit_amount = credit_amount

    def get_credit_amount(self):
        """Get credit amount.

        Returns:
            float: Credit amount.

        """
        return self.credit_amount

    def set_source(self, source):
        """Set source.

        Args:
            source(str): Source.

        """
        self.source = source

    def get_source(self):
        """Get source.
 
        Returns:
            str: Source.

        """
        return self.source

    def set_imported_transaction(self, imported_transactions):
        """Set imported transactions.

        Args:
            imported_transaction: Imported transaction.

        """
        self.imported_transactions.append(imported_transactions)

    def get_imported_transaction(self): 
        """Get imported transactions.

        Returns:
            list: List of imported transactions.

        """
        return self.imported_transactions

    def set_status_formatted(self, status_formatted):
        """Set status formatted.

        Args:
            status_formatted(str): Status formatted.

        """
        self.status_formatted = status_formatted

    def get_status_formatted(self):
        """Get status formatted.

        Returns:
            str: Status formatted.

        """
        return self.status_formatted

    def to_json(self):
        """This method is used to convert taransaction object to json format.

        Returns:
            dict: Dictionary containing json object for transaction.

        """
        data = {}
        if self.from_account_id != '':
            data['from_account_id'] = self.from_account_id
        if self.to_account_id != '':
            data['to_account_id'] = self.to_account_id
        if self.transaction_type != '':
            data['transaction_type'] = self.transaction_type
        if self.amount > 0:
            data['amount'] = self.amount
        if self.payment_mode != '':
            data['payment_mode'] = self.payment_mode
        if self.exchange_rate > 0:
            data['exchange_rate'] = self.exchange_rate
        if self.date != '':
            data['date'] = self.date
        if self.customer_id != '':
            data['customer_id'] = self.customer_id
        if self.reference_number != '':
            data['reference_number'] = self.reference_number
        if self.description != '':
            data['description'] = self.description
        if self.currency_id != '':
            data['currency_id'] = self.currency_id
        return data

