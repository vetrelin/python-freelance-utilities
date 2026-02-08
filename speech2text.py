import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
from datetime import datetime
import os
import sys

def record_and_transcribe():
    # настройка
    fs = 16000  # частота для Whisper
    print("--- ПРОГРАММА ЗАПУЩЕНА ---")
    print("Слушаю английскую речь... (Нажми Ctrl+C, чтобы остановить и сохранить)")
    
    recorded_chunks = []
    
    try:
        # записываем поток с микрофона
        with sd.InputStream(samplerate=fs, channels=1, dtype='float32') as stream:
            while True:
                chunk, overflowed = stream.read(fs) 
                recorded_chunks.append(chunk.copy())
    except KeyboardInterrupt:
        print("\n[Инфо] Запись остановлена пользователем.")

    if not recorded_chunks:
        print("Запись пуста, сохранять нечего.")
        return

    # обработка звука
    print("Обработка аудио данных...")
    full_recording = np.concatenate(recorded_chunks, axis=0)
    temp_filename = "temp_recording.wav"
    wav.write(temp_filename, fs, full_recording)

    # 3. нейросеть Whisper
    print("Загрузка модели AI (Whisper)...")
    model = whisper.load_model("base") 
    
    print("Распознавание текста (это может занять минуту)...")
    result = model.transcribe(temp_filename, language="en")
    text = result["text"]

    # сохранение на рабочий стол
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = f"speech2text + {date_str}.txt"
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    
    # если папки Desktop нет
    if not os.path.exists(desktop_path):
        desktop_path = os.path.join(os.path.expanduser("~"), "Рабочий стол")
        
    filepath = os.path.join(desktop_path, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(text.strip())

    # чистка
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    print(f"--- ГОТОВО ---")
    print(f"Текст сохранен здесь: {filepath}")
    print("Результат:")
    print(text)

if __name__ == "__main__":
    record_and_transcribe()