#############################################################
# cs3430_s26_hw_4_prob_5_uts.py
# Problem 5 Unit Tests: Image Deblurring (Row-wise, 1D)
# Copyright (C) Vladimir Kulyukin.
# For personal study by my students enrolled in
# CS3430 S26: Scientific Computing, USU.
#############################################################

import unittest
import numpy as np
import os
import matplotlib.pyplot as plt

from cs3430_s26_hw_4_prob_5 import (
    build_blur_matrix_1d,
    blur_row,
    deblur_row_lu,
    blur_image_rows,
    deblur_image_rows
)

import numpy as np
import matplotlib.pyplot as plt

def load_grayscale_image(path: str) -> np.ndarray:
    """
    Load an image using matplotlib and convert to grayscale if needed.
    Returns a float array with values in [0, 255].
    """
    I = plt.imread(path)

    # If image is RGB or RGBA, convert to grayscale
    if I.ndim == 3:
        I = I[..., :3]              # drop alpha if present
        I = np.mean(I, axis=2)      # simple luminance approximation

    # Normalize to [0,255] if needed
    if I.max() <= 1.0:
        I = I * 255.0

    return I.astype(float)

def save_grayscale_image(I: np.ndarray, path: str) -> None:
    """
    Save a grayscale image using matplotlib.
    """
    plt.imsave(
        path,
        np.clip(I, 0, 255),
        cmap="gray",
        vmin=0,
        vmax=255
    )


class cs3430_s26_hw_4_prob_5_uts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW4 Problem 5 Unit Tests: Image Deblurring (1D)")
        print("============================================================")

    def test_blur_matrix_tridiagonal(self) -> None:
        print("\nSTART: test_blur_matrix_tridiagonal")

        A = build_blur_matrix_1d(5, alpha=0.2, beta=1.0)

        print("A =\n", A)

        for i in range(5):
            for j in range(5):
                if abs(i - j) > 1:
                    self.assertEqual(A[i, j], 0.0)

        print("PASS !!! test_blur_matrix_tridiagonal")

    def test_blur_deblur_identity_small(self) -> None:
        print("\nSTART: test_blur_deblur_identity_small")

        row = np.array([10., 20., 30., 40., 50.])
        alpha = 0.1
        beta = 1.0

        blurred = blur_row(row, alpha, beta)
        recovered = deblur_row_lu(blurred, alpha, beta)

        error = np.linalg.norm(recovered - row)

        print("row       =", row)
        print("recovered =", recovered)
        print("||error|| =", error)

        self.assertTrue(np.allclose(recovered, row, atol=1e-8))

        print("PASS !!! test_blur_deblur_identity_small")

    def test_deblurring_amplifies_error(self):
        x = np.linspace(0, 255, 50)
        A = build_blur_matrix_1d(len(x), alpha=0.2, beta=0.2)

        b = A @ x

        # Add small noise
        noise = 1e-6 * np.random.randn(len(b))
        b_noisy = b + noise
        
        x_rec = deblur_row_lu(b_noisy, alpha=0.2, beta=0.2)
        
        error = np.linalg.norm(x_rec - x)
        
        print("||recovery error|| =", error)

        self.assertTrue(error > 1e-3)
        
    def test_image_rowwise_blur_deblur(self) -> None:
        print("\nSTART: test_image_rowwise_blur_deblur")

        image = np.array([
            [10, 20, 30, 40],
            [40, 30, 20, 10]
        ], dtype=float)

        alpha = 0.2
        beta = 1.0

        blurred = blur_image_rows(image, alpha, beta)
        recovered = deblur_image_rows(blurred, alpha, beta)

        error = np.linalg.norm(recovered - image)

        print("image =\n", image)
        print("recovered =\n", recovered)
        print("||error|| =", error)

        self.assertTrue(np.allclose(recovered, image, atol=1e-8))

        print("PASS !!! test_image_rowwise_blur_deblur")

    def test_batch_rowwise_blur_deblur_on_imgs(self) -> None:
        print("\nSTART: test_batch_rowwise_blur_deblur_on_imgs")

        alpha = 0.2
        beta  = 0.2

        img_paths = [
            'imgs/BirdOrnament.jpg',
            'imgs/Elephant.jpg',
            'imgs/hive_1.png',
            'imgs/june.jpg',
            'imgs/nt_01.jpg',
            'imgs/road_1.png',
            'imgs/road_2.png',
            'imgs/road_3.png',
            'imgs/road_4.png',
            'imgs/sudoku.jpg'
            ]

        for path in img_paths:
            print("\n------------------------------------------------------------")
            print("Processing:", path)
            
            self.assertTrue(os.path.exists(path), f"Missing file: {path}")
            
            # 1) Load grayscale
            I = load_grayscale_image(path)
            print("  I.shape =", I.shape)
            print("  I.min/max =", float(I.min()), float(I.max()))
            
            # 2) Blur
            I_blur = blur_image_rows(I, alpha, beta)
            
            # 3) Attempt deblur (may fail!)
            try:
                I_deblur = deblur_image_rows(I_blur, alpha, beta)
                deblur_status = "success"
            except ValueError as e:
                print("  deblur failed:", e)
                deblur_status = "failed"
                I_deblur = I_blur.copy()
                
            # 4) Save outputs
            base, _ = os.path.splitext(path)
            blur_path   = base + "_blurred.png"
            deblur_path = base + "_deblurred.png"
            
            save_grayscale_image(I_blur, blur_path)
            save_grayscale_image(I_deblur, deblur_path)
                
            print("  blurred saved:", blur_path)
            print("  deblurred saved:", deblur_path)
            print("  status:", deblur_status)
                
            self.assertTrue(os.path.exists(blur_path))
            self.assertTrue(os.path.exists(deblur_path))
                
        print("\nPASS !!! test_batch_rowwise_blur_deblur_on_imgs")


if __name__ == "__main__":
    unittest.defaultTestLoader.sortTestMethodsUsing = None
    unittest.main()
