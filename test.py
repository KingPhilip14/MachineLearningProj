import requests
from rembg import remove
from PIL import Image

if __name__ == '__main__':
    print('starting image process')

    # Open the input image
    input_image = Image.open(requests.get('https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/132.png', stream=True).raw).convert('RGB')
    print('Input image: collected')

    # Remove the background
    output_image = remove(input_image)
    print('Output image: collected')

    # Save the processed image
    output_image.save('C:/Users/ianth/PycharmProjects/MachineLearningProj/')
    print('Output image: saved')
