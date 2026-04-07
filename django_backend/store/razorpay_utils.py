import razorpay
import json
from decimal import Decimal

# Hardcode Razorpay credentials directly
RAZORPAY_KEY_ID = 'rzp_test_SZ7O4UsIzQBDVI'
RAZORPAY_KEY_SECRET = 'sDXhikw5YhF5eRz5Lvc92PhZ'

# print(f"DEBUG: Using hardcoded Razorpay credentials")
# print(f"DEBUG: RAZORPAY_KEY_ID = {RAZORPAY_KEY_ID}")
# print(f"DEBUG: RAZORPAY_KEY_SECRET = {'SET' if RAZORPAY_KEY_SECRET else 'NOT_SET'}")

try:
    client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))
    print("DEBUG: Razorpay client initialized successfully")
except Exception as e:
    print(f"DEBUG: Error initializing Razorpay client: {e}")
    raise

def create_order(amount, currency='INR', receipt=None, notes=None):
    """
    Create a Razorpay order
    
    Args:
        amount: Amount in rupees (will be converted to paise)
        currency: Currency code (default: INR)
        receipt: Optional receipt ID
        notes: Optional notes dictionary
    
    Returns:
        Razorpay order object
    """
    try:
        # Convert rupees to paise (Razorpay expects amount in paise)
        amount_paise = int(Decimal(str(amount)) * 100)
        
        order_data = {
            'amount': amount_paise,
            'currency': currency,
            'receipt': receipt,
            'notes': notes or {},
            'payment_capture': 1  # Auto-capture payment
        }
        
        order = client.order.create(data=order_data)
        return order
        
    except Exception as e:
        print(f"Error creating Razorpay order: {e}")
        return None

def verify_payment(payment_id, order_id):
    """
    Verify Razorpay payment
    
    Args:
        payment_id: Razorpay payment ID
        order_id: Razorpay order ID
    
    Returns:
        Boolean indicating if payment is verified
    """
    try:
        payment = client.payment.fetch(payment_id)
        
        # Check if payment is captured and matches the order
        if (
            payment['status'] == 'captured' and 
            payment['order_id'] == order_id
        ):
            return True
        
        return False
        
    except Exception as e:
        print(f"Error verifying Razorpay payment: {e}")
        return False

def get_payment_details(payment_id):
    """
    Get payment details from Razorpay
    
    Args:
        payment_id: Razorpay payment ID
    
    Returns:
        Payment details dictionary or None
    """
    try:
        payment = client.payment.fetch(payment_id)
        return payment
        
    except Exception as e:
        print(f"Error fetching Razorpay payment details: {e}")
        return None

def process_refund(payment_id, amount=None):
    """
    Process refund for a payment
    
    Args:
        payment_id: Razorpay payment ID to refund
        amount: Amount to refund in rupees (partial refund if less than original amount)
    
    Returns:
        Refund object or None
    """
    try:
        refund_data = {}
        if amount:
            # Convert rupees to paise
            refund_data['amount'] = int(Decimal(str(amount)) * 100)
        
        refund = client.payment.refund(payment_id, data=refund_data)
        return refund
        
    except Exception as e:
        print(f"Error processing Razorpay refund: {e}")
        return None
