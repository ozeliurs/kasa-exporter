from typing import Dict

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from plug import Plug

app = FastAPI()

plugs: Dict[str, Plug] = {}


@app.get("/scrape", response_class=HTMLResponse)
async def scrape(target: str):
    if target not in plugs:
        plugs[target] = Plug(target)

    plug_data = await plugs[target].scrape()

    return f"""# HELP plug_is_on Whether the plug is on
# TYPE plug_is_on gauge
plug_is_on{{alias="{plug_data['alias']}"}} {int(plug_data['is_on'])}
# HELP plug_rssi The signal strength of the plug
# TYPE plug_rssi gauge
plug_rssi{{alias="{plug_data['alias']}"}} {plug_data['rssi']}
# HELP plug_emeter_realtime_power The current power usage of the plug
# TYPE plug_emeter_realtime_power gauge
plug_emeter_realtime_power{{alias="{plug_data['alias']}"}} {plug_data['emeter_realtime']['power_mw']}
# HELP plug_emeter_this_month The power usage of the plug this month
# TYPE plug_emeter_this_month gauge
plug_emeter_this_month{{alias="{plug_data['alias']}"}} {plug_data['emeter_this_month']}
# HELP plug_emeter_today The power usage of the plug today
# TYPE plug_emeter_today gauge
plug_emeter_today{{alias="{plug_data['alias']}"}} {plug_data['emeter_today']}"""
