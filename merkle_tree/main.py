from hashlib import sha256

def hasha(str): # sha256
    return sha256(str).digest()

def split(list_: list, chunk_size: int):
    # split a list in N lists of lenght = chunk_size
    for i in range(0, len(list_), chunk_size):
        yield list_[i:i + chunk_size]

def merkleTree(items: list[str]) -> str:
    # calc the merkle root of a list
    hash_list = [hasha(item) for item in items]
    merkle = {0: hash_list}
    n = 0

    # loop until the merkle root is found
    # the root is one single hash 
    # https://en.wikipedia.org/wiki/Merkle_tree
    while(len(merkle[n]) > 1): 

        # if there are an even number of leaf/node
        # duplicate the last one
        if len(merkle[n]) % 2 == 1:
            merkle[n].append(merkle[n][-1])

        # split the list into n list of len() = 2
        merkle[n] = list(split(list_=merkle[n], chunk_size=2))

        # add the next layer of the tree
        # concatenate 2 element and perform an hash
        merkle[n+1] = [hasha(a+b) for (a,b) in merkle[n]]

        n +=1
    
    # return merkle # return the entire merkle tree
    return merkle[n][0].hex() # return the merkle root

if __name__ == '__main__':
    item = [b'A',b'B',b'C',b'D', b'E', b'F', b'G']
    merkle_root = merkleTree(item)

    print(f'{merkle_root=}')

