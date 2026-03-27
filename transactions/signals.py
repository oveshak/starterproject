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

#     #  Original Loan Amount
#     original_amount = float(instance.amount)
#     total_amount = original_amount

#     #  LoanType behaviour_type calculation (percent = original_amount)
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

#     #  First Down Payment
#     if instance.first_down_payment:
#         total_amount -= float(instance.first_down_payment)
#         total_amount = max(total_amount, 0)
#         print(f"After First Down Payment Deduct: {total_amount:.2f}")

#     #  InstallmentType check
#     installment_type = instance.installment_type
#     if not installment_type:
#         print("No InstallmentType. Exiting.")
#         return

#     installment_amount = installment_type.instalment_cullect
#     if not installment_amount or installment_amount <= 0:
#         print("Invalid Installment Amount. Exiting.")
#         return

#     #  Generate installment dates
#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         print("No Installment Dates. Exiting.")
#         return

#     print(f"Generating {len(dates)} Installments (approx)")

#     #  Create installments
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

#     #  Update updated_at
#     if hasattr(instance, "updated_at"):
#         Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

import json
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import timedelta, date
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from contacts.models import Customer
from products.models import BranchProductStock, Variation
from .models import Loan, Installment, Purchase, PurchaseItem, Transection, DailySaving
from decimal import Decimal
from django.db import models
from django.core.exceptions import ValidationError
import traceback
import json
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Purchase

from decimal import Decimal, ROUND_HALF_UP
from datetime import date
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import transaction
from django.db.models import F
from rest_framework.exceptions import ValidationError



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



# def generate_installment_dates(start_date, installment_type):
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

#     #  KEY LOGIC:
#     # 1st installment = loan_date + instalment_cullect
#     first_date = start_date + delta

#     # Friday skip
#     current_date = get_next_valid_date(first_date)

#     for _ in range(total_installments):
#         dates.append(current_date)
#         current_date = get_next_valid_date(current_date + delta)

#     return dates

from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from django.core.exceptions import ValidationError

def generate_installment_dates(start_date, installment_type):
    dates = []
    frequency = installment_type.type
    total_duration_months = installment_type.total_duration or 12

    try:
        total_duration_months = float(total_duration_months)
    except (TypeError, ValueError):
        raise ValidationError("Total duration must be numeric.")

    if total_duration_months <= 0:
        return dates

    instalment_collect = installment_type.instalment_cullect or 1
    instalment_collect = int(instalment_collect)

    if frequency == "daily":
        total_installments = int(total_duration_months * 22)
        delta = timedelta(days=instalment_collect)

    elif frequency == "weekly":
        total_installments = int(total_duration_months * 4.3)
        delta = timedelta(weeks=instalment_collect)

    elif frequency == "monthly":
        if not total_duration_months.is_integer():
            raise ValidationError("For monthly installment, total duration must be a whole number.")
        total_installments = int(total_duration_months)
        delta = relativedelta(months=instalment_collect)

    elif frequency == "yearly":
        if not total_duration_months.is_integer():
            raise ValidationError("For yearly installment, total duration must be a whole number.")
        total_installments = max(1, int(total_duration_months) // 12)
        delta = relativedelta(years=instalment_collect)

    else:
        return dates

    first_date = start_date + delta
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
        print(f" Error updating customer balance: {str(e)}")


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
        print(f" {error_msg}")
        raise InsufficientBalanceError(error_msg)
    
    # Deduct from balance
    update_customer_balance(customer, -required_amount)
    return True





# @receiver(post_save, sender=Customer)
# def create_customer_type_transactions(sender, instance, created, **kwargs):
#     """
#     Create transactions based on customer type behavior when a new customer is created.
#     """
#     if not created:
#         return
   
#     try:
#         instance.refresh_from_db()
        
#         if not instance.coustomer_type:
#             print(f"No customer type assigned for Customer: {instance.full_name}")
#             return
           
#         if not instance.coustomer_type.behaviour_type:
#             print(f"No behaviors defined for customer type: {instance.coustomer_type.name}")
#             return
       
#         print(f"\n--- Customer Created: {instance.full_name} (ID: {instance.id}) ---")
#         print(f"Customer Type: {instance.coustomer_type.name}")
#         print(f"\nProcessing Customer Type behaviors...")
       
#         for item in instance.coustomer_type.behaviour_type:
#             try:
#                 behavior_name = item.get("name", "Unknown")
#                 amt = Decimal(str(item.get("amount", 0)))
               
#                 if amt <= 0:
#                     print(f"  Skipping {behavior_name}: Amount is 0")
#                     continue
               
#                 transaction_type = item.get("transaction_type", "cashout")
               
#                 if item.get("is_percent"):
#                     print(f"  ! {behavior_name} ({amt}%): Percentage-based behaviors not implemented")
#                     continue
               
#                 print(f"  + {behavior_name} (Fixed): {transaction_type.upper()} {amt:.2f}")
               
#                 transaction_data = {
#                     "transection_type": transaction_type,
#                     "amount": amt,
#                     "customer_name": instance,
#                     "modelname": f"Customer Type Behavior: {behavior_name}",
#                     "received_by": getattr(instance, "received_by", None),
#                 }
               
#                 if hasattr(instance, "created_by") and instance.created_by:
#                     transaction_data["received_by"] = instance.created_by
               
#                 transaction = create_transaction_with_customer_info(instance, **transaction_data)

#                 # only concrete fields
#                 transaction.paid_amount = amt
#                 transaction.due_amount = Decimal("0")
#                 transaction.save(update_fields=["paid_amount", "due_amount"])
                
#                 print(
#                     f"  ✓ Transaction created: ID {transaction.id} | "
#                     f"Amount: {transaction.amount} | Paid: {transaction.paid_amount} | Due: {transaction.due_amount}"
#                 )
               
#             except Exception as behavior_error:
#                 print(f"  ✗ Error processing behavior '{behavior_name}': {str(behavior_error)}")
#                 print(f"     Details: {traceback.format_exc()}")
#                 continue
       
#         print(f"Customer type transactions completed for {instance.full_name}")
       
#     except Exception as e:
#         print(f"\nSIGNAL ERROR for customer {instance.full_name}:")
#         print(f"Error: {str(e)}")
#         print(f"Traceback: {traceback.format_exc()}")

# @receiver(post_save, sender=Customer)
# def create_customer_type_transactions(sender, instance, created, **kwargs):
#     """
#     Create transactions based on customer type behavior when a new customer is created.
#     Update transactions automatically when customer is updated.
#     """
#     try:
#         instance.refresh_from_db()
        
#         if not instance.coustomer_type:
#             print(f"No customer type assigned for Customer: {instance.full_name}")
#             return
           
#         if not instance.coustomer_type.behaviour_type:
#             print(f"No behaviors defined for customer type: {instance.coustomer_type.name}")
#             return
       
#         if created:
#             print(f"\n--- Customer Created: {instance.full_name} (ID: {instance.id}) ---")
#         else:
#             print(f"\n--- Customer Updated: {instance.full_name} (ID: {instance.id}) ---")

#         print(f"Customer Type: {instance.coustomer_type.name}")
#         print(f"\nProcessing Customer Type behaviors...")
       
#         for item in instance.coustomer_type.behaviour_type:
#             try:
#                 behavior_name = item.get("name", "Unknown")
#                 amt = Decimal(str(item.get("amount", 0)))
               
#                 if amt <= 0:
#                     print(f"  Skipping {behavior_name}: Amount is 0")
#                     continue
               
#                 transaction_type = item.get("transaction_type", "cashout")
               
#                 if item.get("is_percent"):
#                     print(f"  ! {behavior_name} ({amt}%): Percentage-based behaviors not implemented")
#                     continue
               
#                 print(f"  + {behavior_name} (Fixed): {transaction_type.upper()} {amt:.2f}")
                
#                 modelname = f"Customer Type Behavior: {behavior_name}"
                
#                 transaction_data = {
#                     "transection_type": transaction_type,
#                     "amount": amt,
#                     "customer_name": instance,
#                     "modelname": modelname,
#                     "received_by": getattr(instance, "received_by", None),
#                 }
               
#                 if hasattr(instance, "created_by") and instance.created_by:
#                     transaction_data["received_by"] = instance.created_by

#                 if created:
#                     transaction = create_transaction_with_customer_info(instance, **transaction_data)
#                     print(f"  ✓ Transaction created: ID {transaction.id}")
#                 else:
#                     transaction = Transection.objects.filter(
#                         customer_name=instance,
#                         modelname=modelname
#                     ).first()

#                     if transaction:
#                         transaction.transection_type = transaction_type
#                         transaction.amount = amt
#                         transaction.customer_name = instance
#                         transaction.received_by = transaction_data["received_by"]
#                         transaction.modelname = modelname
#                         transaction.save()
#                         print(f"  ✓ Transaction updated: ID {transaction.id}")
#                     else:
#                         transaction = create_transaction_with_customer_info(instance, **transaction_data)
#                         print(f"  ✓ Transaction created (missing old one): ID {transaction.id}")

#                 # only concrete fields
#                 transaction.paid_amount = amt
#                 transaction.due_amount = Decimal("0")
#                 transaction.save(update_fields=["paid_amount", "due_amount"])
                
#                 print(
#                     f"  ✓ Transaction saved: ID {transaction.id} | "
#                     f"Amount: {transaction.amount} | Paid: {transaction.paid_amount} | Due: {transaction.due_amount}"
#                 )
               
#             except Exception as behavior_error:
#                 print(f"  ✗ Error processing behavior '{behavior_name}': {str(behavior_error)}")
#                 print(f"     Details: {traceback.format_exc()}")
#                 continue
       
#         print(f"Customer type transactions completed for {instance.full_name}")
       
#     except Exception as e:
#         print(f"\nSIGNAL ERROR for customer {instance.full_name}:")
#         print(f"Error: {str(e)}")
#         print(f"Traceback: {traceback.format_exc()}")









import traceback
from decimal import Decimal
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Customer, Transection


@receiver(pre_save, sender=Customer)
def store_old_customer_type(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_instance = Customer.objects.get(pk=instance.pk)
            instance._old_customer_type = old_instance.coustomer_type
        except Customer.DoesNotExist:
            instance._old_customer_type = None
    else:
        instance._old_customer_type = None


@receiver(post_save, sender=Customer)
def create_customer_type_transactions(sender, instance, created, **kwargs):
    """
    Create transactions based on customer type behavior when a new customer is created.
    Update transactions automatically when customer is updated.
    Only transaction create/update/delete হবে.
    Customer balance change হবে না.
    """
    try:
        if not instance.coustomer_type:
            print(f"No customer type assigned for Customer: {instance.full_name}")
            return

        if not instance.coustomer_type.behaviour_type:
            print(f"No behaviors defined for customer type: {instance.coustomer_type.name}")
            return

        if created:
            print(f"\n--- Customer Created: {instance.full_name} (ID: {instance.id}) ---")
        else:
            print(f"\n--- Customer Updated: {instance.full_name} (ID: {instance.id}) ---")

        print(f"Customer Type: {instance.coustomer_type.name}")
        print(f"Customer Type ID: {instance.coustomer_type_id}")
        print(f"\nProcessing Customer Type behaviors...")

        old_customer_type = getattr(instance, "_old_customer_type", None)

        old_behavior_names = set()
        if old_customer_type and old_customer_type.behaviour_type:
            old_behavior_names = {
                item.get("name", "Unknown")
                for item in old_customer_type.behaviour_type
            }

        new_behavior_names = set()

        for item in instance.coustomer_type.behaviour_type:
            try:
                behavior_name = item.get("name", "Unknown")
                new_behavior_names.add(behavior_name)

                amt = Decimal(str(item.get("amount", 0)))

                if amt <= 0:
                    print(f"  Skipping {behavior_name}: Amount is 0")
                    continue

                transaction_type = item.get("transaction_type", "cashout")

                if item.get("is_percent"):
                    print(f"  ! {behavior_name} ({amt}%): Percentage-based behaviors not implemented")
                    continue

                print(f"  + {behavior_name} (Fixed): {transaction_type.upper()} {amt:.2f}")

                modelname = f"Customer Type Behavior "

                transaction_data = {
                    "transection_type": transaction_type,
                    "amount": amt,
                    "customer_name": instance,
                    "modelname": modelname,
                    "received_by": getattr(instance, "received_by", None),
                }

                if hasattr(instance, "created_by") and instance.created_by:
                    transaction_data["received_by"] = instance.created_by

                # existing transaction খোঁজা
                transaction = Transection.objects.filter(
                    customer_name=instance,
                    modelname=modelname
                ).first()

                if transaction:
                    transaction.transection_type = transaction_type
                    transaction.amount = amt
                    transaction.customer_name = instance
                    transaction.received_by = transaction_data["received_by"]
                    transaction.modelname = modelname
                    transaction.save()

                    print(
                        f"  ✓ Transaction updated: ID {transaction.id} | "
                        f"Amount: {transaction.amount}"
                    )
                else:
                    transaction = create_transaction_with_customer_info(instance, **transaction_data)

                    print(
                        f"  ✓ Transaction created: ID {transaction.id} | "
                        f"Amount: {transaction.amount}"
                    )

                # paid / due set
                transaction.paid_amount = amt
                transaction.due_amount = Decimal("0")
                transaction.save(update_fields=["paid_amount", "due_amount"])

                print(
                    f"  ✓ Transaction saved: ID {transaction.id} | "
                    f"Amount: {transaction.amount} | Paid: {transaction.paid_amount} | Due: {transaction.due_amount}"
                )

            except Exception as behavior_error:
                print(f"  ✗ Error processing behavior '{behavior_name}': {str(behavior_error)}")
                print(f"     Details: {traceback.format_exc()}")
                continue

        # old customer type এর removed behavior delete
        if not created and old_behavior_names:
            removed_behaviors = old_behavior_names - new_behavior_names

            for behavior_name in removed_behaviors:
                deleted_count, _ = Transection.objects.filter(
                    customer_name=instance,
                    modelname=f"Customer Type Behavior: {behavior_name}"
                ).delete()

                print(
                    f"  ✓ Removed old behavior transaction: "
                    f"{behavior_name} | deleted={deleted_count}"
                )

        print(f"Customer type transactions completed for {instance.full_name}")

    except Exception as e:
        print(f"\nSIGNAL ERROR for customer {instance.full_name}:")
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")




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





# def deduct_branch_and_variation_stock(branch, variation, qty):
#     if qty <= 0:
#         raise ValidationError("Quantity must be positive")

#     # 🔒 lock branch stock row
#     branch_stock = (
#         BranchProductStock.objects
#         .select_for_update()
#         .filter(
#             stock_branch=branch,
#             product_variation=variation
#         )
#         .first()
#     )

#     if not branch_stock:
#         raise ValidationError(
#             f"No branch stock for variation {variation.id}"
#         )

#     #  validate BEFORE update (int vs int)
#     if branch_stock.quantity < qty:
#         raise ValidationError(
#             f"Branch stock insufficient. Have {branch_stock.quantity}, need {qty}"
#         )

#     if variation.quantity < qty:
#         raise ValidationError(
#             f"Variation stock insufficient. Have {variation.quantity}, need {qty}"
#         )

#     #  update WITHOUT triggering clean()
#     BranchProductStock.objects.filter(
#         id=branch_stock.id
#     ).update(
#         quantity=F("quantity") - qty
#     )

#     Variation.objects.filter(
#         id=variation.id
#     ).update(
#         quantity=F("quantity") - qty
#     )



# def deduct_branch_and_variation_stock(
#     *,
#     branch,
#     variation,
#     qty,
#     unique_key_id=None
# ):
#     """
#      Deduct quantity from:
#        - BranchProductStock.quantity
#        - Variation.quantity

#      If unique_key_id exists:
#        - remove from BranchProductStock.unickkey
#        - remove from Variation.unickkey (if exists)
#     """

#     if qty <= 0:
#         raise ValidationError("Quantity must be positive")

#     # 🔒 Lock branch stock row
#     branch_stock = (
#         BranchProductStock.objects
#         .select_for_update()
#         .filter(
#             stock_branch=branch,
#             product_variation=variation
#         )
#         .first()
#     )

#     if not branch_stock:
#         raise ValidationError(
#             f"No branch stock for variation {variation.id}"
#         )

#     # 🔒 Lock variation row
#     variation = (
#         Variation.objects
#         .select_for_update()
#         .get(id=variation.id)
#     )

#     #  Validate quantity
#     if branch_stock.quantity < qty:
#         raise ValidationError(
#             f"Branch stock insufficient "
#             f"(have {branch_stock.quantity}, need {qty})"
#         )

#     if variation.quantity < qty:
#         raise ValidationError(
#             f"Variation stock insufficient "
#             f"(have {variation.quantity}, need {qty})"
#         )

#     # 🔑 UNIQUE KEY CASE
#     if unique_key_id:
#         # Branch stock unickkey remove
#         if not branch_stock.unickkey.filter(id=unique_key_id).exists():
#             raise ValidationError(
#                 f"UniqueKey {unique_key_id} not found in branch stock"
#             )

#         branch_stock.unickkey.remove(unique_key_id)

#         # Variation unickkey remove (if relation exists)
#         if hasattr(variation, "unickkey"):
#             if variation.unickkey.filter(id=unique_key_id).exists():
#                 variation.unickkey.remove(unique_key_id)

#     #  Deduct quantities (DB-level atomic update)
#     BranchProductStock.objects.filter(
#         id=branch_stock.id
#     ).update(
#         quantity=F("quantity") - qty
#     )

#     Variation.objects.filter(
#         id=variation.id
#     ).update(
#         quantity=F("quantity") - qty
#     )




# @receiver(post_save, sender=Loan)
# def handle_loan_create(sender, instance, created, **kwargs):
#     if not created:
#         return

#     if instance.receive_type != "product":
#         return

#     if not instance.product_details:
#         return

#     with transaction.atomic():
#         for row in instance.product_details:
#             variation_id = row.get("variation_id")
#             qty = int(row.get("quantity", 0))

#             if not variation_id or qty <= 0:
#                 continue

#             try:
#                 variation = Variation.objects.select_for_update().get(
#                     id=variation_id
#                 )
#             except Variation.DoesNotExist:
#                 raise ValidationError(
#                     f"Variation {variation_id} not found"
#                 )

#             deduct_branch_and_variation_stock(
#                 branch=instance.branch_name,
#                 variation=variation,
#                 qty=qty
#             )




# @receiver(post_save, sender=Loan)
# def handle_loan_create(sender, instance, created, **kwargs):
#     if not created:
#         return

#     if instance.receive_type != "product":
#         return

#     if not instance.product_details:
#         return

#     #  JSONField safe parse
#     if isinstance(instance.product_details, str):
#         try:
#             rows = json.loads(instance.product_details)
#         except Exception:
#             raise ValidationError("Invalid product_details JSON")
#     else:
#         rows = instance.product_details

#     with transaction.atomic():
#         for row in rows:
#             variation_id = row.get("variation_id")
#             qty = int(row.get("quantity", 0))
#             unique_key_id = row.get("unique_key_id")

#             if not variation_id or qty <= 0:
#                 continue

#             try:
#                 variation = Variation.objects.get(id=variation_id)
#             except Variation.DoesNotExist:
#                 raise ValidationError(
#                     f"Variation {variation_id} not found"
#                 )

#             deduct_branch_and_variation_stock(
#                 branch=instance.branch_name,
#                 variation=variation,
#                 qty=qty,
#                 unique_key_id=unique_key_id
#             )

# @receiver(post_save, sender=Loan)
# def create_installments_and_transactions(sender, instance, created, **kwargs):
#     """
#     Create installments and transactions with auto-populated customer info
#     """
#     if not created:
#         return

#     print(f"\n--- Loan Created: ID {instance.id} ---")

#     original_amount = q2(instance.amount)
#     total_amount = original_amount

#     # 1) LoanType behavior charges
#     if instance.loan_type and instance.loan_type.behaviour_type:
#         print("Processing LoanType behaviors...")
#         for item in instance.loan_type.behaviour_type:
#             behavior_name = item.get("name", "Unknown")
#             amt = q2(item.get("amount", 0))
#             if item.get("is_percent"):
#                 added = q2(original_amount * amt / Decimal(100))
#                 total_amount = q2(total_amount + added)
#                 print(f"  + {behavior_name} ({amt}%): +{added:.2f}")
#                 create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashout",
#                     amount=added,
#                     customer_name=instance.customer_name,
#                     received_by=getattr(instance, 'created_by', None),
#                     modelname=f"Loan Behavior: {behavior_name}"
#                 )
#             else:
#                 total_amount = q2(total_amount + amt)
#                 print(f"  + {behavior_name} (Fixed): +{amt:.2f}")
#                 create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashout",
#                     amount=amt,
#                     customer_name=instance.customer_name,
#                     received_by=getattr(instance, 'created_by', None),
#                     modelname=f"Loan Behavior: {behavior_name}"
#                 )

#     print(f"Total Amount: {total_amount:.2f}")

#     # 2) Pre-validate installment type
#     installment_type = instance.installment_type
#     if not installment_type or not getattr(installment_type, "instalment_cullect", None) or installment_type.instalment_cullect <= 0:
#         print("Invalid Installment Amount. Exiting.")
#         return

#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         print("No Installment Dates. Exiting.")
#         return

#     print(f"Generating {len(dates)} Installments")

#     # ---- Everything below happens atomically ----
#     try:
#         with transaction.atomic():
#             # 3) If product loan, deduct branch stock now (row-locked)
#             _process_product_receipt(instance)

#             # 4) First down payment (apply ONCE)
#             down_payment = q2(instance.first_down_payment or 0)
#             if down_payment > 0:
#                 if instance.pay_from_account:
#                     print("Pay from account enabled - checking customer balance...")
#                     check_and_deduct_balance(
#                         instance.customer_name,
#                         down_payment,
#                         f"Down Payment for Loan ID: {instance.id}"
#                     )
#                     print(f"✓ Deducted {down_payment:.2f} from customer account")
#                     create_transaction_with_customer_info(
#                         instance.customer_name,
#                         transection_type="cashout",
#                         amount=down_payment,
#                         customer_name=instance.customer_name,
#                         received_by=getattr(instance, 'created_by', None),
#                         modelname=f"Down Payment from Account : {instance.id})"
#                     )
#                 else:
#                     create_transaction_with_customer_info(
#                         instance.customer_name,
#                         transection_type="cashin",
#                         amount=down_payment,
#                         customer_name=instance.customer_name,
#                         received_by=getattr(instance, 'created_by', None),
#                         modelname=f"Loan Down Payment : {instance.id})"
#                     )
#                 total_amount = q2(max(Decimal('0'), total_amount - down_payment))
#                 print(f"Down Payment: {down_payment:.2f}, Remaining: {total_amount:.2f}")

#             # 5) Main loan disbursement (principal outflow)
#             create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashout",
#                 amount=original_amount,
#                 customer_name=instance.customer_name,
#                 received_by=getattr(instance, 'created_by', None),
#                 modelname=f"Loan Disbursement : {instance.id})"
#             )

#             # 6) Create installments (sum == total_amount)
#             n = len(dates)
#             per_installment_amount = q2(total_amount / n) if n else Decimal('0')
#             remaining_amount = total_amount

#             installments = []
#             for i, inst_date in enumerate(dates):
#                 if i == n - 1:
#                     amount = q2(remaining_amount)  # remainder to last
#                 else:
#                     amount = per_installment_amount
#                     remaining_amount = q2(remaining_amount - amount)

#                 if amount <= 0:
#                     break

#                 inst = Installment.objects.create(
#                     customer_name=instance.customer_name,
#                     installment_date=inst_date,
#                     amount=amount,
#                     installment_status="due",
#                     area_name=instance.area_name,
#                     branch_name=instance.branch_name,
#                     loan_id=str(instance.id),
#                     pay_from_account=instance.pay_from_account,
#                     due_amount=amount
#                 )
#                 installments.append(inst)
#                 print(f"  Installment {i+1}: {inst_date} = {amount:.2f}")

#             if installments:
#                 # attach installments
#                 instance.installment.set(installments)

#                 # IMPORTANT: updated_at manually touch কোরো না
#                 # শুধু normal save করলেই হবে (Common/Loan যেটা আছে সেটাই update হবে)
#                 instance.save()
#                 print(f" {len(installments)} installments attached to Loan ID {instance.id}")


#             # 7) Touch updated_at (optional; save above already did)
#             Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

#     except InsufficientBalanceError as e:
#         print("⚠ Down payment skipped due to insufficient balance")
#         raise ValidationError(str(e))
#     except Exception as e:
#         print(f" Error creating installments: {str(e)}")
#         raise

    
# @receiver(post_save, sender=DailySaving)
# def create_daily_saving_transaction(sender, instance, created, **kwargs):
#     if created:
#         if instance.amount < 0:
#             print(f"Skipping transaction for negative DailySaving: {instance.amount}")
#             return
        
#         # Add to customer account balance
#         update_customer_balance(instance.customer_name, instance.amount)
        
#         create_transaction_with_customer_info(
#             instance.customer_name,
#             transection_type="cashin",
#             amount=instance.amount,
#             customer_name=instance.customer_name,
#             received_by=instance.received_by,
#             modelname=f"Daily Saving : {instance.id})"
#         )
#         print(f"✓ Transaction created for DailySaving: {instance.amount:.2f}")


# @receiver(pre_save, sender=Installment)
# def store_old_installment_status(sender, instance, **kwargs):
#     """Store old status and due amount before saving"""
#     if instance.pk:
#         try:
#             old_instance = Installment.objects.get(pk=instance.pk)
#             instance._old_status = old_instance.installment_status
#             instance._old_pay = old_instance.installment_pay
#             instance._old_due_amount = old_instance.due_amount
#         except Installment.DoesNotExist:
#             instance._old_status = None
#             instance._old_pay = None
#             instance._old_due_amount = None
#     else:
#         instance._old_status = None
#         instance._old_pay = None
#         instance._old_due_amount = None


# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Handle installment payment with pay_from_account logic and proper due tracking.
#     Transaction is created with correct amount, paid_amount, and due_amount.
#     """
#     if created:
#         return
    
#     old_status = getattr(instance, '_old_status', None)
#     old_pay = getattr(instance, '_old_pay', None)
#     old_due_amount = getattr(instance, '_old_due_amount', None)
    
#     # Check if payment is being made (i.e., installment_pay is updated)
#     if not (old_pay != instance.installment_pay and instance.installment_pay):
#         return
    
#     print(f"\n--- Installment Payment: ID {instance.id} ---")
    
#     installment_pay = Decimal(str(instance.installment_pay or 0))
#     current_due = Decimal(str(instance.due_amount or instance.amount))
    
#     if installment_pay <= 0:
#         print("Warning: No payment amount recorded")
#         return
    
#     # If installment_pay > amount, extra payment should be treated as savings
#     if installment_pay > instance.amount:
#         actual_payment = instance.amount
#         extra_amount = installment_pay - instance.amount
#         print(f" Payment: {installment_pay:.2f}, Due: {current_due:.2f}, Extra: {extra_amount:.2f}")
#     else:
#         actual_payment = installment_pay
#         extra_amount = Decimal('0')
#         print(f"Payment: {installment_pay:.2f}, Due: {current_due:.2f}")
    
#     # Create the transaction based on whether the payment is from the account or normal payment
#     if instance.pay_from_account:
#         print(f" Pay from account enabled - processing account deduction...")
        
#         try:
#             # Check and deduct from account
#             check_and_deduct_balance(
#                 instance.customer_name,
#                 installment_pay,  # Deduct total payment including extra
#                 f"Installment Payment ID: {instance.id}"
#             )
#             print(f"✓ Deducted {installment_pay:.2f} from account")
            
#             # Create transaction for actual installment payment
#             transaction = create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=instance.amount,  # Transaction amount = Installment amount
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id})"
#             )
#             print(f"✓ Transaction created: {instance.amount:.2f}")

#             # Set the paid_amount and due_amount in the transaction
#             transaction.paid_amount = actual_payment  # Paid amount = Installment pay (or amount)
#             transaction.due_amount = instance.due_amount - actual_payment  # Due amount = Installment due - paid amount
#             transaction.save()
            
#             # Calculate new due amount
#             new_due_amount = current_due - actual_payment
            
#             if new_due_amount <= 0:
#                 # Fully paid
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status='paid',
#                     due_amount=0
#                 )
#                 print(f" Installment FULLY PAID! Due Amount: 0.00")
#             else:
#                 # Partially paid
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status='due',
#                     due_amount=new_due_amount
#                 )
#                 print(f"⚠ Partial payment! Remaining Due: {new_due_amount:.2f}")
            
#             # Handle extra payment (if any)
#             if extra_amount > 0:
#                 print(f" Extra payment: {extra_amount:.2f} - adding to account balance")
                
#                 # Add extra to customer account balance
#                 update_customer_balance(instance.customer_name, extra_amount)
                
#                 create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashin",
#                     amount=extra_amount,
#                     customer_name=instance.customer_name,
#                     received_by=instance.received_by,
#                     modelname=f"Extra Payment Savings : {instance.id})"
#                 )
#                 print(f"✓ Extra amount added to balance: {extra_amount:.2f}")
            
#         except InsufficientBalanceError as e:
#             print(f"⚠ Payment REJECTED due to insufficient balance")
#             # Reset payment fields - DO NOT process the payment
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,  # Restore old payment
#                 installment_status=old_status,  # Restore old status
#                 due_amount=old_due_amount  # Restore old due amount
#             )
#             # Re-raise as ValidationError so API can catch it
#             raise ValidationError(str(e))
    
#     else:
#         # Normal payment (not from account)
#         print(f"Normal payment processing...")

#         # Create transaction for actual installment payment
#         transaction = create_transaction_with_customer_info(
#             instance.customer_name,
#             transection_type="cashin",
#             amount=instance.amount,  # Transaction amount = Installment amount
#             customer_name=instance.customer_name,
#             received_by=instance.received_by,
#             modelname=f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"
#         )
#         print(f"✓ Transaction created: {instance.amount:.2f}")
        
#         # Set the paid_amount and due_amount in the transaction
#         transaction.paid_amount = actual_payment  # Paid amount = Installment pay
#         transaction.due_amount = instance.due_amount - actual_payment  # Due amount = Installment due amount
#         transaction.save()

#         # Calculate new due amount
#         new_due_amount = current_due - actual_payment
        
#         if new_due_amount <= 0:
#             # Fully paid
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status='paid',
#                 due_amount=0
#             )
#             print(f" Installment FULLY PAID! Due Amount: 0.00")
#         else:
#             # Partially paid
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status='due',
#                 due_amount=new_due_amount
#             )
#             print(f"⚠ Partial payment! Remaining Due: {new_due_amount:.2f}")
        
#         # Handle extra payment (if any)
#         if extra_amount > 0:
#             print(f" Extra payment: {extra_amount:.2f} - adding to account balance")
            
#             # Add extra to customer account balance
#             update_customer_balance(instance.customer_name, extra_amount)
            
#             create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=extra_amount,
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=f"Extra Payment Savings : {instance.id})"
#             )
#             print(f"✓ Extra payment added to balance: {extra_amount:.2f}")


@receiver(post_save, sender=Loan)
def handle_loan_create(sender, instance, created, **kwargs):
    if not created:
        return

    if instance.receive_type != "product":
        return

    if not instance.product_details:
        return

    # JSONField safe parse
    if isinstance(instance.product_details, str):
        try:
            rows = json.loads(instance.product_details)
        except Exception:
            raise ValidationError("Invalid product_details JSON")
    else:
        rows = instance.product_details

    with transaction.atomic():
        for row in rows:
            variation_id = row.get("variation_id")
            qty = int(row.get("quantity", 0))

            # new format support
            unique_key_ids = row.get("unique_key_ids", None)

            # backward compatibility for old format
            if unique_key_ids is None:
                unique_key_id = row.get("unique_key_id")
                if unique_key_id:
                    unique_key_ids = [unique_key_id]
                else:
                    unique_key_ids = []

            if not variation_id or qty <= 0:
                continue

            try:
                variation = Variation.objects.get(id=variation_id)
            except Variation.DoesNotExist:
                raise ValidationError(
                    f"Variation {variation_id} not found"
                )

            deduct_branch_and_variation_stock(
                branch=instance.branch_name,
                variation=variation,
                qty=qty,
                unique_key_ids=unique_key_ids
            )


from decimal import Decimal
import json
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone


def mark_transaction_as_paid(transaction_obj, amount=None):
    """
    Mark selected transaction as fully paid.
    paid = True
    paid_amount = full amount
    due_amount = 0
    """
    if not transaction_obj:
        return transaction_obj

    full_amount = Decimal(str(
        amount if amount is not None else getattr(transaction_obj, "amount", 0) or 0
    ))

    update_fields = []

    if hasattr(transaction_obj, "paid"):
        transaction_obj.paid = True
        update_fields.append("paid")

    if hasattr(transaction_obj, "paid_amount"):
        transaction_obj.paid_amount = full_amount
        update_fields.append("paid_amount")

    if hasattr(transaction_obj, "due_amount"):
        transaction_obj.due_amount = Decimal("0")
        update_fields.append("due_amount")

    if update_fields:
        transaction_obj.save(update_fields=update_fields)

    return transaction_obj


# @receiver(post_save, sender=Loan)
# def handle_loan_create(sender, instance, created, **kwargs):
#     if not created:
#         return

#     if instance.receive_type != "product":
#         return

#     if not instance.product_details:
#         return

#     if isinstance(instance.product_details, str):
#         try:
#             rows = json.loads(instance.product_details)
#         except Exception:
#             raise ValidationError("Invalid product_details JSON")
#     else:
#         rows = instance.product_details

#     with transaction.atomic():
#         for row in rows:
#             variation_id = row.get("variation_id")
#             qty = int(row.get("quantity", 0))
#             unique_key_id = row.get("unique_key_id")

#             if not variation_id or qty <= 0:
#                 continue

#             try:
#                 variation = Variation.objects.get(id=variation_id)
#             except Variation.DoesNotExist:
#                 raise ValidationError(f"Variation {variation_id} not found")

#             deduct_branch_and_variation_stock(
#                 branch=instance.branch_name,
#                 variation=variation,
#                 qty=qty,
#                 unique_key_id=unique_key_id
#             )


# @receiver(post_save, sender=Loan)
# def create_installments_and_transactions(sender, instance, created, **kwargs):
#     """
#     Create installments and transactions with auto-populated customer info
#     """
#     if not created:
#         return

#     print(f"\n--- Loan Created: ID {instance.id} ---")

#     original_amount = q2(instance.amount)
#     total_amount = original_amount

#     # Loan Behavior -> always paid
#     if instance.loan_type and instance.loan_type.behaviour_type:
#         print("Processing LoanType behaviors...")
#         for item in instance.loan_type.behaviour_type:
#             behavior_name = item.get("name", "Unknown")
#             amt = q2(item.get("amount", 0))

#             if item.get("is_percent"):
#                 added = q2(original_amount * amt / Decimal(100))
#                 total_amount = q2(total_amount + added)
#                 print(f"  + {behavior_name} ({amt}%): +{added:.2f}")

#                 tx = create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashin",
#                     amount=added,
#                     customer_name=instance.customer_name,
#                     received_by=getattr(instance, "created_by", None),
#                     modelname=f"Loan Behavior: {behavior_name}"
#                 )
#                 mark_transaction_as_paid(tx, added)

#             else:
#                 total_amount = q2(total_amount + amt)
#                 print(f"  + {behavior_name} (Fixed): +{amt:.2f}")

#                 tx = create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashIn",
#                     amount=amt,
#                     customer_name=instance.customer_name,
#                     received_by=getattr(instance, "created_by", None),
#                     modelname=f"Loan Behavior: {behavior_name}"
#                 )
#                 mark_transaction_as_paid(tx, amt)

#     print(f"Total Amount: {total_amount:.2f}")

#     installment_type = instance.installment_type
#     if (
#         not installment_type
#         or not getattr(installment_type, "instalment_cullect", None)
#         or installment_type.instalment_cullect <= 0
#     ):
#         print("Invalid Installment Amount. Exiting.")
#         return

#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         print("No Installment Dates. Exiting.")
#         return

#     print(f"Generating {len(dates)} Installments")

#     try:
#         with transaction.atomic():
#             _process_product_receipt(instance)

#             # Loan Down Payment -> always paid
#             down_payment = q2(instance.first_down_payment or 0)
#             if down_payment > 0:
#                 if instance.pay_from_account:
#                     print("Pay from account enabled - checking customer balance...")
#                     check_and_deduct_balance(
#                         instance.customer_name,
#                         down_payment,
#                         f"Down Payment for Loan ID: {instance.id}"
#                     )
#                     print(f"✓ Deducted {down_payment:.2f} from customer account")

#                     tx = create_transaction_with_customer_info(
#                         instance.customer_name,
#                         transection_type="cashIn",
#                         amount=down_payment,
#                         customer_name=instance.customer_name,
#                         received_by=getattr(instance, "created_by", None),
#                         modelname=f"Loan Down Payment from Account : {instance.id})"
#                     )
#                     mark_transaction_as_paid(tx, down_payment)

#                 else:
#                     tx = create_transaction_with_customer_info(
#                         instance.customer_name,
#                         transection_type="cashin",
#                         amount=down_payment,
#                         customer_name=instance.customer_name,
#                         received_by=getattr(instance, "created_by", None),
#                         modelname=f"Loan Down Payment : {instance.id})"
#                     )
#                     mark_transaction_as_paid(tx, down_payment)

#                 total_amount = q2(max(Decimal("0"), total_amount - down_payment))
#                 print(f"Down Payment: {down_payment:.2f}, Remaining: {total_amount:.2f}")

#             # Main loan disbursement -> normal
#             create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashout",
#                 amount=original_amount,
#                 customer_name=instance.customer_name,
#                 received_by=getattr(instance, "created_by", None),
#                 modelname=f"Loan Disbursement : {instance.id})"
#             )

#             # Create installments
#             n = len(dates)
#             per_installment_amount = q2(total_amount / n) if n else Decimal("0")
#             remaining_amount = total_amount

#             installments = []
#             for i, inst_date in enumerate(dates):
#                 if i == n - 1:
#                     amount = q2(remaining_amount)
#                 else:
#                     amount = per_installment_amount
#                     remaining_amount = q2(remaining_amount - amount)

#                 if amount <= 0:
#                     break

#                 inst = Installment.objects.create(
#                     customer_name=instance.customer_name,
#                     installment_date=inst_date,
#                     amount=amount,
#                     installment_status="due",
#                     area_name=instance.area_name,
#                     branch_name=instance.branch_name,
#                     loan_id=str(instance.id),
#                     pay_from_account=instance.pay_from_account,
#                     due_amount=amount
#                 )
#                 installments.append(inst)
#                 print(f"  Installment {i + 1}: {inst_date} = {amount:.2f}")

#             if installments:
#                 instance.installment.set(installments)
#                 instance.save()
#                 print(f"{len(installments)} installments attached to Loan ID {instance.id}")

#             Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

#     except InsufficientBalanceError as e:
#         print("⚠ Down payment skipped due to insufficient balance")
#         raise ValidationError(str(e))
#     except Exception as e:
#         print(f"Error creating installments: {str(e)}")
#         raise















# import json
# from decimal import Decimal
# from datetime import date

# from django.core.exceptions import ValidationError
# from django.db import transaction
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone

# from .models import Loan, Installment, Variation, Transection
# # যদি Transaction অন্য app এ থাকে, তাহলে উপরের import বদলাও
# # example:
# # from transactions.models import Transaction


# # =========================================================
# # Helpers
# # =========================================================

# class InsufficientBalanceError(Exception):
#     pass


# def q2(value):
#     return Decimal(value).quantize(Decimal("0.01"))


# def loan_behavior_modelname(loan_id, behavior_name):
#     return f"Loan Behavior | Loan: {loan_id} | Name: {behavior_name}"


# def loan_down_payment_modelname(loan_id):
#     return f"Loan Down Payment | Loan: {loan_id}"


# def loan_disbursement_modelname(loan_id):
#     return f"Loan Disbursement | Loan: {loan_id}"


# def get_existing_transaction(customer, modelname):
#     return Transection.objects.filter(
#         customer_name=customer,
#         modelname=modelname
#     ).first()


# def create_or_update_transaction(
#     *,
#     customer,
#     transection_type,
#     amount,
#     received_by,
#     modelname,
#     mark_paid=False
# ):
#     """
#     Same modelname থাকলে update করবে, না থাকলে create করবে.
#     """
#     tx = get_existing_transaction(customer, modelname)

#     if tx:
#         tx.transection_type = transection_type
#         tx.amount = amount
#         tx.customer_name = customer
#         tx.received_by = received_by
#         tx.modelname = modelname

#         update_fields = [
#             "transection_type",
#             "amount",
#             "customer_name",
#             "received_by",
#             "modelname",
#         ]
#         if hasattr(tx, "updated_at"):
#             update_fields.append("updated_at")

#         tx.save(update_fields=update_fields)
#     else:
#         tx = create_transaction_with_customer_info(
#             customer,
#             transection_type=transection_type,
#             amount=amount,
#             customer_name=customer,
#             received_by=received_by,
#             modelname=modelname
#         )

#     if mark_paid:
#         mark_transaction_as_paid(tx, amount)

#     return tx


# def delete_removed_behavior_transactions(instance, valid_modelnames):
#     """
#     Loan behavior list থেকে remove হওয়া old behavior transaction delete করবে.
#     """
#     Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname__startswith=f"Loan Behavior | Loan: {instance.id} |"
#     ).exclude(modelname__in=valid_modelnames).delete()


# # =========================================================
# # Product stock processing
# # =========================================================

# def sync_product_stock_on_create_only(instance, created):
#     """
#     Product stock deduction শুধু create এ হবে.
#     Update এ stock auto-adjust করছি না, কারণ old/new diff লাগবে.
#     """
#     if not created:
#         return

#     if instance.receive_type != "product":
#         return

#     if not instance.product_details:
#         return

#     if isinstance(instance.product_details, str):
#         try:
#             rows = json.loads(instance.product_details)
#         except Exception:
#             raise ValidationError("Invalid product_details JSON")
#     else:
#         rows = instance.product_details

#     for row in rows:
#         variation_id = row.get("variation_id")
#         qty = int(row.get("quantity", 0))
#         unique_key_id = row.get("unique_key_id")

#         if not variation_id or qty <= 0:
#             continue

#         try:
#             variation = Variation.objects.get(id=variation_id)
#         except Variation.DoesNotExist:
#             raise ValidationError(f"Variation {variation_id} not found")

#         deduct_branch_and_variation_stock(
#             branch=instance.branch_name,
#             variation=variation,
#             qty=qty,
#             unique_key_id=unique_key_id
#         )


# # =========================================================
# # Transaction sync
# # =========================================================

# def sync_loan_transactions(instance):
#     """
#     Loan create/update এ সব related transaction sync করবে.
#     Return করবে installment এর জন্য final total_amount.
#     """
#     original_amount = q2(instance.amount or 0)
#     total_amount = original_amount
#     received_by = getattr(instance, "created_by", None)

#     valid_behavior_modelnames = []

#     # -------------------------
#     # 1) Loan behavior charges
#     # -------------------------
#     if instance.loan_type and instance.loan_type.behaviour_type:
#         for item in instance.loan_type.behaviour_type:
#             behavior_name = item.get("name", "Unknown")
#             amt = q2(item.get("amount", 0))
#             is_percent = item.get("is_percent", False)

#             modelname = loan_behavior_modelname(instance.id, behavior_name)
#             valid_behavior_modelnames.append(modelname)

#             if is_percent:
#                 added = q2(original_amount * amt / Decimal("100"))
#                 total_amount = q2(total_amount + added)

#                 create_or_update_transaction(
#                     customer=instance.customer_name,
#                     transection_type="cashin",
#                     amount=added,
#                     received_by=received_by,
#                     modelname=modelname,
#                     mark_paid=True
#                 )
#             else:
#                 total_amount = q2(total_amount + amt)

#                 create_or_update_transaction(
#                     customer=instance.customer_name,
#                     transection_type="cashin",
#                     amount=amt,
#                     received_by=received_by,
#                     modelname=modelname,
#                     mark_paid=True
#                 )

#     delete_removed_behavior_transactions(instance, valid_behavior_modelnames)

#     # -------------------------
#     # 2) Down payment
#     # -------------------------
#     down_payment = q2(instance.first_down_payment or 0)
#     dp_modelname = loan_down_payment_modelname(instance.id)

#     if down_payment > 0:
#         # pay_from_account check/deduct only on create হলে করবা
#         # update এ balance আবার deduct না করাই safer
#         create_or_update_transaction(
#             customer=instance.customer_name,
#             transection_type="cashin",
#             amount=down_payment,
#             received_by=received_by,
#             modelname=dp_modelname,
#             mark_paid=True
#         )
#         total_amount = q2(max(Decimal("0"), total_amount - down_payment))
#     else:
#         Transection.objects.filter(
#             customer_name=instance.customer_name,
#             modelname=dp_modelname
#         ).delete()

#     # -------------------------
#     # 3) Main loan disbursement
#     # -------------------------
#     disbursement_modelname = loan_disbursement_modelname(instance.id)
#     create_or_update_transaction(
#         customer=instance.customer_name,
#         transection_type="cashout",
#         amount=original_amount,
#         received_by=received_by,
#         modelname=disbursement_modelname,
#         mark_paid=False
#     )

#     return total_amount


# # =========================================================
# # Installment sync
# # =========================================================

# def sync_loan_installments(instance, total_amount):
#     """
#     Duplicate avoid করতে old installments delete করে নতুন করে create করবে.
#     """
#     installment_type = instance.installment_type
#     if (
#         not installment_type
#         or not getattr(installment_type, "instalment_cullect", None)
#         or installment_type.instalment_cullect <= 0
#     ):
#         instance.installment.clear()
#         Installment.objects.filter(loan_id=str(instance.id)).delete()
#         return

#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         instance.installment.clear()
#         Installment.objects.filter(loan_id=str(instance.id)).delete()
#         return

#     # IMPORTANT:
#     # old installments first clear + delete
#     # এতে duplicate বন্ধ হবে
#     old_installments = Installment.objects.filter(loan_id=str(instance.id))
#     instance.installment.clear()
#     old_installments.delete()

#     n = len(dates)
#     per_installment_amount = q2(total_amount / n) if n else Decimal("0")
#     remaining_amount = total_amount

#     new_installments = []

#     for i, inst_date in enumerate(dates):
#         if i == n - 1:
#             amount = q2(remaining_amount)
#         else:
#             amount = per_installment_amount
#             remaining_amount = q2(remaining_amount - amount)

#         if amount <= 0:
#             continue

#         inst = Installment.objects.create(
#             customer_name=instance.customer_name,
#             installment_date=inst_date,
#             amount=amount,
#             installment_status="due",
#             area_name=instance.area_name,
#             branch_name=instance.branch_name,
#             loan_id=str(instance.id),
#             pay_from_account=instance.pay_from_account,
#             due_amount=amount
#         )
#         new_installments.append(inst)

#     if new_installments:
#         instance.installment.set(new_installments)


# # =========================================================
# # Main signal
# # =========================================================

# @receiver(post_save, sender=Loan, dispatch_uid="loan_create_update_sync_signal")
# def handle_loan_create_or_update(sender, instance, created, **kwargs):
#     """
#     Loan create/update দুই ক্ষেত্রেই run করবে.
#     """
#     try:
#         with transaction.atomic():
#             # Product stock only on create
#             sync_product_stock_on_create_only(instance, created)

#             # Transactions create/update
#             total_amount = sync_loan_transactions(instance)

#             # Installments recreate
#             sync_loan_installments(instance, total_amount)

#             # direct update, no instance.save() here
#             Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

#     except InsufficientBalanceError as e:
#         raise ValidationError(str(e))
#     except Exception as e:
#         print(f"Error syncing loan data: {str(e)}")
#         raise






import json
from decimal import Decimal
from datetime import date

from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import (
    Loan,
    Installment,
    
    Transection,
   
)
# যদি Transaction অন্য app এ থাকে, তাহলে উপরের import বদলাও


# =========================================================
# Helpers
# =========================================================

class InsufficientBalanceError(Exception):
    pass


def q2(value):
    return Decimal(value).quantize(Decimal("0.01"))


def loan_behavior_modelname(loan_id, behavior_name):
    return f"Loan Behavior | Loan: {loan_id} | Name: {behavior_name}"


def loan_down_payment_modelname(loan_id):
    return f"Loan Down Payment | Loan: {loan_id}"


def loan_disbursement_modelname(loan_id):
    return f"Loan Disbursement | Loan: {loan_id}"


def get_existing_transaction(customer, modelname):
    return Transection.objects.filter(
        customer_name=customer,
        modelname=modelname
    ).first()


def create_or_update_transaction(
    *,
    customer,
    transection_type,
    amount,
    received_by,
    modelname,
    mark_paid=False
):
    """
    Same modelname থাকলে update করবে, না থাকলে create করবে.
    """
    tx = get_existing_transaction(customer, modelname)

    if tx:
        tx.transection_type = transection_type
        tx.amount = amount
        tx.customer_name = customer
        tx.received_by = received_by
        tx.modelname = modelname

        update_fields = [
            "transection_type",
            "amount",
            "customer_name",
            "received_by",
            "modelname",
        ]
        if hasattr(tx, "updated_at"):
            update_fields.append("updated_at")

        tx.save(update_fields=update_fields)
    else:
        tx = create_transaction_with_customer_info(
            customer,
            transection_type=transection_type,
            amount=amount,
            customer_name=customer,
            received_by=received_by,
            modelname=modelname
        )

    if mark_paid:
        mark_transaction_as_paid(tx, amount)

    return tx


def delete_removed_behavior_transactions(instance, valid_modelnames):
    """
    Loan behavior list থেকে remove হওয়া old behavior transaction delete করবে.
    """
    Transection.objects.filter(
        customer_name=instance.customer_name,
        modelname__startswith=f"Loan Behavior | Loan: {instance.id} |"
    ).exclude(modelname__in=valid_modelnames).delete()


# =========================================================
# Product stock processing
# =========================================================

def deduct_branch_and_variation_stock(
    *,
    branch,
    variation,
    qty,
    unique_key_ids=None,
    unique_key_id=None
):
    if qty <= 0:
        raise ValidationError("Quantity must be positive")

    if unique_key_ids is None:
        if unique_key_id is not None:
            unique_key_ids = [unique_key_id]
        else:
            unique_key_ids = []

    if not isinstance(unique_key_ids, list):
        unique_key_ids = [unique_key_ids]

    # lock branch stock
    branch_stock = (
        BranchProductStock.objects
        .select_for_update()
        .filter(
            stock_branch=branch,
            product_variation=variation
        )
        .first()
    )

    print("DEBUG BEFORE branch =", branch)
    print("DEBUG BEFORE variation =", variation.id)
    print("DEBUG BEFORE requested qty =", qty)
    print("DEBUG BEFORE unique_key_ids =", unique_key_ids)
    print("DEBUG BEFORE branch_stock id =", branch_stock.id if branch_stock else None)
    print("DEBUG BEFORE branch_stock qty =", branch_stock.quantity if branch_stock else None)

    if not branch_stock:
        raise ValidationError(f"No branch stock for variation {variation.id}")

    variation = (
        Variation.objects
        .select_for_update()
        .get(id=variation.id)
    )

    print("DEBUG BEFORE variation qty =", variation.quantity)
    print("DEBUG BEFORE branch_stock keys =", list(branch_stock.unickkey.values_list("id", flat=True)))
    if hasattr(variation, "unickkey"):
        print("DEBUG BEFORE variation keys =", list(variation.unickkey.values_list("id", flat=True)))

    if branch_stock.quantity < qty:
        raise ValidationError(
            f"Branch stock insufficient (have {branch_stock.quantity}, need {qty})"
        )

    if variation.quantity < qty:
        raise ValidationError(
            f"Variation stock insufficient (have {variation.quantity}, need {qty})"
        )

    if unique_key_ids:
        if len(unique_key_ids) != qty:
            raise ValidationError(
                f"Quantity ({qty}) and unique_key_ids count ({len(unique_key_ids)}) must match"
            )

        existing_branch_key_ids = set(
            branch_stock.unickkey.filter(id__in=unique_key_ids).values_list("id", flat=True)
        )
        missing_branch_keys = set(unique_key_ids) - existing_branch_key_ids
        if missing_branch_keys:
            raise ValidationError(
                f"UniqueKey(s) not found in branch stock: {sorted(missing_branch_keys)}"
            )

        branch_stock.unickkey.remove(*unique_key_ids)

        if hasattr(variation, "unickkey"):
            existing_variation_key_ids = set(
                variation.unickkey.filter(id__in=unique_key_ids).values_list("id", flat=True)
            )
            if existing_variation_key_ids:
                variation.unickkey.remove(*list(existing_variation_key_ids))

    BranchProductStock.objects.filter(id=branch_stock.id).update(
        quantity=F("quantity") - qty
    )

    Variation.objects.filter(id=variation.id).update(
        quantity=F("quantity") - qty
    )

    # fresh read from DB
    fresh_branch_stock = BranchProductStock.objects.get(id=branch_stock.id)
    fresh_variation = Variation.objects.get(id=variation.id)

    print("DEBUG AFTER branch_stock qty =", fresh_branch_stock.quantity)
    print("DEBUG AFTER variation qty =", fresh_variation.quantity)
    print("DEBUG AFTER branch_stock keys =", list(fresh_branch_stock.unickkey.values_list("id", flat=True)))
    if hasattr(fresh_variation, "unickkey"):
        print("DEBUG AFTER variation keys =", list(fresh_variation.unickkey.values_list("id", flat=True)))


def sync_product_stock_on_create_only(instance, created):
    """
    Product stock deduction শুধু create এ হবে.
    Update এ stock auto-adjust করছি না, কারণ old/new diff লাগবে.
    """
    if not created:
        return

    if instance.receive_type != "product":
        return

    if not instance.product_details:
        return

    if isinstance(instance.product_details, str):
        try:
            rows = json.loads(instance.product_details)
        except Exception:
            raise ValidationError("Invalid product_details JSON")
    else:
        rows = instance.product_details

    for row in rows:
        variation_id = row.get("variation_id")
        qty = int(row.get("quantity", 0))

        # support both old and new format
        unique_key_ids = row.get("unique_key_ids", None)

        # backward compatibility
        if unique_key_ids is None:
            single_unique_key_id = row.get("unique_key_id")
            if single_unique_key_id:
                unique_key_ids = [single_unique_key_id]
            else:
                unique_key_ids = []

        if not variation_id or qty <= 0:
            continue

        try:
            variation = Variation.objects.get(id=variation_id)
        except Variation.DoesNotExist:
            raise ValidationError(f"Variation {variation_id} not found")

        deduct_branch_and_variation_stock(
            branch=instance.branch_name,
            variation=variation,
            qty=qty,
            unique_key_ids=unique_key_ids
        )


# =========================================================
# Transaction sync
# =========================================================

def sync_loan_transactions(instance):
    """
    Loan create/update এ সব related transaction sync করবে.
    Return করবে installment এর জন্য final total_amount.
    """
    original_amount = q2(instance.amount or 0)
    total_amount = original_amount
    received_by = getattr(instance, "created_by", None)

    valid_behavior_modelnames = []

    # -------------------------
    # 1) Loan behavior charges
    # -------------------------
    if instance.loan_type and instance.loan_type.behaviour_type:
        for item in instance.loan_type.behaviour_type:
            behavior_name = item.get("name", "Unknown")
            amt = q2(item.get("amount", 0))
            is_percent = item.get("is_percent", False)

            modelname = loan_behavior_modelname(instance.id, behavior_name)
            valid_behavior_modelnames.append(modelname)

            if is_percent:
                added = q2(original_amount * amt / Decimal("100"))
                total_amount = q2(total_amount + added)

                create_or_update_transaction(
                    customer=instance.customer_name,
                    transection_type="cashin",
                    amount=added,
                    received_by=received_by,
                    modelname=modelname,
                    mark_paid=True
                )
            else:
                total_amount = q2(total_amount + amt)

                create_or_update_transaction(
                    customer=instance.customer_name,
                    transection_type="cashin",
                    amount=amt,
                    received_by=received_by,
                    modelname=modelname,
                    mark_paid=True
                )

    delete_removed_behavior_transactions(instance, valid_behavior_modelnames)

    # -------------------------
    # 2) Down payment
    # -------------------------
    down_payment = q2(instance.first_down_payment or 0)
    dp_modelname = loan_down_payment_modelname(instance.id)

    if down_payment > 0:
        create_or_update_transaction(
            customer=instance.customer_name,
            transection_type="cashin",
            amount=down_payment,
            received_by=received_by,
            modelname=dp_modelname,
            mark_paid=True
        )
        total_amount = q2(max(Decimal("0"), total_amount - down_payment))
    else:
        Transection.objects.filter(
            customer_name=instance.customer_name,
            modelname=dp_modelname
        ).delete()

    # -------------------------
    # 3) Main loan disbursement
    # -------------------------
    disbursement_modelname = loan_disbursement_modelname(instance.id)
    create_or_update_transaction(
        customer=instance.customer_name,
        transection_type="cashout",
        amount=original_amount,
        received_by=received_by,
        modelname=disbursement_modelname,
        mark_paid=False
    )

    return total_amount


# =========================================================
# Installment sync
# =========================================================

def sync_loan_installments(instance, total_amount):
    """
    Duplicate avoid করতে old installments delete করে নতুন করে create করবে.
    """
    installment_type = instance.installment_type
    if (
        not installment_type
        or not getattr(installment_type, "instalment_cullect", None)
        or installment_type.instalment_cullect <= 0
    ):
        instance.installment.clear()
        Installment.objects.filter(loan_id=str(instance.id)).delete()
        return

    start_date = date.today()
    dates = generate_installment_dates(start_date, installment_type)
    if not dates:
        instance.installment.clear()
        Installment.objects.filter(loan_id=str(instance.id)).delete()
        return

    old_installments = Installment.objects.filter(loan_id=str(instance.id))
    instance.installment.clear()
    old_installments.delete()

    n = len(dates)
    per_installment_amount = q2(total_amount / n) if n else Decimal("0")
    remaining_amount = total_amount

    new_installments = []

    for i, inst_date in enumerate(dates):
        if i == n - 1:
            amount = q2(remaining_amount)
        else:
            amount = per_installment_amount
            remaining_amount = q2(remaining_amount - amount)

        if amount <= 0:
            continue

        inst = Installment.objects.create(
            customer_name=instance.customer_name,
            installment_date=inst_date,
            amount=amount,
            installment_status="due",
            area_name=instance.area_name,
            branch_name=instance.branch_name,
            customergroup_name=instance.customergroup_name,
            loan_id=str(instance.id),
            pay_from_account=instance.pay_from_account,
            due_amount=amount
        )
        new_installments.append(inst)

    if new_installments:
        instance.installment.set(new_installments)


# =========================================================
# Main signal
# =========================================================
@receiver(post_save, sender=Loan, dispatch_uid="loan_create_update_sync_signal")
def handle_loan_create_or_update(sender, instance, created, **kwargs):
    print("DEBUG signal called | loan id =", instance.pk, "| created =", created)
    """
    Loan create/update দুই ক্ষেত্রেই run করবে.
    """
    try:
        with transaction.atomic():
            # Product stock only separate signal এ handle হবে
            # sync_product_stock_on_create_only(instance, created)

            # Transactions create/update
            total_amount = sync_loan_transactions(instance)

            # Installments recreate
            sync_loan_installments(instance, total_amount)

            # direct update, no instance.save() here
            Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

    except InsufficientBalanceError as e:
        raise ValidationError(str(e))
    except Exception as e:
        print(f"Error syncing loan data: {str(e)}")
        raise





























# import json
# import traceback
# from decimal import Decimal
# from datetime import date

# from django.core.exceptions import ValidationError
# from django.db import transaction
# from django.db.models import F
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils import timezone

# from .models import (
#     Loan,
#     Installment,
#     Transection,
#     Customer,
#     # BranchProductStock,
#     # Variation,
# )


# # =========================================================
# # Helpers
# # =========================================================

# class InsufficientBalanceError(Exception):
#     pass


# def q2(value):
#     return Decimal(str(value or 0)).quantize(Decimal("0.01"))


# def loan_behavior_modelname(loan_id, behavior_name):
#     return f"Loan Behavior | Loan: {loan_id} | Name: {behavior_name}"


# def loan_down_payment_modelname(loan_id):
#     return f"Loan Down Payment | Loan: {loan_id}"


# def loan_disbursement_modelname(loan_id):
#     return f"Loan Disbursement | Loan: {loan_id}"


# def get_existing_transaction(customer, modelname):
#     return Transection.objects.filter(
#         customer_name=customer,
#         modelname=modelname
#     ).first()


# def create_transaction_with_customer_info(
#     *,
#     customer,
#     transection_type,
#     amount,
#     customer_name,
#     received_by,
#     modelname
# ):
#     """
#     New Transection create করবে।
#     এখানে customer/customer_name দুটোই Customer instance হবে।
#     """
#     tx = Transection.objects.create(
#         transection_type=transection_type,
#         amount=q2(amount),
#         paid_amount=None,
#         due_amount=q2(amount) if transection_type == "cashout" else Decimal("0.00"),
#         customer_name=customer_name,
#         received_by=received_by,
#         modelname=modelname,
#     )
#     return tx


# def mark_transaction_as_paid(tx, amount):
#     """
#     Transaction কে paid-like state এ নেবে।
#     """
#     amount = q2(amount)

#     update_fields = []

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount
#         update_fields.append("paid_amount")

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0.00")
#         update_fields.append("due_amount")

#     if update_fields:
#         tx.save(update_fields=update_fields)
#     else:
#         tx.save()


# def create_or_update_transaction(
#     *,
#     customer,
#     transection_type,
#     amount,
#     received_by,
#     modelname,
#     mark_paid=False
# ):
#     """
#     Same modelname থাকলে update করবে, না থাকলে create করবে.
#     """
#     amount = q2(amount)
#     tx = get_existing_transaction(customer, modelname)

#     if tx:
#         tx.transection_type = transection_type
#         tx.amount = amount
#         tx.customer_name = customer
#         tx.received_by = received_by
#         tx.modelname = modelname

#         # cashin হলে due 0, cashout হলে due = amount (unless mark_paid)
#         if hasattr(tx, "due_amount"):
#             tx.due_amount = Decimal("0.00") if transection_type == "cashin" else amount

#         update_fields = [
#             "transection_type",
#             "amount",
#             "customer_name",
#             "received_by",
#             "modelname",
#         ]

#         if hasattr(tx, "due_amount"):
#             update_fields.append("due_amount")

#         if hasattr(tx, "updated_at"):
#             update_fields.append("updated_at")

#         tx.save(update_fields=update_fields)
#     else:
#         tx = create_transaction_with_customer_info(
#             customer=customer,
#             transection_type=transection_type,
#             amount=amount,
#             customer_name=customer,
#             received_by=received_by,
#             modelname=modelname
#         )

#     if mark_paid:
#         mark_transaction_as_paid(tx, amount)

#     return tx


# def delete_removed_behavior_transactions(instance, valid_modelnames):
#     """
#     Loan behavior list থেকে remove হওয়া old behavior transaction delete করবে.
#     """
#     Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname__startswith=f"Loan Behavior | Loan: {instance.id} |"
#     ).exclude(modelname__in=valid_modelnames).delete()


# # =========================================================
# # Optional: Product stock processing
# # =========================================================

# def deduct_branch_and_variation_stock(
#     *,
#     branch,
#     variation,
#     qty,
#     unique_key_ids=None,
#     unique_key_id=None
# ):
#     if qty <= 0:
#         raise ValidationError("Quantity must be positive")

#     if unique_key_ids is None:
#         if unique_key_id is not None:
#             unique_key_ids = [unique_key_id]
#         else:
#             unique_key_ids = []

#     if not isinstance(unique_key_ids, list):
#         unique_key_ids = [unique_key_ids]

#     branch_stock = (
#         BranchProductStock.objects
#         .select_for_update()
#         .filter(
#             stock_branch=branch,
#             product_variation=variation
#         )
#         .first()
#     )

#     print("DEBUG BEFORE branch =", branch)
#     print("DEBUG BEFORE variation =", variation.id)
#     print("DEBUG BEFORE requested qty =", qty)
#     print("DEBUG BEFORE unique_key_ids =", unique_key_ids)
#     print("DEBUG BEFORE branch_stock id =", branch_stock.id if branch_stock else None)
#     print("DEBUG BEFORE branch_stock qty =", branch_stock.quantity if branch_stock else None)

#     if not branch_stock:
#         raise ValidationError(f"No branch stock for variation {variation.id}")

#     variation = (
#         Variation.objects
#         .select_for_update()
#         .get(id=variation.id)
#     )

#     print("DEBUG BEFORE variation qty =", variation.quantity)
#     print("DEBUG BEFORE branch_stock keys =", list(branch_stock.unickkey.values_list("id", flat=True)))
#     if hasattr(variation, "unickkey"):
#         print("DEBUG BEFORE variation keys =", list(variation.unickkey.values_list("id", flat=True)))

#     if branch_stock.quantity < qty:
#         raise ValidationError(
#             f"Branch stock insufficient (have {branch_stock.quantity}, need {qty})"
#         )

#     if variation.quantity < qty:
#         raise ValidationError(
#             f"Variation stock insufficient (have {variation.quantity}, need {qty})"
#         )

#     if unique_key_ids:
#         if len(unique_key_ids) != qty:
#             raise ValidationError(
#                 f"Quantity ({qty}) and unique_key_ids count ({len(unique_key_ids)}) must match"
#             )

#         existing_branch_key_ids = set(
#             branch_stock.unickkey.filter(id__in=unique_key_ids).values_list("id", flat=True)
#         )
#         missing_branch_keys = set(unique_key_ids) - existing_branch_key_ids
#         if missing_branch_keys:
#             raise ValidationError(
#                 f"UniqueKey(s) not found in branch stock: {sorted(missing_branch_keys)}"
#             )

#         branch_stock.unickkey.remove(*unique_key_ids)

#         if hasattr(variation, "unickkey"):
#             existing_variation_key_ids = set(
#                 variation.unickkey.filter(id__in=unique_key_ids).values_list("id", flat=True)
#             )
#             if existing_variation_key_ids:
#                 variation.unickkey.remove(*list(existing_variation_key_ids))

#     BranchProductStock.objects.filter(id=branch_stock.id).update(
#         quantity=F("quantity") - qty
#     )

#     Variation.objects.filter(id=variation.id).update(
#         quantity=F("quantity") - qty
#     )

#     fresh_branch_stock = BranchProductStock.objects.get(id=branch_stock.id)
#     fresh_variation = Variation.objects.get(id=variation.id)

#     print("DEBUG AFTER branch_stock qty =", fresh_branch_stock.quantity)
#     print("DEBUG AFTER variation qty =", fresh_variation.quantity)
#     print("DEBUG AFTER branch_stock keys =", list(fresh_branch_stock.unickkey.values_list("id", flat=True)))
#     if hasattr(fresh_variation, "unickkey"):
#         print("DEBUG AFTER variation keys =", list(fresh_variation.unickkey.values_list("id", flat=True)))


# def sync_product_stock_on_create_only(instance, created):
#     """
#     Product stock deduction শুধু create এ হবে.
#     Update এ stock auto-adjust করছি না, কারণ old/new diff লাগবে.
#     """
#     if not created:
#         return

#     if instance.receive_type != "product":
#         return

#     if not instance.product_details:
#         return

#     if isinstance(instance.product_details, str):
#         try:
#             rows = json.loads(instance.product_details)
#         except Exception:
#             raise ValidationError("Invalid product_details JSON")
#     else:
#         rows = instance.product_details

#     for row in rows:
#         variation_id = row.get("variation_id")
#         qty = int(row.get("quantity", 0))

#         unique_key_ids = row.get("unique_key_ids", None)

#         if unique_key_ids is None:
#             single_unique_key_id = row.get("unique_key_id")
#             if single_unique_key_id:
#                 unique_key_ids = [single_unique_key_id]
#             else:
#                 unique_key_ids = []

#         if not variation_id or qty <= 0:
#             continue

#         try:
#             variation = Variation.objects.get(id=variation_id)
#         except Variation.DoesNotExist:
#             raise ValidationError(f"Variation {variation_id} not found")

#         deduct_branch_and_variation_stock(
#             branch=instance.branch_name,
#             variation=variation,
#             qty=qty,
#             unique_key_ids=unique_key_ids
#         )


# # =========================================================
# # Loan transaction sync
# # =========================================================

# def sync_loan_transactions(instance):
#     """
#     Loan create/update এ সব related transaction sync করবে.
#     Return করবে installment এর জন্য final total_amount.
#     """
#     original_amount = q2(instance.amount or 0)
#     total_amount = original_amount
#     received_by = getattr(instance, "created_by", None)

#     valid_behavior_modelnames = []

#     # -------------------------
#     # 1) Loan behavior charges
#     # -------------------------
#     if instance.loan_type and instance.loan_type.behaviour_type:
#         for item in instance.loan_type.behaviour_type:
#             behavior_name = item.get("name", "Unknown")
#             amt = q2(item.get("amount", 0))
#             is_percent = item.get("is_percent", False)

#             modelname = loan_behavior_modelname(instance.id, behavior_name)
#             valid_behavior_modelnames.append(modelname)

#             if is_percent:
#                 added = q2(original_amount * amt / Decimal("100"))
#                 total_amount = q2(total_amount + added)

#                 create_or_update_transaction(
#                     customer=instance.customer_name,
#                     transection_type="cashin",
#                     amount=added,
#                     received_by=received_by,
#                     modelname=modelname,
#                     mark_paid=True
#                 )
#             else:
#                 total_amount = q2(total_amount + amt)

#                 create_or_update_transaction(
#                     customer=instance.customer_name,
#                     transection_type="cashin",
#                     amount=amt,
#                     received_by=received_by,
#                     modelname=modelname,
#                     mark_paid=True
#                 )

#     delete_removed_behavior_transactions(instance, valid_behavior_modelnames)

#     # -------------------------
#     # 2) Down payment
#     # -------------------------
#     down_payment = q2(instance.first_down_payment or 0)
#     dp_modelname = loan_down_payment_modelname(instance.id)

#     if down_payment > 0:
#         create_or_update_transaction(
#             customer=instance.customer_name,
#             transection_type="cashin",
#             amount=down_payment,
#             received_by=received_by,
#             modelname=dp_modelname,
#             mark_paid=True
#         )
#         total_amount = q2(max(Decimal("0.00"), total_amount - down_payment))
#     else:
#         Transection.objects.filter(
#             customer_name=instance.customer_name,
#             modelname=dp_modelname
#         ).delete()

#     # -------------------------
#     # 3) Main loan disbursement
#     # -------------------------
#     disbursement_modelname = loan_disbursement_modelname(instance.id)
#     create_or_update_transaction(
#         customer=instance.customer_name,
#         transection_type="cashout",
#         amount=original_amount,
#         received_by=received_by,
#         modelname=disbursement_modelname,
#         mark_paid=False
#     )

#     return total_amount


# # =========================================================
# # Installment dates helper
# # =========================================================

# def generate_installment_dates(start_date, installment_type):
#     """
#     আপনার existing logic থাকলে সেটা use করবেন.
#     নিচে sample fallback দিলাম।
#     """
#     count = getattr(installment_type, "instalment_cullect", 0)
#     if not count:
#         return []

#     dates = []
#     current_date = start_date

#     installment_method = getattr(installment_type, "installment_method", "daily")

#     for _ in range(count):
#         dates.append(current_date)

#         if installment_method == "daily":
#             from datetime import timedelta
#             current_date = current_date + timedelta(days=1)
#         elif installment_method == "weekly":
#             from datetime import timedelta
#             current_date = current_date + timedelta(days=7)
#         elif installment_method == "monthly":
#             # simple monthly fallback
#             month = current_date.month + 1
#             year = current_date.year
#             if month > 12:
#                 month = 1
#                 year += 1
#             day = min(current_date.day, 28)
#             current_date = current_date.replace(year=year, month=month, day=day)
#         else:
#             from datetime import timedelta
#             current_date = current_date + timedelta(days=1)

#     return dates


# # =========================================================
# # Installment sync
# # =========================================================

# # def sync_loan_installments(instance, total_amount):
# #     """
# #     Duplicate avoid করতে old installments delete করে নতুন করে create করবে.
# #     """
# #     installment_type = instance.installment_type
# #     if (
# #         not installment_type
# #         or not getattr(installment_type, "instalment_cullect", None)
# #         or installment_type.instalment_cullect <= 0
# #     ):
# #         instance.installment.clear()
# #         Installment.objects.filter(loan_id=str(instance.id)).delete()
# #         return

# #     start_date = date.today()
# #     dates = generate_installment_dates(start_date, installment_type)
# #     if not dates:
# #         instance.installment.clear()
# #         Installment.objects.filter(loan_id=str(instance.id)).delete()
# #         return

# #     old_installments = Installment.objects.filter(loan_id=str(instance.id))
# #     instance.installment.clear()
# #     old_installments.delete()

# #     n = len(dates)
# #     per_installment_amount = q2(total_amount / n) if n else Decimal("0.00")
# #     remaining_amount = total_amount

# #     new_installments = []

# #     for i, inst_date in enumerate(dates):
# #         if i == n - 1:
# #             amount = q2(remaining_amount)
# #         else:
# #             amount = per_installment_amount
# #             remaining_amount = q2(remaining_amount - amount)

# #         if amount <= 0:
# #             continue

# #         inst = Installment.objects.create(
# #             customer_name=instance.customer_name,
# #             installment_date=inst_date,
# #             amount=amount,
# #             installment_status="due",
# #             area_name=instance.area_name,
# #             branch_name=instance.branch_name,
# #             customergroup_name=instance.customer_group,
# #             loan_id=str(instance.id),
# #             pay_from_account=instance.pay_from_account,
# #             due_amount=amount
# #         )
# #         new_installments.append(inst)

# #     if new_installments:
# #         instance.installment.set(new_installments)


# def sync_loan_installments(instance, total_amount):
#     installment_type = instance.installment_type
#     if (
#         not installment_type
#         or not getattr(installment_type, "instalment_cullect", None)
#         or installment_type.instalment_cullect <= 0
#     ):
#         instance.installment.clear()
#         Installment.objects.filter(loan_id=str(instance.id)).delete()
#         return

#     start_date = date.today()
#     dates = generate_installment_dates(start_date, installment_type)
#     if not dates:
#         instance.installment.clear()
#         Installment.objects.filter(loan_id=str(instance.id)).delete()
#         return

#     old_installments = Installment.objects.filter(loan_id=str(instance.id))
#     instance.installment.clear()
#     old_installments.delete()

#     n = len(dates)
#     per_installment_amount = q2(total_amount / n) if n else Decimal("0.00")
#     remaining_amount = total_amount

#     new_installments = []

#     for i, inst_date in enumerate(dates):
#         if i == n - 1:
#             amount = q2(remaining_amount)
#         else:
#             amount = per_installment_amount
#             remaining_amount = q2(remaining_amount - amount)

#         if amount <= 0:
#             continue

#         inst = Installment.objects.create(
#             customer_name=instance.customer_name,
#             installment_date=inst_date,
#             amount=amount,
#             installment_status="due",
#             area_name=instance.area_name,
#             branch_name=instance.branch_name,
#             customergroup_name=getattr(instance, "customergroup", None),
#             loan_id=str(instance.id),
#             pay_from_account=instance.pay_from_account,
#             due_amount=amount
#         )
#         new_installments.append(inst)

#     if new_installments:
#         instance.installment.set(new_installments)

# # =========================================================
# # Main Loan signal
# # =========================================================

# @receiver(post_save, sender=Loan, dispatch_uid="loan_create_update_sync_signal")
# def handle_loan_create_or_update(sender, instance, created, **kwargs):
#     print("DEBUG signal called | loan id =", instance.pk, "| created =", created)

#     try:
#         with transaction.atomic():
#             # sync_product_stock_on_create_only(instance, created)

#             total_amount = sync_loan_transactions(instance)

#             sync_loan_installments(instance, total_amount)

#             Loan.objects.filter(pk=instance.pk).update(updated_at=timezone.now())

#     except InsufficientBalanceError as e:
#         raise ValidationError(str(e))
#     except Exception as e:
#         print("Error syncing loan data:", str(e))
#         traceback.print_exc()
#         raise




























# @receiver(post_save, sender=DailySaving)
# def create_daily_saving_transaction(sender, instance, created, **kwargs):
#     if not created:
#         return

#     if instance.amount < 0:
#         print(f"Skipping transaction for negative DailySaving: {instance.amount}")
#         return

#     update_customer_balance(instance.customer_name, instance.amount)

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=instance.amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=f"Daily Saving : {instance.id})"
#     )
#     mark_transaction_as_paid(tx, instance.amount)

#     print(f"✓ Transaction created for DailySaving: {instance.amount:.2f}")


from decimal import Decimal
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

from .models import DailySaving, Transection


def daily_saving_modelname(instance_id):
    return f"Daily Saving "


@receiver(pre_save, sender=DailySaving)
def store_old_daily_saving_data(sender, instance, **kwargs):
    """
    update এর আগে old amount + old customer store করবে
    """
    if instance.pk:
        try:
            old_instance = DailySaving.objects.get(pk=instance.pk)
            instance._old_amount = old_instance.amount or Decimal("0.00")
            instance._old_customer = old_instance.customer_name
        except DailySaving.DoesNotExist:
            instance._old_amount = Decimal("0.00")
            instance._old_customer = None
    else:
        instance._old_amount = Decimal("0.00")
        instance._old_customer = None


@receiver(post_save, sender=DailySaving)
def create_or_update_daily_saving_transaction(sender, instance, created, **kwargs):
    if instance.amount is None or instance.amount < 0:
        print(f"Skipping DailySaving transaction for invalid amount: {instance.amount}")
        return

    modelname = daily_saving_modelname(instance.id)
    new_amount = instance.amount or Decimal("0.00")

    if created:
        # 1) customer balance update
        update_customer_balance(instance.customer_name, new_amount)

        # 2) transaction create
        tx = create_transaction_with_customer_info(
            instance.customer_name,
            transection_type="cashin",
            amount=new_amount,
            customer_name=instance.customer_name,
            received_by=instance.received_by,
            modelname=modelname
        )
        mark_transaction_as_paid(tx, new_amount)

        print(f"✓ DailySaving created | balance +{new_amount} | tx created")
        return

    # -------------------------
    # update case
    # -------------------------
    old_amount = getattr(instance, "_old_amount", Decimal("0.00"))
    old_customer = getattr(instance, "_old_customer", None)

    # customer same থাকলে শুধু diff adjust হবে
    if old_customer == instance.customer_name:
        diff = new_amount - old_amount
        if diff != 0:
            update_customer_balance(instance.customer_name, diff)

    else:
        # customer change হলে old customer থেকে minus, new customer এ plus
        if old_customer:
            update_customer_balance(old_customer, -old_amount)
        if instance.customer_name:
            update_customer_balance(instance.customer_name, new_amount)

    # transaction update
    tx = Transection.objects.filter(
        modelname=modelname
    ).first()

    if tx:
        tx.customer_name = instance.customer_name
        tx.transection_type = "cashin"
        tx.amount = new_amount
        tx.received_by = instance.received_by
        tx.modelname = modelname
        tx.save()

        mark_transaction_as_paid(tx, new_amount)
        print(f"✓ DailySaving updated | balance adjusted | tx updated")
    else:
        # যদি পুরান transaction না পাওয়া যায়, নতুন create করবে
        tx = create_transaction_with_customer_info(
            instance.customer_name,
            transection_type="cashin",
            amount=new_amount,
            customer_name=instance.customer_name,
            received_by=instance.received_by,
            modelname=modelname
        )
        mark_transaction_as_paid(tx, new_amount)
        print(f"✓ DailySaving updated | missing tx recreated")


@receiver(post_delete, sender=DailySaving)
def delete_daily_saving_transaction(sender, instance, **kwargs):
    """
    delete হলে balance minus হবে + transaction delete হবে
    """
    amount = instance.amount or Decimal("0.00")

    if instance.customer_name and amount > 0:
        update_customer_balance(instance.customer_name, -amount)

    Transection.objects.filter(
        modelname=daily_saving_modelname(instance.id)
    ).delete()

    print(f"✓ DailySaving deleted | balance -{amount} | tx deleted")


@receiver(pre_save, sender=Installment)
def store_old_installment_status(sender, instance, **kwargs):
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


# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Installment payment keeps partial/full payment logic.
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = getattr(instance, "_old_pay", None)
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if not (old_pay != instance.installment_pay and instance.installment_pay):
#         return

#     print(f"\n--- Installment Payment: ID {instance.id} ---")

#     installment_pay = Decimal(str(instance.installment_pay or 0))
#     current_due = Decimal(str(instance.due_amount or instance.amount))

#     if installment_pay <= 0:
#         print("Warning: No payment amount recorded")
#         return

#     if installment_pay > instance.amount:
#         actual_payment = instance.amount
#         extra_amount = installment_pay - instance.amount
#         print(f"Payment: {installment_pay:.2f}, Due: {current_due:.2f}, Extra: {extra_amount:.2f}")
#     else:
#         actual_payment = installment_pay
#         extra_amount = Decimal("0")
#         print(f"Payment: {installment_pay:.2f}, Due: {current_due:.2f}")

#     if instance.pay_from_account:
#         print("Pay from account enabled - processing account deduction...")

#         try:
#             check_and_deduct_balance(
#                 instance.customer_name,
#                 installment_pay,
#                 f"Installment Payment ID: {instance.id}"
#             )
#             print(f"✓ Deducted {installment_pay:.2f} from account")

#             transaction_obj = create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=instance.amount,
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id})"
#             )

#             if hasattr(transaction_obj, "paid"):
#                 transaction_obj.paid = actual_payment >= instance.amount

#             if hasattr(transaction_obj, "paid_amount"):
#                 transaction_obj.paid_amount = actual_payment

#             if hasattr(transaction_obj, "due_amount"):
#                 transaction_obj.due_amount = current_due - actual_payment

#             transaction_obj.save()

#             new_due_amount = current_due - actual_payment

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=0
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount
#                 )

#             if extra_amount > 0:
#                 update_customer_balance(instance.customer_name, extra_amount)

#                 extra_tx = create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashin",
#                     amount=extra_amount,
#                     customer_name=instance.customer_name,
#                     received_by=instance.received_by,
#                     modelname=f"Extra Payment Savings : {instance.id})"
#                 )
#                 mark_transaction_as_paid(extra_tx, extra_amount)

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount
#             )
#             raise ValidationError(str(e))

#     else:
#         transaction_obj = create_transaction_with_customer_info(
#             instance.customer_name,
#             transection_type="cashin",
#             amount=instance.amount,
#             customer_name=instance.customer_name,
#             received_by=instance.received_by,
#             modelname=f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"
#         )

#         if hasattr(transaction_obj, "paid"):
#             transaction_obj.paid = actual_payment >= instance.amount

#         if hasattr(transaction_obj, "paid_amount"):
#             transaction_obj.paid_amount = actual_payment

#         if hasattr(transaction_obj, "due_amount"):
#             transaction_obj.due_amount = current_due - actual_payment

#         transaction_obj.save()

#         new_due_amount = current_due - actual_payment

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=0
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount
#             )

#         if extra_amount > 0:
#             update_customer_balance(instance.customer_name, extra_amount)

#             extra_tx = create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=extra_amount,
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=f"Extra Payment Savings : {instance.id})"
#             )
#             mark_transaction_as_paid(extra_tx, extra_amount)





from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError


def sync_transaction_amount(tx, amount):
    """
    Update transaction amount.
    If amount <= 0 then delete transaction.
    """
    amount = Decimal(str(amount or 0))

    if amount <= 0:
        tx.delete()
        return None

    tx.amount = amount

    if hasattr(tx, "paid"):
        tx.paid = True

    if hasattr(tx, "paid_amount"):
        tx.paid_amount = amount

    if hasattr(tx, "due_amount"):
        tx.due_amount = Decimal("0")

    tx.save()
    return tx


# def get_existing_transaction(transaction_model, modelname):
#     return transaction_model.objects.filter(modelname=modelname).order_by("-id").first()


def get_existing_transaction(customer, modelname):
    return Transection.objects.filter(
        customer_name=customer,
        modelname=modelname
    ).order_by("-id").first()

# def get_existing_transaction(transaction_model, customer, modelname):
#     return transaction_model.objects.filter(
#         customer_name=customer,
#         modelname=modelname
#     ).order_by("-id").first()


# def sync_main_installment_transaction(instance, transaction_model, payment_amount, from_account=False):
#     """
#     Main installment transaction create/update/delete
#     """
#     payment_amount = Decimal(str(payment_amount or 0))

#     if from_account:
#         modelname = f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id})"
#     else:
#         modelname = f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"

#     tx = get_existing_transaction(
#         transaction_model,
#         instance.customer_name,
#         modelname
#     )

#     if payment_amount <= 0:
#         if tx:
#             tx.delete()
#         return None

#     if tx:
#         tx.amount = payment_amount

#         if hasattr(tx, "customer_name"):
#             tx.customer_name = instance.customer_name

#         if hasattr(tx, "received_by"):
#             tx.received_by = instance.received_by

#         if hasattr(tx, "transection_type"):
#             tx.transection_type = "cashin"

#         if hasattr(tx, "paid"):
#             tx.paid = True

#         if hasattr(tx, "paid_amount"):
#             tx.paid_amount = payment_amount

#         if hasattr(tx, "due_amount"):
#             tx.due_amount = Decimal("0")

#         tx.save()
#         return tx

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=payment_amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname
#     )
#     mark_transaction_as_paid(tx, payment_amount)
#     return tx


# def sync_extra_payment_savings(instance, transaction_model, old_extra_amount, new_extra_amount):
#     """
#     Extra Payment Savings transaction + customer balance sync
#     """
#     old_extra_amount = Decimal(str(old_extra_amount or 0))
#     new_extra_amount = Decimal(str(new_extra_amount or 0))

#     modelname = f"Extra Payment Savings : {instance.id})"
#     extra_tx = get_existing_transaction(
#         transaction_model,
#         instance.customer_name,
#         modelname
#     )

#     # old extra reverse from customer balance
#     if old_extra_amount > 0:
#         update_customer_balance(instance.customer_name, -old_extra_amount)

#     # if new extra = 0 -> delete old transaction
#     if new_extra_amount <= 0:
#         if extra_tx:
#             extra_tx.delete()
#         return None

#     # apply new extra to customer balance
#     update_customer_balance(instance.customer_name, new_extra_amount)

#     if extra_tx:
#         extra_tx.amount = new_extra_amount

#         if hasattr(extra_tx, "customer_name"):
#             extra_tx.customer_name = instance.customer_name

#         if hasattr(extra_tx, "received_by"):
#             extra_tx.received_by = instance.received_by

#         if hasattr(extra_tx, "transection_type"):
#             extra_tx.transection_type = "cashin"

#         if hasattr(extra_tx, "paid"):
#             extra_tx.paid = True

#         if hasattr(extra_tx, "paid_amount"):
#             extra_tx.paid_amount = new_extra_amount

#         if hasattr(extra_tx, "due_amount"):
#             extra_tx.due_amount = Decimal("0")

#         extra_tx.save()
#         return extra_tx

#     extra_tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=new_extra_amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname
#     )
#     mark_transaction_as_paid(extra_tx, new_extra_amount)
#     return extra_tx



# def sync_main_installment_transaction(instance, transaction_model, payment_amount, from_account=False):
#     """
#     Main installment transaction create/update/delete
#     """
#     payment_amount = Decimal(str(payment_amount or 0))

#     if from_account:
#         modelname = f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id})"
#     else:
#         modelname = f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"

#     tx = get_existing_transaction(
#         instance.customer_name,
#         modelname
#     )

#     if payment_amount <= 0:
#         if tx:
#             tx.delete()
#         return None

#     if tx:
#         tx.amount = payment_amount

#         if hasattr(tx, "customer_name"):
#             tx.customer_name = instance.customer_name

#         if hasattr(tx, "received_by"):
#             tx.received_by = instance.received_by

#         if hasattr(tx, "transection_type"):
#             tx.transection_type = "cashin"

#         if hasattr(tx, "paid"):
#             tx.paid = True

#         if hasattr(tx, "paid_amount"):
#             tx.paid_amount = payment_amount

#         if hasattr(tx, "due_amount"):
#             tx.due_amount = Decimal("0")

#         tx.save()
#         return tx

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=payment_amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname
#     )
#     mark_transaction_as_paid(tx, payment_amount)
#     return tx


# def sync_extra_payment_savings(instance, transaction_model, old_extra_amount, new_extra_amount):
#     """
#     Extra Payment Savings transaction + customer balance sync
#     """
#     old_extra_amount = Decimal(str(old_extra_amount or 0))
#     new_extra_amount = Decimal(str(new_extra_amount or 0))

#     modelname = f"Extra Payment Savings : {instance.id})"
#     extra_tx = get_existing_transaction(
#         instance.customer_name,
#         modelname
#     )

#     # old extra reverse from customer balance
#     if old_extra_amount > 0:
#         update_customer_balance(instance.customer_name, -old_extra_amount)

#     # if new extra = 0 -> delete old transaction
#     if new_extra_amount <= 0:
#         if extra_tx:
#             extra_tx.delete()
#         return None

#     # apply new extra to customer balance
#     update_customer_balance(instance.customer_name, new_extra_amount)

#     if extra_tx:
#         extra_tx.amount = new_extra_amount

#         if hasattr(extra_tx, "customer_name"):
#             extra_tx.customer_name = instance.customer_name

#         if hasattr(extra_tx, "received_by"):
#             extra_tx.received_by = instance.received_by

#         if hasattr(extra_tx, "transection_type"):
#             extra_tx.transection_type = "cashin"

#         if hasattr(extra_tx, "paid"):
#             extra_tx.paid = True

#         if hasattr(extra_tx, "paid_amount"):
#             extra_tx.paid_amount = new_extra_amount

#         if hasattr(extra_tx, "due_amount"):
#             extra_tx.due_amount = Decimal("0")

#         extra_tx.save()
#         return extra_tx

#     extra_tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=new_extra_amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname
#     )
#     mark_transaction_as_paid(extra_tx, new_extra_amount)
#     return extra_tx

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Installment payment update logic:
#     - main transaction update
#     - extra savings transaction update/delete
#     - customer balance reverse/apply correctly
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = getattr(instance, "_old_pay", None)
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if not (old_pay != instance.installment_pay and instance.installment_pay is not None):
#         return

#     print(f"\n--- Installment Payment: ID {instance.id} ---")

#     installment_amount = Decimal(str(instance.amount or 0))
#     new_pay = Decimal(str(instance.installment_pay or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     current_due = Decimal(str(instance.due_amount or installment_amount))

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     old_actual_payment = min(old_pay, installment_amount)
#     new_actual_payment = min(new_pay, installment_amount)

#     old_extra_amount = max(old_pay - installment_amount, Decimal("0"))
#     new_extra_amount = max(new_pay - installment_amount, Decimal("0"))

#     print(
#         f"Old Pay: {old_pay:.2f}, New Pay: {new_pay:.2f}, "
#         f"Old Extra: {old_extra_amount:.2f}, New Extra: {new_extra_amount:.2f}"
#     )

#     if instance.pay_from_account:
#         print("Pay from account enabled - processing account deduction...")

#         try:
#             # only deduct the difference from account
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}"
#                 )
#                 print(f"✓ Deducted extra {pay_diff:.2f} from account")

#             elif pay_diff < 0:
#                 # refund account if payment reduced
#                 update_customer_balance(instance.customer_name, abs(pay_diff))
#                 print(f"✓ Refunded {abs(pay_diff):.2f} to account")

#             # get transaction model from existing/created tx
#             tx_model = None

#             sample_tx_name = f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id})"
#             existing_tx = create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=new_actual_payment,
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=sample_tx_name
#             )
#             tx_model = existing_tx.__class__

#             # delete the just-created duplicate if old one exists situation happens
#             # safer approach: use existing transaction after getting model
#             duplicate_check = tx_model.objects.filter(modelname=sample_tx_name).order_by("-id")
#             if duplicate_check.count() > 1:
#                 duplicate_check.first().delete()

#             # main transaction sync
#             sync_main_installment_transaction(
#                 instance=instance,
#                 transaction_model=tx_model,
#                 payment_amount=new_actual_payment,
#                 from_account=True
#             )

#             # extra transaction sync
#             sync_extra_payment_savings(
#                 instance=instance,
#                 transaction_model=tx_model,
#                 old_extra_amount=old_extra_amount,
#                 new_extra_amount=new_extra_amount
#             )

#             new_due_amount = installment_amount - new_actual_payment

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0")
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount
#             )
#             raise ValidationError(str(e))

#     else:
#         # create one tx only to get model class
#         temp_tx = create_transaction_with_customer_info(
#             instance.customer_name,
#             transection_type="cashin",
#             amount=new_actual_payment,
#             customer_name=instance.customer_name,
#             received_by=instance.received_by,
#             modelname=f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"
#         )
#         tx_model = temp_tx.__class__

#         # remove duplicate temp create if exists
#         duplicate_check = tx_model.objects.filter(
#             modelname=f"Installment Payment : {instance.id}, Loan: {instance.loan_id})"
#         ).order_by("-id")
#         if duplicate_check.count() > 1:
#             duplicate_check.first().delete()

#         # main transaction sync
#         sync_main_installment_transaction(
#             instance=instance,
#             transaction_model=tx_model,
#             payment_amount=new_actual_payment,
#             from_account=False
#         )

#         # extra savings sync
#         sync_extra_payment_savings(
#             instance=instance,
#             transaction_model=tx_model,
#             old_extra_amount=old_extra_amount,
#             new_extra_amount=new_extra_amount
#         )

#         new_due_amount = installment_amount - new_actual_payment

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0")
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount
#             )



# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save
# from django.dispatch import receiver


# def get_installment_payment_modelname(from_account=False):
#     return "Installment Payment From Account" if from_account else "Installment Payment"


# def get_extra_payment_savings_modelname():
#     return "Extra Payment Savings"


# def get_existing_installment_transaction(instance, from_account=False):
#     modelname = get_installment_payment_modelname(from_account)

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# def get_existing_extra_transaction(instance):
#     modelname = get_extra_payment_savings_modelname()

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# def assign_installment_transaction_fields(tx, instance, amount, from_account=False):
#     """
#     Common transaction field assignment
#     """
#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_installment_payment_modelname(from_account)

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# def assign_extra_transaction_fields(tx, instance, amount):
#     """
#     Common extra payment savings transaction field assignment
#     """
#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_extra_payment_savings_modelname()

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# def create_installment_transaction(instance, amount, from_account=False):
#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_installment_payment_modelname(from_account)
#     )

#     tx = assign_installment_transaction_fields(tx, instance, amount, from_account)
#     tx.save()
#     mark_transaction_as_paid(tx, amount)
#     return tx


# def create_extra_transaction(instance, amount):
#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_extra_payment_savings_modelname()
#     )

#     tx = assign_extra_transaction_fields(tx, instance, amount)
#     tx.save()
#     mark_transaction_as_paid(tx, amount)
#     return tx


# def sync_main_installment_transaction(instance, payment_amount, from_account=False):
#     """
#     Main installment transaction create/update/delete
#     modelname fixed থাকবে
#     loan_id + installment_id আলাদা field এ যাবে
#     """
#     payment_amount = Decimal(str(payment_amount or 0))
#     tx = get_existing_installment_transaction(instance, from_account=from_account)

#     if payment_amount <= 0:
#         if tx:
#             tx.delete()
#         return None

#     if tx:
#         tx = assign_installment_transaction_fields(
#             tx=tx,
#             instance=instance,
#             amount=payment_amount,
#             from_account=from_account
#         )
#         tx.save()
#         return tx

#     return create_installment_transaction(
#         instance=instance,
#         amount=payment_amount,
#         from_account=from_account
#     )


# def sync_extra_payment_savings(instance, old_extra_amount, new_extra_amount):
#     """
#     Extra Payment Savings transaction + customer balance sync
#     """
#     old_extra_amount = Decimal(str(old_extra_amount or 0))
#     new_extra_amount = Decimal(str(new_extra_amount or 0))

#     extra_tx = get_existing_extra_transaction(instance)

#     # old extra reverse from customer balance
#     if old_extra_amount > 0:
#         update_customer_balance(instance.customer_name, -old_extra_amount)

#     # if new extra = 0 -> delete old transaction
#     if new_extra_amount <= 0:
#         if extra_tx:
#             extra_tx.delete()
#         return None

#     # apply new extra to customer balance
#     update_customer_balance(instance.customer_name, new_extra_amount)

#     if extra_tx:
#         extra_tx = assign_extra_transaction_fields(
#             tx=extra_tx,
#             instance=instance,
#             amount=new_extra_amount
#         )
#         extra_tx.save()
#         return extra_tx

#     return create_extra_transaction(instance, new_extra_amount)


# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Installment payment update logic:
#     - main transaction update
#     - extra savings transaction update/delete
#     - customer balance reverse/apply correctly
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = getattr(instance, "_old_pay", None)
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if not (old_pay != instance.installment_pay and instance.installment_pay is not None):
#         return

#     print(f"\n--- Installment Payment: ID {instance.id} | Loan: {instance.loan_id} ---")

#     installment_amount = Decimal(str(instance.amount or 0))
#     new_pay = Decimal(str(instance.installment_pay or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     current_due = Decimal(str(instance.due_amount or installment_amount))

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     old_actual_payment = min(old_pay, installment_amount)
#     new_actual_payment = min(new_pay, installment_amount)

#     old_extra_amount = max(old_pay - installment_amount, Decimal("0"))
#     new_extra_amount = max(new_pay - installment_amount, Decimal("0"))

#     print(
#         f"Old Pay: {old_pay:.2f}, New Pay: {new_pay:.2f}, "
#         f"Old Extra: {old_extra_amount:.2f}, New Extra: {new_extra_amount:.2f}"
#     )

#     if instance.pay_from_account:
#         print("Pay from account enabled - processing account deduction...")

#         try:
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )
#                 print(f"✓ Deducted extra {pay_diff:.2f} from account")

#             elif pay_diff < 0:
#                 update_customer_balance(instance.customer_name, abs(pay_diff))
#                 print(f"✓ Refunded {abs(pay_diff):.2f} to account")

#             # main transaction sync
#             sync_main_installment_transaction(
#                 instance=instance,
#                 payment_amount=new_actual_payment,
#                 from_account=True
#             )

#             # extra transaction sync
#             sync_extra_payment_savings(
#                 instance=instance,
#                 old_extra_amount=old_extra_amount,
#                 new_extra_amount=new_extra_amount
#             )

#             new_due_amount = installment_amount - new_actual_payment

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0")
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount
#             )
#             raise ValidationError(str(e))

#     else:
#         # main transaction sync
#         sync_main_installment_transaction(
#             instance=instance,
#             payment_amount=new_actual_payment,
#             from_account=False
#         )

#         # extra transaction sync
#         sync_extra_payment_savings(
#             instance=instance,
#             old_extra_amount=old_extra_amount,
#             new_extra_amount=new_extra_amount
#         )

#         new_due_amount = installment_amount - new_actual_payment

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0")
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount
#             )




# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver

# # ---------------------------------------------------
# # MODELNAME HELPERS
# # ---------------------------------------------------

# def get_installment_payment_modelname(from_account=False):
#     return "Installment Payment From Account" if from_account else "Installment Payment"


# def get_extra_payment_savings_modelname():
#     return "Extra Payment Savings"


# # ---------------------------------------------------
# # QUERY HELPERS
# # ---------------------------------------------------

# def get_existing_installment_transaction(instance, from_account=False):
#     modelname = get_installment_payment_modelname(from_account)

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname,
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# def get_existing_extra_transaction(instance):
#     modelname = get_extra_payment_savings_modelname()

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname,
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# # ---------------------------------------------------
# # FIELD ASSIGN HELPERS
# # ---------------------------------------------------

# def assign_main_transaction_fields(tx, instance, amount, from_account=False):
#     amount = Decimal(str(amount or 0))

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_installment_payment_modelname(from_account)

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# def assign_extra_transaction_fields(tx, instance, amount):
#     amount = Decimal(str(amount or 0))

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_extra_payment_savings_modelname()

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# # ---------------------------------------------------
# # CREATE HELPERS
# # ---------------------------------------------------

# def create_installment_transaction(instance, amount, from_account=False):
#     amount = Decimal(str(amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_installment_payment_modelname(from_account),
#     )

#     tx = assign_main_transaction_fields(tx, instance, amount, from_account)
#     tx.save()
#     mark_transaction_as_paid(tx, amount)
#     return tx


# def create_extra_transaction(instance, amount):
#     amount = Decimal(str(amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_extra_payment_savings_modelname(),
#     )

#     tx = assign_extra_transaction_fields(tx, instance, amount)
#     tx.save()
#     mark_transaction_as_paid(tx, amount)
#     return tx


# # ---------------------------------------------------
# # SYNC HELPERS
# # ---------------------------------------------------

# def sync_main_installment_transaction(instance, payment_amount, from_account=False):
#     """
#     Main installment transaction create/update/delete
#     """
#     payment_amount = Decimal(str(payment_amount or 0))
#     tx = get_existing_installment_transaction(instance, from_account=from_account)

#     if payment_amount <= 0:
#         if tx:
#             tx.delete()
#         return None

#     if tx:
#         tx = assign_main_transaction_fields(
#             tx=tx,
#             instance=instance,
#             amount=payment_amount,
#             from_account=from_account,
#         )
#         tx.save()
#         return tx

#     return create_installment_transaction(
#         instance=instance,
#         amount=payment_amount,
#         from_account=from_account,
#     )


# def sync_extra_payment_savings(instance, old_extra_amount, new_extra_amount):
#     """
#     Extra Payment Savings transaction + customer balance sync
#     """
#     old_extra_amount = Decimal(str(old_extra_amount or 0))
#     new_extra_amount = Decimal(str(new_extra_amount or 0))

#     extra_tx = get_existing_extra_transaction(instance)

#     # reverse previous extra from customer balance
#     if old_extra_amount > 0:
#         update_customer_balance(instance.customer_name, -old_extra_amount)

#     # if no new extra -> delete extra tx
#     if new_extra_amount <= 0:
#         if extra_tx:
#             extra_tx.delete()
#         return None

#     # apply new extra to customer balance
#     update_customer_balance(instance.customer_name, new_extra_amount)

#     if extra_tx:
#         extra_tx = assign_extra_transaction_fields(
#             tx=extra_tx,
#             instance=instance,
#             amount=new_extra_amount,
#         )
#         extra_tx.save()
#         return extra_tx

#     return create_extra_transaction(instance, new_extra_amount)


# # ---------------------------------------------------
# # PRE SAVE - OLD VALUE CAPTURE
# # ---------------------------------------------------

# @receiver(pre_save, sender=Installment)
# def store_old_installment_values(sender, instance, **kwargs):
#     if not instance.pk:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None
#         return

#     try:
#         old_instance = Installment.objects.get(pk=instance.pk)
#         instance._old_status = old_instance.installment_status
#         instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
#         instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
#     except Installment.DoesNotExist:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None


# # ---------------------------------------------------
# # MAIN SIGNAL
# # ---------------------------------------------------

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Installment payment update logic:
#     - main transaction update
#     - extra savings transaction update/delete
#     - customer balance reverse/apply correctly
#     - due amount update
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if instance.installment_pay is None:
#         return

#     new_pay = Decimal(str(instance.installment_pay or 0))

#     # no change হলে কিছু করবে না
#     if old_pay == new_pay:
#         return

#     print(f"\n--- Installment Payment Update ---")
#     print(f"Installment ID: {instance.id}")
#     print(f"Loan ID: {instance.loan_id}")
#     print(f"Old Pay: {old_pay}")
#     print(f"New Pay: {new_pay}")

#     installment_amount = Decimal(str(instance.amount or 0))

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     # installment মূল amount পর্যন্ত main payment
#     old_actual_payment = min(old_pay, installment_amount)
#     new_actual_payment = min(new_pay, installment_amount)

#     # installment amount এর বেশি গেলে extra saving
#     old_extra_amount = max(old_pay - installment_amount, Decimal("0"))
#     new_extra_amount = max(new_pay - installment_amount, Decimal("0"))

#     print(
#         f"Old Actual: {old_actual_payment:.2f}, New Actual: {new_actual_payment:.2f}, "
#         f"Old Extra: {old_extra_amount:.2f}, New Extra: {new_extra_amount:.2f}"
#     )

#     if instance.pay_from_account:
#         print("Pay from account enabled...")

#         try:
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )
#                 print(f"✓ Deducted {pay_diff:.2f} from account")

#             elif pay_diff < 0:
#                 update_customer_balance(instance.customer_name, abs(pay_diff))
#                 print(f"✓ Refunded {abs(pay_diff):.2f} to account")

#             # main installment transaction
#             sync_main_installment_transaction(
#                 instance=instance,
#                 payment_amount=new_actual_payment,
#                 from_account=True,
#             )

#             # extra savings transaction
#             sync_extra_payment_savings(
#                 instance=instance,
#                 old_extra_amount=old_extra_amount,
#                 new_extra_amount=new_extra_amount,
#             )

#             # due update
#             new_due_amount = installment_amount - new_actual_payment

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0"),
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount,
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount if old_due_amount is not None else installment_amount,
#             )
#             raise ValidationError(str(e))

#     else:
#         # main installment transaction
#         sync_main_installment_transaction(
#             instance=instance,
#             payment_amount=new_actual_payment,
#             from_account=False,
#         )

#         # extra savings transaction
#         sync_extra_payment_savings(
#             instance=instance,
#             old_extra_amount=old_extra_amount,
#             new_extra_amount=new_extra_amount,
#         )

#         # due update
#         new_due_amount = installment_amount - new_actual_payment

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0"),
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount,
#             )









# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver

# # =========================================================
# # MODELNAME HELPERS
# # =========================================================

# def get_installment_payment_modelname(from_account=False):
#     return "Installment Payment From Account" if from_account else "Installment Payment"


# def get_extra_payment_savings_modelname():
#     return "Extra Payment Savings"
# 
# 
# # =========================================================
# # TRANSACTION CREATE HELPERS
# # =========================================================

# def create_installment_payment_history_transaction(instance, payment_delta, remaining_due, from_account=False):
#     """
#     Every payment creates a NEW transaction row.
#     This keeps payment history.
#     """
#     payment_delta = Decimal(str(payment_delta or 0))
#     remaining_due = Decimal(str(remaining_due or 0))

#     if payment_delta <= 0:
#         return None

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=payment_delta,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_installment_payment_modelname(from_account),
#     )

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = payment_delta

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = payment_delta

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = remaining_due

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_installment_payment_modelname(from_account)

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     tx.save()
#     return tx


# def create_extra_payment_savings_transaction(instance, extra_amount):
#     """
#     Extra amount over installment amount goes to savings transaction.
#     """
#     extra_amount = Decimal(str(extra_amount or 0))

#     if extra_amount <= 0:
#         return None

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=extra_amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_extra_payment_savings_modelname(),
#     )

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = extra_amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = extra_amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_extra_payment_savings_modelname()

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     tx.save()
#     return tx


# # =========================================================
# # PRE SAVE - OLD VALUE STORE
# # =========================================================

# @receiver(pre_save, sender=Installment)
# def store_old_installment_values(sender, instance, **kwargs):
#     if not instance.pk:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None
#         return

#     try:
#         old_instance = Installment.objects.get(pk=instance.pk)
#         instance._old_status = old_instance.installment_status
#         instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
#         instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
#     except Installment.DoesNotExist:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None


# # =========================================================
# # MAIN SIGNAL
# # =========================================================

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Rule:
#     - installment_pay is treated as TOTAL PAID so far for this installment
#     - every increase creates a NEW transaction row for only the increased amount
#     - due_amount decreases accordingly
#     - every transaction stores loan_id and installment_id
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if instance.installment_pay is None:
#         return

#     new_pay = Decimal(str(instance.installment_pay or 0))
#     installment_amount = Decimal(str(instance.amount or 0))

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     if old_pay == new_pay:
#         return

#     # current actual paid up to installment amount
#     old_actual_paid = min(old_pay, installment_amount)
#     new_actual_paid = min(new_pay, installment_amount)

#     # only new payment portion for this save
#     payment_delta = new_actual_paid - old_actual_paid

#     # extra over installment amount
#     old_extra_amount = max(old_pay - installment_amount, Decimal("0"))
#     new_extra_amount = max(new_pay - installment_amount, Decimal("0"))
#     extra_delta = new_extra_amount - old_extra_amount

#     # new remaining due after this save
#     remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

#     print("\n--- Installment Payment Update ---")
#     print(f"Installment ID: {instance.id}")
#     print(f"Loan ID: {instance.loan_id}")
#     print(f"Old Pay: {old_pay}")
#     print(f"New Pay: {new_pay}")
#     print(f"Payment Delta: {payment_delta}")
#     print(f"Remaining Due: {remaining_due}")
#     print(f"Extra Delta: {extra_delta}")

#     if instance.pay_from_account:
#         try:
#             total_diff = new_pay - old_pay

#             if total_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     total_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )

#             elif total_diff < 0:
#                 # rollback/reduction case
#                 update_customer_balance(instance.customer_name, abs(total_diff))

#             # create new main payment transaction only for increased amount
#             if payment_delta > 0:
#                 create_installment_payment_history_transaction(
#                     instance=instance,
#                     payment_delta=payment_delta,
#                     remaining_due=remaining_due,
#                     from_account=True,
#                 )

#             # extra payment savings transaction only for increased extra
#             if extra_delta > 0:
#                 update_customer_balance(instance.customer_name, extra_delta)
#                 create_extra_payment_savings_transaction(
#                     instance=instance,
#                     extra_amount=extra_delta,
#                 )

#             # if payment reduced and old extra existed, reverse savings balance
#             elif extra_delta < 0:
#                 update_customer_balance(instance.customer_name, extra_delta)  # negative adjustment

#             # update installment due/status
#             if remaining_due <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0"),
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=remaining_due,
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount if old_due_amount is not None else installment_amount,
#             )
#             raise ValidationError(str(e))

#     else:
#         # only create transaction for increased payment
#         if payment_delta > 0:
#             create_installment_payment_history_transaction(
#                 instance=instance,
#                 payment_delta=payment_delta,
#                 remaining_due=remaining_due,
#                 from_account=False,
#             )

#         # handle extra payment savings delta
#         if extra_delta > 0:
#             update_customer_balance(instance.customer_name, extra_delta)
#             create_extra_payment_savings_transaction(
#                 instance=instance,
#                 extra_amount=extra_delta,
#             )
#         elif extra_delta < 0:
#             update_customer_balance(instance.customer_name, extra_delta)  # negative adjustment

#         # update installment due/status
#         if remaining_due <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0"),
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=remaining_due,
#             )






# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from django.utils import timezone

# # =========================================================
# # MODEL NAME HELPERS
# # =========================================================

# def get_installment_modelname(instance, from_account=False):
#     base = "Installment Payment From Account" if from_account else "Installment Payment"
#     return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# def get_previous_installment_modelname(instance, from_account=False):
#     base = "Previous Installment Pay From Account" if from_account else "Previous Installment Pay"
#     return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# def get_extra_payment_modelname(instance):
#     return f"Extra Payment Savings | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# # =========================================================
# # DATE HELPERS
# # =========================================================

# def is_same_day_transaction(tx):
#     if not tx:
#         return False

#     today = timezone.localdate()

#     # use whichever field exists in your Transection model
#     if hasattr(tx, "date") and tx.date:
#         try:
#             return tx.date == today
#         except Exception:
#             pass

#     if hasattr(tx, "created_at") and tx.created_at:
#         try:
#             return tx.created_at.date() == today
#         except Exception:
#             pass

#     if hasattr(tx, "created") and tx.created:
#         try:
#             return tx.created.date() == today
#         except Exception:
#             pass

#     return False


# # =========================================================
# # QUERY HELPERS
# # =========================================================

# def get_installment_transactions(instance):
#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     qs = qs.filter(
#         modelname__iregex=r"^(Installment Payment|Installment Payment From Account|Previous Installment Pay|Previous Installment Pay From Account)"
#     )

#     return qs.order_by("-id")


# def get_latest_installment_transaction(instance):
#     return get_installment_transactions(instance).first()


# def get_extra_transactions(instance):
#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     qs = qs.filter(modelname__startswith="Extra Payment Savings")

#     return qs.order_by("-id")


# def get_latest_extra_transaction(instance):
#     return get_extra_transactions(instance).first()


# # =========================================================
# # COMMON FIELD SETTER
# # =========================================================

# def set_common_transaction_fields(tx, instance, modelname, amount, due_amount):
#     amount = Decimal(str(amount or 0))
#     due_amount = Decimal(str(due_amount or 0))

#     if hasattr(tx, "modelname"):
#         tx.modelname = modelname

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = due_amount

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# # =========================================================
# # CREATE / UPDATE TRANSACTION HELPERS
# # =========================================================

# def create_transaction_row(instance, modelname, amount, due_amount):
#     amount = Decimal(str(amount or 0))
#     due_amount = Decimal(str(due_amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname,
#     )

#     tx = set_common_transaction_fields(
#         tx=tx,
#         instance=instance,
#         modelname=modelname,
#         amount=amount,
#         due_amount=due_amount,
#     )
#     tx.save()
#     return tx


# def update_transaction_row(tx, instance, modelname, amount, due_amount):
#     tx = set_common_transaction_fields(
#         tx=tx,
#         instance=instance,
#         modelname=modelname,
#         amount=amount,
#         due_amount=due_amount,
#     )
#     tx.save()
#     return tx


# # =========================================================
# # INSTALLMENT PAYMENT SYNC
# # =========================================================

# def sync_installment_payment_transaction(instance, old_pay, new_pay, from_account=False):
#     """
#     Logic:
#     - first payment -> Installment Payment
#     - same day edit -> update same transaction
#     - later day increase -> create new Previous Installment Pay transaction
#     """
#     installment_amount = Decimal(str(instance.amount or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     new_pay = Decimal(str(new_pay or 0))

#     old_actual_paid = min(old_pay, installment_amount)
#     new_actual_paid = min(new_pay, installment_amount)

#     delta = new_actual_paid - old_actual_paid
#     remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

#     latest_tx = get_latest_installment_transaction(instance)

#     # no main payment
#     if new_actual_paid <= 0:
#         if latest_tx and is_same_day_transaction(latest_tx):
#             latest_tx.delete()
#         return None

#     # first ever payment
#     if not latest_tx:
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_installment_modelname(instance, from_account=from_account),
#             amount=new_actual_paid,
#             due_amount=remaining_due,
#         )

#     # same day edit -> update latest row
#     if is_same_day_transaction(latest_tx):
#         current_amount = Decimal(str(getattr(latest_tx, "amount", 0) or 0))
#         updated_amount = current_amount + delta

#         if updated_amount <= 0:
#             latest_tx.delete()
#             return None

#         return update_transaction_row(
#             tx=latest_tx,
#             instance=instance,
#             modelname=latest_tx.modelname,  # keep old modelname
#             amount=updated_amount,
#             due_amount=remaining_due,
#         )

#     # another day + increased pay -> new "Previous Installment Pay"
#     if delta > 0:
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_previous_installment_modelname(instance, from_account=from_account),
#             amount=delta,
#             due_amount=remaining_due,
#         )

#     # another day + reduced pay -> no new transaction
#     return latest_tx


# # =========================================================
# # EXTRA PAYMENT SAVINGS SYNC
# # =========================================================

# def sync_extra_payment_savings(instance, old_pay, new_pay):
#     """
#     Extra amount = payment over installment amount

#     Rules:
#     - same day extra create/update/delete
#     - later extra increase -> create new row
#     """
#     installment_amount = Decimal(str(instance.amount or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     new_pay = Decimal(str(new_pay or 0))

#     old_extra = max(old_pay - installment_amount, Decimal("0"))
#     new_extra = max(new_pay - installment_amount, Decimal("0"))

#     latest_extra_tx = get_latest_extra_transaction(instance)

#     # same day existing extra -> update/delete
#     if latest_extra_tx and is_same_day_transaction(latest_extra_tx):
#         delta_balance = new_extra - old_extra

#         if delta_balance != 0:
#             update_customer_balance(instance.customer_name, delta_balance)

#         if new_extra <= 0:
#             latest_extra_tx.delete()
#             return None

#         return update_transaction_row(
#             tx=latest_extra_tx,
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=new_extra,
#             due_amount=Decimal("0"),
#         )

#     # no existing extra row yet
#     if new_extra > 0 and not latest_extra_tx:
#         update_customer_balance(instance.customer_name, new_extra)
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=new_extra,
#             due_amount=Decimal("0"),
#         )

#     # later day extra increase -> new row
#     extra_delta = new_extra - old_extra
#     if extra_delta > 0:
#         update_customer_balance(instance.customer_name, extra_delta)
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=extra_delta,
#             due_amount=Decimal("0"),
#         )

#     # later day extra reduced -> do not touch old history row
#     return latest_extra_tx


# # =========================================================
# # PRE SAVE - STORE OLD VALUES
# # =========================================================

# @receiver(pre_save, sender=Installment)
# def store_old_installment_values(sender, instance, **kwargs):
#     if not instance.pk:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None
#         return

#     try:
#         old_instance = Installment.objects.get(pk=instance.pk)
#         instance._old_status = old_instance.installment_status
#         instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
#         instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
#     except Installment.DoesNotExist:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None


# # =========================================================
# # MAIN SIGNAL
# # =========================================================

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     installment_pay is treated as cumulative total paid for that installment
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if instance.installment_pay is None:
#         return

#     new_pay = Decimal(str(instance.installment_pay or 0))
#     installment_amount = Decimal(str(instance.amount or 0))

#     if old_pay == new_pay:
#         return

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     new_actual_paid = min(new_pay, installment_amount)
#     remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

#     print("\n--- Installment Payment Update ---")
#     print(f"Installment ID: {instance.id}")
#     print(f"Loan ID: {instance.loan_id}")
#     print(f"Old Pay: {old_pay}")
#     print(f"New Pay: {new_pay}")
#     print(f"Remaining Due: {remaining_due}")

#     if instance.pay_from_account:
#         try:
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )
#             elif pay_diff < 0:
#                 update_customer_balance(instance.customer_name, abs(pay_diff))

#             sync_installment_payment_transaction(
#                 instance=instance,
#                 old_pay=old_pay,
#                 new_pay=new_pay,
#                 from_account=True,
#             )

#             sync_extra_payment_savings(
#                 instance=instance,
#                 old_pay=old_pay,
#                 new_pay=new_pay,
#             )

#             if remaining_due <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0"),
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=remaining_due,
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount if old_due_amount is not None else installment_amount,
#             )
#             raise ValidationError(str(e))

#     else:
#         sync_installment_payment_transaction(
#             instance=instance,
#             old_pay=old_pay,
#             new_pay=new_pay,
#             from_account=False,
#         )

#         sync_extra_payment_savings(
#             instance=instance,
#             old_pay=old_pay,
#             new_pay=new_pay,
#         )

#         if remaining_due <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0"),
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=remaining_due,
#             )




# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import pre_save, post_save
# from django.dispatch import receiver
# from django.utils import timezone

# # =========================================================
# # MODEL NAME HELPERS
# # =========================================================

# def get_installment_modelname(instance, from_account=False):
#     base = "Installment Payment From Account" if from_account else "Installment Payment"
#     return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# def get_previous_installment_modelname(instance, from_account=False):
#     base = "Previous Installment Pay From Account" if from_account else "Previous Installment Pay"
#     return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# def get_extra_payment_modelname(instance):
#     return f"Extra Payment Savings | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# # =========================================================
# # DATE HELPERS
# # =========================================================

# def is_same_day_transaction(tx):
#     if not tx:
#         return False

#     today = timezone.localdate()

#     # use whichever field exists in your Transection model
#     if hasattr(tx, "date") and tx.date:
#         try:
#             return tx.date == today
#         except Exception:
#             pass

#     if hasattr(tx, "created_at") and tx.created_at:
#         try:
#             return tx.created_at.date() == today
#         except Exception:
#             pass

#     if hasattr(tx, "created") and tx.created:
#         try:
#             return tx.created.date() == today
#         except Exception:
#             pass

#     return False


# # =========================================================
# # QUERY HELPERS
# # =========================================================

# def transection_has_field(field_name):
#     try:
#         Transection._meta.get_field(field_name)
#         return True
#     except Exception:
#         return False


# def scope_transaction_queryset_to_installment(qs, instance):
#     """
#     Must scope to the exact installment.
#     Otherwise same customer's other installment transactions
#     can be picked and updated accidentally.
#     """
#     if transection_has_field("loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)
#     else:
#         qs = qs.filter(modelname__icontains=f"Loan: {instance.loan_id}")

#     if transection_has_field("installment_id"):
#         qs = qs.filter(installment_id=instance.id)
#     else:
#         qs = qs.filter(modelname__icontains=f"Installment ID: {instance.id}")

#     return qs


# def get_installment_transactions(instance):
#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name
#     )

#     qs = scope_transaction_queryset_to_installment(qs, instance)

#     qs = qs.filter(
#         modelname__iregex=r"^(Installment Payment|Installment Payment From Account|Previous Installment Pay|Previous Installment Pay From Account)"
#     )

#     return qs.order_by("-id")


# def get_latest_installment_transaction(instance):
#     return get_installment_transactions(instance).first()


# def get_extra_transactions(instance):
#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name
#     )

#     qs = scope_transaction_queryset_to_installment(qs, instance)

#     qs = qs.filter(modelname__startswith="Extra Payment Savings")

#     return qs.order_by("-id")


# def get_latest_extra_transaction(instance):
#     return get_extra_transactions(instance).first()


# # =========================================================
# # COMMON FIELD SETTER
# # =========================================================

# def set_common_transaction_fields(tx, instance, modelname, amount, due_amount):
#     amount = Decimal(str(amount or 0))
#     due_amount = Decimal(str(due_amount or 0))

#     if hasattr(tx, "modelname"):
#         tx.modelname = modelname

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = due_amount

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# # =========================================================
# # CREATE / UPDATE TRANSACTION HELPERS
# # =========================================================

# def create_transaction_row(instance, modelname, amount, due_amount):
#     amount = Decimal(str(amount or 0))
#     due_amount = Decimal(str(due_amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=modelname,
#     )

#     tx = set_common_transaction_fields(
#         tx=tx,
#         instance=instance,
#         modelname=modelname,
#         amount=amount,
#         due_amount=due_amount,
#     )
#     tx.save()
#     return tx


# def update_transaction_row(tx, instance, modelname, amount, due_amount):
#     tx = set_common_transaction_fields(
#         tx=tx,
#         instance=instance,
#         modelname=modelname,
#         amount=amount,
#         due_amount=due_amount,
#     )
#     tx.save()
#     return tx


# # =========================================================
# # INSTALLMENT PAYMENT SYNC
# # =========================================================

# def sync_installment_payment_transaction(instance, old_pay, new_pay, from_account=False):
#     """
#     Logic:
#     - first payment -> Installment Payment
#     - same day edit -> update same transaction
#     - later day increase -> create new Previous Installment Pay transaction
#     """
#     installment_amount = Decimal(str(instance.amount or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     new_pay = Decimal(str(new_pay or 0))

#     old_actual_paid = min(old_pay, installment_amount)
#     new_actual_paid = min(new_pay, installment_amount)

#     delta = new_actual_paid - old_actual_paid
#     remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

#     latest_tx = get_latest_installment_transaction(instance)

#     # no main payment
#     if new_actual_paid <= 0:
#         if latest_tx and is_same_day_transaction(latest_tx):
#             latest_tx.delete()
#         return None

#     # first ever payment
#     if not latest_tx:
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_installment_modelname(instance, from_account=from_account),
#             amount=new_actual_paid,
#             due_amount=remaining_due,
#         )

#     # same day edit -> update latest row
#     if is_same_day_transaction(latest_tx):
#         current_amount = Decimal(str(getattr(latest_tx, "amount", 0) or 0))
#         updated_amount = current_amount + delta

#         if updated_amount <= 0:
#             latest_tx.delete()
#             return None

#         return update_transaction_row(
#             tx=latest_tx,
#             instance=instance,
#             modelname=latest_tx.modelname,  # keep old modelname
#             amount=updated_amount,
#             due_amount=remaining_due,
#         )

#     # another day + increased pay -> new "Previous Installment Pay"
#     if delta > 0:
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_previous_installment_modelname(instance, from_account=from_account),
#             amount=delta,
#             due_amount=remaining_due,
#         )

#     # another day + reduced pay -> no new transaction
#     return latest_tx


# # =========================================================
# # EXTRA PAYMENT SAVINGS SYNC
# # =========================================================

# def sync_extra_payment_savings(instance, old_pay, new_pay):
#     """
#     Extra amount = payment over installment amount

#     Rules:
#     - same day extra create/update/delete
#     - later extra increase -> create new row
#     """
#     installment_amount = Decimal(str(instance.amount or 0))
#     old_pay = Decimal(str(old_pay or 0))
#     new_pay = Decimal(str(new_pay or 0))

#     old_extra = max(old_pay - installment_amount, Decimal("0"))
#     new_extra = max(new_pay - installment_amount, Decimal("0"))

#     latest_extra_tx = get_latest_extra_transaction(instance)

#     # same day existing extra -> update/delete
#     if latest_extra_tx and is_same_day_transaction(latest_extra_tx):
#         delta_balance = new_extra - old_extra

#         if delta_balance != 0:
#             update_customer_balance(instance.customer_name, delta_balance)

#         if new_extra <= 0:
#             latest_extra_tx.delete()
#             return None

#         return update_transaction_row(
#             tx=latest_extra_tx,
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=new_extra,
#             due_amount=Decimal("0"),
#         )

#     # no existing extra row yet
#     if new_extra > 0 and not latest_extra_tx:
#         update_customer_balance(instance.customer_name, new_extra)
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=new_extra,
#             due_amount=Decimal("0"),
#         )

#     # later day extra increase -> new row
#     extra_delta = new_extra - old_extra
#     if extra_delta > 0:
#         update_customer_balance(instance.customer_name, extra_delta)
#         return create_transaction_row(
#             instance=instance,
#             modelname=get_extra_payment_modelname(instance),
#             amount=extra_delta,
#             due_amount=Decimal("0"),
#         )

#     # later day extra reduced -> do not touch old history row
#     return latest_extra_tx


# # =========================================================
# # PRE SAVE - STORE OLD VALUES
# # =========================================================

# @receiver(pre_save, sender=Installment)
# def store_old_installment_values(sender, instance, **kwargs):
#     if not instance.pk:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None
#         return

#     try:
#         old_instance = Installment.objects.get(pk=instance.pk)
#         instance._old_status = old_instance.installment_status
#         instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
#         instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
#     except Installment.DoesNotExist:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None


# # =========================================================
# # MAIN SIGNAL
# # =========================================================

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     installment_pay is treated as cumulative total paid for that installment
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if instance.installment_pay is None:
#         return

#     new_pay = Decimal(str(instance.installment_pay or 0))
#     installment_amount = Decimal(str(instance.amount or 0))

#     if old_pay == new_pay:
#         return

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     new_actual_paid = min(new_pay, installment_amount)
#     remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

#     print("\n--- Installment Payment Update ---")
#     print(f"Installment ID: {instance.id}")
#     print(f"Loan ID: {instance.loan_id}")
#     print(f"Old Pay: {old_pay}")
#     print(f"New Pay: {new_pay}")
#     print(f"Remaining Due: {remaining_due}")

#     if instance.pay_from_account:
#         try:
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )
#             elif pay_diff < 0:
#                 update_customer_balance(instance.customer_name, abs(pay_diff))

#             sync_installment_payment_transaction(
#                 instance=instance,
#                 old_pay=old_pay,
#                 new_pay=new_pay,
#                 from_account=True,
#             )

#             sync_extra_payment_savings(
#                 instance=instance,
#                 old_pay=old_pay,
#                 new_pay=new_pay,
#             )

#             if remaining_due <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0"),
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=remaining_due,
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount if old_due_amount is not None else installment_amount,
#             )
#             raise ValidationError(str(e))

#     else:
#         sync_installment_payment_transaction(
#             instance=instance,
#             old_pay=old_pay,
#             new_pay=new_pay,
#             from_account=False,
#         )

#         sync_extra_payment_savings(
#             instance=instance,
#             old_pay=old_pay,
#             new_pay=new_pay,
#         )

#         if remaining_due <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0"),
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=remaining_due,
#             )













from decimal import Decimal
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils import timezone

# =========================================================
# MODEL NAME HELPERS
# =========================================================

def get_installment_modelname(instance, from_account=False):
    base = "Installment Payment From Account" if from_account else "Installment Payment"
    return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


def get_previous_installment_modelname(instance, from_account=False):
    base = "Previous Installment Pay From Account" if from_account else "Previous Installment Pay"
    return f"{base} | Loan: {instance.loan_id} | Installment ID: {instance.id}"


def get_extra_payment_modelname(instance):
    return f"Extra Payment Savings | Loan: {instance.loan_id} | Installment ID: {instance.id}"


# =========================================================
# DATE HELPERS
# =========================================================

def is_same_day_transaction(tx):
    if not tx:
        return False

    today = timezone.localdate()

    if hasattr(tx, "date") and tx.date:
        try:
            return tx.date == today
        except Exception:
            pass

    if hasattr(tx, "created_at") and tx.created_at:
        try:
            return tx.created_at.date() == today
        except Exception:
            pass

    if hasattr(tx, "created") and tx.created:
        try:
            return tx.created.date() == today
        except Exception:
            pass

    return False


# =========================================================
# QUERY HELPERS
# =========================================================

def transection_has_field(field_name):
    try:
        Transection._meta.get_field(field_name)
        return True
    except Exception:
        return False


def scope_transaction_queryset_to_installment(qs, instance):
    if transection_has_field("loan_id"):
        qs = qs.filter(loan_id=instance.loan_id)
    else:
        qs = qs.filter(modelname__icontains=f"Loan: {instance.loan_id}")

    if transection_has_field("installment_id"):
        qs = qs.filter(installment_id=instance.id)
    else:
        qs = qs.filter(modelname__icontains=f"Installment ID: {instance.id}")

    return qs


def get_installment_transactions(instance):
    qs = Transection.objects.filter(customer_name=instance.customer_name)
    qs = scope_transaction_queryset_to_installment(qs, instance)

    qs = qs.filter(
        modelname__iregex=r"^(Installment Payment|Installment Payment From Account|Previous Installment Pay|Previous Installment Pay From Account)"
    )

    return qs.order_by("-id")


def get_latest_installment_transaction(instance):
    return get_installment_transactions(instance).first()


def get_extra_transactions(instance):
    qs = Transection.objects.filter(customer_name=instance.customer_name)
    qs = scope_transaction_queryset_to_installment(qs, instance)
    qs = qs.filter(modelname__startswith="Extra Payment Savings")
    return qs.order_by("-id")


def get_latest_extra_transaction(instance):
    return get_extra_transactions(instance).first()


# =========================================================
# COMMON FIELD SETTER
# =========================================================

def set_common_transaction_fields(tx, instance, modelname, amount, due_amount):
    amount = Decimal(str(amount or 0))
    due_amount = Decimal(str(due_amount or 0))

    if hasattr(tx, "modelname"):
        tx.modelname = modelname

    if hasattr(tx, "customer_name"):
        tx.customer_name = instance.customer_name

    if hasattr(tx, "received_by"):
        tx.received_by = instance.received_by

    if hasattr(tx, "transection_type"):
        tx.transection_type = "cashin"

    if hasattr(tx, "amount"):
        tx.amount = amount

    if hasattr(tx, "paid"):
        tx.paid = True

    if hasattr(tx, "paid_amount"):
        tx.paid_amount = amount

    if hasattr(tx, "due_amount"):
        tx.due_amount = due_amount

    if transection_has_field("loan_id"):
        tx.loan_id = instance.loan_id

    if transection_has_field("installment_id"):
        tx.installment_id = instance.id

    return tx


# =========================================================
# CREATE / UPDATE TRANSACTION HELPERS
# =========================================================

def create_transaction_row(instance, modelname, amount, due_amount):
    amount = Decimal(str(amount or 0))
    due_amount = Decimal(str(due_amount or 0))

    tx = create_transaction_with_customer_info(
        instance.customer_name,
        transection_type="cashin",
        amount=amount,
        customer_name=instance.customer_name,
        received_by=instance.received_by,
        modelname=modelname,
    )

    tx = set_common_transaction_fields(
        tx=tx,
        instance=instance,
        modelname=modelname,
        amount=amount,
        due_amount=due_amount,
    )
    tx.save()
    return tx


def update_transaction_row(tx, instance, modelname, amount, due_amount):
    tx = set_common_transaction_fields(
        tx=tx,
        instance=instance,
        modelname=modelname,
        amount=amount,
        due_amount=due_amount,
    )
    tx.save()
    return tx


# =========================================================
# INSTALLMENT PAYMENT SYNC
# =========================================================

def sync_installment_payment_transaction(instance, old_pay, new_pay, from_account=False):
    """
    Logic:
    - first payment -> Installment Payment
    - same day edit -> update same transaction
    - later day increase -> create new Previous Installment Pay transaction
    """
    installment_amount = Decimal(str(instance.amount or 0))
    old_pay = Decimal(str(old_pay or 0))
    new_pay = Decimal(str(new_pay or 0))

    old_actual_paid = min(old_pay, installment_amount)
    new_actual_paid = min(new_pay, installment_amount)

    delta = new_actual_paid - old_actual_paid
    remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

    latest_tx = get_latest_installment_transaction(instance)

    if new_actual_paid <= 0:
        if latest_tx and is_same_day_transaction(latest_tx):
            latest_tx.delete()
        return None

    if not latest_tx:
        return create_transaction_row(
            instance=instance,
            modelname=get_installment_modelname(instance, from_account=from_account),
            amount=new_actual_paid,
            due_amount=remaining_due,
        )

    if is_same_day_transaction(latest_tx):
        current_amount = Decimal(str(getattr(latest_tx, "amount", 0) or 0))
        updated_amount = current_amount + delta

        if updated_amount <= 0:
            latest_tx.delete()
            return None

        return update_transaction_row(
            tx=latest_tx,
            instance=instance,
            modelname=latest_tx.modelname,
            amount=updated_amount,
            due_amount=remaining_due,
        )

    if delta > 0:
        return create_transaction_row(
            instance=instance,
            modelname=get_previous_installment_modelname(instance, from_account=from_account),
            amount=delta,
            due_amount=remaining_due,
        )

    return latest_tx


# =========================================================
# EXTRA PAYMENT SAVINGS SYNC
# =========================================================

def sync_extra_payment_savings(instance, old_pay, new_pay):
    """
    Extra amount = payment over installment amount

    Rules:
    - same day extra create/update/delete
    - later extra increase -> create new row
    """
    installment_amount = Decimal(str(instance.amount or 0))
    old_pay = Decimal(str(old_pay or 0))
    new_pay = Decimal(str(new_pay or 0))

    old_extra = max(old_pay - installment_amount, Decimal("0"))
    new_extra = max(new_pay - installment_amount, Decimal("0"))

    latest_extra_tx = get_latest_extra_transaction(instance)

    if latest_extra_tx and is_same_day_transaction(latest_extra_tx):
        delta_balance = new_extra - old_extra

        if delta_balance != 0:
            update_customer_balance(instance.customer_name, delta_balance)

        if new_extra <= 0:
            latest_extra_tx.delete()
            return None

        return update_transaction_row(
            tx=latest_extra_tx,
            instance=instance,
            modelname=get_extra_payment_modelname(instance),
            amount=new_extra,
            due_amount=Decimal("0"),
        )

    if new_extra > 0 and not latest_extra_tx:
        update_customer_balance(instance.customer_name, new_extra)
        return create_transaction_row(
            instance=instance,
            modelname=get_extra_payment_modelname(instance),
            amount=new_extra,
            due_amount=Decimal("0"),
        )

    extra_delta = new_extra - old_extra
    if extra_delta > 0:
        update_customer_balance(instance.customer_name, extra_delta)
        return create_transaction_row(
            instance=instance,
            modelname=get_extra_payment_modelname(instance),
            amount=extra_delta,
            due_amount=Decimal("0"),
        )

    return latest_extra_tx


# =========================================================
# PRE SAVE - STORE OLD VALUES
# =========================================================

@receiver(pre_save, sender=Installment)
def store_old_installment_values(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_status = None
        instance._old_pay = Decimal("0")
        instance._old_due_amount = None
        return

    try:
        old_instance = Installment.objects.get(pk=instance.pk)
        instance._old_status = old_instance.installment_status
        instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
        instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
    except Installment.DoesNotExist:
        instance._old_status = None
        instance._old_pay = Decimal("0")
        instance._old_due_amount = None


# =========================================================
# MAIN SIGNAL
# =========================================================

@receiver(post_save, sender=Installment)
def handle_installment_payment(sender, instance, created, **kwargs):
    """
    installment_pay is treated as cumulative total paid for that installment
    """
    if created:
        return

    old_status = getattr(instance, "_old_status", None)
    old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
    old_due_amount = getattr(instance, "_old_due_amount", None)

    if instance.installment_pay is None:
        return

    new_pay = Decimal(str(instance.installment_pay or 0))
    installment_amount = Decimal(str(instance.amount or 0))

    if old_pay == new_pay:
        return

    if new_pay < 0:
        raise ValidationError("Payment cannot be negative")

    new_actual_paid = min(new_pay, installment_amount)
    remaining_due = max(installment_amount - new_actual_paid, Decimal("0"))

    print("\n--- Installment Payment Update ---")
    print(f"Installment ID: {instance.id}")
    print(f"Loan ID: {instance.loan_id}")
    print(f"Old Pay: {old_pay}")
    print(f"New Pay: {new_pay}")
    print(f"Remaining Due: {remaining_due}")

    if instance.pay_from_account:
        try:
            pay_diff = new_pay - old_pay

            if pay_diff > 0:
                check_and_deduct_balance(
                    instance.customer_name,
                    pay_diff,
                    f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
                )
            elif pay_diff < 0:
                update_customer_balance(instance.customer_name, abs(pay_diff))

            sync_installment_payment_transaction(
                instance=instance,
                old_pay=old_pay,
                new_pay=new_pay,
                from_account=True,
            )

            sync_extra_payment_savings(
                instance=instance,
                old_pay=old_pay,
                new_pay=new_pay,
            )

            if remaining_due <= 0:
                Installment.objects.filter(pk=instance.pk).update(
                    installment_status="paid",
                    due_amount=Decimal("0"),
                )
            else:
                Installment.objects.filter(pk=instance.pk).update(
                    installment_status="due",
                    due_amount=remaining_due,
                )

        except InsufficientBalanceError as e:
            Installment.objects.filter(pk=instance.pk).update(
                installment_pay=old_pay,
                installment_status=old_status,
                due_amount=old_due_amount if old_due_amount is not None else installment_amount,
            )
            raise ValidationError(str(e))

    else:
        sync_installment_payment_transaction(
            instance=instance,
            old_pay=old_pay,
            new_pay=new_pay,
            from_account=False,
        )

        sync_extra_payment_savings(
            instance=instance,
            old_pay=old_pay,
            new_pay=new_pay,
        )

        if remaining_due <= 0:
            Installment.objects.filter(pk=instance.pk).update(
                installment_status="paid",
                due_amount=Decimal("0"),
            )
        else:
            Installment.objects.filter(pk=instance.pk).update(
                installment_status="due",
                due_amount=remaining_due,
            )
















# from decimal import Decimal
# from django.core.exceptions import ValidationError
# from django.db.models.signals import post_save, pre_save
# from django.dispatch import receiver

# # =========================================================
# # MODELNAME HELPERS
# # =========================================================

# def get_installment_payment_modelname(from_account=False):
#     return "Installment Payment From Account" if from_account else "Installment Payment"


# def get_extra_payment_savings_modelname():
#     return "Extra Payment Savings"


# # =========================================================
# # QUERY HELPERS
# # =========================================================

# def get_existing_installment_transaction(instance, from_account=False):
#     modelname = get_installment_payment_modelname(from_account)

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname,
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# def get_existing_extra_transaction(instance):
#     modelname = get_extra_payment_savings_modelname()

#     qs = Transection.objects.filter(
#         customer_name=instance.customer_name,
#         modelname=modelname,
#     )

#     if hasattr(Transection, "loan_id"):
#         qs = qs.filter(loan_id=instance.loan_id)

#     if hasattr(Transection, "installment_id"):
#         qs = qs.filter(installment_id=instance.id)

#     return qs.order_by("-id").first()


# # =========================================================
# # FIELD ASSIGN HELPERS
# # =========================================================

# def assign_main_transaction_fields(tx, instance, amount, from_account=False):
#     amount = Decimal(str(amount or 0))
#     installment_amount = Decimal(str(instance.amount or 0))
#     due_amount = max(installment_amount - amount, Decimal("0"))

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_installment_payment_modelname(from_account)

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = due_amount

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# def assign_extra_transaction_fields(tx, instance, amount):
#     amount = Decimal(str(amount or 0))

#     if hasattr(tx, "modelname"):
#         tx.modelname = get_extra_payment_savings_modelname()

#     if hasattr(tx, "customer_name"):
#         tx.customer_name = instance.customer_name

#     if hasattr(tx, "received_by"):
#         tx.received_by = instance.received_by

#     if hasattr(tx, "transection_type"):
#         tx.transection_type = "cashin"

#     if hasattr(tx, "amount"):
#         tx.amount = amount

#     if hasattr(tx, "paid"):
#         tx.paid = True

#     if hasattr(tx, "paid_amount"):
#         tx.paid_amount = amount

#     if hasattr(tx, "due_amount"):
#         tx.due_amount = Decimal("0")

#     if hasattr(tx, "loan_id"):
#         tx.loan_id = instance.loan_id

#     if hasattr(tx, "installment_id"):
#         tx.installment_id = instance.id

#     return tx


# # =========================================================
# # CREATE HELPERS
# # =========================================================

# def create_installment_transaction(instance, amount, from_account=False):
#     amount = Decimal(str(amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_installment_payment_modelname(from_account),
#     )

#     tx = assign_main_transaction_fields(tx, instance, amount, from_account)
#     tx.save()

#     # mark_transaction_as_paid(tx, amount)  <-- এটা main transaction এ আর use করবে না
#     return tx


# def create_extra_transaction(instance, amount):
#     amount = Decimal(str(amount or 0))

#     tx = create_transaction_with_customer_info(
#         instance.customer_name,
#         transection_type="cashin",
#         amount=amount,
#         customer_name=instance.customer_name,
#         received_by=instance.received_by,
#         modelname=get_extra_payment_savings_modelname(),
#     )

#     tx = assign_extra_transaction_fields(tx, instance, amount)
#     tx.save()
#     return tx


# # =========================================================
# # SYNC HELPERS
# # =========================================================

# def sync_main_installment_transaction(instance, payment_amount, from_account=False):
#     payment_amount = Decimal(str(payment_amount or 0))
#     tx = get_existing_installment_transaction(instance, from_account=from_account)

#     if payment_amount <= 0:
#         if tx:
#             tx.delete()
#         return None

#     if tx:
#         tx = assign_main_transaction_fields(
#             tx=tx,
#             instance=instance,
#             amount=payment_amount,
#             from_account=from_account,
#         )
#         tx.save()
#         return tx

#     return create_installment_transaction(
#         instance=instance,
#         amount=payment_amount,
#         from_account=from_account,
#     )


# def sync_extra_payment_savings(instance, old_extra_amount, new_extra_amount):
#     old_extra_amount = Decimal(str(old_extra_amount or 0))
#     new_extra_amount = Decimal(str(new_extra_amount or 0))

#     extra_tx = get_existing_extra_transaction(instance)

#     if old_extra_amount > 0:
#         update_customer_balance(instance.customer_name, -old_extra_amount)

#     if new_extra_amount <= 0:
#         if extra_tx:
#             extra_tx.delete()
#         return None

#     update_customer_balance(instance.customer_name, new_extra_amount)

#     if extra_tx:
#         extra_tx = assign_extra_transaction_fields(
#             tx=extra_tx,
#             instance=instance,
#             amount=new_extra_amount,
#         )
#         extra_tx.save()
#         return extra_tx

#     return create_extra_transaction(instance, new_extra_amount)


# # =========================================================
# # PRE SAVE
# # =========================================================

# @receiver(pre_save, sender=Installment)
# def store_old_installment_values(sender, instance, **kwargs):
#     if not instance.pk:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None
#         return

#     try:
#         old_instance = Installment.objects.get(pk=instance.pk)
#         instance._old_status = old_instance.installment_status
#         instance._old_pay = Decimal(str(old_instance.installment_pay or 0))
#         instance._old_due_amount = Decimal(str(old_instance.due_amount or 0))
#     except Installment.DoesNotExist:
#         instance._old_status = None
#         instance._old_pay = Decimal("0")
#         instance._old_due_amount = None


# # =========================================================
# # MAIN SIGNAL
# # =========================================================

# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = Decimal(str(getattr(instance, "_old_pay", 0) or 0))
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if instance.installment_pay is None:
#         return

#     new_pay = Decimal(str(instance.installment_pay or 0))

#     if old_pay == new_pay:
#         return

#     installment_amount = Decimal(str(instance.amount or 0))

#     if new_pay < 0:
#         raise ValidationError("Payment cannot be negative")

#     old_actual_payment = min(old_pay, installment_amount)
#     new_actual_payment = min(new_pay, installment_amount)

#     old_extra_amount = max(old_pay - installment_amount, Decimal("0"))
#     new_extra_amount = max(new_pay - installment_amount, Decimal("0"))

#     if instance.pay_from_account:
#         try:
#             pay_diff = new_pay - old_pay

#             if pay_diff > 0:
#                 check_and_deduct_balance(
#                     instance.customer_name,
#                     pay_diff,
#                     f"Installment Payment Update ID: {instance.id}, Loan: {instance.loan_id}"
#                 )
#             elif pay_diff < 0:
#                 update_customer_balance(instance.customer_name, abs(pay_diff))

#             sync_main_installment_transaction(
#                 instance=instance,
#                 payment_amount=new_actual_payment,
#                 from_account=True,
#             )

#             sync_extra_payment_savings(
#                 instance=instance,
#                 old_extra_amount=old_extra_amount,
#                 new_extra_amount=new_extra_amount,
#             )

#             new_due_amount = max(installment_amount - new_actual_payment, Decimal("0"))

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=Decimal("0"),
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount,
#                 )

#         except InsufficientBalanceError as e:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_pay=old_pay,
#                 installment_status=old_status,
#                 due_amount=old_due_amount if old_due_amount is not None else installment_amount,
#             )
#             raise ValidationError(str(e))

#     else:
#         sync_main_installment_transaction(
#             instance=instance,
#             payment_amount=new_actual_payment,
#             from_account=False,
#         )

#         sync_extra_payment_savings(
#             instance=instance,
#             old_extra_amount=old_extra_amount,
#             new_extra_amount=new_extra_amount,
#         )

#         new_due_amount = max(installment_amount - new_actual_payment, Decimal("0"))

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=Decimal("0"),
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount,
#             )













































# @receiver(post_save, sender=Installment)
# def handle_installment_payment(sender, instance, created, **kwargs):
#     """
#     Installment payment keeps partial/full payment logic.
#     Update হলে transaction update হবে + customer account update হবে
#     """
#     if created:
#         return

#     old_status = getattr(instance, "_old_status", None)
#     old_pay = getattr(instance, "_old_pay", None)
#     old_due_amount = getattr(instance, "_old_due_amount", None)

#     if not (old_pay != instance.installment_pay and instance.installment_pay):
#         return

#     print(f"\n--- Installment Payment: ID {instance.id} ---")

#     installment_pay = Decimal(str(instance.installment_pay or 0))
#     current_due = Decimal(str(instance.due_amount or instance.amount))

#     if installment_pay <= 0:
#         print("Warning: No payment amount recorded")
#         return

#     if installment_pay > current_due:
#         actual_payment = current_due
#         extra_amount = installment_pay - current_due
#         print(f"Payment: {installment_pay:.2f}, Due: {current_due:.2f}, Extra: {extra_amount:.2f}")
#     else:
#         actual_payment = installment_pay
#         extra_amount = Decimal("0")
#         print(f"Payment: {installment_pay:.2f}, Due: {current_due:.2f}")

#     if instance.pay_from_account:
#         print("Pay from account enabled - processing account deduction...")

#         try:
#             check_and_deduct_balance(
#                 instance.customer_name,
#                 installment_pay,
#                 f"Installment Payment ID: {instance.id}"
#             )
#             print(f"✓ Deducted {installment_pay:.2f} from account")

#             main_modelname = f"Installment Payment from Account : {instance.id}, Loan: {instance.loan_id}"

#             transaction_obj = Transection.objects.filter(
#                 customer_name=instance.customer_name,
#                 modelname=main_modelname
#             ).first()

#             if transaction_obj:
#                 transaction_obj.transection_type = "cashin"
#                 transaction_obj.amount = instance.amount
#                 transaction_obj.customer_name = instance.customer_name
#                 transaction_obj.received_by = instance.received_by
#                 transaction_obj.modelname = main_modelname
#             else:
#                 transaction_obj = create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashin",
#                     amount=instance.amount,
#                     customer_name=instance.customer_name,
#                     received_by=instance.received_by,
#                     modelname=main_modelname
#                 )

#             if hasattr(transaction_obj, "paid"):
#                 transaction_obj.paid = actual_payment >= current_due

#             if hasattr(transaction_obj, "paid_amount"):
#                 transaction_obj.paid_amount = actual_payment

#             if hasattr(transaction_obj, "due_amount"):
#                 transaction_obj.due_amount = max(Decimal("0"), current_due - actual_payment)

#             transaction_obj.save()

#             new_due_amount = current_due - actual_payment

#             if new_due_amount <= 0:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="paid",
#                     due_amount=0
#                 )
#             else:
#                 Installment.objects.filter(pk=instance.pk).update(
#                     installment_status="due",
#                     due_amount=new_due_amount
#                 )

#             # extra saving হলে customer account update হবে
#             if extra_amount > 0:
#                 update_customer_balance(instance.customer_name, extra_amount)

#                 extra_modelname = f"Extra Payment Savings : {instance.id}"

#                 extra_tx = Transection.objects.filter(
#                     customer_name=instance.customer_name,
#                     modelname=extra_modelname
#                 ).first()

#                 if extra_tx:
#                     extra_tx.transection_type = "cashin"
#                     extra_tx.amount = extra_amount
#                     extra_tx.customer_name = instance.customer_name
#                     extra_tx.received_by = instance.received_by
#                     extra_tx.modelname = extra_modelname
#                     extra_tx.save()
#                 else:
#                     extra_tx = create_transaction_with_customer_info(
#                         instance.customer_name,
    #                     transection_type="cashin",
    #                     amount=extra_amount,
    #                     customer_name=instance.customer_name,
    #                     received_by=instance.received_by,
    #                     modelname=extra_modelname
    #                 )

    #             mark_transaction_as_paid(extra_tx, extra_amount)

    #     except InsufficientBalanceError as e:
    #         Installment.objects.filter(pk=instance.pk).update(
    #             installment_pay=old_pay,
    #             installment_status=old_status,
    #             due_amount=old_due_amount
    #         )
    #         raise ValidationError(str(e))

    # else:
    #     main_modelname = f"Installment Payment : {instance.id}, Loan: {instance.loan_id}"

    #     transaction_obj = Transection.objects.filter(
    #         customer_name=instance.customer_name,
    #         modelname=main_modelname
    #     ).first()

    #     if transaction_obj:
    #         transaction_obj.transection_type = "cashin"
    #         transaction_obj.amount = instance.amount
    #         transaction_obj.customer_name = instance.customer_name
#             transaction_obj.received_by = instance.received_by
#             transaction_obj.modelname = main_modelname
#         else:
#             transaction_obj = create_transaction_with_customer_info(
#                 instance.customer_name,
#                 transection_type="cashin",
#                 amount=instance.amount,
#                 customer_name=instance.customer_name,
#                 received_by=instance.received_by,
#                 modelname=main_modelname
#             )

#         if hasattr(transaction_obj, "paid"):
#             transaction_obj.paid = actual_payment >= current_due

#         if hasattr(transaction_obj, "paid_amount"):
#             transaction_obj.paid_amount = actual_payment

#         if hasattr(transaction_obj, "due_amount"):
#             transaction_obj.due_amount = max(Decimal("0"), current_due - actual_payment)

#         transaction_obj.save()

#         new_due_amount = current_due - actual_payment

#         if new_due_amount <= 0:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="paid",
#                 due_amount=0
#             )
#         else:
#             Installment.objects.filter(pk=instance.pk).update(
#                 installment_status="due",
#                 due_amount=new_due_amount
#             )

#         # extra saving হলে customer account update হবে
#         if extra_amount > 0:
#             update_customer_balance(instance.customer_name, extra_amount)

#             extra_modelname = f"Extra Payment Savings : {instance.id}"

#             extra_tx = Transection.objects.filter(
#                 customer_name=instance.customer_name,
#                 modelname=extra_modelname
#             ).first()

#             if extra_tx:
#                 extra_tx.transection_type = "cashin"
#                 extra_tx.amount = extra_amount
#                 extra_tx.customer_name = instance.customer_name
#                 extra_tx.received_by = instance.received_by
#                 extra_tx.modelname = extra_modelname
#                 extra_tx.save()
#             else:
#                 extra_tx = create_transaction_with_customer_info(
#                     instance.customer_name,
#                     transection_type="cashin",
#                     amount=extra_amount,
#                     customer_name=instance.customer_name,
#                     received_by=instance.received_by,
#                     modelname=extra_modelname
#                 )

#             mark_transaction_as_paid(extra_tx, extra_amount)




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

#             #  attach installments to loan
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

#     #  Increase stock
#     variation.quantity += qty
#     variation.save(update_fields=["quantity"])

#     #  Attach unickkeys if variation is unique
#     if variation.isunck:
#         variation.unickkey.add(*instance.unickkey.all())







# from django.db.models.signals import m2m_changed
# from django.dispatch import receiver
# from django.db import transaction

# @receiver(m2m_changed, sender=Purchase.purchaseitem.through)
# def purchase_items_added(sender, instance, action, pk_set, **kwargs):
#     """
#     When Purchase.purchaseitem is changed (items added),
#     update stock and attach unick keys to Variation for isunck=True variations.
#     """

#     # ✅ only after items are added
#     if action != "post_add":
#         return

#     # pk_set = which PurchaseItem IDs were newly added
#     if not pk_set:
#         return

#     # ✅ Fetch only newly added items
#     items = PurchaseItem.objects.select_related("purchase_product_variation").filter(pk__in=pk_set)

#     # ✅ transaction safety (optional but good)
#     with transaction.atomic():
#         for item in items:
#             variation = item.purchase_product_variation
#             if not variation:
#                 continue

#             # ✅ Increase stock
#             variation.quantity += item.qty
#             variation.save(update_fields=["quantity"])

#             # ✅ Attach unick keys if variation.isunck
#             if getattr(variation, "isunck", False):
#                 keys = item.unickkey.all()
#                 if keys.exists():
#                     variation.unickkey.add(*keys)






# from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
# from django.dispatch import receiver
# from django.db import transaction


# # ─── helpers ──────────────────────────────────────────────────────────────────

# def _get_old_instance(instance):
#     """Return the DB-saved version of instance, or None if it's new."""
#     if not instance.pk:
#         return None
#     try:
#         return instance.__class__.objects.get(pk=instance.pk)
#     except instance.__class__.DoesNotExist:
#         return None


# def _current_unick_ids(purchase_item_instance):
#     """IDs of unickkeys already attached to this PurchaseItem in the DB."""
#     if not purchase_item_instance.pk:
#         return set()
#     return set(
#         purchase_item_instance.unickkey.values_list("id", flat=True)
#     )


# # ─── PurchaseItem: stash old state before save ────────────────────────────────

# @receiver(pre_save, sender=PurchaseItem)
# def purchaseitem_pre_save(sender, instance, **kwargs):
#     """
#     Before saving, snapshot the old qty and soft-delete flag so
#     post_save can compute the diff.
#     """
#     old = _get_old_instance(instance)

#     if old is None:
#         # Brand-new item — no prior state
#         instance._old_qty = 0
#         instance._old_is_deleted = False
#         instance._is_new = True
#     else:
#         instance._old_qty = old.qty
#         instance._old_is_deleted = bool(getattr(old, "is_deleted", False))
#         instance._is_new = False


# # ─── PurchaseItem: update variation stock after save ─────────────────────────

# @receiver(post_save, sender=PurchaseItem)
# def purchaseitem_post_save(sender, instance, created, **kwargs):
#     """
#     After a PurchaseItem is saved (create OR update), keep Variation.quantity
#     in sync by applying only the *delta*.

#     Cases handled:
#       • New item (created=True)        → add full qty to variation
#       • Qty changed                    → add/subtract the diff
#       • Soft-deleted (is_deleted=True) → reverse the item's full qty
#       • Un-soft-deleted                → re-apply the qty
#     """
#     variation = instance.purchase_product_variation
#     if not variation:
#         return

#     is_now_deleted = bool(getattr(instance, "is_deleted", False))
#     old_is_deleted = getattr(instance, "_old_is_deleted", False)
#     old_qty = getattr(instance, "_old_qty", 0)
#     new_qty = instance.qty

#     with transaction.atomic():
#         # Re-fetch variation inside the transaction to get a fresh lock
#         from django.db.models import F
#         variation.__class__.objects.filter(pk=variation.pk).update(
#             quantity=_compute_new_qty(
#                 variation.__class__.objects.get(pk=variation.pk).quantity,
#                 old_qty=old_qty,
#                 new_qty=new_qty,
#                 was_deleted=old_is_deleted,
#                 is_deleted=is_now_deleted,
#                 is_new=getattr(instance, "_is_new", False),
#             )
#         )


# def _compute_new_qty(current_stock, old_qty, new_qty, was_deleted, is_deleted, is_new):
#     """
#     Pure function — easier to unit-test separately.

#     is_new          → stock += new_qty
#     just deleted    → stock -= old_qty  (reverse contribution)
#     just undeleted  → stock += new_qty  (re-apply contribution)
#     qty changed     → stock += (new_qty - old_qty)
#     """
#     if is_new:
#         return current_stock + new_qty

#     if is_deleted and not was_deleted:
#         # Item just got soft-deleted → reverse old qty
#         return current_stock - old_qty

#     if not is_deleted and was_deleted:
#         # Item just got un-soft-deleted → apply new qty
#         return current_stock + new_qty

#     if is_deleted and was_deleted:
#         # Already deleted, saved again — no change
#         return current_stock

#     # Normal update: apply only the diff
#     return current_stock + (new_qty - old_qty)


# # ─── PurchaseItem: handle hard delete ────────────────────────────────────────

# @receiver(post_delete, sender=PurchaseItem)
# def purchaseitem_post_delete(sender, instance, **kwargs):
#     """
#     If a PurchaseItem is hard-deleted, reverse its qty contribution
#     and remove its unick keys from the variation.
#     """
#     variation = instance.purchase_product_variation
#     if not variation:
#         return

#     with transaction.atomic():
#         variation.__class__.objects.filter(pk=variation.pk).update(
#             quantity=variation.__class__.objects.get(pk=variation.pk).quantity - instance.qty
#         )

#         if getattr(variation, "isunck", False):
#             keys = instance.unickkey.all()
#             if keys.exists():
#                 variation.unickkey.remove(*keys)


# # ─── PurchaseItem.unickkey M2M: sync keys onto Variation ─────────────────────

# @receiver(m2m_changed, sender=PurchaseItem.unickkey.through)
# def purchaseitem_unickkey_changed(sender, instance, action, pk_set, **kwargs):
#     """
#     When unick keys are added/removed on a PurchaseItem,
#     mirror that change onto the related Variation (if isunck=True).
#     """
#     variation = instance.purchase_product_variation
#     if not variation or not getattr(variation, "isunck", False):
#         return

#     if not pk_set:
#         return

#     with transaction.atomic():
#         if action == "post_add":
#             variation.unickkey.add(*pk_set)

#         elif action == "post_remove":
#             variation.unickkey.remove(*pk_set)

#         elif action == "post_clear":
#             # All keys cleared from this purchase item
#             # Only remove keys that no OTHER PurchaseItem also holds for this variation
#             other_key_ids = set(
#                 PurchaseItem.objects.filter(
#                     purchase_product_variation=variation
#                 ).exclude(
#                     pk=instance.pk
#                 ).values_list("unickkey__id", flat=True)
#             )
#             # Remove only keys not referenced by other items
#             keys_to_remove = set(
#                 variation.unickkey.values_list("id", flat=True)
#             ) - other_key_ids

#             if keys_to_remove:
#                 variation.unickkey.remove(*keys_to_remove)


# # ─── Purchase.purchaseitem M2M: handle bulk attach/detach ─────────────────────
# # (Keep your existing signal but guard against double-counting —
# #  PurchaseItem post_save already ran when the item was created/saved.
# #  This signal is now only useful when an *existing* item is linked to
# #  a *different* Purchase, which is rare. You can keep it or remove it.)

# @receiver(m2m_changed, sender=Purchase.purchaseitem.through)
# def purchase_items_added(sender, instance, action, pk_set, **kwargs):
#     """
#     Only act when an already-existing PurchaseItem is attached to a Purchase
#     for the first time (edge case). Skip brand-new items — post_save handles them.
#     """
#     if action != "post_add" or not pk_set:
#         return

#     # Only process items that were already in DB before this M2M link
#     # (i.e. not just created in the same request)
#     items = PurchaseItem.objects.select_related(
#         "purchase_product_variation"
#     ).filter(pk__in=pk_set)

#     with transaction.atomic():
#         for item in items:
#             variation = item.purchase_product_variation
#             if not variation:
#                 continue

#             # Check if this variation's stock was already updated by post_save
#             # by checking if the item was JUST created (no purchase linked yet)
#             already_counted = not Purchase.objects.filter(
#                 purchaseitem=item
#             ).exclude(pk=instance.pk).exists()

#             if already_counted:
#                 # post_save already ran — skip to avoid double-counting
#                 continue

#             variation.quantity += item.qty
#             variation.save(update_fields=["quantity"])

#             if getattr(variation, "isunck", False):
#                 keys = item.unickkey.all()
#                 if keys.exists():
#                     variation.unickkey.add(*keys)









# signals.py
# from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
# from django.dispatch import receiver
# from django.db import transaction


# # ════════════════════════════════════════════════════════
# # HELPER
# # ════════════════════════════════════════════════════════

# def _get_old(instance):
#     if not instance.pk:
#         return None
#     try:
#         return instance.__class__.objects.get(pk=instance.pk)
#     except instance.__class__.DoesNotExist:
#         return None


# def _compute_stock(current, old_qty, new_qty, was_deleted, is_deleted, is_new):
#     if is_new:
#         return current + new_qty
#     if is_deleted and not was_deleted:
#         return current - old_qty          # এইমাত্র soft-delete হয়েছে
#     if not is_deleted and was_deleted:
#         return current + new_qty          # restore হয়েছে
#     if is_deleted and was_deleted:
#         return current                    # already deleted, no change
#     return current + (new_qty - old_qty)  # normal qty change — delta only


# # ════════════════════════════════════════════════════════
# # SIGNAL 1 — PurchaseItem pre_save
# # পুরনো state snapshot
# # ════════════════════════════════════════════════════════

# @receiver(pre_save, sender=PurchaseItem)
# def purchaseitem_pre_save(sender, instance, **kwargs):
#     old = _get_old(instance)
#     if old is None:
#         instance._old_qty        = 0
#         instance._old_is_deleted = False
#         instance._is_new         = True
#         # ✅ NEW: পুরনো unick key ids snapshot করো
#         instance._old_unick_ids  = set()
#     else:
#         instance._old_qty        = old.qty
#         instance._old_is_deleted = bool(getattr(old, 'is_deleted', False))
#         instance._is_new         = False
#         # ✅ NEW: existing item এর current unick keys snapshot
#         instance._old_unick_ids  = set(old.unickkey.values_list('id', flat=True))


# # ════════════════════════════════════════════════════════
# # SIGNAL 2 — PurchaseItem post_save
# # qty delta apply করো variation-এ
# # ════════════════════════════════════════════════════════

# @receiver(post_save, sender=PurchaseItem)
# def purchaseitem_post_save(sender, instance, created, **kwargs):
#     variation = instance.purchase_product_variation
#     if not variation:
#         return

#     is_now_deleted = bool(getattr(instance, 'is_deleted', False))
#     old_is_deleted = getattr(instance, '_old_is_deleted', False)
#     old_qty        = getattr(instance, '_old_qty', 0)

#     with transaction.atomic():
#         fresh = variation.__class__.objects.select_for_update().get(pk=variation.pk)
#         new_stock = _compute_stock(
#             current    = fresh.quantity,
#             old_qty    = old_qty,
#             new_qty    = instance.qty,
#             was_deleted= old_is_deleted,
#             is_deleted = is_now_deleted,
#             is_new     = getattr(instance, '_is_new', False),
#         )
#         variation.__class__.objects.filter(pk=variation.pk).update(quantity=new_stock)

#     # ✅ NEW: unick key sync — post_save এর পরে M2M টা already set হয়েছে
#     # তাই এখানে sync করা নিরাপদ
#     # কিন্তু M2M signal আলাদাভাবে handle করা ভালো (Signal 4 দেখো)


# # ════════════════════════════════════════════════════════
# # SIGNAL 3 — PurchaseItem post_delete
# # hard delete হলে stock reverse করো
# # ════════════════════════════════════════════════════════

# @receiver(post_delete, sender=PurchaseItem)
# def purchaseitem_post_delete(sender, instance, **kwargs):
#     variation = instance.purchase_product_variation
#     if not variation:
#         return

#     with transaction.atomic():
#         fresh = variation.__class__.objects.select_for_update().get(pk=variation.pk)
#         variation.__class__.objects.filter(pk=variation.pk).update(
#             quantity=max(0, fresh.quantity - instance.qty)
#         )

#         # ✅ variation থেকে এই item এর unick keys সরাও
#         if getattr(variation, 'isunck', False):
#             keys = list(instance.unickkey.all())
#             if keys:
#                 # অন্য purchase item ব্যবহার করছে না এমন keys সরাও
#                 _safe_remove_unick_keys(variation, instance.pk, keys)


# # ════════════════════════════════════════════════════════
# # SIGNAL 4 — PurchaseItem.unickkey M2M changed
# # ✅ KEY FIX: add/remove/clear সব handle করো
# # ════════════════════════════════════════════════════════

# @receiver(m2m_changed, sender=PurchaseItem.unickkey.through)
# def purchaseitem_unickkey_changed(sender, instance, action, pk_set, **kwargs):
#     """
#     PurchaseItem.unickkey change হলে Variation.unickkey-তেও mirror করো।
    
#     ✅ IMPORTANT: Django M2M .set() করলে এই sequence হয়:
#         1. post_remove (পুরনো keys)
#         2. post_add (নতুন keys)
#     তাই আমরা শুধু post_add এবং post_remove handle করলেই হবে।
#     """
#     variation = instance.purchase_product_variation
#     if not variation or not getattr(variation, 'isunck', False):
#         return

#     if not pk_set and action not in ('post_clear',):
#         return

#     with transaction.atomic():
#         variation_obj = variation.__class__.objects.select_for_update().get(pk=variation.pk)

#         if action == 'post_add':
#             # ✅ নতুন keys variation-এ add করো
#             variation_obj.unickkey.add(*pk_set)

#         elif action == 'post_remove':
#             # ✅ শুধু সেই keys সরাও যেগুলো অন্য কোনো active PurchaseItem ব্যবহার করছে না
#             _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, pk_set)

#         elif action == 'post_clear':
#             # ✅ এই item এর সব keys সরাও (safe way)
#             all_item_key_ids = set(instance.unickkey.values_list('id', flat=True))
#             if all_item_key_ids:
#                 _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, all_item_key_ids)


# def _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids_to_remove):
#     """
#     variation থেকে key_ids_to_remove গুলো সরাও,
#     কিন্তু যেগুলো অন্য active PurchaseItem-এও আছে সেগুলো রাখো।
#     """
#     if not key_ids_to_remove:
#         return

#     # অন্য active items যে keys ব্যবহার করছে
#     other_key_ids = set(
#         PurchaseItem.objects.filter(
#             purchase_product_variation=variation,
#             is_deleted=False,
#         ).exclude(
#             pk=exclude_item_pk
#         ).values_list('unickkey__id', flat=True)
#     )

#     # safely removable = remove করতে চাই - অন্যরা ব্যবহার করছে না এমন
#     safely_removable = set(key_ids_to_remove) - other_key_ids

#     if safely_removable:
#         variation.unickkey.remove(*safely_removable)


# def _safe_remove_unick_keys(variation, exclude_item_pk, keys):
#     key_ids = {k.id for k in keys}
#     _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids)


# # ════════════════════════════════════════════════════════
# # SIGNAL 5 — Purchase.purchaseitem M2M changed
# # ✅ Double-count guard সহ
# # ════════════════════════════════════════════════════════

# @receiver(m2m_changed, sender=Purchase.purchaseitem.through)
# def purchase_purchaseitem_m2m_changed(sender, instance, action, pk_set, **kwargs):
#     """
#     Purchase.purchaseitem M2M-এ নতুন item link হলে।
#     post_save (Signal 2) already qty update করেছে নতুন item-এর জন্য।
#     এখানে শুধু existing item যা নতুন purchase-এ link হচ্ছে সেটা handle করো।
#     """
#     if action != 'post_add' or not pk_set:
#         return

#     items = PurchaseItem.objects.select_related(
#         'purchase_product_variation'
#     ).filter(pk__in=pk_set, is_deleted=False)

#     with transaction.atomic():
#         for item in items:
#             variation = item.purchase_product_variation
#             if not variation:
#                 continue

#             # ✅ Double-count guard:
#             # এই item কি অন্য কোনো Purchase-এও আছে?
#             # যদি থাকে তাহলে post_save already count করেছে
#             other_purchase_count = Purchase.objects.filter(
#                 purchaseitem=item
#             ).exclude(pk=instance.pk).count()

#             if other_purchase_count > 0:
#                 continue  # already counted, skip

#             # Fresh link — stock update
#             fresh = variation.__class__.objects.select_for_update().get(pk=variation.pk)
#             variation.__class__.objects.filter(pk=variation.pk).update(
#                 quantity=fresh.quantity + item.qty
#             )

#             # unick keys sync
#             if getattr(variation, 'isunck', False):
#                 keys = list(item.unickkey.all())
#                 if keys:
#                     variation.unickkey.add(*keys)





# from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
# from django.dispatch import receiver
# from django.db import transaction


# # ════════════════════════════════════════════════════════
# # HELPERS
# # ════════════════════════════════════════════════════════

# def _get_old(instance):
#     if not instance.pk:
#         return None
#     try:
#         return instance.__class__.objects.get(pk=instance.pk)
#     except instance.__class__.DoesNotExist:
#         return None


# def _safe_bool(value):
#     if isinstance(value, bool):
#         return value
#     if isinstance(value, int):
#         return value == 1
#     if isinstance(value, str):
#         return value.strip().lower() in ("true", "1", "yes")
#     return False


# def _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids_to_remove):
#     """
#     variation থেকে key_ids_to_remove remove করবে,
#     কিন্তু যেগুলো অন্য active PurchaseItem-এ এখনও use হচ্ছে সেগুলো remove করবে না।
#     """
#     if not variation or not key_ids_to_remove:
#         return

#     other_key_ids = set(
#         PurchaseItem.objects.filter(
#             purchase_product_variation=variation,
#             is_deleted=False,
#         ).exclude(
#             pk=exclude_item_pk
#         ).values_list("unickkey__id", flat=True)
#     )

#     safely_removable = set(key_ids_to_remove) - other_key_ids
#     safely_removable.discard(None)

#     if safely_removable:
#         variation.unickkey.remove(*safely_removable)


# def _safe_remove_unick_keys(variation, exclude_item_pk, keys):
#     key_ids = {k.id for k in keys if getattr(k, "id", None)}
#     _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids)


# def _apply_stock_delta(variation_model, variation_id, delta):
#     """
#     variation.quantity += delta
#     negative হলে 0 এর নিচে নামতে দেবে না
#     """
#     if not variation_id or delta == 0:
#         return

#     with transaction.atomic():
#         fresh = variation_model.objects.select_for_update().get(pk=variation_id)
#         new_qty = (fresh.quantity or 0) + delta
#         if new_qty < 0:
#             new_qty = 0
#         variation_model.objects.filter(pk=variation_id).update(quantity=new_qty)


# # ════════════════════════════════════════════════════════
# # SIGNAL 1 — PurchaseItem pre_save
# # পুরনো state snapshot
# # ════════════════════════════════════════════════════════

# @receiver(pre_save, sender=PurchaseItem)
# def purchaseitem_pre_save(sender, instance, **kwargs):
#     old = _get_old(instance)

#     if old is None:
#         instance._is_new = True
#         instance._old_qty = 0
#         instance._old_is_deleted = False
#         instance._old_variation_id = None
#         instance._old_unick_ids = set()
#     else:
#         instance._is_new = False
#         instance._old_qty = old.qty or 0
#         instance._old_is_deleted = bool(getattr(old, "is_deleted", False))
#         instance._old_variation_id = getattr(old, "purchase_product_variation_id", None)
#         instance._old_unick_ids = set(old.unickkey.values_list("id", flat=True))


# # ════════════════════════════════════════════════════════
# # SIGNAL 2 — PurchaseItem post_save
# # qty / variation move / soft delete / restore সব handle
# # ════════════════════════════════════════════════════════

# @receiver(post_save, sender=PurchaseItem)
# def purchaseitem_post_save(sender, instance, created, **kwargs):
#     new_variation = instance.purchase_product_variation
#     new_variation_id = getattr(instance, "purchase_product_variation_id", None)

#     old_variation_id = getattr(instance, "_old_variation_id", None)
#     old_qty = getattr(instance, "_old_qty", 0)
#     old_is_deleted = getattr(instance, "_old_is_deleted", False)
#     is_new = getattr(instance, "_is_new", False)

#     new_qty = instance.qty or 0
#     new_is_deleted = bool(getattr(instance, "is_deleted", False))

#     variation_model = None
#     if new_variation is not None:
#         variation_model = new_variation.__class__
#     elif old_variation_id:
#         variation_model = Variation

#     if variation_model is None:
#         return

#     # ─── STOCK SYNC ─────────────────────────────────────
#     if is_new:
#         # new item create
#         if new_variation_id and not new_is_deleted:
#             _apply_stock_delta(variation_model, new_variation_id, new_qty)

#     else:
#         # variation changed
#         if old_variation_id != new_variation_id:
#             # old variation থেকে reverse
#             if old_variation_id and not old_is_deleted:
#                 _apply_stock_delta(variation_model, old_variation_id, -old_qty)

#             # new variation এ apply
#             if new_variation_id and not new_is_deleted:
#                 _apply_stock_delta(variation_model, new_variation_id, new_qty)

#         else:
#             # same variation, normal delta logic
#             if new_variation_id:
#                 if not old_is_deleted and not new_is_deleted:
#                     # normal qty change
#                     _apply_stock_delta(variation_model, new_variation_id, new_qty - old_qty)

#                 elif not old_is_deleted and new_is_deleted:
#                     # soft delete
#                     _apply_stock_delta(variation_model, new_variation_id, -old_qty)

#                 elif old_is_deleted and not new_is_deleted:
#                     # restore
#                     _apply_stock_delta(variation_model, new_variation_id, new_qty)

#                 # old deleted -> new deleted হলে no-op

#     # ─── UNIQUE KEY SYNC ────────────────────────────────
#     # variation change হলে old variation থেকে old keys safe remove করতে হবে
#     # এবং new variation এ current keys add করতে হবে
#     def _sync_variation_keys_after_commit():
#         current_key_ids = set(instance.unickkey.values_list("id", flat=True))
#         old_key_ids = set(getattr(instance, "_old_unick_ids", set()) or set())

#         # old variation cleanup
#         if old_variation_id and old_variation_id != new_variation_id:
#             try:
#                 old_variation = Variation.objects.get(pk=old_variation_id)
#                 if getattr(old_variation, "isunck", False) and old_key_ids:
#                     _safe_remove_unick_keys_by_ids(old_variation, instance.pk, old_key_ids)
#             except Variation.DoesNotExist:
#                 pass

#         # new variation add
#         if new_variation_id and not new_is_deleted:
#             try:
#                 current_variation = Variation.objects.get(pk=new_variation_id)
#                 if getattr(current_variation, "isunck", False) and current_key_ids:
#                     current_variation.unickkey.add(*current_key_ids)
#             except Variation.DoesNotExist:
#                 pass

#     transaction.on_commit(_sync_variation_keys_after_commit)


# # ════════════════════════════════════════════════════════
# # SIGNAL 3 — PurchaseItem post_delete
# # hard delete হলে stock reverse
# # ════════════════════════════════════════════════════════

# @receiver(post_delete, sender=PurchaseItem)
# def purchaseitem_post_delete(sender, instance, **kwargs):
#     variation = instance.purchase_product_variation
#     if not variation:
#         return

#     # already soft-deleted item hard delete হলে আবার minus করা যাবে না
#     if bool(getattr(instance, "is_deleted", False)):
#         return

#     with transaction.atomic():
#         fresh = variation.__class__.objects.select_for_update().get(pk=variation.pk)
#         new_qty = (fresh.quantity or 0) - (instance.qty or 0)
#         if new_qty < 0:
#             new_qty = 0
#         variation.__class__.objects.filter(pk=variation.pk).update(quantity=new_qty)

#     if getattr(variation, "isunck", False):
#         keys = list(instance.unickkey.all())
#         if keys:
#             _safe_remove_unick_keys(variation, instance.pk, keys)


# # ════════════════════════════════════════════════════════
# # SIGNAL 4 — PurchaseItem.unickkey M2M changed
# # add/remove/clear সব handle
# # ════════════════════════════════════════════════════════

# @receiver(m2m_changed, sender=PurchaseItem.unickkey.through)
# def purchaseitem_unickkey_changed(sender, instance, action, pk_set, **kwargs):
#     variation = instance.purchase_product_variation
#     if not variation or not getattr(variation, "isunck", False):
#         return

#     if not pk_set and action not in ("post_clear",):
#         return

#     with transaction.atomic():
#         variation_obj = variation.__class__.objects.select_for_update().get(pk=variation.pk)

#         if action == "post_add":
#             variation_obj.unickkey.add(*pk_set)

#         elif action == "post_remove":
#             _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, pk_set)

#         elif action == "post_clear":
#             old_key_ids = set(getattr(instance, "_old_unick_ids", set()) or set())
#             if old_key_ids:
#                 _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, old_key_ids)


# # ════════════════════════════════════════════════════════
# # SIGNAL 5 — Purchase.purchaseitem M2M changed
# # IMPORTANT: stock update করবে না
# # কারণ PurchaseItem post_save already stock handle করে
# # ════════════════════════════════════════════════════════

# @receiver(m2m_changed, sender=Purchase.purchaseitem.through)
# def purchase_purchaseitem_m2m_changed(sender, instance, action, pk_set, **kwargs):
#     """
#     এখানে stock touch করা যাবে না।
#     কারণ PurchaseItem create/update signal already quantity sync করে।

#     এই signal রাখার একটাই কারণ:
#     future এ link/unlink logging বা validation লাগলে use করা যাবে।
#     """
#     return




from django.db.models.signals import pre_save, post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.db import transaction

from .models import Purchase, PurchaseItem, Variation


def _get_old(instance):
    if not instance.pk:
        return None
    try:
        return instance.__class__.objects.get(pk=instance.pk)
    except instance.__class__.DoesNotExist:
        return None


def _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids_to_remove):
    if not variation or not key_ids_to_remove:
        return

    other_key_ids = set(
        PurchaseItem.objects.filter(
            purchase_product_variation=variation,
            is_deleted=False,
        ).exclude(
            pk=exclude_item_pk
        ).values_list("unickkey__id", flat=True)
    )

    safely_removable = set(key_ids_to_remove) - other_key_ids
    safely_removable.discard(None)

    if safely_removable:
        variation.unickkey.remove(*safely_removable)


def _safe_remove_unick_keys(variation, exclude_item_pk, keys):
    key_ids = {k.id for k in keys if getattr(k, "id", None)}
    _safe_remove_unick_keys_by_ids(variation, exclude_item_pk, key_ids)


def _apply_stock_delta(variation_model, variation_id, delta):
    if not variation_id or delta == 0:
        return

    with transaction.atomic():
        fresh = variation_model.objects.select_for_update().get(pk=variation_id)
        new_qty = (fresh.quantity or 0) + delta
        if new_qty < 0:
            new_qty = 0
        variation_model.objects.filter(pk=variation_id).update(quantity=new_qty)


@receiver(pre_save, sender=PurchaseItem)
def purchaseitem_pre_save(sender, instance, **kwargs):
    old = _get_old(instance)

    if old is None:
        instance._is_new = True
        instance._old_qty = 0
        instance._old_is_deleted = False
        instance._old_variation_id = None
        instance._old_unick_ids = set()
    else:
        instance._is_new = False
        instance._old_qty = old.qty or 0
        instance._old_is_deleted = bool(getattr(old, "is_deleted", False))
        instance._old_variation_id = getattr(old, "purchase_product_variation_id", None)
        instance._old_unick_ids = set(old.unickkey.values_list("id", flat=True))


# @receiver(post_save, sender=PurchaseItem)
# def purchaseitem_post_save(sender, instance, created, **kwargs):
#     new_variation = instance.purchase_product_variation
#     new_variation_id = getattr(instance, "purchase_product_variation_id", None)

#     old_variation_id = getattr(instance, "_old_variation_id", None)
#     old_qty = getattr(instance, "_old_qty", 0)
#     old_is_deleted = getattr(instance, "_old_is_deleted", False)
#     is_new = getattr(instance, "_is_new", False)

#     new_qty = instance.qty or 0
#     new_is_deleted = bool(getattr(instance, "is_deleted", False))

#     variation_model = None
#     if new_variation is not None:
#         variation_model = new_variation.__class__
#     elif old_variation_id:
#         variation_model = Variation

#     if variation_model is not None:
#         if is_new:
#             if new_variation_id and not new_is_deleted:
#                 _apply_stock_delta(variation_model, new_variation_id, new_qty)
#         else:
#             if old_variation_id != new_variation_id:
#                 if old_variation_id and not old_is_deleted:
#                     _apply_stock_delta(variation_model, old_variation_id, -old_qty)

#                 if new_variation_id and not new_is_deleted:
#                     _apply_stock_delta(variation_model, new_variation_id, new_qty)
#             else:
#                 if new_variation_id:
#                     if not old_is_deleted and not new_is_deleted:
#                         _apply_stock_delta(variation_model, new_variation_id, new_qty - old_qty)
#                     elif not old_is_deleted and new_is_deleted:
#                         _apply_stock_delta(variation_model, new_variation_id, -old_qty)
#                     elif old_is_deleted and not new_is_deleted:
#                         _apply_stock_delta(variation_model, new_variation_id, new_qty)

#     def _sync_after_commit():
#         current_key_ids = set(instance.unickkey.values_list("id", flat=True))
#         old_key_ids = set(getattr(instance, "_old_unick_ids", set()) or set())

#         if old_variation_id and old_variation_id != new_variation_id:
#             try:
#                 old_variation = Variation.objects.get(pk=old_variation_id)
#                 if getattr(old_variation, "isunck", False) and old_key_ids:
#                     _safe_remove_unick_keys_by_ids(old_variation, instance.pk, old_key_ids)
#             except Variation.DoesNotExist:
#                 pass

#         if new_variation_id and not new_is_deleted:
#             try:
#                 current_variation = Variation.objects.get(pk=new_variation_id)
#                 if getattr(current_variation, "isunck", False) and current_key_ids:
#                     current_variation.unickkey.add(*current_key_ids)
#             except Variation.DoesNotExist:
#                 pass

#         # soft delete হলে সব parent Purchase থেকে unlink
#         if not old_is_deleted and new_is_deleted:
#             for purchase in Purchase.objects.filter(purchaseitem=instance):
#                 purchase.purchaseitem.remove(instance)

#     transaction.on_commit(_sync_after_commit)


@receiver(post_save, sender=PurchaseItem)
def purchaseitem_post_save(sender, instance, created, **kwargs):
    new_variation = instance.purchase_product_variation
    new_variation_id = getattr(instance, "purchase_product_variation_id", None)

    old_variation_id = getattr(instance, "_old_variation_id", None)
    old_qty = getattr(instance, "_old_qty", 0)
    old_is_deleted = getattr(instance, "_old_is_deleted", False)
    is_new = getattr(instance, "_is_new", False)

    new_qty = instance.qty or 0
    new_is_deleted = bool(getattr(instance, "is_deleted", False))

    variation_model = None
    if new_variation is not None:
        variation_model = new_variation.__class__
    elif old_variation_id:
        variation_model = Variation

    # ─── QTY / STOCK SYNC ─────────────────────────────────────
    if variation_model is not None:
        if is_new:
            if new_variation_id and not new_is_deleted:
                _apply_stock_delta(variation_model, new_variation_id, new_qty)
        else:
            if old_variation_id != new_variation_id:
                if old_variation_id and not old_is_deleted:
                    _apply_stock_delta(variation_model, old_variation_id, -old_qty)

                if new_variation_id and not new_is_deleted:
                    _apply_stock_delta(variation_model, new_variation_id, new_qty)
            else:
                if new_variation_id:
                    if not old_is_deleted and not new_is_deleted:
                        _apply_stock_delta(variation_model, new_variation_id, new_qty - old_qty)
                    elif not old_is_deleted and new_is_deleted:
                        _apply_stock_delta(variation_model, new_variation_id, -old_qty)
                    elif old_is_deleted and not new_is_deleted:
                        _apply_stock_delta(variation_model, new_variation_id, new_qty)

    # ─── UNIQUE KEY + PARENT PURCHASE UNLINK SYNC ─────────────────────────
    def _sync_after_commit():
        current_key_ids = set(instance.unickkey.values_list("id", flat=True))
        old_key_ids = set(getattr(instance, "_old_unick_ids", set()) or set())

        # variation change হলে old variation থেকে old keys safe remove
        if old_variation_id and old_variation_id != new_variation_id:
            try:
                old_variation = Variation.objects.get(pk=old_variation_id)
                if getattr(old_variation, "isunck", False) and old_key_ids:
                    _safe_remove_unick_keys_by_ids(old_variation, instance.pk, old_key_ids)
            except Variation.DoesNotExist:
                pass

        # same variation + soft delete হলে old keys remove
        if old_variation_id and old_variation_id == new_variation_id and not old_is_deleted and new_is_deleted:
            try:
                same_variation = Variation.objects.get(pk=old_variation_id)
                if getattr(same_variation, "isunck", False) and old_key_ids:
                    _safe_remove_unick_keys_by_ids(same_variation, instance.pk, old_key_ids)
            except Variation.DoesNotExist:
                pass

        # restore / new / moved-to-new-variation হলে current keys add
        if new_variation_id and not new_is_deleted:
            try:
                current_variation = Variation.objects.get(pk=new_variation_id)
                if getattr(current_variation, "isunck", False) and current_key_ids:
                    current_variation.unickkey.add(*current_key_ids)
            except Variation.DoesNotExist:
                pass

        # soft delete হলে unlink + item-এর own keys clear
        if not old_is_deleted and new_is_deleted:
            for purchase in Purchase.objects.filter(purchaseitem=instance):
                purchase.purchaseitem.remove(instance)

            if old_key_ids:
                instance.unickkey.clear()

    transaction.on_commit(_sync_after_commit)

@receiver(post_delete, sender=PurchaseItem)
def purchaseitem_post_delete(sender, instance, **kwargs):
    variation = instance.purchase_product_variation
    if not variation:
        return

    if bool(getattr(instance, "is_deleted", False)):
        return

    with transaction.atomic():
        fresh = variation.__class__.objects.select_for_update().get(pk=variation.pk)
        new_qty = (fresh.quantity or 0) - (instance.qty or 0)
        if new_qty < 0:
            new_qty = 0
        variation.__class__.objects.filter(pk=variation.pk).update(quantity=new_qty)

    if getattr(variation, "isunck", False):
        keys = list(instance.unickkey.all())
        if keys:
            _safe_remove_unick_keys(variation, instance.pk, keys)


@receiver(m2m_changed, sender=PurchaseItem.unickkey.through)
def purchaseitem_unickkey_changed(sender, instance, action, pk_set, **kwargs):
    variation = instance.purchase_product_variation
    if not variation or not getattr(variation, "isunck", False):
        return

    if bool(getattr(instance, "is_deleted", False)):
        return

    if action == "pre_clear":
        instance._preclear_unick_ids = set(instance.unickkey.values_list("id", flat=True))
        return

    if not pk_set and action not in ("post_clear",):
        return

    with transaction.atomic():
        variation_obj = variation.__class__.objects.select_for_update().get(pk=variation.pk)

        if action == "post_add":
            variation_obj.unickkey.add(*pk_set)

        elif action == "post_remove":
            _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, pk_set)

        elif action == "post_clear":
            old_key_ids = set(getattr(instance, "_preclear_unick_ids", set()) or set())
            if old_key_ids:
                _safe_remove_unick_keys_by_ids(variation_obj, instance.pk, old_key_ids)


@receiver(m2m_changed, sender=Purchase.purchaseitem.through)
def purchase_purchaseitem_m2m_changed(sender, instance, action, pk_set, **kwargs):
    return