from flask import Flask, jsonify, render_template
from kasa import SmartPlug
import ShellyPy
import asyncio
import os
from tapo import ApiClient
import subprocess



app = Flask(__name__)

# Smart-Geräte die initialisiert werden sollen:
device_shelly_schl_zimmer = ShellyPy.Shelly("192.168.10.75")
device_shelly_wohn_zimmer = ShellyPy.Shelly("192.168.10.80")
device_ip_kasasmartplug = '192.168.10.23'

# Flask app route für index.html (templates Ordner)
@app.route('/')
def index():
    return render_template('index.html')

# Funktionen zur Steuerung des Kasa-Smartplug
async def turn_on(device_ip):
    plug = SmartPlug(device_ip)
    await plug.update()
    await plug.turn_on()
    print(f"Der Smart Plug mit der IP-Adresse {device_ip} wurde eingeschaltet.")


async def turn_off(device_ip):
    plug = SmartPlug(device_ip)
    await plug.update()
    await plug.turn_off()
    print(f"Der Smart Plug mit der IP-Adresse {device_ip} wurde ausgeschaltet.")


async def get_status(device_ip):
    plug = SmartPlug(device_ip)
    await plug.update()
    status = 1 if plug.is_on else 0
    return f"{status}"

# Beispielaufrufe der Funktionen
# asyncio.run(turn_on(device_ip_kasasmartplug))
# asyncio.run(get_status(device_ip_kasasmartplug))
# asyncio.run(turn_off(device_ip_kasasmartplug))


#device_shelly_schl_zimmer.relay(0, turn=False)
#device_shelly_wohn_zimmer.relay(0, turn=False)


# Flask Routen:
@app.route('/wohnzimmer_deckenlampe_an/')
def wohnzimmer_deckenlampe_an():
    device_shelly_wohn_zimmer.relay(0, turn=True)
    return 'Wohnzimmer-Deckenlicht eingeschaltet.'

@app.route('/wohnzimmer_deckenlampe_aus/')
def wohnzimmer_deckenlampe_aus():
    device_shelly_wohn_zimmer.relay(0, turn=False)
    return 'Wohnzimmer-Deckenlicht ausgeschaltet.'

#------------------------------------------------

@app.route('/schlafzimmer_deckenlampe_an/')
def schlafzimmer_deckenlampe_an():
    device_shelly_schl_zimmer.relay(0, turn=True)
    return 'Schlafzimmer-Deckenlicht eingeschaltet.'

@app.route('/schlafzimmer_deckenlampe_aus/')
def schlafzimmer_deckenlampe_aus():
    device_shelly_schl_zimmer.relay(0, turn=False)
    return 'Schlafzimmer-Deckenlicht ausgeschaltet.'

#------------------------------------------------

@app.route('/schlafzimmer_wand_an/')
def schlafzimmer_wand_an():
    asyncio.run(turn_on(device_ip_kasasmartplug))
    return 'schlafzimmer_wand_an.'

@app.route('/schlafzimmer_wand_aus/')
def schlafzimmer_wand_aus():
    asyncio.run(turn_off(device_ip_kasasmartplug))
    return 'schlafzimmer_wand_aus.'

#------------------------------------------------

@app.route('/cpu_temp/')
def get_cpu_temperature():
    try:
        temperature_str = os.popen("vcgencmd measure_temp").readline().strip()
        temperature = float(temperature_str.split("=")[1].split("'")[0])

        ram_str = os.popen('free -m').read()
        free_ram = ram_str[121:126]
        ram = ram_str[96:101]

        get_my_ip = os.popen('hostname -I').read()
        my_ip = get_my_ip[0:13]

        spaces = os.popen('df -H /').read()
        size = spaces[66:68]
        avail = spaces[78:80]

        return f'IP: {my_ip}\nCPU Temperatur: {temperature}°C\nRAM: {ram} / {free_ram}MB\nSpeicher: {size}GB / {avail}GB'
    except Exception as e:
        return {'error': str(e)}



@app.route('/plug_workstation/')
async def main():
    tapo_username = "syildirimkdz@gmail.com"
    tapo_password = "Kerem007"
    device_ip = "192.168.10.82"
    client = ApiClient(tapo_username, tapo_password)

    try:
        device = await client.p110(device_ip)
        energy_usage = await device.get_energy_usage()
        aktueller_verbrauch = energy_usage.current_power
        return f"Verbrauch aktuell: {int(energy_usage.current_power/1000)} Watt\nVerbrauch Heute: {energy_usage.today_energy/1000} kWh\nVerbrauch Monat: {energy_usage.month_energy} kWh\nLaufzeit Heute: {int(energy_usage.today_runtime/60)} Std.\nLaufzeit Monat: {int(energy_usage.month_runtime/60)} Std.\nKosten akt. Monat: {round(energy_usage.month_energy/1000*.34,2)} €"
    except Exception as e:
        print(f"Error: {e}")


@app.route('/plug_kitchen/')
async def main2():
    tapo_username = "syildirimkdz@gmail.com"
    tapo_password = "Kerem007"
    device_ip = "192.168.10.84"
    client = ApiClient(tapo_username, tapo_password)

    try:
        device = await client.p110(device_ip)
        energy_usage = await device.get_energy_usage()
        aktueller_verbrauch = energy_usage.current_power
        return f"Verbrauch aktuell: {int(energy_usage.current_power/1000)} Watt\nVerbrauch Heute: {energy_usage.today_energy/1000} kWh\nVerbrauch Monat: {energy_usage.month_energy} kWh\nLaufzeit Heute: {int(energy_usage.today_runtime/60)} Std.\nLaufzeit Monat: {int(energy_usage.month_runtime/60)} Std.\nKosten akt. Monat: {round(energy_usage.month_energy/1000*.34,2)} €"
    except Exception as e:
        print(f"Error: {e}")

@app.route('/mariadb/status')
def mariadb_status():
    result = run_command("systemctl is-active mariadb")
    is_active = result == "active"
    return jsonify({"status": is_active})


################ Status services ##################        

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e.output}"
    
@app.route('/befehl/<cmd>')
def eigener_befehl(cmd):
    result = run_command(cmd)
    return jsonify({"Ausgabe": result})
        



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)