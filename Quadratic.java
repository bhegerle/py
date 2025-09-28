public class Quadratic {
    public static void main(String[] args) {
        Quadratic q = Quadratic.fit(
                1, 2,
                1.3, 1.3,
                4, 8);
        System.out.printf("%s\n", q);
    }

    public Quadratic(double a, double b, double c) {
        this.a = a;
        this.b = b;
        this.c = c;
    }

    public final double a, b, c;

    public static Quadratic fit(
            double x1, double y1,
            double x2, double y2,
            double x3, double y3) {
        // use lagrange interpolation formula
        double a = ((y1 - y2) * (x2 - x3) - (y2 - y3) * (x1 - x2))
                / ((x1 + x2) * (x1 - x2) * (x2 - x3) - (x2 + x3) * (x2 - x3) * (x1 - x2));
        double b = (y2 - y1) / (x2 - x1) - a * (x1 + x2);
        double c = y1 - a * x1 * x1 - b * x1;
        return new Quadratic(a, b, c);
    }

    @Override
    public String toString() {
        return String.format("%.15f x**2 + %.15f x + %.15f", a, b, c);
    }
}
