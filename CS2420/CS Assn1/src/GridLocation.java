public  class GridLocation implements Comparable<GridLocation> {
    public final int row;
    public final int col;
    public int whenFlood;

    public GridLocation(int row, int col) {
        this.row = row;
        this.col = col;
        this.whenFlood = Integer.MAX_VALUE;

    }

    @Override public boolean equals(Object o) {
        if (!(o instanceof GridLocation)) return false;

        var other = (GridLocation) o;
        return row == other.row && col == other.col;
    }

    @Override public String toString() {
        String sb = "{ " + row + ", " + col + " } ";
        return sb;
    }
    // Compare based on whenFlood time
    @Override public int compareTo(GridLocation other) {
        return Integer.compare(this.whenFlood, other.whenFlood);
    }

}
