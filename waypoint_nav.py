#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus
from geometry_msgs.msg import PoseWithCovarianceStamped

def set_initial_pose():
    pub = rospy.Publisher('/initialpose', PoseWithCovarianceStamped, queue_size=1)
    rospy.sleep(1)
    pose = PoseWithCovarianceStamped()
    pose.header.frame_id = "map"
    pose.header.stamp = rospy.Time.now()
    pose.pose.pose.position.x = -2.0
    pose.pose.pose.position.y = -0.5
    pose.pose.pose.orientation.w = 1.0
    pose.pose.covariance[0] = 0.25
    pose.pose.covariance[7] = 0.25
    pose.pose.covariance[35] = 0.06
    pub.publish(pose)
    rospy.loginfo("Baslangic pozisyonu ayarlandi: (0, 0)")
    rospy.sleep(2)

def send_goal(client, x, y, point_num):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0

    rospy.loginfo(f"Nokta {point_num} hedefleniyor: ({x}, {y})")
    client.send_goal(goal)

    finished = client.wait_for_result(rospy.Duration(90))

    if not finished:
        rospy.logwarn(f"Nokta {point_num} - timeout, sonraki noktaya geciliyor")
        client.cancel_goal()
    else:
        state = client.get_state()
        if state == GoalStatus.SUCCEEDED:
            rospy.loginfo(f"Nokta {point_num} - BASARILI")
        else:
            rospy.logwarn(f"Nokta {point_num} - basarisiz, state: {state}")

    rospy.sleep(1)

def main():
    rospy.init_node('waypoint_navigator')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("move_base bekleniyor...")
    client.wait_for_server()

    set_initial_pose()
    rospy.loginfo("Baslaniyor!")

    waypoints = [
        (0.491,  0.181),
        (1.377,  1.014),
        (2.809, -0.302),
        (1.754, -1.057),
        (0.515, -1.394),
    ]

    for i, (x, y) in enumerate(waypoints):
        send_goal(client, x, y, i + 1)

    rospy.loginfo("Tum noktalar tamamlandi!")

if __name__ == '__main__':
    main()
