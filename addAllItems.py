from game_server.resource.configdb.weapon_data import WeaponData
from game_server.resource.configdb.stigmata_data import StigmataData
from game_server.resource import ResourceManager
from game_server.game.enum.item_type import MainType
from database import MongoDBConnection

import tkinter as tk
from tkinter import messagebox


class MongoDBExec:
    def __init__(self, mongo):
        self.mongo = mongo
        self.manager = ResourceManager.instance()

    def items(self):
        last_item = self.mongo.get_collection("items").find_one(sort=[("UniqueID", -1)])
        unique_id = last_item["UniqueID"] + 1 if last_item else 1

        items_data = []

        for weapon in self.manager.instance().values(WeaponData):
            if weapon.rarity == weapon.maxRarity:
                weapon_data = {
                    "UniqueID": unique_id,
                    "ItemID": weapon.ID,
                    "Level": weapon.maxLv,
                    "Exp": 0,
                    "IsLocked": False,
                    "IsExtracted": False,
                    "QuantumBranchLists": None,
                    "MainType": MainType.WEAPON.value,
                    "EquipAvatarID": 0
                }
                items_data.append(weapon_data)
                unique_id += 1

        for stigmata in self.manager.instance().values(StigmataData):
            if stigmata.rarity == stigmata.maxRarity:
                stigmata_data = {
                    "UniqueID": unique_id,
                    "ItemID": stigmata.ID,
                    "Level": stigmata.maxLv,
                    "Exp": 0,
                    "SlotNum": 0,
                    "RefineValue": 0,
                    "PromoteTimes": 0,
                    "IsLocked": False,
                    "RuneLists": [],
                    "WaitSelectRuneLists": [],
                    "WaitSelectRuneGroupLists": [],
                    "MainType": MainType.STIGMATA.value,
                    "EquipAvatarID": 0
                }
                items_data.append(stigmata_data)
                unique_id += 1

        self.mongo.get_collection("items").insert_many(items_data)


def add_items(total: str, exe: MongoDBExec):
    try:
        total = int(total)
    except ValueError:
        messagebox.showerror("error type","you must input a number")
    n = 0
    while n < total:
        exe.items()
        n += 1
    messagebox.showinfo("success","success")


if __name__ == '__main__':
    # connect db
    mongoConn = MongoDBConnection()
    mongoConn.connect()
    executor = MongoDBExec(mongoConn)

    # gui
    root = tk.Tk()
    root.title("input number of each items your want")
    root.geometry("400x80")
    # text box
    entry = tk.Entry(root)
    entry.pack()
    # button
    button = tk.Button(root, text="add items", command=lambda: add_items(entry.get(),executor))
    button.pack()
    # loop
    root.mainloop()
