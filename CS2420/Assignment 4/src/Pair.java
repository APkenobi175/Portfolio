public class Pair<T1,T2> {
    private T1 first;
    private T2 second;

    public T1 get1(){
        return this.first;
    }
    public T2 get2(){
        return this.second;
    }
    Pair( T1 a, T2 b){
        this.first = a;
        this.second = b;
    }

    public String toString(){
        return  "(" + first +"," +second +")";
    }

    public static void main(String args[]){
        Pair<String,Integer> class1 = new Pair<>( "CS", 2420);
        Pair<String,Integer> class2 = new Pair<>( "Math", 2610);
        System.out.println("I am taking " + class1 + class2);
    }
}