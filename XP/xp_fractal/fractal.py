"""Create beautiful fractal images."""
from PIL import Image


class Fractal:
    """Fractal class."""

    def __init__(self, size, scale, computation):
        """
        Initialize fractal.

        Arguments:
        size -- the size of the image as a tuple (x, y)
        scale -- the scale of x and y as a list of 2-tuple
                 [(minimum_x, minimum_y), (maximum_x, maximum_y)]
                 these are mathematical coordinates
        computation -- the function used for computing pixel values as a function
        """
        self.size = size
        self.scale = scale  # coordinates
        self.computation = computation
        self.image = Image.new("RGB", size)

    def compute(self):
        """Create the fractal by computing every pixel value."""
        width, height = self.size
        pixels = self.image.load()

        for px in range(width):
            for py in range(height):
                x = self.scale[0][0] + (px / width) * (self.scale[1][0] - self.scale[0][0])
                y = self.scale[0][1] + (py / height) * (self.scale[1][1] - self.scale[0][1])
                color = self.pixel_value((x, y))  # def color by the time or delay
                pixels[px, py] = color

    def pixel_value(self, pixel):
        """
        Return the number of iterations it took for the pixel to go out of bounds.

        Arguments:
        pixel -- the pixel coordinate (x, y)

        Returns:
        the number of iterations of computation it took to go out of bounds as integer.
        """
        x, y = pixel
        max_iter = 256
        x0, y0 = x, y

        for i in range(max_iter):
            x, y = self.computation(x, y, x0, y0)
            if x * x + y * y > 4:
                return i % 8 * 32, i % 16 * 16, i % 32 * 8  # Coloring pattern on your choice

        return 0, 0, 0  # Black for points within the set

    def save_image(self, filename):
        """
        Save the image to hard drive.

        Arguments:
        filename -- the file name to save the file to as a string.
        """
        self.image.save(filename)


def mandelbrot_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    return x * x - y * y + x_original, 2 * x * y + y_original


def julia_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    For different c and n make new function rather than change these constants.
    Otherwise tester will not give you any points :p

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    c = -0.7869 + 0.1889j  # DO NOT CHANGE
    n = 3  # EXPONENT. DO NOT CHANGE
    z = complex(x, y) ** n + c
    return z.real, z.imag


def ship_computation(x: float, y: float, x_original: float, y_original: float) -> tuple:
    """
    Return single iteration result of computation as tuple[x, y].

    You should invert y axis for correct results and picture

    :param x - mathematical x coordinate (transformed)
    :param y - mathematical y coordinate (transformed)
    :param x_original - mathematical x coordinate of pixel
    :param y_original - mathematical y coordinate of pixel

    :return tuple[x, y] after single iteration
    """
    x, y = abs(x), abs(y)  # Ensure both x and y are non-negative
    return x * x - y * y + x_original, -1 * (-2 * x * y + y_original)


if __name__ == "__main__":
    size = (1000, 1000)
    used_arguments = f"size_{size}_"

    # mandelbrot = Fractal(size, [(-2, -2), (2, 2)], mandelbrot_computation)
    # mandelbrot.compute()
    # mandelbrot.save_image(used_arguments + "mandelbrot.png")
    # print("Mandelbrot image generation completed.")

    # mandelbrot2 = Fractal(size, [(-0.74877, 0.065053), (-0.74872, 0.065103)], mandelbrot_computation)
    # mandelbrot2.compute()
    # mandelbrot2.save_image(used_arguments + "mandelbrot2.png")
    # print("Mandelbrot2 image generation completed.")

    # julia = Fractal(size, [(-2, -2), (2, 2)], julia_computation)
    # julia.compute()
    # julia.save_image(used_arguments + "julia.png")
    # print("Julia image generation completed.")
    #
    # ship = Fractal(size, [(-2, -2), (2, 2)], ship_computation)
    # ship.compute()
    # ship.save_image(used_arguments + "ship.png")
    # print("Ship image generation completed.")
