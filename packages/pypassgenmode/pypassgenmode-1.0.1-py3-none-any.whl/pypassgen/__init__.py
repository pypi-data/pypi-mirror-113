import random

def genpass(length):
  chars = 'abcdefghyjklmnopqrstuvwxyz'
  chars += chars.upper()
  nums = str(1234567890)
  chars += nums
  special_chars = '!@#$%^&*()_+-'
  chars += special_chars
  result = "".join(random.sample(chars, length))
  return result
