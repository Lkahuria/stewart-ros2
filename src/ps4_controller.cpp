#include <cmath>
#include <memory>

#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "sensor_msgs/msg/joy.hpp"

class Controller : public rclcpp::Node
{
public:
  Controller() : Node("ps4_controller")
  {
    pub_ = this->create_publisher<geometry_msgs::msg::Twist>("/stewart/platform_twist", 10);
    sub_ = this->create_subscription<sensor_msgs::msg::Joy>(
      "/joy", 10, std::bind(&Controller::callback, this, std::placeholders::_1));
  }

private:
  void callback(const sensor_msgs::msg::Joy::SharedPtr msg)
  {
    if (msg->axes.size() < 5 || msg->buttons.size() < 8) return;

    twist_msg_.linear.x = -msg->axes.at(0) / 2.0;
    twist_msg_.linear.y = msg->axes.at(1) / 2.0;
    twist_msg_.angular.x = -msg->axes.at(4) / 5.0;
    twist_msg_.angular.y = -msg->axes.at(3) / 5.0;

    if (msg->buttons.at(7) && twist_msg_.linear.z < 1.0)
      twist_msg_.linear.z += 0.01;
    else if (msg->buttons.at(6) && twist_msg_.linear.z > 0.0)
      twist_msg_.linear.z -= 0.01;

    if (msg->buttons.at(5) && twist_msg_.angular.z < M_PI / 2.0)
      twist_msg_.angular.z += 0.01;
    else if (msg->buttons.at(4) && twist_msg_.angular.z > -M_PI / 2.0)
      twist_msg_.angular.z -= 0.01;

    pub_->publish(twist_msg_);
  }

  geometry_msgs::msg::Twist twist_msg_;
  rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr pub_;
  rclcpp::Subscription<sensor_msgs::msg::Joy>::SharedPtr sub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<Controller>());
  rclcpp::shutdown();
  return 0;
}
