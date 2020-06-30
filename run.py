#!/usr/bin/env python3
import argparse
import json
import logging
import os
import requests
import sys
import time

AUTH_URL = "https://owner-api.teslamotors.com/oauth/token"
BEARER_PATH = "bearer_key"

class Credentials(object):
    def __init__(self, email, password, client_id, client_secret):
        self.email = email
        self.password = password
        self.client_id = client_id
        self.client_secret = client_secret
    
    def get_bearer(self):
        # return bearer either stored locally or fresh from Tesla
        if os.path.isfile(BEARER_PATH):
            with open(BEARER_PATH) as f:
                try:
                    bearer = json.loads(f.read())
                except json.decoder.JSONDecodeError:
                    bearer = {}
            # check if it's still valid
            if bearer.get("expires_in", 0) + bearer.get("created_at", 0) > time.time():
                logging.info("found stored key")
                return bearer.get("access_token")
        bearer = self.get_credentials()
        self.store_bearer(bearer)
        return bearer.get("access_token")

    def store_bearer(self, bearer):
        # stores bearer info in filesystem
        with open(BEARER_PATH, "w") as f:
            f.write(json.dumps(bearer))

    def get_credentials(self):
        body = { 
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "email": self.email,
            "password": self.password,
        }
        header = {"Content-Type": "application/json"}
        resp = requests.post(AUTH_URL, headers=header, json=body)
        return resp.json()


class VehicleManager(object):
    def __init__(self, bearer):
        self.header_auth = {
            "Authorization": "Bearer {}".format(bearer),
            "User-Agent": "github.com/ph0enix49/tesla-api",
        }
    
    def list_vehicles(self):
        resp = requests.get("https://owner-api.teslamotors.com/api/1/vehicles", headers=self.header_auth)
        for response in resp.json()['response']:
            print("{} with VIN: {} and vehicle ID: {}".format(
                response['display_name'], response['vin'], response['id']
            ))
    
    def wake_up(self, vehicle_id):
        requests.post(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/wake_up".format(vehicle_id),
            headers=self.header_auth,
        )

    def get_vehicle_state(self, vehicle_id):
        self.wake_up(vehicle_id)
        time.sleep(30)
        resp = requests.get(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/data_request/vehicle_state".format(vehicle_id),
            headers=self.header_auth,
        )
        print(resp.json())

    def get_drive_state(self, vehicle_id):
        self.wake_up(vehicle_id)
        time.sleep(30)
        resp = requests.get(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/data_request/drive_state".format(vehicle_id),
            headers=self.header_auth,
        )
        print(resp.json())
    
    def set_sentry(self, vehicle_id, param):
        self.wake_up(vehicle_id)
        time.sleep(30)
        body = {
            "on": param
        }
        resp = requests.post(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/command/set_sentry_mode".format(vehicle_id),
            headers=self.header_auth,
            json=body,
        )
        if resp.json().get("response", "{}").get("result") is True:
            msg = "sentry mode set to {}".format(param)
            logging.info(msg)
            print(msg)

    def charge_start(self, vehicle_id):
        self.wake_up(vehicle_id)
        time.sleep(30)
        resp = requests.post(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/command/charge_start".format(vehicle_id),
            headers=self.header_auth,
        )
        if resp.json().get("response", "{}").get("result") is True:
            msg = "charge successfully started"
            logging.info(msg)
            print(msg)

    def charge_stop(self, vehicle_id):
        self.wake_up(vehicle_id)
        time.sleep(30)
        resp = requests.post(
            "https://owner-api.teslamotors.com/api/1/vehicles/{}/command/charge_stop".format(vehicle_id),
            headers=self.header_auth,
        )
        if resp.json().get("response", "{}").get("result") is True:
            msg = "charge successfully stopped"
            logging.info(msg)
            print(msg)

def main():
    parser = argparse.ArgumentParser(description="run commands against a Tesla vehicle")
    parser.add_argument("-i", help="vehicle id to operate on")
    parser.add_argument("-l", "--list", help="lists all available vehicles", action="store_true")
    parser.add_argument("-s", "--state", help="get vehicle state", action="store_true")
    parser.add_argument("-d", "--drive-state", help="get drive state", action="store_true")
    parser.add_argument("-c", "--charging-start", help="initiate charging on vehicle", action="store_true")
    parser.add_argument("-f", "--charging-stop", help="finish charging on vehicle", action="store_true")
    parser.add_argument("-w", "--wake", help="wake up the vehicle", action="store_true")

    subparsers = parser.add_subparsers()
    sentry_cmd = subparsers.add_parser("sentry-mode", help="manipulate sentry mode")

    sentry_on_off = sentry_cmd.add_mutually_exclusive_group()
    sentry_on_off.add_argument("--on", help="turn sentry mode on", action="store_true", dest="sentry_on")
    sentry_on_off.add_argument("--off", help="turn sentry mode off", action="store_true", dest="sentry_off")

    args = parser.parse_args()
    credentials = Credentials(
        os.environ.get("TESLA_EMAIL"),
        os.environ.get("TESLA_PASSWORD"),
        os.environ.get("TESLA_CLIENT_ID"),
        os.environ.get("TESLA_CLIENT_SECRET"),
    )
    if not credentials.get_bearer():
        print("credentials are not available")
        sys.exit(1)
    vehicle_manager = VehicleManager(credentials.get_bearer())
    if args.list is True:
        vehicle_manager.list_vehicles()
    if not args.i:
        print("please provide vehicle ID to continue.")
        sys.exit(0)
    if args.state:
        vehicle_manager.get_vehicle_state(args.i)
    if args.drive_state:
        vehicle_manager.get_drive_state(args.i)
    if args.charging_start:
        vehicle_manager.charge_start(args.i)
    if args.charging_stop:
        vehicle_manager.charge_stop(args.i)
    if args.wake:
        vehicle_manager.wake_up(args.i)
    if hasattr(args, "sentry_on") or hasattr(args, "sentry_off"):
        param = "true" if args.sentry_on else "false"
        vehicle_manager.set_sentry(args.i, param)
    sys.exit(0)

if __name__ == "__main__":
    main()