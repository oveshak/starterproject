from django.db.models import Sum, Q
from decimal import Decimal
from .models import Customer, Transection, Loan, Installment, DailySaving


def get_customer_account_balance(customer):
    """
    Calculate customer's current account balance from DailySaving
    Includes both positive (deposits) and negative (withdrawals) amounts
    """
    customer_id = customer.id if hasattr(customer, 'id') else customer
    
    try:
        customer_obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return Decimal('0')
    
    total_balance = DailySaving.objects.filter(
        customer_name=customer_obj
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    return total_balance


def get_customer_financial_summary(customer):
    """
    Calculate complete financial summary for a customer
    Returns a dictionary with all financial details
    """
    customer_id = customer.id if hasattr(customer, 'id') else customer
    
    try:
        customer_obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return None
    
    # Calculate total cash in (payments received)
    total_cash_in = Transection.objects.filter(
        customer_name=customer_obj,
        transection_type="cashin"
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate total cash out (loans disbursed, charges)
    total_cash_out = Transection.objects.filter(
        customer_name=customer_obj,
        transection_type="cashout"
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate total loans taken
    total_loans = Loan.objects.filter(
        customer_name=customer_obj
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate total installments paid
    total_installments_paid = Installment.objects.filter(
        customer_name=customer_obj,
        installment_status="paid"
    ).aggregate(total=Sum('installment_pay'))['total'] or Decimal('0')
    
    # Calculate total installments due
    total_installments_due = Installment.objects.filter(
        customer_name=customer_obj,
        installment_status="due"
    ).aggregate(total=Sum('amount'))['total'] or Decimal('0')
    
    # Calculate total savings (account balance)
    account_balance = get_customer_account_balance(customer_obj)
    
    # Calculate outstanding loan amount
    outstanding_amount = total_installments_due
    
    # Calculate net balance (cash in - cash out)
    net_balance = total_cash_in - total_cash_out
    
    # Count active loans (with due installments)
    active_loans = Loan.objects.filter(
        customer_name=customer_obj,
        installment__installment_status="due"
    ).distinct().count()
    
    # Count completed loans
    all_loans = Loan.objects.filter(customer_name=customer_obj).count()
    completed_loans = all_loans - active_loans
    
    return {
        'customer': customer_obj,
        'customer_name': str(customer_obj),
        'total_cash_in': total_cash_in,
        'total_cash_out': total_cash_out,
        'net_balance': net_balance,
        'total_loans_taken': total_loans,
        'total_installments_paid': total_installments_paid,
        'total_installments_due': total_installments_due,
        'outstanding_amount': outstanding_amount,
        'account_balance': account_balance,  # Customer's savings account
        'total_savings': account_balance,  # Alias for backward compatibility
        'active_loans_count': active_loans,
        'completed_loans_count': completed_loans,
        'total_loans_count': all_loans,
    }


def get_customer_transaction_history(customer, limit=None):
    """
    Get all transactions for a customer with details
    """
    customer_id = customer.id if hasattr(customer, 'id') else customer
    
    try:
        customer_obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return []
    
    transactions = Transection.objects.filter(
        customer_name=customer_obj
    ).order_by('-created_at')
    
    if limit:
        transactions = transactions[:limit]
    
    return [{
        'id': t.id,
        'type': t.transection_type,
        'type_display': t.get_transection_type_display(),
        'amount': t.amount,
        'model_name': t.modelname,
        'received_by': str(t.received_by) if t.received_by else 'N/A',
        'date': t.created_at,
    } for t in transactions]


def get_customer_savings_history(customer, limit=None):
    """
    Get all savings (DailySaving) for a customer
    """
    customer_id = customer.id if hasattr(customer, 'id') else customer
    
    try:
        customer_obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return []
    
    savings = DailySaving.objects.filter(
        customer_name=customer_obj
    ).order_by('-created_at')
    
    if limit:
        savings = savings[:limit]
    
    return [{
        'id': s.id,
        'amount': s.amount,
        'type': 'Deposit' if s.amount > 0 else 'Withdrawal',
        'received_by': str(s.received_by) if s.received_by else 'N/A',
        'branch': str(s.branch_name) if s.branch_name else 'N/A',
        'area': str(s.area_name) if s.area_name else 'N/A',
        'date': s.created_at,
    } for s in savings]


def get_loan_details_with_payments(loan_id):
    """
    Get complete loan details including all payments
    """
    try:
        loan = Loan.objects.get(id=loan_id)
    except Loan.DoesNotExist:
        return None
    
    # Get all installments
    installments = loan.installment.all().order_by('installment_date')
    
    total_paid = sum(
        Decimal(str(i.installment_pay)) for i in installments 
        if i.installment_status == 'paid' and i.installment_pay
    )
    
    total_due = sum(
        Decimal(str(i.amount)) for i in installments 
        if i.installment_status == 'due'
    )
    
    total_installments_amount = sum(Decimal(str(i.amount)) for i in installments)
    
    return {
        'loan_id': loan.id,
        'customer': str(loan.customer_name),
        'loan_amount': loan.amount,
        'loan_type': str(loan.loan_type) if loan.loan_type else 'N/A',
        'installment_type': str(loan.installment_type) if loan.installment_type else 'N/A',
        'first_down_payment': loan.first_down_payment or Decimal('0'),
        'pay_from_account': loan.pay_from_account,
        'total_installments_amount': total_installments_amount,
        'total_paid': total_paid,
        'total_due': total_due,
        'total_installments': installments.count(),
        'paid_installments': installments.filter(installment_status='paid').count(),
        'due_installments': installments.filter(installment_status='due').count(),
        'installments': [{
            'id': i.id,
            'date': i.installment_date,
            'amount': i.amount,
            'paid_amount': i.installment_pay,
            'status': i.installment_status,
            'is_extra_payment': i.is_extra_payment() if i.installment_pay else False,
        } for i in installments]
    }


def check_customer_can_afford_loan(customer, down_payment_amount):
    """
    Check if customer has sufficient account balance for down payment
    """
    customer_id = customer.id if hasattr(customer, 'id') else customer
    
    try:
        customer_obj = Customer.objects.get(id=customer_id)
    except Customer.DoesNotExist:
        return False, Decimal('0')
    
    account_balance = get_customer_account_balance(customer_obj)
    can_afford = account_balance >= Decimal(str(down_payment_amount))
    
    return can_afford, account_balance


# Example usage in views.py or Django shell:
"""
# Get customer summary with account balance
from .utils import get_customer_financial_summary, get_customer_account_balance

customer = Customer.objects.get(id=1)
summary = get_customer_financial_summary(customer)
print(f"Customer: {summary['customer_name']}")
print(f"Account Balance: {summary['account_balance']}")
print(f"Total Cash In: {summary['total_cash_in']}")
print(f"Total Cash Out: {summary['total_cash_out']}")
print(f"Net Balance: {summary['net_balance']}")
print(f"Outstanding: {summary['outstanding_amount']}")

# Check if customer can afford a down payment
from .utils import check_customer_can_afford_loan

can_afford, balance = check_customer_can_afford_loan(customer, 5000)
print(f"Can afford 5000 down payment: {can_afford}")
print(f"Current balance: {balance}")

# Get savings history
from .utils import get_customer_savings_history

savings = get_customer_savings_history(customer, limit=10)
for s in savings:
    print(f"{s['date']}: {s['type']} - {s['amount']}")

# Get transaction history
from .utils import get_customer_transaction_history

transactions = get_customer_transaction_history(customer, limit=10)
for t in transactions:
    print(f"{t['date']}: {t['type_display']} - {t['amount']} ({t['model_name']})")

# Get loan details
from .utils import get_loan_details_with_payments

loan_details = get_loan_details_with_payments(loan_id=1)
print(f"Loan Amount: {loan_details['loan_amount']}")
print(f"Total Paid: {loan_details['total_paid']}")
print(f"Total Due: {loan_details['total_due']}")
print(f"Pay from Account: {loan_details['pay_from_account']}")
"""