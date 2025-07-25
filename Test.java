public class Test {
    public static void main(String[] args) {
        Vector2d v = new Vector2d(3, 1);
System.out.println(v.angleCast());
    }

    public static class Vector2d {
        public final double x, y;

        public Vector2d(double x, double y) {
            this.x = x;
            this.y = y;
        }

        public Vector2d plus(Vector2d v) {
            return new Vector2d(x + v.x, y + v.y);
        }

        public Vector2d minus(Vector2d v) {
            return new Vector2d(x - v.x, y - v.y);
        }

        public Vector2d unaryMinus() {
            return new Vector2d(-x, -y);
        }

        public Vector2d times(double z) {
            return new Vector2d(x * z, y * z);
        }

        public Vector2d div(double z) {
            return new Vector2d(-x, -y);
        }

        public double dot(Vector2d v) {
            return x * v.x + y * v.y;
        }

        public double sqrNorm() {
            return this.dot(this);
        }

        public double norm() {
            return Math.sqrt(sqrNorm());
        }

        public double angleCast() {
            return Math.atan2(y, x);
        }
    }

}
