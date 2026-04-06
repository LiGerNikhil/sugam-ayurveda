from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from .models import Product, Customer, Order, OrderItem
from decimal import Decimal
from .razorpay_utils import create_order, verify_payment, get_payment_details

class OrderItemForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={
        'class': 'w-20 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'min': '1'
    }))
    notes = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'rows': 3,
        'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent',
        'placeholder': 'Special instructions for this order'
    }))

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, available=True)
    
    # Get or create customer
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    # Get cart from session
    cart = request.session.get('cart', {})
    
    # Add to cart
    product_key = str(product_id)
    if product_key in cart:
        cart[product_key]['quantity'] += 1
    else:
        cart[product_key] = {
            'name': product.name,
            'price': str(product.price) if product.price else '0',
            'quantity': 1,
            'image': product.get_image_url()
        }
    
    request.session['cart'] = cart
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = sum(item['quantity'] for item in cart.values())
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart_count
        })
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = Decimal('0')
    
    for product_id, item in cart.items():
        quantity = item['quantity']
        price = Decimal(item['price'])
        subtotal = price * quantity
        total += subtotal
        
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'image': item.get('image', '/static/images/default-product.jpg')
        })
    
    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'item_count': sum(item['quantity'] for item in cart_items)
    })

@login_required
def update_cart(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        product_key = str(product_id)
        
        if product_key in cart:
            quantity = int(request.POST.get('quantity', 1))
            if quantity > 0:
                cart[product_key]['quantity'] = quantity
            else:
                del cart[product_key]
                messages.info(request, 'Item removed from cart')
        
        request.session['cart'] = cart
        messages.success(request, 'Cart updated!')
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_key = str(product_id)
    
    if product_key in cart:
        del cart[product_key]
        request.session['cart'] = cart
        messages.info(request, 'Item removed from cart')
    
    return redirect('view_cart')

@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Your cart is empty!')
        return redirect('view_cart')
    
    # Get customer
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        customer = Customer.objects.create(user=request.user)
    
    # Calculate total
    total = Decimal('0')
    cart_items = []
    
    for product_id, item in cart.items():
        quantity = item['quantity']
        price = Decimal(item['price'])
        subtotal = price * quantity
        total += subtotal
        
        cart_items.append({
            'id': product_id,
            'name': item['name'],
            'price': price,
            'quantity': quantity,
            'subtotal': subtotal,
            'image': item.get('image', '/static/images/default-product.jpg')
        })
    
    if request.method == 'POST':
        order_notes = request.POST.get('order_notes', '')
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            order_notes=order_notes,
            status='pending'
        )
        
        # Create order items
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
        
        # Clear cart
        request.session['cart'] = {}
        
        messages.success(request, f'Order #{order.id} placed successfully! We will contact you soon.')
        return redirect('order_confirmation', order_id=order.id)
    
    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'total': total,
        'customer': customer
    })

@login_required
def order_tracking(request, order_id):
    """Track order status"""
    try:
        order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
        return render(request, 'store/order_tracking.html', {'order': order})
    except Customer.DoesNotExist:
        return redirect('login')

@login_required
def order_confirmation(request, order_id):
    try:
        order = get_object_or_404(Order, id=order_id, customer=request.user.customer)
        order_items = OrderItem.objects.filter(order=order).select_related('product')
        
        return render(request, 'store/order_confirmation.html', {
            'order': order,
            'order_items': order_items
        })
    except Customer.DoesNotExist:
        return redirect('login')

@login_required
def order_history(request):
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        return redirect('user_dashboard')
    
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    return render(request, 'store/order_history.html', {
        'orders': orders
    })

@login_required
def payment_success(request):
    """Handle successful payment from Razorpay"""
    payment_id = request.GET.get('payment_id')
    order_id = request.GET.get('order_id')
    
    if not payment_id or not order_id:
        messages.error(request, 'Invalid payment details')
        return redirect('checkout')
    
    # Verify payment with Razorpay
    if verify_payment(payment_id, order_id):
        # Get payment details
        payment_details = get_payment_details(payment_id)
        
        # Create order in database
        try:
            customer = request.user.customer
        except Customer.DoesNotExist:
            customer = Customer.objects.create(user=request.user)
        
        # Get cart from session
        cart = request.session.get('cart', {})
        total = Decimal('0')
        cart_items = []
        
        for product_id, item in cart.items():
            quantity = item['quantity']
            price = Decimal(item['price'])
            subtotal = price * quantity
            total += subtotal
            
            cart_items.append({
                'id': product_id,
                'name': item['name'],
                'price': price,
                'quantity': quantity,
                'subtotal': subtotal
            })
        
        # Create order
        order = Order.objects.create(
            customer=customer,
            total_amount=total,
            payment_method='razorpay',
            payment_id=payment_id,
            razorpay_order_id=order_id,
            status='paid'
        )
        
        # Create order items
        for item in cart_items:
            product = Product.objects.get(id=item['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )
        
        # Clear cart
        request.session['cart'] = {}
        
        messages.success(request, 'Payment successful! Your order has been placed.')
        return render(request, 'store/payment_success.html', {
            'payment_id': payment_id,
            'order_id': order_id
        })
    else:
        messages.error(request, 'Payment verification failed. Please contact support.')
        return redirect('checkout')

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def create_razorpay_order(request):
    """API endpoint to create Razorpay order"""
    try:
        import json
        data = json.loads(request.body)
        
        amount = data.get('amount')
        currency = data.get('currency', 'INR')
        receipt = data.get('receipt')
        notes = data.get('notes', {})
        
        if not amount:
            return JsonResponse({'error': 'Amount is required'}, status=400)
        
        # Create Razorpay order
        order = create_order(amount, currency, receipt, notes)
        
        if order:
            return JsonResponse({
                'id': order['id'],
                'amount': order['amount'],
                'currency': order['currency'],
                'receipt': order['receipt']
            })
        else:
            return JsonResponse({'error': 'Failed to create order'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def cart_count(request):
    """API endpoint to get cart item count"""
    if request.user.is_authenticated:
        try:
            customer = request.user.customer
            # Get cart from session or database
            cart = request.session.get('cart', {})
            total_items = sum(int(item.get('quantity', 0)) for item in cart.values())
            return JsonResponse({'count': total_items})
        except Customer.DoesNotExist:
            return JsonResponse({'count': 0})
    else:
        return JsonResponse({'count': 0})
