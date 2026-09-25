from abc import ABC, abstractmethod

# ЗАВДАННЯ 1: Класова ієрархія зі спадковістю

class NetworkDevice:
    def __init__(self, ip_address, hostname):
        self.ip_address = ip_address
        self.hostname = hostname

    def process_traffic(self):
        return f"{self.hostname} обробляє базовий мережевий трафік."

    def __str__(self):
        return f"Пристрій: {self.hostname} (IP: {self.ip_address})"

class Router(NetworkDevice):
    def __init__(self, ip_address, hostname, routing_protocol):
        super().__init__(ip_address, hostname)
        self.routing_protocol = routing_protocol

    def process_traffic(self):
        return f"{self.hostname} маршрутизує пакети за протоколом {self.routing_protocol}."

class Switch(NetworkDevice):
    def __init__(self, ip_address, hostname, ports_count):
        super().__init__(ip_address, hostname)
        self.ports_count = ports_count

    def process_traffic(self):
        return f"{self.hostname} комутує кадри на {self.ports_count} портах."

class Firewall(NetworkDevice):
    def __init__(self, ip_address, hostname, security_level):
        super().__init__(ip_address, hostname)
        self.security_level = security_level

    def process_traffic(self):
        return f"{self.hostname} фільтрує трафік (Рівень захисту: {self.security_level})."



# ЗАВДАННЯ 2: Інкапсуляція та property

class Sensor:
    def __init__(self, model, initial_temp):
        self._model = model                  
        self.__temperature = initial_temp    

    @property
    def temperature(self):
        return self.__temperature

    @temperature.setter
    def temperature(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Температура має бути числом!")
        if value < -273.15:
            raise ValueError("Температура не може бути нижчою за абсолютний нуль!")
        self.__temperature = value

    @property
    def state(self):
        """Обчислювана властивість (лише читання)"""
        if self.__temperature > 80:
            return "КРИТИЧНЕ НАГРІВАННЯ"
        elif self.__temperature < 0:
            return "ЗАМОРОЖУВАННЯ"
        return "НОРМА"



# ЗАВДАННЯ 3: Магічні методи

class DataSize:
    """Клас для представлення обсягу даних у мегабайтах."""
    def __init__(self, megabytes):
        self.mb = megabytes

    def __str__(self):
        return f"{self.mb} MB"
        
    def __repr__(self):
        return f"DataSize({self.mb})"

    def __add__(self, other):
        if isinstance(other, DataSize):
            return DataSize(self.mb + other.mb)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, DataSize):
            return DataSize(self.mb - other.mb)
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, DataSize):
            return self.mb == other.mb
        return False

    def __len__(self):
        """Повертає розмір у байтах (як умовну 'довжину')"""
        return int(self.mb * 1024 * 1024)



# ЗАВДАННЯ 4: Абстрактні класи та композиція

class NotificationSender(ABC):
    @property
    @abstractmethod
    def platform_name(self):
        pass

    @abstractmethod
    def send(self, message):
        pass

    def log_dispatch(self, message):
        print(f"[LOG] Повідомлення відправлено: {message[:10]}...")

class EmailSender(NotificationSender):
    @property
    def platform_name(self):
        return "Email Service"

    def send(self, message):
        print(f"Відправка Email: {message}")
        self.log_dispatch(message)

class SMSSender(NotificationSender):
    @property
    def platform_name(self):
        return "SMS Gateway"

    def send(self, message):
        print(f"Відправка SMS: {message}")
        self.log_dispatch(message)

class AlertSystem:
    
    def __init__(self, sender: NotificationSender):
        self.sender = sender  

    def broadcast_alert(self, text):
        print(f"--- Запуск оповіщення через {self.sender.platform_name} ---")
        self.sender.send(text)



# ЗАВДАННЯ 5: Патерн Strategy

class EncryptionStrategy(ABC):
    @abstractmethod
    def encrypt(self, data):
        pass

class AESEncryption(EncryptionStrategy):
    def encrypt(self, data):
        return f"[AES-256 Зашифровано]: {data[::-1]}"

class RSAEncryption(EncryptionStrategy):
    def encrypt(self, data):
        return f"[RSA-2048 Зашифровано]: {data.upper()}"

class XOREncryption(EncryptionStrategy):
    def encrypt(self, data):
        return f"[XOR Зашифровано]: {''.join([chr(ord(c) ^ 1) for c in data])}"

class SecureCommunicator:
    def __init__(self, strategy: EncryptionStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: EncryptionStrategy):
        self._strategy = strategy

    def send_data(self, data):
        encrypted_data = self._strategy.encrypt(data)
        print(f"Відправлення даних: {encrypted_data}")



if __name__ == "__main__":
    
    print("-" * 40)
    print("ЗАВДАННЯ 1: Класова ієрархія")
    devices = [
        Router("192.168.1.1", "R1", "OSPF"),
        Switch("192.168.1.2", "SW1", 24),
        Firewall("192.168.1.254", "FW1", "High")
    ]
    for dev in devices:
        print(dev)
        print(" ->", dev.process_traffic())
    
    print(f"\nЧи є R1 об'єктом NetworkDevice? {isinstance(devices[0], NetworkDevice)}")
    print(f"Чи є Switch підкласом NetworkDevice? {issubclass(Switch, NetworkDevice)}")


    print("\n" + "-" * 40)
    print("ЗАВДАННЯ 2: Інкапсуляція")
    cpu_temp = Sensor("AMD Ryzen", 45)
    print(f"Модель (protected): {cpu_temp._model}")
    print(f"Поточна температура: {cpu_temp.temperature}°C, Статус: {cpu_temp.state}")
    try:
        cpu_temp.temperature = -300
    except ValueError as e:
        print(f"Перехоплена помилка (setter): {e}")
    cpu_temp.temperature = 90
    print(f"Нова температура: {cpu_temp.temperature}°C, Статус: {cpu_temp.state}")
    print("Прямий доступ через name mangling:", cpu_temp._Sensor__temperature)


    print("\n" + "-" * 40)
    print("ЗАВДАННЯ 3: Магічні методи")
    file1 = DataSize(500)
    file2 = DataSize(250)
    print(f"__str__: {file1}")
    print(f"__repr__: {repr(file1)}")
    print(f"Додавання (__add__): {file1 + file2}")
    print(f"Віднімання (__sub__): {file1 - file2}")
    print(f"Рівність (__eq__): {file1 == file2}")
    print(f"Довжина в байтах (__len__): {len(file2)} bytes")


    print("\n" + "-" * 40)
    print("ЗАВДАННЯ 4: Абстрактні класи та композиція")
    try:
        base = NotificationSender()
    except TypeError as e:
        print(f"Спроба створити абстрактний клас: {e}")
    
    email_service = EmailSender()
    sms_service = SMSSender()
    system = AlertSystem(email_service)
    system.broadcast_alert("Увага! Виявлено загрозу.")
    system.sender = sms_service  
    system.broadcast_alert("Сервер перезавантажується.")


    print("\n" + "-" * 40)
    print("ЗАВДАННЯ 5: Патерн Strategy")
    secret_message = "SecretKey123"
    communicator = SecureCommunicator(AESEncryption())
    communicator.send_data(secret_message)
    communicator.set_strategy(RSAEncryption())
    communicator.send_data(secret_message)
    communicator.set_strategy(XOREncryption())
    communicator.send_data(secret_message)
    print("-" * 40)