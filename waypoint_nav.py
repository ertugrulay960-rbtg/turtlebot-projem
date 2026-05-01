#!/usr/bin/env python3
import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from actionlib_msgs.msg import GoalStatus

def send_goal(client, x, y, point_num):
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y
    goal.target_pose.pose.orientation.w = 1.0  # yön önemli değil

    rospy.loginfo(f"Nokta {point_num} hedefleniyor: ({x}, {y})")
    client.send_goal(goal)

    finished = client.wait_for_result(rospy.Duration(60))

    if not finished:
        rospy.logwarn(f"Nokta {point_num} - timeout, iptal ediliyor")
        client.cancel_goal()
    else:
        state = client.get_state()
        if state == GoalStatus.SUCCEEDED:
            rospy.loginfo(f"Nokta {point_num} - BASARILI")
        else:
            rospy.logwarn(f"Nokta {point_num} - basarisiz, state: {state}")

    rospy.sleep(1)  # 3'ten 1'e indirdik

def main():
    rospy.init_node('waypoint_navigator')
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    rospy.loginfo("move_base bekleniyor...")
    client.wait_for_server()
    rospy.loginfo("Baslaniyor!")

    waypoints = [
        (0.5,  0.5),
        (1.0, -0.5),
        (-0.5, 1.0),
        (-2.0,  0.0),
        (-1.5, -1.5),
    ]

    for i, (x, y) in enumerate(waypoints):
        send_goal(client, x, y, i + 1)

    rospy.loginfo("Tum noktalar tamamlandi!")

if __name__ == '__main__':
    main()
