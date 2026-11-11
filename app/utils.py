from passlib.context import CryptContext


pwd_context = CryptContext(schemes = ["bcrypt"],deprecated="auto")
# telling what hashing algorithm we are using for hashing password 


def Hash(password:str):
  # HASHING THE PASSWORD
  return pwd_context.hash(password)

def verify_password(plain_password , hashed_password): # this verify methodo of pwd context just verifies the password 
  return pwd_context.verify(plain_password , hashed_password)