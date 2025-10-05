# Valikkokäynnistin uasyncio: valitse tehtävä ajettavaksi (ekstra)
try:
    import uasyncio as asyncio
except:
    print("uasyncio ei saatavilla tällä buildilla.")
    raise SystemExit

import sys

TASKS = {
    "1": "task01_print.py",
    "2": "task02_name.py",
    "3": "task03_blink.py",
    "4": "task04_timer_blink.py",
    "5": "task05_external_led.py",
    "6": "task06_button_led.py",
    "7": "task07_traffic.py",
    "8": "task08_reaction.py",
    "9": "task09_pir_alarm.py",
    "10": "task10_dht_console.py",
    "11": "task11_dht_oled.py",
    "12": "task12_pot_adc_pwm.py",
    "13": "task13_thingspeak.py",
    "14": "task14_buzzer_pwm.py",
    "15": "task15_button_irq.py",
}

def run_task(path):
    print("== Running:", path)
    with open(path) as f:
        code = f.read()
    exec(code, {"__name__":"__main__"})

def show_menu():
    print("\nIOT-tehtävät — valitse numero ja paina Enter:")
    for k in sorted(TASKS, key=lambda x: int(x)):
        print(" ", k, TASKS[k])
    print("q = quit")

def main():
    while True:
        show_menu()
        ch = input("> ").strip().lower()
        if ch == "q":
            break
        if ch in TASKS:
            run_task(TASKS[ch])
        else:
            print("Tuntematon valinta")

if __name__ == "__main__":
    main()
