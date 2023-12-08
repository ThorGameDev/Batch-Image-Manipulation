from PIL import Image
from PIL.Image import Image as pic
import numpy as np

# A dictionary of available functions and the parameters they expect
operation_identities = [
        {"Name": "Save_Backup", "Params": ("Prefix", )}, 
        {"Name": "Scale", "Params": ("X_Scale", "Y_Scale")}, 
        {"Name": "Crop_To_Square", "Params": ()},
        {"Name": "Crop", "Params": ("Start_X", "End_X", "Start_Y", "End_Y")},
        {"Name": "Crop_To_Contents", "Params": ()},
        {"Name": "Reduce_Scale", "Params": ("Factor", )},
        {"Name": "Flip_Across_X_Axis", "Params": ()},
        {"Name": "Flip_Across_Y_Axis", "Params": ()},
        {"Name": "Rotate", "Params": ("Amount", )},
        {"Name": "Rotate_And_Crop", "Params": ("Amount", )},
        {"Name": "Hue_Shift", "Params": ("Amount", )},
        {"Name": "Saturation_Shift", "Params": ("Amount", )},
        {"Name": "Vividness_Shift", "Params": ("Amount", )},
        {"Name": "HSV_Shift", "Params": ("Hue", "Saturation", "Vividness" )},
        ]

class Operation:
    '''Responsible for performing a single action on the picture'''
    def __init__(self, index: int, params: list = []):
        self.index = index
        self.save = False
        self.params = params
        try:
            match index:
                # 0: Save Backup
                case 0:
                    self.function = lambda img: save_point(img)
                    self.save = True
                    self.save_prefix = params[0]
                # 1: Scale
                case 1: 
                    p0 = int(params[0])
                    p1 = int(params[1])
                    self.function = lambda img: scale(img, p0, p1)
                # 2: Crop to square
                case 2:
                    self.function = crop_to_square
                # 3: Crop
                case 3:
                    p0 = int(params[0])
                    p1 = int(params[1])
                    p2 = int(params[2])
                    p3 = int(params[3])
                    self.function = lambda img: crop(img, p0, p1, p2, p3)
                # 4: Crop to contents
                case 4:
                    self.function = crop_to_contents
                # 5: Reduce
                case 5:
                    p0 = int(params[0])
                    self.function = lambda img: reduce_scale(img, p0)
                # 6: flip across x axis
                case 6:
                    self.function = flip_across_x_axis
                # 7: flip across x axis
                case 7:
                    self.function = flip_across_y_axis
                # 8: Rotate
                case 8:
                    p0 = int(params[0])
                    self.function = lambda img: rotate(img, p0)
                # 9: Rotate and crop
                case 9:
                    p0 = int(params[0])
                    self.function = lambda img: rotate_and_crop(img, p0)
                # 10: Shift Hue
                case 10:
                    p0 = int(params[0])
                    self.function = lambda img: hue_shift(img, p0)
                # 11: Shift Saturation
                case 11:
                    p0 = int(params[0])
                    self.function = lambda img: saturation_shift(img, p0)
                # 12: Shift Vividness
                case 12:
                    p0 = int(params[0])
                    self.function = lambda img: vividness_shift(img, p0)
                # 13: Shift Vividness
                case 13:
                    p0 = int(params[0])
                    p1 = int(params[1])
                    p2 = int(params[2])
                    self.function = lambda img: hsv_shift(img, p0, p1, p2)
        except:
            # Notifies the user if something went wrong
            print("Invalid Function was added! ")
            self.function = Invalid_Function
            self.index = -1

    def to_string(self):
        '''returns the contents of this operation in a human readable format'''
        if self.index == -1:
            return "INVALID FUNCTION"
        function = operation_identities[self.index] 
        string = function["Name"] + "("
        param_names = function["Params"]
        for num in range(len(param_names)):
            string = string + param_names[num].__str__() + "=" + self.params[num].__str__() + ", "
        return string + ")"

def Invalid_Function(image: pic) -> pic:
    print("An invalid function was executed!")
    return image

def save_point(image: pic) -> pic:
    return image

def scale(image: pic, x_scale: int, y_scale: int) -> pic:
    return image.resize((x_scale, y_scale))

def crop_to_square(image: pic) -> pic:
    width, height = image.size
    new = width if width < height else height
    left = (width - new)/2
    top = (height - new)/2
    right = (width + new)/2
    bottom = (height + new)/2
    left, top, right, bottom = int(left), int(top), int(right), int(bottom)
    return image.crop((left, top, right, bottom))

def crop(image: pic, start_x: int, end_x: int, start_y: int, end_y: int) -> pic:
    return image.crop((start_x, end_x, start_y, end_y))

def crop_to_contents(image: pic) -> pic:
    image_box = image.getbbox()
    return image.crop(image_box)

def reduce_scale(image: pic, factor: int) -> pic:
    return image.reduce(factor)

def flip_across_x_axis(image: pic) -> pic:
    return image.transpose(Image.FLIP_TOP_BOTTOM)

def flip_across_y_axis(image: pic) -> pic:
    return image.transpose(Image.FLIP_LEFT_RIGHT)

def rotate(image: pic, amount: int) -> pic:
    return image.rotate(amount, expand=True)

def rotate_and_crop(image: pic, amount: int) -> pic:
    return image.rotate(amount)

def hue_shift(image: pic, amount: int) -> pic:
    hsv_img = image.convert('HSV')
    hsv = np.array(hsv_img)
    hsv[..., 0] = (hsv[..., 0]+amount) % 360
    new_img = Image.fromarray(hsv, 'HSV')
    return new_img.convert('RGB')

def saturation_shift(image: pic, amount: int) -> pic:
    hsv_img = image.convert('HSV')
    hsv = np.array(hsv_img)
    hsv[..., 1] = np.clip(hsv[..., 1] + amount, 0, 255)
    new_img = Image.fromarray(hsv, 'HSV')
    return new_img.convert('RGB')

def vividness_shift(image: pic, amount: int) -> pic:
    hsv_img = image.convert('HSV')
    hsv = np.array(hsv_img)
    hsv[..., 2] = np.clip(hsv[..., 2] + amount, 0, 255)
    new_img = Image.fromarray(hsv, 'HSV')
    return new_img.convert('RGB')

def hsv_shift(image: pic, hue: int, saturation: int, vividness: int) -> pic:
    image = hue_shift(image, hue)
    image = saturation_shift(image, saturation)
    image = vividness_shift(image, vividness)
    return image
