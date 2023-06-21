import datetime
from asgiref.sync import sync_to_async
from apps.authentication.models import MegaUser as User
from apps.main.models import Order, Sale, Comment, UserCashback, UserSale, OrderDetail, Cashback, Admin


@sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(telegram_id=user_id)
        return user
    except:    
        return None 


@sync_to_async
def chek_user(phone):
    try:
        user = User.objects.filter(phone=phone).first()
        if user:
            return True
        return False
    except:
        return False
    
    
@sync_to_async
def get_user_by_phone(phone):
    try:
        user = User.objects.filter(phone=phone).first()
        return user
    except:
        return None


@sync_to_async
def set_user_telegram(user_id, phone, name):
    try:
        user = User.objects.get(phone=phone)
        user.telegram_id = user_id
        user.name = name
        user.save()
        return user
    except:
        return None


@sync_to_async
def get_user_monthly(user_id):
    try:
        month = datetime.date.today().month
        orders = Order.objects.filter(user__telegram_id=user_id, created_date__month=month, created_date__year=datetime
                                      .date.today().year).values('u_sumuzs').all()
        order_sum_list = [order['u_sumuzs'] for order in orders]
        return sum(order_sum_list)   
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_user_yearly(user_id):
    try:
        orders = Order.objects.filter(user__telegram_id=user_id, created_date__year=datetime.date.today().year)\
            .values('u_sumuzs').all()
        order_sum_list = [order['u_sumuzs'] for order in orders]
        return sum(order_sum_list)   
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_user_seasonly(user_id):
    try:
        current_month = datetime.date.today().month
        year = datetime.date.today().year
        start_month = ((current_month - 1) // 3) * 3
        end_month = start_month + 2 if start_month != 12 else 12
        orders = Order.objects.filter(user__telegram_id=user_id, 
                                      created_date__year=year,
                                      created_date__month__gte=start_month,
                                      created_date__month__lte=end_month
                                      ).values('u_sumuzs').all()
        order_sum_list = [order['u_sumuzs'] for order in orders]
        return sum(order_sum_list)
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_active_sales():
    try:
        return Sale.objects.filter(active=True).all().order_by('-id')
    except:
        return None
    

@sync_to_async
def get_user_sales(user_id):
    try:
        return UserSale.objects.filter(user__telegram_id=user_id, sale__active=True, is_full=False).all()
    except:
        return None
    

@sync_to_async
def get_user_kashbacks(user_id):
    try:
        cashbacks = UserCashback.objects.filter(user__telegram_id=user_id, active=True).all()
        cashback_sum_list = [cash['summa'] for cash in cashbacks]
        return sum(cashback_sum_list)
    except Exception as exx:
        print(exx)
        return None


@sync_to_async 
def add_comment(user_id, comment):
    user = User.objects.get(telegram_id=user_id)
    return Comment(user=user, comment=comment)


@sync_to_async
def get_orders(user_id):
    try:
        orders = Order.objects.filter(user__telegram_id=user_id).all()
        return orders
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_orders_by_year(user_id, year):
    try:
        orders = Order.objects.filter(user__telegram_id=user_id, created_date__year=year).all()
        return orders
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_orders_by_month(user_id, year, month):
    try:
        orders = Order.objects.filter(
            user__telegram_id=user_id,
            created_date__year=year,
            created_date__month=month).all()
        return orders
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def cash_m(user_id):
    try:
        cash = UserCashback.objects.filter(active=True, user__telegram_id=user_id, period="month").first()
        return cash
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def cash_s(user_id):
    try:
        cash = UserCashback.objects.filter(active=True, user__telegram_id=user_id, period="season").first()
        return cash
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def cash_y(user_id):
    try:
        cash = UserCashback.objects.filter(active=True, user__telegram_id=user_id, period="year").first()
        return cash
    except Exception as exx:
        print(exx)
        return None


@sync_to_async
def get_sales():
    return Sale.object.filter(active=True).all()

@sync_to_async
def add_user_sale(user_id, sale_id):
    user = User.objects.get(telegram_id=user_id)
    sale = Sale.objects.get(id=sale_id)
    print(sale_id)
    sale, created = UserSale.objects.get_or_create(user=user, sale=sale)
    sale.save()
    return sale


@sync_to_async
def get_sale(sale_id):
    try:
        return Sale.objects.get(id=sale_id)
    except:
        return None


@sync_to_async
def get_order_details(order_id):
    return OrderDetail.objects.filter(order_id=order_id).all()


@sync_to_async
def get_cashback_monthly():
    cashback, created = Cashback.objects.get_or_create(
        period="month"
    )
    return cashback


@sync_to_async
def get_cashback_season():
    cashback, created = Cashback.objects.get_or_create(
        period="season"
    )
    return cashback


@sync_to_async
def get_cashback_year():
    cashback, created = Cashback.objects.get_or_create(
        period="year"
    )
    return cashback


@sync_to_async
def check_user_is_admin(user_id):
    admin = Admin.objects.get(user_id=user_id)
    if admin:
        return True
    return False

