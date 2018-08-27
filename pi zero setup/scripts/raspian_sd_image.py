from run_commands import run, cd, exists, isdir, _expand



print('moving to your ~/Downloads directory')
cd('~/Downloads')

raspbian_dir = 'raspbian_download_dir'

print(f"Checking on {raspbian_dir} directory.")
if not exists(raspbian_dir):
    print(f"It dosn't exist. Creating {raspbian_dir} directory.")
    run(f'mkdir {raspbian_dir}')
elif exists(raspbian_dir) and not isdir(raspbian_dir):
    print(f'"~/Downloads/{raspbian_dir}" exists but is not a directory. I\'m confused. exiting')
    exit(1)

print(f"The {raspbian_dir} exists. Moving into that directory.")
cd(raspbian_dir)

download_filename = "raspbian_lite_latest"
print(f"Checking on download file: {download_filename}")
if not exists(download_filename):
    print("It doesn't exist. Downloading ...")
    run('wget https://downloads.raspberrypi.org/raspbian_lite_latest', capture_output=False)
else:
    print("It exists.")

print("Checking on the extracted file.")
extracted_file = "*raspbian*.img"
if not exists(extracted_file):
    print("it doesn't exist. extracting.")
    run(f'unzip {download_filename}')
else:
    print('It exists.')

print("Find SD card.")
input('Remove it from the computer and hit enter.')
results1 = run('lsblk | grep disk')

not_the_SD_card = []
for line in results1.stdout.split('\n'):
    split_line = line.strip().split()
    if len(split_line) > 0:
        not_the_SD_card.append(line.split()[0])
print("\nCurrent Disks:")
print(", ".join(not_the_SD_card))


input('Please insert the SD card and hit enter.')
results2 = run('lsblk | grep disk')

has_the_SD_card = []
for line in results2.stdout.split('\n'):
    split_line = line.strip().split()
    if len(split_line) > 0:
        has_the_SD_card.append(line.split()[0])
print("\nCurrent Disks:")
print(", ".join(has_the_SD_card))

the_SD_card = []
for disk in has_the_SD_card:
    if disk not in not_the_SD_card:
        the_SD_card.append(disk)
print("\nNew Disks:")
print(", ".join(the_SD_card))

if len(the_SD_card) < 1:
    print('No SD card found.')
    exit(1)
elif len(the_SD_card) > 1:
    print("Too many, I'm confused.")
    exit(1)
else:
    the_SD_card = the_SD_card[0]
print(f"It apears that the SD card is {the_SD_card}")

write_the_image_to_the_SD_card_command = _expand(f"sudo ddrescue -D --force *-raspbian-*.img /dev/{the_SD_card}")
print('Do really want to run this command:')
print(write_the_image_to_the_SD_card_command)
response = input("type 'yes' to do so [anything else exits]:")
if response == 'yes':
    run(write_the_image_to_the_SD_card_command, capture_output=False)
else:
    print('okay. Skipping. Bye.')
    exit(1)

exit(0)
