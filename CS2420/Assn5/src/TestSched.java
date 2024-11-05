import java.io.File;
import java.io.FileNotFoundException;
import java.util.*;

public class TestSched {


    public static void readTasks(String filename, ArrayList<Task> taskX, ArrayList<Task> taskY, ArrayList<Task> taskZ) {
        int idCounter = 1; // Start ID at 1 because if you don't the program will get confused because its asking for 4 parameters but there is only 3 in each file

        try (Scanner scanner = new Scanner(new File(filename))) {
            while (scanner.hasNextLine()) {
                String[] parts = scanner.nextLine().trim().split("\\s+"); // Split by any whitespace (spaces, tabs, etc.)
                if (parts.length == 3) {
                    int start = Integer.parseInt(parts[0]);
                    int deadline = Integer.parseInt(parts[1]);
                    int duration = Integer.parseInt(parts[2]);

                    // Create tasks ID start time, deadline, and duration
                    TaskByDeadline taskDeadline = new TaskByDeadline(idCounter, start, deadline, duration);
                    TaskByStartTime taskStartTime = new TaskByStartTime(idCounter, start, deadline, duration);
                    TaskByDuration taskDuration = new TaskByDuration(idCounter, start, deadline, duration);

                    // Add the task to each list
                    taskX.add(taskDeadline);
                    taskY.add(taskStartTime);
                    taskZ.add(taskDuration);

                    idCounter++; // Increment the ID for the next task
                }
            }
        } catch (FileNotFoundException e) {
            System.out.println("File not found: " + filename);
        }
    }






    public static void main(String args[]) throws Exception {
        Scheduler s = new Scheduler();
        String [] files = {"tasksetA.txt", "tasksetB.txt", "tasksetC.txt", "tasksetD.txt", "tasksetE.txt"};
        for (String f : files) {
            ArrayList<Task> versionX = new ArrayList();    // elements are TaskByDeadline
            ArrayList<Task> versionY = new ArrayList();    // elements are TaskByStartTime
            ArrayList<Task> versionZ = new ArrayList();    // elements are TaskByDuration
            readTasks(f, versionX,versionY,versionZ);
            Comparator<Task> deadlineComparator = Comparator.comparingInt(Task::getDeadline);
            s.makeSchedule("Deadline " + f, versionX, deadlineComparator);

            Comparator<Task> startTimeComparator = Comparator.comparingInt(Task::getStart)
                    .thenComparingInt(Task::getDeadline);
            s.makeSchedule("Start-time, deadline if tied " + f, versionY, startTimeComparator);

            Comparator<Task> durationComparator = Comparator.comparingInt(Task::getDuration)
                    .thenComparingInt(Task::getDeadline);
            s.makeSchedule("Duration, deadline if tied " + f, versionZ, durationComparator);
        }

    }
}
