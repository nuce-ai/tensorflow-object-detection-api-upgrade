import pandas as pd 
df = pd.read_excel(r'object.xlsx')
classes = {}
counter = 1
for i in df["english"]:
    temp = {i.replace(" ","_") : counter}
    counter = counter + 1
    classes.update(temp)
def class_text_to_int(row_label):
    try:
        return classes[row_label]
    except:
        return None
# print(type(class_text_to_int("mop")))
# for i in classes:
#     print("item {")
#     print("     id: ",classes[i] )
#     print("     name: "+"'"+i.replace(" ","_")+"'")
#     print("}")

dicts = {'kettle': 1, 'teapot': 2, 'table': 3, 'toothbrush': 4, 'scrub_brush': 5, 'bowl': 6, 'stove': 7, 'jug': 8, 'toilet': 9, 'sink': 10, 'bathtub': 11, 'bath_sponge': 12, 'sieve': 13, 'whisk': 14, 'bottle': 15, 'pan': 16, 'floss': 17, 'cup': 18, 'knife': 19, 'plate': 20, 'clock': 21, 'chopsticks': 22, 'plunger': 23, 'toilet_paper': 24, 'chair': 25, 'mirror': 26, 'toothpaste': 27, 'kitchen_scissors': 28, 'towel': 29, 'microwave': 30, 'comb': 31, 'washing_machine': 32, 'exhaust_hood': 33, 'toaster': 34, 'coffee_maker': 35, 'hairdrier': 36, 'mixer': 37, 'blender': 38, 'fork': 39, 'pot': 40, 'rice_cooker': 41, 'fan': 42, 'spoon': 43, 'rolling_pin': 44, 'fridge': 45, 'showerhead': 46, 'faucet': 47, 'soap': 48, 'spatula': 49, 'bucket': 50, 'dustbin': 51, 'bookshelf': 52, 'broom': 53, 'candle': 54, 'lighter': 55, 'iron': 56, 'lamp': 57, 'sellotape': 58, 'telephone': 59, 'television': 60, 'vase': 61, 'curtains': 62, 'radio': 63, 'air_onditioner': 64, 'tray': 65, 'grater': 66, 'peeler': 67, 'chopping_board': 68, 'tweezer': 69, 'nail_clippers': 70, 'lock': 71, 'spade': 72, 'hoe': 73, 'rake': 74, 'glove': 75, 'jar': 76, 'can': 77, 'tissue': 78, 'razor': 79, 'tongs': 80, 'straw': 81, 'bottle_opener': 82, 'hanger': 83, 'mop': 84, 'switch': 85}

import os 
temp = []
for i in os.listdir("images"):
    temp.append(i.replace("-","_"))

n = {k: dicts[k] for k in dicts.keys() & set(temp)}
print(n)