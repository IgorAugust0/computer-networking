#include <iostream>
#include <bitset>
#include <sstream>
#include <vector>

using namespace std;

bitset<16> getChecksum(vector<bitset<16>> words) {
    bitset<32> sum = 0;
    for (auto word : words) {
        sum += (bitset<32>)word.to_ulong();
        while (sum.to_ulong() >> 16) {
            sum = (sum.to_ulong() & 0xFFFF) + (sum.to_ulong() >> 16);
        }
    }
    bitset<16> checksum = ~((bitset<16>)sum.to_ulong());
    return checksum;
}

int main() {
    string input;
    vector<bitset<16>> words;
    int numWords;
    cout << "How many words do you want to input? ";
    cin >> numWords;
    for (int i = 0; i < numWords; i++) {
        cout << "Insert word " << i+1 << ": ";
        cin >> input;
        bitset<16> word;
        if (input.find('.') != string::npos) {
            input.erase(remove(input.begin(), input.end(), '.'), input.end());
            stringstream(input) >> word;
        } else {
            stringstream(input) >> word;
        }
        words.push_back(word);
    }
    bitset<16> sum = words[0];
    for (int i = 1; i < words.size(); i++) {
        sum ^= words[i];
    }
    bitset<16> checksum = getChecksum(words);
    string sumStr = sum.to_string();
    string checksumStr = checksum.to_string();
    sumStr.insert(4, ".");
    sumStr.insert(9, ".");
    checksumStr.insert(4, ".");
    checksumStr.insert(9, ".");
    cout << "Sum of all words: " << sumStr << endl;
    cout << "Checksum: " << checksumStr << endl;
    return 0;
}