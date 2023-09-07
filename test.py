from smb.SMBConnection import SMBConnection
import sys

if len(sys.argv) ==0:

    print("Usage: python smb_connection.py <server_ip>")

    sys.exit(1)

def access_smb_shares(ip_address, username, password):
    try:
        conn = SMBConnection(username, password, "my_client", ip_address)
        conn.connect(ip_address, 139)  # Port 139 is the default SMB port

        shares = conn.listShares()
        for share in shares:
            share_name = share.name
            try:
                # Attempt to access the share
                share_files = conn.listPath(share_name, "/")
                print(f"Contents of {share_name}:")
                for file_info in share_files:
                    print(f"  {file_info.filename}")

            except Exception as share_error:
                print(f"Error accessing share '{share_name}': Incorrect credentials")

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    username = " "
    password = " "
    server_ip = sys.argv[1]  # Replace with the IP address of your SMB server

    access_smb_shares(server_ip, username, password)
