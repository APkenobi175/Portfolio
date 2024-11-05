// PRIORITY IS START TIME - DEADLINE IF TIED
public class TaskByStartTime extends Task implements Comparable<Task> {

    public TaskByStartTime(int ID, int start, int deadline, int duration) {
        super(ID, start, deadline, duration);
    }

    @Override
    public int compareTo(Task other) {
        if (this.start == other.start) {
            return Integer.compare(this.deadline, other.deadline);
        }
        return Integer.compare(this.start, other.start);
    }
}
