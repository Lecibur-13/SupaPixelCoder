import os
import math
import argparse
from PIL import Image

def file_to_image(file_path, output_dir):
    with open(file_path, 'rb') as file:
        data = file.read()
    
    binary_string = ''.join(format(byte, '08b') for byte in data)
    
    side_length = math.ceil(math.sqrt(len(binary_string)))
    total_bits = side_length * side_length
    
    binary_string = binary_string.ljust(total_bits, '0')
    
    image = Image.new('1', (side_length, side_length))
    pixels = image.load()
    
    for i in range(side_length):
        for j in range(side_length):
            index = i * side_length + j
            pixels[j, i] = int(binary_string[index])
    
    base_name = os.path.basename(file_path)
    name, _ = os.path.splitext(base_name)
    output_image_path = os.path.join(output_dir, f'{name}.png')
    image.save(output_image_path)
    print(f'Saved image to {output_image_path}')

def process_folder(folder_path, output_dir):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            file_to_image(file_path, output_dir)

def image_to_file(image_path, output_dir):
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size
    
    binary_string = ''
    for i in range(height):
        for j in range(width):
            binary_string += str(pixels[j, i])
    
    # Remove any padding bits added during encoding
    binary_string = binary_string.rstrip('0')
    
    byte_array = bytearray()
    for i in range(0, len(binary_string), 8):
        byte_segment = binary_string[i:i+8]
        if len(byte_segment) == 8:
            byte_array.append(int(byte_segment, 2))
    
    base_name = os.path.basename(image_path)
    name, _ = os.path.splitext(base_name)
    output_file_path = os.path.join(output_dir, name)
    with open(output_file_path, 'wb') as file:
        file.write(byte_array)
    print(f'Saved file to {output_file_path}')

def process_image_folder(folder_path, output_dir):
    for image_name in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_name)
        if os.path.isfile(image_path):
            image_to_file(image_path, output_dir)

def main():
    parser = argparse.ArgumentParser(description='Convert files to binary pixel images and vice versa.')
    parser.add_argument('--file', type=str, help='Path to the file to convert to an image.')
    parser.add_argument('--folder', type=str, help='Path to the folder containing files to convert to images.')
    parser.add_argument('--image', type=str, help='Path to the image to convert to a file.')
    parser.add_argument('--imagef', type=str, help='Path to the folder containing images to convert to files.')
    parser.add_argument('--output', type=str, required=True, help='Path to the output directory.')
    parser.add_argument('--decode', action='store_true', help='Decode image(s) to file(s).')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    
    if args.decode:
        if args.image:
            image_to_file(args.image, args.output)
        elif args.imagef:
            process_image_folder(args.imagef, args.output)
        else:
            print('You must specify either --image or --imagef for decoding.')
    else:
        if args.file:
            file_to_image(args.file, args.output)
        elif args.folder:
            process_folder(args.folder, args.output)
        else:
            print('You must specify either --file or --folder for encoding.')

if __name__ == '__main__':
    main()
