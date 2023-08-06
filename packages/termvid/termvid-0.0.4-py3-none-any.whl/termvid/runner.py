import struct
import pickle
import time
import cv2
import blessed
import threading

term = blessed.Terminal()
width_to_send = 300

def get(s, box):
	global size_to_send
	payload_size = struct.calcsize("L")
	recv_data = b''
	spf = 0.0
	drawer = threading.Thread()
	while True:
		start = time.time()

		# Get timestamp
		ts_size = struct.calcsize(">i")
		while len(recv_data) < ts_size:
			recv_data += s.recv(4096)
		buffer, recv_data = recv_data[:ts_size], recv_data[ts_size:]
		timestamp = struct.unpack(">i", buffer)[0]

		# Get frame data from other computer
		while len(recv_data) < payload_size:
			recv_data += s.recv(4096)
		packed_msg_size = recv_data[:payload_size]
		recv_data = recv_data[payload_size:]
		msg_size = struct.unpack("L", packed_msg_size)[0]
		while len(recv_data) < msg_size:
			recv_data += s.recv(4096)
		frame_data = recv_data[:msg_size]
		recv_data = recv_data[msg_size:]
		frame, width_to_send = pickle.loads(frame_data)
		# input(width_to_send)
		# size_to_send = (sts_x, sts_y)

		# input(timee)
		if time.time() - timestamp > 1 or drawer.is_alive():
			continue

		def _draw(f):
			# Draw other person
			box.draw(f)
			# cv2.imshow('Window', f)
			# cv2.waitKey(1)

		drawer = threading.Thread(target=_draw, args=[frame])
		drawer.start()

		time.time() - start


def send(s, capture, small_frame, nh=200):
	global width_to_send
	while True:
		# Send timestamp
		cur_time = int(time.time())
		b = struct.pack(">i", cur_time)
		s.sendall(b)
		capture.set(cv2.CAP_PROP_POS_FRAMES, 0)

		# Send frame to other computer
		_, send_data = capture.read()
		small_frame.draw(send_data)
		send_data = cv2.resize(send_data, (width_to_send, -1), fx=0.5, fy=0.5)
		tosend = pickle.dumps((
			send_data,
			term.width
		))
		s.sendall(struct.pack("L", len(tosend)) + tosend)
