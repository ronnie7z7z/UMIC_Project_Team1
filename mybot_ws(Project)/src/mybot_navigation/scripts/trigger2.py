 #!/usr/bin/env python
import rospy
from std_msgs.msg import String
if __name__ == '__main__':
  with open("passwords.txt","r") as f:
    passwords=f.readlines()
  #detected = detect()
  #passwords = makeword(detected)
  #print(passwords)
  #NEW UNCERTAIN CODE BELOW
  #assuming that passwords is a singleton set of possible passcodes
  rospy.init_node('pwd_generator',anonymous=True)
  sub=rospy.Subscriber("/validity_of_detection",String,cb)
  pub=rospy.Publisher("possible_passcodes",String,queue_size=10)
  def cb(msg):
    if msg=='exit':
      print("exit sign detected, publishing passwords")
      for password in passwords:
        pub.publish(password)
        print(password)
      time.sleep(10.0)
      os.system(' rosnode kill --all ')

    else:
      print('exit not detected or incorrectly detected before maze')
