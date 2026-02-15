'''
Annika Hoag
February 5, 2026
PA 1
'''



# Hard coded parameters 
FILE_SIZE = 5*(2**20)#MiB, (5*2^20) bytes
PACKET_PAYLOAD_SIZES = [700, 1400, 2800] #bytes
PACKET_HEADER_SIZE = 100 #bytes
LINK_1_TRANS = 10 #Mbps
LINK_1_PROP = 10 #ms
LINK_2_TRANS = 5 #Mbps
LINK_2_PROP = 20 #ms
LINK_3_TRANS = 20 #Mbps
LINK_3_PROP = 5 #ms



for payload_size in PACKET_PAYLOAD_SIZES:
    trans_delay=[]
    prop_delay = []
    utilization = []


    print("Payload size: ", payload_size, " bytes")

    # -------------------PART A-------------

    # Number of packets needed to send file (last packet may be smaller)
    packet_size_on_wire = payload_size + PACKET_HEADER_SIZE
    num_packets = round(FILE_SIZE / packet_size_on_wire)
    print("\nNumber of packets needed to send the file: ", num_packets)

    # Packet size in bits
    packet_size_bits = packet_size_on_wire * 8
    print("\nPacket size: ", packet_size_bits, " bits")

    # Transmission delay per link (d_trans=L/R)
    d_trans1 = packet_size_bits / (LINK_1_TRANS*(10**6)) 
    d_trans2 = packet_size_bits / (LINK_2_TRANS*(10**6))
    d_trans3 = packet_size_bits / (LINK_3_TRANS*(10**6))
    trans_delay = [d_trans1, d_trans2, d_trans3]
    print("\nTransmission delay for each link: ")
    for delay in trans_delay:
        print(delay, "  seconds")

    # Propagation delay 
    d_prop1 = LINK_1_PROP*(10**-3)
    d_prop2 = LINK_2_PROP*(10**-3)
    d_prop3 = LINK_3_PROP*(10**-3)
    prop_delay = [d_prop1, d_prop2, d_prop3]
    print("\nPropagation delay per link: ")
    for delay in prop_delay:
        print(delay, " seconds")



    #-------------------PART B--------------

    # Compute arrival time of the first packet at the destination
    t_first = 0
    N = 3 #number of links 
    for i in range(N):
        t_first = t_first + (trans_delay[i] + prop_delay[i])
    print("\nArrival time of first packet at the destination: ", t_first, " seconds")



    #------------------PART C---------------

    # Identify bottleneck transmission delay
    bottleneck_trans_delay = max(trans_delay)
    print("\nBottleneck transmission delay: ", bottleneck_trans_delay, " seconds")

    # Compute total file arrival time
    t_file = t_first + (num_packets-1) * bottleneck_trans_delay
    print("\nTotal file arrival time: ", t_file, " seconds")



    #------------Part D--------------------

    # Effective throughput in Mbps
    throughput = ((FILE_SIZE*8) / t_file) / (10*(10**5))
    print("\nEffective throughput: ", throughput, " Mbps")

    # Utilization per link
    util1 = throughput / LINK_1_TRANS
    util2 = throughput / LINK_2_TRANS
    util3 = throughput / LINK_3_TRANS
    utilization = [util1, util2, util3]
    print("\nUtilization per link: ", utilization)


    print("\n----------------------------------------------------------------------------------------------------\n")