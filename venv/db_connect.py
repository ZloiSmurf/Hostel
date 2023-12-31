import os
from dotenv import load_dotenv
import pymysql
from tkinter.messagebox import showerror, showwarning, showinfo

load_dotenv()

class DataBase():
    def __init__(self):
        super().__init__()
        self.connect()

    def connect(self):
        PASSWORD = os.getenv("DB_PASSWORD")
        LOGIN = os.getenv("DB_LOGIN")
        try:
            self.connection = pymysql.connect(
                host='localhost',
                port=3306,
                user=LOGIN,
                password=PASSWORD,
                database='hotel',
                cursorclass=pymysql.cursors.DictCursor
            )
            print("successfully connected...")
        except Exception as e:
            print("Connection refused...")
            print(e)
        """
        try:
                with self.connection.cursor() as cursor:
                    select_all_rows = "SELECT * FROM `hotels`"
                    cursor.execute(select_all_rows)
                    rows = cursor.fetchall()

                    print(rows)

            finally:
                self.connection.close()"""

    def login(self, email, password, table):
        """
        :param email: guest`s email
        :param password: guest`s password
        :return:
        """
        try:
            email = removeSQLinjection(email)
            password = removeSQLinjection(password)

            cursor = self.connection.cursor()
            if table == 'guest':
                select_all_rows = f"SELECT * FROM guests WHERE guest_email = '{email}' AND guest_password = '{password}'"
            else:
                select_all_rows = f"SELECT * FROM employees WHERE employee_email = '{email}' AND employee_password = '{password}'"
            cursor.execute(select_all_rows)
            rows = cursor.fetchall()
            if rows:
                #print(rows)
                #showinfo(title="Информация", message="Вход выполнен")
                return rows
            else:
                #showerror(title="Ошибка", message="Введённые ваи данные не верны")
                return rows
        except Exception as e:
            print(e)

    def registration(self, phone, email, name, surname, password):
        """
        Registers the user
        :param str phone: guest`s phone number
        :param str email: guest`s email
        :param str name: guest`s name
        :param str surname: guest`s surname
        :param str password: guest`s password
        :return:
        """
        try:
            cursor = self.connection.cursor()
            insert_query = f"INSERT INTO guests VALUES ('{phone}', '{name}', '{surname}', '{email}', '{password}', '0')"
            cursor.execute(insert_query)
            self.connection.commit()
            print("Succes")
        except Exception as e:
            print(e)

    def get_hotels(self, adress):
         try:
             adress = removeSQLinjection(adress)
             #print(adress)
             cursor = self.connection.cursor()
             select_all_rows = f"SELECT * FROM hotels WHERE country LIKE '%{adress}%' " \
                               f"OR city LIKE '%{adress}%' OR adress LIKE '%{adress}%'"
             cursor.execute(select_all_rows)
             rows = cursor.fetchall()
             #print(rows)
             return rows
         except Exception as e:
             print(e)

    def get_rooms(self, hotel, type, date1, date2):
        try:
            cursor = self.connection.cursor()
            select_hotel_rooms = f"SELECT DISTINCT type_name, facilities, price, getAvailableRoomsCount({hotel}, {type}, '{date1}', '{date2}') AS count FROM rooms " \
                                 f"JOIN types ON rooms.types_idType = types.idType " \
                                 f"WHERE rooms.hotels_idHotel = {hotel} AND types.idType = '{type}'"
            cursor.execute(select_hotel_rooms)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("get rooms error:", e)

    def reservate(self, phone, hotel, type, date1, date2):
        types = {'economy':1, 'standart':3, 'business':4}
        try:

            cursor = self.connection.cursor()
            free_rooms = f"SELECT getAvailableRooms({hotel}, {types[type]}, '{date1}', '{date2}') AS avaliable;"
            cursor.execute(free_rooms)
            rows = cursor.fetchall()[0]['avaliable'].split(", ")
            print(rows)
            print(phone, hotel, type, date1, date2)
            create_reservation = f"INSERT INTO reservation (guests_phone_number, rooms_hotels_idHotel, rooms_room_number, start_date, end_date) " \
                                 f"VALUES ('{phone}', {int(hotel)}, {int(rows[0])}, '{date1}', '{date2}')"
            print(create_reservation)
            cursor.execute(create_reservation)
            self.connection.commit()
        except Exception as e:
            print(e)

    def get_users_reservaion(self, phone):
        try:
            cursor = self.connection.cursor()
            select_users_reservations = f"SELECT country, city, adress, start_date, end_date FROM reservation " \
                                        f"JOIN hotels ON reservation.rooms_hotels_idHotel = hotels.idHotel " \
                                        f"WHERE reservation.guests_phone_number = '{phone}'"
            cursor.execute(select_users_reservations)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("get_user_resrvation error", e)

    def select_hotel(self, idHotel):
        try:
            cursor = self.connection.cursor()
            select_hotel = f"SELECT country, city, adress FROM hotels WHERE idHotel = {idHotel}"
            cursor.execute(select_hotel)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("select_hotel error", e)

    def select_rooms(self, idHotel):
        try:
            cursor = self.connection.cursor()
            select_rooms = f"SELECT DISTINCT get_room_guest({idHotel}, room_number) AS name, room_number, status_name, type_name FROM rooms " \
                           f"JOIN statuses ON rooms.statuses_idStatus = statuses.idStatus " \
                           f"JOIN types ON rooms.types_idType = types.idType " \
                           f"JOIN reservation ON reservation.rooms_hotels_idHotel = rooms.hotels_idHotel " \
                           f"WHERE hotels_idHotel = {idHotel}"
            cursor.execute(select_rooms)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("select_rooms error", e)

    def select_hotel_reservations(self, idHotel):
        try:
            cursor = self.connection.cursor()
            select_hotel_reservations = f"SELECT idReservation, phone_number, CONCAT(guest_name, ' ', guest_surname), " \
                                        f"rooms_room_number, start_date, end_date, checked_in, checked_out FROM reservation " \
                                        f"JOIN guests ON guests.phone_number = reservation.guests_phone_number " \
                                        f"WHERE rooms_hotels_idHotel = {idHotel}"
            cursor.execute(select_hotel_reservations)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("select_hotel_reservations error", e)

    def check_in_guest(self, idReservation):
        try:
            cursor = self.connection.cursor()
            check_in = f"UPDATE reservation SET checked_in = 1 WHERE idReservation = {idReservation};"
            cursor.execute(check_in)
            self.connection.commit()
        except Exception as e:
            print("check_in_guest error", e)

    def check_out_guest(self, idReservation):
        try:
            cursor = self.connection.cursor()
            check_out = f"UPDATE reservation SET checked_out = 1 WHERE idReservation = {idReservation}"
            cursor.execute(check_out)
            self.connection.commit()
            print("check_out")
        except Exception as e:
            print("check_out_guest error", e)

    def get_idVending(self, idHotel):
        try:
            cursor = self.connection.cursor()
            get_idVending = f"SELECT idVending_machines FROM vending_machines WHERE hotels_idHotel = {idHotel}"
            cursor.execute(get_idVending)
            rows = cursor.fetchall()
            return rows[0]['idVending_machines']
        except Exception as e:
            print("get_idVending error", e)

    def get_products(self, idVending):
        try:
            cursor = self.connection.cursor()
            get_products = f"SELECT product_name, quantity, product_price FROM vending_machines_has_products " \
                           f"JOIN products ON products_idProducts = idProducts " \
                           f"WHERE vending_machines_idVending_machines = {idVending}"
            cursor.execute(get_products)
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print("get_products error", e)

    def buy_products(self, idVending, products):
        try:
            products = [prod['quantity'] for prod in products]
            cursor = self.connection.cursor()
            buy_products = f"CALL set_new_products({idVending}, {products[0]}, {products[1]}, {products[2]}, " \
                        f"{products[3]}, {products[4]}, {products[5]})"
            cursor.execute(buy_products)
            self.connection.commit()
        except Exception as e:
            print("buy_products error", e)


def removeSQLinjection(text) -> str:
    text = text.replace("'", "")
    text = text.replace('"', '')
    return text.replace('\\', '')

