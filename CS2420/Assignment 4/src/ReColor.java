import javax.imageio.ImageIO;
import java.awt.*;
import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.Buffer;
import java.util.ArrayList;
import java.util.Comparator;

public class ReColor {
    BufferedImage img;
    String imageName;
    String redImageName;
    int cube;
    int height = 0;
    int width = 0;
    int colorLimit = 0;
    HashTable<ColorMap> hashTable = new HashTable<>();

    /**
     * Set up the ReColor Class
     * @param filename  File containing the original image
     * @param cube Size of cube for which will accumulate colors
     * @param colorLimit
     */
    ReColor(String filename, int cube, int colorLimit) {
        img = null;
        this.cube = cube;
        this.colorLimit = colorLimit;
        File f;
        String[] p = filename.split("\\.");
        imageName = p[0] + colorLimit + "." + p[1];
        redImageName = p[0] + "Red." + p[1];
        try {
            f = new File(
                    filename);
            img = ImageIO.read(f);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        width = img.getWidth();
        height = img.getHeight();
    }

    /**
     * Process image to extract colors and populate hash table
     */
    public void grabColors() {
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int pixel = img.getRGB(x, y);

                // Extract the ARGB components from the pixel
                int alpha = (pixel >> 24) & 0xff;
                int red = (pixel >> 16) & 0xff;
                int green = (pixel >> 8) & 0xff;
                int blue = pixel & 0xff;

                // Create a ColorMap for the current pixel
                ColorMap colorMap = new ColorMap(alpha, red, green, blue, cube);

                // Check if the ColorMap already exists in the hash table
                ColorMap existing = hashTable.find(colorMap);
                if (existing == null) {
                    hashTable.insert(colorMap);
                } else {
                    existing.occurCt++;
                }
            }
        }
        // Print the total colors and porbe count
        System.out.println("Number of Colors: " + hashTable.size());
    }

    public void printColorTable(ArrayList<ColorMap> topColors) {
        for (int i = 0; i < topColors.size(); i++) {
            ColorMap color = topColors.get(i);
            System.out.printf("ColorTable [%d] (%d) %d %d %d\n", i, color.occurCt, color.red * cube, color.green * cube, color.blue * cube);
        }
    }


    /**
     * Get the top popular colors
     * @param topN Number of top colors to retrieve.
     * @return ArrayList of the most popular colors
     */
    public ArrayList<ColorMap> getTopColors(int topN) {
        ArrayList<ColorMap> allColors = hashTable.getAll();
        allColors.sort(Comparator.reverseOrder());  // Sort by occurCt (descending)
        return new ArrayList<>(allColors.subList(0, Math.min(topN, allColors.size())));
    }

    /*
    Generate new image
     */
    public void generateImage(ArrayList<ColorMap> topColors) {
        BufferedImage newImg = new BufferedImage(width, height, img.getType());

        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int pixel = img.getRGB(x, y);

                // Extract ARGB components from the pixel

                int alpha = (pixel >> 24) & 0xff;
                int red = (pixel >> 16) & 0xff;
                int green = (pixel >> 8) & 0xff;
                int blue = pixel & 0xff;


                // Create a ColorMap for current pixel
                ColorMap colorMap = new ColorMap(alpha, red, green, blue, cube);

                // Find the closest color from the top with Euclidean distance

                ColorMap closestColor = findClosestColor(colorMap, topColors);

                // Set the pixel to the new color

                Color newColor = closestColor.getRepresentativeColor();
                int newPixel = (alpha << 24) | (newColor.getRed() << 16) |
                        (newColor.getGreen() << 8) | newColor.getBlue();
                newImg.setRGB(x, y, newPixel);
            }
        }

        try {

            File output = new File(imageName);
            ImageIO.write(newImg, "png", output);
        }
        catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

    private ColorMap findClosestColor(ColorMap target, ArrayList<ColorMap> topColors) {
        ColorMap closest = topColors.get(0);
        double minDist = Double.MAX_VALUE;

        for (ColorMap color : topColors){
            double distance = calculateDistance(target, color);
            if (distance < minDist){
                minDist = distance;
                closest = color;
            }
        }
        return closest;
    }

    /**
     * Calculate the Euclidean distance between two colormaps
     */
    private double calculateDistance(ColorMap c1, ColorMap c2) {
        int dr = c1.red - c2.red;
        int dg = c1.green - c2.green;
        int db = c1.blue - c2.blue;
        return Math.sqrt(dr * dr + dg * dg + db * db);
    }

    public void makeRed() {
        BufferedImage img2 = new BufferedImage(width, height, img.getType());
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                int p = img.getRGB(x, y);
                int alpha = (p >> 24) & 0xff; //transparency measure
                int r = (p >> 16) & 0xff;  //red
                int g = (p >> 8) & 0xff;   //green
                int b = p & 0xff;          //blue
                // set new RGB keeping the alpha and the color wanted. Setting others to 0.
                p = (alpha << 24) | (r << 16) | (0 << 8) | 0;//Show red
                img2.setRGB(x, y, p);
            }
        }
        try {
            File f = new File(
                    redImageName);
            ImageIO.write(img2, "png", f);
        } catch (Exception e) {
            System.out.println(e);
        }
    }



    public static void main(String[] args) {
        String[] files = {"chart.png", "bird.png", "butterfly.png", "cat.png", "dice.png", "flowers.png"};
        int[] colorMax = {5, 100, 100, 25, 6, 40};
        for (int i = 0; i < files.length; i++) {
            System.out.println("File name: " + files[i]);
            ReColor r = new ReColor(files[i], 6, colorMax[i]);
            // Extract colors and print statistics
            r.hashTable.setUseBetterHash(false);
            r.grabColors();
            System.out.print("Average probes with bad hash: ");
            r.hashTable.printAverageProbes();
            System.out.println();
            // Get top colors and print the ColorTable if colorLimit <= 25
            ArrayList<ColorMap> topColors = r.getTopColors(r.colorLimit);
            if (r.colorLimit <= 25) {
                r.printColorTable(topColors);
            }
            // print the number of hash table entries
            System.out.println("Hash Table Entries: " + r.hashTable.size());


            // Generate and save the new image
            r.generateImage(topColors);

            // Now reset and use the new hash code
            System.out.println("Using Better Hash Code:");
            r.hashTable = new HashTable<>();  // Clear the hash table
            r.hashTable.setUseBetterHash(true);  // Use mod hash code
            r.grabColors();
            System.out.print("Average probes with better hash: ");
            r.hashTable.printAverageProbes();
            System.out.println();
            System.out.println("----------");
    }
}}
