public class Dwarf implements Comparable<Dwarf> {
    String data;
    int positionVal;
    static int count = 0;
    public Dwarf(String word) {
        data = word;
        positionVal = count++;
    }
    @Override
    public int compareTo(Dwarf b2) {
        return (this.data.compareTo(b2.data));
    }
    public String toString() {
        return data + positionVal;
    }
}

