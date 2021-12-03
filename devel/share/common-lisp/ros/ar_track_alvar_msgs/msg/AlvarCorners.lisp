; Auto-generated. Do not edit!


(cl:in-package ar_track_alvar_msgs-msg)


;//! \htmlinclude AlvarCorners.msg.html

(cl:defclass <AlvarCorners> (roslisp-msg-protocol:ros-message)
  ((header
    :reader header
    :initarg :header
    :type std_msgs-msg:Header
    :initform (cl:make-instance 'std_msgs-msg:Header))
   (corners
    :reader corners
    :initarg :corners
    :type (cl:vector geometry_msgs-msg:Point)
   :initform (cl:make-array 4 :element-type 'geometry_msgs-msg:Point :initial-element (cl:make-instance 'geometry_msgs-msg:Point))))
)

(cl:defclass AlvarCorners (<AlvarCorners>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <AlvarCorners>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'AlvarCorners)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name ar_track_alvar_msgs-msg:<AlvarCorners> is deprecated: use ar_track_alvar_msgs-msg:AlvarCorners instead.")))

(cl:ensure-generic-function 'header-val :lambda-list '(m))
(cl:defmethod header-val ((m <AlvarCorners>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ar_track_alvar_msgs-msg:header-val is deprecated.  Use ar_track_alvar_msgs-msg:header instead.")
  (header m))

(cl:ensure-generic-function 'corners-val :lambda-list '(m))
(cl:defmethod corners-val ((m <AlvarCorners>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader ar_track_alvar_msgs-msg:corners-val is deprecated.  Use ar_track_alvar_msgs-msg:corners instead.")
  (corners m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <AlvarCorners>) ostream)
  "Serializes a message object of type '<AlvarCorners>"
  (roslisp-msg-protocol:serialize (cl:slot-value msg 'header) ostream)
  (cl:map cl:nil #'(cl:lambda (ele) (roslisp-msg-protocol:serialize ele ostream))
   (cl:slot-value msg 'corners))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <AlvarCorners>) istream)
  "Deserializes a message object of type '<AlvarCorners>"
  (roslisp-msg-protocol:deserialize (cl:slot-value msg 'header) istream)
  (cl:setf (cl:slot-value msg 'corners) (cl:make-array 4))
  (cl:let ((vals (cl:slot-value msg 'corners)))
    (cl:dotimes (i 4)
    (cl:setf (cl:aref vals i) (cl:make-instance 'geometry_msgs-msg:Point))
  (roslisp-msg-protocol:deserialize (cl:aref vals i) istream)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<AlvarCorners>)))
  "Returns string type for a message object of type '<AlvarCorners>"
  "ar_track_alvar_msgs/AlvarCorners")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'AlvarCorners)))
  "Returns string type for a message object of type 'AlvarCorners"
  "ar_track_alvar_msgs/AlvarCorners")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<AlvarCorners>)))
  "Returns md5sum for a message object of type '<AlvarCorners>"
  "c15398c181f13f4b18a3bb1244b338fa")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'AlvarCorners)))
  "Returns md5sum for a message object of type 'AlvarCorners"
  "c15398c181f13f4b18a3bb1244b338fa")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<AlvarCorners>)))
  "Returns full string definition for message of type '<AlvarCorners>"
  (cl:format cl:nil "Header header~%geometry_msgs/Point[4] corners~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'AlvarCorners)))
  "Returns full string definition for message of type 'AlvarCorners"
  (cl:format cl:nil "Header header~%geometry_msgs/Point[4] corners~%================================================================================~%MSG: std_msgs/Header~%# Standard metadata for higher-level stamped data types.~%# This is generally used to communicate timestamped data ~%# in a particular coordinate frame.~%# ~%# sequence ID: consecutively increasing ID ~%uint32 seq~%#Two-integer timestamp that is expressed as:~%# * stamp.sec: seconds (stamp_secs) since epoch (in Python the variable is called 'secs')~%# * stamp.nsec: nanoseconds since stamp_secs (in Python the variable is called 'nsecs')~%# time-handling sugar is provided by the client library~%time stamp~%#Frame this data is associated with~%# 0: no frame~%# 1: global frame~%string frame_id~%~%================================================================================~%MSG: geometry_msgs/Point~%# This contains the position of a point in free space~%float64 x~%float64 y~%float64 z~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <AlvarCorners>))
  (cl:+ 0
     (roslisp-msg-protocol:serialization-length (cl:slot-value msg 'header))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'corners) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ (roslisp-msg-protocol:serialization-length ele))))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <AlvarCorners>))
  "Converts a ROS message object to a list"
  (cl:list 'AlvarCorners
    (cl:cons ':header (header msg))
    (cl:cons ':corners (corners msg))
))
