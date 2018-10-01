# Check if a string is a letter
def checkIfChar(s):
    for i in range(0, len(s)):
        if s[i] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            return True
        else:
            return False


# Check if a string is a length of 2
def checkLen(s):
    for i in range(0, len(s)):
        if len(s[i]) == 2:
            return False
        else:
            return True


# Encrypt a file related to a key list
def encryptFile(inputFile, keyList):
    outputFile = open("cipher.txt", "w")

    charList = []
    bitList = []
    inputList = inputFile.readlines()
    for i in range(0, len(inputList)):
        for x in range(0, len(inputList[i])):
            charList.append(inputList[i][x: x + 1])

    print("The File is being encrypted...", end="", flush=True)

    for i in range(0, len(charList)):
        bitList.append(str("{0:010b}".format(ord(charList[i]))))

    modNum = len(bitList) % 8
    if len(bitList) % 8 != 0:
        for i in range(0, modNum):
            bitList.append("0000000000")

    numToLoop = len(bitList) / 8
    newBitList = []
    for i in range(0, int(numToLoop)):
        for x in range(0, 10):
            bitStr = int()
            for c in range(i * 8, (i * 8) + 8):
                bitStr = (bitStr << 1) + ord(chr(ord(bitList[c][int(keyList[x])]) - 48))
            newBitList.append(bitStr)

    newChar = []
    for item in newBitList:
        newChar.append(chr(item))

    for i in newChar:
        outputFile.write(i)
    # Something weird I found was that if I tried to use the chr(value) on my windows machine the compiler would give
    # an error saying that the 'charmap' couldn't encode character \x9b in position 0.
    # However on my macOS machine the code executed perfectly. I don't know if this is due to the OS of the machine or
    # if the international ascii table, or unicode as this is what python uses, was not properly installed on the
    # windows machine. - Robert Boutiiler

    print("done")
    outputFile.close()


# Decrypt a file related key list, kl = keyList
def decryptFile(cipFile, kl):
    print("The File is being decrypted...", end="", flush=True)

    decryptFile = open("decrypt.txt", "w")
    cipherText = cipFile.readlines()
    charList = []
    for i in range(0, len(cipherText)):
        for x in range(0, len(cipherText[i])):
            charList.append(cipherText[i][x: x + 1])

    bitList = []
    for i in range(0, len(charList)):
        bitList.append(str("{0:08b}".format(ord(charList[i]))))

    newCharList = []
    numToLoop = int(len(bitList) / 10)

    for i in range(0, numToLoop * 8):
        newCharList.append([])

    intList = []
    zeroToTen = 0
    # Iterate through the bitlist and slice out the cols at the index of keyList
    for i in range(0, numToLoop):
        for x in range(0, 8):
            bitStr = int()
            for c in range(i * 10, (i * 10) + 10):
                if c < 10:
                    bitStr = (bitStr << 1) + ord(chr(ord(bitList[kl[zeroToTen]][x:x + 1]) - 48))
                else:
                    bitStr = (bitStr << 1) + ord(chr(ord(bitList[kl[zeroToTen] + (10 * i)][x:x + 1]) - 48))
                zeroToTen += 1
            zeroToTen = 0
            intList.append(bitStr)

    # Making a null char a space
    for i in range(0, len(intList)):
        if intList[i] == 0:
            intList[i] += 32

    for i in range(0, len(newCharList)):
        newCharList[i] = chr(intList[i])
        decryptFile.write(newCharList[i])

    print("done")
    decryptFile.close()


encOrDec = input("Type E for encrypt or D decrypt: ")
encOrDec = encOrDec.lower()

# need to check if the user enters a e or d
while encOrDec not in "ed":
    print("Enter a E or a D")
    encOrDec = input("Type E for encrypt or D decrypt: ")
    encOrDec = encOrDec.lower()
else:
    if encOrDec == "e":
        inputFile = open("input.txt", "r")

        keyList = []
        key = input("Enter as many two digit numbers as you want: ")
        for i in range(0, 10):
            keyList.append(i)

        while checkIfChar(key) or checkLen(key.split()):
            print("Do not enter a char. Each digit needs to be two long and separated by a space.")
            key = input("Enter as many two digit numbers as you want: ")

        key = key.split(" ")

        for i in range(0, len(key)):
            num = str(key[i])
            leftNum = num[0:1]
            rightNum = num[1:]

            keyList[keyList.index(int(rightNum))] = int(leftNum)
            keyList[keyList.index(int(leftNum))] = int(rightNum)

        encryptFile(inputFile, keyList)
        inputFile.close()
    else:
        # Decryption of the cipher text
        cipherFile = open("cipher.txt", "r")

        keyList = []
        # The key for the encryption is needed
        key = input("Enter the key: ")

        while checkIfChar(key) or checkLen(key.split()):
            print("Do not enter a char. Each digit needs to be two long and separated by a space.")
            key = input("Enter as many two digit numbers as you want: ")

        key = key.split(" ")

        for i in range(0, 10):
            keyList.append(i)

        # Flipping the nums in keyList
        for i in range(0, len(key)):
            num = str(key[i])
            leftNum = num[0:1]
            rightNum = num[1:]

            keyList[keyList.index(int(rightNum))] = int(leftNum)
            keyList[keyList.index(int(leftNum))] = int(rightNum)

        decryptFile(cipherFile, keyList)
        cipherFile.close()
