public class Task implements Comparable<Task> {
    public int ID;
    public int start;
    public int deadline;
    public int duration;
    public Task() {
        this.ID = 0;
        this.start = 0;
        this.deadline = 0;
        this.duration = 0;
    }


    public Task(int ID, int start, int deadline, int duration) {
        this.ID = ID;
        this.start = start;
        this.deadline = deadline;
        this.duration = duration;
    }

    public String toString() {
        return "Task " + ID;
    }

    public String toStringL() {
        return "Task " + ID + "[" + start + "-" + deadline + "] " + duration;
    }


    public int compareTo(Task t2) {
        System.out.println("NO compareTo");
        // Supply your own comparator method wait what oh wait I did in taskByDeadline and TaskByDuration and TaskByStartTime
        return 0;
    }
    // Getter for start
    public int getStart() {
        return start;
    }

    // Getter for deadline
    public int getDeadline() {
        return deadline;
    }

    // Getter for duration
    public int getDuration() {
        return duration;
    }
    // Getter for ID
    public int getID(){
        return ID;
    }

}
