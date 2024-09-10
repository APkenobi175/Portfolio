public class pattern {
    public static void pattern(int center){
        if(center<=0) return;
        pattern(center-1);
        System.out.println(center);
        pattern(center-1);
        }

}