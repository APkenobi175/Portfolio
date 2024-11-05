import java.util.Comparator;
import java.util.List;
import java.util.HashSet;
import java.util.Set;

public class Scheduler {
    private LeftistHeap<Task> taskQueue;
    private List<Task> tasks;
    private int currentTime = 0;
    private int totalMinutesLate = 0;
    private int lateTasksCount = 0;
    private Set<Task> addedTasks = new HashSet<>();

    public Scheduler() {
        this.taskQueue = new LeftistHeap<>();
    }

    public void makeSchedule(String label, List<Task> tasks, Comparator<Task> comparator) throws Exception {
        System.out.println("Priority is " + label);
        this.tasks = tasks;
        this.currentTime = 0;
        this.totalMinutesLate = 0;
        this.lateTasksCount = 0;
        this.addedTasks.clear();

        // Initial insertion of tasks that start at time 0
        for (Task task : tasks) {
            if (task.getStart() == currentTime) {
                taskQueue.insert(task);
                addedTasks.add(task);
            }
        }

        run();
    }

    private void run() {
        while (!taskQueue.isEmpty() || hasPendingTasks()) {
            if (taskQueue.isEmpty()) {
                // Increment time if nothing is in the queue and we have pending tasks
                currentTime++;
                for (Task t : tasks) {
                    if (t.getStart() == currentTime && !addedTasks.contains(t)) {
                        taskQueue.insert(t);
                        addedTasks.add(t);
                    }
                }
                continue;
            }

            Task task;
            try {
                task = taskQueue.deleteMin();
            } catch (Exception e) {
                System.out.println("Error retrieving task from queue: " + e.getMessage());
                break;
            }

            // Process task for one unit of time
            task.duration--;
            currentTime++;

            if (task.duration == 0) {
                if (currentTime > task.getDeadline()) {
                    int minutesLate = currentTime - task.getDeadline();
                    System.out.println("Time: " + currentTime + " Task " + task.getID() + " ** Late " + minutesLate);
                    lateTasksCount++;
                    totalMinutesLate += minutesLate;
                } else {
                    System.out.println("Time: " + currentTime + " Task " + task.getID() + " **");
                }
            } else {
                System.out.println("Time: " + currentTime + " Task " + task.getID());
                taskQueue.insert(task);
            }

            // Add new tasks to queue at their start time
            for (Task t : tasks) {
                if (t.getStart() == currentTime && !addedTasks.contains(t)) {
                    taskQueue.insert(t);
                    addedTasks.add(t);
                }
            }
        }

        // Print summary pls
        System.out.println("Tasks late " + lateTasksCount + " total Late " + totalMinutesLate);
    }



// do we have pending tasks?

    private boolean hasPendingTasks() {
        for (Task task : tasks) {
            if (task.getStart() >= currentTime) {
                return true;
            }
        }
        return false;
    }
}
