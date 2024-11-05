// PRIORITY IS DURATION - DEADLINE IF TIED
public class TaskByDuration extends Task implements Comparable<Task> {

    public TaskByDuration(int ID, int start, int deadline, int duration) {
        super(ID, start, deadline, duration);
    }

    @Override
    public int compareTo(Task other) {
        if (this.duration == other.duration) {
            return Integer.compare(this.deadline, other.deadline);
        }
        return Integer.compare(this.duration, other.duration);
    }
}
