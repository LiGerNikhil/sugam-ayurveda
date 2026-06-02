import qrcode

# The Google Review link
data = "https://g.page/r/CYNt4uNK-BVREAE/review?sc"

# Initialize the QRCode object
qr = qrcode.QRCode(
    version=1,  # Controls the size of the QR Code (1 is the smallest)
    error_correction=qrcode.constants.ERROR_CORRECT_L, # About 7% or less errors can be corrected
    box_size=10, # How many pixels each “box” of the QR code is
    border=4,    # How many boxes thick the border should be
)

# Add data to the QR code
qr.add_data(data)
qr.make(fit=True)

# Create an image from the QR Code instance
img = qr.make_image(fill_color="black", back_color="white")

# Save the image
file_name = "google_review_qr.png"
img.save(file_name)

print(f"QR Code successfully saved as {file_name}")