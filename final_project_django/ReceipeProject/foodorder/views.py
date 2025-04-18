from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from recipes.models import Recipe
from .models import Cart, DeliveryAddress, Order
from django.urls import reverse
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

@login_required
def add_to_cart(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, recipe=recipe)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"Added {recipe.title} to your cart!")
    except Recipe.DoesNotExist:
        messages.error(request, "Recipe not found.")
    except Exception as e:
        messages.error(request, f"Error adding to cart: {str(e)}")
    return redirect(reverse('foodorder:cart'))

@login_required
def cart(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items)

        if request.method == "POST":
            item_id = request.POST.get('item_id')
            try:
                if 'increase' in request.POST:
                    cart_item = Cart.objects.get(id=item_id, user=request.user)
                    cart_item.quantity += 1
                    cart_item.save()
                elif 'decrease' in request.POST:
                    cart_item = Cart.objects.get(id=item_id, user=request.user)
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                    else:
                        cart_item.delete()
                elif 'delete' in request.POST:
                    Cart.objects.filter(id=item_id, user=request.user).delete()
                # Return updated total as HttpResponse
                updated_total = sum(item.get_total_price() for item in Cart.objects.filter(user=request.user))
                return HttpResponse(f"Success: Cart updated, new total is {updated_total}")
            except Cart.DoesNotExist:
                return HttpResponse("Error: Cart item not found.")
            except Exception as e:
                return HttpResponse(f"Error updating cart: {str(e)}")

        return render(request, 'foodorder/cart.html', {'cart_items': cart_items, 'total': total})
    except Exception as e:
        messages.error(request, f"Error loading cart: {str(e)}")
        return render(request, 'foodorder/cart.html', {'cart_items': [], 'total': 0})

@login_required
def checkout(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk=recipe_id)
        cart_item, created = Cart.objects.get_or_create(user=request.user, recipe=recipe, defaults={'quantity': 1})
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items) if cart_items.exists() else 0
        return render(request, 'foodorder/checkout.html', {'recipe': recipe, 'cart_items': cart_items, 'total': total})
    except Recipe.DoesNotExist:
        messages.error(request, "Recipe not found.")
    except Exception as e:
        messages.error(request, f"Error loading checkout: {str(e)}")
    return redirect(reverse('foodorder:cart'))

@login_required
def delivery_address(request):
    try:
        existing_addresses = DeliveryAddress.objects.filter(user=request.user).order_by('-created_at')
        if request.method == "POST":
            action = request.POST.get('action')
            if action == 'continue':
                selected_address_id = request.POST.get('address_id')
                if selected_address_id:
                    # Store address ID in session instead of creating orders
                    request.session['selected_address_id'] = selected_address_id
                    cart_items = Cart.objects.filter(user=request.user)
                    if not cart_items.exists():
                        messages.error(request, "Your cart is empty.")
                        return redirect(reverse('foodorder:cart'))
                    messages.success(request, "Address selected. Review your order.")
                    return redirect(reverse('foodorder:order_review'))
            elif action == 'add_new':
                address = DeliveryAddress(
                    user=request.user,
                    address_line1=request.POST['address_line1'],
                    address_line2=request.POST.get('address_line2', ''),
                    city=request.POST['city'],
                    state=request.POST['state'],
                    postal_code=request.POST['postal_code'],
                    country=request.POST['country']
                )
                address.save()
                messages.success(request, "New address added successfully.")
                return redirect(reverse('foodorder:delivery_address'))

        return render(request, 'foodorder/delivery_address.html', {'addresses': existing_addresses})
    except Exception as e:
        messages.error(request, f"Error processing delivery address: {str(e)}")
        return redirect(reverse('foodorder:cart'))

@login_required
def my_orders(request):
    try:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'foodorder/my_orders.html', {'orders': orders})
    except Exception as e:
        messages.error(request, f"Error loading orders: {str(e)}")
        return render(request, 'foodorder/my_orders.html', {'orders': []})

@login_required
def order_review(request):
    try:
        cart_items = Cart.objects.filter(user=request.user)
        total = sum(item.get_total_price() for item in cart_items)
        selected_address_id = request.session.get('selected_address_id')
        if not selected_address_id:
            messages.error(request, "No address selected.")
            return redirect(reverse('foodorder:delivery_address'))

        try:
            selected_address = DeliveryAddress.objects.get(id=selected_address_id, user=request.user)
        except DeliveryAddress.DoesNotExist:
            messages.error(request, "Selected address not found.")
            return redirect(reverse('foodorder:delivery_address'))

        if request.method == "POST":
            item_id = request.POST.get('item_id')
            try:
                if 'increase' in request.POST:
                    cart_item = Cart.objects.get(id=item_id, user=request.user)
                    cart_item.quantity += 1
                    cart_item.save()
                elif 'decrease' in request.POST:
                    cart_item = Cart.objects.get(id=item_id, user=request.user)
                    if cart_item.quantity > 1:
                        cart_item.quantity -= 1
                        cart_item.save()
                    else:
                        cart_item.delete()
                elif 'delete' in request.POST:
                    Cart.objects.filter(id=item_id, user=request.user).delete()
                # Return updated total as HttpResponse
                updated_total = sum(item.get_total_price() for item in Cart.objects.filter(user=request.user))
                return HttpResponse(f"Success: Cart updated, new total is {updated_total}")
            except Cart.DoesNotExist:
                return HttpResponse("Error: Cart item not found.")
            except Exception as e:
                return HttpResponse(f"Error updating cart: {str(e)}")

        return render(request, 'foodorder/order_review.html', {
            'cart_items': cart_items,
            'total': total,
            'selected_address': selected_address
        })
    except Exception as e:
        messages.error(request, f"Error loading order review: {str(e)}")
        return redirect(reverse('foodorder:cart'))

@login_required
def payment(request):
    try:
        selected_address_id = request.session.get('selected_address_id')
        if not selected_address_id:
            messages.error(request, "No address selected.")
            return redirect(reverse('foodorder:delivery_address'))

        try:
            selected_address = DeliveryAddress.objects.get(id=selected_address_id, user=request.user)
        except DeliveryAddress.DoesNotExist:
            messages.error(request, "Selected address not found.")
            return redirect(reverse('foodorder:delivery_address'))

        cart_items = Cart.objects.filter(user=request.user)
        if not cart_items.exists():
            messages.error(request, "Your cart is empty.")
            return redirect(reverse('foodorder:cart'))

        if request.method == "POST":
            # Create orders for all cart items
            for item in cart_items:
                order = Order.objects.create(
                    user=request.user,
                    recipe=item.recipe,
                    quantity=item.quantity,
                    total_price=item.get_total_price(),
                    delivery_address=selected_address,
                    payment_status=True,
                    delivery_status='PENDING'
                )
            # Clear cart and session
            cart_items.delete()
            if 'selected_address_id' in request.session:
                del request.session['selected_address_id']
            messages.success(request, "Order confirmed successfully! Thank you for your purchase.")
            return redirect(reverse('foodorder:thank_you'))

        # Display all cart items for review
        total = sum(item.get_total_price() for item in cart_items)
        return render(request, 'foodorder/payment.html', {
            'cart_items': cart_items,
            'total': total,
            'selected_address': selected_address
        })
    except Exception as e:
        messages.error(request, f"Error processing payment: {str(e)}")
        return redirect(reverse('foodorder:cart'))

@login_required
def thank_you(request):
    return render(request, 'foodorder/thank_you.html')