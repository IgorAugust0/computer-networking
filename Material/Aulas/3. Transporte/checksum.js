function getChecksum(words) {
    let sum = 0;
    for (let word of words) {
        sum += word;
        while ((sum & 0xFFFF0000) !== 0) {
            sum = (sum & 0xFFFF) + (sum >> 16);
        }
    }
    return ~sum & 0xFFFF;
}

import { createInterface } from 'readline';
const rl = createInterface({
    input: process.stdin,
    output: process.stdout
});

let words = [];
rl.question("How many words do you want to input? ", (numWords) => {
    for (let i = 0; i < parseInt(numWords); i++) {
        rl.question(`Insert word ${i+1}: `, (wordStr) => {
            let word;
            if (wordStr.includes('.')) {
                word = parseInt(wordStr.replace(/\./g, ''), 2);
            } else {
                word = parseInt(wordStr);
            }
            words.push(word);
            if (words.length === parseInt(numWords)) {
                let sum = words[0];
                for (let i = 1; i < words.length; i++) {
                    sum ^= words[i];
                }
                let checksum = getChecksum(words);
                let sumStr = sum.toString(2).padStart(16, '0');
                let checksumStr = checksum.toString(2).padStart(16, '0');
                sumStr = `${sumStr.slice(0, 4)}.${sumStr.slice(4, 8)}.${sumStr.slice(8, 12)}.${sumStr.slice(12)}`;
                checksumStr = `${checksumStr.slice(0, 4)}.${checksumStr.slice(4, 8)}.${checksumStr.slice(8, 12)}.${checksumStr.slice(12)}`;
                console.log(`Sum of all words: ${sumStr}`);
                console.log(`Checksum: ${checksumStr}`);
                rl.close();
            }
        });
    }
});