from smb.SMBConnection import SMBConnection
import argparse
import os

def download_file(conn, share_name, remote_file_path, local_file_path):
    try:
        with open(local_file_path, 'wb') as local_file:
            file_attributes, file_size = conn.retrieveFile(share_name, remote_file_path, local_file)
            if file_size > 0:
                print(f"Downloaded: {local_file_path} ({file_size} bytes)")
            else:
                print(f"Warning: Downloaded file '{remote_file_path}' is empty.")
    except Exception as e:
        print(f"Error downloading file '{remote_file_path}': {e}")

def search_and_download_files(ip_address, username, password, keywords, download_dir):
    try:
        conn = SMBConnection(username, password, "my_client", ip_address)
        conn.connect(ip_address, 139)  # Port 139 is the default SMB port

        shares = conn.listShares()
        for share in shares:
            share_name = share.name
            try:
                # Attempt to access the share
                share_files = conn.listPath(share_name, "/")
                print(f"Searching in {share_name} for files with keywords:")
                for keyword in keywords:
                    for file_info in share_files:
                        if keyword.lower() in file_info.filename.lower():
                            print(f"  Found: {file_info.filename} (Keyword: {keyword})")
                            # Retrieve and download the file
                            remote_file_path = f"/{file_info.filename}"
                            local_file_path = os.path.join(download_dir, file_info.filename)
                            download_file(conn, share_name, remote_file_path, local_file_path)

            except Exception as share_error:
                print(f"Error accessing share '{share_name}': Incorrect credentials")

        conn.close()

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and download files from SMB shares")
    parser.add_argument("server_ip", help="Server IP address")
    parser.add_argument("--keywords", nargs="+", default=["document", "report", "invoice", "attention"], help="Keywords to search for")
    parser.add_argument("--download-dir", default="./downloads", help="Directory to save downloaded files")

    args = parser.parse_args()
    
    username = " "  # Replace with your username
    password = " "  # Replace with your password
    server_ip = args.server_ip
    keywords_to_search = args.keywords
    download_directory = os.path.abspath(args.download_dir)

    os.makedirs(download_directory, exist_ok=True)  # Create the download directory if it doesn't exist
    search_and_download_files(server_ip, username, password, keywords_to_search, download_directory)
