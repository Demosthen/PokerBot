;; Auto-generated. Do not edit!


(when (boundp 'ar_track_alvar_msgs::AlvarCorners)
  (if (not (find-package "AR_TRACK_ALVAR_MSGS"))
    (make-package "AR_TRACK_ALVAR_MSGS"))
  (shadow 'AlvarCorners (find-package "AR_TRACK_ALVAR_MSGS")))
(unless (find-package "AR_TRACK_ALVAR_MSGS::ALVARCORNERS")
  (make-package "AR_TRACK_ALVAR_MSGS::ALVARCORNERS"))

(in-package "ROS")
;;//! \htmlinclude AlvarCorners.msg.html
(if (not (find-package "GEOMETRY_MSGS"))
  (ros::roseus-add-msgs "geometry_msgs"))
(if (not (find-package "STD_MSGS"))
  (ros::roseus-add-msgs "std_msgs"))


(defclass ar_track_alvar_msgs::AlvarCorners
  :super ros::object
  :slots (_header _corners ))

(defmethod ar_track_alvar_msgs::AlvarCorners
  (:init
   (&key
    ((:header __header) (instance std_msgs::Header :init))
    ((:corners __corners) (let (r) (dotimes (i 4) (push (instance geometry_msgs::Point :init) r)) r))
    )
   (send-super :init)
   (setq _header __header)
   (setq _corners __corners)
   self)
  (:header
   (&rest __header)
   (if (keywordp (car __header))
       (send* _header __header)
     (progn
       (if __header (setq _header (car __header)))
       _header)))
  (:corners
   (&rest __corners)
   (if (keywordp (car __corners))
       (send* _corners __corners)
     (progn
       (if __corners (setq _corners (car __corners)))
       _corners)))
  (:serialization-length
   ()
   (+
    ;; std_msgs/Header _header
    (send _header :serialization-length)
    ;; geometry_msgs/Point[4] _corners
    (apply #'+ (send-all _corners :serialization-length))
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; std_msgs/Header _header
       (send _header :serialize s)
     ;; geometry_msgs/Point[4] _corners
     (dolist (elem _corners)
       (send elem :serialize s)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; std_msgs/Header _header
     (send _header :deserialize buf ptr-) (incf ptr- (send _header :serialization-length))
   ;; geometry_msgs/Point[4] _corners
   (dotimes (i 4)
     (send (elt _corners i) :deserialize buf ptr-) (incf ptr- (send (elt _corners i) :serialization-length))
     )
   ;;
   self)
  )

(setf (get ar_track_alvar_msgs::AlvarCorners :md5sum-) "c15398c181f13f4b18a3bb1244b338fa")
(setf (get ar_track_alvar_msgs::AlvarCorners :datatype-) "ar_track_alvar_msgs/AlvarCorners")
(setf (get ar_track_alvar_msgs::AlvarCorners :definition-)
      "Header header
geometry_msgs/Point[4] corners
================================================================================
MSG: std_msgs/Header
# Standard metadata for higher-level stamped data types.
# This is generally used to communicate timestamped data 
# in a particular coordinate frame.
# 
# sequence ID: consecutively increasing ID 
uint32 seq
#Two-integer timestamp that is expressed as:
# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')
# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')
# time-handling sugar is provided by the client library
time stamp
#Frame this data is associated with
# 0: no frame
# 1: global frame
string frame_id

================================================================================
MSG: geometry_msgs/Point
# This contains the position of a point in free space
float64 x
float64 y
float64 z

")



(provide :ar_track_alvar_msgs/AlvarCorners "c15398c181f13f4b18a3bb1244b338fa")


