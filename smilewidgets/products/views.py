from datetime import datetime

from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import get_object_or_404

from .models import (GiftCard, Product)


def get_product_price(request):
    params = request.GET
    if 'productCode' not in params and 'date' in params:
        return HttpResponseBadRequest(
            'You are getting close, but are missing the required query param "productCode". ex. productCode=sm_widget')
    if 'date' not in params and 'productCode' in params:
        return HttpResponseBadRequest(
            'You are getting close, but are missing the required query param "date". ex. date=sep%2010%202018')
    if 'productCode' and 'date' not in params:
        return HttpResponseBadRequest(
            'So close, but your are missing required query params "productCode" and "date".'
            ' ex. productCode=1&date=sep%2010%202018')
    else:
        query_product_code = params.get('productCode')
        query_date = params.get('date')
        gift_card_code = params.get('giftCardCode') or 'giftCardCode'

        try:
            date_format = datetime.strptime(query_date, '%b %d %Y').date()

        except ValueError:
            return HttpResponseBadRequest(
                'Oops!  That was not a valid date.  The format should be "sep 10 2018",  Try again...', status=400)

        product = get_object_or_404(Product, code=query_product_code)
        low_price = product.price.filter(date_start__lte=date_format, date_end__gte=date_format)\
            .order_by('price').first()

        res = {'Price': low_price.formatted_amount}

        if gift_card_code:
            gift_card = get_object_or_404(GiftCard, code=gift_card_code)
            is_valid = gift_card.date_start < date_format < gift_card.date_end

            if is_valid:
                gift_card_price = low_price.price - gift_card.amount or 0

                if gift_card_price < 0:
                    res['Price'] = 'Your gift card has ${0:.2f} remaining'.format(abs(gift_card_price) / 100)

                else:
                    res['Price'] = '${0:.2f}'.format(gift_card_price / 100)

        return JsonResponse(res, status=200)
