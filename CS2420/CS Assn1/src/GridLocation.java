public  class GridLocation {
    public final int row;
    public final int col;

    public GridLocation(int row, int col) {
        this.row = row;
        this.col = col;

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

}
