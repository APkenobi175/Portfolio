
public class TaskX extends Task {
    public TaskX(int ID, int start, int deadline, int duration) {
        super(ID,start,deadline,duration);
    }
    // Prioirity is deadline
    @Override
    public int compareTo(Task t) {
        System.out.println("Using TaskX compareTo");
        return deadline-t.deadline;
    }

}
