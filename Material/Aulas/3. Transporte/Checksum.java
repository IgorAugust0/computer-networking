import java.util.ArrayList;
import java.util.Scanner;

public class Checksum {
    public static short getChecksum(ArrayList<Short> words) {
        int sum = 0;
        for (short word : words) {
            sum += word;
            while ((sum & 0xFFFF0000) != 0) {
                sum = (sum & 0xFFFF) + (sum >> 16);
            }
        }
        return (short)~sum;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        ArrayList<Short> words = new ArrayList<>();
        System.out.print("How many words do you want to input? ");
        int numWords = scanner.nextInt();
        for (int i = 0; i < numWords; i++) {
            System.out.print("Insert word " + (i+1) + ": ");
            short word = scanner.nextShort();
            words.add(word);
        }
        short sum = words.get(0);
        for (int i = 1; i < words.size(); i++) {
            sum ^= words.get(i);
        }
        short checksum = getChecksum(words);
        System.out.println("Sum of all words: " + sum);
        System.out.println("Checksum: " + checksum);
    }
}