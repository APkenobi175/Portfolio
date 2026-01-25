#############################################################
# cs3430_s26_hw_3_prob_3_uts.py
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

import unittest
import numpy as np
import os
import matplotlib.pyplot as plt

from edge import edge

class cs3430_s26_hw_3_prob_3_edge_uts(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 3 Unit Tests: Edge Detection")
        print("============================================================")

    def test_vertical_step_edge_detected_by_gx(self) -> None:
        print("\nSTART: test_vertical_step_edge_detected_by_gx")

        H, W = 40, 60
        I = edge.make_vertical_step_edge_image(H, W)

        Gx = edge.sobel_kx_response(I)
        Ex = edge.binary_edge_map(Gx, T=100.0)

        print("  I.shape  =", I.shape)
        print("  Gx.shape =", Gx.shape)
        print("  Ex.shape =", Ex.shape)

        # Confirm edges exist.
        self.assertTrue(np.any(Ex == 255.0))
        self.assertTrue(np.any(Ex == 0.0))

        # The edge should occur near the vertical boundary at column W//2.
        col_mid = W // 2
        edge_band = Ex[:, col_mid - 2: col_mid + 2]

        print("  edge band shape =", edge_band.shape)

        # There should be some detected edges in that band.
        self.assertTrue(np.any(edge_band == 255.0))

        # Far away from the edge, there should be no edges.
        #
        # The vertical step edge is located near column col_mid = W//2.
        # Pixels far to the left or far to the right should be uniform
        # (all black or all white), so Sobel should NOT detect edges there.
        #
        # Ex[:, :col_mid - 10] means:
        #   - ":"           -> all rows
        #   - ":col_mid-10" -> all columns from 0 up to (col_mid-10)
        #
        # This selects a region safely on the LEFT side of the image, well away
        # from the boundary.
        left_far = Ex[:, :col_mid - 10]

        # Ex[:, col_mid + 10:] means:
        #   - ":"             -> all rows
        #   - "col_mid+10:"   -> all columns from (col_mid+10) to the end
        #
        # This selects a region safely on the RIGHT side of the image, well away
        # from the boundary.
        right_far = Ex[:, col_mid + 10:]

        # np.any(left_far == 255.0) checks whether there exists at least one pixel
        # in left_far that equals 255.0 (meaning it was marked as an edge).
        #
        # Since left_far is far away from the true boundary, we expect NO edges there.
        # Therefore, np.any(left_far == 255.0) should be False.
        self.assertFalse(np.any(left_far == 255.0))

        # Same logic for the region far to the right of the boundary.
        # We expect NO edge pixels (255.0) in right_far either.
        self.assertFalse(np.any(right_far == 255.0))

        print("PASS !!! test_vertical_step_edge_detected_by_gx")

    def test_horizontal_step_edge_detected_by_gy(self) -> None:
        print("\nSTART: test_horizontal_step_edge_detected_by_gy")

        H, W = 40, 60
        I = edge.make_horizontal_step_edge_image(H, W)

        Gy = edge.sobel_ky_response(I)
        Ey = edge.binary_edge_map(Gy, T=100.0)

        print("  I.shape  =", I.shape)
        print("  Gy.shape =", Gy.shape)
        print("  Ey.shape =", Ey.shape)

        self.assertTrue(np.any(Ey == 255.0))
        self.assertTrue(np.any(Ey == 0.0))

        row_mid = H // 2
        edge_band = Ey[row_mid - 2: row_mid + 2, :]

        print("  edge band shape =", edge_band.shape)

        self.assertTrue(np.any(edge_band == 255.0))

        top_far = Ey[:row_mid - 10, :]
        bottom_far = Ey[row_mid + 10:, :]

        self.assertFalse(np.any(top_far == 255.0))
        self.assertFalse(np.any(bottom_far == 255.0))

        print("PASS !!! test_horizontal_step_edge_detected_by_gy")

    def test_vh_step_edges_detected_by_grad_mag(self) -> None:
        print("\nSTART: test_vh_step_edges_detected_by_grad_mag")

        H, W = 40, 60
        I = edge.make_vh_step_edge_image(H, W)

        Gx = edge.sobel_kx_response(I)
        Gy = edge.sobel_ky_response(I)

        Gmag, Emag = edge.binary_edge_map_from_gradmag(Gx, Gy, T=100.0)

        print("  I.shape    =", I.shape)
        print("  Gmag.shape =", Gmag.shape)
        print("  Emag.shape =", Emag.shape)
        print("  |G| min/max =", float(np.min(Gmag)), float(np.max(Gmag)))

        self.assertTrue(np.any(Emag == 255.0))
        self.assertTrue(np.any(Emag == 0.0))

        # Check edges show up near both the horizontal and vertical midlines.
        row_mid = H // 2
        col_mid = W // 2

        vertical_band = Emag[:, col_mid - 2: col_mid + 2]
        horizontal_band = Emag[row_mid - 2: row_mid + 2, :]

        self.assertTrue(np.any(vertical_band == 255.0))
        self.assertTrue(np.any(horizontal_band == 255.0))

        print("PASS !!! test_vh_step_edges_detected_by_grad_mag")

    def test_border_pixels_remain_zero(self) -> None:
        print("\nSTART: test_border_pixels_remain_zero")

        H, W = 40, 60
        I = edge.make_vh_step_edge_image(H, W)

        Gx = edge.sobel_kx_response(I)
        Ex = edge.binary_edge_map(Gx, T=100.0)

        # Since the loops run from 1..H-2 and 1..W-2,
        # the border must remain 0 (black).
        self.assertTrue(np.all(Ex[0, :] == 0.0))
        self.assertTrue(np.all(Ex[H - 1, :] == 0.0))
        self.assertTrue(np.all(Ex[:, 0] == 0.0))
        self.assertTrue(np.all(Ex[:, W - 1] == 0.0))

        print("PASS !!! test_border_pixels_remain_zero")

class cs3430_s26_hw_3_prob_3_save_fig_uts(unittest.TestCase):
    """
    Unit tests for edge.save_fig().

    This ensures students can generate a plot and save it to disk
    without GUI pop-ups.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 3 Unit Tests: save_fig")
        print("============================================================")

    def test_save_fig_creates_png_file(self) -> None:
        print("\nSTART: test_save_fig_creates_png_file")

        I = edge.make_vh_step_edge_image(H=20, W=30)

        fig = plt.figure()
        plt.title("UT: Synthetic Image")
        plt.imshow(I, cmap="gray", vmin=0, vmax=255)
        plt.axis("off")
        plt.tight_layout()

        out_path = "ut_saved_figure.png"

        edge.save_fig(fig, out_path)

        # Close figure so no GUI resources hang around.
        plt.close(fig)

        # Verify output file exists and is non-empty.
        self.assertTrue(os.path.exists(out_path))

        file_size = os.path.getsize(out_path)
        print("  file size =", file_size, "bytes")

        self.assertTrue(file_size > 0)

        # Cleanup: if you want to remove file after test passes, do:
        # os.remove(out_path)

        print("PASS !!! test_save_fig_creates_png_file")

class cs3430_s26_hw_3_prob_3_batch_edge_on_real_images_uts(unittest.TestCase):
    """
    Batch test that loads real images from imgs/ and saves binary edge maps.

    For each image file imgs/<name>.<ext>, we save:

        imgs/<name>_edges.png

    This test is intentionally "visual" in nature: you should inspect
    the resulting *_edges.png files. Some images my take a while.
    """

    @classmethod
    def setUpClass(cls) -> None:
        print("\n============================================================")
        print("CS3430 S26 HW3 Problem 3 Unit Tests: Batch Edge Maps on imgs/")
        print("============================================================")

        cls.img_paths = [
            "imgs/BirdOrnament.jpg",
            "imgs/EdgeImage_1.jpg",
            "imgs/EdgeImage_2.jpg",
            "imgs/EdgeImage_3.jpg",
            "imgs/EdgeImage_4.jpg",
            "imgs/EdgeImage_5.jpg",
            "imgs/EdgeImage_6.jpg",
            "imgs/EdgeImage_7.jpg", 
            "imgs/Elephant.jpg",
            "imgs/hive_1.png",
            "imgs/hive_2.png",
            "imgs/june.jpg",
            "imgs/lunch.jpg", ### This is a BIG image!!!
            "imgs/nt_01.jpg",
            "imgs/road_1.png",
            "imgs/road_2.png",
            "imgs/road_3.png",
            "imgs/road_4.png",
            "imgs/sudoku.jpg"
        ]

    def test_batch_edges_on_imgs_directory(self) -> None:
        print("\nSTART: test_batch_edges_on_imgs_directory")

        # Optional: lower threshold makes edges show up more strongly
        # for some lower-contrast photos.
        T = 100.0

        for path in self.img_paths:
            print("\n------------------------------------------------------------")
            print("Processing:", path)

            self.assertTrue(os.path.exists(path), f"Missing file: {path}")

            # 1) Load grayscale
            I = edge.load_grayscale_image(path)

            print("  I.shape =", I.shape)
            print("  I.min/max =", float(np.min(I)), float(np.max(I)))

            # 2) Compute gradients
            Gx = edge.sobel_kx_response(I)
            Gy = edge.sobel_ky_response(I)

            # 3) Magnitude + threshold into 0/255 edge map
            Gmag, Emag = edge.binary_edge_map_from_gradmag(Gx, Gy, T=T)

            print("  |G| min/max =", float(np.min(Gmag)), float(np.max(Gmag)))
            print("  edges (255 count) =", int(np.sum(Emag == 255.0)))

            # 4) Build output name: always save as PNG
            base, _ = os.path.splitext(path)
            out_path = base + "_edges.png"

            # 5) Save figure
            fig = plt.figure()
            plt.title(f"Edges: {os.path.basename(path)} (T={T})")
            plt.imshow(Emag, cmap="gray", vmin=0, vmax=255)
            plt.axis("off")
            plt.tight_layout()

            edge.save_fig(fig, out_path)
            plt.close(fig)

            # 6) Verify output exists and is non-empty
            self.assertTrue(os.path.exists(out_path), f"Output not created: {out_path}")

            file_size = os.path.getsize(out_path)
            print("  saved:", out_path)
            print("  file size =", file_size, "bytes")

            self.assertTrue(file_size > 0)

        print("\nPASS !!! test_batch_edges_on_imgs_directory")

if __name__ == "__main__":
    unittest.main()
