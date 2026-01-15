from werkzeug.security import generate_password_hash, check_password_hash

pw = input("entrer mpd: ")

print(generate_password_hash(pw, method='pbkdf2:sha256'))