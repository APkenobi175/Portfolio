import javax.swing.*;
import java.io.*;
import java.awt.*;
import java.awt.event.*;
import java.lang.reflect.*;

public class FloodMain {
    private Display display;
    private JComboBox<File> fileSelector;
    private JFrame window;
    private JTextField heightSelection;
    private JTextField showRange;
    private JLabel statusLine;
    private JPanel controlPanel;
    private File lastFile = null;
    private Terrain terrain = null;


    /* Makes the drop-down file selector. */
    private JComboBox<File> makeFileSelector() {
        var result = new JComboBox<File>();
        result.addItem(new File("World1.txt"));
        result.addItem(new File("World2.txt"));
        result.addItem(new File("World3.txt"));
        result.addItem(new File("World1b.txt"));
        result.addItem(new File("World2b.txt"));
        result.addItem(new File("World3b.txt"));
        result.addItem(new File("CraterLake.txt"));
        result.addItem(new File("NewYorkCity.txt"));
        result.addItem(new File("Senegal.txt"));
        result.addItem(new File("SouthBayArea.txt"));
        result.addItem(new File("RioDeJaneiro.txt"));
        return result;
    }

    private JButton makeLoadButton() {
        var result = new JButton("Load");
        result.addActionListener((ActionEvent e) -> {
            heightSelection.setText("0");
            runSimulation((File) fileSelector.getSelectedItem(), 4);
        });
        return result;
    }

    private JButton makeShowFloodingButton() {
        var result = new JButton("ShowFlooding");
        result.addActionListener((ActionEvent e) -> {
            runSimulation((File) fileSelector.getSelectedItem(), 0);
        });
        return result;
    }

    private JButton makeShowFloodingRecursiveButton() {
        var result = new JButton("RecursiveFlooding");
        result.addActionListener((ActionEvent e) -> {
            runSimulation((File) fileSelector.getSelectedItem(), 1);
        });
        return result;
    }
/*  Will be used in Program 3
    private JButton makeWhenFloodButton() {
        var result = new JButton("When Flood!");
        result.addActionListener((ActionEvent e) -> {

            runSimulation((File) fileSelector.getSelectedItem(), 2);
        });
        return result;
    }

    private JButton makeWhenFloodButtonExhaustive() {
        var result = new JButton("When Flood Exhaustive!");
        result.addActionListener((ActionEvent e) -> {
            runSimulation((File) fileSelector.getSelectedItem(), 3);
        });
        return result;
    }*/

    /* Builds the control panel. */
    private JPanel makeControlPanel() {
        JPanel container = new JPanel();
        container.setLayout(new GridLayout(2, 1));

        /* The main control panel. */
        JPanel panel = new JPanel();
        panel.setLayout(new FlowLayout());

        fileSelector = makeFileSelector();
        panel.add(fileSelector);

        var loadButton = makeLoadButton();
        panel.add(loadButton);

        /* Spacer. */
        panel.add(new JLabel("          "));

        heightSelection = new JTextField("0", 6);
        panel.add(new JLabel("Water Height: "));
        panel.add(heightSelection);
        showRange    = new JTextField("", 6);
        showRange.setBackground(Color.YELLOW);
        panel.add(showRange);

        var showFlooding = makeShowFloodingButton();
        panel.add(showFlooding);

        var showFloodingR = makeShowFloodingRecursiveButton();
        panel.add(showFloodingR);
//  Will be used in program 3
//        var whenFloodButton = makeWhenFloodButton();
//        panel.add(whenFloodButton);
//        var whenFloodButtonExhaustive = makeWhenFloodButtonExhaustive();
//        panel.add(whenFloodButtonExhaustive);
        container.add(panel);

        /* The status line. */
        JPanel statusBox = new JPanel();
        statusLine = new JLabel("");
        statusBox.add(statusLine);
        container.add(statusBox);

        return container;
    }

    private FloodMain() {
        /* Main window. */
        window = new JFrame();
        window.setLayout(new BorderLayout());
        window.setTitle("Terrain Map");
        window.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        /* Main display. */
        display = new Display();
        window.add(display, BorderLayout.CENTER);

        /* Control panel. */
        controlPanel = makeControlPanel();
        window.add(controlPanel, BorderLayout.SOUTH);

        window.pack();
        window.setVisible(true);
    }

    private void setStatusLine(final String text) {
        SwingUtilities.invokeLater(() -> {
            statusLine.setText(text);
        });
    }

    /* Disables/enables all components in the given container.
     */
    private void setEnabled(Container container, boolean enabled) {
        Component[] components = container.getComponents();
        for (Component component : components) {
            component.setEnabled(enabled);
            if (component instanceof Container) {
                setEnabled((Container) component, enabled);
            }
        }
    }

    private void runSimulation(File terrainFile, int action) {
        int waterHeight;
        try {
            waterHeight = Integer.parseInt(heightSelection.getText());
        } catch (NumberFormatException e) {
            JOptionPane.showMessageDialog(window, "Please enter a number for the water height.", "Water Height", JOptionPane.ERROR_MESSAGE);
            return;
        }

        setEnabled(controlPanel, false);
        new Thread() {
            public void run() {
                Flooding f;
                boolean[][] flooded;
                try {

                    setStatusLine("Loading the Terrain...");
                    terrain = TerrainLoader.loadTerrain(terrainFile);
                    display.setTerrain(terrain);
                    showRange.setText( String.valueOf(terrain.min) + ":" + String.valueOf(terrain.max));
                    f = new Flooding(terrain.heights, terrain.waterSources, waterHeight);
                    switch (action) {
                        case 0:
                            window.setTitle("Show Flooding Breadth First " );
                            flooded = f.markFlooded();
                            display.setFlooding(flooded);
                            display.repaint();
                            break;
                        case 1:
                            window.setTitle("Show FLooding Recursive ");
                            flooded = f.markFloodedR();
                            display.setFlooding(flooded);
                            display.repaint();
                            break;
/*      Will be used in program 3
                        case 2:
                            window.setTitle("When Flood ");
                            var whenFlood = f.whenFlood();
                            terrain.heights = whenFlood;
                            display.setTerrain(terrain );
                            display.repaint();
                            break;
                        case 3:
                            window.setTitle("When Flood Exhaustive ");
                            var whenFloodE = f.whenFloodExhaustive();
                            terrain.heights = whenFloodE;
                            display.setTerrain(terrain);
                            display.repaint();
                            break;*/
                        case 4:
                            window.setTitle("Terrain");
                            display.repaint();
                            break;
                        default:
                            break;
                    }

                    try {
                        SwingUtilities.invokeAndWait(() -> display.repaint());
                    } catch (InterruptedException e) {
                        SwingUtilities.invokeLater(() -> display.repaint());
                    } catch (InvocationTargetException e) {
                        throw new IOException(e);
                    }
                    setStatusLine("");
                } catch (IOException e) {
                    setStatusLine("Error: " + e.getMessage());
                    throw new RuntimeException(e);
                } finally {
                    SwingUtilities.invokeLater(() -> {
                        setEnabled(controlPanel, true);
                    });
                }
            }
        }.start();
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(
                () -> {
                    new FloodMain();
                });

    }
}

