#############################################################
# edge.py
# Problem 3: Edge Detection
# bugs to vladimir kulyukin in canvas
#
# Copyright (C) Vladimir Kulyukin. All rights reserved.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, SoC, CoE, USU.
# No redistribution or online posting (e.g., Course Hero,
# Chegg, GitHub, ChatGPT, Gemini, Co-Pilot, Claude, DeepSeek,
# public drives, any LLMs) without prior written permission.
##############################################################

from __future__ import annotations

import numpy as np


class edge(object):
    """
    Sobel-like edge detection (pure NumPy).

    This implementation treats a grayscale image as a matrix:

        I[r, c] in [0, 255]

    and applies 3x3 Sobel-like kernels to compute:

        Gx: horizontal gradient response (detects vertical edges)
        Gy: vertical gradient response   (detects horizontal edges)

    We then compute the gradient magnitude:

        Gmag = sqrt(Gx^2 + Gy^2)

    and threshold it into a binary edge map (0 or 255).
    """

    KX = np.array([
        [-1.0, 0.0, 1.0],
        [-2.0, 0.0, 2.0],
        [-1.0, 0.0, 1.0]
    ], dtype=float)

    KY = np.array([
        [-1.0, -2.0, -1.0],
        [0.0,   0.0,  0.0],
        [1.0,   2.0,  1.0]
    ], dtype=float)

    @staticmethod
    def make_vertical_step_edge_image(H: int = 40, W: int = 60) -> np.ndarray:
        """
        Make a synthetic grayscale image with a sharp vertical boundary:
          left half = 0 (black)
          right half = 255 (white)
        """
        # 1) Create a 2D NumPy array (matrix) of shape (H, W) filled with zeros.
        #
        # - np.zeros((H, W), ...) makes an H-by-W matrix of 0's.
        # - dtype=float means the entries are stored as floating-point numbers,
        #   not integers. (Float is often more convenient in scientific computing
        #   because many computations produce non-integer values.)
        #
        # At this point, every pixel is 0.0, so the image is completely black.
        I = np.zeros((H, W), dtype=float)

        # 2) NumPy slicing: I[:, W//2:] means:
        #
        #   - ":"  means "all rows"
        #   - W//2 means integer division (middle column index)
        #   - "W//2:" means "all columns from the middle column to the end"
        #
        # So I[:, W//2:] selects the RIGHT HALF of the image matrix.
        #
        # We assign 255.0 to that entire region, meaning:
        #   - left half  stays 0.0   (black)
        #   - right half becomes 255.0 (white)
        #
        # This creates a sharp vertical boundary (a step edge) in the image,
        # which is perfect for testing edge detection.
        I[:, W // 2:] = 255.0

        # The above line is a great example of why NumPy is so powerful in scientific computing.
        # With a single statement:
        #
        #     I[:, W//2:] = 255.0
        #
        # we assign a value to an entire rectangular region of the matrix at once.
        # Without NumPy slicing, we would have to use the nested for-loops nightmare over rows and columns.
        # NumPy lets us express the operation clearly, compactly, and efficiently in one (one!) line:
        # I[:, W // 2:] = 255.0

        return I

    @staticmethod
    def make_horizontal_step_edge_image(H: int = 40, W: int = 60) -> np.ndarray:
        """
        Make a synthetic grayscale image with a sharp horizontal boundary:
          top half    = 0 (black)
          bottom half = 255 (white)
        """
        I = np.zeros((H, W), dtype=float)
        
        # More NumPy slicing below: I[H//2:, :] means:
        #   - "H//2" means integer division, so it gives the middle row index.
        #   - "H//2:" means "all rows from the middle row down to the last row"
        #   - ":" means "all columns"
        #
        # So I[H//2:, :] selects the BOTTOM HALF of the image matrix.
        #
        # We assign 255.0 to that entire region, meaning:
        #   - top half    stays 0.0   (black)
        #   - bottom half becomes 255.0 (white)
        #
        # This creates a sharp horizontal boundary (a step edge) in the image,
        # which is ideal for testing horizontal edge detection.
        #
        # Again, notice how much work NumPy does for us in a single statement.
        I[H // 2:, :] = 255.0
        return I

    @staticmethod
    def make_vh_step_edge_image(H: int = 40, W: int = 60) -> np.ndarray:
        """
        Make a synthetic grayscale image with BOTH a vertical and horizontal boundary.
        The image is split into 4 quadrants:

          top-left     = 0
          top-right    = 255
          bottom-left  = 255
          bottom-right = 0
        """
        I = np.zeros((H, W), dtype=float)

        h_mid = H // 2
        w_mid = W // 2

        # We use NumPy slicing again to assign values to two rectangular regions
        # (quadrants) of the image matrix.
        #
        # Recall:
        #   - h_mid = H//2 is the middle row index
        #   - w_mid = W//2 is the middle column index
        #
        # The image is split into four quadrants:
        #
        #   top-left      : rows [0 : h_mid),   cols [0 : w_mid)
        #   top-right     : rows [0 : h_mid),   cols [w_mid : W)
        #   bottom-left   : rows [h_mid : H),   cols [0 : w_mid)
        #   bottom-right  : rows [h_mid : H),   cols [w_mid : W)
        #
        # 1) I[:h_mid, w_mid:] selects the TOP-RIGHT quadrant:
        #    - ":h_mid"  means rows 0 up to (but not including) h_mid
        #    - "w_mid:"  means columns from w_mid to the end
        #
        # So, we set it to 255.0, making the top-right quadrant white.
        I[:h_mid, w_mid:] = 255.0   # top-right

        # 2) I[h_mid:, :w_mid] selects the BOTTOM-LEFT quadrant:
        #    - "h_mid:" means rows from h_mid to the end
        #    - ":w_mid" means columns 0 up to (but not including) w_mid
        #
        # So, we also set it to 255.0, making the bottom-left quadrant white.
        I[h_mid:, :w_mid] = 255.0   # bottom-left

        # The remaining two quadrants (top-left and bottom-right) stay 0.0 (black).
        #
        # This guarantees BOTH a vertical edge and a horizontal edge exist in the image,
        # which is useful for testing gradient magnitude edge detection.
        # This all done in two lines of code!
        
        return I

    @staticmethod
    def sobel_kx_response(I: np.ndarray) -> np.ndarray:
        """
        Compute the Sobel-like horizontal gradient response Gx using kernel Kx.

        This detects vertical edges (changes in intensity left-to-right).
        """
        H, W = I.shape

        # We create an output matrix Gx with the SAME shape as the input image I.
        #
        # np.zeros_like(I, ...) builds a new NumPy array that matches I in shape:
        #   if I has shape (H, W), then Gx also has shape (H, W).
        #
        # We fill it with zeros because we will compute the Sobel response
        # one pixel at a time and store the results into Gx[r, c].
        #
        # dtype=float ensures the Sobel responses are stored as floating-point
        # numbers (responses can be negative and not limited to [0,255]).
        Gx = np.zeros_like(I, dtype=float)

        # Below we loop over the "interior" pixels of the image (not the border).
        #
        # Why do we skip the border?
        # The Sobel kernel is 3x3, so to compute the response at pixel (r, c),
        # we need a full 3x3 patch centered at (r, c). That patch includes:
        #   rows r-1, r, r+1 and columns c-1, c, c+1
        #
        # If r or c is on the border (0 or H-1 / W-1), then r-1 or r+1 would go
        # out of bounds. So we iterate only from 1 to H-2 and 1 to W-2.
        for r in range(1, H - 1):
            for c in range(1, W - 1):
                # Extract the 3x3 patch centered at (r, c).
                #
                # NumPy slicing I[r-1:r+2, c-1:c+2] means:
                #   - rows from r-1 up to r+1 (because r+2 is excluded)
                #   - columns from c-1 up to c+1 (because c+2 is excluded)
                #
                # The result is a 3x3 matrix of pixel values.
                patch = I[r - 1:r + 2, c - 1:c + 2]

                # Compute the Sobel response at (r, c).
                #
                # edge.KX is the 3x3 Sobel-like horizontal gradient kernel:
                #   [-1  0  1]
                #   [-2  0  2]
                #   [-1  0  1]
                #
                # edge.KX * patch performs elementwise multiplication,
                # producing another 3x3 matrix.
                #
                # np.sum(...) then adds up all 9 products into one scalar value,
                # which is exactly the kernel response (a weighted sum of pixels).
                #
                # We store that scalar into Gx[r, c].
                Gx[r, c] = np.sum(edge.KX * patch)

        return Gx

    @staticmethod
    def sobel_ky_response(I: np.ndarray) -> np.ndarray:
        """
        Compute the Sobel-like vertical gradient response Gy using kernel Ky.

        This detects horizontal edges (changes in intensity top-to-bottom).
        """
        H, W = I.shape

        # 1) Create an output matrix Gy with the SAME shape as the input image I.
        #
        # Gy will store the vertical gradient response at each pixel.
        # (This detects horizontal edges: changes in intensity top-to-bottom.)
        #
        # We fill it with zeros at first and then compute responses for the
        # interior pixels.
        Gy = np.zeros_like(I, dtype=float)

        # 2) Loop over interior pixels only (skip border pixels), because we need
        # a full 3x3 patch around each pixel to apply the Sobel kernel.
        for r in range(1, H - 1):
            for c in range(1, W - 1):

                # 2.1) Extract the 3x3 patch centered at (r, c). You can use
                # this slicing I[r - 1:r + 2, c - 1:c + 2]. Save the slide in patch.

                patch = I[r - 1:r + 2, c - 1:c + 2]

                # 2.2) Apply the Sobel-like vertical kernel Ky using elementwise
                # multiplication and sum the results.
                #
                # edge.KY is the 3x3 Sobel-like vertical gradient kernel:
                #   [-1 -2 -1]
                #   [ 0  0  0]
                #   [ 1  2  1]
                #
                # This kernel responds strongly when pixel values change
                # significantly from top to bottom (a horizontal edge).
                # Save the response in Gy[r,c]. This is identical to
                # the compute of Gx[r, c] in the previous method. But,
                # of course, you have to apply edge.KY.

                Gy[r, c] = np.sum(edge.KY * patch)

        return Gy

    @staticmethod
    def grad_magnitude(Gx: np.ndarray, Gy: np.ndarray) -> np.ndarray:
        """
        Compute gradient magnitude:

            |G| = sqrt(Gx^2 + Gy^2)
        """
        # YOUR CODE HERE. You can use np.sqrt.
        Gmag = np.sqrt(Gx**2 + Gy**2)
        return Gmag

    @staticmethod
    def binary_edge_map(G: np.ndarray, T: float = 100.0) -> np.ndarray:
        """
        Convert gradient response into a binary edge map:
          non-edge -> 0
          edge     -> 255
        """
        E = np.zeros_like(G, dtype=float)

        # The next code line thresholds the gradient response matrix G into a binary edge map.
        #
        # Step 1: np.abs(G)
        # -----------------
        # The Sobel response values in G can be positive or negative:
        #   - positive means intensity increases in one direction
        #   - negative means intensity increases in the opposite direction
        #
        # Since we care about the *strength* of the edge (not the direction),
        # we take the absolute value of every entry.
        #
        # Step 2: np.abs(G) >= T
        # ----------------------
        # This produces a Boolean mask (a matrix of True/False values) of the same
        # shape as G. For each pixel:
        #   True  means "this pixel is an edge candidate"
        #   False means "this pixel is not an edge"
        #
        # Step 3: E[mask] = 255.0
        # -----------------------
        # This is NumPy Boolean indexing. It means:
        #   "For every location where the mask is True, set E to 255.0."
        #
        # Since E starts as all zeros, the result is a binary image:
        #   - 0.0    means "not an edge" (black)
        #   - 255.0  means "edge"       (white)
        #
        # This is a very compact and efficient NumPy shortcut. Without Boolean
        # indexing, we would need nested loops with if-statements.
        E[np.abs(G) >= T] = 255.0
        return E

    @staticmethod
    def binary_edge_map_from_mag(Gmag: np.ndarray, T: float = 100.0) -> np.ndarray:
        """
        Threshold gradient magnitude into a 0/255 binary edge map.
        """
        E = np.zeros_like(Gmag, dtype=float)
        E[Gmag >= T] = 255.0
        return E

    @staticmethod
    def binary_edge_map_from_gradmag(Gx: np.ndarray, Gy: np.ndarray,
                                     T: float = 100.0) -> tuple[np.ndarray, np.ndarray]:
        """
        Compute gradient magnitude and threshold it into a binary edge map.

        Returns
        -------
        tuple[np.ndarray, np.ndarray]
            (Gmag, E)
        """
        # 1) Compute Gmag from Gx and Gy by applying grad_magnitude

        Gmag = edge.grad_magnitude(Gx, Gy)

        # 2) Apply binary_edge_map_from_mag(Gmag, T=T) to compute E.
        
        E = edge.binary_edge_map_from_mag(Gmag, T=T)       
        
        return Gmag, E

    # helper method
    import matplotlib.figure as mplfig
    @staticmethod
    def save_fig(fig: mplfig.Figure, out_path: str) -> None:
        fig.savefig(out_path, dpi=200, bbox_inches="tight")
        print(f"Saved: {out_path}")


    # helper method
    @staticmethod
    def rgb_to_grayscale(Irgb: np.ndarray) -> np.ndarray:
        """
        Convert an RGB (or RGBA) image array into a grayscale float image.

        Parameters
        ----------
        Irgb : np.ndarray
            Image array of shape (H, W, 3) or (H, W, 4).

        Returns
        -------
        np.ndarray
            Grayscale image of shape (H, W), dtype=float, with values in [0,255].
        """
        # 1) Check that the input looks like a color image array.
        #
        # A typical RGB image loaded into NumPy has shape:
        #    (H, W, 3)
        # meaning:
        #    H rows (height), W columns (width), and 3 color channels (R,G,B).
        #
        # Sometimes an image includes an alpha channel (transparency) and has shape:
        #    (H, W, 4)
        # meaning:
        #    R, G, B, and A (alpha).
        #
        # If Irgb is not 3D OR the third dimension is not 3 or 4, we reject it.
        if Irgb.ndim != 3 or Irgb.shape[2] not in [3, 4]:
            raise ValueError("Irgb must have shape (H, W, 3) or (H, W, 4).")

        # 2) Drop alpha channel if present (RGBA -> RGB).
        #
        # If the image is RGBA, we ignore the 4th channel because our grayscale
        # conversion formula only needs R, G, and B.
        #
        # Irgb[:, :, :3] means:
        #   - all rows (:)
        #   - all columns (:)
        #   - only channels 0,1,2 (the first 3 channels)
        if Irgb.shape[2] == 4:
            Irgb = Irgb[:, :, :3]

        # 3) Convert to float so arithmetic is safe and predictable.
        #
        # Image libraries often load images using integer types such as uint8.
        # Converting to float allows multiplication and weighted sums without
        # integer rounding/truncation errors.
        Irgb = Irgb.astype(float)

        # 4) Different file types may load into NumPy using different numeric ranges:
        #
        #   - Many PNG images load as floats in [0, 1]
        #   - Many JPG images load as integers in [0, 255]
        #
        # We want a consistent range in this homework: [0, 255].
        # So if the maximum value is <= 1.0, we assume the image is in [0,1]
        # and scale it up to [0,255].
        if np.max(Irgb) <= 1.0:
            Irgb = Irgb * 255.0

        # 5) Extract the three color channels using NumPy slicing.
        #
        # After this:
        #   R, G, B are each (H, W) matrices.
        #
        # R[r,c] is the red intensity at pixel (r,c),
        # G[r,c] is the green intensity at pixel (r,c),
        # B[r,c] is the blue intensity at pixel (r,c).
        R = Irgb[:, :, 0]
        G = Irgb[:, :, 1]
        B = Irgb[:, :, 2]

        # 6) Convert RGB to grayscale using the standard luminance formula:
        #
        #   gray = 0.299*R + 0.587*G + 0.114*B
        #
        # This is a perceptual weighting:
        # the human visual system is most sensitive to green, then red,
        # then blue. This formula produces a grayscale image that looks
        # natural to human eyes.
        #
        # The result is a grayscale matrix of shape (H, W).
        return 0.299 * R + 0.587 * G + 0.114 * B

    # helper method
    @staticmethod
    def load_grayscale_image(path: str) -> np.ndarray:
        """
        Load an image file (PNG/JPG) and return it as a grayscale matrix.

        Parameters
        ----------
        path : str
            Path to the image file.

        Returns
        -------
        np.ndarray
            A grayscale image matrix of shape (H, W), dtype=float, in [0,255].

        Notes
        -----
        This method uses matplotlib.pyplot.imread under the hood.

        - Some images load with values in [0,1] (especially PNG).
        - Others load with values in [0,255] (often JPG / uint8).
        This method normalizes to float intensities in [0,255].
        """
        import matplotlib.pyplot as plt

        I = plt.imread(path)

        # If already grayscale (H, W), just normalize range.
        if I.ndim == 2:
            I = I.astype(float)
            if np.max(I) <= 1.0:
                I = I * 255.0
            return I

        # Otherwise assume RGB or RGBA.
        return edge.rgb_to_grayscale(I)
        

