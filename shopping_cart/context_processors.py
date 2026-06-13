from shopping_cart.cart import Cart


def cart_context(request):
    cart = Cart(request)
    return {"cart_item_count": len(cart)}
