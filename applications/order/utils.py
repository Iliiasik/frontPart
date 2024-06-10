from django.core.mail import send_mail


def send_order_email(email, code, name):
    send_mail(
        'Nedvizhimost',
        f'Привет, перейди по этому пути что бы подвердить покупку: '
        f' \n\n http://127.0.0.1:8000/api/v1/order/activate/{code}',
        'iptest228228@gmail.com',
        [email]
    )


def calculate_booking_price(apartment, start_date, end_date, man, kids, animals):
    # Рассчитываем количество ночей
    num_nights = (end_date - start_date).days

    # Рассчитываем стоимость для взрослых и детей
    adult_price_per_night = 300  # Стоимость для взрослых за ночь
    child_price_per_night = 120  # Стоимость для детей за ночь

    total_adult_price = man * adult_price_per_night * num_nights
    total_child_price = kids * child_price_per_night * num_nights

    # Рассчитываем стоимость для животных
    animal_price_per_night = 60  # Стоимость для животных за ночь

    total_animal_price = 0
    if animals:
        total_animal_price = animal_price_per_night * num_nights

    # Рассчитываем стоимость аренды за ночь
    apartment_price_per_night = apartment.price
    total_apartment_price = apartment_price_per_night * num_nights

    # Суммируем все стоимости
    total_price = total_apartment_price + total_adult_price + total_child_price + total_animal_price

    return total_price
