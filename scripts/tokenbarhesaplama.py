from User.models import CranioTokenBar
def hesapla():
    hesaplanmiş = 0
    price_per_token = 1
    for price in range(100, 5001, 100):
        if price == 100:
            hesaplanmiş = price * price_per_token
            print(price_per_token)
            print(float(hesaplanmiş))
            tokenbar = CranioTokenBar.objects.get(
                token=price,
                total_price=hesaplanmiş,
                token_per_price=price_per_token,
                )
            tokenbar.total_price = tokenbar.total_price/2
            tokenbar.token_per_price = tokenbar.token_per_price/2
            tokenbar.save()
            continue
        if price < 1100:
            percent = 4
            price_per_token = price_per_token - (price_per_token*percent/100)
            print(price_per_token)
            hesaplanmiş = price * price_per_token
        elif price < 2100:
            percent = 3
            price_per_token = price_per_token - (price_per_token*percent/100)

            print(price_per_token)

            hesaplanmiş = price * price_per_token
        elif price < 4100:
            percent = 2
            price_per_token = price_per_token - (price_per_token*percent/100)

            print(price_per_token)

            hesaplanmiş = price * price_per_token
        elif price < 5100:
            percent = 1
            price_per_token = price_per_token - (price_per_token*percent/100)

            print(price_per_token)

            hesaplanmiş = price * price_per_token

        tokenbar = CranioTokenBar.objects.get(
                token=price,
                total_price=hesaplanmiş,
                token_per_price=price_per_token,
                )
        tokenbar.total_price = tokenbar.total_price/2
        tokenbar.token_per_price = tokenbar.token_per_price/2
        tokenbar.save()
        print(float(hesaplanmiş))