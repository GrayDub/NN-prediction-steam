import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler

# Устанавливаем использование GPU, если доступен
physical_devices = tf.config.list_physical_devices('GPU')
if physical_devices:
    try:
        # Устанавливаем использование GPU и настраиваем автоматическую настройку использования памяти
        tf.config.experimental.set_memory_growth(physical_devices[0], True)
        print("GPU найден и настроен на использование")
    except:
        print("Ошибка настройки GPU")
else:
    print("GPU не найден, будет использоваться CPU")

# Чтение данных из файла
file_path = r"C:\Users\User\Desktop\Specialized%20Killstreak%20Brass%20Beast.txt"
with open(file_path, 'r') as file:
    data = file.read()

# Преобразование данных в список
import json
data = json.loads(data)

# Извлечение цен продажи
prices = [entry[1] for entry in data["prices"]]

if not prices:
    print("Ошибка: Не удалось найти данные о ценах в файле.")
    exit()

# Преобразование данных в numpy массив
prices_array = np.array(prices)
print(np.array(prices))
# Масштабирование значений
scaler = MinMaxScaler(feature_range=(0, 1))
prices_scaled = scaler.fit_transform(prices_array.reshape(-1, 1))

# Создание набора данных для обучения
def create_dataset(dataset, time_steps=1):
    X, y = [], []
    for i in range(len(dataset)-time_steps):
        X.append(dataset[i:(i+time_steps), 0])
        y.append(dataset[i + time_steps, 0])
    return np.array(X), np.array(y)

time_steps = 3
X_train, y_train = create_dataset(prices_scaled, time_steps)

# Преобразование в трехмерный массив
X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))

# Создание модели нейронной сети
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)),
    tf.keras.layers.LSTM(units=50, return_sequences=False),
    tf.keras.layers.Dense(units=1)
])

# Компиляция модели
model.compile(optimizer='adam', loss='mean_squared_error')

# Обучение модели
model.fit(X_train, y_train, epochs=100, batch_size=1)

# Предсказание цен на следующие 3 дня
test_input = prices_scaled[-time_steps:].reshape((1, time_steps, 1))
predicted_prices_scaled = model.predict(test_input)

# Инвертирование масштабированных значений обратно в исходные цены
predicted_prices = scaler.inverse_transform(predicted_prices_scaled)
print("Predicted prices for the next 3 days:")
for price in predicted_prices:
    print("€", price[0])
