def binary_to_decimal(binary_str):
    return int(binary_str, 2)

def decimal_to_binary(decimal):
    return bin(decimal)[2:].zfill(16)

def ones_complement(binary_str):
    return ''.join(['1' if bit == '0' else '0' for bit in binary_str])

def calculate_checksum(words):
    checksum = '0' * 16
    carry = 0

    # Initialize a variable to keep track of the sum of all words
    sum_of_words = '0' * 16

    for word in words:
        word_decimal = binary_to_decimal(word)
        checksum_decimal = binary_to_decimal(checksum)

        # Step 1: Add word to checksum
        result = word_decimal + checksum_decimal + carry
        carry = result >> 16
        checksum = decimal_to_binary(result & 0xFFFF)

        # Step 2: If there is a carry, add it back to the result
        if carry:
            checksum = decimal_to_binary(binary_to_decimal(checksum) + 1)

        # Update the sum of all words
        sum_of_words = decimal_to_binary(binary_to_decimal(sum_of_words) + word_decimal)

    # Step 3: Take the one's complement of the final sum
    checksum = ones_complement(checksum)

    return checksum, sum_of_words

def main():
    num_words = int(input("Enter the number of 16-bit words: "))
    words = []

    for i in range(num_words):
        while True:
            word_input = input(f"Enter word {i + 1} (16-bit binary without spaces): ")
            word_input = ''.join(word_input.split('.'))  # Remove dots if present
            if len(word_input) != 16:
                print("Invalid input. Please enter a 16-bit binary word.")
                continue

            words.append(word_input)
            break

    checksum, sum_of_words = calculate_checksum(words)

    # Display the sum of all words and the results with periods
    print("\nStep-by-Step Calculation:")
    for i, word in enumerate(words):
        print(f"Step {i + 1}: {word[:4]}.{word[4:8]}.{word[8:12]}.{word[12:]}")
    print(f"Sum of All Words: {sum_of_words[:4]}.{sum_of_words[4:8]}.{sum_of_words[8:12]}.{sum_of_words[12:]}")
    print(f"Final Checksum: {checksum[:4]}.{checksum[4:8]}.{checksum[8:12]}.{checksum[12:]}")

if __name__ == "__main__":
    main()
    
def calculate_checksum(data):
    # Initialize the sum to 0
    checksum = 0

    # Divide the data into 16-bit chunks and add them to the sum
    chunk_sums = []  # To store intermediate sums

    for i in range(0, len(data), 16):
        chunk = data[i:i+16]
        chunk_value = int(chunk.replace(".", ""), 2)  # Remove periods and convert to integer
        checksum += chunk_value

        # Handle any carry
        while checksum > 0xFFFF:
            carry = checksum >> 16
            checksum &= 0xFFFF
            checksum += carry

        chunk_sums.append((chunk, chunk_value))

    # Take the 1's complement of the sum
    checksum = ~checksum & 0xFFFF

    return format(checksum, '016b'), chunk_sums


def verify_checksum(data, received_checksum):
    calculated_checksum, chunk_sums = calculate_checksum(data)

    if calculated_checksum == received_checksum:
        return "Checksum is valid. Data was transmitted without errors."
    else:
        return "Checksum is invalid. Data transmission may have errors."

# Function to manually input data chunks
def input_data_chunks():
    chunks = []
    while True:
        chunk = input("Enter a 16-bit data chunk (binary, e.g., 0110011001100000): ")
        # Remove periods if present
        chunk = chunk.replace(".", "")
        if len(chunk) != 16:
            print("Chunk must be 16 bits long. Try again.")
            continue
        chunks.append(chunk)
        another_chunk = input("Do you want to enter another chunk? (yes/no): ")
        if another_chunk.lower() != 'yes':
            break
    return chunks

# Choose between predefined data or manual input
choice = input("Press Enter or type 'yes' (or 'y') to use predefined data, or 'no' (or 'n') to manually enter data: ")

if choice.lower() in ['', 'yes', 'y']:
    # Example data
    data = [
        "0110011001100000",
        "0101010101010101",
        "1000111100001100"
    ]
else:
    # Manually input data chunks
    num_chunks = int(input("Enter the number of 16-bit data chunks you want to input: "))
    data = input_data_chunks()[:num_chunks]

# Calculate the checksum and get intermediate chunk sums
checksum, chunk_sums = calculate_checksum("".join(data))

print("Intermediate Chunk Sums:")
for i, (chunk, value) in enumerate(chunk_sums):
    print(f"Chunk {i + 1}: {chunk} ({value})")

print("\nSum of the First Two Chunks:")
sum_1_2 = chunk_sums[0][1] + chunk_sums[1][1]
print(f"{chunk_sums[0][1]} + {chunk_sums[1][1]} = {sum_1_2} ({format(sum_1_2, '016b')})")

print("\nResult of Adding the Third Chunk:")
sum_1_2_3 = sum_1_2 + chunk_sums[2][1]
print(f"{sum_1_2} + {chunk_sums[2][1]} = {sum_1_2_3} ({format(sum_1_2_3, '016b')})")

print("\nSum Before the Final Checksum (with carry):")
while sum_1_2_3 > 0xFFFF:
    carry = sum_1_2_3 >> 16
    sum_1_2_3 &= 0xFFFF
    sum_1_2_3 += carry
print(format(sum_1_2_3, '016b'))

print("\nFinal Checksum:")
print(checksum)

# Verify the checksum
result = verify_checksum("".join(data), checksum)
print(result)


