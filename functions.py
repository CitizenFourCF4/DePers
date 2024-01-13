import numpy as np 
from PIL import Image
import pandas as pd
import random
import imageio
import glob
import contextlib


def transform_file_to_df(file_path:str):
    with open (file_path, 'r') as file_:
        file = [string for string in file_]

    text = []
    for string in file:
        new_string = []
        for letter in string[:-1]:
            new_string.append(letter)
        text.append(new_string)
    text = np.array(text, dtype=str)

    df = pd.DataFrame(text, columns=None)
    sensitive_data = [elem for elem in range(34,60)]
    quasi_identifiers = [i for i in range(0,34)] + [i for i in range(60,80)]

    return df, sensitive_data, quasi_identifiers


def generate_k_anonymyty_cat(df:pd.DataFrame, quasi_identifiers:list, k:int, output_file_name:str) -> None:
    """
    Write k anonymity cat to file
    """
    if (df.shape[0] % k) == 0:
        for i in range(0,df.shape[0],k):
            for j in quasi_identifiers:
                candinates = [df[i+k][j] for k in range(0,k)]
                choice = random.choice(candinates)
                for k_ in range(k):
                    df.at[i+k_, j] = choice
    else:
        t = df.shape[0] - (df.shape[0] % k) - k
        for i in range(0,t,k):
            for j in quasi_identifiers:
                candinates = [df[i+k][j] for k in range(0,k)]
                choice = random.choice(candinates)
                for k_ in range(k):
                    df.at[i+k_, j] = choice

        for j in quasi_identifiers:
            candinates = [df[i][j] for i in range(t, df.shape[0])]
            choice = random.choice(candinates)
            for i in range(t, df.shape[0]):
                df.at[i, j] = choice
    
    k_anonymity_cat_np = df.to_numpy()
    
    with open(output_file_name, 'w+') as file:
        for elem in k_anonymity_cat_np:
            for sign in elem:
                file.write(sign)
            file.write('\n')


def check_k_anonym(df:pd.DataFrame, quasi_identifiers:list) -> int:
    equal_classes = df.groupby(quasi_identifiers)
    return equal_classes.size()[equal_classes.size()!=0].min()


def generate_gif(input_file_path, output_file_path="./image.gif"):
    # EXAMPLE
    # input_file_path = "./content*.png"
    # output_file_path = "./image.gif"
    with contextlib.ExitStack() as stack:
        imgs = (stack.enter_context(Image.open(f))
                for f in sorted(glob.glob(input_file_path)))
        img = next(imgs)
        img.save(fp=output_file_path, format='GIF', append_images=imgs,
                save_all=True, duration=400, loop=0)