# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from datetime import timedelta, date, timezone
# from dateutil.relativedelta import relativedelta
# from .models import Loan, Installment

# def get_next_valid_date(current_date):
#     while current_date.weekday() == 4:  # skip Friday
#         current_date += timedelta(days=1)
#     return current_date

# def generate_installment_dates(start_date, installment_type):
#     dates = []
#     frequency = installment_type.type
    
#     total_duration_months = installment_type.total_duration or 12
#     print(total_duration_months  or 12)
#     print(installment_type.instalment_cullect or 122 )
#     print( installment_type.type)
#     if frequency == "daily":
#         total_installments = total_duration_months * 22
#         delta = timedelta(days=installment_type.instalment_cullect)
#     elif frequency == "weekly":
#         total_installments = int(total_duration_months * 4.3)
#         delta = timedelta(weeks=installment_type.instalment_cullect)
#     elif frequency == "monthly":
#         total_installments = total_duration_months
#         delta = relativedelta(months=installment_type.instalment_cullect)
#     elif frequency == "yearly":
#         total_installments = max(1, total_duration_months // 12)
#         delta = relativedelta(years=installment_type.instalment_cullect)
#     else:
#         return dates

#     current_date = get_next_valid_date(start_date)
#     for _ in range(total_installments):
#         dates.append(current_date)
#         current_date = get_next_valid_date(current_date + delta)
#     return dates

# @receiver(post_save, sender=Loan)
# def create_installments(sender, instance, created, **kwargs):
#     if not created:
#         return

#     print(f"\n--- Loan Created Debug ---")
#     print(f"Loan ID: {instance.id}, Customer: {instance.customer_name}, Receive Type: {instance.receive_type}")
#     print(f"Loan Amount: {instance.amount}, Installment Type: {getattr(instance.installment_type, 'type', 'N/A')}")
#     print(f"First Down Payment: {instance.first_down_payment}")
#     print(f"Loan Type: {getattr(instance.loan_type, 'name', 'N/A')}")

#     # 🔹 Original Loan Amount
#     original_amount = float(instance.amount)
#     total_amount = original_amount

#     # 🔹 LoanType behaviour_type calculation (percent = original_amount)
#     if instance.loan_type and instance.loan_type.behaviour_type:
#         print("Applying LoanType behaviour_type...")
#         for item in instance.loan_type.behaviour_type:
#             amt = float(item.get("amount", 0))
#             if item.get("is_percent"):
#                 added = original_amount * amt / 100   # always original_amount
#                 total_amount += added
#                 print(f"  + {item['name']} (Percent {amt}%) => Added {added:.2f}")
#             else:
#                 total_amount += amt
#                 print(f"  + {item['name']} (Fixed {amt}) => Added {amt:.2f}")

#     print(f"Total Amount before Down Payment: {total_amount:.2f}")

#     # 🔹 First Down Payment
#     if instance.first_down_payment:
#         total_amount -= float(instance.first_down_payment)
#         total_amount = max(total_amount, 0)
#         print(f"After First Down Payment Deduct: {total_amount:.2f}")

#     # 🔹 InstallmentType check
#     installment_type = instance.installment_type
#     if not installment_type:
#         print("No InstallmentType. Exiting.")
#         return

#     installment_amount = installment_type.instalment_cullect
#     if not installment_amount or installment_amount <= 0:
#         print("Invalid Installment Amount. Exiting.")
#         return

#     # 🔹 Generate installment dates
#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         print("No Installment Dates. Exiting.")
#         return

#     print(f"Generating {len(dates)} Installments (approx)")

#     # 🔹 Create installments
#     num_installments = len(dates)
#     per_installment_amount = round(total_amount / num_installments, 2)
#     remaining_amount = total_amount
#     installments = []

#     for i, inst_date in enumerate(dates):
#         if i == num_installments - 1:
#             amount = round(remaining_amount, 2)
#         else:
#             amount = per_installment_amount
#             remaining_amount -= amount

#         if amount <= 0:
#             break

#         installment = Installment.objects.create(
#             customer_name=instance.customer_name,
#             installment_date=inst_date,
#             amount=amount,
#             installment_status="due",
#             area_name=instance.area_name,
#             branch_name=instance.branch_name,
#             loan_id=instance.id
#         )
#         installments.append(installment)
#         print(f"  Installment {i+1}: Date={inst_date}, Amount={amount:.2f}, Remaining={remaining_amount:.2f}")

#     if installments:
#         instance.installment.set(installments, clear=True)
#         print(f"{len(installments)} installments attached to Loan ID {instance.id}")

#     # 🔹 Update updated_at
#     if hasattr(instance, "updated_at"):
#         Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from contacts.models import Customer
from products.models import BranchProductStock, Variation
from .models import Loan, Installment, Purchase, Transection, DailySaving
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
import traceback


class InsufficientBalanceError(Exception):
    """Custom exception for insufficient balance"""
    pass


def get_next_valid_date(current_date):
    # Friday = 4
    while current_date.weekday() == 4:
        current_date += timedelta(days=1)
    return current_date


# def generate_installment_dates(start_date, installment_type):
#     """Generate installment dates based on frequency"""
#     dates = []
#     frequency = installment_type.type
#     total_duration_months = installment_type.total_duration or 12
    
#     if frequency == "daily":
#         total_installments = total_duration_months * 22
#         delta = timedelta(days=installment_type.instalment_cullect)
#     elif frequency == "weekly":
#         total_installments = int(total_duration_months * 4.3)
#         delta = timedelta(weeks=installment_type.instalment_cullect)
#     elif frequency == "monthly":
#         total_installments = total_duration_months
#         delta = relativedelta(months=installment_type.instalment_cullect)
#     elif frequency == "yearly":
#         total_installments = max(1, total_duration_months // 12)
#         delta = relativedelta(years=installment_type.instalment_cullect)
#     else:
#         return dates

#     current_date = get_next_valid_date(start_date)
#     for _ in range(total_installments):
#         dates.append(current_date)
#         current_date = get_next_valid_date(current_date + delta)
#     return dates



def generate_installment_dates(start_date, installment_type):
    dates = []
    frequency = installment_type.type
    total_duration_months = installment_type.total_duration or 12

    if frequency == "daily":
        total_installments = total_duration_months * 22
        delta = timedelta(days=installment_type.instalment_cullect)

    elif frequency == "weekly":
        total_installments = int(total_duration_months * 4.3)
        delta = timedelta(weeks=installment_type.instalment_cullect)

    elif frequency == "monthly":
        total_installments = total_duration_months
        delta = relativedelta(months=installment_type.instalment_cullect)

    elif frequency == "yearly":
        total_installments = max(1, total_duration_months // 12)
        delta = relativedelta(years=installment_type.instalment_cullect)

    else:
        return dates

    # ✅ KEY LOGIC:
    # 1st installment = loan_date + instalment_cullect
    first_date = start_date + delta

    # Friday skip
    current_date = get_next_valid_date(first_date)

    for _ in range(total_installments):
        dates.append(current_date)
        current_date = get_next_valid_date(current_date + delta)

    return dates


def create_transaction_with_customer_info(customer, **transaction_data):
    """
    Helper function to create transaction with auto-populated customer info
    """
    # Auto-add customer's branch, area, and group if not provided
    if 'branch_name' not in transaction_data and hasattr(customer, 'branch_name'):
        transaction_data['branch_name'] = customer.branch_name
    
    if 'area_name' not in transaction_data and hasattr(customer, 'area_name'):
        transaction_data['area_name'] = customer.area_name
    
    if 'customer_group' not in transaction_data and hasattr(customer, 'customer_group'):
        transaction_data['customer_group'] = customer.customer_group
    
    return Transection.objects.create(**transaction_data)


def update_customer_balance(customer, amount):
    """
    Update customer account balance
    Only called for DailySavings and Extra Savings
    """
    try:
        customer.account_balance += Decimal(str(amount))
        customer.save(update_fields=['account_balance'])
        print(f"✓ Customer balance updated: {customer.account_balance:.2f}")
    except Exception as e:
        print(f"❌ Error updating customer balance: {str(e)}")


def check_and_deduct_balance(customer, amount, purpose="payment"):
    """
    Check if customer has sufficient balance and deduct if available
    Raises InsufficientBalanceError if balance is insufficient
    """
    # Refresh customer from database to get latest balance
    customer.refresh_from_db()
    customer_balance = customer.account_balance
    required_amount = Decimal(str(amount))
    
    if customer_balance < required_amount:
        error_msg = (
            f"Insufficient balance! "
            f"Customer: {customer.full_name}, "
            f"Required: {required_amount:.2f} Tk, "
            f"Available: {customer_balance:.2f} Tk, "
            f"Shortage: {(required_amount - customer_balance):.2f} Tk"
        )
        print(f"❌ {error_msg}")
        raise InsufficientBalanceError(error_msg)
    
    # Deduct from balance
    update_customer_balance(customer, -required_amount)
    return True


@receiver(post_save, sender=Customer)
def create_customer_type_transactions(sender, instance, created, **kwargs):
    """
    Create transactions based on customer type behavior when a new customer is created.
    """
    if not created:
        return
   
    try:
        # IMPORTANT: Refresh from database to get all related fields
        instance.refresh_from_db()
        
        if not instance.coustomer_type:
            print(f"No customer type assigned for Customer: {instance.full_name}")
            return
           
        if not instance.coustomer_type.behaviour_type:
            print(f"No behaviors defined for customer type: {instance.coustomer_type.name}")
            return
       
        print(f"\n--- Customer Created: {instance.full_name} (ID: {instance.id}) ---")
        print(f"Customer Type: {instance.coustomer_type.name}")
        
        # Debug: Check all customer_group related attributes
        print(f"\n🔍 DEBUG - Customer Group Info:")
        print(f"  - hasattr(instance, 'customer_group'): {hasattr(instance, 'customer_group')}")
        if hasattr(instance, 'customer_group'):
            print(f"  - instance.customer_group: {instance.customer_group}")
            print(f"  - instance.customer_group type: {type(instance.customer_group)}")
            print(f"  - instance.customer_group is None: {instance.customer_group is None}")
            if instance.customer_group:
                print(f"  - instance.customer_group.id: {instance.customer_group.id if hasattr(instance.customer_group, 'id') else 'NO ID'}")
        
        # Check for customer_group_id field
        if hasattr(instance, 'customer_group_id'):
            print(f"  - instance.customer_group_id: {instance.customer_group_id}")
        
        # Display customer group info if available
        if hasattr(instance, 'customer_group') and instance.customer_group:
            print(f"\n✅ Customer Group: {instance.customer_group} (ID: {instance.customer_group.id if hasattr(instance.customer_group, 'id') else 'N/A'})")
        else:
            print(f"\n❌ Customer Group: NOT ASSIGNED")
        
        print(f"\nProcessing Customer Type behaviors...")
       
        for item in instance.coustomer_type.behaviour_type:
            try:
                behavior_name = item.get("name", "Unknown")
                amt = Decimal(str(item.get("amount", 0)))
               
                if amt <= 0:
                    print(f"  Skipping {behavior_name}: Amount is 0")
                    continue
               
                transaction_type = item.get("transaction_type", "cashout")
               
                if item.get("is_percent"):
                    print(f"  ! {behavior_name} ({amt}%): Percentage-based behaviors not implemented")
                    continue
               
                print(f"  + {behavior_name} (Fixed): {transaction_type.upper()} {amt:.2f}")
               
                transaction_data = {
                    "transection_type": transaction_type,
                    "amount": amt,
                    "customer_name": instance,
                    "modelname": f"Customer Type Behavior: {behavior_name}",
                     "received_by": instance.received_by,  # <-- added lin
                }
               
                # Add created_by if available
                if hasattr(instance, 'created_by') and instance.created_by:
                    transaction_data["received_by"] = instance.created_by
               
                # This function auto-adds branch_name, area_name, and customer_group from customer
                transaction = create_transaction_with_customer_info(instance, **transaction_data)
                
                # Log customer group info
                if hasattr(instance, 'customer_group') and instance.customer_group:
                    print(f"  ✓ Transaction created: ID {transaction.id} (Group: {instance.customer_group})")
                else:
                    print(f"  ✓ Transaction created: ID {transaction.id} (No Group)")
                    print(f"    ⚠ Warning: Customer has no customer_group assigned")
               
            except Exception as behavior_error:
                print(f"  ✗ Error processing behavior '{behavior_name}': {str(behavior_error)}")
                print(f"     Details: {traceback.format_exc()}")
                continue
       
        print(f"✅ Customer type transactions completed for {instance.full_name}")
       
    except Exception as e:
        print(f"\n❌ SIGNAL ERROR for customer {instance.full_name}:")
        print(f"   Error: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")


from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

Q2 = Decimal("0.01")
def q2(x):  # quantize to 2 decimal
    return Decimal(str(x)).quantize(Q2, rounding=ROUND_HALF_UP)

def _adjust_branch_stock(branch, product, qty):
    """
    এখন থেকে opening_stock থেকে কমাবে (quantity ছোঁয়া হবে না)
    """
    

    stock = (BranchProductStock.objects
             .select_for_update()
             .filter(branch_name=branch, product_name=product)
             .first())

    if stock is None:
        raise ValidationError(f"No stock record for {product} at branch {branch}.")

    if qty <= 0:
        raise ValidationError("Quantity must be positive.")

    # opening_stock দিয়েই যাচাই ও কমানো হবে
    if stock.opening_stock < qty:
        raise ValidationError(
            f"Insufficient opening stock for {product} at {branch}. "
            f"Have {stock.opening_stock}, need {qty}."
        )

    stock.opening_stock = F('opening_stock') - qty
    stock.save(update_fields=["opening_stock"])

def _process_product_receipt(instance):
    # if loan is given as products, deduct branch stock
    if instance.receive_type != "product" or not instance.product_details:
        return
    from .models import Product
    for row in (instance.product_details or []):
        pid = row.get("productId")
        qty = int(row.get("quantity", 0) or 0)
        if not pid or qty <= 0:
            continue
        try:
            product = Product.objects.get(pk=pid)
        except Product.DoesNotExist:
            raise ValidationError(f"Product (id={pid}) not found.")
        _adjust_branch_stock(instance.branch_name, product, qty)
def deduct_branch_and_variation_stock(branch, variation, qty):
    if qty <= 0:
        raise ValidationError("Quantity must be positive")

    # 🔒 lock branch stock row
    branch_stock = (
        BranchProductStock.objects
        .select_for_update()
        .filter(
            stock_branch=branch,
            product_variation=variation
        )
        .first()
    )

    if not branch_stock:
        raise ValidationError(
            f"No branch stock for variation {variation.id}"
        )

    # ✅ validate BEFORE update (int vs int)
    if branch_stock.quantity < qty:
        raise ValidationError(
            f"Branch stock insufficient. Have {branch_stock.quantity}, need {qty}"
        )

    if variation.quantity < qty:
        raise ValidationError(
            f"Variation stock insufficient. Have {variation.quantity}, need {qty}"
        )

    # ✅ update WITHOUT triggering clean()
    BranchProductStock.objects.filter(
        id=branch_stock.id
    ).update(
        quantity=F("quantity") - qty
    )

    Variation.objects.filter(
        id=variation.id
    ).update(
        quantity=F("quantity") - qty
    )

@receiver(post_save, sender=Loan)
def handle_loan_create(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.receive_type != "product":
        return

    if not instance.product_details:
        return

    with transaction.atomic():
        for row in instance.product_details:
            variation_id = row.get("variation_id")
            qty = int(row.get("quantity", 0))

            if not variation_id or qty <= 0:
                continue

            try:
                variation = Variation.objects.select_for_update().get(
                    id=variation_id
                )
            except Variation.DoesNotExist:
                raise ValidationError(
                    f"Variation {variation_id} not found"
                )

            deduct_branch_and_variation_stock(
                branch=instance.branch_name,
                variation=variation,
                qty=qty
            )


@receiver(post_save, sender=Loan)
def create_installments_and_transactions(sender, instance, created, **kwargs):
    """
    Create installments and transactions with auto-populated customer info
    """
    if not created:
        return

    print(f"\n--- Loan Created: ID {instance.id} ---")

    original_amount = q2(instance.amount)
    total_amount = original_amount

    # 1) LoanType behavior charges
    if instance.loan_type and instance.loan_type.behaviour_type:
        print("Processing LoanType behaviors...")
        for item in instance.loan_type.behaviour_type:
            behavior_name = item.get("name", "Unknown")
            amt = q2(item.get("amount", 0))
            if item.get("is_percent"):
                added = q2(original_amount * amt / Decimal(100))
                total_amount = q2(total_amount + added)
                print(f"  + {behavior_name} ({amt}%): +{added:.2f}")
                create_transaction_with_customer_info(
                    instance.customer_name,
                    transection_type="cashout",
                    amount=added,
                    customer_name=instance.customer_name,
                    received_by=getattr(instance, 'created_by', None),
                    modelname=f"Loan Behavior: {behavior_name}"
                )
            else:
                total_amount = q2(total_amount + amt)
                print(f"  + {behavior_name} (Fixed): +{amt:.2f}")
                create_transaction_with_customer_info(
                    instance.customer_name,
                    transection_type="cashout",
                    amount=amt,
                    customer_name=instance.customer_name,
                    received_by=getattr(instance, 'created_by', None),
                    modelname=f"Loan Behavior: {behavior_name}"
                )

    print(f"Total Amount: {total_amount:.2f}")

    # 2) Pre-validate installment type
    installment_type = instance.installment_type
    if not installment_type or not getattr(installment_type, "instalment_cullect", None) or installment_type.instalment_cullect <= 0:
        print("Invalid Installment Amount. Exiting.")
        return

    start_date = date.today()
    dates = generate_installment_dates(start_date, installment_type)
    if not dates:
        print("No Installment Dates. Exiting.")
        return

    print(f"Generating {len(dates)} Installments")

    # ---- Everything below happens atomically ----
    try:
        with transaction.atomic():
            # 3) If product loan, deduct branch stock now (row-locked)
            _process_product_receipt(instance)

            # 4) First down payment (apply ONCE)
            down_payment = q2(instance.first_down_payment or 0)
            if down_payment > 0:
                if instance.pay_from_account:
                    print("Pay from account enabled - checking customer balance...")
                    check_and_deduct_balance(
                        instance.customer_name,
                        down_payment,
                        f"Down Payment for Loan ID: {instance.id}"
                    )
                    print(f"✓ Deducted {down_payment:.2f} from customer account")
                    create_transaction_with_customer_info(
                        instance.customer_name,
                        transection_type="cashout",
                        amount=down_payment,
                        customer_name=instance.customer_name,
                        received_by=getattr(instance, 'created_by', None),
                        modelname=f"Down Payment from Account (Loan ID: {instance.id})"
                    )
                else:
                    create_transaction_with_customer_info(
                        instance.customer_name,
                        transection_type="cashin",
                        amount=down_payment,
                        customer_name=instance.customer_name,
                        received_by=getattr(instance, 'created_by', None),
                        modelname=f"Loan Down Payment (Loan ID: {instance.id})"
                    )
                total_amount = q2(max(Decimal('0'), total_amount - down_payment))
                print(f"Down Payment: {down_payment:.2f}, Remaining: {total_amount:.2f}")

            # 5) Main loan disbursement (principal outflow)
            create_transaction_with_customer_info(
                instance.customer_name,
                transection_type="cashout",
                amount=original_amount,
                customer_name=instance.customer_name,
                received_by=getattr(instance, 'created_by', None),
                modelname=f"Loan Disbursement (Loan ID: {instance.id})"
            )

            # 6) Create installments (sum == total_amount)
            n = len(dates)
            per_installment_amount = q2(total_amount / n) if n else Decimal('0')
            remaining_amount = total_amount

            installments = []
            for i, inst_date in enumerate(dates):
                if i == n - 1:
                    amount = q2(remaining_amount)  # remainder to last
                else:
                    amount = per_installment_amount
                    remaining_amount = q2(remaining_amount - amount)

                if amount <= 0:
                    break

                inst = Installment.objects.create(
                    customer_name=instance.customer_name,
                    installment_date=inst_date,
                    amount=amount,
                    installment_status="due",
                    area_name=instance.area_name,
                    branch_name=instance.branch_name,
                    loan_id=str(instance.id),
                    pay_from_account=instance.pay_from_account,
                    due_amount=amount
                )
                installments.append(inst)
                print(f"  Installment {i+1}: {inst_date} = {amount:.2f}")

            if installments:
                # attach installments
                instance.installment.set(installments)

                # IMPORTANT: updated_at manually touch কোরো না
                # শুধু normal save করলেই হবে (Common/Loan যেটা আছে সেটাই update হবে)
                instance.save()
                print(f"✅ {len(installments)} installments attached to Loan ID {instance.id}")


            # 7) Touch updated_at (optional; save above already did)
            Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

    except InsufficientBalanceError as e:
        print("⚠ Down payment skipped due to insufficient balance")
        raise ValidationError(str(e))
    except Exception as e:
        print(f"❌ Error creating installments: {str(e)}")
        raise

    
@receiver(post_save, sender=DailySaving)
def create_daily_saving_transaction(sender, instance, created, **kwargs):
    if created:
        if instance.amount < 0:
            print(f"Skipping transaction for negative DailySaving: {instance.amount}")
            return
        
        # Add to customer account balance
        update_customer_balance(instance.customer_name, instance.amount)
        
        create_transaction_with_customer_info(
            instance.customer_name,
            transection_type="cashin",
            amount=instance.amount,
            customer_name=instance.customer_name,
            received_by=instance.received_by,
            modelname=f"Daily Saving (ID: {instance.id})"
        )
        print(f"✓ Transaction created for DailySaving: {instance.amount:.2f}")


@receiver(pre_save, sender=Installment)
def store_old_installment_status(sender, instance, **kwargs):
    """Store old status and due amount before saving"""
    if instance.pk:
        try:
            old_instance = Installment.objects.get(pk=instance.pk)
            instance._old_status = old_instance.installment_status
            instance._old_pay = old_instance.installment_pay
            instance._old_due_amount = old_instance.due_amount
        except Installment.DoesNotExist:
            instance._old_status = None
            instance._old_pay = None
            instance._old_due_amount = None
    else:
        instance._old_status = None
        instance._old_pay = None
        instance._old_due_amount = None


@receiver(post_save, sender=Installment)
def handle_installment_payment(sender, instance, created, **kwargs):
    """
    Handle installment payment with pay_from_account logic and proper due tracking.
    Transaction is created with correct amount, paid_amount, and due_amount.
    """
    if created:
        return
    
    old_status = getattr(instance, '_old_status', None)
    old_pay = getattr(instance, '_old_pay', None)
    old_due_amount = getattr(instance, '_old_due_amount', None)
    
    # Check if payment is being made (i.e., installment_pay is updated)
    if not (old_pay != instance.installment_pay and instance.installment_pay):
        return
    
    print(f"\n--- Installment Payment: ID {instance.id} ---")
    
    installment_pay = Decimal(str(instance.installment_pay or 0))
    current_due = Decimal(str(instance.due_amount or instance.amount))
    
    if installment_pay <= 0:
        print("Warning: No payment amount recorded")
        return
    
    # If installment_pay > amount, extra payment should be treated as savings
    if installment_pay > instance.amount:
        actual_payment = instance.amount
        extra_amount = installment_pay - instance.amount
        print(f"💰 Payment: {installment_pay:.2f}, Due: {current_due:.2f}, Extra: {extra_amount:.2f}")
    else:
        actual_payment = installment_pay
        extra_amount = Decimal('0')
        print(f"💵 Payment: {installment_pay:.2f}, Due: {current_due:.2f}")
    
    # Create the transaction based on whether the payment is from the account or normal payment
    if instance.pay_from_account:
        print(f"💳 Pay from account enabled - processing account deduction...")
        
        try:
            # Check and deduct from account
            check_and_deduct_balance(
                instance.customer_name,
                installment_pay,  # Deduct total payment including extra
                f"Installment Payment ID: {instance.id}"
            )
            print(f"✓ Deducted {installment_pay:.2f} from account")
            
            # Create transaction for actual installment payment
            transaction = create_transaction_with_customer_info(
                instance.customer_name,
                transection_type="cashin",
                amount=instance.amount,  # Transaction amount = Installment amount
                customer_name=instance.customer_name,
                received_by=instance.received_by,
                modelname=f"Installment Payment from Account (ID: {instance.id}, Loan: {instance.loan_id})"
            )
            print(f"✓ Transaction created: {instance.amount:.2f}")

            # Set the paid_amount and due_amount in the transaction
            transaction.paid_amount = actual_payment  # Paid amount = Installment pay (or amount)
            transaction.due_amount = instance.due_amount - actual_payment  # Due amount = Installment due - paid amount
            transaction.save()
            
            # Calculate new due amount
            new_due_amount = current_due - actual_payment
            
            if new_due_amount <= 0:
                # Fully paid
                Installment.objects.filter(pk=instance.pk).update(
                    installment_status='paid',
                    due_amount=0
                )
                print(f"✅ Installment FULLY PAID! Due Amount: 0.00")
            else:
                # Partially paid
                Installment.objects.filter(pk=instance.pk).update(
                    installment_status='due',
                    due_amount=new_due_amount
                )
                print(f"⚠ Partial payment! Remaining Due: {new_due_amount:.2f}")
            
            # Handle extra payment (if any)
            if extra_amount > 0:
                print(f"💰 Extra payment: {extra_amount:.2f} - adding to account balance")
                
                # Add extra to customer account balance
                update_customer_balance(instance.customer_name, extra_amount)
                
                create_transaction_with_customer_info(
                    instance.customer_name,
                    transection_type="cashin",
                    amount=extra_amount,
                    customer_name=instance.customer_name,
                    received_by=instance.received_by,
                    modelname=f"Extra Payment Savings (Installment ID: {instance.id})"
                )
                print(f"✓ Extra amount added to balance: {extra_amount:.2f}")
            
        except InsufficientBalanceError as e:
            print(f"⚠ Payment REJECTED due to insufficient balance")
            # Reset payment fields - DO NOT process the payment
            Installment.objects.filter(pk=instance.pk).update(
                installment_pay=old_pay,  # Restore old payment
                installment_status=old_status,  # Restore old status
                due_amount=old_due_amount  # Restore old due amount
            )
            # Re-raise as ValidationError so API can catch it
            raise ValidationError(str(e))
    
    else:
        # Normal payment (not from account)
        print(f"💵 Normal payment processing...")

        # Create transaction for actual installment payment
        transaction = create_transaction_with_customer_info(
            instance.customer_name,
            transection_type="cashin",
            amount=instance.amount,  # Transaction amount = Installment amount
            customer_name=instance.customer_name,
            received_by=instance.received_by,
            modelname=f"Installment Payment (ID: {instance.id}, Loan: {instance.loan_id})"
        )
        print(f"✓ Transaction created: {instance.amount:.2f}")
        
        # Set the paid_amount and due_amount in the transaction
        transaction.paid_amount = actual_payment  # Paid amount = Installment pay
        transaction.due_amount = instance.due_amount - actual_payment  # Due amount = Installment due amount
        transaction.save()

        # Calculate new due amount
        new_due_amount = current_due - actual_payment
        
        if new_due_amount <= 0:
            # Fully paid
            Installment.objects.filter(pk=instance.pk).update(
                installment_status='paid',
                due_amount=0
            )
            print(f"✅ Installment FULLY PAID! Due Amount: 0.00")
        else:
            # Partially paid
            Installment.objects.filter(pk=instance.pk).update(
                installment_status='due',
                due_amount=new_due_amount
            )
            print(f"⚠ Partial payment! Remaining Due: {new_due_amount:.2f}")
        
        # Handle extra payment (if any)
        if extra_amount > 0:
            print(f"💰 Extra payment: {extra_amount:.2f} - adding to account balance")
            
            # Add extra to customer account balance
            update_customer_balance(instance.customer_name, extra_amount)
            
            create_transaction_with_customer_info(
                instance.customer_name,
                transection_type="cashin",
                amount=extra_amount,
                customer_name=instance.customer_name,
                received_by=instance.received_by,
                modelname=f"Extra Payment Savings (Installment ID: {instance.id})"
            )
            print(f"✓ Extra payment added to balance: {extra_amount:.2f}")



# @receiver(post_save, sender=Loan)
# def create_installments_on_loan_create(sender, instance, created, **kwargs):
#     if not created:
#         return

#     # 🔒 run only after DB commit (VERY IMPORTANT)
#     def _create():
#         installment_type = instance.installment_type
#         if not installment_type:
#             return

#         dates = generate_installment_dates(date.today(), installment_type)
#         if not dates:
#             return

#         total_amount = instance.amount
#         n = len(dates)
#         per_installment = (total_amount / n).quantize(Decimal("0.01"))
#         remaining = total_amount

#         installments = []

#         with transaction.atomic():
#             for i, inst_date in enumerate(dates):
#                 if i == n - 1:
#                     amount = remaining
#                 else:
#                     amount = per_installment
#                     remaining -= amount

#                 inst = Installment.objects.create(
#                     customer_name=instance.customer_name,
#                     installment_date=inst_date,
#                     amount=amount,
#                     due_amount=amount,
#                     installment_status="due",
#                     branch_name=instance.branch_name,
#                     area_name=instance.area_name,
#                     loan_id=str(instance.id),
#                     pay_from_account=instance.pay_from_account
#                 )
#                 installments.append(inst)

#             # ✅ attach installments to loan
#             instance.installment.set(installments)

#     transaction.on_commit(_create)



# @receiver(post_save, sender=Purchase)
# def increase_variation_stock_on_purchase(sender, instance, created, **kwargs):
#     if not created:
#         return

#     variation = instance.purchase_product_variation
#     qty = instance.qty

#     if variation and qty:
#         variation.quantity += qty
#         variation.save()
            



# @receiver(post_save, sender=Purchase)
# def increase_variation_stock_on_purchase(sender, instance, created, **kwargs):
#     if not created:
#         return

#     variation = instance.purchase_product_variation
#     qty = instance.qty

#     if not variation:
#         return

#     # 🔹 Increase stock
#     variation.quantity += qty
#     variation.save(update_fields=["quantity"])

#     # 🔹 Attach unickkeys if variation is unique
#     if variation.isunck:
#         variation.unickkey.add(*instance.unickkey.all())


from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Purchase


@receiver(m2m_changed, sender=Purchase.unickkey.through)
def attach_unick_to_variation(sender, instance, action, **kwargs):
    """
    When unickkey is added to Purchase,
    attach them to Variation if isunck=True
    """
    if action != "post_add":
        return

    variation = instance.purchase_product_variation

    if not variation or not variation.isunck:
        return

    # 🔥 THIS WILL NOW WORK
    variation.unickkey.add(*instance.unickkey.all())

@receiver(post_save, sender=Purchase)
def increase_variation_stock_on_purchase(sender, instance, created, **kwargs):
    if not created:
        return

    variation = instance.purchase_product_variation
    if variation:
        variation.quantity += instance.qty
        variation.save(update_fields=["quantity"])


@receiver(m2m_changed, sender=Purchase.unickkey.through)
def attach_unick_to_variation(sender, instance, action, **kwargs):
    if action == "post_add":
        variation = instance.purchase_product_variation
        if variation and variation.isunck:
            variation.unickkey.add(*instance.unickkey.all())

