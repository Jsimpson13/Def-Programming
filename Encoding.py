class Encoding:
    @staticmethod
    def Encrypt(s, key)->str:
        encoded_bytes = [(ord(char) + i + key) % 255 for i, char in enumerate(s)]
        char_array = [chr(byte) for byte in encoded_bytes]
        enc_s = Encoding.ENCS_TRANS(char_array)
        return enc_s
    @staticmethod
    def ENCS_TRANS(charArray) -> str:
        #splits char array in half 
        middle = len(charArray) // 2
        firstHalf = charArray[:middle]
        secondHalf = charArray[middle:]
        
        #reverses the two halves
        firstHalf.reverse()
        secondHalf.reverse()

        #joins the two reversed halves
        return ''.join(firstHalf) + ''.join(secondHalf)

