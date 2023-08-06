import binascii
import os
import shutil
import socket
import subprocess

import psutil
import werkzeug.security


def create_pass(password):
    return werkzeug.security.generate_password_hash(password).replace("$", "$$")


def create_new_secret():
    return binascii.hexlify(os.urandom(16)).decode("ascii")


def check_user_and_pass(app, user, password):
    # check if pwhash is used
    admin_users = app.config["ADMIN_USERS"]
    user_info = admin_users.get(user, None)
    if not user_info:
        return False

    admin_pw_hash = user_info["password_hash"]
    admin_pw_hash = admin_pw_hash.replace("$$", "$")

    if admin_pw_hash:
        if werkzeug.security.check_password_hash(admin_pw_hash, password):
            return True
    else:
        # fallback til plaintext
        admin_password = user_info["password"]
        if password == admin_password:
            return True
    return False


def update_usertable(admin_users, config, section):

    prefixes = {}

    for key, val in config.get_dict("webadmin").items():
        if key.startswith("users.") and key.count(".") == 2:
            prefix, attr = key.split(".")[1:3]
            if attr in ("user", "password", "password_hash", "roles"):
                if not prefix in prefixes:
                    prefixes[prefix] = create_usertable_item("", "", "", "")
                if attr == "roles":
                    prefixes[prefix][attr] = set(map(str.strip, val.split(",")))
                else:
                    config.set_hidden_value(section, key)
                    prefixes[prefix][attr] = val

    for user_info in prefixes.values():
        admin_users[user_info["user"]] = user_info

    return admin_users


def create_usertable_item(user, password, password_hash, roles):
    return {
        "user": user,
        "password": password,
        "password_hash": password_hash,
        "roles": set(map(str.strip, roles.split(","))) if roles else set(),
    }


def get_ip_addresses():
    for interfaces in psutil.net_if_addrs().values():
        for interface in interfaces:
            if interface.family == socket.AF_INET:
                yield interface.address


def get_host_names():
    return [socket.gethostname()]


# default cert filenames:
# general
default_pem_file = os.path.join("ssl", "certs", "certificate.pem")
default_key_file = os.path.join("ssl", "private", "certificate.pem.key")
default_der_file = os.path.join("ssl", "certs", "certificate.der")
default_derkey_file = os.path.join("ssl", "private", "certificate.der.key")

# webadmin
default_webadmin_pem_file = os.path.join("ssl", "certs", "webadmin_certificate.pem")
default_webadmin_key_file = os.path.join(
    "ssl", "private", "webadmin_certificate.pem.key"
)
default_webadmin_der_file = os.path.join("ssl", "certs", "webadmin_certificate.der")
default_webadmin_derkey_file = os.path.join(
    "ssl", "private", "webadmin_certificate.der.key"
)

# opcua
default_opcua_pem_file = os.path.join("ssl", "certs", "opcua_certificate.pem")
default_opcua_key_file = os.path.join("ssl", "private", "opcua_certificate.pem.key")
default_opcua_der_file = os.path.join("ssl", "certs", "opcua_certificate.der")
default_opcua_derkey_file = os.path.join("ssl", "private", "opcua_certificate.der.key")
default_opcua_urn = "urn:opcua:server"


def can_generate_certs():
    if shutil.which("openssl") is None:
        return False
    else:
        return True


def generate_overwrite_certificates(
    pem_file,
    key_file,
    der_file,
    derkey_file,
    common_name,
    days=3650,
    opcua_ext=0,
    uri_list=[],
    dns_list=[],
    ip_list=[],
    basicConstraints="",
    keyUsage="",
    extendedKeyUsage="",
):
    cmd_req_pem = [
        "openssl",
        "req",
        "-x509",
        "-sha256",
        "-newkey",
        "rsa:4096",
        "-keyout",
        key_file,
        "-out",
        pem_file,
        "-days",
        str(days),
        "-nodes",
    ]

    cmd_der = ["openssl", "x509", "-outform", "der", "-in", pem_file, "-out", der_file]
    cmd_der_key = [
        "openssl",
        "rsa",
        "-outform",
        "der",
        "-in",
        key_file,
        "-out",
        derkey_file,
    ]

    os.makedirs(os.path.join("ssl", "certs"), exist_ok=True)
    os.makedirs(os.path.join("ssl", "private"), exist_ok=True)

    if common_name:
        cmd_req_pem.append("-subj")
        cmd_req_pem.append("/CN={:s}".format(common_name))
    else:
        cmd_req_pem.append("-batch")

    if opcua_ext:
        cmd_req_pem.append("-addext")
        if basicConstraints:
            cmd_req_pem.append("basicConstraints = {}".format(basicConstraints))
        else:
            cmd_req_pem.append("basicConstraints = CA:TRUE")
        cmd_req_pem.append("-addext")
        subjectAltName = []
        for n, uri in enumerate(uri_list, 1):
            if uri:
                subjectAltName.append("URI.{}:{}".format(n, uri))

        for n, dns in enumerate(dns_list, 1):
            if dns:
                subjectAltName.append("DNS.{}:{}".format(n, dns))

        for n, ip in enumerate(ip_list, 1):
            if ip:
                subjectAltName.append("IP.{}:{}".format(n, ip))
        cmd_req_pem.append("subjectAltName = " + ", ".join(subjectAltName))

        cmd_req_pem.append("-addext")
        if keyUsage:
            cmd_req_pem.append("keyUsage = {}".format(keyUsage))
        else:
            cmd_req_pem.append(
                "keyUsage = critical, cRLSign, digitalSignature, keyCertSign"
            )
        cmd_req_pem.append("-addext")
        if extendedKeyUsage:
            cmd_req_pem.append("extendedKeyUsage = {}".format(extendedKeyUsage))
        else:
            cmd_req_pem.append("extendedKeyUsage = critical, serverAuth")

    res = subprocess.run(cmd_req_pem, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        return "{}\n{}".format(res.stdout, res.stderr)

    res = subprocess.run(cmd_der, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        return "{}\n{}".format(res.stdout, res.stderr)

    res = subprocess.run(cmd_der_key, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        return "{}\n{}".format(res.stdout, res.stderr)

    return ""
