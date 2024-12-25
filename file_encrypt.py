
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

def encrypt_file(key, in_file_name, out_file_name=None, chunksize=64*1024):
    
    if not out_file_name:
        out_filename = in_file_name + ".enc"
        
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    print("The iv is, ", iv)
    print("The cipher is: ", cipher)
    
    result = iv
    
    with open(in_file_name, 'rb') as infile, open(out_filename,'wb') as outfile:
        outfile.write(iv)
        
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            elif len(chunk) % 16 !=0:
                chunk = pad(chunk,16)
            outfile.write(cipher.encrypt(chunk))
    
    return out_file_name



def decrypt_file(key, encrypted_file_name, out_file_name=None, chunksize=24*1024):
    """_summary_

    Args:
        key (_type_): _description_
        in_file_name (_type_): _description_
        out_file_name (_type_, optional): _description_. Defaults to None.
        chunsize (_type_, optional): _description_. Defaults to 24*1024.

    Returns:
        _type_: _description_
    """
    if not out_file_name:
        out_file_name = os.path.splitext(encrypted_file_name)[0]
    
    with open(encrypted_file_name, 'rb') as infile, open(out_file_name,'wb') as outfile:
        iv = infile.read(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        while True:
            chunk = infile.read(chunksize)
            if len(chunk) == 0:
                break
            outfile.write(cipher.decrypt(chunk))
            
        #outfile.truncate(os.stat(out_file_name).st_size -16) # remove padding
    return out_file_name


key = b'mysecretpassword'
in_file = "csv_file"
enc_file = "csv_file.enc"

#encrypted_file = encrypt_file(key, in_file)

decrypted_file = decrypt_file(key, enc_file, "csv_decrupted")


#print("File encrypted successfully ", encrypted_file)
print("File decrypted successfully ", decrypted_file)