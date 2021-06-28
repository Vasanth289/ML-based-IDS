ML based Intrusion Detection System

  -> 	captures folder contains all the pcap files captured using tshark.

  -> 	lists folder contains all the list files, which has all the connections identified and the attribute values used by NSL-KDD dataset.

  ->	Sec_Proj_NSL_KDD.py is used to train the model. Give a test dataset/list file 
		
		$ python3 Sec_Proj_NSL_KDD.py <list_filename>

  -> 	ids.py is a python script which captures network traffic on a specified interface and computes list files and predicts them on our trained model. You can specify how many packets to capture using <count>. <capture_file> is the path where pcap files will be stored
		
		$ python3 ids.py <capture_file> live <count> <interface>