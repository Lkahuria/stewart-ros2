#include <cmath>
#include <memory>
#include <string>
#include <vector>

#include "Eigen/Core"
#include "geometry_msgs/msg/twist.hpp"
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class IK : public rclcpp::Node
{
public:
  IK() : Node("ik")
  {
    z_home_ = 2.125;
    nominal_length_ = 1.9291198;

    b_ << -0.101,  0.800,  0.25, 1,
           0.101,  0.800,  0.25, 1,
           0.743, -0.313,  0.25, 1,
           0.642, -0.487,  0.25, 1,
          -0.643, -0.486,  0.25, 1,
          -0.744, -0.311,  0.25, 1;

    p_ << -0.642,  0.487, -0.05, 1,
           0.642,  0.487, -0.05, 1,
           0.743,  0.313, -0.05, 1,
           0.101, -0.800, -0.05, 1,
          -0.101, -0.800, -0.05, 1,
          -0.743,  0.313, -0.05, 1;

    for (int i = 0; i < 6; ++i) {
      std::string topic = "/stewart/piston" + std::to_string(i + 1) + "_cmd";
      pubs_.push_back(this->create_publisher<std_msgs::msg::Float64>(topic, 10));
    }

    sub_ = this->create_subscription<geometry_msgs::msg::Twist>(
      "/stewart/platform_twist", 10,
      std::bind(&IK::callback, this, std::placeholders::_1));
  }

private:
  void callback(const geometry_msgs::msg::Twist::SharedPtr msg)
  {
    float x = msg->linear.x;
    float y = msg->linear.y;
    float z = msg->linear.z;
    float roll = msg->angular.x;
    float pitch = msg->angular.y;
    float yaw = msg->angular.z;

    Eigen::Matrix<float, 4, 4> T = transformation_matrix(x, y, z + z_home_, roll, pitch, yaw);
    for (size_t i = 0; i < 6; ++i) {
      Eigen::Matrix<float, 4, 1> length = T * p_.row(i).transpose() - b_.row(i).transpose();
      std_msgs::msg::Float64 out;
      out.data = std::sqrt(std::pow(length(0), 2) + std::pow(length(1), 2) + std::pow(length(2), 2)) - nominal_length_;
      pubs_[i]->publish(out);
    }
  }

  Eigen::Matrix<float, 4, 4> transformation_matrix(float x, float y, float z, float r, float p, float yaw)
  {
    Eigen::Matrix<float, 4, 4> T;
    T << std::cos(yaw)*std::cos(p), -std::sin(yaw)*std::cos(r) + std::cos(yaw)*std::sin(p)*std::sin(r),  std::sin(yaw)*std::sin(r) + std::cos(yaw)*std::sin(p)*std::cos(r), x,
         std::sin(yaw)*std::cos(p),  std::cos(yaw)*std::cos(r) + std::sin(yaw)*std::sin(p)*std::sin(r), -std::cos(yaw)*std::sin(r) + std::sin(yaw)*std::sin(p)*std::cos(r), y,
                     -std::sin(p),                                            std::cos(p)*std::sin(r),                                            std::cos(p)*std::cos(r), z,
                                0,                                                                  0,                                                                  0, 1;
    return T;
  }

  float z_home_;
  float nominal_length_;
  Eigen::Matrix<float, 6, 4> b_, p_;
  std::vector<rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr> pubs_;
  rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr sub_;
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  rclcpp::spin(std::make_shared<IK>());
  rclcpp::shutdown();
  return 0;
}
