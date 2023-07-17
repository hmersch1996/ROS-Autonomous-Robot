import rospy
import random
from std_msgs.msg import String

def sensores():
    pub = rospy.Publisher('chatter',String,queue_size=10)
    rospy.init_node('sensores',anonymous=True)
    
    rate=rospy.Rate(1)
    
    
    while not rospy.is_shutdown():
        #Aqui se cargan los valores del magnetometro
        x=random.random()
        y=random.random()
        z=random.random()
        
        #Aqui se cargan los valores de los ultrasonicos
        u1=random.random()
        u2=random.random()
        u3=random.random()
        
        mensaje="hola"#str(x)+"/"+str(y)+"/"+str(z)+"/"+str(u1)+"/"+str(u2)+"/"+str(u3)
        rospy.loginfo(mensaje)
        pub.publish(mensaje)
        rate.sleep()

        
        
if __name__ == '__main__':
    try:
        sensores()
    except rospy.ROSInterruptException:
        pass
        
        
        