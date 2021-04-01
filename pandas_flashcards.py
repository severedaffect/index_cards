import tkinter as tk
import pandas as pd

# -------------------------- GLOBAL Variables ----------------------------------------
TOP_WIDTH = 1000
#TOP_WIDTH = TOP_WIDTH/2
ANS_WIDTH = 800
#ANS_WIDTH = ANS_WIDTH/2

# ------------- Colors -------------
green = "#00ff00"
pastel_green = '#bbfaac'
dark_pastel_green = '#84b079'
lime_green = '#84ff82'
dark_lime = '#60ba5f'
yellow = "#ffff66"
red = "#ff0000"
mulled_blue = "#4d4dff"
dark_blue = "#004080"
light_lavender = '#e3c5fa'
lavender = '#c278fa'
dark_lavender = '#7b4c9e'

# ---------------------- notes
# Makes subject text smaller
# Fix text offset for answers, specifically with RAID answers
#
#
#
#
# ---------------------------------------- Classes ------------------------------------------------
class FlashCards(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        # -------------------------------------- GUI formatting
        self.cell_phone = False
        self.flipped = False

        self.computer_reso = [580, 960]
        self.phone_reso = [290, 480]

        if self.cell_phone:
            _reso = self.phone_reso
        else:
            _reso = self.computer_reso

        self.geometry("{}x{}+0+0".format(_reso[0], _reso[1]))

        # Pandas formatting
        desired_width = 1000
        desired_height = 1000
        pd.set_option('display.width', desired_width)
        pd.set_option('display.max_columns', desired_height)
        pd.set_option('display.max_rows', desired_height)

        # -------------------------------------- Core GUI
        self.reveal = None
        self.first_message = None
        self.second_message = None
        self.hidden_reveal = None
        self.in_depth_label = None

        # ---------------------------------------
        self.first_placement = [0.5, 0.05]

        self.desktop_reveal_placement = [0.3, 0.8]
        self.cell_reveal_placement = [0.2, 0.8]

        if self.cell_phone:
            _reveal_placement = self.cell_reveal_placement
        else:
            _reveal_placement = self.desktop_reveal_placement

        self.reveal_placement = _reveal_placement
        self.second_placement = [0.5, 0.2]

        self.hidden_button_desktop = [0.3, 0.4]
        self.hidden_button_cell = [0.2, 0.4]

        if self.cell_phone:
            #_hidden_butt = self.hidden_button_cell
            self.hidden_button_placement = self.hidden_button_cell
        else:
            #_hidden_butt = self.hidden_button_desktop
            self.hidden_button_placement = self.hidden_button_desktop
        #self.hidden_button_placement = _hidden_butt

        self.hidden_desktop = [0.5, 0.48]
        self.hidden_cell = [0.5, 0.55]

        # if self.cell_phone:
        #     _hidden_placement = self.cell_reveal_placement
        # else:
        #     _hidden_placement = self.desktop_reveal_placement

        #self.hidden_placement = _hidden_placement
        self.hidden_placement = self.hidden_cell

        self.hidden_offset = 0
        self.font_size = 30
        self.secondary_font = 20
        self.font_size_med = 20
        self.font_size_sm = 10

        self.wrap_cell = 1000
        self.wrap_desktop = 300
        if self.cell_phone:
            _wrap = self.wrap_cell
        else:
            _wrap = self.wrap_desktop
        self.wrap_len = _wrap

        # ---------------------------------------
        self.container = tk.Frame(self)
        self.container.place(relx=0, rely=0, relwidth=1, relheight=1)


        # -------------------------------------- Database information
        self.dict_keys = ['Subject', 'Clue', 'Answer', 'In Depth']
        self.final_keys = None
        self.final_dicts = None
        self.current_card_index = 0
        self.card_index_max = 0
        self.key_index = [1, 2]


        # Create the database ---------------------------------change which one you pull questions from
        self.format_a_plus_database()
        #self.format_network_plus_database()
        self.compile_database(self.group_list)


        self.database = pd.DataFrame(data=self.parent_list, columns=self.dict_keys)
        self.card_index_max = self.database.shape[0]

        self.frame = tk.Canvas(self)
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.subject_name = tk.Label(self, text='', font=("Calibri", self.font_size_med), wraplength=self.wrap_len)
        self.subject_name.place(relx=0, rely=0.0)

        self.prepare_card()

    def format_network_plus_database(self):
        self.parent_list = []
        self.network_models = [
            ['Network', 'Models'],
            ['Model', 'The key focus to this is representation, despite models having a multitude of different forms. Usually these are somewhat idealized and simplified', 'A weather map, a model plane, or a super model'],
            ['Network model', 'This is used to represent how networks function'],
            ['OSI seven layer model', 'Seven distinct functions that a network must do'],
            ['TCP/IP model', 'Four distinct laws which perform functions of the OSI layers, sometimes removing the antiquated portions']
        ]
        self.network_layers = [['Network', 'Layers'],
                               ['OSI', 'Open Systems Interconnection', 'Older model, more detailed'],
                               ['07: Application', "This is not the application it's self, but the processes within them that make them network aware",
                                "API(Application Programmer's Interface) is usually used as the definition of the processes of an application that allow us to make an application network aware"],
                               ['06: Presentation', 'This used to be used to convert data into a format that your applications can read'],
                               ['05: Session', 'The connection between two systems'],
                               ['04: Transport','Responsible for the disassembly and reassembly of transferred data'],
                               ['03: Network','This has to do with logical addresses, or, IP addresses', 'routers function in layer three mainly'],
                               ['02: Data Link', 'This will primarily have to do with anything that has a MAC address, the network cards, switches and such'],
                               ['01: Physical', 'relates primarily to the types of cables required and hubs'],
                               ['TCP/IP Model', 'Transmission Control Protocol/Internet Protocol Model', 'Newer, not as complicated'],
                               ['04: Application', 'This essentially covers the Application, Presentation and Session layers of the OSI model except that Application relates to the actual applications themselves'],
                               ['03: Transport', 'This covers the assembly and disasembly of data, but also whatever it takes to connect ot the other system in order for that data to get to the proper destination', 'TCP, UDP'],
                               ['02: Internet', 'This focuses primarily on IP addresses', 'routers end up falling in this layer due to that'],
                               ['01: Network Interface(Link)', 'This covers most physical objects in relation to your connection, with a few exceptions like routers', 'physical cabling, MAC addresses, Network cards'],
                               ['Ethernet Frame'],
                               ['IP packet'],
                               ['TCP segment', 'This is a portion of data the remains from an ethernet frame after passing through the first three layers of the OSI model(or the first two TCP/IP layers)',
                                'This data has been readied for your computer to handle']
                               ]
        self.layer_roles = [
            ['Layer', 'Roles'],
            ['Handling an ethernet frame', 'While receiving data'],
            ['OSI: 01:Physical, TCP:01:Network Interface(link)',
             "Inspect MAC address to verify that it's for this NIC"],
            ['OSI: 02:Data Link, TCP:01:Network Interface(link)',
             "Perform FCS, then strip the FCS and MAC addresses, leaving you with what is called an IP packet",
             'Good NICs will store the MAC addresses for later use'],
            ['OSI: 03:Network, TCP:02:Internet',
             'First will confirm that the IP address has reached the right destination, then store the IP address the packet was sent from'],
            ['OSI: 04:Transport, TCP: 03:Transport',
             'Acts as the assembler/disassembler of data, this process occurs by using the sequencing number',
             'Data and port numbers are passed to the next layer'],
            ['OSI: 05:Session, TCP: 04:Application',
             "Designed to connect a server to a client on a remote system, mostly used with older systems that wern't network aware",
             "In todays systems we have applications that're network aware"],
            ['OSI: 06:Presentation, TCP: 04:Application', "This was designed in the past as a means to handle files that wern't in a form the application could handle"],
            ['OSI: 07:Application, TCP: 04:Application',
             'This does not reference a program, but the built in smarts that allows them to interface to a network',
             'Here the model looks at the port numbers, stores the return number, then passes the data off to the right program'],
            ['Handling an ethernet frame', 'While preparing to send data'],
            ['OSI: 07:Application/06:Presentation/05:Session, TCP: 04:Application',
             'Here is where data is received from an application, takes the stored port number and reverses the positions of them before sending them and the data downward'],
            ['OSI: 04:Transport, TCP: 03:Transport',
             'If the data is large enough, it will be broken down in small enough sizes for individual chunks in order to pass on as a TCP segment',
             'this is also where sequencing numbers will be implemented'],
            ['OSI: 03:Network, TCP:02:Internet',
             'Here, the stored IP information will be reversed and then attached to create a IP packet, passed downward'],
            ['OSI: 01:Physical, TCP:01:Network Interface(link)',
             "The MAC addresses are now attached, and then finally a FCS before before being sent out"],
        ]
        self.frame_explanation = [
            ['Frame', 'Discreet chunks of binary'],
            ['Packetized data'],
            ['One frame can be up to?', '1500 bytes long'],
            ['Frames are generated in?', 'The network card in order to be sent out'],
            ['Frames are wiped out in?', 'The network card once the data is recieved'],
            ['Frames have a discreet beginning and end'],
            ['A hub is also known as what?', 'A repeater',
             'It takes an incoming signal and sends it out on all other connections'],
            ['MAC(Media Access Control) Address', 'This is also known as the physical address. This is a 48 bit, 12 hexidecimal digit string'],
            ['First three pairs of digits are known as?', 'the OEM numbers, this is issued to the NIC brand'],
            ['The last three pairs of digits are known as?', 'The Unique ID. These numbers are given to the card at the factory'],
            ['When constructing a frame', 'To and from MAC addresses are attached'],
            ['A CRC(cyclic redundancy check) is also attached, which', 'This is simply used to check if the data is good'],
            ['When a frame is recieved by a network card, what occurs?', "The MAC addresses are checked, if the frame is meant to be recieved, it moves forward in processing, otherwise it's removed"],
            ['Broadcast',
             'This type of casting uses a special type of MAC address, the frame is sent to every computer and the address moves it through processing',
             'FF-FF-FF-FF-FF-FF'],
            ['Unicast', 'This is the standard casting method in which a specific MAC address is known for the destination'],
            ['Broastcast Domain', 'Any time you have a group of computers that can hear eachothers broadcast, they are in a broadcast domain']
        ]
        self.ip_addressing = [
            ['Router',
             'This device typically has two or more connections and is used to make a connection between multiple local area networks',
             "If sending a frame to a different network, upon reaching the router, the frame's MAC addresses will be updated for the correct destination within the other network"],
            ['IP address', 'These are used for communication between multiple networks in order to distinguish the source and destination computers', 'When a frame is contructed, these are added'],
            ['IP Packet', "These sit within frames and consist of the frame's data and IP addresses", "This never changes as it is sent to it's destination, only the frame that surrounds it is changed"],
            ['Default Gateway',
             "This is typically the direct connection to your router, it's used when your NIC recognizes that the IP address it's using is not part of the NIC's network",
             "This is built into every NIC, and causes the MAC address to be addresses to the router instead of a computer's MAC address"],
            ['Routing Table', 'This is built into every router, this tells the router where to send data, based on the network information'],
        ]
        self.ports = [
            ['Port numbers are unique to', 'Individual applications thats are used all over the internet'],
            ['Certain port numbers are commonly known as being in use by specific functions', 'The first 1024 port numbers are known as Well Known Ports, these are reserved ports'],
            ['The first port number is what type of application is receiving the data', 'the second port number is how the information gets back to the sending computer after a response is made'],
            ['Port numbers range as high as', '0-65,535'],
            ['TCP(Transmission Control Protocol)', 'This is a connection oriented conversation between two computers in order to confirm that the data gets to you complete'],
            ['Sequencing Number', 'This number is the squence in which pieces of a large data file are put back together'],
            ['Acknowledgement number', 'This is the number used to confirm that data has been received'],
            ['UDP(User Datagram Protocol)',
             'This is similar to TCP, however it is not connection oriented, it is assumed that where you send this is already waiting to receive it',
             "It is up to the application it's self to verify the data and then try again if not all received"],
        ]

        self.cabling_and_topology = [
            ['Sometimes when installing new connection outlets, they are referred to as?',
             'A drop',
             'Comes from the old ethernet method of connecting to a bus as a "vampire connection" would be lowered from the cieling'],
            ['Topology', 'This is the form of how the data is moved from host to host',
             'Refers specifically to what transfer medium you use, cable, RF, Fiber Optic, Ect'],
            ['Physical Topology', 'How a topology physically looks in regards to cable structure'],
            ['Logical Topology', 'This refers more to the electronic diagram or circuit flow of frames'],
            ['Bus/Linear bus', 'It is unique in that all of the hosts are connected by a single cable, called a bus', 'Mostly Obsolete'],
            ['Ring',
             'This consists of a single ring of cabling that connects a number of systems. Anyone wanting to connect to this network, has to connect to this ring',
             'Used a technology known as token ring and originally created by IBM'],
            ['Star', 'This consists of a single "block" that sends signal out to each individual host', 'These are both rare and quite old'],
            ['Star-bus', 'Commonly this shows up in a router setup with multiple computers linking to it',
             'This is the primary topology used every day and considered a hybrid topology'],
            ['Ethernet networks', 'More often than not uses Star-Bus'],
            ['(Fully) Mesh(ed)', 'All hosts are connected to each other', 'This topology is primarily unique to wireless networks'],
            ['Partially Meshed', 'All hosts are connected to each other, one or more hosts may make connection through another host'],
            ['Coaxial Cable',
             'Conside of a copper cable in the center, covered by a insulation jacket and a mesh conducter surrounding that',
             'Referred to as Coaxial due to sharing the same Axis(co-ax). Most commonly used on home office modems'],
            ['RG', 'Radio Grade', 'This defines the thickness of the cable, thickness of the conductors, insulation and shielding'],
            ['OHMs', 'This is a measure of resistance and important to know in relation to coaxial cable'],
            ['RG-58', '50 OHM, one of the oldest types of cable discussed on the exam in relation to networking'],
            ['RG-59', '75 OHM rating, uses a threaded F-type connector', 'Not super robust'],
            ['RG-6', '75 OHM rating, thicker than the RG-59', 'The most common type to see with cable modems'],
            ['Thicknet', 'Thick ethernet coaxial cable, supports up to 10 megabits'],
            ['F-Type', 'Threaded coaxial connector, you will only see these in relation to cable modems'],
            ['BNC', 'unthreaded connector used on coaxial cables'],
            ['Twisted Pair Cabling', 'The most common type of network cabling, usually found in groupings of four twisted pairs'],
            ['Unshielded Twisted Pair(UTP)',
             'No metal covering coating the collection of inner wires used in a cable',
             'Not for use around machinery, strong magnetic fields, or intense heat as it will degrade the signal, however the tradeoff makes it quite cheap'],
            ['Shielded Twisted Pair(STP)',
             'This is a twisted pair cable in which a metal jacket runs the length of the cable.',
             'This type of cable is great if you cannot avoid putting cables near devices which may causes signal degradation'],
            ['EIA/TIA 568A Wiring Standard', 'Brown, brown-white, orange, blue-white, blue, orange-white, green, green-white'],
            ['EIA/TIA 568B Wiring Standard', 'Brown, brown-white, green, blue-white, blue, green-white, orange, orange-white'],
            ['Solid core', 'This refers to a single, solid piece of wire that '],
            ['Stranded core', 'This refers to a stranded piece of wire '],
            ['Cat ratings(Categories)',
             'A methodology to quickly identify which types of unshielded twisted pair cables will work with certain networks',
             'This defines the speed and cable length specifications and have a different number of twists per inch'],
            ['Cat 3', '10Mbps networks'],
            ['Cat 5', '100Mbps networks at 100 meters'],
            ['Cat 5e', '100-1000Mbps at 100 meters'],
            ['Cat 6', '1Gbps at 100 meters'],
            ['Cat 6a', '10Gbps at 100 meters'],
            ['Cat 7', '10Gbps at 100 meters, shielded', 'This came about as a fix for having RJ45 connectors'],
            ['The fiberous white strands found within cables', 'Kevlar, used to pull cables through conduits'],
            ['Fiber Optic Cabling',
             'This consists of a fiber optic(the core) which carries the light, the cladding(which reflects the light), and the cable jacket(which protects the cable)',
             'You have to have the right type of device for the right type of cabling'],
            ['Multimode', 'This is designed to propagate light, using LED signals which results in short to moderate distances', 'Typically this will be orange'],
            ['Single-mode', 'This carries laser signals which results in long distance signals', 'Typically this will be yellow'],
            ['Duplex', 'This refers to the two cable methodology for fiber optic. The cable is typically split at the ends, but the casings are one along the middle'],
            ['ST Connector', 'Looks similar to a BNC, push it into place, then twist to make a connection', 'One of the earliest types of connectors'],
            ['SC Connector', 'Square shaped, push them into place in order to make a connection, pull them out to break connection'],
            ['FC Connector', 'Looks similar to the ST, however it screws into place'],
            ['LC Connector', 'This connector has two cables attaches, and looks like a pair of square push pins'],
            ['MT-RJ Connector', 'This connector is small enough to looks like one cable end, but theres are two signals, It is squar shapes and has a small depressable latch on the top'],
            ['PC', 'Physical Contact', 'From the side it appears to have slightly rounded edges'],
            ['UPC', 'Ultra Physical Contact', 'From the side, the end appears close to the shape of a hemisphere, causing for less light loss'],
            ['APC', 'Angled physical contact', 'Has a seven degree angle on the cut of the cable, from one side to the other, this is also an improvement over PC. '],
            ['Plenum Rated',
             'Designed to run through various types of plenums and has the highest fire rating, therefore, the highest resistance',
             'This will typically be two to three times more expensive than PVC rated cabling'],
            ['Riser Rated',
             "This is designed to run between floors and doesnt have quite as good of a fire resistance rating as plenum",
             'Due to using something known as firestop, there is not as much of a need for fire resistance'],
            ['PVC/non-plenum rated', 'No fire protection'],
            ['Serial Port(DB-0)', 'Oldest I/O port used in computing, low speed, two way port for making connections. Has nine pins', 'Only one send pin so data bits must be sent out serially'],
            ['Parallel Port(IEEE1284)(DB-25)', 'This was a long port commonly used for printers'],
            ['RD-232', 'A language used by serial ports that will request and confirm upon sending'],
            ['IEEE', 'American standards organization, responsible for network standards'],
            ['Rollover/Yost cable',
             'Sometimes on high end routers you use on of these which has an RJ-45 connection on one end and serial on the other',
             'Mostly used for initial configuration or factory resets'],
            ['', ''],
            ['', ''],
            ['', ''],
        ]

        self.group_list = [
            self.network_models,
            self.network_layers,
            self.layer_roles,
            self.frame_explanation
        ]
        self.alternative_distribution_panels = [
            ['Alternative', 'Distribution'],
            ['66-punchdown block', 'A very old patch panel typically used in non-VoIP telephone systems'],
            ['110-punchdown block', 'A way to distribute copper wired networks'],
            ['Fiber distribution patch panel', 'Used to distribute fiber-optic networks']
        ]
        self.testing_cable = [
            ['Testing', 'Cable'],
            ['Wiremap', 'This refers to confirming that all of the wires on a cable are plugged into the connector properly'],
            ['Continuity', 'This refers to whether or not a wire within a cable is connected'],
            ['Distance', 'This is testing to make sure the run of the cable is not longer than practice standards'],
            ['TDR', 'Time domain reflectometer', 'Used to measure the distance of a run for ethernet and help pinpoint mid-cable breaks'],
            ['OTDR', 'Optical Time Domain Reflectometer', 'Used to measure the distance of a run for fiber optics and help pinpoint mid-cable breaks'],
            ['Crosstalk', 'Refers to the intereference between wire pairs within a run', 'Measured in decibels'],
            ['NEXT', 'Near-end Crosstalk'],
            ['FEXT', 'Far-end Crosstalk'],
            ['Crosstalk Report', 'This is what a cable installer will give you as proof to make sure the installation was done correctly'],
        ]

        self.troubleshoot_structured_cabling = [
            ['This is typically the last place you are going to look when an issue arises', 
            'Usually you will perform this if the system is unable to find connection, which is usually explicitly shown as a warning(Usually as "No network connection")'],
            ['When you suspect a problem with your structured cabling you do what?', 
            'Verify that there is a link light on your system', 
            'Verify you have a link light on your switch'],
            ['Go into device manager and check the network card', 
            'Is your network card enabled', 
            'Do you have good IP information'],
            ['Although rare, could you have bad device drivers', 
            "A Loopback plug can be used to check the NIC's ability to send and receive", 
            'Once plugged in, ping 127.0.0.1'],
            ['If your ping returns without issue, in theory it indicates the following', 
            'The network card is good', 
            'The pin connectors of the network card are good'],
            ['One issue however is that often times a network card will perform a loopback without ever using the internet connection', 
            'Check your patch cables as they are notorious for breaking'],
            ['The ethernet outlet is another common break point due to how much physical stress they receive', ''],
        ]

    def format_a_plus_database(self):
        # --------------------------------------- Databases
        self.port_numbers = [['Port', 'Numbers'],
                             ['21, 20', 'FTP, Active FTP', 'File Transfer Protocol'],
                             ['22', 'SSH', 'Secure Shell, this is a secure version of telnet'],
                             ['23', 'TELNET', 'Although this can be useful, it lacks security'],
                             ['25', 'SMTP', 'Simple Mail Tranfer Protocol'],
                             ['53', 'DNS', 'Domain Name System'],
                             ['67, 68', 'DHCP', 'Dynamic Host Configuration Protocol'],
                             ['80', 'HTTP', 'Hypertext Transfer Protocol'],
                             ['110', 'POP3', 'Post Office Protocol'],
                             ['137, 139', 'NETBIOS/NETBT', 'Network Basic Input Output System'],
                             ['143', 'IMAP', 'Internet Message Access Protocol'],
                             ['161, 162', 'SNMP', 'Simple Network Management Protocol'],
                             ['389', 'LDAP', 'Lightweight Directory Access Protocol'],
                             ['427', 'SLP', 'Service Location Protocol'],
                             ['443', 'HTTPS (encrypted/protected web page)', 'HTTP Secure'],
                             ['445', 'SMB/CIFS', 'Server Message Block/Common Internet File System'],
                             ['465, 587', 'SMTP encrypted port', 'Simple Mail Transfer Protocol'],
                             ['548', 'AFP', 'Apple Filing Protocol'],
                             ['993', 'IMAP encrypted port'],
                             ['995', 'POP3 encrypted port'],
                             ['3389', 'RDP', 'Remote Desktop Protocol']
                             ]
        self.cable_connectors = [['Cable', 'Connectors'],
                                 ['RJ11', 'Dial up/Telephone', 'Four contacts'],
                                 ['RJ45', 'Ethernet', 'Eight contacts'],
                                 ['BNC', 'Bayonet Neill-Concelman, Coaxial', 'F-Type connector'],
                                 ['PS2', 'Green for mouse, purple for keyboard'],
                                 ['Serial', '9 pins'],
                                 ['HDMI', 'High-definition multimedia interface', 'Compatible with DRM'],
                                 ['VGA', 'Video Graphics Array', '15 pins'],
                                 ['DVI', 'Digital visual Interface', "Can handle analog and digital with DVI-I"],
                                 ]
        self.cable_stats = [['Cable', 'Statistics'],
                            ['Cat-3', '10 Mbps'],
                            ['Cat-5', '100 Mbps'],
                            ['Cat5e', '1 Gbps'],
                            ['Cat-6', '1 Gbps up to 100 meters/ 10 Gbps up to 55 meters'],
                            ['Cat-6a', '10 Gbps up to 100 meters'],
                            ['Plenum rating', 'Fire resistance rating of cables'],
                            ['Plenum', 'The space between the ceiling/floor and drop ceiling/raised floor where cables are run through'],
                            ['PVC rated', 'Non Plenum, most burnable'],
                            ['Plenum rated', 'Highly resistant to heat and fire'],
                            ['Riser rated', 'Used for running between floors, more fire resistant than PVCm but not as much as plenum'],
                            ['10 Base T', '10 Mbps baseband Twisted Pair'],
                            ['10Gb base T', '10 Gigabit per second baseband twisted pair'],
                            ['RG ratings', 'An important coaxial cable classification'],
                            ['RG 58', 'This was commonly used in the networking world at one time'],
                            ['RG 59', 'Common cable in domestic settings, RG-59 cable is similar to the RG-6, but it has an even thinner centre conductor.','good choice for short runs and low-frequency transmissions.'],
                            ['RG 6', 'RG-6 cables have larger conductors, so they provide better signal quality.', 'They have thicker dielectric insulation and are made with a different kind of shielding, allowing them to handle GHz level signals more effectively. As this type of cable is thin, it can also be easily installed in walls or ceilings.'],
                            ['UTP', 'Unshielded Twisted Pair', 'Twisting cables helps propagate the signal, lending towards greater distances'],
                            ['STP', 'Shielded Twisted Pair', 'Cable shielding runs from end to end, helping to reduce interference.'],
                            ['Fiber', 'Fiber Optic Cableing', "Doesn't use electricity, uses light to transmit signal"],
                            ['Multimode', 'Fiber Optic cable that uses LEDs to propagate signal'],
                            ['Singlemode', 'Fiber Optic cable, uses lasers to propagate signal']
                            ]
        self.usb_rates = [['USB', 'Rates'],
                          ['1.0', '1.5Mbps'],
                          ['1.1', '12 Mbps'],
                          ['2.0', '480 Mbps'],
                          ['3.0', '5 Gbps'],
                          ['3.1, gen1', '5 Gbps'],
                          ['3.1, gen2', '10 Gbps']]
        self.optical_disks = [['Optical', 'Disk sizes'],
                              ['Compact discs(CDs)', '650-700mb'],
                              ['Digital video/versatile discs(DVDs)', '4.37GB to 15.9GB'],
                              ['Blu-ray discs(BDs)', '25GB to 50GB']]
        self.network_info = [['Network', 'Information'],
                             ['IP', 'Internet Protocol'],
                             ['SFTP', 'SSH File Transfer Protocol', 'Uses FTP with security to transfer files, uses port 22'],
                             ['TCP', 'Transmission Control Protocol',
                              'One of the main protocols of the Internet protocol suite, it is connection oriented and provides reliable, ordered, and error-checked delivery of a stream of octets (bytes) between applications'],
                             ['UDP', 'User Datagram Protocol',
                              "a connectionless protocol that sends out a query knowing that where ever it's going is all ready to return what you may ask for"],
                             ['ICMP', 'Internet Control Message Protocol', 'Single-Packet only, a good example of this is the ping command in command prompt'],
                             ['NAT', 'Network Address Translation', 'Developed as a method to fix running out of IPv4 addresses'],
                             ['ISP', 'Internet Service Provider'],
                             ['APIPA', 'Automatic Private IP Addressing'],
                             ['DSL', 'Direct Subscriber Line', ' a family of technologies that are used to transmit digital data over telephone lines'],
                             ['QoS', 'Quality of Service', 'Used to meter how much bandwith is given to certain users and/or types of network use'],
                             ['UPnP', 'Universal plug and play', "a set of networking protocols that permits networked devices to seamlessly discover each other's presence on the network"],
                             ['ADSL', 'Asynchronous Direct Subscriber Line'],
                             ['NAS', 'Network attached storage'],
                             ['TLS', 'Transport Layer Security'],
                             ['SSL', 'Secure Socket Layer'],
                             ['Thick Client', 'This is most often the basic desktop office computer with middle tier components, on board graphics are typically fine for this'],
                             ['Thin Client', 'This minimizes internal storage and maximizes internet connectivity'],
                             ['CAD', 'Computer aided design'],
                             ['CAM', 'Computer Aided Manufacturing'],
                             ['Virtualization workstation', 'This type of system usually focuses on RAM and CPU', 'values storage capacity as once they are powered down, virtual machines tend to take up a fair amount of space. '],
                             ['Gaming PC', 'This tends to have high tier components in order to maximize performance/minimize latency'],
                             ['Audio/Video editing workstation', 'Specialized video and audio cards for these systems are a must', 'Large storage capacity is also important as these type of raw files tend to take up lots of space']
                             ]
        self.wifi_standards = [['Wifi', 'Standards'],
                               ['2.4Ghz', '2.412 to 2.4884'],
                               ['# of specific channels', '14'],
                               ["Japan's channels", '14'],
                               ["Europe's channels", '13'],
                               ["USA's channels", '11'],
                               ['5 GHz band', '5.150, 5.875'],
                               ['5 GHz band', 'three tiers of ranges'],
                               ['The first', '36, 40, 44, 48, 52, 60, 64'],
                               ['The second', '100, 104, 108, 112, 116, 120, 124, 128, 132, 136, 140, 144'],
                               ['third range', '149, 153, 157, 161, 165']
                               ]
        self.wifi_extensions = [['Wifi', 'Extensions'],
                                ['802.11', 'ran at 54Mbps at 5GHz'],
                                ['802.11b', 'runs at 11Mbps on the 2.4GHz'],
                                ['802.11g', '54Mbps on the 2.4GHz'],
                                ['802.11n', '100Mbps on 2.4 and 5GHz'],
                                ['MIMO', 'Multiple-input and Multiple-output']
                                ]
        self.network_layers = [['Open Systems Interconnection(OSI)', 'Layers'],
                               ['07: Application',
                                ' layer closest to the end user, which means both the OSI application layer and the user interact directly with the software application'],
                               ['06: Presentation', 'establishes context between application-layer entities'],
                               ['05: Session', 'controls the dialogues (connections) between computers'],
                               ['04: Transport',
                                'provides the functional and procedural means of transferring variable-length data sequences from a source to a destination host, while maintaining the quality of service functions'],
                               ['03: Network',
                                'provides the functional and procedural means of transferring variable length data sequences (called packets) from one node to another connected in "different networks"'],
                               ['02: Data Link', 'provides node-to-node data transfer'],
                               ['01: Physical',
                                'the transmission and reception of unstructured raw data between a device and a physical transmission medium'],
                               ]
        self.hex_to_binary = [["Hex to", 'Binary'],
                              ['0000', '0'],
                              ['0001', '1'],
                              ['0010', '2'],
                              ['0011', '3'],
                              ['0100', '4'],
                              ['0101', '5'],
                              ['0110', '6'],
                              ['0111', '7'],
                              ['1000', '8'],
                              ['1001', '9'],
                              ['1010', 'A'],
                              ['1011', 'B'],
                              ['1100', 'C'],
                              ['1101', 'D'],
                              ['1110', 'E'],
                              ['1111', 'F']]
        self.hex_to_num = [['Hex to', 'Number'],
                           ['a', '10'],
                           ['b', '11'],
                           ['c', '12'],
                           ['d', '13'],
                           ['e', '14'],
                           ['f', '15'],
                           ['10', '16'],
                           ['4f', '79'],
                           ['2a', '42']]
        self.raid_types = [['Raid', 'Types'], # Less offset on answers
                           ['Raid level 0',
                            'Provides higher save speeds by breaking the data between two drives, piece by piece', 'requires a minimum of two drives and known as striping'],
                           ['Raid level 1',
                            'This process saves data in duplicates across a pair(at minimum) of drives in order to achieve redundancy, if you lose one drive you will always have a backup drive',
                            'This process slows recording data and is known as mirroring'],
                           ['Raid level 5',
                            "Data is saved similarily to raid 0, except, after each repitition of saving pieces the two pieces are multiplied together using a binary operation to compile a parity value which is placed onto the third drive",
                            'requires a minimum of three drives. the data can then be recreated on the fly through comparison against the parity drive and is known as striping with parity'],
                           ['Raid level 6',
                            "Works similarily to raid 5 however there are two backup drives that the saved parity files are stored on, redundantly. You can lose up to two drives before losing any data",
                            'requires a minimum of four drives'],
                           ['Raid level 10',
                            'Requires a minimum of four drives, known as striping mirrors',
                            "It consists of two mirrored pairs of drives, that data is striped across. You can lose one of the mirrored pairs on each side and still function"]
                           ]
        self.ram_types = [['RAM', 'Specifications'],
                          ['DDR4', '288 pins'],
                          ['DDR3', '240 pins'],
                          ['DDR2', '240 pins'],
                          ['SO-DIMM', '200 pins'],
                          ['DDR', '184 pins', 'also known as SDRAM']
                          ]
        self.ip_address_types = [['IP', 'Types'],
                                 ['IP Address',
                                  'A unique string of numbers identifying a computer using the Internet Protocol'],
                                 ['MAC Address', 'Logical Address, Ethernet Address or physical address',
                                  'A Media Access Control address is a unique identifier assisgned to a NIC for use as a network address'],
                                 ['Class A', '1-126', 'No Octets locked'],
                                 ['Class B', '128-191', 'Second Octet locked'],
                                 ['Class C', '192-223', 'Second and third octets locked'],
                                 ['Class D', '224', 'Each other octet assigned'],
                                 ['Class E', '240', 'Each other octet assigned'],
                                 ['Private IP', 'These are for those who are not connected to the standardized internet.', 'They come in three sets.'],
                                 ['Private Class A', 'Starts with 10', '10.x.x.x'],
                                 ['Private Class B', 'Starts within the range of 172.16.x.x - 173.31.x.x'],
                                 ['Private Class C', '192.168.x.x'],
                                 ['Loopback IP Address', '127.0.0.1', 'Used to be a common method for checking your own system'],
                                 ['APIPA', '169.245.x.x address', 'This will be assigned if your DHCP is down. You can use ipconfig /release and ipconfig /renew to try and reset'],
                                 ['IPv4', 'This is an old 32 bit, form for IP addresses consisting of four octets separated by three dots', '11.12.13.66'],
                                 ['IPv6', 'A 128 bit address consisting of eight groupings of four hexidecimal numbers separated by seven columns', 'This was designed as a means to better accommodate the amount of IP addresses for how expansive the internet became'],
                                 ['IPv6 syntax', '2001:0000:0000:0001:0000:0000:0000:8a2e', 'Rewritten without any of the leading zeros looks like this: 2001:0:0:1:0:0:0:8a2e, If you have three zeros in a row, you can replace that with a double colon: 2001:0:0:1::8a2e'],
                                 ['8.8.8.8 / 8.8.4.4', 'Google public DNS provider'],
                                 ['FCS', 'Frame check sequence']
                                ]
        self.network_types = [['Network', 'Types'],
                              ['PAN', 'Personal Area Network'],
                              ['LAN', 'Local Area Network'],
                              ['WLAN', 'Wireless Local Area Network'],
                              ['MAN', "Metropolitan Area Network"],
                              ["WAN", "Wide Area Network"]
                              ]
        self.email_specs = [['Email', 'Specifications'],
                            ['Email is sent on which port', '25, SMTP'],
                            ['Email is commonly recieved on which port', '110, POP3'],
                            ['Email is sometimes recieved on which port', '143, IMAP']
                            ]
        self.os_and_virtualization_specs = [['OS/virtualization', 'Specifications'],
                                            ['Hypervisor', 'a host the runs one or more virtual machines'],
                                            ['Type 1', 'Is installed directly on the hardware with nothing separating the two'],
                                            ['Type 2', 'Is installed onto an OS like any other application'],
                                            ['IaaS', 'Infrastructure as a service', 'moves network tasks such as firewalls into the Cloud'],
                                            ['PaaS', 'Platform as a Service', 'moves the machines into the cloud so you can concentrate on the apps.'],
                                            ['SaaS', 'Software as a Service', 'moves apps to the Cloud, such as Google Docs'],
                                            ['Private clouds','are owned and used only by a single organizations'],
                                            ['Public clouds','are privately owned but are available for public use'],
                                            ['Hybrid clouds','have both private and public aspects'],
                                            ['Community clouds','are owned by multiple organizations for their own private use']
                                           ]
        self.storage_and_memory = [['Storage', 'Specifications'],
                                   ['NVMe', 'Non-volatile Memory Express', 'a host controller interface and storage protocol created to accelerate the transfer of data between enterprise and client systems and solid-state drives'],
                                   ['SCSI', 'Small Computer System Interface'],
                                   ['iSCSI', 'internet Small Computer System Interface'],
                                   ['SAS', 'Serial attached SCSI'],
                                   ['SATA', 'Serial Advanced Technology Attachment'],
                                   ['PATA', 'Parallel Advanced Technology Attachment'],
                                   ['LBA', 'Logical block addressing'],
                                   ['DEP', 'Data Execution Prvention'],
                                   ['GDPR', 'General Data Protection Regulation'],
                                   ['PII', 'Personally Identifiable Information'],
                                   ['PRL', 'Preferred Roaming List'],
                                   ['QVL', 'Quality Vendor List'],
                                   ['OEM', 'Original Equipment List'],
                                   ['JBOD', 'Just a bunch of disks'],
                                   ['HTPC', 'Home Theater Personal Computer'],
                                   ['S/MIME', 'Secure/Multipurpose internet Mail Extensions']
                                   ]
        self.motherboard_formfactors = [['Motherboard', 'Form Factors'],
                                        ["ATX", "12in by 13in", "This is currently the most common motherboard used for desktop computers."],
                                        ["Micro ATX", "9.6in by 9.6in", "This board is commonly used for small form factor desktop computers."],
                                        ["Mini ITX", "6.7in by 6.7in", "Originally designed for low power comsumption computing, it's popularity has sky rocketed it's use elsewhere."],
                                        ["Nano ITX", "4.7in by 4.7in", "It was designed for smart entertainment, PVRs, media centers, smart TVs, in-vehicle devices, and more."],
                                        ["Pico ITX", "3.9in by 2.8in", "developed by VIA, to open up innovation for smaller and smarter IoT devices."],
                                        ['What you do first if new hardware installed is not functioning correctly', 'Recheck the physical installation that occured'],
                                        ['Boot sequence', 'Power good, CPU, POST, Boot loader, O.S.']]
        self.display_technologies = [['Display', 'Technologies'],
                                     ['CCFL', 'cold cathode fluorescent lamp'],
                                     ['TN', 'Twisted Nematic'],
                                     ['IPS', 'In-Plane Switching'],
                                     ['nit','a measure of light'],
                                     ['DLP', 'Digital Light Processing'],
                                     ['Projectors use these', 'Most use DLP or LCD'],
                                     ['Lumen', 'A measure of brightness for projectors'],
                                     ["How many lumens should you use for a small room that you can make pretty dark?", "1000-1200 lumens"],
                                     ["In a place that has a lot of light?", "around 2500 lumens"],
                                     ['Throw', 'A measurement between the screen and projector length', 'There is a minimum and maximum you typically want to work between'],
                                     ['Pincusion', 'sides of the screen are bowed'],
                                     ['Keystone', 'screen appears trapezoidal'],
                                     ['Skew', 'when the sides of the image slope in one direction'],
                                     ['4:3 aspect ratios', 'originally this mimiced televisions that were in use during this era.'],
                                     ["VGA ratio", "640 by 480"],
                                     ["SVGA", "800 by 600", "this resolution is important as most versions of Windows will downgrade to this if difficulties arise"],
                                     ['SXGA', '1280 by 1024'],
                                     ['UXGA', '1600 by 1200'],
                                     ['16:10', "second generation of aspect ratios", 'tied into The Golden Ratio. This is a mathematical equation that is also perceived as quite aesthetically pleasing'],
                                     ['WSXGA', '1440 by 900', 'common at that time for laptops'],
                                     ['WUXGA', '1920 by 1200'],
                                     ['720p', '1280x720', 'The P stands for progressive scan'],
                                     ['Interlaced scanning', 'The procedure of scanning ever other line, starting at 1, then 3, and so forth, the repeating but starting at 2'],
                                     ['1920x1080', '1080p', 'standard HGTV pixel ratio, this is most common ratio used currently.'],
                                     ['3840x2160', 'this is considered a classic 4K ratio'],
                                     ['5120x2880', 'this is considered a 5K ratio, more common in mac systems']
                                     ]
        self.common_sockets = [['Common', 'Socket types'],
                               ['LGA 2011', 'Intel'],
                               ['LGA 1151', 'Intel'],
                               ['LGA 1200', 'Intel'],
                               ['AM4', 'AMD'],
                               ['TR4', 'AMD'],
                               ['sTRX4', 'AMD'],
                               ['TR4', 'AMD'],
                               ['1150', 'Intel'],
                               ['FM2', 'AMD'],
                               ['AM3', 'AMD'],
                               ['1155', 'Intel']
                               ]
        self.command_line_w = [['Windows', 'Command line'],
                               ['dir', 'Shows all directories and files'],
                               ['cd', 'This is used to navigate the directories', 'cd directory_name, cd ..'],
                               ['x:', 'This is used to navigate other drives', 'a:, b:, d:, ect.'],
                               ['help', 'This is used to display the list of commands or explain commands', 'help or dir /?'],
                               ['cls', 'Clears the screen'],
                               ['exit', 'Exits the command line'],
                               ['Switch', 'Refines details of the command', '/p, /s, /r, /?, ect'],
                               ['md', 'This will create a new directory'],
                               ['rd', 'This will remove a directory specified'],
                               ['del or erase', 'This is used to delete files'],
                               ['*', 'This is a wildcard denoting one or more characters'],
                               ['?', 'This is a wildcard denoting one character'],
                               ['copy', 'This is used to copy a file from the current directory', 'copy file_name dir_to_copy_to'],
                               ['move', 'This is used to move a file from the current directory', 'move file_name dir_to_move_to'],
                               ['ipconfig', 'This returns current network details', '/release, /renew, /flushdns'],
                               ['tracert', 'This returns each IP connection made when connecting to a specific address'],
                               ['format', 'Used to format drives', 'format drive_letter /FS:file_system'],
                               ['chkdsk', 'This performs a check disk', 'It verifies the file system integrity of a volume and fixes logical file system errors'],
                               ['sfc', 'Performs system file checker', 'System File Checker is a utility in Microsoft Windows that allows users to scan for and restore corruptions in Windows system files'],
                               ['dism', "Compares windows image to microsoft's internet stores and updates/corrects them if needed", 'used for corrupted files'],
                               ['diskpart', 'Used to do anything mass storage related', 'Functions as a sub program of the CLI'],
                               ['xcopy', "The original copy command with ability to verify data as it's copied", 'xcopy path_to_copy path_copy_destination'],
                               ['robocopy', "copy command with greater ability to verify data as it's copied and faster", 'robocopy path_to_copy path_copy_destination'],
                               ['shutdown', 'Shuts down system from command line', '/s simple shutdown. /r shut down and restart'],
                               ['tasklist','Displays a list of all processes that are currently running on the system'],
                               ['taskkill', 'Stops any task by name or PID'],
                               ['gpupdate', 'Updates multiple group policy settings by querying the domain controller for changes'],
                               ['gpresult', 'displays what domain controller changes will be applied'],
                               ['icacls', 'Used to change permissions', 'icacls file_name /grant user_name:F'],
                               ['ping', 'Used to check that your network card is working', 'Sends a special type of packet known as a ping packet to a specific IP address']
                               ]
        self.command_line_l = [['Linux', 'Command line'],
                               ['ls', 'Shows all directories and files', '-l will show file permissions'],
                               ['cd', 'This is used to navigate the directories', 'Linux is case sensitive'],
                               ['cd ~', 'This is used to return to home directory'],
                               ['pwd', 'This will return your directory path'],
                               ['man', 'This brings up the command manual', 'ls man'],
                               ['clear', 'clears the screen'],
                               ['Switch', 'Refines details of the command', '-p, -s, -r, ect'],
                               ['mkdir', 'This will make a specified directory'],
                               ['rmdir', 'This will remove a specified directory'],
                               ['rm', 'deletes a file'],
                               ['*', 'Wildcard for one or more characters', 'M*'],
                               ['cp', 'This is used to copy from the current directory', 'cp file_name, dir_to_move_to'],
                               ['mv', 'This is used to move from current directory', 'mv file_name dir_to_move_to'],
                               ['ifconfig', 'This returns all current network connection information'],
                               ['dd', 'Heavy lifting copy command that copies bit by bit', 'Can be used to make disk image files or wipe drives'],
                               ['shutdown', 'Used to shut the system down'],
                               ['apt-get', 'Used to install software from Debian store of files from internet'],
                               ['sudo', 'denotes that a superuser is carrying out the command', 'prompts user for credentials'],
                               ['apt-get update', "Updates your system's database of known programs"],
                               ['ps', 'Show currently running processes'],
                               ['ps aux', 'Show currently running processes, including those from other systems and users'],
                               ['kill', "Used to kill a process using it's ID"],
                               ['vi file_name', 'opens Vi text editor', 'vi file_name, "I" to insert'],
                               ['chmod', 'used to change specified user permissions for the User, Group and other', 'chmod 777 filename, for each group, read equals 4, write equals 2 and execute equals 1'],
                               ['chown', 'Used to gain ownership of a file', 'chown user_name file_name'],
                               ['passwd', 'used to change unix password', 'sudo passwd']
                               ]
        self.six_steps = [['Troubleshooting', 'Theory'],
                          ['1', 'Identify the problem'],
                          ['2', 'Establish a theory of probable cause'],
                          ['3', 'Test the theory to determine cause'],
                          ['4', 'Establish a plan of action to resolve the problem and implement the solution'],
                          ['5', 'Verify full system functionality and if applicable implement preventative measures'],
                          ['6', 'Document findings, actions, and outcomes']
                          ]
        self.seven_steps = [['Seven Steps', 'Malware'],
                            ['1', "Identify and research malware symptoms"],
                            ['2', "Quarantine infected systems: Remove the system from the network, unplug the cable so this machine cannot infect other machines on the network. Disable the wireless connection if needed"],
                            ['3', "Disable System Restore: This may seem strange but Windows will initiate system restore on certain situations. For example, if you shut down the system and it creates an restore point. By disabling it, you remove the chance of having infected restore points."],
                            ['4', "Remediate the infected systems:\n1. Update the anti-malware software. These require signature files to work, updating these help this software to work.\n 2. Scan and use removal techniques(safe mode, pre-installation environment) Often times using your anti-malware software will be sufficient to take care of the problem but at times you need to use a boot-disk in order to fix something. Using a boot disk is an extremely polarizing topic that have fervent supporters on each side of the fence."],
                            ['5', "Schedule scans and run updates, scanning about once a week is a good metric for scans. Useful to schedule it for a time you don't plan to be using your system"],
                            ['6', "At this point go ahead and turn your system restore back on and create a new system restore point (if in Windows). It might not be a bad idea to also delete the last week or month of restore points from here as there's a relatively high chance of them containing some form of malware in them."],
                            ['7', "Educate your end user, make sure they understand the symptoms of malware so they understand if there is a certain kind of issue to run a scan, or if the problem is bad enough they can call you.]"]]

        # ---------------- final groups
        self.parent_list = []

        if self.flipped:
            self.group_list = [self.port_numbers,
                               #self.cable_connectors,
                               self.cable_stats,
                               self.usb_rates,
                               #self.optical_disks,
                               self.wifi_extensions,
                               self.network_layers,
                               # self.hex_to_binary,
                               # self.hex_to_num,
                               self.raid_types,
                               self.ram_types,
                               self.ip_address_types,
                               self.email_specs,
                               self.os_and_virtualization_specs,
                               self.storage_and_memory,
                               self.motherboard_formfactors,
                               self.display_technologies,
                               self.common_sockets,
                               self.command_line_w,
                               self.command_line_l
                               ]
        else:
            self.group_list = [self.port_numbers,
                               #self.cable_connectors,
                               self.cable_stats,
                               self.usb_rates,
                               #self.optical_disks,
                               self.network_info,
                               #self.wifi_standards,
                               self.wifi_extensions,
                               self.network_layers,
                               # self.hex_to_binary,
                               # self.hex_to_num,
                               self.raid_types,
                               self.ram_types,
                               self.ip_address_types,
                               #self.network_types,
                               self.email_specs,
                               self.os_and_virtualization_specs,
                               self.storage_and_memory,
                               self.motherboard_formfactors,
                               self.display_technologies,
                               self.common_sockets,
                               self.command_line_w,
                               self.command_line_l,
                               self.six_steps,
                               self.seven_steps
                               ]

        # Format the data groups for pandas
        # for _sub in self.group_list:
        #     # Identify and join subject name
        #     _sub_name = [_sub[0][0] + ' ' + _sub[0][1]]

        #     # Loop through all cards in the subject group while adding the subject to the card
        #     for _card in _sub[1:]:
        #         _card = _sub_name + _card

        #         # Add empty strings to the list if there isn't enough data
        #         if len(_card) < 3:
        #             _card.append('')

        #         if len(_card) < 4:
        #             _card.append('')

        #         self.parent_list.append(_card)
        return self.group_list

    def compile_database(self, _grouping):
        # Format the data groups for pandas
        for _sub in _grouping:
            # Identify and join subject name
            _sub_name = [_sub[0][0] + ' ' + _sub[0][1]]

            # Loop through all cards in the subject group while adding the subject to the card
            for _card in _sub[1:]:
                _card = _sub_name + _card

                # Add empty strings to the list if there isn't enough data
                if len(_card) < 3:
                    _card.append('')

                if len(_card) < 4:
                    _card.append('')

                self.parent_list.append(_card)

    def prepare_card(self):
        self.setup_answer()

        if self.flipped:
            self.key_index = [2, 1]
        else:
            self.key_index = [1, 2]

        _message, _text_offset, _font_size = self.string_offset(self.dict_keys[self.key_index[0]], [13, 80])

        if self.subject_name.cget('text') != self.database.loc[self.current_card_index, self.dict_keys[0]]:
            self.subject_name.configure(text=self.database.loc[self.current_card_index, self.dict_keys[0]])

        # ---------------------------------------------------- First message setup
        self.first_message = self.message_setup(self.first_message,
                                                _message,
                                                _font_size,
                                                _text_offset,
                                                self.first_placement)

        _message_depth, self.hidden_offset, _font_size_depth = self.string_offset(self.dict_keys[3], [13, 80])
        #print(_message_depth, self.hidden_offset, _font_size_depth)

        self.in_depth_label = self.evaluate_in_depth(self.in_depth_label, _message_depth, _font_size_depth)

    def setup_answer(self):
        # ---------------------------------------------------- Reveal setup
        if self.in_depth_label != None:
            self.in_depth_label.destroy()
            self.in_depth_label = None

        if self.hidden_reveal != None:
            self.hidden_reveal.destroy()
            self.hidden_reveal = None

        if self.reveal != None:
            # If the variables already exists
            self.reveal.configure(text='Reveal', command=lambda: self.show_answer())
        else:
            # If the variable does not yet exist
            self.reveal = tk.Button(self,
                                    text='Reveal',
                                    height=5,
                                    width=20,
                                    command=lambda: self.show_answer())
            self.reveal.place(relx=self.reveal_placement[0], rely=self.reveal_placement[1])

        if self.second_message != None:
            self.second_message.destroy()

        if self.first_message != None:
            self.current_card_index += 1

            if self.current_card_index > self.card_index_max:
                self.current_card_index = 0

    def string_offset(self, _dict_key, _string_lengths):
        # ----------------------- String length offsets -----------------------------
        #_message = _card = _db.loc[self.current_card_index, _dict_key]
        _message = _card = self.database.loc[self.current_card_index, _dict_key]
        _text_length = len(str(_message))
        _font_size = self.font_size

        if _text_length > _string_lengths[0] and _text_length < _string_lengths[1]:
            _font_size = self.font_size_med
        elif _text_length >= _string_lengths[1]:
            _font_size = self.font_size_sm

        if _text_length > 10:
            _text_length = 10

            if _font_size == self.font_size_sm:
                _text_length = 20

        _text_offset = _text_length * 0.5
        _text_offset = _text_offset * 0.1

        return [_message, _text_offset, _font_size]

    def message_setup(self, _message_obj, _message, _font_size, _text_offset, _placement):
        # ---------------------------------------------------- First message setup
        if _message_obj != None:
            # If the Label exists
            _message_obj.destroy()

            _message_obj = tk.Label(self,
                                    text=_message,
                                    font=("Calibri", _font_size),
                                    wraplength=self.wrap_len)
        else:
            # If the label does not yet exist
            _message_obj = tk.Label(self,
                                    text=_message,
                                    font=("Calibri", self.font_size),
                                    wraplength=self.wrap_len)

        # Placement
        _end_placement = _placement[0] - _text_offset
        if _end_placement < 0:
            _end_placement = 0
        _message_obj.place(relx=_end_placement, rely=_placement[1])

        return _message_obj

    def evaluate_in_depth(self, _message_obj, _message, _font_size):
        # ---------------------------------------------------- hidden message setup
        if  len(self.database.loc[self.current_card_index, self.dict_keys[3]]) > 0:  # ---------------------- to be debugged
            # ---------------------------------------------------- First message setup
            if _message_obj != None:
                # If the Label exists
                _message_obj.destroy()

                _message_obj = tk.Label(self, text=_message, font=("Calibri", _font_size))
                # self.first_message.place(relx=self.first_placement[0] - _text_offset, rely=self.first_placement[1])
            else:
                # If the label does not yet exist
                _message_obj = tk.Label(self,
                                        text=_message,
                                        font=("Calibri", _font_size),
                                        wraplength=self.wrap_len)

            return _message_obj
        else:
            _message_obj = None
            return _message_obj

    def show_answer(self):
        # --------------------------- Centering adjustment
        _message, _text_offset, _font_size = self.string_offset(self.dict_keys[self.key_index[1]], [20, 80])

        self.second_message = tk.Label(self,
                                       text=_message,
                                       font=("Calibri", _font_size),
                                       wraplength=self.wrap_len)

        _end_placement = self.second_placement[0] - _text_offset

        if _end_placement < 0:
            _end_placement = 0

        self.second_message.place(relx=_end_placement, rely=self.second_placement[1])

        self.reveal.configure(text="Next Fact", command=lambda: self.prepare_card())

        # if hidden information exists, show button
        if self.in_depth_label != None:
            # self.reveal = tk.Button(self, text='Reveal', height=5, width=20, command=lambda: self.show_answer())
            self.hidden_reveal = tk.Button(self,
                                           text='In Depth Look',
                                           height=5,
                                           width=20,
                                           command=lambda: self.show_hidden())
            #print(self.hidden_button_placement[0], self.hidden_button_placement[1])
            self.hidden_reveal.place(relx=self.hidden_button_placement[0], rely=self.hidden_button_placement[1])

    def show_hidden(self):
        _end_placement = self.hidden_placement[0] - self.hidden_offset
        if _end_placement < 0:
            _end_placement = 0

        self.in_depth_label.place(relx=_end_placement, rely=self.hidden_placement[1])


cards = FlashCards()
cards.mainloop()

